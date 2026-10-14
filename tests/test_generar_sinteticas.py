"""Pruebas del generador de conversaciones sintéticas v2 (tools/corpus/generar_sinteticas.py)."""

import importlib.util
import re
from collections import Counter
from itertools import pairwise
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "generar_sinteticas", ROOT / "tools" / "corpus" / "generar_sinteticas.py"
)
assert _spec is not None and _spec.loader is not None
gs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gs)

FILAS = gs.generar(80, 20, gs.SEED)
PRECIOS_APROBADOS = {"89.99", "149.99", "59.99", "49.99"}


def _conversaciones() -> dict[str, list[dict[str, object]]]:
    por: dict[str, list[dict[str, object]]] = {}
    for f in FILAS:
        por.setdefault(str(f["conversacion_id"]), []).append(f)
    return por


def test_same_seed_gives_same_corpus_and_other_seed_differs() -> None:
    assert gs.generar(80, 20, gs.SEED) == FILAS
    assert gs.generar(80, 20, gs.SEED + 1) != FILAS


def test_schema_turns_and_timestamps_are_consistent() -> None:
    claves = {
        "conversacion_id",
        "turno",
        "rol",
        "texto",
        "ts",
        "canal",
        "origen",
        "emisor",
    }
    assert len(_conversaciones()) == 100
    for msgs in _conversaciones().values():
        assert [m["turno"] for m in msgs] == list(range(1, len(msgs) + 1))
        tiempos = [str(m["ts"]) for m in msgs]
        assert tiempos == sorted(tiempos)
        assert len({m["canal"] for m in msgs}) == 1
        for m in msgs:
            assert claves <= m.keys()
            assert m["origen"] == "sintetica"
            assert m["rol"] == ("user" if m["emisor"] == "cliente" else "assistant")
            assert m["emisor"] in {"cliente", "humano", f"bot_{m['canal']}"}


def test_natural_split_follows_measured_quotas_exactly() -> None:
    natural = {
        cid: msgs[0]
        for cid, msgs in _conversaciones().items()
        if msgs[0]["split"] == "natural"
    }
    esperado = Counter(gs._cuotas(gs.PARAMS["escenarios"]["valor"], 80))
    assert Counter(m["escenario"] for m in natural.values()) == esperado


def test_quota_split_is_exact_and_sums_to_total() -> None:
    cuotas = gs._cuotas({"a": 24, "b": 7, "c": 5, "d": 3}, 39)
    assert Counter(cuotas) == {"a": 24, "b": 7, "c": 5, "d": 3}
    assert len(gs._cuotas({"a": 1, "b": 1, "c": 1}, 10)) == 10


def test_coverage_split_forces_the_rare_paths() -> None:
    desenlaces = {
        msgs[0]["desenlace"]
        for msgs in _conversaciones().values()
        if msgs[0]["split"] == "cobertura"
    }
    assert {
        "cita",
        "reprogramar",
        "cancelar",
        "handoff_clinico",
        "ciudad_otra",
        "n8n_repite",
    } <= desenlaces


def test_no_personal_data_in_any_message() -> None:
    for f in FILAS:
        texto = str(f["texto"])
        assert not re.search(r"\d{7,}", texto)
        assert "@" not in texto
        assert "http" not in texto.lower()


def test_prices_only_come_from_the_approved_catalog_and_glow_has_none() -> None:
    for msgs in _conversaciones().values():
        precios = set(
            re.findall(r"S/ (\d+\.\d{2})", " ".join(str(m["texto"]) for m in msgs))
        )
        assert precios <= PRECIOS_APROBADOS
        cliente = " ".join(
            str(m["texto"]) for m in msgs if m["emisor"] == "cliente"
        ).lower()
        if "glow" in cliente:
            assert not precios


def test_staff_never_gives_clinical_advice() -> None:
    prohibidas = (
        "diagnóstico",
        "dosis",
        "medicamento",
        "te recomiendo tomar",
        "debes tomar",
    )
    for f in FILAS:
        if f["emisor"] != "cliente":
            assert not any(p in str(f["texto"]).lower() for p in prohibidas)


def test_confirmed_hour_is_inside_opening_hours_and_matches_what_the_client_asked() -> (
    None
):
    for msgs in _conversaciones().values():
        for ant, m in pairwise(msgs):
            hora = re.search(r"te anoto a las (\d+):00", str(m["texto"]))
            if hora:
                assert 15 <= int(hora.group(1)) <= 18
                pedida = re.search(r"a las (\d)", str(ant["texto"]))
                assert pedida and int(pedida.group(1)) + 12 == int(hora.group(1))


def test_every_param_declares_source_and_type() -> None:
    for p in gs.PARAMS.values():
        assert p["fuente"] and p["tipo"]
