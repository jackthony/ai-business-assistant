"""Pruebas de las reglas de issue_orden (hito por semana, tracker y semana del título)."""

import importlib.util
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / ".github" / "scripts"
sys.path.insert(0, str(SCRIPTS))
_spec = importlib.util.spec_from_file_location(
    "issue_orden", SCRIPTS / "issue_orden.py"
)
assert _spec is not None and _spec.loader is not None
io = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(io)


def test_week_from_title_or_label() -> None:
    assert io.week_of("[S05 D1] LangGraph", []) == 5
    assert io.week_of("Estudio guiado", ["week:S07"]) == 7
    assert io.week_of("Gestión: algo", []) is None


def test_milestone_by_week_range() -> None:
    assert io.milestone_prefix(5, []) == "HITO 1"
    assert io.milestone_prefix(8, []) == "HITO 2"
    assert io.milestone_prefix(11, []) == "HITO 3"
    assert io.milestone_prefix(15, []) == "Demo final"


def test_milestone_for_operation_issues_without_week() -> None:
    assert io.milestone_prefix(None, ["coach"]) == io.OPERACION
    assert io.milestone_prefix(None, ["tipo:gestion"]) == io.OPERACION
    assert io.milestone_prefix(None, ["bug-sin-tipo"]) is None


def test_tracker_title_prefix() -> None:
    assert io.tracker_prefix(5) == "[S05] Semana"
    assert "[S05] Semana 5 — tracker".startswith(io.tracker_prefix(5))
