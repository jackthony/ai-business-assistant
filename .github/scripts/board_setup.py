"""Deja el board listo y repetible: campo de fecha, vistas con filtros y fechas de hitos.

Idempotente: se puede correr las veces que haga falta (si el board se recrea, vuelve a quedar igual).
    python .github/scripts/board_setup.py [--dry-run]

Lo que la API de GitHub NO deja configurar (hazlo una vez a mano en la UI del board):
  - `Tabla por Semana`  -> menú de la vista -> Group by -> Semana
  - `Board por Estado`  -> menú de la vista -> Group by -> Alumno (carriles por persona)
  - `Roadmap`           -> Date fields -> Fecha objetivo
"""

import argparse
import json
import sys

from board_sync import CONFIG, gh, gql

FECHAS_OBJETIVO = {  # número de Issue -> fecha objetivo (solo las que el plan fija)
    3: "2026-10-09",  # demo del ciclo (viernes)
    4: "2026-10-09",
    5: "2026-10-07",  # su propio criterio dice 2026-10-07
    11: "2026-10-10",  # presentación del informe quincenal
    12: "2026-10-10",
    13: "2026-10-10",
    27: "2026-10-10",
}
# Hitos: viernes de la semana que indica su título (S4 empezó el lunes 2026-10-05).
HITOS = {
    "HITO 1": "2026-10-23",  # S6
    "HITO 2": "2026-11-13",  # S9
    "HITO 3": "2026-12-04",  # S12
    "Demo final": "2026-12-31",  # S16 (el 1-ene es feriado)
}
VISTAS = [  # (nombre, layout, filtro)
    ("🎯 Mis tareas", "TABLE_LAYOUT", "assignee:@me -status:Done"),
    ("📣 Disponibles (pull)", "TABLE_LAYOUT", "label:disponible -status:Done"),
    ("🧑‍🏫 Gestión del monitor", "TABLE_LAYOUT", "area:Gestión -status:Done"),
]
RENOMBRES = {
    "View 1": "📋 Resumen del proyecto"
}  # la vista por defecto no dice nada: se nombra por lo que muestra
CAMPOS_VISIBLES = [
    "Title", "Assignees", "Status", "Alumno", "Semana", "Complejidad", "Fecha objetivo",
    "Labels", "Linked pull requests", "Parent issue", "Sub-issues progress",
]  # fmt: skip


def campos(project_id: str) -> dict[str, str]:
    data = gql(
        "query($p:ID!){ node(id:$p){ ... on ProjectV2{ fields(first:50){ nodes{ ... on ProjectV2Field{ id name } "
        "... on ProjectV2SingleSelectField{ id name } ... on ProjectV2IterationField{ id name } } } } } }",
        p=project_id,
    )
    return {n["name"]: n["id"] for n in data["node"]["fields"]["nodes"] if n}


def vistas(project_id: str) -> dict[str, str]:
    data = gql(
        "query($p:ID!){ node(id:$p){ ... on ProjectV2{ views(first:30){ nodes{ id name } } } } }",
        p=project_id,
    )
    return {n["name"]: n["id"] for n in data["node"]["views"]["nodes"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    dry = parser.parse_args().dry_run
    project_id = CONFIG["project_id"]
    repo = CONFIG["repo"]

    # 1) campo "Fecha objetivo"
    ids = campos(project_id)
    if "Fecha objetivo" not in ids:
        print("+ campo 'Fecha objetivo' (DATE)")
        if not dry:
            gql(
                'mutation($p:ID!){ createProjectV2Field(input:{projectId:$p,dataType:DATE,name:"Fecha objetivo"})'
                "{ projectV2Field{ ... on ProjectV2Field{ id } } } }",
                p=project_id,
            )
            ids = campos(project_id)

    # 2) valores de fecha por Issue
    if "Fecha objetivo" in ids and not dry:
        items = gql(
            "query($p:ID!){ node(id:$p){ ... on ProjectV2{ items(first:100){ nodes{ id content{ ... on Issue{ number } } } } } } }",
            p=project_id,
        )["node"]["items"]["nodes"]
        for item in items:
            numero = (item["content"] or {}).get("number")
            if numero in FECHAS_OBJETIVO:
                gql(
                    "mutation($p:ID!,$i:ID!,$f:ID!,$d:Date!){ updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,"
                    "fieldId:$f,value:{date:$d}}){ projectV2Item{ id } } }",
                    p=project_id, i=item["id"], f=ids["Fecha objetivo"], d=FECHAS_OBJETIVO[numero],
                )  # fmt: skip
                print(f"  #{numero} -> {FECHAS_OBJETIVO[numero]}")

    # 3) vistas
    existentes = vistas(project_id)
    visibles = [ids[n] for n in CAMPOS_VISIBLES if n in ids]
    for nombre, layout, filtro in VISTAS:
        vid = existentes.get(nombre)
        if vid is None:
            print(f"+ vista '{nombre}' filtro: {filtro}")
            if dry:
                continue
            created = gql(
                "mutation($p:ID!,$n:String!){ createProjectV2View(input:{projectId:$p,name:$n,layout:" + layout + "})"
                "{ projectV2View{ id } } }",
                p=project_id, n=nombre,
            )  # fmt: skip
            vid = created["createProjectV2View"]["projectV2View"]["id"]
        else:
            print(f"= vista '{nombre}' existe: se actualiza el filtro")
        if not dry:
            gql(
                "mutation($v:ID!,$f:String!){ updateProjectV2View(input:{viewId:$v,filter:$f})"
                "{ projectV2View{ id } } }",
                v=vid, f=filtro,
            )  # fmt: skip
            if visibles:
                payload = json.dumps(visibles)
                gh(
                    "api", "graphql", "-f",
                    "query=mutation($v:ID!){ updateProjectV2View(input:{viewId:$v,configuration:{visibleFieldIds:"
                    + payload + "}}){ projectV2View{ id } } }",
                    "-f", f"v={vid}",
                )  # fmt: skip

    # 3a) nombres claros para las vistas por defecto
    for viejo, nuevo in RENOMBRES.items():
        if viejo in existentes and not dry:
            gql(
                "mutation($v:ID!,$n:String!){ updateProjectV2View(input:{viewId:$v,name:$n}){ projectV2View{ id } } }",
                v=existentes[viejo], n=nuevo,
            )  # fmt: skip
            existentes[nuevo] = existentes.pop(viejo)
            print(f"~ vista '{viejo}' -> '{nuevo}'")

    # 3b) columnas útiles también en las vistas que ya existían (no se toca su filtro)
    if not dry and visibles:
        for nombre in (
            "📋 Resumen del proyecto",
            "Tabla por Semana",
            "Board por Estado",
        ):
            if nombre in existentes:
                gh(
                    "api", "graphql", "-f",
                    "query=mutation($v:ID!){ updateProjectV2View(input:{viewId:$v,configuration:{visibleFieldIds:"
                    + json.dumps(visibles) + "}}){ projectV2View{ id } } }",
                    "-f", f"v={existentes[nombre]}",
                )  # fmt: skip

    # 4) fechas de los hitos (milestones)
    for hito in json.loads(gh("api", f"repos/{repo}/milestones?state=all")):
        for prefijo, fecha in HITOS.items():
            if hito["title"].startswith(prefijo) and not hito.get("due_on"):
                print(f"+ milestone '{hito['title']}' vence {fecha}")
                if not dry:
                    gh(
                        "api",
                        "-X",
                        "PATCH",
                        f"repos/{repo}/milestones/{hito['number']}",
                        "-f",
                        f"due_on={fecha}T23:59:59Z",
                    )
    return 0


if __name__ == "__main__":
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    raise SystemExit(main())
