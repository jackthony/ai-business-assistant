"""Estado del agente: TypedDict con 5 campos exactos (contrato S05 D1)."""

from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    phone: str
    tenant: str
    intent: str | None
    status: str
