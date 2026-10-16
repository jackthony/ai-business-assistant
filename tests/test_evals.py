"""Los evals del HITO 2: pasan con el código actual y FALLAN cuando se rompe lo que dicen cubrir."""

import contextlib
import uuid

import pytest
from conftest import DATA
from langgraph.types import Command

from evals.run import SCRIPTED_MAX_DISTANCE, main
from evals.runner import Result, check, percentile, render, run_suite
from evals.scenarios import SCENARIOS, Expect
from evals.scripted import ScriptedModel
from rag.documents import load_documents
from rag.embedding import LexicalEmbedder
from rag.store import ChromaStore


@pytest.fixture(scope="module")
def eval_store():
    store = ChromaStore(
        LexicalEmbedder(),
        f"evals-{uuid.uuid4().hex[:8]}",
        max_distance=SCRIPTED_MAX_DISTANCE,
    )
    store.ingest(load_documents(DATA))
    return store


def run_all(store) -> dict[int, Result]:
    results = run_suite(SCENARIOS, store, lambda sc: ScriptedModel(*sc.script))
    return {r.scenario.id: r for r in results}


def failing(results: dict[int, Result]) -> set[int]:
    return {i for i, r in results.items() if not r.passed}


def test_son_los_12_escenarios_del_hito():
    assert [s.id for s in SCENARIOS] == list(range(1, 13))
    assert sum(s.handoff for s in SCENARIOS) == 2  # 2 de derivación
    assert any("Re-ejecución" in s.name for s in SCENARIOS)  # 1 de re-ejecución


def test_12_de_12_con_el_modelo_guionado(eval_store):
    results = run_all(eval_store)
    assert failing(results) == set(), {
        i: r.failures for i, r in results.items() if r.failures
    }


def test_el_escenario_de_promocion_si_llega_a_consultar_al_modelo(eval_store):
    assert run_all(eval_store)[4].model_calls == 1  # no pasa «por vacío»


# --- Los evals deben poder fallar: se rompe una regla y el escenario que la cubre lo detecta ---


def test_si_la_validacion_de_cifras_se_afloja_fallan_5_y_12(eval_store, monkeypatch):
    monkeypatch.setattr("agents.info.validate_answer", lambda answer, q, passages: [1])
    assert {5, 12} <= failing(run_all(eval_store))


def test_si_se_acepta_un_importe_de_la_pregunta_falla_el_12(eval_store, monkeypatch):
    from agents import info

    original = info._AMOUNT
    monkeypatch.setattr(
        info, "_AMOUNT", info.re.compile(r"(?!x)x")
    )  # ningún importe se vigila
    assert 12 in failing(run_all(eval_store))
    monkeypatch.setattr(info, "_AMOUNT", original)


def test_si_se_apaga_la_derivacion_fallan_10_y_11(eval_store, monkeypatch):
    monkeypatch.setattr("agents.graph.classify", lambda text: None)
    assert {10, 11} <= failing(run_all(eval_store))


def test_si_la_clave_no_es_idempotente_falla_el_8(eval_store, monkeypatch):
    monkeypatch.setattr("tools.agendar.idempotency_key", lambda inp: uuid.uuid4().hex)
    assert 8 in failing(run_all(eval_store))


def test_si_se_escribe_sin_esperar_la_aprobacion_fallan_6_y_7(eval_store, monkeypatch):
    monkeypatch.setattr("agents.booking.interrupt", lambda payload: {"approved": True})
    assert {6, 7} <= failing(run_all(eval_store))


def test_si_se_ofrece_un_horario_ocupado_falla_el_9(eval_store, monkeypatch):
    monkeypatch.setattr(
        "services.calendar_memory.InMemoryCalendar.is_free", lambda self, start: True
    )
    assert 9 in failing(run_all(eval_store))


def test_si_las_promociones_entran_al_rag_falla_el_4(eval_store, monkeypatch):
    from rag.documents import Document

    promo = Document(
        doc_id="PROMO-LUNARES",
        text="Promoción eliminación de verrugas y lunares. Precio: S/ 49.99.",
        label="Promoción lunares",
        source="promociones.json#LUNARES",
        kind="promocion",
    )
    store = ChromaStore(
        LexicalEmbedder(), f"evals-{uuid.uuid4().hex[:8]}", max_distance=0.9
    )
    store.ingest([*load_documents(DATA), promo])
    results = run_suite(
        [s for s in SCENARIOS if s.id == 4],
        store,
        lambda sc: ScriptedModel("Hay promoción [1]."),
    )
    assert not results[0].passed


# --- El corredor: expectativas, métricas y reporte ---


def test_check_detecta_cada_tipo_de_desvio():
    msg = type(
        "M",
        (),
        {
            "content": "Cuesta S/ 1 gratis",
            "additional_kwargs": {"citations": [{"doc_id": "PROMO-X"}]},
        },
    )()
    out = {"messages": [msg], "intent": "info", "status": "active"}
    exp = Expect(
        intent_in=["handoff_clinical"],
        status="handoff_requested",
        contains=["149.99"],
        not_contains=["gratis"],
        not_matches=[r"S/\s*1(?!\d)"],
        interrupt=True,
        cites=["HM-ACA-001"],
        cites_not_prefix=["PROMO-"],
    )
    assert len(check(exp, out)) == 8


def test_percentil():
    assert percentile([], 0.95) == 0.0
    assert percentile([5.0], 0.95) == 5.0
    assert percentile([1, 2, 3, 4, 100], 0.95) == 100


def test_el_reporte_trae_tabla_contencion_y_aviso(eval_store):
    results = run_suite(SCENARIOS, eval_store, lambda sc: ScriptedModel(*sc.script))
    texto = render(results, "guionado")
    assert "**Escenarios:** 12/12" in texto
    assert "**Contención** (resueltos sin derivar): 10/10" in texto
    assert "**Derivación correcta:** 2/2" in texto
    assert "no** mide al modelo real" in texto
    assert (
        sum(line.startswith("| ") for line in texto.splitlines()) == 13
    )  # cabecera + 12


def test_la_cli_guionada_sale_en_0_y_guarda_la_tabla(tmp_path, capsys):
    destino = tmp_path / "tabla.md"
    assert main(["--out", str(destino)]) == 0
    assert "12/12" in capsys.readouterr().out
    assert "Escenarios E2E del HITO 2" in destino.read_text(encoding="utf-8")


def test_la_cli_sale_en_1_si_algo_falla(monkeypatch):
    monkeypatch.setattr("agents.graph.classify", lambda text: None)
    assert main([]) == 1


def test_reanudar_un_hilo_sin_pendiente_no_agenda(eval_store):
    """Reanudar dos veces (canal que reintenta) no escribe una segunda cita."""
    from evals.runner import Run

    sc = next(s for s in SCENARIOS if s.id == 7)
    run = Run(sc, eval_store, ScriptedModel(*sc.script))
    run.say(sc.steps[0].say)
    run.resume(True)
    with contextlib.suppress(
        Exception
    ):  # LangGraph puede rechazar el reintento: también es seguro
        run.graph.invoke(Command(resume={"approved": True}), run.config)
    assert len(run.calendar.bookings()) == 1
