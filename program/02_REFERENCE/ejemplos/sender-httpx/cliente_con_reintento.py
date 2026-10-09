"""Bloque 3 — POST async con 1 reintento ante fallo de RED y medición de latencia.

Regla: se reintenta solo cuando NO llegó respuesta (timeout, conexión caída).
Un 4xx significa "tu petición está mal": reintentar solo repite el error y, en
mensajería, puede duplicar envíos. Un 5xx se devuelve tal cual para que el
llamador decida (no se reintenta aquí a propósito: decisión de tu Issue).
"""

import time
from typing import Any

import httpx


async def post_con_reintento(
    client: httpx.AsyncClient,
    url: str,
    *,
    json: dict[str, Any],
    headers: dict[str, str] | None = None,
    reintentos: int = 1,
) -> tuple[httpx.Response, float]:
    """Devuelve (respuesta, latencia_ms). Relanza el error de red si se agotan los reintentos."""
    for intento in range(reintentos + 1):
        inicio = time.perf_counter()
        try:
            respuesta = await client.post(url, json=json, headers=headers)
        except httpx.TransportError:  # ConnectError, ReadTimeout, etc.
            if intento == reintentos:
                raise  # se agotaron los reintentos: que el llamador decida
            continue
        return respuesta, (time.perf_counter() - inicio) * 1000
    raise ValueError("reintentos no puede ser negativo")


def cuerpo_texto(destino_wa_id: str, texto: str) -> dict[str, Any]:
    """Cuerpo de un mensaje de texto de la Cloud API (forma documentada por Meta)."""
    return {
        "messaging_product": "whatsapp",
        "to": destino_wa_id,
        "type": "text",
        "text": {"body": texto},
    }
