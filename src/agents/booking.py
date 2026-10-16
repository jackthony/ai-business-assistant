"""Agendar dentro del agente único: extraer → validar (código) → aprobación humana → escribir.

`draft` no tiene efectos: solo propone. `commit` pide la aprobación con `interrupt()` y recién
después llama a la herramienta N2; como todo lo anterior al `interrupt` es puro, reanudar un
checkpoint no repite nada, y si aun así se repite, la clave de idempotencia evita la cita doble
(ADR-009).
"""

import datetime as dt
import json
import re
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import StructuredTool
from langgraph.types import interrupt
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

from agents.info import last_user_text
from agents.ports import ChatModel
from agents.state import AgentState
from rag.catalog import ServiceCatalog
from tools.agendar import AgendarInput, check_request
from tools.ports import Calendar
from tools.schedule import LIMA, Schedule

DAYS = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")
INTENT_RE = re.compile(
    r"\b(agend\w*|reserv\w*|separ\w*|turno|(?:quiero|quisiera|necesito|puedo|sacar|pedir|hacer|"
    r"programar)\s+(?:una\s+|mi\s+)?cita)\b"
)
HISTORY = 6  # mensajes de la clienta que se leen para completar los datos de la cita

ASK_SERVICE = "¡Claro! 😊 ¿Qué servicio te gustaría agendar?"
FAIL = "No pude dejar lista tu cita 🙏. Una persona del equipo de Hola Mujer te ayuda enseguida."
REJECTED = (
    "Por ahora no pudimos confirmar ese horario 🙏. Una persona del equipo te escribirá para "
    "coordinar otro."
)


class Extraction(BaseModel):
    """Lo que el LLM pudo sacar de la conversación. Todo opcional: lo dudoso queda en None."""

    model_config = ConfigDict(extra="ignore")

    service: str | None = None
    date: dt.date | None = None
    time: dt.time | None = None

    @field_validator("service", "date", "time", mode="before")
    @classmethod
    def _tolerant(cls, v: Any, info: Any) -> Any:
        if v in ("", "null", None):
            return None
        try:
            if info.field_name == "date":
                return dt.date.fromisoformat(str(v))
            if info.field_name == "time":
                return dt.time.fromisoformat(str(v))
        except ValueError:
            return None
        return str(v)


class Approval(BaseModel):
    model_config = ConfigDict(extra="ignore")

    approved: bool = False
    reason: str | None = None


@dataclass(frozen=True)
class BookingDeps:
    catalog: ServiceCatalog
    calendar: Calendar
    schedule: Schedule
    tool: StructuredTool
    prompt: str
    clock: Callable[[], datetime]


def _plain(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def wants_booking(state: AgentState) -> bool:
    """Router determinista: sigue en agendar si falta un dato o si la clienta lo pide."""
    if state["intent"] == "booking_needs_info":
        return True
    last = last_user_text(state["messages"])
    return bool(INTENT_RE.search(_plain(last)))


def parse_extraction(raw: str) -> Extraction:
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
    try:
        return Extraction.model_validate(json.loads(text))
    except (ValueError, ValidationError):
        return Extraction()


def fmt_slot(start: datetime) -> str:
    local = start.astimezone(LIMA)
    hour12 = local.hour % 12 or 12
    ampm = "am" if local.hour < 12 else "pm"
    return f"{DAYS[local.weekday()]} {local:%d/%m} a las {hour12}:{local:%M} {ampm}"


def _reply(
    text: str, intent: str, status: str = "active", **extra: Any
) -> dict[str, Any]:
    return {
        "messages": [AIMessage(content=text, additional_kwargs=extra)],
        "intent": intent,
        "status": status,
    }


def _alternatives(deps: BookingDeps, now: datetime, n: int = 3) -> list[datetime]:
    free = (s for s in deps.schedule.upcoming_starts(now) if deps.calendar.is_free(s))
    return [s for _, s in zip(range(n), free, strict=False)]


def _offer(deps: BookingDeps, now: datetime, intro: str) -> dict[str, Any]:
    opciones = _alternatives(deps, now)
    if not opciones:
        return _reply(FAIL, "booking_failed")
    lista = "\n".join(f"• {fmt_slot(s)}" for s in opciones)
    return _reply(
        f"{intro} Tengo libre:\n{lista}\n¿Cuál te acomoda?", "booking_needs_info"
    )


def _extraction_prompt(texts: list[str], now: datetime) -> str:
    local = now.astimezone(LIMA)
    hoy = f"{DAYS[local.weekday()]} {local:%Y-%m-%d} {local:%H:%M}"
    cuerpo = "\n".join(t.replace("<", " ").replace(">", " ") for t in texts)
    return f"Ahora (Lima): {hoy}\n<conversacion>\n{cuerpo}\n</conversacion>"


def make_draft_node(
    model: ChatModel, deps: BookingDeps
) -> Callable[[AgentState], dict[str, Any]]:
    def draft_node(state: AgentState) -> dict[str, Any]:
        now = deps.clock()
        humans = [
            str(m.content) for m in state["messages"] if isinstance(m, HumanMessage)
        ]
        raw = model.complete(deps.prompt, _extraction_prompt(humans[-HISTORY:], now))
        ex = parse_extraction(raw)
        matches = deps.catalog.find(ex.service) if ex.service else []
        if not matches:
            return _reply(ASK_SERVICE, "booking_needs_info")
        if len(matches) > 1:
            nombres = "\n".join(f"• {s.nombre}" for s in matches[:4])
            return _reply(
                f"¿Cuál de estos servicios quieres?\n{nombres}", "booking_needs_info"
            )
        service = matches[0]
        if ex.date is None or ex.time is None:
            a, c = deps.schedule.open, deps.schedule.close
            return _reply(
                f"¿Qué día y a qué hora te gustaría tu cita de *{service.nombre}*? "
                f"Atendemos de {a:%H:%M} a {c:%H:%M}.",
                "booking_needs_info",
            )
        start = datetime.combine(ex.date, ex.time, tzinfo=LIMA)
        try:
            inp = AgendarInput(
                phone=state["phone"], service_id=service.service_id, start=start
            )
        except ValidationError:
            return _reply(FAIL, "booking_failed")
        problem = check_request(inp, deps.catalog, deps.schedule, deps.calendar, now)
        if problem == "service_unknown":
            return _reply(FAIL, "booking_failed")
        if problem:
            motivo = (
                "Ese horario ya está ocupado."
                if problem == "slot_busy"
                else "Ese horario no está disponible."
            )
            return _offer(deps, now, motivo)
        draft = {
            "service_id": service.service_id,
            "service_label": service.nombre,
            "phone": state["phone"],
            "start": start.isoformat(),
        }
        return _reply(
            f"Perfecto 🙌 Anoté tu solicitud de *{service.nombre}* para el {fmt_slot(start)}. "
            "Una persona del equipo la confirma y te escribimos apenas esté lista.",
            "booking_pending",
            "pending_approval",
            booking_draft=draft,
        )

    return draft_node


def make_commit_node(deps: BookingDeps) -> Callable[[AgentState], dict[str, Any]]:
    def commit_node(state: AgentState) -> dict[str, Any]:
        draft = state["messages"][-1].additional_kwargs.get("booking_draft")
        if not draft:
            return _reply(FAIL, "booking_failed")
        # Todo lo anterior es puro; desde aquí el flujo se detiene hasta que un humano responda.
        answer = interrupt({"type": "booking_approval", "draft": draft})
        try:
            decision = Approval.model_validate(answer)
        except ValidationError:
            decision = Approval()  # respuesta ilegible = no aprobada (falla cerrada)
        if not decision.approved:
            return _reply(REJECTED, "booking_rejected")
        result = deps.tool.invoke(
            {
                "phone": draft["phone"],
                "service_id": draft["service_id"],
                "start": draft["start"],
            }
        )
        if result["status"] in ("created", "already_booked"):
            start = datetime.fromisoformat(draft["start"])
            return _reply(
                f"¡Listo! 🎉 Tu cita de *{draft['service_label']}* quedó confirmada para el "
                f"{fmt_slot(start)}.",
                "booking_confirmed",
            )
        if result["reason"] == "slot_busy":
            return _offer(
                deps, deps.clock(), "Ese horario se ocupó mientras confirmábamos."
            )
        return _reply(FAIL, "booking_failed")

    return commit_node


def after_draft(state: AgentState) -> str:
    return "commit" if state["status"] == "pending_approval" else "end"
