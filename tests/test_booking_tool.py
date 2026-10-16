"""Herramienta agendar_cita (N2): validación determinista, idempotencia y rejilla de horarios."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pytest
from conftest import CONFIGS, DATA
from pydantic import ValidationError

from rag.catalog import ServiceCatalog
from services.calendar_memory import InMemoryCalendar
from tools.agendar import AgendarInput, make_agendar_tool
from tools.schedule import LIMA, load_schedule

NOW = datetime(2026, 10, 19, 10, 0, tzinfo=LIMA)  # lunes 10:00
CITA = {
    "phone": "51900000000",
    "service_id": "HM-ACA-001",
    "start": "2026-10-20T16:00:00-05:00",
}


@pytest.fixture
def schedule():
    return load_schedule(CONFIGS / "schedule.json")


@pytest.fixture
def calendar():
    return InMemoryCalendar()


@pytest.fixture
def tool(calendar, schedule):
    catalog = ServiceCatalog.from_file(DATA / "servicios.json")
    return make_agendar_tool(calendar, catalog, schedule, lambda: NOW)


def test_es_una_herramienta_n2_con_schema_estricto(tool):
    assert tool.metadata == {"permission_level": "N2"}
    assert set(tool.args) == {"phone", "service_id", "start"}


def test_agendar_dos_veces_crea_una_sola_cita(tool, calendar):
    primera, segunda = tool.invoke(CITA), tool.invoke(CITA)
    assert (primera["status"], segunda["status"]) == ("created", "already_booked")
    assert primera["key"] == segunda["key"]
    assert len(calendar.bookings()) == 1


def test_la_clave_no_depende_del_formato_de_la_hora(tool, calendar):
    tool.invoke(CITA)
    otra = {**CITA, "start": "2026-10-20T21:00:00+00:00"}  # misma hora, en UTC
    assert tool.invoke(otra)["status"] == "already_booked"
    assert len(calendar.bookings()) == 1


def test_reintentos_en_paralelo_no_duplican(tool, calendar):
    with ThreadPoolExecutor(8) as pool:
        estados = [r["status"] for r in pool.map(lambda _: tool.invoke(CITA), range(8))]
    assert estados.count("created") == 1
    assert len(calendar.bookings()) == 1


def test_horario_ocupado_por_otra_persona_se_rechaza(tool, calendar):
    tool.invoke(CITA)
    r = tool.invoke({**CITA, "phone": "51911111111"})
    assert (r["status"], r["reason"]) == ("rejected", "slot_busy")
    assert len(calendar.bookings()) == 1


@pytest.mark.parametrize(
    ("cambio", "motivo"),
    [
        ({"start": "2026-10-20T20:00:00-05:00"}, "not_in_schedule"),  # tras el cierre
        (
            {"start": "2026-10-20T16:30:00-05:00"},
            "not_in_schedule",
        ),  # fuera de la rejilla
        (
            {"start": "2026-10-20T10:00:00-05:00"},
            "not_in_schedule",
        ),  # mañana sin atención
        ({"start": "2026-10-19T09:00:00-05:00"}, "past"),
        ({"service_id": "HM-NOEXISTE-999"}, "service_unknown"),
    ],
)
def test_validacion_determinista(tool, calendar, cambio, motivo):
    r = tool.invoke({**CITA, **cambio})
    assert (r["status"], r["reason"]) == ("rejected", motivo)
    assert calendar.bookings() == []


@pytest.mark.parametrize(
    "malo",
    [
        {"phone": "abc"},
        {"phone": "123"},
        {"start": "2026-10-20T16:00:00"},  # sin zona horaria
        {"extra": "x"},
    ],
)
def test_entrada_invalida_ni_llega_a_la_logica(malo):
    datos = {
        "phone": "51900000000",
        "service_id": "HM-ACA-001",
        "start": "2026-10-20T16:00:00-05:00",
    }
    with pytest.raises(ValidationError):
        AgendarInput(**{**datos, **malo})


def test_rejilla_del_horario(schedule):
    en_punto = lambda h, m=0: datetime(2026, 10, 20, h, m, tzinfo=LIMA)
    assert schedule.is_slot_start(en_punto(15))
    assert schedule.is_slot_start(en_punto(18))
    assert not schedule.is_slot_start(en_punto(19))  # termina después del cierre
    assert not schedule.is_slot_start(en_punto(14))
    assert not schedule.is_slot_start(en_punto(15, 30))


def test_proximos_horarios_saltan_al_dia_siguiente(schedule):
    tarde = datetime(2026, 10, 19, 18, 30, tzinfo=LIMA)
    primero = next(schedule.upcoming_starts(tarde))
    assert primero == datetime(2026, 10, 20, 15, 0, tzinfo=LIMA)


def test_horario_coincide_con_el_dato_confirmado():
    import json

    negocio = json.loads((DATA / "negocio.json").read_text(encoding="utf-8"))["items"]
    horas = next(i for i in negocio if i["clave"] == "OPENING_HOURS")
    assert horas["estado"] == "CONFIRMED" and "15:00-19:00" in horas["valor"]


def test_catalogo_resuelve_por_codigo():
    cat = ServiceCatalog.from_file(DATA / "servicios.json")
    assert [s.service_id for s in cat.find("PRP facial")] == [
        "HM-FAC-001"
    ]  # exacto gana
    assert [s.service_id for s in cat.find("taller PRP facial")] == ["HM-ACA-001"]
    assert len(cat.find("facial")) > 1  # ambiguo: hay que preguntar
    assert cat.find("vuelo a marte") == []
    assert cat.find("") == []
