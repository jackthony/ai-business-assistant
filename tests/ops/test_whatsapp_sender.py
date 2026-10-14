# tests/test_whatsapp_sender.py
import json

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
async def test_loguea_latencia(caplog):
    sender = make_sender(lambda r: httpx.Response(200, json={}))
    with caplog.at_level("INFO"):
        await sender.send_text("51999999999", "hola")
    assert any("latency_ms" in r.message for r in caplog.records)
