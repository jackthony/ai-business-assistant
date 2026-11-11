"""Validate product PR contracts and test-first history using Git objects."""

import ast
import os
import re
import subprocess
from pathlib import PurePosixPath

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


def changed_tests(before: str, after: str, files: set[str]) -> set[tuple[str, str]]:
    tests = set()
    for path in files:
        original = test_functions(read_at(before, path))
        for name, implementation in test_functions(read_at(after, path)).items():
            if implementation != original.get(name):
                tests.add((path, name))
    return tests


def ancestor(before: str, after: str) -> bool:
    return (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", before, after], check=False
        ).returncode
        == 0
    )


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

    for sha, files in history:
        if any(product(p) for p in files) or not files & test_paths:
            continue
        if not legacy and read_at(sha, path) != contract:
            continue
        if not changed_tests(f"{sha}^", sha, files & test_paths) & final_tests:
            continue
        if all(ancestor(sha, code_sha) for code_sha, _ in product_commits):
            return f"TDD: contrato #{issue} y commit de pruebas anterior al código ({sha[:12]})."
    raise ValueError(
        "El contrato y la prueba deben existir en un commit separado antes del código."
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
    except (ValueError, SyntaxError) as exc:
        print(f"::error::{exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
