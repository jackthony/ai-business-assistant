import pytest
from conftest import ScriptedModel
from fastapi.testclient import TestClient
from langgraph.checkpoint.memory import InMemorySaver

from agents.graph import build_graph
from api.chat_app import create_chat_app
from services.notifier_memory import InMemoryNotifier

RESPUESTA = "El Taller PRP Facial + Capilar cuesta S/ 149.99 [1]."
PREGUNTA = "¿Cuánto cuesta el taller PRP facial?"
CLINICA = "Me duele mucho después del tratamiento, ¿es normal?"


@pytest.fixture
def client(store):
    model = ScriptedModel(RESPUESTA)
    graph = build_graph(
        store, model, "SISTEMA", InMemoryNotifier(), None, InMemorySaver()
    )
    app = create_chat_app(graph)
    return TestClient(app)


def test_w1_web_router_and_health(client):
    resp_health = client.get("/health")
    assert resp_health.status_code == 200
    assert resp_health.json() == {"status": "ok"}

    response = client.post("/chat", json={"user_id": "u123", "text": PREGUNTA})
    assert response.status_code == 200
    data = response.json()
    assert "S/ 149.99" in data["reply"]
    assert data["silent"] is False
    assert isinstance(data["first_response_ms"], float)


def test_w2_web_validation_boundaries(client):
    # W2: Validaciones estrictas de contrato en /chat (deben dar 422)
    invalid_payloads = [
        {
            "user_id": "a b",
            "text": PREGUNTA,
        },  # user_id con espacios (inválido por ID_PATTERN)
        {"user_id": "", "text": PREGUNTA},  # user_id vacío
        {"user_id": "u1", "text": ""},  # texto vacío
        {"user_id": "u1", "text": "a" * 1001},  # texto excede 1000 caracteres
        {"user_id": "u1"},  # falta el campo text
    ]
    for payload in invalid_payloads:
        resp = client.post("/chat", json=payload)
        assert resp.status_code == 422


def test_w3_web_handoff_and_silence(client):
    # W3: Handoff en web y congelamiento de hilo (silent: true, reply: null)
    # 1. Mensaje clínico activa handoff
    resp1 = client.post("/chat", json={"user_id": "u_handoff", "text": CLINICA})
    assert resp1.status_code == 200

    # 2. Siguiente mensaje en hilo congelado debe retornar silent: true y reply: null
    resp2 = client.post("/chat", json={"user_id": "u_handoff", "text": PREGUNTA})
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["reply"] is None
    assert data2["silent"] is True
    assert data2["first_response_ms"] == 0.0
