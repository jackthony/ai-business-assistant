import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from agents.config import load_tenant_config
from agents.style import check_reply_style

CORPUS = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "conversaciones"
    / "sinteticas_v2.jsonl"
)

Runner = Callable[[str, str], str]


class StyleSummary(BaseModel):
    model_config = {"frozen": True}
    total: int
    compliant: int
    too_many_lines: int
    too_many_questions: int
    empty: int


def style_summary(replies: list[str]) -> StyleSummary:
    compliant = 0
    too_many_lines = 0
    too_many_questions = 0
    empty = 0

    for reply in replies:
        codes = check_reply_style(reply)
        if not codes:
            compliant += 1
        else:
            if "too_many_lines" in codes:
                too_many_lines += 1
            if "too_many_questions" in codes:
                too_many_questions += 1
            if "empty" in codes:
                empty += 1

    return StyleSummary(
        total=len(replies),
        compliant=compliant,
        too_many_lines=too_many_lines,
        too_many_questions=too_many_questions,
        empty=empty,
    )


def render_comparison(v1: StyleSummary, v2: StyleSummary) -> str:
    return (
        "| Métrica | v1 | v2 |\n"
        "|---|---|---|\n"
        f"| Respuestas | {v1.total} | {v2.total} |\n"
        f"| Cumplen el estilo | {v1.compliant} | {v2.compliant} |\n"
        f"| Más de 3 líneas | {v1.too_many_lines} | {v2.too_many_lines} |\n"
        f"| Más de 1 pregunta | {v1.too_many_questions} | {v2.too_many_questions} |\n"
        f"| Vacías | {v1.empty} | {v2.empty} |"
    )


def pick_conversations(path: Path, n: int = 10) -> list[str]:
    if not path.exists():
        return []

    lines = path.read_text(encoding="utf-8").splitlines()
    rows = []
    for line in lines:
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            if data.get("escenario") == "servicios" and data.get("rol") == "user":
                rows.append(data)
        except json.JSONDecodeError:
            continue

    rows_sorted = sorted(
        rows, key=lambda x: (x.get("conversacion_id", ""), x.get("turno", 0))
    )

    seleccionados = []
    vistos = set()

    for row in rows_sorted:
        texto = row.get("texto", "").strip()
        if not texto:
            continue

        palabras = texto.split()
        if len(palabras) < 3:
            continue

        t_lower = texto.lower()
        if t_lower.startswith(("hola", "buen", "[")):
            continue

        if t_lower in vistos:
            continue

        vistos.add(t_lower)
        seleccionados.append(texto)

        if len(seleccionados) == n:
            break

    return seleccionados


def make_live_runner() -> Runner:
    from agents.graph import build_graph
    from infrastructure.wiring import (
        DATA_DIR,
        ChromaStore,
        InMemoryNotifier,
        OllamaChat,
        OllamaEmbedder,
        load_documents,
    )

    tenant_dir = Path("configs") / "hola_mujer"
    embedder = OllamaEmbedder()
    # Usar tenant_dir.name ("hola_mujer") en lugar de la ruta completa con barras
    store = ChromaStore(embedder, tenant_dir.name)

    docs = load_documents(DATA_DIR)
    store.ingest(docs)

    model = OllamaChat()
    notifier = InMemoryNotifier()

    cache: dict[str, Any] = {}

    def live_runner(prompt: str, texto: str) -> str:
        if prompt not in cache:
            cache[prompt] = build_graph(
                retriever=store,
                model=model,
                system_prompt=prompt,
                notifier=notifier,
            )

        graph = cache[prompt]
        state = {
            "messages": [HumanMessage(content=texto)],
        }
        result = graph.invoke(state)
        messages = result.get("messages", [])
        if messages:
            return messages[-1].content
        return ""

    return live_runner


def main(argv: list[str] | None = None, runner: Runner | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compara prompts v1 y v2 usando un corpus sintético."
    )
    parser.add_argument(
        "--live", action="store_true", help="Ejecuta la evaluación real"
    )
    parser.add_argument(
        "--n", type=int, default=10, help="Número de conversaciones a evaluar"
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=CORPUS,
        help="Ruta al archivo corpus jsonl",
    )

    args = parser.parse_args(argv)

    if not args.live:
        sys.stderr.write(
            "Error: Se requiere --live para ejecutar la evaluación real.\n"
        )
        return 2

    cfg = load_tenant_config("hola_mujer")
    active_runner = runner or make_live_runner()

    preguntas = pick_conversations(args.corpus, args.n)

    respuestas_v1 = [active_runner(cfg.prompt, p) for p in preguntas]
    respuestas_v2 = [active_runner(cfg.prompt_v2, p) for p in preguntas]

    summary_v1 = style_summary(respuestas_v1)
    summary_v2 = style_summary(respuestas_v2)

    tabla = render_comparison(summary_v1, summary_v2)
    print(tabla)
    return 0


if __name__ == "__main__":
    sys.exit(main())
