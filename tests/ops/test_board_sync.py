"""Pruebas de la lógica pura de board_sync (sin red)."""

import importlib.util
import pathlib

_RUTA = (
    pathlib.Path(__file__).resolve().parents[2]
    / ".github"
    / "scripts"
    / "board_sync.py"
)
_spec = importlib.util.spec_from_file_location("board_sync", _RUTA)
assert _spec is not None and _spec.loader is not None
bs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bs)


def issue(**kw):
    base = {
        "title": "x",
        "state": "OPEN",
        "labels": [],
        "assignees": [],
        "pr_abierto": False,
        "status_actual": "Todo",
    }
    return {**base, **kw}


def test_alumno_sale_del_assignee_antes_que_del_label():
    q = bs.deseado(issue(assignees=["WhoAllan"], labels=["alumno:pilar"]))
    assert q["Alumno"] == "Allan Zerpa"


def test_alumno_sale_del_label_si_no_hay_assignee():
    assert bs.deseado(issue(labels=["alumno:pilar"]))["Alumno"] == "Pilar Aguilar"


def test_sin_alumno_no_se_inventa_ninguno():
    assert "Alumno" not in bs.deseado(issue(assignees=["otra-persona"]))


def test_semana_desde_label_o_titulo_normalizada():
    assert bs.deseado(issue(labels=["week:S5"]))["Semana"] == "S5"
    assert bs.deseado(issue(title="[S04] Semana 4 — tracker"))["Semana"] == "S4"
    assert bs.deseado(issue(title="[S06 D2] algo"))["Semana"] == "S6"


def test_area_y_complejidad_desde_labels():
    q = bs.deseado(issue(labels=["tipo:docs", "complejidad:media"]))
    assert (q["Area"], q["Complejidad"]) == ("Gestión", "Media")
    assert bs.deseado(issue(labels=["tipo:feature"]))["Area"] == "Producto"


def test_status_cerrado_en_curso_y_reabierto():
    assert bs.deseado(issue(state="CLOSED"))["Status"] == "Done"
    assert bs.deseado(issue(pr_abierto=True))["Status"] == "In Progress"
    assert bs.deseado(issue(status_actual="Done"))["Status"] == "Todo"
    assert "Status" not in bs.deseado(issue())  # abierto sin PR: no se toca


def test_cambios_solo_lista_lo_que_difiere():
    assert bs.cambios(
        {"Area": "Gestión", "Semana": None}, {"Area": "Gestión", "Semana": "S4"}
    ) == {"Semana": "S4"}


def test_digests_no_entran_al_board():
    assert not bs.debe_estar_en_board(
        {"title": "Digest semanal — 2026-10-09", "labels": ["senati"]}
    )
    assert bs.debe_estar_en_board(
        {"title": "Gestión: algo", "labels": ["tipo:gestion"]}
    )
    assert not bs.debe_estar_en_board({"title": "Sin labels", "labels": ["coach"]})
