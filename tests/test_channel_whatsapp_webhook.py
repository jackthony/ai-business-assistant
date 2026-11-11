import hashlib
import hmac
import json
from unittest.mock import MagicMock

import pytest
from conftest import ScriptedModel
from fastapi.testclient import TestClient
from langgraph.checkpoint.memory import InMemorySaver

import channels.whatsapp.webhook
from agents.graph import build_graph
from api.chat_app import create_chat_app
from channels.dispatch import thread_id_for
from channels.telegram import parse_update
from rag.documents import Document
from rag.embedding import LexicalEmbedder
from rag.store import ChromaStore
from services.notifier_memory import InMemoryNotifier

webhook = channels.whatsapp.webhook

SECRET = "secreto-de-prueba"
VERIFY = "token-de-prueba"
PHONE = "51900000000"
TEXT = "Hola, ¿qué horarios tienen?"
PREGUNTA = "¿Cuánto cuesta el taller ficticio SENATI?"
RESPUESTA = "El taller ficticio SENATI cuesta S/ 42.00 [1]."
STATUSES = {"entry": [{"changes": [{"value": {"statuses": [{"id": "x"}]}}]}]}


def _payload(msg: dict) -> dict:
    return {"entry": [{"changes": [{"value": {"messages": [msg]}}]}]}


def _text(body: str = TEXT) -> dict:
    return _payload({"from": PHONE, "type": "text", "text": {"body": body}})


def _sign(body: bytes) -> str:
    return "sha256=" + hmac.new(SECRET.encode(), body, hashlib.sha256).hexdigest()


def _post(client, payload, signature=None):
    body = json.dumps(payload).encode()
    headers = {"X-Hub-Signature-256": signature or _sign(body)}
    return client.post("/whatsapp/webhook", content=body, headers=headers)


def _app(graph, send):
    return create_chat_app(
        graph,
        whatsapp_verify_token=VERIFY,
        whatsapp_app_secret=SECRET,
        whatsapp_send=send,
    )


def test_w1_verify_challenge():
    assert webhook.verify_challenge("subscribe", VERIFY, "123", VERIFY) == "123"
    assert webhook.verify_challenge("subscribe", "otro", "123", VERIFY) is None
    assert webhook.verify_challenge("unsubscribe", VERIFY, "123", VERIFY) is None
    assert webhook.verify_challenge("subscribe", "", "123", "") is None


def test_w2_get_verification_http():
    client = TestClient(_app(MagicMock(), lambda u, t: None))
    url = "/whatsapp/webhook?hub.mode=subscribe&hub.challenge=987&hub.verify_token="
    ok = client.get(url + VERIFY)
    assert ok.status_code == 200
    assert ok.text == "987"
    assert client.get(url + "malo").status_code == 403


def test_w3_signature_is_valid():
    body = b'{"a": 1}'
    assert webhook.signature_is_valid(body, _sign(body), SECRET) is True
    assert webhook.signature_is_valid(b'{"a": 2}', _sign(body), SECRET) is False
    assert webhook.signature_is_valid(body, None, SECRET) is False
    assert webhook.signature_is_valid(body, _sign(body), "") is False
    assert webhook.signature_is_valid(body, _sign(body)[7:], SECRET) is False


def test_w4_parse_text():
    event = webhook.parse_payload(_text())
    assert event is not None
    assert event.channel == "whatsapp"
    assert event.type == "text"
    assert event.user_id == PHONE
    assert event.content == TEXT
    assert event.tenant == "hola_mujer"


def test_w5_parse_audio_and_image():
    voice = webhook.parse_payload(
        _payload({"from": PHONE, "type": "audio", "audio": {}})
    )
    media = webhook.parse_payload(
        _payload({"from": PHONE, "type": "image", "image": {}})
    )
    assert voice is not None and voice.type == "voice" and voice.content is None
    assert media is not None and media.type == "media" and media.content is None


def test_w6_parse_ignored():
    assert webhook.parse_payload({}) is None
    assert webhook.parse_payload(STATUSES) is None
    assert webhook.parse_payload(_payload({"from": PHONE, "type": "reaction"})) is None
    assert webhook.parse_payload(_payload({"from": PHONE, "type": "location"})) is None
    assert (
        webhook.parse_payload(_payload({"type": "text", "text": {"body": "hola"}}))
        is None
    )
    assert (
        webhook.parse_payload(
            _payload({"from": PHONE, "type": "text", "text": {"body": None}})
        )
        is None
    )


def test_w7_bad_signature_rejected():
    sent: list = []
    client = TestClient(_app(MagicMock(), lambda u, t: sent.append((u, t))))
    assert _post(client, _text(), signature="sha256=abc").status_code == 403
    body = json.dumps(_text()).encode()
    assert client.post("/whatsapp/webhook", content=body).status_code == 403
    assert sent == []


def test_w8_router_fails_closed():
    def send(user_id, text):
        return None

    with pytest.raises(ValueError):
        webhook.build_whatsapp_router(MagicMock(), "", SECRET, send)
    with pytest.raises(ValueError):
        webhook.build_whatsapp_router(MagicMock(), VERIFY, "  ", send)


def test_w9_post_sends_reply_in_background():
    store = ChromaStore(LexicalEmbedder(), "whatsapp-contract-test")
    store.ingest(
        [
            Document(
                doc_id="taller-ficticio",
                text="El taller ficticio SENATI cuesta S/ 42.00.",
                label="Catálogo ficticio",
                source="fixture:taller-ficticio",
                kind="servicio",
            )
        ]
    )
    graph = build_graph(
        store,
        ScriptedModel(RESPUESTA),
        "SISTEMA",
        InMemoryNotifier(),
        None,
        InMemorySaver(),
    )
    sent: list = []
    with TestClient(_app(graph, lambda u, t: sent.append((u, t)))) as client:
        malformed = b"{"
        ignored = client.post(
            "/whatsapp/webhook",
            content=malformed,
            headers={"X-Hub-Signature-256": _sign(malformed)},
        )
        assert ignored.status_code == 200
        assert not sent
        accepted = _post(client, _text(PREGUNTA))
        assert (accepted.status_code, accepted.json()) == (200, {"ok": True})
        assert _post(client, STATUSES).status_code == 200
    assert len(sent) == 1
    assert sent[0][0] == PHONE
    assert "S/ 42.00" in sent[0][1]
    assert "Catálogo ficticio" in sent[0][1]


def test_w10_same_phone_two_channels_two_threads():
    wa = webhook.parse_payload(_text())
    raw = {"message": {"chat": {"id": int(PHONE), "type": "private"}, "text": "hola"}}
    tg = parse_update(raw)
    assert wa is not None and tg is not None
    assert thread_id_for(wa) == f"whatsapp:{PHONE}"
    assert thread_id_for(tg) == f"telegram:{PHONE}"
    assert thread_id_for(wa) != thread_id_for(tg)
