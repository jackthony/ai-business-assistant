import json
from pathlib import Path

from navegar_payload import es_solo_estado, leer_mensaje

FIXTURES = Path(__file__).parent / "fixtures"


def cargar(nombre: str) -> dict:
    return json.loads((FIXTURES / nombre).read_text(encoding="utf-8"))


def test_mensaje_de_texto():
    msg = leer_mensaje(cargar("webhook_text.json"))
    assert msg == {
        "wa_id": "51900000000",
        "id": "wamid.TEST0001",
        "tipo": "text",
        "texto": "Hola, ¿qué horarios tienen?",
    }


def test_imagen_distingue_tipo_y_no_tiene_texto():
    msg = leer_mensaje(cargar("webhook_image.json"))
    assert msg is not None
    assert msg["tipo"] == "image"
    assert msg["texto"] is None


def test_status_no_es_mensaje_de_usuario():
    payload = cargar("webhook_status.json")
    assert es_solo_estado(payload)
    assert leer_mensaje(payload) is None


def test_payload_de_texto_no_es_solo_estado():
    assert not es_solo_estado(cargar("webhook_text.json"))


def test_payloads_raros_no_revientan():
    for raro in ({}, {"entry": []}, {"entry": [{"changes": []}]}, {"entry": None}):
        assert leer_mensaje(raro) is None
        assert not es_solo_estado(raro)
