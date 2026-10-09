"""Bloque 1 — comprobar que un POST viene de Meta (firma HMAC-SHA256).

Meta firma el CUERPO CRUDO (bytes) del POST con el App Secret y manda el
resultado en la cabecera ``X-Hub-Signature-256: sha256=<hex>``.
Si no validas la firma, cualquiera que conozca tu URL puede inventar mensajes.
"""

import hashlib
import hmac


def firmar(cuerpo: bytes, app_secret: str) -> str:
    """Devuelve la cabecera esperada: ``sha256=<hex>``."""
    digest = hmac.new(app_secret.encode(), cuerpo, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def firma_valida(cuerpo: bytes, cabecera: str | None, app_secret: str) -> bool:
    """True solo si la cabecera coincide con la firma del cuerpo.

    - Sin cabecera o sin secreto configurado -> False (falla cerrado, nunca abierto).
    - ``compare_digest`` compara en tiempo constante (evita ataques de temporización).
    """
    if not cabecera or not app_secret:
        return False
    esperada = firmar(cuerpo, app_secret)
    return hmac.compare_digest(esperada.encode(), cabecera.encode())
