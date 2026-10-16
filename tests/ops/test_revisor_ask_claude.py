"""Pruebas de la lectura de la respuesta de Claude en el revisor-agente (Issue #150), sin red."""

import importlib.util
import json
import pathlib
from typing import Self

import pytest

_RUTA = (
    pathlib.Path(__file__).resolve().parents[2]
    / ".github"
    / "scripts"
    / "revisor_agente.py"
)
_spec = importlib.util.spec_from_file_location("revisor_agente", _RUTA)
assert _spec is not None and _spec.loader is not None
ra = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ra)

VEREDICTO = json.dumps({"veredicto": "APROBAR", "resumen": "ok", "hallazgos": []})


class _Resp:
    def __init__(self, body: dict | str) -> None:
        self._raw = (body if isinstance(body, str) else json.dumps(body)).encode()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    def read(self) -> bytes:
        return self._raw


def _ask(monkeypatch: pytest.MonkeyPatch, body: dict | str) -> str:
    monkeypatch.setattr(
        ra.urllib.request, "urlopen", lambda *a, **k: _Resp(body), raising=True
    )
    return ra.ask_claude("prompt", "clave-falsa")


def test_respuesta_normal(monkeypatch):
    body = {"content": [{"type": "text", "text": VEREDICTO}]}
    assert _ask(monkeypatch, body) == VEREDICTO


def test_ignora_el_bloque_thinking_que_viene_primero(monkeypatch):
    # Caso real del Issue #150: claude-haiku-5-5 devuelve [thinking, text].
    body = {
        "content": [
            {"type": "thinking", "thinking": "...", "signature": "x"},
            {"type": "text", "text": VEREDICTO},
        ]
    }
    assert _ask(monkeypatch, body) == VEREDICTO


@pytest.mark.parametrize(
    "body",
    [
        {"content": []},
        {"content": [{"type": "thinking", "thinking": "...", "signature": "x"}]},
        {"content": [{"type": "text"}]},
        {"type": "error", "error": {"type": "overloaded_error", "message": "x"}},
        "no es json",
    ],
    ids=[
        "content-vacio",
        "solo-thinking",
        "text-sin-campo",
        "error-con-200",
        "no-json",
    ],
)
def test_respuesta_ilegible_levanta_error_explicito(monkeypatch, body):
    with pytest.raises(ra.RespuestaIlegible):
        _ask(monkeypatch, body)


def test_decide_nombra_el_fallo_de_lectura_y_deja_warning(capsys):
    def llm(_: str) -> str:
        raise ra.RespuestaIlegible("ningún bloque de texto", '{"content": []}')

    o = ra.decide(False, False, "clave", llm, set(), "p")
    assert not o.failed
    assert "Error al leer la respuesta" in o.note
    assert "no respondió" not in o.note
    out = capsys.readouterr().out
    assert out.startswith("::warning::") and '{"content": []}' in out
    assert "clave" not in out
