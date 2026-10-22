from typing import Literal, Protocol

from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    text: str


class LLMPort(Protocol):
    def generate(self, system: str, messages: list[ChatMessage]) -> str: ...
