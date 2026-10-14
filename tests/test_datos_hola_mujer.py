"""Pruebas de los JSON normalizados de Hola Mujer (data/hola_mujer/) y de su esquema."""

import importlib.util
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hola_mujer"
_spec = importlib.util.spec_from_file_location(
    "normalizar_hola_mujer", ROOT / "tools" / "datos" / "normalizar_hola_mujer.py"
)
assert _spec is not None and _spec.loader is not None
nz = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(nz)


def _items(nombre: str) -> list[dict[str, object]]:
    return json.loads((DATA / nombre).read_text(encoding="utf-8"))["items"]


def test_services_validate_against_schema_and_are_unique() -> None:
    servicios = [nz.Servicio(**s) for s in _items("servicios.json")]
    assert len(servicios) == 47
    assert len({s.service_id for s in servicios}) == 47
    assert [s.service_id for s in servicios] == sorted(s.service_id for s in servicios)


def test_services_business_rules() -> None:
    for s in (nz.Servicio(**x) for x in _items("servicios.json")):
        assert s.reserva_pen <= s.precio_pen
        assert s.activo
        if s.sensible_clinico:
            assert s.categoria in nz.CATEGORIAS_SENSIBLES


def test_uniform_duration_is_flagged_as_unverified() -> None:
    servicios = _items("servicios.json")
    assert len({s["duracion_min"] for s in servicios}) == 1
    assert not any(s["duracion_verificada"] for s in servicios)


def test_glow_is_not_in_the_catalog_so_the_bot_cannot_quote_a_price() -> None:
    assert not any("glow" in str(s["nombre"]).lower() for s in _items("servicios.json"))


def test_promotions_are_not_usable_until_the_business_confirms() -> None:
    promos = [nz.Promocion(**p) for p in _items("promociones.json")]
    assert {p.promo_id for p in promos} == {"LUNARES", "MOLDEA", "GLUTEOS"}
    assert not any(p.usable_en_rag for p in promos)


def test_inactive_or_ambiguous_promotion_cannot_be_marked_usable() -> None:
    base = _items("promociones.json")[0]
    with pytest.raises(ValueError, match="inactiva"):
        nz.Promocion(**{**base, "usable_en_rag": True})


def test_business_facts_confirmed_by_the_monitor() -> None:
    hechos = {h["clave"]: h for h in _items("negocio.json")}
    for clave in ("ADDRESS", "MAP_URL", "OPENING_HOURS"):
        assert hechos[clave]["estado"] == "CONFIRMED"
        assert hechos[clave]["fuente"] == nz.FUENTE_CONFIRMADOS
    assert "15:00-19:00" in str(hechos["OPENING_HOURS"]["valor"])
    assert hechos["EMERGENCY_PROTOCOL"]["valor"] is None


def test_vocabularies_cover_the_values_the_domain_uses() -> None:
    voc = json.loads((DATA / "vocabularios.json").read_text(encoding="utf-8"))
    assert (
        voc["etapas_contacto"][0] == "P00_NUEVO_LEAD"
        and "PERDIDO" in voc["etapas_contacto"]
    )
    assert {"HANDOFF_REQUESTED", "BOOKING_CONFIRMED", "INTEGRATION_ERROR"} <= set(
        voc["tipos_evento"]
    )
    assert {"CONFIRMED", "ATTENDED", "NO_SHOW"} <= set(voc["estados_cita"])


def test_no_personal_data_in_any_normalized_file() -> None:
    for archivo in DATA.glob("*.json"):
        texto = archivo.read_text(encoding="utf-8")
        assert not re.search(r"\d{7,}", texto), archivo.name
        assert "@" not in texto, archivo.name
        assert "docs.google.com" not in texto, archivo.name
