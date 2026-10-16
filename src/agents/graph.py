"""Grafo del agente único: START -> info -> END. Las siguientes capas (agendar, safety/handoff)
se agregan como nodos del MISMO grafo (ADR-007)."""

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agents.info import make_info_node
from agents.ports import ChatModel, Retriever
from agents.state import AgentState


def build_graph(
    retriever: Retriever, model: ChatModel, system_prompt: str
) -> CompiledStateGraph:
    grafo = StateGraph(AgentState)
    grafo.add_node("info", make_info_node(retriever, model, system_prompt))  # type: ignore[call-overload]
    grafo.add_edge(START, "info")
    grafo.add_edge("info", END)
    return grafo.compile()
