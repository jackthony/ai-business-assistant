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
    assert "rojo → verde" in result.stdout


@pytest.mark.parametrize(
    ("test", "expected"),
    [
        ("def test_answer():\n    assert True\n", "falló"),
        ("import missing_senati_module\n" + TEST_BODY, "colección"),
        (
            "import pytest\n@pytest.mark.skip\ndef test_answer():\n    assert False\n",
            "falló",
        ),
        (
            TEST_BODY.replace("== 42", "== 7"),
            "verde",
        ),
        (
            (
                "import pytest\nfrom service import answer\ndef test_answer():\n"
                "    if answer() == 42:\n        pytest.skip('oculta el caso')\n"
                "    assert False\n"
            ),
            "verde",
        ),
    ],
)
def test_replay_rejects_unproven_red_green(repo, test, expected):
    root, base = repo
    commit(root, "contrato y prueba", {CONTRACT: CONTRACT_TEXT, TEST: test})
    commit(root, "producto", {SOURCE: SOURCE_BODY})

    result = gate(root, base)

    assert result.returncode == 1, result.stdout + result.stderr
    assert expected in result.stdout.lower()


def test_green_must_preserve_the_test_from_red(repo):
    root, base = repo
    commit(root, "contrato y prueba", {CONTRACT: CONTRACT_TEXT, TEST: TEST_BODY})
    commit(
        root,
        "producto y prueba alterada",
        {SOURCE: SOURCE_BODY, TEST: "def test_answer():\n    assert True\n"},
    )

    result = gate(root, base)

    assert result.returncode == 1, result.stdout + result.stderr
    assert "misma prueba" in result.stdout


def test_replay_does_not_pass_ci_credentials(repo, monkeypatch):
    root, base = repo
    monkeypatch.setenv("GH_TOKEN", "fake-ci-token")
    isolated_test = "import os\n" + TEST_BODY.replace(
        "    assert answer()",
        "    assert 'GH_TOKEN' not in os.environ\n    assert answer()",
    )
    commit(root, "contrato y prueba", {CONTRACT: CONTRACT_TEXT, TEST: isolated_test})
    commit(root, "producto", {SOURCE: SOURCE_BODY})

    result = gate(root, base)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "rojo → verde" in result.stdout


def test_green_can_include_junit_properties(repo):
    root, base = repo
    test_with_property = TEST_BODY.replace(
        "def test_answer():",
        "def test_answer(record_property):\n    record_property('case', '42')",
    )
    commit(
        root, "contrato y prueba", {CONTRACT: CONTRACT_TEXT, TEST: test_with_property}
    )
    commit(root, "producto", {SOURCE: SOURCE_BODY})

    result = gate(root, base)

    assert result.returncode == 0, result.stdout + result.stderr


def test_red_replays_changed_tests_only(repo):
    root, _ = repo
    old_test = TEST_BODY.replace("test_answer", "test_untouched")
    base = commit(root, "prueba existente", {TEST: old_test})
    commit(
        root,
        "contrato y prueba",
        {
            CONTRACT: CONTRACT_TEXT,
            TEST: old_test + "\ndef test_answer():\n    assert True\n",
        },
    )
    commit(root, "producto", {SOURCE: SOURCE_BODY})

    result = gate(root, base)

    assert result.returncode == 1, result.stdout + result.stderr
    assert "falló" in result.stdout


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
