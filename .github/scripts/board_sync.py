"""Sincroniza el board (GitHub Project) con los Issues: labels, assignees y PRs -> campos.

Uso (necesita `gh` autenticado con permiso de proyectos; en CI usa BOARD_PAT):
    python .github/scripts/board_sync.py --all [--dry-run]
    python .github/scripts/board_sync.py --issue 33 [--dry-run]

Reglas (solo se ESCRIBE lo que se puede deducir; nunca se borra un valor existente):
    Alumno      <- assignee (login del roster) o label `alumno:*`
    Semana      <- label `week:S##` o título `[S## D#]` / `[S##]`
    Area        <- label `tipo:*` (feature/bug = Producto; gestion/infra/docs = Gestión)
    Complejidad <- label `complejidad:*`
    Status      <- cerrado = Done · abierto con PR abierto que lo cierra = In Progress ·
                   reabierto (estaba Done) = Todo
Los digests (`Digest semanal …`) no entran al board.
"""

import argparse
import json
import pathlib
import re
import subprocess
import sys
from typing import Any

CONFIG = json.loads(
    (pathlib.Path(__file__).resolve().parents[1] / "coach.json").read_text(
        encoding="utf-8"
    )
)
ROSTER = {a["login"]: a for a in CONFIG["alumnos"]}
LABEL_ALUMNO = {a["label"]: a["nombre"] for a in CONFIG["alumnos"]}
TIPO_A_AREA = {
    "tipo:feature": "Producto",
    "tipo:bug": "Producto",
    "tipo:gestion": "Gestión",
    "tipo:infra": "Gestión",
    "tipo:docs": "Gestión",
}
COMPLEJIDAD = {
    "complejidad:alta": "Alta",
    "complejidad:media": "Media",
    "complejidad:baja": "Baja",
}


def gh(*args: str) -> str:
    return subprocess.run(
        ["gh", *args], check=True, capture_output=True, text=True
    ).stdout


def gql(query: str, **variables: str) -> dict[str, Any]:
    cmd = ["api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        cmd += ["-f", f"{key}={value}"]
    return json.loads(gh(*cmd))["data"]  # type: ignore[no-any-return]


# ---------- lógica pura (se prueba sin red) ----------


def semana_de(title: str, labels: list[str]) -> str | None:
    for label in labels:
        if label.startswith("week:"):
            return label.split(":", 1)[1]
    found = re.search(r"\[S(\d+)(?: D\d+)?\]", title)
    return f"S{int(found.group(1))}" if found else None


def deseado(issue: dict[str, Any]) -> dict[str, str]:
    """Campos que el board DEBERÍA tener para este Issue (solo los deducibles)."""
    labels: list[str] = issue["labels"]
    out: dict[str, str] = {}
    for login in issue["assignees"]:
        if login in ROSTER:
            out["Alumno"] = ROSTER[login]["nombre"]
            break
    else:
        for label in labels:
            if label in LABEL_ALUMNO:
                out["Alumno"] = LABEL_ALUMNO[label]
    semana = semana_de(issue["title"], labels)
    if semana:
        out["Semana"] = semana
    for label in labels:
        if label in TIPO_A_AREA:
            out["Area"] = TIPO_A_AREA[label]
            break
    for label in labels:
        if label in COMPLEJIDAD:
            out["Complejidad"] = COMPLEJIDAD[label]
            break
    if issue["state"] == "CLOSED":
        out["Status"] = "Done"
    elif issue.get("pr_abierto"):
        out["Status"] = "In Progress"
    elif issue.get("status_actual") == "Done":
        out["Status"] = "Todo"  # reabierto
    return out


def cambios(actual: dict[str, str | None], quiere: dict[str, str]) -> dict[str, str]:
    return {
        campo: valor for campo, valor in quiere.items() if actual.get(campo) != valor
    }


def es_digest(title: str) -> bool:
    return title.startswith("Digest semanal")


def debe_estar_en_board(issue: dict[str, Any]) -> bool:
    if es_digest(issue["title"]):
        return False
    return any(
        label.startswith(("tipo:", "week:", "alumno:")) or label in {"hito", "senati"}
        for label in issue["labels"]
    )


# ---------- acceso a GitHub ----------

FIELDS_Q = """query($p:ID!){ node(id:$p){ ... on ProjectV2{ fields(first:50){ nodes{
  ... on ProjectV2Field{ id name } ... on ProjectV2SingleSelectField{ id name options{ id name } } } } } } }"""

ITEMS_Q = """query($p:ID!,$c:String){ node(id:$p){ ... on ProjectV2{ items(first:100,after:$c){
  pageInfo{ hasNextPage endCursor }
  nodes{ id content{ __typename ... on Issue{ id number title state
      labels(first:30){ nodes{ name } } assignees(first:5){ nodes{ login } }
      closedByPullRequestsReferences(first:5,includeClosedPrs:false){ nodes{ number state } } } }
    fieldValues(first:30){ nodes{ __typename
      ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2Field{ name } } }
      ... on ProjectV2ItemFieldSingleSelectValue{ name field{ ... on ProjectV2SingleSelectField{ name } } } } } } } } } }"""


def cargar_campos(project_id: str) -> dict[str, dict[str, Any]]:
    nodes = gql(FIELDS_Q, p=project_id)["node"]["fields"]["nodes"]
    return {n["name"]: n for n in nodes if n}


def cargar_items(project_id: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    variables: dict[str, str] = {"p": project_id}
    while True:
        data = gql(ITEMS_Q, **variables)["node"]["items"]
        items += data["nodes"]
        if not data["pageInfo"]["hasNextPage"]:
            return items
        variables["c"] = data["pageInfo"]["endCursor"]


def normalizar(
    item: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, str | None]] | None:
    content = item["content"]
    if not content or content.get("__typename") != "Issue":
        return None
    valores: dict[str, str | None] = {}
    for fv in item["fieldValues"]["nodes"]:
        if not fv or "field" not in fv or not fv["field"]:
            continue
        valores[fv["field"]["name"]] = (
            fv.get("text") if fv["__typename"].endswith("TextValue") else fv.get("name")
        )
    issue = {
        "id": content["id"],
        "number": content["number"],
        "title": content["title"],
        "state": content["state"],
        "labels": [n["name"] for n in content["labels"]["nodes"]],
        "assignees": [n["login"] for n in content["assignees"]["nodes"]],
        "pr_abierto": any(
            p["state"] == "OPEN"
            for p in content["closedByPullRequestsReferences"]["nodes"]
        ),
        "status_actual": valores.get("Status"),
    }
    return issue, valores


def escribir(project_id: str, item_id: str, campo: dict[str, Any], valor: str) -> bool:
    if "options" in campo:
        opcion = next((o["id"] for o in campo["options"] if o["name"] == valor), None)
        if opcion is None:
            print(
                f"   ! opción '{valor}' no existe en '{campo['name']}'", file=sys.stderr
            )
            return False
        value = "{singleSelectOptionId:$v}"
        v = opcion
    else:
        value = "{text:$v}"
        v = valor
    gql(
        "mutation($p:ID!,$i:ID!,$f:ID!,$v:String!){ updateProjectV2ItemFieldValue(input:"
        "{projectId:$p,itemId:$i,fieldId:$f,value:"
        + value
        + "}){ projectV2Item{ id } } }",
        p=project_id,
        i=item_id,
        f=campo["id"],
        v=v,
    )
    return True


def agregar(project_id: str, issue_node_id: str) -> str:
    data = gql(
        "mutation($p:ID!,$c:ID!){ addProjectV2ItemById(input:{projectId:$p,contentId:$c}){ item{ id } } }",
        p=project_id,
        c=issue_node_id,
    )
    return data["addProjectV2ItemById"]["item"]["id"]  # type: ignore[no-any-return]


def issues_abiertos_fuera(en_board: set[int]) -> list[dict[str, Any]]:
    repo = CONFIG["repo"]
    raw = json.loads(
        gh(
            "issue",
            "list",
            "--repo",
            repo,
            "--state",
            "open",
            "--limit",
            "200",
            "--json",
            "id,number,title,labels,assignees,state",
        )
    )
    out = []
    for r in raw:
        if r["number"] in en_board:
            continue
        out.append(
            {
                "id": r["id"],
                "number": r["number"],
                "title": r["title"],
                "state": r["state"],
                "labels": [lab["name"] for lab in r["labels"]],
                "assignees": [a["login"] for a in r["assignees"]],
                "pr_abierto": False,
                "status_actual": None,
            }
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--all", action="store_true")
    grupo.add_argument("--issue", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    project_id = CONFIG["project_id"]
    campos = cargar_campos(project_id)
    items = {}
    for item in cargar_items(project_id):
        norm = normalizar(item)
        if norm:
            items[norm[0]["number"]] = (item["id"], norm[0], norm[1])

    pendientes: list[tuple[str | None, dict[str, Any], dict[str, str | None]]] = [
        (iid, issue, valores) for iid, issue, valores in items.values()
    ]
    for issue in issues_abiertos_fuera(set(items)):
        if debe_estar_en_board(issue):
            pendientes.append((None, issue, {}))

    total = 0
    for item_id, issue, valores in pendientes:
        if args.issue is not None and issue["number"] != args.issue:
            continue
        quiere = deseado(issue)
        diff = cambios(valores, quiere)
        if item_id is None:
            print(f"#{issue['number']}: AGREGAR al board + {diff}")
            if not args.dry_run:
                item_id = agregar(project_id, issue["id"])
            else:
                total += 1
                continue
        elif diff:
            print(f"#{issue['number']}: {diff}")
        for campo, valor in diff.items():
            if campo in campos and not args.dry_run:
                escribir(project_id, item_id, campos[campo], valor)
        total += 1 if diff or item_id is None else 0
    print(f"{'(dry-run) ' if args.dry_run else ''}{total} issue(s) con cambios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
