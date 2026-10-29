import asyncio

from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

from channels.contract import ID_PATTERN, MAX_CONTENT_CHARS, InboundEvent, OutboundReply
from channels.dispatch import handle_inbound


class ChatRequest(BaseModel):
    user_id: str
    text: str = Field(..., min_length=1, max_length=MAX_CONTENT_CHARS)

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        if not ID_PATTERN.match(v):
            raise ValueError(f"Invalid user_id format: {v}")
        return v


class ChatResponse(BaseModel):
    reply: str | None
    silent: bool
    first_response_ms: float


def build_web_router(graph, tenant: str = "hola_mujer") -> APIRouter:
    router = APIRouter()

    @router.post("/chat", response_model=ChatResponse)
    async def chat_endpoint(payload: ChatRequest):
        event = InboundEvent(
            tenant=tenant,
            user_id=payload.user_id,
            type="text",
            content=payload.text,
            channel="web",
        )

        # Ejecutar handle_inbound en un hilo separado para no bloquear el bucle async de FastAPI
        reply: OutboundReply | None = await asyncio.to_thread(
            handle_inbound, event, graph=graph
        )

        if reply is None:
            return ChatResponse(
                reply=None,
                silent=True,
                first_response_ms=0.0,
            )

        return ChatResponse(
            reply=reply.text,
            silent=False,
            first_response_ms=reply.channel_metadata.get("first_response_ms", 0.0),
        )

    return router
