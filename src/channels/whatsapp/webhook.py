import asyncio
import hashlib
import hmac
import json
import logging
from collections.abc import Callable, Iterator
from inspect import isawaitable
from typing import Any, Literal

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
from langgraph.graph.state import CompiledStateGraph

from channels.contract import InboundEvent
from channels.dispatch import handle_inbound

MEDIA_TYPES = {"image", "video", "document", "sticker"}
logger = logging.getLogger(__name__)


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
    except (KeyError, IndexError, TypeError):
        return None
    return _parse_message(message, tenant)


def _parse_message(message: dict[str, Any], tenant: str) -> InboundEvent | None:
    try:
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


def _object_items(container: object, field: str) -> Iterator[dict[str, Any]]:
    values = container.get(field) if isinstance(container, dict) else None
    if isinstance(values, list):
        yield from (value for value in values if isinstance(value, dict))


def _parse_batch(payload: object, tenant: str) -> list[InboundEvent]:
    events = []
    for entry in _object_items(payload, "entry"):
        for change in _object_items(entry, "changes"):
            for message in _object_items(change.get("value"), "messages"):
                event = _parse_message(message, tenant)
                if event is not None:
                    events.append(event)
    return events


async def process_whatsapp_event(
    event: InboundEvent, graph: CompiledStateGraph, send_func: Callable[[str, str], Any]
) -> None:
    reply = await asyncio.to_thread(handle_inbound, event, graph=graph)
    if reply and reply.text:
        send_result = await asyncio.to_thread(send_func, event.user_id, reply.text)
        if isawaitable(send_result):
            await send_result


async def _process_batch(
    events: list[InboundEvent],
    graph: CompiledStateGraph,
    send_func: Callable[[str, str], Any],
) -> None:
    for event in events:
        try:
            await process_whatsapp_event(event, graph, send_func)
        # A provider failure belongs to this message. Do not log its payload.
        except Exception as exc:  # noqa: BLE001
            logger.error("whatsapp_event_failed error_type=%s", type(exc).__name__)


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
        events = _parse_batch(payload, tenant)
        if events:
            background_tasks.add_task(_process_batch, events, graph, send_func)
        return {"ok": True}

    return router
