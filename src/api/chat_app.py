from collections.abc import Callable
from typing import Any

from fastapi import FastAPI

from channels.telegram import build_telegram_router
from channels.web import build_web_router


def create_chat_app(
    graph,
    telegram_secret: str | None = None,
    telegram_send: Callable[[str, str], Any] | None = None,
    tenant: str = "hola_mujer",
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

    return app
