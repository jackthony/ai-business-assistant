"""Bloque 2 — leer el payload anidado de WhatsApp sin romperse.

Forma real (Cloud API): entry[0].changes[0].value, y dentro de value hay
``messages`` (mensaje de la clienta) O ``statuses`` (acuse de entrega).
Meta manda ``statuses`` muchas veces: si tu código asume ``messages[0]`` siempre,
revienta con KeyError/IndexError y Meta reintenta -> bucle de errores.

Este bloque devuelve un dict simple; convertirlo a ``InboundEvent`` (ADR-011),
fijar el tenant y limpiar el texto es TU trabajo en el Issue #3.
"""

from typing import Any


def _value(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        return payload["entry"][0]["changes"][0]["value"]  # type: ignore[no-any-return]
    except (KeyError, IndexError, TypeError):
        return {}


def es_solo_estado(payload: dict[str, Any]) -> bool:
    """True si el payload trae acuses (statuses) y ningún mensaje de usuario."""
    value = _value(payload)
    return bool(value.get("statuses")) and not value.get("messages")


def leer_mensaje(payload: dict[str, Any]) -> dict[str, Any] | None:
    """Extrae wa_id, tipo y texto del primer mensaje, o None si no hay mensaje.

    Tipos que no sean ``text`` devuelven ``texto=None`` (imagen/audio se
    mapearán a ``media``/``voice`` en el contrato; aquí solo se distinguen).
    """
    value = _value(payload)
    mensajes = value.get("messages") or []
    if not mensajes:
        return None
    msg = mensajes[0]
    tipo = msg.get("type", "unknown")
    texto = msg.get("text", {}).get("body") if tipo == "text" else None
    return {"wa_id": msg.get("from"), "id": msg.get("id"), "tipo": tipo, "texto": texto}
