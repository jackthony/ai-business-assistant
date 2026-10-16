"""CLI del agente: se prueba sin Ollama (el grafo real se inyecta con un modelo guionado)."""

import pytest
from conftest import ScriptedModel

from agents import cli
from agents.graph import build_graph
from services.notifier_memory import InMemoryNotifier


def test_cli_imprime_respuesta(store, capsys, monkeypatch):
    modelo = ScriptedModel("Cuesta S/ 149.99 [1].")
    monkeypatch.setattr(
        cli,
        "build_default_graph",
        lambda tenant: build_graph(store, modelo, "SISTEMA", InMemoryNotifier()),
    )
    codigo = cli.main(["--phone", "51900000000", "precio taller PRP facial"])
    assert codigo == 0
    assert "Cuesta S/ 149.99" in capsys.readouterr().out


def test_cli_sin_texto_es_error():
    with pytest.raises(SystemExit) as e:
        cli.main([])
    assert e.value.code == 2
