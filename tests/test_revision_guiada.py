"""Pruebas de las funciones puras del revisor guiado (.github/scripts/revision_guiada.py)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "revision_guiada", ROOT / ".github" / "scripts" / "revision_guiada.py"
)
assert _spec is not None and _spec.loader is not None
rg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rg)


def test_issue_number_prefers_closes_over_branch() -> None:
    assert rg.issue_number("Resumen\nCloses #52", "issue-99-otro") == "52"


def test_issue_number_falls_back_to_branch_name() -> None:
    assert rg.issue_number("", "issue-54-memoria-persistente") == "54"
    assert rg.issue_number("", "feature-sin-numero") is None


def test_find_contract_reads_readme_table(monkeypatch) -> None:
    monkeypatch.chdir(ROOT)
    assert rg.find_contract("52") == "S05_D1.md"
    assert rg.find_contract("9999") is None


def test_expected_paths_from_section_4_table() -> None:
    sec4 = "| Ruta | Acción |\n|---|---|\n| `src/a.py` | crear |\n| `tests\\t.py` | crear |"
    assert rg.expected_paths(sec4) == ["src/a.py", "tests/t.py"]


def test_report_marks_touched_existing_and_missing_and_extra() -> None:
    report = rg.build_report(
        ["a.py", "b.py", "c.py"], {"a.py", "b.py"}, ["a.py", "otro.md"]
    )
    assert "con trabajo tuyo: 1/3" in report
    assert "`b.py` | ◻️" in report
    assert "`c.py` | ⬜ falta" in report
    assert "- `otro.md`" in report


def test_skips_monitor_and_any_bot_but_not_students() -> None:
    assert rg.is_skipped_author("jackthony")
    assert rg.is_skipped_author("dependabot[bot]")
    assert rg.is_skipped_author("renovate[bot]")
    assert not rg.is_skipped_author("adbon-dm1")
    assert not rg.is_skipped_author("")
