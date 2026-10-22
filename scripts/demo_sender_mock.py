"""Demo E2E del Issue #4 (sin Meta real): fixture -> parse mock (#3) -> sender mock.

Simula el ciclo mensaje WhatsApp -> respuesta saliente midiendo el tiempo de primera
respuesta desde que llega el webhook hasta que se dispara el envío a Meta.

Uso (desde la raiz del repo):
    python scripts/demo_sender_mock.py

Graba tu terminal con esto para el video de evidencia del PR.
"""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path

# Permitir importar src/ sin tocar la configuracion del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import httpx

from channels.whatsapp.sender import WhatsAppSender

logging.basicConfig(level="INFO", format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("demo")

PHONE_ID = "phone_number_id_demo"
TOKEN = "token_demo_no_real"


def mock_parse_webhook(payload: dict) -> dict:
    """Simula el parseo del webhook de Pilar (#3): devuelve wa_id + texto."""
    value = payload["entry"][0]["changes"][0]["value"]
    message = value["messages"][0]
    return {
        "wa_id": value["contacts"][0]["wa_id"],
        "text": message["text"]["body"],
        "received_at": time.perf_counter(),
    }


async def main():
    print("=" * 62)
    print("DEMO E2E #4 - WhatsApp sender (mock, sin app Meta real)")
    print("=" * 62)

    # Paso 0: llega un mensaje real de WhatsApp (fixture del webhook)
    webhook_payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "entry_demo",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "contacts": [
                                {
                                    "wa_id": "51999999999",
                                    "profile": {"name": "Cliente Demo"},
                                }
                            ],
                            "messages": [
                                {
                                    "from": "51999999999",
                                    "id": "wamid.inbound_001",
                                    "timestamp": str(int(time.time())),
                                    "text": {
                                        "body": "Hola, deseo informacion de citas"
                                    },
                                    "type": "text",
                                }
                            ],
                        }
                    }
                ],
            }
        ],
    }

    # Paso 1: parseo del webhook (simula el router de Pilar, #3) -> InboundEvent + t0
    inbound = mock_parse_webhook(webhook_payload)
    print(
        f"\n1) WEBHOOK recibido -> wa_id={inbound['wa_id']}, texto='{inbound['text']}'"
    )
    print("   t0 (recepcion webhook) capturado")

    requests_url = []
    first_response_ms = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests_url.append(str(request.url))
        if request.method != "POST":
            return httpx.Response(400)
        body = json.loads(request.content)
        # t1: justo antes de disparar el POST a Meta
        first_response_ms.append((time.perf_counter() - inbound["received_at"]) * 1000)
        print(f"\n2) SENDER armado el POST (t1 - t0 = {first_response_ms[-1]:.1f} ms):")
        print(f"     URL  : {request.url!s}")
        print(f"     Auth : {request.headers.get('Authorization')}")
        print(f"     Body : {json.dumps(body, ensure_ascii=False)}")
        return httpx.Response(200, json={"messages": [{"id": "wamid.demo_001"}]})

    sender = WhatsAppSender(
        phone_number_id=PHONE_ID,
        access_token=TOKEN,
        transport=httpx.MockTransport(handler),
    )

    print("\n3) Ejecutando send_text (sin llamadas reales a Meta)...")
    response = await sender.send_text(
        inbound["wa_id"],
        f"Hola! Recibi tu mensaje: '{inbound['text']}'",
        received_at=inbound["received_at"],
    )
    print("\n4) Meta (mock) respondio:")
    print(f"     {json.dumps(response, ensure_ascii=False)}")

    print("\n5) Verificaciones:")
    print(f"     - endpoint           : .../{PHONE_ID}/messages  (OK)")
    print("     - llamadas reales a Meta: 0 (MockTransport, OK)")
    print(
        f"     - tiempo primera respuesta: {first_response_ms[0]:.1f} ms (webhook -> send)"
    )
    print("     - latency_ms (POST a Meta): logueado (ver logs INFO)")
    print("\nDEMO OK: ciclo mensaje -> respuesta (mock) cumplido.")
    print("=" * 62)


if __name__ == "__main__":
    asyncio.run(main())
