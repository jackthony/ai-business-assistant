"""Pruebas de la CLI (T7–T8)."""

import pytest

from agents.cli import main


def test_cli_imprime_respuesta(capsys):
    codigo = main(["--phone", "51900000000", "hola"])
    assert codigo == 0
    assert capsys.readouterr().out == "eco: hola\n"


def test_cli_sin_texto_es_error():
    with pytest.raises(SystemExit) as e:
        main([])
    assert e.value.code == 2
