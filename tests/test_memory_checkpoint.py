from pathlib import Path

import pytest
from conftest import ScriptedModel
from langchain_core.messages import HumanMessage

from agents.graph import build_graph
from memory.sqlite_checkpointer import open_checkpointer
from memory.thread_config import config_for_phone
from services.notifier_memory import InMemoryNotifier

ROOT = Path(__file__).resolve().parents[1]
PRICE_QUESTION = "¿Cuánto cuesta el taller PRP facial?"
PRICE_ANSWER = "El Taller PRP Facial + Capilar cuesta S/ 149.99 [1]."


def test_t1_same_phone_history_grows(tmp_path, store):
    db = tmp_path / "memoria.db"
    model = ScriptedModel(PRICE_ANSWER)
    config = config_for_phone("51900000000")
    with open_checkpointer(str(db)) as saver:
        graph = build_graph(store, model, "SISTEMA", InMemoryNotifier(), None, saver)
        graph.invoke(
            {
                "messages": [HumanMessage(content=PRICE_QUESTION)],
                "phone": "51900000000",
                "tenant": "hola_mujer",
                "intent": None,
                "status": "nuevo",
            },
            config=config,
        )
        out = graph.invoke(
            {
                "messages": [HumanMessage(content=PRICE_QUESTION)],
                "phone": "51900000000",
                "tenant": "hola_mujer",
            },
            config=config,
        )
    types = [type(m).__name__ for m in out["messages"]]
    assert types == ["HumanMessage", "AIMessage", "HumanMessage", "AIMessage"]
    assert out["messages"][0].content == PRICE_QUESTION


def test_t2_memory_survives_a_restart(tmp_path, store):
    db = tmp_path / "memoria.db"
    config = config_for_phone("51900000000")

    with open_checkpointer(str(db)) as saver:
        model = ScriptedModel(PRICE_ANSWER)
        graph = build_graph(store, model, "SISTEMA", InMemoryNotifier(), None, saver)
        first = graph.invoke(
            {
                "messages": [HumanMessage(content=PRICE_QUESTION)],
                "phone": "51900000000",
                "tenant": "hola_mujer",
                "intent": None,
                "status": "nuevo",
            },
            config=config,
        )
    assert len(first["messages"]) == 2

    with open_checkpointer(str(db)) as saver:
        model = ScriptedModel(PRICE_ANSWER)
        graph = build_graph(store, model, "SISTEMA", InMemoryNotifier(), None, saver)
        second = graph.invoke(
            {
                "messages": [HumanMessage(content=PRICE_QUESTION)],
                "phone": "51900000000",
                "tenant": "hola_mujer",
            },
            config=config,
        )
    assert len(second["messages"]) == 4
    assert second["messages"][0].content == PRICE_QUESTION


def test_t3_two_phones_do_not_share_a_thread(tmp_path, store):
    db = tmp_path / "memoria.db"
    with open_checkpointer(str(db)) as saver:
        model = ScriptedModel(PRICE_ANSWER)
        graph = build_graph(store, model, "SISTEMA", InMemoryNotifier(), None, saver)
        graph.invoke(
            {
                "messages": [HumanMessage(content=PRICE_QUESTION)],
                "phone": "51900000001",
                "tenant": "hola_mujer",
                "intent": None,
                "status": "nuevo",
            },
            config=config_for_phone("51900000001"),
        )
        other = graph.invoke(
            {
                "messages": [HumanMessage(content="¿Cuál es la dirección del local?")],
                "phone": "51900000002",
                "tenant": "hola_mujer",
                "intent": None,
                "status": "nuevo",
            },
            config=config_for_phone("51900000002"),
        )
    assert len(other["messages"]) == 2
    assert other["messages"][0].content == "¿Cuál es la dirección del local?"
    assert other["phone"] == "51900000002"


def test_t4_rejects_invalid_phone_numbers():
    with pytest.raises(ValueError):
        config_for_phone("")

    with pytest.raises(ValueError):
        config_for_phone("   ")

    # Tercer caso: un teléfono válido seguido de una inyección SQL.
    with pytest.raises(ValueError):
        config_for_phone("51900000000'; DROP TABLE checkpoints;--")


def test_t5_env_example_declares_strict_msgpack():
    lines = (ROOT / ".env.example").read_text(encoding="utf-8").splitlines()

    assert "LANGGRAPH_STRICT_MSGPACK=true" in lines


def test_t6_gitignore_ignores_db_files():
    lines = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()

    assert "*.db" in lines


def test_t7_caller_decides_the_db_path(tmp_path, store):
    db = tmp_path / "chat.db"
    model = ScriptedModel(PRICE_ANSWER)
    with open_checkpointer(str(db)) as saver:
        graph = build_graph(store, model, "SISTEMA", InMemoryNotifier(), None, saver)
        graph.invoke(
            {
                "messages": [HumanMessage(content=PRICE_QUESTION)],
                "phone": "51900000000",
                "tenant": "hola_mujer",
                "intent": None,
                "status": "nuevo",
            },
            config=config_for_phone("51900000000"),
        )
    assert db.exists()
