from typing import Literal

from pydantic import BaseModel

from agents.llm_port import ChatMessage
from agents.verification import verify_response


class ConversationResult(BaseModel):
    status: Literal["respondido", "revision_humana"]
    text: str | None
    reasons: list[str]


class ConversationService:
    def __init__(self, llm, system: str) -> None:
        self.llm = llm
        self.system = system

    def respond(self, messages: list[ChatMessage]) -> ConversationResult:
        texto = self.llm.generate(self.system, messages)
        resultado_verificacion = verify_response(texto)

        if resultado_verificacion.ok:
            return ConversationResult(
                status="respondido",
                text=texto,
                reasons=[],
            )
        return ConversationResult(
            status="revision_humana",
            text=None,
            reasons=resultado_verificacion.reasons,
        )
