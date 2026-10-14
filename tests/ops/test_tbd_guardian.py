"""Pruebas del guardián TBD: Dependabot exento; los alumnos siguen sujetos a las reglas."""

import os
import pathlib
import re
import subprocess
import sys

_WORKFLOW = (
    pathlib.Path(__file__).resolve().parents[2]
    / ".github"
    / "workflows"
    / "tbd-guardian.yml"
)


def _script() -> str:
    text = _WORKFLOW.read_text(encoding="utf-8")
    m = re.search(r"python3 - <<'PY'\n(.*?)\n\s*PY\n", text, re.DOTALL)
    assert m, "no se encontró el script embebido del guardián"
    lines = m.group(1).splitlines()
    indent = len(lines[0]) - len(lines[0].lstrip())
    return "\n".join(line[indent:] for line in lines)


def _run(
    author: str, head: str, base: str = "main"
) -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "AUTHOR": author,
        "HEAD": head,
        "BASE": base,
        "BODY": "",
        "COMMITS": "1",
        "GH_REPO": "x/y",
        "PR_NUM": "1",
    }
    return subprocess.run(
        [sys.executable, "-c", _script()],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_dependabot_to_main_is_exempt() -> None:
    r = _run("dependabot[bot]", "dependabot/pip/httpx")
    assert r.returncode == 0
    assert "Dependabot" in r.stdout


def test_dependabot_to_other_base_fails() -> None:
    assert _run("dependabot[bot]", "dependabot/pip/httpx", base="dev").returncode == 1


def test_student_with_bad_branch_still_fails() -> None:
    r = _run("estefanyP-hub", "mi-rama")
    assert r.returncode == 1
    assert "no cumple TBD" in r.stdout
