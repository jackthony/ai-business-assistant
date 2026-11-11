import asyncio
import hashlib
import hmac
import json
from collections.abc import Callable
from inspect import isawaitable
from typing import Any, Literal

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
from langgraph.graph.state import CompiledStateGraph

from channels.contract import InboundEvent
from channels.dispatch import handle_inbound

MEDIA_TYPES = {"image", "video", "document", "sticker"}


def verify_challenge(
    mode: str | None, token: str | None, challenge: str | None, verify_token: str
) -> str | None:
    if mode != "subscribe" or not verify_token or token is None:
        return None
    if not hmac.compare_digest(token.encode(), verify_token.encode()):
        return None
    return challenge


def signature_is_valid(body: bytes, header: str | None, app_secret: str) -> bool:
    if not header or not app_secret or not header.startswith("sha256="):
        return False
    digest = hmac.new(app_secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={digest}".encode(), header.encode())


def parse_payload(
    payload: dict[str, Any], tenant: str = "hola_mujer"
) -> InboundEvent | None:
    try:
        message = payload["entry"][0]["changes"][0]["value"]["messages"][0]
        user_id = message["from"]
        kind = message["type"]
        if kind == "text":
            content = message["text"]["body"]
            if not isinstance(content, str):
                return None
            return InboundEvent(
                tenant=tenant,
                user_id=user_id,
                type="text",
                content=content,
                channel="whatsapp",
            )
        event_type: Literal["media", "voice"]
        if kind == "audio":
            event_type = "voice"
        elif kind in MEDIA_TYPES:
            event_type = "media"
        else:
            return None
        return InboundEvent(
            tenant=tenant,
            user_id=user_id,
            type=event_type,
            content=None,
            channel="whatsapp",
        )
    except (KeyError, IndexError, TypeError, ValueError):
        return None


async def process_whatsapp_event(
    event: InboundEvent, graph: CompiledStateGraph, send_func: Callable[[str, str], Any]
) -> None:
    reply = await asyncio.to_thread(handle_inbound, event, graph=graph)
    if reply and reply.text:
        send_result = await asyncio.to_thread(send_func, event.user_id, reply.text)
        if isawaitable(send_result):
            await send_result


def build_whatsapp_router(
    graph: CompiledStateGraph,
    verify_token: str,
    app_secret: str,
    send_func: Callable[[str, str], Any],
    tenant: str = "hola_mujer",
) -> APIRouter:
    if not verify_token.strip() or not app_secret.strip():
        raise ValueError("WhatsApp verify token and app secret must be configured")

    router = APIRouter(prefix="/whatsapp")

    @router.get("/webhook")
    async def whatsapp_verify(
        mode: str | None = Query(None, alias="hub.mode"),
        token: str | None = Query(None, alias="hub.verify_token"),
        challenge: str | None = Query(None, alias="hub.challenge"),
    ) -> PlainTextResponse:
        answer = verify_challenge(mode, token, challenge, verify_token)
        if answer is None:
            raise HTTPException(status_code=403, detail="Verification failed")
        return PlainTextResponse(answer)

    @router.post("/webhook")
    async def whatsapp_webhook(
        request: Request,
        background_tasks: BackgroundTasks,
        x_hub_signature_256: str | None = Header(None),
    ) -> dict[str, bool]:
        body = await request.body()
        if not signature_is_valid(body, x_hub_signature_256, app_secret):
            raise HTTPException(status_code=403, detail="Invalid signature")
        try:
            payload = json.loads(body)
        except ValueError:
            return {"ok": True}
        event = (
            parse_payload(payload, tenant=tenant) if isinstance(payload, dict) else None
        )
        if event:
            background_tasks.add_task(process_whatsapp_event, event, graph, send_func)
        return {"ok": True}

    return router
