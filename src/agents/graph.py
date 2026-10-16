"""Grafo del agente único (ADR-007), con la seguridad por delante de todo:

    START ─ congelado ─────────────► END            (el bot calla hasta que una persona lo libere)
          ─ salud / «una persona» ─► handoff ─► END (avisa, congela y responde con un puente)
          ─ agendar ───────────────► draft ─► commit (aprobación humana antes de escribir)
          ─ todo lo demás ─────────► info ─► END

Sin `booking`, el agente solo informa. Con `booking` hace falta un `checkpointer` para pausar.
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
from agents.handoff import is_frozen, make_handoff_node
from agents.info import last_user_text, make_info_node
from agents.ports import ChatModel, Notifier, Retriever
from agents.safety import classify
from agents.state import AgentState


def _route(booking: BookingDeps | None) -> Any:
    def route(state: AgentState) -> str:
        if is_frozen(state):
            return "frozen"
        if classify(last_user_text(state["messages"])) is not None:
            return "handoff"
        return "draft" if booking is not None and wants_booking(state) else "info"

    return route


def build_graph(
    retriever: Retriever,
    model: ChatModel,
    system_prompt: str,
    notifier: Notifier,
    booking: BookingDeps | None = None,
    checkpointer: BaseCheckpointSaver[Any] | None = None,
) -> CompiledStateGraph:
    if booking is not None and checkpointer is None:
        raise ValueError(
            "agendar con aprobación necesita un checkpointer (pausa y reanuda)"
        )
    grafo = StateGraph(AgentState)
    grafo.add_node("info", make_info_node(retriever, model, system_prompt))  # type: ignore[call-overload]
    grafo.add_node("handoff", make_handoff_node(notifier))  # type: ignore[call-overload]
    grafo.add_edge("handoff", END)
    destinos: dict[Hashable, str] = {
        "info": "info",
        "handoff": "handoff",
        "frozen": END,
    }
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
