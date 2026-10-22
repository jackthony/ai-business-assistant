"""Prueba W1: cableado del grafo de conversación con LLM falso."""

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from agents.conversation_graph import build_conversation_graph
from agents.conversation_service import ConversationService


@pytest.mark.parametrize(
    "reply, es_valido",
    [
        ("Hola, ¿en qué te ayudo?", True),
        ("a\nb\nc\nd", False),
    ],
)
def test_w1_grafo_conversacion_con_llm_falso(fake_llm, reply, es_valido):
    fake_llm.reply = reply
    servicio = ConversationService(llm=fake_llm, system="SYS")
    grafo = build_conversation_graph(servicio)

    estado_inicial = {
        "messages": [HumanMessage("Hola")],
        "phone": "51900000000",
        "tenant": "hola_mujer",
        "intent": None,
        "status": "nuevo",
    }

    resultado = grafo.invoke(estado_inicial)

    # TODO: completar las aserciones según el contrato W1
    # Caso a (es_valido=True):
    #   len(resultado["messages"]) == 2
    #   resultado["messages"][1] es AIMessage con content == reply
    #   resultado["status"] == "respondido"
    # Caso b (es_valido=False):
    #   resultado["status"] == "revision_humana"
    #   len(resultado["messages"]) == 1
    # En ambos:
    #   resultado["intent"] is None
    #   resultado["phone"] == "51900000000"
    #   resultado["tenant"] == "hola_mujer"
    #   len(fake_llm.calls) == 1
    assert len(fake_llm.calls) == 1
    assert resultado["intent"] is None
    assert resultado["phone"] == "51900000000"
    assert resultado["tenant"] == "hola_mujer"

    if es_valido:
        assert len(resultado["messages"]) == 2
        assert isinstance(resultado["messages"][1], AIMessage)
        assert resultado["messages"][1].content == reply
        assert resultado["status"] == "respondido"
    else:
        assert len(resultado["messages"]) == 1
        assert resultado["status"] == "revision_humana"
