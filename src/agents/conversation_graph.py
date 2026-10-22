"""Grafo de conversación: START → respond → END.

Recibe un ConversationService y devuelve un grafo compilado listo para invoke.
"""

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agents.conversation_service import ConversationService
from agents.respond_node import make_respond_node
from agents.state import AgentState


def build_conversation_graph(service: ConversationService) -> CompiledStateGraph:
    """Construye el grafo de conversación con un solo nodo respond."""
    grafo = StateGraph(AgentState)
    grafo.add_node("respond", make_respond_node(service))  # type: ignore[call-overload]
    grafo.add_edge(START, "respond")
    grafo.add_edge("respond", END)
    return grafo.compile()
