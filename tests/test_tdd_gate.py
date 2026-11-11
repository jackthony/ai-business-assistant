"""Exercise the gate against actual Git history, without GitHub or secrets."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

GATE = Path(__file__).resolve().parents[1] / ".github/scripts/tdd_gate.py"
CONTRACT = "program/01_CURRICULUM/asignaciones/issue-42.md"
TEST = "tests/test_service.py"
SOURCE = "src/service.py"
CONTRACT_TEXT = """# Respuesta del servicio

## Comportamiento

El servicio devuelve 42.

## Archivos

- `src/service.py`

## Pruebas

- `tests/test_service.py`
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def commit(repo: Path, name: str, files: dict[str, str]) -> str:
    for filename, contents in files.items():
        path = repo / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", name)
    return git(repo, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "Pruebas")
    git(tmp_path, "config", "user.email", "pruebas@example.test")
    base = commit(tmp_path, "base", {SOURCE: "def answer():\n    return 0\n"})
    return tmp_path, base


def gate(repo: Path, base: str, body: str = "Closes #42"):
    return subprocess.run(
        [sys.executable, str(GATE)],
        cwd=repo,
        env={
            **os.environ,
            "TDD_BASE_SHA": base,
            "TDD_HEAD_SHA": git(repo, "rev-parse", "HEAD"),
            "TDD_HEAD_REF": "issue-42-servicio",
            "TDD_PR_BODY": body,
        },
        capture_output=True,
        text=True,
        check=False,
    )


TEST_BODY = (
    "from service import answer\n\ndef test_answer():\n    assert answer() == 42\n"
)
SOURCE_BODY = "def answer():\n    return 42\n"


def test_separate_contract_test_and_product_pass(repo):
    root, base = repo
    commit(root, "contrato y prueba", {CONTRACT: CONTRACT_TEXT, TEST: TEST_BODY})
    commit(root, "producto", {SOURCE: SOURCE_BODY})
    result = gate(root, base)
    assert result.returncode == 0, result.stdout + result.stderr


def test_documentation_only_does_not_need_product_tests(repo):
    root, base = repo
    commit(root, "documentacion", {"README.md": "Texto\n"})
    assert gate(root, base, body="").returncode == 0


@pytest.mark.parametrize(
    ("history", "expected"),
    [
        ([{TEST: TEST_BODY}, {SOURCE: SOURCE_BODY}], "contrato"),
        ([{CONTRACT: CONTRACT_TEXT, TEST: TEST_BODY, SOURCE: SOURCE_BODY}], "separado"),
        (
            [{CONTRACT: CONTRACT_TEXT}, {SOURCE: SOURCE_BODY}, {TEST: TEST_BODY}],
            "antes",
        ),
        (
            [{CONTRACT: CONTRACT_TEXT, TEST: "# marcador\n"}, {SOURCE: SOURCE_BODY}],
            "prueba",
        ),
        (
            [
                {
                    CONTRACT: CONTRACT_TEXT,
                    TEST: "def helper():\n    def test_answer():\n        assert False\n",
                },
                {SOURCE: SOURCE_BODY},
            ],
            "prueba",
        ),
        ([{TEST: TEST_BODY}, {CONTRACT: CONTRACT_TEXT, SOURCE: SOURCE_BODY}], "antes"),
        (
            [{CONTRACT: CONTRACT_TEXT, TEST: TEST_BODY}, {"src/otro.py": "x = 1\n"}],
            "fuera del contrato",
        ),
    ],
)
def test_product_pr_rejects_missing_evidence(repo, history, expected):
    root, base = repo
    for index, files in enumerate(history):
        commit(root, f"paso {index}", files)
    result = gate(root, base)
    assert result.returncode == 1, result.stdout + result.stderr
    assert expected in result.stdout.lower()


def test_issue_number_must_match_branch(repo):
    root, base = repo
    commit(root, "contrato y prueba", {CONTRACT: CONTRACT_TEXT, TEST: TEST_BODY})
    commit(root, "producto", {SOURCE: SOURCE_BODY})
    result = gate(root, base, body="Closes #84")
    assert result.returncode == 1
    assert "#42" in result.stdout


def test_existing_assignment_contract_is_read_from_base(repo):
    root, _ = repo
    directory = "program/01_CURRICULUM/asignaciones"
    base = commit(
        root,
        "contrato vigente",
        {
            f"{directory}/README.md": "| #42 | [`S05_D1.md`](S05_D1.md) |\n",
            f"{directory}/S05_D1.md": (
                "## 4. Archivos\n"
                "| `src/service.py` | modificar |\n"
                "| `tests/test_service.py` | crear |\n"
                "## 6. Pruebas\n"
                "Debe devolver 42.\n"
            ),
        },
    )
    commit(root, "prueba", {TEST: TEST_BODY})
    commit(root, "producto", {SOURCE: SOURCE_BODY})
    result = gate(root, base)
    assert result.returncode == 0, result.stdout + result.stderr
