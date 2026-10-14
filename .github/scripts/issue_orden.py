"""Deja cada Issue «completo» en GitHub: hito, tracker padre y bloqueos.

Uso: python3 .github/scripts/issue_orden.py <numero> | --all      (DRY_RUN=1 solo imprime)
Reglas (idempotentes; nunca pisan lo que ya está puesto):
  - Hito: por semana (S01–S06 → HITO 1, S07–S09 → HITO 2, S10–S12 → HITO 3, S13–S16 → Demo final);
    sin semana pero con etiqueta coach/senati/tipo:* → «Operación del programa».
  - Tracker: un Issue con semana (título «[S05 D1] …» o etiqueta week:S05) cuelga como
    sub-issue del tracker «[S05] Semana 5 …» si no tiene ya un padre. Los «[Pull]» no (van en la cola).
  - Bloqueos: «Depende de» de la tabla Issue → contrato del README de asignaciones → `blocked by`.
"""

import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import equipo_avisa

REPO = os.environ.get("GH_REPO") or os.environ.get(
    "GITHUB_REPOSITORY", "jackthony/ai-business-assistant"
)
README = "program/01_CURRICULUM/asignaciones/README.md"
OPERACION = "Operación del programa"


def week_of(title: str, labels: list[str]) -> int | None:
    m = re.match(r"\s*\[S(\d{1,2})\b", title)
    if m:
        return int(m.group(1))
    for label in labels:
        m = re.fullmatch(r"week:S(\d{1,2})", label)
        if m:
            return int(m.group(1))
    return None


def milestone_prefix(week: int | None, labels: list[str]) -> str | None:
    if week is not None:
        if week <= 6:
            return "HITO 1"
        if week <= 9:
            return "HITO 2"
        if week <= 12:
            return "HITO 3"
        return "Demo final"
    if any(x in {"coach", "senati"} or x.startswith("tipo:") for x in labels):
        return OPERACION
    return None


def tracker_prefix(week: int) -> str:
    return f"[S{week:02d}] Semana"


def api(*args: str) -> str:
    return subprocess.run(
        ["gh", "api", *args], capture_output=True, text=True, check=False
    ).stdout


def issue(n: str) -> dict:
    return json.loads(api(f"repos/{REPO}/issues/{n}") or "{}")


def milestones() -> list[dict]:
    return json.loads(api(f"repos/{REPO}/milestones?state=open&per_page=50") or "[]")


def open_issues() -> list[dict]:
    out = json.loads(
        api(f"repos/{REPO}/issues?state=open&per_page=100", "--paginate", "--slurp")
        or "[]"
    )
    flat = (
        [i for page in out for i in page] if out and isinstance(out[0], list) else out
    )
    return [i for i in flat if "pull_request" not in i]


def log(msg: str) -> None:
    print(("(dry-run) " if os.environ.get("DRY_RUN") else "") + msg)


def ordenar(n: str, ms: list[dict], issues: list[dict], readme: str) -> None:
    it = issue(n)
    if not it or it.get("pull_request") or it.get("state") != "open":
        return
    title, labels = it["title"], [x["name"] for x in it["labels"]]
    week = week_of(title, labels)
    dry = bool(os.environ.get("DRY_RUN"))
    if it.get("milestone") is None:
        prefix = milestone_prefix(week, labels)
        ms_n = next(
            (m["number"] for m in ms if prefix and m["title"].startswith(prefix)), None
        )
        if ms_n:
            log(f"#{n}: hito {prefix}")
            if not dry:
                api(
                    "-X", "PATCH", f"repos/{REPO}/issues/{n}", "-F", f"milestone={ms_n}"
                )
    es_tracker = ("tracker" in title.lower()) or (
        it.get("sub_issues_summary") or {}
    ).get("total", 0) > 0
    if week is not None and not title.startswith("[Pull]") and not es_tracker:
        tracker = next(
            (i for i in issues if i["title"].startswith(tracker_prefix(week))), None
        )
        tiene_padre = (
            api(f"repos/{REPO}/issues/{n}/parent", "--jq", ".number").strip().isdigit()
        )
        if tracker and not tiene_padre and tracker["number"] != int(n):
            log(f"#{n}: sub-issue de #{tracker['number']}")
            if not dry:
                api(
                    "-X",
                    "POST",
                    f"repos/{REPO}/issues/{tracker['number']}/sub_issues",
                    "-F",
                    f"sub_issue_id={it['id']}",
                )
    ya = {
        b["number"]
        for b in json.loads(
            api(f"repos/{REPO}/issues/{n}/dependencies/blocked_by") or "[]"
        )
    }
    for dep in equipo_avisa.deps_of(readme, n):
        if int(dep) in ya or dep == n:
            continue
        dep_issue = issue(dep)
        if dep_issue.get("state") == "closed":
            continue
        log(f"#{n}: bloqueado por #{dep}")
        if not dry:
            api(
                "-X",
                "POST",
                f"repos/{REPO}/issues/{n}/dependencies/blocked_by",
                "-F",
                f"issue_id={dep_issue['id']}",
            )
            api(
                "-X",
                "POST",
                f"repos/{REPO}/issues/{n}/labels",
                "-f",
                "labels[]=bloqueado",
            )


def main() -> None:
    arg = sys.argv[1] if len(sys.argv) > 1 else "--all"
    with open(README, encoding="utf-8") as f:
        readme = f.read()
    ms, issues = milestones(), open_issues()
    targets = [str(i["number"]) for i in issues] if arg == "--all" else [arg]
    for n in targets:
        ordenar(n, ms, issues, readme)


if __name__ == "__main__":
    main()
