# tests/test_whatsapp_sender.py
import json
import time

import httpx
import pytest

from channels.whatsapp.sender import WhatsAppSender

PHONE_ID = "123456789"
TOKEN = "token-falso"


def make_sender(handler):
    transport = httpx.MockTransport(handler)
    return WhatsAppSender(
        phone_number_id=PHONE_ID,
        access_token=TOKEN,
        transport=transport,
    )


@pytest.mark.asyncio
async def test_send_text_arma_bien_el_request():
    capturado = {}

    def handler(request: httpx.Request) -> httpx.Response:
        capturado["url"] = str(request.url)
        capturado["auth"] = request.headers["Authorization"]
        capturado["body"] = json.loads(request.content)
        return httpx.Response(200, json={"messages": [{"id": "wamid.X"}]})

    sender = make_sender(handler)
    resp = await sender.send_text("51999999999", "hola")

    assert capturado["url"].endswith(f"/{PHONE_ID}/messages")
    assert capturado["auth"] == f"Bearer {TOKEN}"
    assert capturado["body"]["to"] == "51999999999"
    assert capturado["body"]["type"] == "text"
    assert capturado["body"]["text"]["body"] == "hola"
    assert resp["messages"][0]["id"] == "wamid.X"


@pytest.mark.asyncio
async def test_reintenta_una_vez_ante_error_de_red():
    llamadas = 0

    def handler(request):
        nonlocal llamadas
        llamadas += 1
        if llamadas == 1:
            raise httpx.ConnectError("caída", request=request)
        return httpx.Response(200, json={"messages": [{"id": "wamid.Y"}]})

    sender = make_sender(handler)
    await sender.send_text("51999999999", "hola")
    assert llamadas == 2


@pytest.mark.asyncio
async def test_no_reintenta_ante_error_401_meta():
    """Meta devuelve 401: falla cerrado en el primer intento, sin reintento."""
    llamadas = 0

    def handler(request):
        nonlocal llamadas
        llamadas += 1
        return httpx.Response(401, json={"error": {"message": "invalid token"}})

    sender = make_sender(handler)
    with pytest.raises(httpx.HTTPStatusError):
        await sender.send_text("51999999999", "hola")
    assert llamadas == 1


@pytest.mark.asyncio
async def test_loguea_latencia(caplog):
    sender = make_sender(lambda r: httpx.Response(200, json={}))
    with caplog.at_level("INFO"):
        await sender.send_text("51999999999", "hola")
    assert any("latency_ms" in r.message for r in caplog.records)


@pytest.mark.asyncio
async def test_loguea_tiempo_primera_respuesta_cuando_recibido(caplog):
    """Si se conoce el timestamp de entrada (webhook), se loguea first_response_ms."""
    t0 = time.perf_counter() - 0.250  # el webhook llegó hace 250 ms
    sender = make_sender(lambda r: httpx.Response(200, json={}))
    with caplog.at_level("INFO"):
        await sender.send_text("51999999999", "hola", received_at=t0)
    assert any("first_response_ms" in r.message for r in caplog.records)
