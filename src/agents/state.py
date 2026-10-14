"""Estado del agente: lo que pasa entre nodos y lo que persiste el checkpointer."""

from typing import Annotated, Any, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    # ``add_messages`` es el reducer: los mensajes NUNCA se pisan,
    # siempre se acumulan = la memoria de la conversación.
    messages: Annotated[list[Any], add_messages]
    phone: str  # = thread_id (un hilo por clienta)
    tenant: str  # "hola_mujer" | "neuracode"
    intent: str | None  # intención detectada (S7)
    status: str  # "ok" | "waiting_human" | "done"
