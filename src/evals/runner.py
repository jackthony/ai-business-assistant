"""Ejecuta los escenarios contra el grafo real y resume resultado, contención y latencia."""

import re
import statistics
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from agents.booking import BookingDeps
from agents.config import load_tenant_config
from agents.graph import build_graph
from agents.handoff import FROZEN
from agents.ports import ChatModel, Retriever
from evals.scenarios import Expect, Scenario, Step
from rag.catalog import ServiceCatalog
from services.calendar_memory import InMemoryCalendar
from services.notifier_memory import InMemoryNotifier
from tools.agendar import make_agendar_tool
from tools.schedule import LIMA

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "hola_mujer"
# Reloj fijo (lunes): «mañana a las 4» significa lo mismo en cada corrida, con modelo guionado o real.
NOW = datetime(2026, 10, 19, 10, 0, tzinfo=LIMA)
PHONE = "51900000000"
OTHER_PHONE = "51911111111"


class CountingModel:
    """Cuenta las llamadas al modelo: la derivación a una persona no debe consultarlo."""

    def __init__(self, inner: ChatModel) -> None:
        self.inner = inner
        self.calls = 0

    def complete(self, system: str, user: str) -> str:
        self.calls += 1
        return self.inner.complete(system, user)


@dataclass
class Result:
    scenario: Scenario
    failures: list[str] = field(default_factory=list)
    latencies_ms: list[float] = field(default_factory=list)
    final_status: str | None = None
    model_calls: int = 0

    @property
    def passed(self) -> bool:
        return not self.failures

    @property
    def handed_off(self) -> bool:
        return self.final_status == FROZEN


class Run:
    """Un escenario en un grafo propio: calendario, avisos y checkpoints no se comparten."""

    def __init__(self, sc: Scenario, retriever: Retriever, inner: ChatModel) -> None:
        cfg = load_tenant_config("hola_mujer")
        catalog = ServiceCatalog.from_file(DATA_DIR / "servicios.json")
        self.calendar = InMemoryCalendar()
        self.notifier = InMemoryNotifier()
        self.model = CountingModel(inner)
        clock = lambda: NOW
        self.tool = make_agendar_tool(self.calendar, catalog, cfg.schedule, clock)
        deps = BookingDeps(
            catalog, self.calendar, cfg.schedule, self.tool, cfg.booking_prompt, clock
        )
        self.graph = build_graph(
            retriever, self.model, cfg.prompt, self.notifier, deps, InMemorySaver()
        )
        self.config: RunnableConfig = {"configurable": {"thread_id": f"eval-{sc.id}"}}
        self.draft: dict[str, Any] | None = None
        for slot in sc.busy_slots:
            self.calendar.book(
                f"ocupado-{slot}",
                OTHER_PHONE,
                "HM-FAC-001",
                datetime.fromisoformat(slot),
            )

    def say(self, text: str) -> dict[str, Any]:
        entrada: dict[str, Any] = {
            "messages": [HumanMessage(text)],
            "phone": PHONE,
            "tenant": "hola_mujer",
        }
        if not self.graph.get_state(self.config).values:
            entrada |= {"intent": None, "status": "nuevo"}
        return self._record(self.graph.invoke(entrada, self.config))

    def resume(self, approve: bool) -> dict[str, Any]:
        return self._record(
            self.graph.invoke(Command(resume={"approved": approve}), self.config)
        )

    def replay_tool(self) -> dict[str, Any]:
        if self.draft is None:
            return {"content": "sin borrador para repetir", "messages": []}
        args = {k: self.draft[k] for k in ("phone", "service_id", "start")}
        return {"content": str(self.tool.invoke(args)), "messages": []}

    def _record(self, out: dict[str, Any]) -> dict[str, Any]:
        for item in out.get("__interrupt__") or []:
            value = getattr(item, "value", {})
            if isinstance(value, dict) and "draft" in value:
                self.draft = value["draft"]
        return out


def _last(out: dict[str, Any]) -> tuple[str, list[str]]:
    if "content" in out:
        return str(out["content"]), []
    msg = out["messages"][-1]
    cites = [c["doc_id"] for c in msg.additional_kwargs.get("citations", [])]
    return str(msg.content), cites


def check(exp: Expect, out: dict[str, Any]) -> list[str]:
    content, cites = _last(out)
    bad: list[str] = []
    if exp.intent_in and out.get("intent") not in exp.intent_in:
        bad.append(f"intent={out.get('intent')!r}, esperado uno de {exp.intent_in}")
    if exp.status is not None and out.get("status") != exp.status:
        bad.append(f"status={out.get('status')!r}, esperado {exp.status!r}")
    if exp.interrupt is not None and bool(out.get("__interrupt__")) != exp.interrupt:
        bad.append(
            f"interrupt={bool(out.get('__interrupt__'))}, esperado {exp.interrupt}"
        )
    bad += [f"falta «{t}»" for t in exp.contains if t.lower() not in content.lower()]
    bad += [
        f"no debía decir «{t}»"
        for t in exp.not_contains
        if t.lower() in content.lower()
    ]
    bad += [f"coincide /{r}/" for r in exp.not_matches if re.search(r, content)]
    bad += [f"no cita {d}" for d in exp.cites if d not in cites]
    bad += [
        f"cita {c} (prohibido {p}*)"
        for p in exp.cites_not_prefix
        for c in cites
        if c.startswith(p)
    ]
    return bad


def _step(run: Run, step: Step) -> dict[str, Any]:
    if step.kind == "resume":
        return run.resume(step.approve)
    if step.kind == "replay_tool":
        return run.replay_tool()
    return run.say(step.say)


def run_scenario(sc: Scenario, retriever: Retriever, model: ChatModel) -> Result:
    run, result = Run(sc, retriever, model), Result(sc)
    last: dict[str, Any] = {}
    for n, step in enumerate(sc.steps, start=1):
        started = time.perf_counter()
        try:
            last = _step(run, step)
        except Exception as exc:  # noqa: BLE001 - un escenario roto no tumba la batería
            result.failures.append(f"paso {n}: {type(exc).__name__}: {exc}")
            break
        result.latencies_ms.append((time.perf_counter() - started) * 1000)
        result.failures += [f"paso {n}: {f}" for f in check(step.expect, last)]
    result.final_status = last.get("status")
    result.model_calls = run.model.calls
    if len(run.calendar.bookings()) != sc.bookings:
        result.failures.append(
            f"citas={len(run.calendar.bookings())}, esperado {sc.bookings}"
        )
    if len(run.notifier.sent()) != sc.alerts:
        result.failures.append(
            f"avisos={len(run.notifier.sent())}, esperado {sc.alerts}"
        )
    if result.handed_off != sc.handoff:
        result.failures.append(f"derivado={result.handed_off}, esperado {sc.handoff}")
    if sc.model_calls_max is not None and run.model.calls > sc.model_calls_max:
        result.failures.append(
            f"llamadas al modelo={run.model.calls}, máximo {sc.model_calls_max}"
        )
    return result


def run_suite(
    scenarios: list[Scenario],
    retriever: Retriever,
    model_for: Callable[[Scenario], ChatModel],
) -> list[Result]:
    return [run_scenario(sc, retriever, model_for(sc)) for sc in scenarios]


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, round(q * (len(ordered) - 1)))]


def render(results: list[Result], mode: str) -> str:
    ok = sum(r.passed for r in results)
    stay = [r for r in results if not r.scenario.handoff]
    derive = [r for r in results if r.scenario.handoff]
    lat = [x for r in results for x in r.latencies_ms]
    lines = [
        f"# Escenarios E2E del HITO 2 — modo {mode}",
        "",
        "| # | Escenario | Resultado | Pasos (ms) | Modelo | Detalle |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        pasos = " / ".join(f"{x:.0f}" for x in r.latencies_ms)
        detalle = "; ".join(r.failures) or "—"
        mark = "✅" if r.passed else "❌"
        lines.append(
            f"| {r.scenario.id} | {r.scenario.name} | {mark} | {pasos} | {r.model_calls} | {detalle} |"
        )
    lines += [
        "",
        f"- **Escenarios:** {ok}/{len(results)}",
        f"- **Contención** (resueltos sin derivar): {sum(not r.handed_off and r.passed for r in stay)}/{len(stay)}",
        f"- **Derivación correcta:** {sum(r.handed_off and r.passed for r in derive)}/{len(derive)}",
        f"- **Latencia por paso:** p50 {statistics.median(lat) if lat else 0:.0f} ms · p95 {percentile(lat, 0.95):.0f} ms",
    ]
    if mode == "guionado":
        lines.append(
            "- ⚠️ Modo guionado: valida la lógica del grafo, **no** mide al modelo real "
            "ni su latencia. La medición del hito se corre con `python -m evals.run --live`."
        )
    return "\n".join(lines) + "\n"
