"""Contrato del grafo del agente (estado de 5 campos, reducer, phone/tenant intactos)."""

from typing import get_type_hints

from conftest import ScriptedModel
from langchain_core.messages import HumanMessage

from agents.graph import build_graph
from agents.state import AgentState


def run(store, texto="hola", phone="51900000000"):
    model = ScriptedModel("Cuesta S/ 149.99 [1].")
    return build_graph(store, model, "SISTEMA").invoke(
        {
            "messages": [HumanMessage(texto)],
            "phone": phone,
            "tenant": "hola_mujer",
            "intent": None,
            "status": "nuevo",
        }
    )


def test_agent_state_campos_exactos():
    hints = get_type_hints(AgentState, include_extras=True)
    assert set(hints) == {"messages", "phone", "tenant", "intent", "status"}


def test_reducer_anade_no_reemplaza(store):
    out = run(store, "precio taller PRP facial")
    assert len(out["messages"]) == 2
    assert out["messages"][0].content == "precio taller PRP facial"


def test_phone_y_tenant_intactos(store):
    out = run(store, phone="51900000001")
    assert (out["phone"], out["tenant"]) == ("51900000001", "hola_mujer")


def test_tildes_y_signos(store):
    out = run(store, "¿Cuánto cuesta el taller PRP facial?")
    assert out["intent"] == "info"
