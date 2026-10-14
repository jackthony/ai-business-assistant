"""Pruebas del check determinista de contrato (.github/scripts/contrato_check.py)."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "contrato_check", ROOT / ".github" / "scripts" / "contrato_check.py"
)
assert _spec is not None and _spec.loader is not None
cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cc)

SEC4 = """## 4. Archivos
| Ruta exacta | Acción | Para qué |
|---|---|---|
| `pyproject.toml` | modificar | Agregar `"langgraph>=1,<2",` y `"langchain-core>=1,<2",` |
| `src/agents/state.py` | crear | AgentState |
| `tests/test_agent_graph.py` | crear | T1-T6 |
"""
SEC9 = """## 9. No hagas
- No conectes el grafo ni toques `src/api/main.py`.
- No agregues checkpointer (`SqliteSaver`), ni `thread_id`, ni `langgraph-checkpoint-sqlite`.
- No cambies los nombres ni los campos de `AgentState`.
- No uses datos reales. Usa solo `51900000000`.
- No agregues herramientas (`@tool`).
- No hagas `git push --force`.
"""
EXPECTED = ["pyproject.toml", "src/agents/state.py", "tests/test_agent_graph.py"]


def diff_of(**files: list[str]) -> str:
    out = []
    for name, lines in files.items():
        path = name.replace("__", "/").replace("_dot_", ".")
        out.append(f"diff --git a/{path} b/{path}\n+++ b/{path}")
        out += [f"+{ln}" for ln in lines]
    return "\n".join(out)


def codes(findings: list) -> set[str]:
    return {f.code for f in findings}


def test_applies_only_to_roster_students() -> None:
    roster = {"adbon-dm1", "WhoAllan"}
    assert cc.applies("adbon-dm1", roster)
    assert not cc.applies("jackthony", roster)
    assert not cc.applies("dependabot[bot]", roster)


def test_forbidden_tokens_come_from_dont_lines_only() -> None:
    toks = cc.forbidden_tokens(SEC9)
    assert {"SqliteSaver", "thread_id", "langgraph-checkpoint-sqlite", "@tool"} <= set(
        toks
    )
    assert "AgentState" not in toks  # «No cambies…» no es una prohibición de uso
    assert "51900000000" not in toks  # dato permitido, no prohibido
    assert "git push --force" not in toks  # tiene espacios: no es un símbolo


def test_expected_paths_extracted_from_section_4() -> None:
    assert cc.expected_paths(SEC4) == EXPECTED


def test_clean_pr_has_no_findings() -> None:
    diff = diff_of(
        src__agents__state_dot_py=["class AgentState: ..."],
        tests__test_agent_graph_dot_py=["def test_x(): ..."],
    )
    f = cc.check(
        EXPECTED,
        ["src/agents/state.py", "tests/test_agent_graph.py"],
        SEC4,
        SEC9,
        diff,
        set(EXPECTED),
        draft=True,
    )
    assert [x for x in f if x.level == "error"] == []


def test_file_outside_contract_is_error() -> None:
    f = cc.check(
        EXPECTED,
        ["src/agents/state.py", ".gitignore"],
        SEC4,
        SEC9,
        "",
        set(),
        draft=True,
    )
    assert "fuera-de-contrato" in codes(f)
    assert any(".gitignore" in x.msg for x in f)


def test_forbidden_symbol_in_added_code_is_error() -> None:
    diff = diff_of(
        src__agents__state_dot_py=[
            "from langgraph.checkpoint.sqlite import SqliteSaver"
        ]
    )
    f = cc.check(EXPECTED, ["src/agents/state.py"], SEC4, SEC9, diff, set(), draft=True)
    assert "prohibido-seccion-9" in codes(f)


def test_forbidden_path_touched_is_error() -> None:
    f = cc.check(EXPECTED, ["src/api/main.py"], SEC4, SEC9, "", set(), draft=True)
    assert "prohibido-seccion-9" in codes(f)


def test_forbidden_symbol_in_markdown_is_ignored() -> None:
    diff = diff_of(docs__nota_dot_md=["mencion de thread_id en prosa"])
    f = cc.check(EXPECTED, [], SEC4, SEC9, diff, set(), draft=True)
    assert "prohibido-seccion-9" not in codes(f)


def test_dependency_not_in_section_4_is_error() -> None:
    diff = diff_of(
        pyproject_dot_toml=['    "langgraph>=1,<2",', '    "langchain-ollama>=1,<2",']
    )
    f = cc.check(
        EXPECTED, ["pyproject.toml"], SEC4, SEC9, diff, set(EXPECTED), draft=True
    )
    msgs = [x.msg for x in f if x.code == "dependencia-nueva"]
    assert len(msgs) == 1 and "langchain-ollama" in msgs[0]


def test_dependency_listed_in_section_4_is_ok() -> None:
    diff = diff_of(
        pyproject_dot_toml=['    "langgraph>=1,<2",', '    "langchain-core>=1,<2",']
    )
    f = cc.check(
        EXPECTED, ["pyproject.toml"], SEC4, SEC9, diff, set(EXPECTED), draft=True
    )
    assert "dependencia-nueva" not in codes(f)


def test_missing_files_warn_in_draft_and_fail_when_ready() -> None:
    draft = cc.check(
        EXPECTED, ["pyproject.toml"], SEC4, SEC9, "", {"pyproject.toml"}, draft=True
    )
    ready = cc.check(
        EXPECTED, ["pyproject.toml"], SEC4, SEC9, "", {"pyproject.toml"}, draft=False
    )
    assert {x.level for x in draft if x.code == "falta-archivo"} == {"warning"}
    assert {x.level for x in ready if x.code == "falta-archivo"} == {"error"}


def test_code_without_tests_is_error_when_ready() -> None:
    f = cc.check(
        EXPECTED, ["src/agents/state.py"], SEC4, SEC9, "", set(EXPECTED), draft=False
    )
    assert "codigo-sin-tests" in codes(f)


def test_tests_first_order_is_a_warning() -> None:
    commits = [("a1", ["src/agents/state.py"]), ("b2", ["tests/test_agent_graph.py"])]
    assert cc.tests_first_warning(commits) is not None
    ok = [("b2", ["tests/test_agent_graph.py"]), ("a1", ["src/agents/state.py"])]
    assert cc.tests_first_warning(ok) is None


def test_josue_pr_81_would_have_been_blocked() -> None:
    """Regresión: el PR #81 real tocó 3 archivos fuera del contrato y metió el checkpointer."""
    diff = diff_of(
        pyproject_dot_toml=['    "langgraph-checkpoint-sqlite>=3,<4",'],
        src__agents__graph_dot_py=[
            "from langgraph.checkpoint.sqlite import SqliteSaver"
        ],
    )
    changed = [
        "pyproject.toml",
        "src/agents/graph.py",
        ".env.example",
        ".gitignore",
        "configs/hola_mujer/prompt_v1.md",
    ]
    f = cc.check(EXPECTED, changed, SEC4, SEC9, diff, set(EXPECTED), draft=False)
    assert {"fuera-de-contrato", "prohibido-seccion-9", "dependencia-nueva"} <= codes(f)


def test_render_marks_failure_and_success() -> None:
    assert "✅" in cc.render([])
    bad = cc.check(EXPECTED, [".gitignore"], SEC4, SEC9, "", set(), draft=True)
    assert "❌" in cc.render(bad)


def test_path_named_in_section_9_but_allowed_in_section_4_is_not_forbidden() -> None:
    sec9 = "- No agregues `langgraph-checkpoint-sqlite` a `pyproject.toml`.\n"
    f = cc.check(
        EXPECTED, ["pyproject.toml"], SEC4, sec9, "", set(EXPECTED), draft=True
    )
    assert "prohibido-seccion-9" not in codes(f)
