"""Check determinista de contrato: ¿el PR de un practicante respeta su `S##_D#.md`?

Sin LLM y sin clave. Falla (exit 1) si el PR:
  - toca archivos que no están en la sección 4 («y nada más»);
  - usa un símbolo/ruta que la sección 9 prohíbe («No agregues/uses/toques…»);
  - agrega una dependencia a pyproject.toml que la sección 4 no nombra;
  - (PR listo, no borrador) deja archivos de la sección 4 sin crear o trae código sin tests.
El orden «pruebas antes que código» solo avisa. Aplica únicamente a los practicantes del roster
(`.github/coach.json`); el monitor y los bots quedan fuera.

Uso en CI: lo invoca revisor_agente.py. Local: DRY_RUN=1 con las mismas variables.
"""

import re
from dataclasses import dataclass

CODE_EXT = (".py", ".toml", ".txt", ".yml", ".yaml", ".cfg", ".ini", ".sh", ".json")
DONT = re.compile(
    r"^-\s*No\s+(?:agregues|a[ñn]adas|instales|conectes|uses|toques|importes)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Finding:
    level: str  # "error" | "warning"
    code: str
    msg: str


def applies(author: str, roster: set[str]) -> bool:
    return author in roster


def expected_paths(sec4: str) -> list[str]:
    paths = re.findall(r"^\|\s*`([^`]+)`\s*\|", sec4, re.MULTILINE)
    return [p.replace("\\", "/") for p in paths]


def forbidden_tokens(sec9: str) -> list[str]:
    """Símbolos entre backticks de las líneas «No agregues/uses/toques…» de la sección 9."""
    out: list[str] = []
    for line in sec9.splitlines():
        if not DONT.match(line):
            continue
        for tok in re.findall(r"`([^`]+)`", line):
            if (
                len(tok) >= 5
                and " " not in tok
                and not tok.isdigit()
                and tok not in out
            ):
                out.append(tok)
    return out


def added_lines(diff: str) -> dict[str, list[str]]:
    files: dict[str, list[str]] = {}
    cur: str | None = None
    for ln in diff.splitlines():
        if ln.startswith("+++ b/"):
            cur = ln[6:]
            files.setdefault(cur, [])
        elif ln.startswith("+") and not ln.startswith("+++") and cur:
            files[cur].append(ln[1:])
    return files


def added_deps(lines: list[str]) -> list[str]:
    deps = []
    for ln in lines:
        m = re.match(
            r'\s*"([A-Za-z0-9_.\-]+)(?:\[[^\]]*\])?\s*(?:[<>=!~].*)?",?\s*$', ln
        )
        if m:
            deps.append(m.group(1).lower())
    return deps


def tests_first_warning(commits: list[tuple[str, list[str]]]) -> str | None:
    first_test = next(
        (
            i
            for i, (_, fs) in enumerate(commits)
            if any(f.startswith("tests/") for f in fs)
        ),
        None,
    )
    first_src = next(
        (
            i
            for i, (_, fs) in enumerate(commits)
            if any(f.startswith("src/") for f in fs)
        ),
        None,
    )
    if first_src is not None and (first_test is None or first_test > first_src):
        return (
            "El primer commit con código de `src/` llegó antes que el primero con pruebas: "
            "el contrato pide escribir las pruebas primero y verlas en rojo (sección 6)."
        )
    return None


def check(
    expected: list[str],
    changed: list[str],
    sec4: str,
    sec9: str,
    diff: str,
    present: set[str],
    draft: bool,
) -> list[Finding]:
    out: list[Finding] = []
    allowed = set(expected)
    extra = [c for c in changed if c not in allowed]
    if extra:
        out.append(
            Finding(
                "error",
                "fuera-de-contrato",
                "Archivos fuera de la sección 4 («y nada más»): "
                + ", ".join(f"`{c}`" for c in extra),
            )
        )
    added = added_lines(diff)
    for tok in forbidden_tokens(sec9):
        if tok in allowed:
            continue
        if "/" in tok or tok.endswith((".py", ".md", ".toml", ".env")):
            hit = tok in changed
        else:
            hit = any(
                tok in ln
                for f, lns in added.items()
                if f.endswith(CODE_EXT)
                for ln in lns
            )
        if hit:
            out.append(
                Finding(
                    "error",
                    "prohibido-seccion-9",
                    f"La sección 9 prohíbe `{tok}` y aparece en tu PR.",
                )
            )
    named = sec4.lower()
    new_deps = [
        d for d in added_deps(added.get("pyproject.toml", [])) if d not in named
    ]
    if new_deps:
        out.append(
            Finding(
                "error",
                "dependencia-nueva",
                "Dependencia(s) que la sección 4 no nombra: "
                + ", ".join(f"`{d}`" for d in new_deps),
            )
        )
    missing = [p for p in expected if p not in present and p not in changed]
    if missing:
        out.append(
            Finding(
                "error" if not draft else "warning",
                "falta-archivo",
                "Faltan archivos de la sección 4: "
                + ", ".join(f"`{m}`" for m in missing),
            )
        )
    touches_src = any(c.startswith("src/") for c in changed)
    touches_tests = any(c.startswith("tests/") for c in changed)
    if touches_src and not touches_tests:
        out.append(
            Finding(
                "error" if not draft else "warning",
                "codigo-sin-tests",
                "Hay código en `src/` pero ningún archivo en `tests/`.",
            )
        )
    return out


def render(findings: list[Finding]) -> str:
    errs = [f for f in findings if f.level == "error"]
    warns = [f for f in findings if f.level == "warning"]
    if not findings:
        return "✅ **Check de contrato:** archivos, dependencias y prohibiciones dentro de lo pedido."
    head = (
        f"❌ **Check de contrato: {len(errs)} error(es)** — no se puede mergear hasta corregirlos."
        if errs
        else "✅ **Check de contrato:** sin errores."
    )
    lines = [head, ""]
    lines += [f"- ❌ `{f.code}` — {f.msg}" for f in errs]
    lines += [f"- ⚠️ `{f.code}` — {f.msg}" for f in warns]
    return "\n".join(lines)
