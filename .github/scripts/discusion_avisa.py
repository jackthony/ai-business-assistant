"""Avisa al equipo de cada discusión nueva: comenta mencionando (@) al resto del equipo.

Se ejecuta en el evento `discussion` (created). Un comentario con @menciones hace que GitHub
envíe correo/notificación a cada mencionado, aunque no vigile Discussions. Ignora a los bots
(la lectura semanal ya menciona al equipo en su cuerpo). DRY_RUN=1 solo imprime.
"""

import json
import os
import subprocess


def team_mentions(monitor: str, roster: list[str], author: str) -> str:
    others = [u for u in [*roster, monitor] if u != author]
    return " ".join(f"@{u}" for u in dict.fromkeys(others))


def build_message(author: str, category: str, title: str, team: str) -> str:
    return (
        f"📣 **@{author} abrió una discusión en «{category}»:** {title}\n\n"
        f"{team}: échenle un ojo y aporten lo que sepan; si es una duda, respondan con su fuente "
        "y marquen la respuesta que ayudó. Aprendemos en público."
    )


def main() -> None:
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
        ev = json.load(f)
    disc = ev["discussion"]
    author = disc["user"]["login"]
    if disc["user"].get("type") == "Bot" or author.endswith("[bot]"):
        print("Discusión de un bot: no se avisa (ya menciona al equipo).")
        return
    with open(".github/coach.json", encoding="utf-8") as f:
        cfg = json.load(f)
    roster = [a["login"] for a in cfg["alumnos"]]
    body = build_message(
        author,
        disc["category"]["name"],
        disc["title"],
        team_mentions(cfg["monitor"], roster, author),
    )
    if os.environ.get("DRY_RUN"):
        print(body)
        return
    r = subprocess.run(
        [
            "gh",
            "api",
            "graphql",
            "-f",
            (
                "query=mutation($d:ID!,$b:String!){addDiscussionComment("
                "input:{discussionId:$d,body:$b}){comment{url}}}"
            ),
            "-f",
            f"d={disc['node_id']}",
            "-f",
            f"b={body}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        print("::warning::no pude comentar en la discusión:", r.stderr[:300])


if __name__ == "__main__":
    main()
