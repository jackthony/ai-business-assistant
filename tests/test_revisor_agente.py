"""Pruebas del revisor-agente (.github/scripts/revisor_agente.py): validación en código del LLM."""

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "revisor_agente", ROOT / ".github" / "scripts" / "revisor_agente.py"
)
assert _spec is not None and _spec.loader is not None
ra = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ra)

SECCIONES = {"4", "5", "5a", "5b", "6", "8", "9"}


def raw(**kw) -> str:
    base = {"veredicto": "CAMBIOS", "resumen": "r", "hallazgos": []}
    base.update(kw)
    return json.dumps(base)


def hallazgo(nivel="BLOCKER", seccion="5b", **kw) -> dict:
    h = {
        "nivel": nivel,
        "seccion": seccion,
        "archivo": "src/agents/graph.py",
        "problema": "p",
        "pista": "mira la doc",
    }
    h.update(kw)
    return h


def test_parse_accepts_fenced_json() -> None:
    v = ra.parse_verdict("```json\n" + raw() + "\n```", SECCIONES)
    assert v is not None and v.veredicto == "CAMBIOS"


def test_parse_rejects_garbage() -> None:
    assert ra.parse_verdict("no soy json", SECCIONES) is None
    assert ra.parse_verdict(raw(veredicto="TAL VEZ"), SECCIONES) is None


def test_blocker_must_cite_a_real_contract_section() -> None:
    v = ra.parse_verdict(raw(hallazgos=[hallazgo(seccion="99")]), SECCIONES)
    assert v is not None and v.hallazgos[0].nivel == "MINOR"  # alucinación → degradado


def test_blocker_with_valid_section_blocks() -> None:
    v = ra.parse_verdict(raw(hallazgos=[hallazgo()]), SECCIONES)
    assert v is not None and ra.blocks(v)


def test_minor_only_does_not_block() -> None:
    v = ra.parse_verdict(
        raw(veredicto="APROBAR", hallazgos=[hallazgo("MINOR")]), SECCIONES
    )
    assert v is not None and not ra.blocks(v)


def test_hint_with_code_block_is_stripped() -> None:
    v = ra.parse_verdict(
        raw(hallazgos=[hallazgo(pista="usa esto:\n```python\nx=1\n```")]), SECCIONES
    )
    assert v is not None and "```" not in v.hallazgos[0].pista


def test_prompt_marks_diff_as_data_and_has_no_secrets() -> None:
    p = ra.build_prompt({"4": "s4", "9": "s9"}, "DIFF-X", "det")
    assert "DIFF-X" in p and "datos" in p.lower() and "JSON" in p


def test_decide_skips_llm_when_deterministic_errors() -> None:
    calls = []
    out = ra.decide(
        has_errors=True, draft=False, key="k", llm=lambda _: calls.append(1) or ""
    )
    assert out.failed and calls == []


def test_decide_skips_llm_when_draft_or_no_key() -> None:
    calls = []
    for draft, key in ((True, "k"), (False, "")):
        out = ra.decide(
            has_errors=False, draft=draft, key=key, llm=lambda _: calls.append(1) or ""
        )
        assert not out.failed
    assert calls == []


def test_decide_fails_closed_when_llm_output_is_invalid() -> None:
    out = ra.decide(
        has_errors=False,
        draft=False,
        key="k",
        llm=lambda _: "basura",
        sections=SECCIONES,
        prompt="p",
    )
    assert out.failed and "no válida" in out.note


def test_decide_passes_on_clean_verdict() -> None:
    out = ra.decide(
        has_errors=False,
        draft=False,
        key="k",
        llm=lambda _: raw(veredicto="APROBAR"),
        sections=SECCIONES,
        prompt="p",
    )
    assert not out.failed and out.verdict is not None


def test_ask_claude_payload_has_no_temperature(monkeypatch) -> None:
    """La API de Anthropic rechaza `temperature` en el modelo por defecto (HTTP 400)."""
    sent: dict = {}

    class FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self) -> bytes:
            return json.dumps({"content": [{"type": "text", "text": "OK"}]}).encode()

    def fake_urlopen(req, timeout):
        sent.update(json.loads(req.data))
        return FakeResp()

    monkeypatch.setattr(ra.urllib.request, "urlopen", fake_urlopen)
    assert ra.ask_claude("hola", "k") == "OK"
    assert "temperature" not in sent
    assert sent["messages"][0]["content"] == "hola"


def test_decide_http_config_error_is_named_but_does_not_block() -> None:
    """Un 4xx es un error nuestro (modelo, clave, parámetro): se nombra el código, no bloquea."""

    def boom(_: str) -> str:
        raise ra.urllib.error.HTTPError("u", 400, "Bad Request", None, None)  # type: ignore[arg-type]

    o = ra.decide(False, False, "k", boom, SECCIONES, "p")
    assert o.failed is False
    assert "HTTP 400" in o.note
    assert "configuración" in o.note


def test_decide_server_outage_keeps_generic_note() -> None:
    def boom(_: str) -> str:
        raise ra.urllib.error.HTTPError("u", 503, "Unavailable", None, None)  # type: ignore[arg-type]

    o = ra.decide(False, False, "k", boom, SECCIONES, "p")
    assert o.failed is False
    assert "HTTP 503" not in o.note


def test_decide_network_failure_is_an_outage_note() -> None:
    def boom(_: str) -> str:
        raise ra.urllib.error.URLError("sin red")

    o = ra.decide(False, False, "k", boom, SECCIONES, "p")
    assert o.failed is False
    assert "URLError" in o.note
    assert "caída de la API" in o.note


def test_decide_internal_bug_is_not_disguised_as_api_outage(capsys) -> None:
    """Un KeyError/IndexError es un bug del script: se nombra como error interno, no como caída."""

    def bug(_: str) -> str:
        return {}["content"]  # type: ignore[index]

    o = ra.decide(False, False, "k", bug, SECCIONES, "p")
    assert o.failed is False
    assert "Error interno" in o.note
    assert "KeyError" in o.note
    assert "caída de la API" not in o.note
    assert "::warning::" in capsys.readouterr().out


def test_claude_model_defaults_and_ignores_empty_variable(monkeypatch) -> None:
    monkeypatch.delenv("REVISOR_MODEL", raising=False)
    assert ra.claude_model() == "claude-haiku-5-5"
    monkeypatch.setenv("REVISOR_MODEL", "")  # una `vars.X` sin definir llega como vacía
    assert ra.claude_model() == "claude-haiku-5-5"
    monkeypatch.setenv("REVISOR_MODEL", "otro-modelo")
    assert ra.claude_model() == "otro-modelo"


def test_verdict_comment_names_the_model(monkeypatch) -> None:
    monkeypatch.setenv("REVISOR_MODEL", "modelo-x")
    v = ra.parse_verdict(
        '{"veredicto":"APROBAR","resumen":"ok","hallazgos":[]}', SECCIONES
    )
    assert v is not None
    assert "_Modelo: `modelo-x`_" in ra.render_verdict(ra.Outcome(False, "ok", v))
