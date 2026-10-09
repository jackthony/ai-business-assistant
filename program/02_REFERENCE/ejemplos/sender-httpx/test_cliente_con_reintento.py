import asyncio

import httpx
import pytest
from cliente_con_reintento import cuerpo_texto, post_con_reintento

URL = "https://graph.example.test/123/messages"  # dominio falso: ningún test toca la red real


def correr(handler, **kwargs):
    async def _go():
        transporte = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transporte) as client:
            return await post_con_reintento(
                client, URL, json=cuerpo_texto("51900000000", "Hola"), **kwargs
            )

    return asyncio.run(_go())


def test_exito_devuelve_respuesta_y_latencia():
    respuesta, ms = correr(
        lambda req: httpx.Response(200, json={"messages": [{"id": "wamid.X"}]})
    )
    assert respuesta.status_code == 200
    assert ms >= 0


def test_arma_la_peticion_correctamente():
    vistas: list[httpx.Request] = []

    def handler(req: httpx.Request) -> httpx.Response:
        vistas.append(req)
        return httpx.Response(200, json={})

    correr(handler, headers={"Authorization": "Bearer token-falso"})
    req = vistas[0]
    assert req.method == "POST"
    assert str(req.url) == URL
    assert req.headers["authorization"] == "Bearer token-falso"
    assert b'"messaging_product":"whatsapp"' in req.content.replace(b" ", b"")


def test_reintenta_una_vez_si_falla_la_red():
    llamadas = {"n": 0}

    def handler(req: httpx.Request) -> httpx.Response:
        llamadas["n"] += 1
        if llamadas["n"] == 1:
            raise httpx.ConnectError("sin red", request=req)
        return httpx.Response(200, json={})

    respuesta, _ = correr(handler)
    assert respuesta.status_code == 200
    assert llamadas["n"] == 2


def test_si_siempre_falla_la_red_relanza_tras_agotar_reintentos():
    llamadas = {"n": 0}

    def handler(req: httpx.Request) -> httpx.Response:
        llamadas["n"] += 1
        raise httpx.ConnectError("sin red", request=req)

    with pytest.raises(httpx.ConnectError):
        correr(handler)
    assert llamadas["n"] == 2  # 1 intento + 1 reintento, no más


def test_un_4xx_no_se_reintenta():
    llamadas = {"n": 0}

    def handler(req: httpx.Request) -> httpx.Response:
        llamadas["n"] += 1
        return httpx.Response(400, json={"error": {"message": "mal formado"}})

    respuesta, _ = correr(handler)
    assert respuesta.status_code == 400
    assert llamadas["n"] == 1
