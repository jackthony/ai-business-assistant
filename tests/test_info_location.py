from unittest.mock import Mock

import pytest
from conftest import ScriptedModel
from langchain_core.messages import HumanMessage

from agents.info import make_info_node
from rag.store import Passage

QUESTION = "¿Cuánto cuesta el taller ficticio?"
PRICE_REPLY = "El taller ficticio cuesta S/ 42.00 [1]."


def evaluate(text):
    retriever = Mock()
    retriever.search.return_value = [
        Passage(
            doc_id="taller-ficticio",
            text="El taller ficticio cuesta S/ 42.00.",
            label="Catálogo ficticio",
            source="fixture:taller-ficticio",
            sensitive=False,
            distance=0,
        )
    ]
    model = ScriptedModel(PRICE_REPLY)
    info = make_info_node(retriever, model, "Contexto de prueba")
    result = info(
        {
            "messages": [HumanMessage(text)],
            "phone": "51900000000",
            "tenant": "hola_mujer",
            "intent": None,
            "status": "nuevo",
        }
    )
    return result, retriever, model


def test_outside_declared_city_asks_about_in_person_visit():
    result, retriever, model = evaluate(f"Vivo en Lima. {QUESTION}")
    answer = result["messages"][0]
    assert result["intent"] == "ubicacion_por_confirmar"
    assert result["status"] == "active"
    assert "Chimbote" in answer.content
    assert "¿Puedes acercarte?" in answer.content
    assert "S/" not in answer.content
    assert answer.additional_kwargs["citations"] == []
    retriever.search.assert_not_called()
    assert model.calls == []


@pytest.mark.parametrize(
    "text",
    [
        f"Vivo en NUEVO CHIMBOTE. {QUESTION}",
        QUESTION,
        f"No vivo en Lima. {QUESTION}",
    ],
    ids=["local", "sin-ciudad", "ciudad-negada"],
)
def test_no_explicit_outside_city_keeps_information_flow(text):
    result, retriever, model = evaluate(text)
    assert result["intent"] == "info"
    assert "S/ 42.00" in result["messages"][0].content
    assert (
        result["messages"][0].additional_kwargs["citations"][0]["doc_id"]
        == "taller-ficticio"
    )
    retriever.search.assert_called_once()
    assert len(model.calls) == 1
