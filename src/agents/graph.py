"""Grafo del agente único (ADR-007): router → info | booking(draft → commit con aprobación).

Las siguientes capas (safety/handoff) se agregan como nodos del MISMO grafo. Sin `booking`, el
agente solo informa (capa 1). Con `booking` hace falta un `checkpointer` para pausar y reanudar.
"""

from collections.abc import Hashable
from typing import Any

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agents.booking import (
    BookingDeps,
    after_draft,
    make_commit_node,
    make_draft_node,
    wants_booking,
)
from agents.info import make_info_node
from agents.ports import ChatModel, Retriever
from agents.state import AgentState


def _route(booking: BookingDeps | None) -> Any:
    def route(state: AgentState) -> str:
        return "draft" if booking is not None and wants_booking(state) else "info"

    return route


def build_graph(
    retriever: Retriever,
    model: ChatModel,
    system_prompt: str,
    booking: BookingDeps | None = None,
    checkpointer: BaseCheckpointSaver[Any] | None = None,
) -> CompiledStateGraph:
    if booking is not None and checkpointer is None:
        raise ValueError(
            "agendar con aprobación necesita un checkpointer (pausa y reanuda)"
        )
    grafo = StateGraph(AgentState)
    grafo.add_node("info", make_info_node(retriever, model, system_prompt))  # type: ignore[call-overload]
    destinos: dict[Hashable, str] = {"info": "info"}
    if booking:
        destinos["draft"] = "draft"
    grafo.add_conditional_edges(START, _route(booking), destinos)
    grafo.add_edge("info", END)
    if booking is not None:
        grafo.add_node("draft", make_draft_node(model, booking))  # type: ignore[call-overload]
        grafo.add_node("commit", make_commit_node(booking))  # type: ignore[call-overload]
        grafo.add_conditional_edges(
            "draft", after_draft, {"commit": "commit", "end": END}
        )
        grafo.add_edge("commit", END)
    return grafo.compile(checkpointer=checkpointer)
