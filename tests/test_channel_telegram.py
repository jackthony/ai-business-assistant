from unittest.mock import MagicMock

import pytest
from conftest import ScriptedModel
from fastapi.testclient import TestClient
from langgraph.checkpoint.memory import InMemorySaver

from agents.graph import build_graph
from api.chat_app import create_chat_app
from channels.telegram import build_telegram_router, parse_update
from services.notifier_memory import InMemoryNotifier

RESPUESTA = "El Taller PRP Facial + Capilar cuesta S/ 149.99 [1]."
PREGUNTA = "¿Cuánto cuesta el taller PRP facial?"


def test_g1_telegram_parse_private_text():
    raw = {
        "update_id": 100,
        "message": {
            "chat": {"id": 123456, "type": "private"},
            "from": {"id": 123456},
            "text": "hola citas",
        },
    }
    event = parse_update(raw, tenant="hola_mujer")
    assert event is not None
    assert event.user_id == "123456"
    assert event.content == "hola citas"
    assert event.channel == "telegram"
    assert event.type == "text"
    assert event.tenant == "hola_mujer"


def test_g2_telegram_parse_voice_and_media():
    voice_raw = {
        "update_id": 102,
        "message": {
            "chat": {"id": 789, "type": "private"},
            "voice": {"file_id": "abc"},
        },
    }
    event_voice = parse_update(voice_raw)
    assert event_voice is not None
    assert event_voice.type == "voice"
    assert event_voice.content is None

    media_raw = {
        "update_id": 103,
        "message": {
            "chat": {"id": 789, "type": "private"},
            "photo": [{"file_id": "xyz"}],
        },
    }
    event_media = parse_update(media_raw)
    assert event_media is not None
    assert event_media.type == "media"
    assert event_media.content is None


def test_g3_telegram_parse_ignored_updates():
    assert parse_update({}, tenant="hola_mujer") is None
    assert (
        parse_update(
            {"edited_message": {"chat": {"id": 1, "type": "private"}, "text": "hi"}},
            tenant="hola_mujer",
        )
        is None
    )
    assert (
        parse_update(
            {
                "callback_query": {
                    "id": "1",
                    "message": {"chat": {"id": 1, "type": "private"}},
                }
            },
            tenant="hola_mujer",
        )
        is None
    )
    assert (
        parse_update(
            {"message": {"chat": {"id": -999, "type": "group"}, "text": "hi"}},
            tenant="hola_mujer",
        )
        is None
    )


def test_g4_telegram_webhook_security():
    dummy_graph = MagicMock()
    sent_calls = []
    dummy_send = lambda uid, text: sent_calls.append((uid, text))

    with pytest.raises(ValueError):
        build_telegram_router(dummy_graph, "", dummy_send)

    app = create_chat_app(
        dummy_graph, telegram_secret="secret123", telegram_send=dummy_send
    )
    client = TestClient(app)

    response = client.post(
        "/telegram/webhook",
        json={"update_id": 1},
        headers={"X-Telegram-Bot-Api-Secret-Token": "bad"},
    )
    assert response.status_code == 403

    response_no_header = client.post("/telegram/webhook", json={"update_id": 1})
    assert response_no_header.status_code == 403

    assert sent_calls == []


def test_g5_telegram_send_injected(store):
    model = ScriptedModel(RESPUESTA)
    graph = build_graph(
        store, model, "SISTEMA", InMemoryNotifier(), None, InMemorySaver()
    )

    sent_calls = []

    def mock_send(user_id, text):
        sent_calls.append((user_id, text))

    app = create_chat_app(graph, telegram_secret="secret123", telegram_send=mock_send)

    payload = {
        "update_id": 200,
        "message": {
            "chat": {"id": 123, "type": "private"},
            "text": PREGUNTA,
        },
    }
    with TestClient(app) as client:
        response = client.post(
            "/telegram/webhook",
            json=payload,
            headers={"X-Telegram-Bot-Api-Secret-Token": "secret123"},
        )
        assert response.status_code == 200

        response_second = client.post(
            "/telegram/webhook",
            json={"update_id": 201},
            headers={"X-Telegram-Bot-Api-Secret-Token": "secret123"},
        )
        assert response_second.status_code == 200

    assert len(sent_calls) == 1
    assert sent_calls[0][0] == "123"
    assert "S/ 149.99" in sent_calls[0][1]


def test_g6_telegram_same_agent_behavior(store):
    model = ScriptedModel(RESPUESTA)
    graph = build_graph(
        store, model, "SISTEMA", InMemoryNotifier(), None, InMemorySaver()
    )

    sent_calls = []

    def mock_send(user_id, text):
        sent_calls.append((user_id, text))

    app = create_chat_app(graph, telegram_secret="secret123", telegram_send=mock_send)

    with TestClient(app) as client:
        web_res = client.post("/chat", json={"user_id": "u123", "text": PREGUNTA})

        telegram_res = client.post(
            "/telegram/webhook",
            json={
                "update_id": 300,
                "message": {"chat": {"id": 123, "type": "private"}, "text": PREGUNTA},
            },
            headers={"X-Telegram-Bot-Api-Secret-Token": "secret123"},
        )

    assert web_res.status_code == 200
    assert telegram_res.status_code == 200

    web_data = web_res.json()
    assert len(sent_calls) == 1
    assert sent_calls[0][1] == web_data["reply"]
