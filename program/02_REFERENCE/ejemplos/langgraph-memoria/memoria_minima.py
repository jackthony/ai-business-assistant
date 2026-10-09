"""Bloque 4 — grafo mínimo de LangGraph con memoria por thread_id en SQLite.

Sin LLM a propósito: el nodo solo hace eco. Aquí se aprende la MECÁNICA
(estado, reducer, checkpoint, thread_id); el modelo y el prompt llegan después.

En el bot real: thread_id = teléfono de la clienta (WhatsApp wa_id) -> cada
persona tiene su propio hilo y la memoria sobrevive a un reinicio del servidor.
"""

import operator
from typing import Annotated, Any, TypedDict

from langgraph.graph import END, START, StateGraph


class Estado(TypedDict):
    # ``operator.add`` es el *reducer*: en vez de reemplazar la lista, cada nodo
    # AÑADE a lo que ya había. Sin reducer, la memoria se sobrescribe.
    historial: Annotated[list[str], operator.add]


def responder(estado: Estado) -> dict[str, Any]:
    ultimo = estado["historial"][-1]
    return {"historial": [f"eco: {ultimo}"]}


def construir_grafo(checkpointer: Any) -> Any:
    grafo = StateGraph(Estado)
    # mypy 2.x + langgraph 1.x: ningún overload de add_node encaja (ni con TypedDict simple).
    # Es una limitación de tipos de la librería, no tu error: se silencia SOLO esta línea.
    grafo.add_node("responder", responder)  # type: ignore[call-overload]
    grafo.add_edge(START, "responder")
    grafo.add_edge("responder", END)
    return grafo.compile(checkpointer=checkpointer)


def config_de(telefono: str) -> dict[str, dict[str, str]]:
    """Cada teléfono = un hilo de conversación independiente."""
    return {"configurable": {"thread_id": telefono}}
