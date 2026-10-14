"""Grafo mínimo: START -> echo -> END (contrato S05 D1)."""

from typing import Any

from langchain_core.messages import AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agents.state import AgentState


def echo_node(state: AgentState) -> dict[str, Any]:
    """Eco del último mensaje: devuelve solo lo que cambia."""
    texto = state["messages"][-1].content
    return {
        "messages": [AIMessage(content=f"eco: {texto}")],
        "intent": "eco",
        "status": "respondido",
    }


def build_graph() -> CompiledStateGraph:
    grafo = StateGraph(AgentState)
    grafo.add_node("echo", echo_node)  # type: ignore[call-overload]
    grafo.add_edge(START, "echo")
    grafo.add_edge("echo", END)
    return grafo.compile()
