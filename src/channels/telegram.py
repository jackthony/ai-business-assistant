import hmac
from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request, status

from channels.contract import InboundEvent
from channels.dispatch import handle_inbound


def parse_update(
    raw: dict[str, Any], tenant: str = "hola_mujer"
) -> InboundEvent | None:
    message = raw.get("message")
    if not message:
        return None

    chat = message.get("chat", {})
    if chat.get("type") != "private":
        return None

    chat_id = chat.get("id")
    if chat_id is None:
        return None
    user_id = str(chat_id)

    if message.get("text"):
        return InboundEvent(
            tenant=tenant,
            user_id=user_id,
            type="text",
            content=message["text"],
            channel="telegram",
        )
    elif "voice" in message or "audio" in message:
        return InboundEvent(
            tenant=tenant,
            user_id=user_id,
            type="voice",
            content=None,
            channel="telegram",
        )
    elif any(
        k in message for k in ("photo", "document", "sticker", "video", "animation")
    ):
        return InboundEvent(
            tenant=tenant,
            user_id=user_id,
            type="media",
            content=None,
            channel="telegram",
        )

    return None


def build_telegram_router(
    graph,
    secret: str,
    send_func: Callable[[str, str], Any],
    tenant: str = "hola_mujer",
) -> APIRouter:
    if not secret or not secret.strip():
        raise ValueError("Telegram webhook secret must be configured")

    router = APIRouter(prefix="/telegram")

    @router.post("/webhook")
    async def telegram_webhook(
        request: Request,
        background_tasks: BackgroundTasks,
        x_telegram_bot_api_secret_token: str | None = Header(None),
    ):
        if not x_telegram_bot_api_secret_token or not hmac.compare_digest(
            x_telegram_bot_api_secret_token, secret
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid secret token"
            )

        body = await request.json()
        event = parse_update(body, tenant=tenant)
        if event:
            background_tasks.add_task(process_telegram_event, event, graph, send_func)

        return {"ok": True}

    return router


def process_telegram_event(
    event: InboundEvent, graph, send_func: Callable[[str, str], Any]
):
    reply = handle_inbound(event, graph=graph)
    if reply and reply.text:
        send_func(event.user_id, reply.text)
