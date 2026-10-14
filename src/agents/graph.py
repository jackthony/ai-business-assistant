"""Grafo mínimo: START -> responder -> END.

El nodo eco es el andamio: aquí se conecta el modelo (S5 D2/D3) SIN tocar
el estado ni el thread_id. Núcleo sin canales ni HTTP (eso llega después).
"""

from typing import Any

from langgraph.graph import END, START, StateGraph

from agents.state import AgentState


def responder(state: AgentState) -> dict[str, Any]:
    """Nodo mínimo: eco del último mensaje.

    TODO (S5 D2): reemplazar el eco por la llamada al modelo
    (Ollama/DeepSeek local) usando configs/hola_mujer/prompt_v1.md.
    """
    ultimo = state["messages"][-1]
    # Con add_messages los mensajes son HumanMessage (no strings):
    # hay que leer .content o el eco imprime el objeto completo.
    texto = getattr(ultimo, "content", ultimo)
    return {"messages": [f"eco: {texto}"]}


def build_graph(checkpointer: Any) -> Any:
    grafo = StateGraph(AgentState)
    grafo.add_node("responder", responder)  # type: ignore[call-overload]
    grafo.add_edge(START, "responder")
    grafo.add_edge("responder", END)
    return grafo.compile(checkpointer=checkpointer)


def config_for(phone: str) -> dict[str, dict[str, str]]:
    """Cada teléfono = un hilo independiente."""
    return {"configurable": {"thread_id": phone}}
