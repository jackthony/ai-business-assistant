"""Derivación a una persona: avisa, congela el bot y responde con un puente sin diagnóstico.

El bot solo se congela si el aviso salió: nunca se le dice a la clienta «ya avisé» sin haber avisado.
Si el notificador falla, la excepción sube (el canal reintenta) y el estado no cambia.
Congelado = `status == "handoff_requested"`: el bot calla hasta que una persona lo libera.
"""

import hashlib
import re
from collections.abc import Callable
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph

from agents.info import last_user_text
from agents.ports import HandoffAlert, Notifier
from agents.safety import Reason, classify
from agents.state import AgentState

FROZEN = "handoff_requested"
EXCERPT_CHARS = 300
BRIDGE: dict[Reason, str] = {
    "clinical": (
        "Gracias por escribirnos 💛 Esa consulta la atiende una especialista de nuestro equipo, "
        "no yo. Ya le avisé para que te escriba. Lo que te cuente este chat no es una indicación "
        "médica."
    ),
    "human_requested": "¡Claro! 😊 Ya avisé a una persona del equipo para que te escriba.",
}
URGENT_LINE = (
    " Si sientes que es una emergencia, no esperes: acude ahora al servicio de emergencias "
    "más cercano."
)


def is_frozen(state: AgentState) -> bool:
    return state["status"] == FROZEN


def _trigger_id(state: AgentState, text: str) -> str:
    """Id del mensaje que dispara la derivación (en el grafo siempre existe; el hash es respaldo)."""
    last = next(
        (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)), None
    )
    return (last.id if last is not None and last.id else None) or hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()[:16]


def make_handoff_node(notifier: Notifier) -> Callable[[AgentState], dict[str, Any]]:
    def handoff_node(state: AgentState) -> dict[str, Any]:
        text = last_user_text(state["messages"])
        signal = classify(text)
        if signal is None:  # no debería pasar: el router ya lo clasificó
            raise RuntimeError("handoff sin señal de derivación")
        key = hashlib.sha256(
            f"{state['phone']}|{_trigger_id(state, text)}".encode()
        ).hexdigest()
        notifier.notify(
            HandoffAlert(
                key=key,
                phone=state["phone"],
                reason=signal.reason,
                urgent=signal.urgent,
                excerpt=re.sub(r"\s+", " ", text).strip()[:EXCERPT_CHARS],
            )
        )
        # En una urgencia lo primero que se lee es la emergencia, no el puente tranquilizador.
        reply = (
            f"{URGENT_LINE.strip()} {BRIDGE[signal.reason]}"
            if signal.urgent
            else BRIDGE[signal.reason]
        )
        return {
            "messages": [AIMessage(content=reply)],
            "intent": f"handoff_{signal.reason}",
            "status": FROZEN,
        }

    return handoff_node


def release_handoff(graph: CompiledStateGraph, config: RunnableConfig) -> None:
    """Una persona devuelve la conversación al bot."""
    graph.update_state(config, {"status": "active", "intent": None})
