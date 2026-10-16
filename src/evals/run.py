"""Corre los 12 escenarios del HITO 2 y imprime la tabla.

python -m evals.run            # modelo guionado: valida la lógica del grafo (CI, sin red)
python -m evals.run --live     # DeepSeek local por Ollama: la medición real del hito (en la M5)
"""

import argparse
import os
import sys
import uuid
from pathlib import Path

from agents.ports import ChatModel
from evals.runner import DATA_DIR, render, run_suite
from evals.scenarios import SCENARIOS, Scenario
from evals.scripted import ScriptedModel
from rag.documents import load_documents
from rag.embedding import Embedder, LexicalEmbedder
from rag.store import ChromaStore

SCRIPTED_MAX_DISTANCE = 0.9


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="evals.run")
    parser.add_argument(
        "--live", action="store_true", help="usar Ollama (modelo y embeddings reales)"
    )
    parser.add_argument("--out", type=Path, help="guardar la tabla en este archivo")
    args = parser.parse_args(argv)

    embedder: Embedder
    model_for: object
    if args.live:
        from models.ollama import OllamaChat, OllamaEmbedder

        base = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        embedder = OllamaEmbedder(os.environ.get("OLLAMA_EMBED_MODEL", "bge-m3"), base)
        chat = OllamaChat(os.environ.get("OLLAMA_CHAT_MODEL", "deepseek-r1:14b"), base)

        def live_model(_: Scenario) -> ChatModel:
            return chat

        model_for = live_model
    else:
        embedder = LexicalEmbedder()

        def scripted_model(sc: Scenario) -> ChatModel:
            return ScriptedModel(*sc.script)

        model_for = scripted_model
    # El embedder léxico solo cuenta palabras: con textos largos sus distancias son altas, así que en
    # modo guionado el umbral se relaja. Con el modelo real manda RAG_MAX_DISTANCE (a calibrar aquí).
    default = "0.6" if args.live else str(SCRIPTED_MAX_DISTANCE)
    store = ChromaStore(
        embedder,
        f"evals-{uuid.uuid4().hex[:8]}",
        max_distance=float(os.environ.get("RAG_MAX_DISTANCE", default)),
    )
    store.ingest(load_documents(DATA_DIR))
    results = run_suite(SCENARIOS, store, model_for)  # type: ignore[arg-type]
    table = render(results, "real (Ollama)" if args.live else "guionado")
    print(table)
    if args.out:
        args.out.write_text(table, encoding="utf-8")
    return 0 if all(r.passed for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
