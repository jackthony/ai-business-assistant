"""Adaptador de Ollama para el puerto LLMPort.

Es el único módulo de esta asignación que importa langchain_ollama.
"""

from langchain_ollama import ChatOllama

from agents.llm_port import ChatMessage


class OllamaAdapter:
    """Adapta ChatOllama a la interfaz LLMPort."""

    def __init__(self, model: str, base_url: str) -> None:
        self._cliente = ChatOllama(model=model, base_url=base_url)

    def generate(self, system: str, messages: list[ChatMessage]) -> str:
        mensajes = [{"role": m.role, "content": m.text} for m in messages]
        if system:
            mensajes.insert(0, {"role": "system", "content": system})
        respuesta = self._cliente.invoke(mensajes)
        return str(respuesta.content)
