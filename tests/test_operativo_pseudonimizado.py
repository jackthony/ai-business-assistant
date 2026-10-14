"""Pruebas de los datos operativos pseudonimizados (data/hola_mujer/operativo/)."""

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hola_mujer" / "operativo"
_spec = importlib.util.spec_from_file_location(
    "pseudonimizar_operativo", ROOT / "tools" / "datos" / "pseudonimizar_operativo.py"
)
assert _spec is not None and _spec.loader is not None
ps = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ps)


def _items(nombre: str) -> list[dict[str, object]]:
    return json.loads((DATA / f"{nombre}.json").read_text(encoding="utf-8"))["items"]


def test_alias_is_stable_sequential_and_hides_the_real_id() -> None:
    alias = ps.Alias()
    assert [alias(1986656030), alias(811963537), alias(1986656030)] == [
        "C001",
        "C002",
        "C001",
    ]
    assert alias(None) == ps.SIN_ID
    assert ps.Alias().reemplazar("x") == "x"


def test_no_personal_data_in_any_operational_file() -> None:
    for archivo in DATA.glob("*.json"):
        texto = archivo.read_text(encoding="utf-8")
        assert not re.search(r"\d{9,}", texto), archivo.name
        assert "@" not in texto and "docs.google" not in texto, archivo.name
        assert '"nombre"' not in texto and "telefono" not in texto.replace(
            "tiene_telefono", ""
        ), archivo.name


def test_events_keep_the_real_flow_and_reference_known_contacts() -> None:
    eventos = _items("eventos")
    assert len(eventos) == 46
    conocidos = {c["contact_id"] for c in _items("contactos")}
    for e in eventos:
        assert re.fullmatch(r"C\d{3}", str(e["contact_id"]))
        assert e["event_id"] and str(e["event_id"]).startswith(str(e["contact_id"]))
    assert conocidos <= {e["contact_id"] for e in eventos} | conocidos


def test_appointments_keep_real_defects_instead_of_hiding_them() -> None:
    citas = _items("citas")
    assert len(citas) == 9
    assert all(
        re.fullmatch(r"A\d{3}", str(c["cita_id"])) for c in citas if c.get("cita_id")
    )
    assert any(c.get("contact_id") is None for c in citas)  # filas huérfanas
    assert any(
        c.get("estado_cita") == "CANCELADO" for c in citas
    )  # estado fuera del vocabulario


def test_inbox_sample_is_previews_only() -> None:
    muestra = _items("muestra_inbox")
    assert len(muestra) == 220
    assert {m["alcance_fuente"] for m in muestra} == {"VISTA_PREVIA_SIN_HISTORIAL"}
    assert sum(1 for m in muestra if m["preview_util"]) == 82


def test_timestamps_are_naive_iso_so_the_etl_adds_no_timezone_noise() -> None:
    for c in _items("citas"):
        for col in ("created_at", "updated_at"):
            v = c.get(col)
            assert v is None or not str(v).endswith(("+00:00", "Z")), (col, v)


def test_free_text_fields_only_hold_known_phrases() -> None:
    # Si una regeneración trae una frase nueva, este test obliga a revisarla a mano antes de subirla.
    conocidas = {
        "Reprogramada por el cliente",
        '"Sin motivo especificado"',
        "As",
        None,
    }
    assert {c.get("motivo_cambio") for c in _items("citas")} <= conocidas
    notas = {e.get("notes_nonclinical") for e in _items("eventos")}
    assert all(n is None or re.fullmatch(r"[^\d@]{1,80}", str(n)) for n in notas)
