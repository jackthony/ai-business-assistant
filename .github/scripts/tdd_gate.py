"""Validate product PR contracts and replay red and green tests."""

import ast
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath

ASSIGNMENTS = "program/01_CURRICULUM/asignaciones"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)


def read_at(sha: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{sha}:{path}"], capture_output=True, text=True, check=False
    )
    return result.stdout if result.returncode == 0 else ""


def changes(before: str, after: str) -> set[str]:
    return set(
        git("diff", "--no-renames", "--name-only", "-z", before, after).split("\0")
    ) - {""}


def product(path: str) -> bool:
    return (
        path.startswith(("src/", "configs/"))
        or (path.startswith("data/hola_mujer/") and path.endswith(".json"))
        or path == "pyproject.toml"
        or re.fullmatch(r"requirements[^/]*\.txt", path) is not None
    )


def test_file(path: str) -> bool:
    name = PurePosixPath(path).name
    return (
        path.startswith("tests/")
        and name.endswith(".py")
        and (name.startswith("test_") or name.endswith("_test.py"))
    )


def section(text: str, title: str) -> str:
    match = re.search(
        rf"^## {title}[^\n]*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL
    )
    return match[1].strip() if match else ""


def paths(text: str) -> set[str]:
    return set(re.findall(r"`([^\s`]+)`", text))


def test_functions(source: str) -> dict[str, str]:
    functions = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            prefix, candidates = f"{node.name}::", node.body
        else:
            prefix, candidates = "", [node]
        for candidate in candidates:
            if isinstance(candidate, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                candidate.name.startswith("test_")
            ):
                functions[prefix + candidate.name] = ast.dump(candidate)
    return functions


def changed_tests(before: str, after: str, files: set[str]) -> dict[str, str]:
    tests = {}
    for path in files:
        original = test_functions(read_at(before, path))
        for name, implementation in test_functions(read_at(after, path)).items():
            if implementation != original.get(name):
                tests[f"{path}::{name}"] = implementation
    return tests


def ancestor(before: str, after: str) -> bool:
    return (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", before, after], check=False
        ).returncode
        == 0
    )


def isolated_env(checkout: Path, home: Path, python: Path) -> dict[str, str]:
    home.mkdir()
    return {
        **{
            name: os.environ[name]
            for name in ("LANG", "LC_ALL", "SYSTEMROOT")
            if name in os.environ
        },
        "HOME": str(home),
        "USERPROFILE": str(home),
        "PATH": os.pathsep.join(
            (str(python.parent), os.environ.get("PATH", os.defpath))
        ),
        "PYTHONPATH": str(checkout / "src"),
        "PYTHONNOUSERSITE": "1",
        "PIP_CONFIG_FILE": os.devnull,
    }


def red_interpreter(checkout: Path, temporary: Path, env: dict[str, str]) -> Path:
    project = checkout / "pyproject.toml"
    requirements = checkout / "requirements.txt"
    if not (project.is_file() or requirements.is_file()):
        return Path(sys.executable)
    venv = temporary / "venv"
    python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run(
        [sys.executable, "-m", "venv", str(venv)],
        cwd=checkout,
        env=env,
        capture_output=True,
        check=True,
        timeout=90,
    )
    dependencies = (
        ["-e", ".[dev]"] if project.is_file() else ["pytest", "-r", "requirements.txt"]
    )
    subprocess.run(
        [str(python), "-m", "pip", "install", "--no-input", *dependencies],
        cwd=checkout,
        env=env,
        capture_output=True,
        check=True,
        timeout=240,
    )
    return python


def run_pytest(
    checkout: Path,
    python: Path,
    env: dict[str, str],
    report: Path,
    selectors: list[str],
) -> tuple[int, list[ET.Element]]:
    result = subprocess.run(
        [
            str(python),
            "-m",
            "pytest",
            "-q",
            "--strict-markers",
            "-o",
            "junit_family=xunit2",
            f"--junitxml={report}",
            "--",
            *selectors,
        ],
        cwd=checkout,
        env=env,
        capture_output=True,
        check=False,
        timeout=180,
    )
    cases = list(ET.parse(report).iter("testcase")) if report.is_file() else []
    return result.returncode, cases


def case_key(case: ET.Element) -> tuple[str, str]:
    return case.get("classname", ""), case.attrib["name"]


def verify_red_green(sha: str, selectors: list[str]) -> int:
    with tempfile.TemporaryDirectory(prefix="tdd-replay-") as directory:
        temporary = Path(directory)
        checkout = temporary / "red"
        checkout.mkdir()
        archive = temporary / "red.tar"
        subprocess.run(
            ["git", "archive", "--format=tar", f"--output={archive}", sha], check=True
        )
        with tarfile.open(archive) as snapshot:
            snapshot.extractall(checkout, filter="data")

        python = Path(sys.executable)
        red_env = isolated_env(checkout, temporary / "red-home", python)
        try:
            red_python = red_interpreter(checkout, temporary, red_env)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            raise ValueError(
                "No se pudieron instalar las dependencias del commit rojo."
            ) from exc
        red_env["PATH"] = os.pathsep.join((str(red_python.parent), red_env["PATH"]))
        red_status, red_cases = run_pytest(
            checkout, red_python, red_env, temporary / "red.xml", selectors
        )
        if red_status not in (0, 1) or any(
            case.find("error") is not None for case in red_cases
        ):
            raise ValueError(
                f"El commit rojo tiene un error de colección o de preparación (pytest {red_status})."
            )
        failed = {
            case_key(case)
            for case in red_cases
            if (failure := case.find("failure")) is not None
            and not failure.get("message", "").startswith("[XPASS")
        }
        if red_status != 1 or not failed:
            raise ValueError(
                "Ninguna prueba nueva o modificada falló al ejecutarse antes del código."
            )

        green_checkout = Path.cwd()
        green_env = isolated_env(green_checkout, temporary / "green-home", python)
        green_status, green_cases = run_pytest(
            green_checkout, python, green_env, temporary / "green.xml", selectors
        )
        passed = {
            case_key(case)
            for case in green_cases
            if all(case.find(tag) is None for tag in ("failure", "error", "skipped"))
        }
        if green_status != 0 or not failed <= passed:
            raise ValueError(
                "En verde deben pasar los mismos casos que fallaron en rojo."
            )
        return len(failed)


def validate(base: str, head: str, ref: str, body: str) -> str:
    fork = git("merge-base", base, head).strip()
    final_changes = changes(fork, head)
    product_paths = {path for path in final_changes if product(path)}
    if not product_paths:
        return "TDD: PR sin cambios de producto."

    branch = re.fullmatch(r"(?:issue|tbd)-(\d+)(?:-[a-z0-9]+)*", ref)
    if not branch:
        raise ValueError("Usa una rama issue-N-descripcion para el cambio de producto.")
    issue = branch[1]
    closed = set(re.findall(r"(?im)^\s*(?:closes|fixes|resolves)\s+#(\d+)\b", body))
    if closed != {issue}:
        raise ValueError(
            f"El cuerpo debe vincular el contrato con una línea Closes #{issue}."
        )

    index = read_at(base, f"{ASSIGNMENTS}/README.md")
    legacy = re.search(
        rf"^\|\s*#{issue}\s*\|\s*\[[^\]]+\]\((S\d+_D\d+\.md)\)", index, re.MULTILINE
    )
    path = f"{ASSIGNMENTS}/{legacy[1] if legacy else f'issue-{issue}.md'}"
    contract = read_at(base if legacy else head, path)
    if not contract:
        raise ValueError(f"Falta el contrato de #{issue} en {path}.")
    expected_paths = paths(section(contract, r"4\." if legacy else "Archivos"))
    test_section = section(contract, r"6\." if legacy else "Pruebas")
    if not test_section or (not legacy and not section(contract, "Comportamiento")):
        raise ValueError(f"El contrato {path} debe describir comportamiento y pruebas.")
    outside = product_paths - expected_paths
    if outside:
        raise ValueError("Archivos fuera del contrato: " + ", ".join(sorted(outside)))
    declared_tests = expected_paths if legacy else paths(test_section)
    test_paths = {path for path in declared_tests & final_changes if test_file(path)}
    final_tests = changed_tests(fork, head, test_paths)
    if not final_tests:
        raise ValueError(
            "Agrega o modifica una prueba ejecutable indicada en el contrato."
        )

    commits = git(
        "rev-list", "--reverse", "--topo-order", "--no-merges", f"{base}..{head}"
    )
    history = [(sha, changes(f"{sha}^", sha)) for sha in commits.splitlines()]
    product_commits = [
        (sha, files & product_paths) for sha, files in history if files & product_paths
    ]
    if set().union(*(files for _, files in product_commits)) != product_paths:
        raise ValueError(
            "Cada cambio de producto debe aparecer en un commit fuera de un merge."
        )

    for sha, files in reversed(history):
        if any(product(p) for p in files) or not files & test_paths:
            continue
        if not legacy and read_at(sha, path) != contract:
            continue
        candidates = changed_tests(f"{sha}^", sha, files & test_paths)
        selectors = sorted(
            name
            for name, implementation in candidates.items()
            if final_tests.get(name) == implementation
        )
        if not selectors:
            continue
        if all(ancestor(sha, code_sha) for code_sha, _ in product_commits):
            count = verify_red_green(sha, selectors)
            return (
                f"TDD: contrato #{issue}, rojo → verde en {count} caso(s) ({sha[:12]})."
            )
    raise ValueError(
        "El contrato y la misma prueba deben existir en un commit separado antes del código."
    )


def main() -> int:
    try:
        print(
            validate(
                os.environ["TDD_BASE_SHA"],
                os.environ["TDD_HEAD_SHA"],
                os.environ["TDD_HEAD_REF"],
                os.environ.get("TDD_PR_BODY", ""),
            )
        )
    except (ValueError, SyntaxError, ET.ParseError, subprocess.TimeoutExpired) as exc:
        print(f"::error::{exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
