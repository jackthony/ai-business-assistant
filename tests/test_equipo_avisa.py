"""Pruebas de las funciones puras de los avisos al equipo y la lectura semanal."""

import datetime
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / ".github" / "scripts" / f"{name}.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ea = _load("equipo_avisa")
ls = _load("lectura_semanal")

README = (
    "| Issue | Contrato | Paso a paso | Tema | Depende de |\n"
    "|---|---|---|---|---|\n"
    "| #52 | [`a`](a) | [`b`](b) | Tema uno | — |\n"
    "| #53 | [`a`](a) | [`b`](b) | Tema dos | #52 en `main` (no toca los de #52) |\n"
    "| #54 | [`a`](a) | [`b`](b) | Tema tres | #52 en `main` |\n"
)


def test_dependents_and_deps_from_readme_table() -> None:
    assert ea.dependents_of(README, "52") == ["53", "54"]
    assert ea.dependents_of(README, "53") == []
    assert ea.deps_of(README, "53") == ["52"]
    assert ea.deps_of(README, "52") == []


def test_team_mentions_exclude_author_and_include_monitor() -> None:
    text = ea.team_mentions("jackthony", ["josue", "pilar", "allan"], "josue")
    assert text == "@pilar @allan @jackthony"


def test_issue_from_body() -> None:
    assert ea.issue_from_body("Resumen\nCloses #52") == "52"
    assert ea.issue_from_body("sin cierre") is None


def test_unblock_message_mentions_assignees_and_issue() -> None:
    msg = ea.msg_desbloqueo(["pilar"], "52", "99", "josue")
    assert "@pilar" in msg
    assert "#52 ya está en `main`" in msg


def test_pick_week_by_start_date() -> None:
    cal = {"S05": "2026-10-12", "S06": "2026-10-19"}
    assert ls.pick_week(cal, datetime.date(2026, 10, 18)) == "S05"
    assert ls.pick_week(cal, datetime.date(2026, 10, 19)) == "S06"
    assert ls.pick_week(cal, datetime.date(2026, 10, 1)) is None


def test_lecturas_json_has_sources_and_questions_per_week() -> None:
    cfg = json.loads((ROOT / ".github" / "lecturas.json").read_text(encoding="utf-8"))
    for semana in cfg["calendario"]:
        entry = cfg["semanas"][semana]
        assert entry["fuentes"] and entry["preguntas"]
        assert semana in ls.render_title(semana, entry)
        assert entry["preguntas"][0] in ls.render_body(semana, entry)


da = _load("discusion_avisa")


def test_discussion_message_mentions_team_without_author() -> None:
    team = da.team_mentions("jackthony", ["josue", "pilar", "allan"], "pilar")
    msg = da.build_message("pilar", "Q&A", "[Duda] reducer", team)
    assert "@josue @allan @jackthony" in msg
    assert "@pilar abrió" in msg


def test_reading_body_mentions_roster_when_given() -> None:
    entry = {
        "titulo": "T",
        "fuentes": [{"nombre": "A", "url": "https://x"}],
        "preguntas": ["P1"],
    }
    assert "cc @a @b" in ls.render_body("S05", entry, "@a @b")
    assert "cc @" not in ls.render_body("S05", entry)
