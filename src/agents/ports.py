"""Puertos del núcleo: lo que el agente necesita del mundo, sin saber quién lo implementa."""

from typing import Protocol

from rag.store import Passage


class ChatModel(Protocol):
    def complete(self, system: str, user: str) -> str: ...


class Retriever(Protocol):
    def search(self, query: str, k: int = 4) -> list[Passage]: ...
