"""Publica en Discussions la «Lectura guiada» de la semana (categoría `lectura-guiada`).

Uso: python3 .github/scripts/lectura_semanal.py [SEMANA]   (p. ej. S05; sin argumento: por fecha)
Es idempotente: si ya existe una discusión con el mismo título, no publica otra.
Si la categoría no existe todavía, avisa cómo crearla y termina sin error. DRY_RUN=1 solo imprime.
"""

import datetime
import json
import os
import subprocess
import sys
from zoneinfo import ZoneInfo

REPO = os.environ.get("GH_REPO") or os.environ.get(
    "GITHUB_REPOSITORY", "jackthony/ai-business-assistant"
)
SLUG = "lectura-guiada"


def pick_week(calendario: dict[str, str], hoy: datetime.date) -> str | None:
    """Última semana cuya fecha de inicio es <= hoy."""
    vigentes = [
        (fecha, sem) for sem, fecha in calendario.items() if fecha <= hoy.isoformat()
    ]
    return max(vigentes)[1] if vigentes else None


def render_title(semana: str, entry: dict) -> str:
    return f"📖 Lectura guiada {semana}: {entry['titulo']}"


def render_body(semana: str, entry: dict, menciones: str = "") -> str:
    fuentes = "\n".join(f"- [{f['nombre']}]({f['url']})" for f in entry["fuentes"])
    preguntas = "\n".join(f"{i}. {q}" for i, q in enumerate(entry["preguntas"], 1))
    return (
        f"## Lectura de la semana {semana}\n\n**Fuentes**\n{fuentes}\n\n**Preguntas** "
        "(responde en un comentario, **con tus palabras** y citando la fuente: archivo, doc oficial o URL)\n"
        f"{preguntas}\n\n"
        "**Cómo participar**\n"
        "- Una respuesta por persona; lee las de tus compañeros y comenta si algo no cuadra con la fuente.\n"
        "- Si usaste tu IA, cuenta **qué te respondió y cómo lo verificaste**: una IA no es autoridad.\n"
        "- Tu duda sin resolver también cuenta: es parte del aprendizaje.\n"
        "- Sin datos reales de clientes ni consejos clínicos.\n"
        + (f"\ncc {menciones}\n" if menciones else "")
    )


def roster_mentions() -> str:
    with open(".github/coach.json", encoding="utf-8") as f:
        cfg = json.load(f)
    users = [a["login"] for a in cfg["alumnos"]] + [cfg["monitor"]]
    return " ".join(f"@{u}" for u in dict.fromkeys(users))


def graphql(query: str, **vars_: str) -> dict:
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in vars_.items():
        args += ["-f", f"{k}={v}"]
    out = subprocess.run(args, capture_output=True, text=True, check=False)
    return json.loads(out.stdout or "{}")


def main() -> None:
    with open(".github/lecturas.json", encoding="utf-8") as f:
        cfg = json.load(f)
    hoy = datetime.datetime.now(ZoneInfo("America/Lima")).date() + datetime.timedelta(
        days=1
    )
    semana = sys.argv[1] if len(sys.argv) > 1 else pick_week(cfg["calendario"], hoy)
    entry = cfg["semanas"].get(semana or "")
    if not entry:
        print(f"Sin lectura configurada para {semana}: nada que publicar.")
        return
    title, body = (
        render_title(semana, entry),
        render_body(semana, entry, roster_mentions()),
    )
    if os.environ.get("DRY_RUN"):
        print(title, "\n\n", body)
        return
    owner, name = REPO.split("/")
    data = graphql(
        "query($o:String!,$n:String!){repository(owner:$o,name:$n){id "
        "discussionCategories(first:25){nodes{id slug}} "
        "discussions(first:50,orderBy:{field:CREATED_AT,direction:DESC}){nodes{title}}}}",
        o=owner,
        n=name,
    )
    repo = (data.get("data") or {}).get("repository")
    if not repo:
        print("::warning::No pude leer el repo por GraphQL:", json.dumps(data)[:300])
        return
    cat = next(
        (c["id"] for c in repo["discussionCategories"]["nodes"] if c["slug"] == SLUG),
        None,
    )
    if not cat:
        print(
            f"::warning::Falta la categoría de Discussions con slug `{SLUG}` (créala en Settings → Discussions)."
        )
        return
    if any(d["title"] == title for d in repo["discussions"]["nodes"]):
        print("Ya existe esa lectura: no se duplica.")
        return
    res = graphql(
        "mutation($r:ID!,$c:ID!,$t:String!,$b:String!){createDiscussion(input:{repositoryId:$r,"
        "categoryId:$c,title:$t,body:$b}){discussion{url}}}",
        r=repo["id"],
        c=cat,
        t=title,
        b=body,
    )
    print(json.dumps(res)[:300])


if __name__ == "__main__":
    main()
