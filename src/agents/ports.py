"""Puertos del núcleo: lo que el agente necesita del mundo, sin saber quién lo implementa."""

from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict

from rag.store import Passage


class ChatModel(Protocol):
    def complete(self, system: str, user: str) -> str: ...


class Retriever(Protocol):
    def search(self, query: str, k: int = 4) -> list[Passage]: ...


class HandoffAlert(BaseModel):
    """Aviso a una persona del equipo. `key` identifica el motivo (mensaje que lo disparó)."""

    model_config = ConfigDict(frozen=True)

    key: str
    phone: str
    reason: Literal["clinical", "human_requested"]
    urgent: bool
    excerpt: str


class Notifier(Protocol):
    def notify(self, alert: HandoffAlert) -> None:
        """Avisa a una persona. Idempotente por `alert.key`; si no puede avisar, lanza."""
        ...
