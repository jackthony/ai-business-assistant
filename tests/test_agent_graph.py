"""Pruebas del grafo mínimo de agente (S5 D1)."""

from typing import get_type_hints

from agents.state import AgentState


def test_agent_state_campos_exactos():
    hints = get_type_hints(AgentState, include_extras=True)
    assert set(hints) == {"messages", "phone", "tenant", "intent", "status"}


"""Prueba T2"""


def test_reducer_anade_no_reemplaza():
    from langchain_core.messages import HumanMessage

    from agents.graph import build_graph

    entrada = {
        "messages": [HumanMessage("hola")],
        "phone": "51900000000",
        "tenant": "hola_mujer",
        "intent": None,
        "status": "nuevo",
    }
    salida = build_graph().invoke(entrada)
    assert len(salida["messages"]) == 2
    assert salida["messages"][0].content == "hola"
    assert salida["messages"][1].content == "eco: hola"


"""Prueba 3"""


def test_intent_y_status():
    from langchain_core.messages import HumanMessage

    from agents.graph import build_graph

    entrada = {
        "messages": [HumanMessage("hola")],
        "phone": "51900000000",
        "tenant": "hola_mujer",
        "intent": None,
        "status": "nuevo",
    }
    salida = build_graph().invoke(entrada)
    assert salida["intent"] == "eco"
    assert salida["status"] == "respondido"


def test_phone_y_tenant_intactos():
    from langchain_core.messages import HumanMessage

    from agents.graph import build_graph

    entrada = {
        "messages": [HumanMessage("hola")],
        "phone": "51900000001",
        "tenant": "hola_mujer",
        "intent": None,
        "status": "nuevo",
    }
    salida = build_graph().invoke(entrada)
    assert salida["phone"] == "51900000001"
    assert salida["tenant"] == "hola_mujer"


def test_tildes():
    from langchain_core.messages import HumanMessage

    from agents.graph import build_graph

    entrada = {
        "messages": [HumanMessage("¿Cuánto cuesta el masaje?")],
        "phone": "51900000000",
        "tenant": "hola_mujer",
        "intent": None,
        "status": "nuevo",
    }
    salida = build_graph().invoke(entrada)
    assert salida["messages"][1].content == "eco: ¿Cuánto cuesta el masaje?"


def test_sin_llm():
    import subprocess
    import sys

    codigo = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import agents.graph, sys; "
                "modulos = [m for m in sys.modules if m.startswith('ollama') or m.startswith('langchain_ollama')]; "
                "sys.exit(1 if modulos else 0)"
            ),
        ],
        check=False,
        capture_output=True,
    )
    assert codigo.returncode == 0
