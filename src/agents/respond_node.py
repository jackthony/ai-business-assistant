"""Nodo respond del grafo de conversación.

Convierte los mensajes del estado a ChatMessage, llama al servicio y
devuelve la actualización del estado.
"""

from collections.abc import Callable, Mapping
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage

from agents.conversation_service import ConversationService
from agents.llm_port import ChatMessage


def make_respond_node(
    service: ConversationService,
) -> Callable[[Mapping[str, Any]], dict[str, Any]]:
    """Crea el nodo respond que usa el servicio de conversación."""

    def respond_node(state: Mapping[str, Any]) -> dict[str, Any]:
        mensajes: list[ChatMessage] = []
        for mensaje in state["messages"]:
            if isinstance(mensaje, HumanMessage):
                contenido = mensaje.content if isinstance(mensaje.content, str) else ""
                mensajes.append(ChatMessage(role="user", text=contenido))
            elif isinstance(mensaje, AIMessage):
                contenido = mensaje.content if isinstance(mensaje.content, str) else ""
                mensajes.append(ChatMessage(role="assistant", text=contenido))

        resultado = service.respond(mensajes)

        if resultado.status == "respondido":
            return {
                "messages": [AIMessage(content=resultado.text or "")],
                "status": "respondido",
            }

        return {"status": "revision_humana"}

    return respond_node
