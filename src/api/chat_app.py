from collections.abc import Callable
from typing import Any

from fastapi import FastAPI

from channels.telegram import build_telegram_router
from channels.web import build_web_router
from channels.whatsapp.webhook import build_whatsapp_router


def create_chat_app(
    graph,
    telegram_secret: str | None = None,
    telegram_send: Callable[[str, str], Any] | None = None,
    tenant: str = "hola_mujer",
    *,
    whatsapp_verify_token: str | None = None,
    whatsapp_app_secret: str | None = None,
    whatsapp_send: Callable[[str, str], Any] | None = None,
) -> FastAPI:
    app = FastAPI(title="AI Business Assistant - API")

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    web_router = build_web_router(graph, tenant=tenant)
    app.include_router(web_router)

    if telegram_secret and telegram_send:
        telegram_router = build_telegram_router(
            graph=graph,
            secret=telegram_secret,
            send_func=telegram_send,
            tenant=tenant,
        )
        app.include_router(telegram_router)

    if whatsapp_verify_token and whatsapp_app_secret and whatsapp_send:
        app.include_router(
            build_whatsapp_router(
                graph=graph,
                verify_token=whatsapp_verify_token,
                app_secret=whatsapp_app_secret,
                send_func=whatsapp_send,
                tenant=tenant,
            )
        )

    return app
