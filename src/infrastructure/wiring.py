"""Raíz de composición: único lugar que conoce los adaptadores concretos."""

import os
from datetime import datetime
from pathlib import Path

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph

from agents.booking import BookingDeps
from agents.config import load_tenant_config
from agents.graph import build_graph
from models.ollama import OllamaChat, OllamaEmbedder
from rag.catalog import ServiceCatalog
from rag.documents import load_documents
from rag.store import ChromaStore
from services.calendar_memory import InMemoryCalendar
from tools.agendar import make_agendar_tool
from tools.schedule import LIMA

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "hola_mujer"


def build_default_graph(tenant: str = "hola_mujer") -> CompiledStateGraph:
    cfg = load_tenant_config(tenant)
    base = os.environ.get("OLLAMA_URL", "http://localhost:11434")
    store = ChromaStore(
        OllamaEmbedder(os.environ.get("OLLAMA_EMBED_MODEL", "bge-m3"), base),
        cfg.namespace,
        path=Path(os.environ.get("CHROMA_PATH", ".chroma")),
        max_distance=float(os.environ.get("RAG_MAX_DISTANCE", "0.6")),
    )
    store.ingest(load_documents(DATA_DIR))
    model = OllamaChat(os.environ.get("OLLAMA_CHAT_MODEL", "deepseek-r1:14b"), base)
    catalog = ServiceCatalog.from_file(DATA_DIR / "servicios.json")
    calendar = InMemoryCalendar()  # el CALENDAR_ID real sigue PENDING en 04_CONFIG
    clock = lambda: datetime.now(LIMA)
    booking = BookingDeps(
        catalog=catalog,
        calendar=calendar,
        schedule=cfg.schedule,
        tool=make_agendar_tool(calendar, catalog, cfg.schedule, clock),
        prompt=cfg.booking_prompt,
        clock=clock,
    )
    # InMemorySaver: la pausa vive mientras viva el proceso; SqliteSaver/Postgres llegan con ADR-005.
    return build_graph(store, model, cfg.prompt, booking, InMemorySaver())
