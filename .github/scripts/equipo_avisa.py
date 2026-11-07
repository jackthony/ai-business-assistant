"""Avisos automáticos al equipo: quién subió qué y quién queda desbloqueado.

Uso (en workflows): python3 .github/scripts/equipo_avisa.py <evento>
  evento = pr   -> lee GITHUB_EVENT_PATH (pull_request: opened / ready_for_review / closed)
  evento = borrador -> env PR_NUM, PR_AUTHOR, ISSUE (lo llama pr-borrador tras abrir el PR)
Un comentario con @menciones hace que GitHub envíe correo/notificación a cada mencionado.
Al mergearse un Issue, avisa a quien dependía de él (columna «Depende de» del README de
asignaciones) y quita la etiqueta `bloqueado`. DRY_RUN=1 imprime en vez de publicar.
"""

import json
import os
import re
import subprocess
import sys

REPO = os.environ.get("GH_REPO") or os.environ.get(
    "GITHUB_REPOSITORY", "jackthony/ai-business-assistant"
)
README = "program/01_CURRICULUM/asignaciones/README.md"
CONFIG = ".github/coach.json"


def gh(*args: str) -> str:
    return subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=False
    ).stdout


def load_roster() -> tuple[str, list[str]]:
    with open(CONFIG, encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg["monitor"], [a["login"] for a in cfg["alumnos"]]


def team_mentions(monitor: str, roster: list[str], author: str) -> str:
    others = [u for u in [*roster, monitor] if u != author]
    return " ".join(f"@{u}" for u in dict.fromkeys(others))


def issue_from_body(body: str) -> str | None:
    m = re.search(r"(?i)(?:closes|fixes|resolves)\s+#(\d+)", body or "")
    return m.group(1) if m else None


def dependents_of(readme: str, n: str) -> list[str]:
    """Issues cuya columna «Depende de» (última de la tabla Issue → contrato) cita #n."""
    out = []
    for row in re.finditer(
        r"^\|\s*#(\d+)\s*\|(.*)\|\s*([^|]*)\|\s*$", readme, re.MULTILINE
    ):
        if f"#{n}" in re.findall(r"#\d+", row.group(3)):
            out.append(row.group(1))
    return out


def deps_of(readme: str, n: str) -> list[str]:
    m = re.search(rf"^\|\s*#{n}\s*\|.*\|\s*([^|]*)\|\s*$", readme, re.MULTILINE)
    return (
        list(dict.fromkeys(d[1:] for d in re.findall(r"#\d+", m.group(1)))) if m else []
    )


def msg_borrador(author: str, issue: str, pr: str, team: str) -> str:
    return (
        f"🆕 **@{author} empezó el Issue #{issue}** (PR en borrador #{pr}).\n\n"
        f"{team}: pueden seguir su avance en el comentario «🧭 Revisión guiada». "
        "Si ya terminaste lo tuyo, ofrece `apoyo`."
    )


def msg_listo(author: str, issue: str, pr: str, team: str) -> str:
    return (
        f"👀 **@{author} dejó el PR #{pr} listo para revisión** (Issue #{issue}).\n\n"
        f"{team}: quien tenga tiempo, revísenlo con la rúbrica (`apoyo`) y anoten en su PR a quién ayudaron."
    )


def msg_merge(author: str, issue: str, pr: str, team: str) -> str:
    return (
        f"✅ **PR #{pr} mergeado en `main`** (cierra #{issue}) — gracias @{author}.\n\n"
        f"{team}: hagan `git pull origin main` antes de seguir."
    )


def msg_desbloqueo(assignees: list[str], issue: str, pr: str, author: str) -> str:
    quien = " ".join(f"@{a}" for a in assignees) or "equipo"
    return (
        f"🔓 {quien}: **#{issue} ya está en `main`** (PR #{pr}, de @{author}). Ya puedes empezar: "
        f"`git pull origin main`, comprueba que existen los archivos de #{issue} y abre tu rama. "
        "Tu contrato y tu paso a paso están en el bloque de arriba."
    )


def comment(num: str, body: str) -> None:
    if os.environ.get("DRY_RUN"):
        print(f"--- comentario en #{num}\n{body}\n")
        return
    r = subprocess.run(
        [
            "gh",
            "api",
            "-X",
            "POST",
            f"repos/{REPO}/issues/{num}/comments",
            "--input",
            "-",
        ],
        input=json.dumps({"body": body}),
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode:
        # The notification is secondary (the PR already exists): warn, never swallow.
        detail = (r.stderr or r.stdout).strip().replace("\n", " | ")
        print(f"::warning::No se pudo comentar en #{num}: {detail}")


def unblock(readme: str, issue: str, pr: str, author: str) -> None:
    for dep in dependents_of(readme, issue):
        pendientes = [
            d
            for d in deps_of(readme, dep)
            if d
            != issue  # el Issue que se acaba de mergear se cierra con retraso: cuenta como cumplido
            and gh("api", f"repos/{REPO}/issues/{d}", "--jq", ".state").strip()
            != "closed"
        ]
        if pendientes:
            continue
        asignados = gh(
            "api",
            f"repos/{REPO}/issues/{dep}",
            "--jq",
            '[.assignees[].login]|join(" ")',
        ).split()
        comment(dep, msg_desbloqueo(asignados, issue, pr, author))
        if not os.environ.get("DRY_RUN"):
            gh("api", "-X", "DELETE", f"repos/{REPO}/issues/{dep}/labels/bloqueado")


def main() -> None:
    evento = sys.argv[1] if len(sys.argv) > 1 else "pr"
    monitor, roster = load_roster()
    with open(README, encoding="utf-8") as f:
        readme = f.read()
    if evento == "borrador":
        pr, author, issue = (
            os.environ["PR_NUM"],
            os.environ["PR_AUTHOR"],
            os.environ["ISSUE"],
        )
        comment(
            pr, msg_borrador(author, issue, pr, team_mentions(monitor, roster, author))
        )
        return
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
        ev = json.load(f)
    pr_data = ev["pull_request"]
    pr, author = str(pr_data["number"]), pr_data["user"]["login"]
    issue = issue_from_body(pr_data.get("body") or "")
    team = team_mentions(monitor, roster, author)
    es_alumno = author in roster
    accion = ev.get("action")
    if accion == "opened" and es_alumno and issue and pr_data.get("draft"):
        comment(pr, msg_borrador(author, issue, pr, team))
    elif accion == "ready_for_review" and es_alumno and issue:
        comment(pr, msg_listo(author, issue, pr, team))
    elif accion == "closed" and pr_data.get("merged") and issue:
        if es_alumno:
            comment(pr, msg_merge(author, issue, pr, team))
        unblock(readme, issue, pr, author)


if __name__ == "__main__":
    main()
