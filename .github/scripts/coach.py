"""Coach proactivo: avisa a cada practicante qué hacer, dónde mirar y cuándo.

Cada mensaje @menciona al practicante, así que GitHub lo notifica (web, correo y app móvil
según SUS ajustes; ver GUIA_PRACTICANTE.md §Notificaciones).

Modos:
    arranque   08:00 Lima  (día de práctica: foco del día, qué hacer primero, dónde mirar)
    pulso      14:00 Lima  (solo si NO hay actividad hoy: pregunta cómo va y avisa al monitor)
    cierre     17:30 Lima  (qué dejar hecho antes de irse)
    revision   evento: alguien revisó el PR de un practicante  --pr N --reviewer X --estado S
    asignado   evento: se le asignó un Issue                    --issue N --asignado X
    merge      evento: su PR se mergeó -> qué sigue (informe, pull, apoyo)  --pr N --autor X
Los modos programados escriben en el Issue "📣 Coach — <nombre>" (se crea si no existe);
los de evento escriben en el PR/Issue correspondiente.

    python .github/scripts/coach.py arranque --dry-run [--fecha 2026-10-09] [--solo adbon-dm1]
"""

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import sys
from typing import Any
from zoneinfo import ZoneInfo

CONFIG = json.loads(
    (pathlib.Path(__file__).resolve().parents[1] / "coach.json").read_text(
        encoding="utf-8"
    )
)
REPO: str = CONFIG["repo"]
MONITOR: str = CONFIG["monitor"]
BOARD: str = CONFIG["board_url"]
TZ = ZoneInfo(CONFIG["tz"])
ALUMNOS: list[dict[str, Any]] = CONFIG["alumnos"]
ROSTER = {a["login"]: a for a in ALUMNOS}
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
ACTIVIDAD = {
    "PushEvent", "PullRequestEvent", "PullRequestReviewEvent", "PullRequestReviewCommentEvent",
    "IssueCommentEvent", "IssuesEvent", "CreateEvent",
}  # fmt: skip


# ---------- lógica pura (se prueba sin red) ----------


def practica_hoy(alumno: dict[str, Any], fecha: dt.date) -> bool:
    return fecha.weekday() in alumno["dias"]


def dia_n(alumno: dict[str, Any], fecha: dt.date) -> tuple[int, int]:
    dias = sorted(alumno["dias"])
    return dias.index(fecha.weekday()) + 1, len(dias)


def hubo_actividad(eventos: list[dict[str, Any]], fecha: dt.date) -> bool:
    for ev in eventos:
        if ev.get("type") not in ACTIVIDAD or ev.get("repo", {}).get("name") != REPO:
            continue
        creado = dt.datetime.fromisoformat(ev["created_at"]).astimezone(TZ)
        if creado.date() == fecha:
            return True
    return False


def enlaces(login: str) -> str:
    return (
        f"[Board]({BOARD}) · "
        f"[Tus Issues](https://github.com/{REPO}/issues?q=is%3Aopen+assignee%3A{login}) · "
        f"[PRs que esperan tu revisión](https://github.com/{REPO}/pulls?q=is%3Aopen+is%3Apr+review-requested%3A{login}) · "
        f"[Disponibles](https://github.com/{REPO}/issues?q=is%3Aopen+label%3Adisponible+no%3Aassignee)"
    )


def lista(items: list[dict[str, Any]], vacio: str, tope: int = 5) -> str:
    if not items:
        return f"- {vacio}"
    filas = [f"- [#{i['number']} {i['title']}]({i['url']})" for i in items[:tope]]
    if len(items) > tope:
        filas.append(f"- … y {len(items) - tope} más (mira el board)")
    return "\n".join(filas)


def msg_arranque(alumno: dict[str, Any], fecha: dt.date, abiertos: list[dict[str, Any]], prs: list[dict[str, Any]],
                 disponibles: list[dict[str, Any]], por_revisar: list[dict[str, Any]], aviso: str | None) -> str:  # fmt: skip
    login = alumno["login"]
    if not practica_hoy(alumno, fecha):  # día sin práctica: solo el aviso de calendario
        return f"### 📌 @{login}\n\n{aviso}\n\n**Dónde mirar:** {enlaces(login)}"
    n, total = dia_n(alumno, fecha)
    partes = [
        f"### 🌅 Buen día, @{login} — hoy practicas (día {n} de {total} de tu semana)",
        "",
    ]
    paso = 0

    def titulo(texto: str) -> str:
        nonlocal paso
        paso += 1
        return f"**{paso}. {texto}**"

    partes += [
        titulo("Tu foco de hoy"),
        lista(
            abiertos,
            "No tienes Issues asignados abiertos 🎉 — salta a «Si terminas antes».",
        ),
        "",
    ]
    if prs:
        partes += [
            titulo("Tus PRs abiertos (¿esperan algo de ti?)"),
            lista(prs, ""),
            "",
        ]
    partes += [
        titulo("Antes de codear (5 min)"),
        "- `git pull origin main` y lee tu Issue + el bloque de tu semana en `program/01_CURRICULUM/pack_contexto.md`.",
        "- Con tu IA: un prompt = una tarea verificable (~10–15 interacciones por sesión). Tú ejecutas, verificas y firmas.",
        "- Si te trabas: tu Issue y docs → un compañero → el grupo → el monitor (orden de consulta).",
        "",
        titulo("Si terminas antes (pull, no solo push)"),
        lista(
            disponibles, "Aún no hay Issues disponibles: revisa el PR de un compañero."
        ),
    ]
    if por_revisar:
        partes += [
            "- Apoya con una revisión (cuenta como evidencia):",
            *["  " + f for f in lista(por_revisar, "", 3).split("\n")],
        ]
    partes += ["", f"**Dónde mirar:** {enlaces(login)}"]
    if aviso:
        partes += ["", f"📌 **Aviso:** {aviso}"]
    return "\n".join(partes)


def msg_pulso(alumno: dict[str, Any], abiertos: list[dict[str, Any]]) -> str:
    login = alumno["login"]
    tarea = (
        f"[#{abiertos[0]['number']}]({abiertos[0]['url']})" if abiertos else "tu Issue"
    )
    return "\n".join([
        f"### 👋 @{login}, ¿cómo vas? Todavía no veo actividad tuya hoy",
        "",
        "Es normal trabarse; lo importante es decirlo temprano:",
        f"1. Comenta en {tarea} **qué intentaste y qué error te sale** (pega el mensaje, no una captura borrosa).",
        "2. Empieza chico: un commit pequeño con su test ya cuenta (`git push` corre el CI y deja respaldo).",
        "3. Orden de consulta: tu Issue y docs → un compañero → el grupo → el monitor.",
        "",
        f"**Dónde mirar:** {enlaces(login)}",
        "",
        f"cc @{MONITOR} — sin actividad registrada hoy en día de práctica.",
    ])  # fmt: skip


def msg_cierre(
    alumno: dict[str, Any],
    fecha: dt.date,
    abiertos: list[dict[str, Any]],
    prs: list[dict[str, Any]],
) -> str:
    login = alumno["login"]
    ultimo = fecha.weekday() == max(alumno["dias"])
    partes = [f"### 🌇 Cierre del día, @{login}", ""]
    partes += [
        "**Antes de irte**",
        "- `git push` de lo que tengas (cada push corre el CI y queda respaldado).",
    ]
    if abiertos and not prs:
        partes += [
            f"- Aún no tienes PR abierto para {', '.join('#' + str(i['number']) for i in abiertos[:3])}: ábrelo aunque sea en borrador, con `Closes #N` y la plantilla."
        ]
    if prs:
        partes += [
            "- Tus PRs abiertos: revisa que el CI esté verde y que las **preguntas de comprensión** estén respondidas con tus palabras:",
            lista(prs, "", 3),
        ]
    partes += ["- Anota en tu Word FPE lo que hiciste hoy (horas y actividades)."]
    if ultimo:
        partes += [
            "",
            "🏁 **Hoy es tu último día de práctica de la semana:** deja el PR abierto, tu informe actualizado y avisa en tu Issue qué quedó pendiente.",
        ]
    else:
        partes += ["", "Mañana: `git pull origin main` antes de empezar."]
    partes += ["", f"**Dónde mirar:** {enlaces(login)}"]
    return "\n".join(partes)


ESTADOS = {
    "approved": "✅ **aprobó** tu PR: el monitor hace el merge (squash); mientras, deja respondidas las preguntas de comprensión.",
    "changes_requested": "🛠 **pidió cambios** en tu PR.",
    "commented": "💬 **dejó comentarios** en tu PR.",
}


def msg_revision(autor: str, revisor: str, estado: str) -> str:
    estado_txt = ESTADOS.get(estado.lower(), ESTADOS["commented"])
    quien = "tu compañero" if revisor in ROSTER else "el monitor"
    return "\n".join([
        f"### 🔔 @{autor}, tienes revisión: {quien} @{revisor} {estado_txt}",
        "",
        "**Qué hacer ahora (en orden):**",
        "1. Lee los comentarios (pestaña *Conversation* y *Files changed*).",
        "2. Responde las **preguntas de comprensión** con tus palabras (no pegues la respuesta de una IA).",
        "3. Corrige con commits chicos y haz `git push` (el CI vuelve a correr).",
        f"4. Cuando termines comenta aquí **«listo para revisar»** y menciona a @{MONITOR}.",
        "",
        "Si te trabas, comenta qué probaste y qué falló: es más rápido que esperar.",
    ])  # fmt: skip


def msg_asignado(login: str, numero: int, titulo: str) -> str:
    return "\n".join([
        f"### 📌 @{login}, este Issue es tuyo",
        "",
        f"**#{numero} — {titulo}**",
        "",
        "1. Lee el Issue completo y su **pack de contexto** (`program/01_CURRICULUM/pack_contexto.md`, bloque de tu semana).",
        "2. `git pull origin main` y rama `issue-" + str(numero) + "-<slug>`; commits convencionales y `Closes #" + str(numero) + "` en el PR.",
        "3. Si hay ejemplos para tu tema, corre sus tests primero: `program/02_REFERENCE/ejemplos/`.",
        "",
        f"**Dónde mirar:** {enlaces(login)}",
    ])  # fmt: skip


def msg_merge(
    autor: str,
    disponibles: list[dict[str, Any]],
    informes: list[dict[str, Any]],
    por_revisar: list[dict[str, Any]],
) -> str:
    partes = [f"### 🎉 @{autor}, tu PR se mergeó. ¿Qué sigue?", ""]
    partes += [
        "**1. Tu informe** — completa horas, seguridad (ATS) y resultados de tu tarea más significativa:",
        lista(informes, "Abre tu borrador de informe en el board."),
        "",
    ]
    partes += [
        "**2. Jala el siguiente Issue** (avisa con un comentario y asígnatelo):",
        lista(
            disponibles,
            "No hay Issues disponibles: propón algo con la plantilla «Propuesta».",
        ),
        "",
    ]
    partes += [
        "**3. Apoya a un compañero** (tu revisión cuenta como evidencia):",
        lista(por_revisar, "No hay PRs abiertos ahora."),
        "",
    ]
    partes += [f"**Dónde mirar:** {enlaces(autor)}"]
    return "\n".join(partes)


# ---------- acceso a GitHub ----------


def gh(*args: str, entrada: str | None = None) -> str:
    return subprocess.run(
        ["gh", *args], check=True, capture_output=True, text=True, input=entrada
    ).stdout


def jget(*args: str) -> Any:
    return json.loads(gh(*args) or "[]")


def con_url(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"number": i["number"], "title": i["title"], "url": i["url"]} for i in items
    ]


def asignados(login: str) -> list[dict[str, Any]]:
    raw = jget(
        "issue",
        "list",
        "--repo",
        REPO,
        "--assignee",
        login,
        "--state",
        "open",
        "--json",
        "number,title,url,labels",
    )
    return con_url(
        [i for i in raw if not any(lab["name"] == "coach" for lab in i["labels"])]
    )


def prs_de(login: str) -> list[dict[str, Any]]:
    return con_url(
        jget(
            "pr",
            "list",
            "--repo",
            REPO,
            "--author",
            login,
            "--state",
            "open",
            "--json",
            "number,title,url",
        )
    )


def disponibles() -> list[dict[str, Any]]:
    raw = jget(
        "issue",
        "list",
        "--repo",
        REPO,
        "--label",
        "disponible",
        "--state",
        "open",
        "--json",
        "number,title,url,assignees",
    )
    return sorted(
        con_url([i for i in raw if not i["assignees"]]), key=lambda i: i["number"]
    )


def prs_ajenos(login: str) -> list[dict[str, Any]]:
    raw = jget(
        "pr",
        "list",
        "--repo",
        REPO,
        "--state",
        "open",
        "--json",
        "number,title,url,author",
    )
    return con_url([p for p in raw if p["author"]["login"] != login])


def informes_de(login: str) -> list[dict[str, Any]]:
    return [i for i in asignados(login) if "informe" in i["title"].lower()]


def eventos(login: str) -> list[dict[str, Any]]:
    return jget("api", f"users/{login}/events/public?per_page=50")  # type: ignore[no-any-return]


def issue_coach(alumno: dict[str, Any], dry: bool) -> int | None:
    titulo = f"📣 Coach — {alumno['nombre']}"
    hallados = jget(
        "issue",
        "list",
        "--repo",
        REPO,
        "--state",
        "open",
        "--label",
        "coach",
        "--search",
        f"{alumno['nombre']} in:title",
        "--json",
        "number,title",
    )
    for h in hallados:
        if h["title"] == titulo:
            return int(h["number"])
    if dry:
        return None
    cuerpo = (f"Hilo personal de seguimiento de @{alumno['login']}: aquí te llegan los avisos del coach "
              f"(arranque del día, pulso, cierre). **No lo cierres.** Dónde mirar: {enlaces(alumno['login'])}")  # fmt: skip
    gh(
        "label",
        "create",
        "coach",
        "--repo",
        REPO,
        "--color",
        "5319e7",
        "--description",
        "Hilo de avisos del coach automático",
        "--force",
    )
    url = gh(
        "issue",
        "create",
        "--repo",
        REPO,
        "--title",
        titulo,
        "--label",
        "coach",
        "--assignee",
        alumno["login"],
        "--body",
        cuerpo,
    ).strip()
    return int(url.rsplit("/", 1)[1])


def publicar(
    destino: str, numero: int | None, cuerpo: str, dry: bool, tipo: str = "issue"
) -> None:
    if dry or numero is None:
        print(
            f"\n=== [{'dry-run' if dry else 'sin destino'}] {destino} ===\n{cuerpo}\n"
        )
        return
    try:
        gh(
            tipo,
            "comment",
            str(numero),
            "--repo",
            REPO,
            "--body-file",
            "-",
            entrada=cuerpo,
        )
        print(f"ok: comentario en {tipo} #{numero} ({destino})")
    except (
        subprocess.CalledProcessError
    ) as error:  # p. ej. PR de fork: token de solo lectura
        print(
            f"aviso: no pude comentar en {tipo} #{numero}: {error.stderr.strip()[:200]}",
            file=sys.stderr,
        )


# ---------- modos ----------


def modo_programado(modo: str, fecha: dt.date, dry: bool, solo: str | None) -> None:
    aviso = CONFIG.get("avisos", {}).get(fecha.isoformat())
    for alumno in ALUMNOS:
        login = alumno["login"]
        if solo and login != solo:
            continue
        if not practica_hoy(alumno, fecha) and not (modo == "arranque" and aviso):
            print(
                f"{login}: hoy ({DIAS[fecha.weekday()]}) no es día de práctica — omitido"
            )
            continue
        abiertos = asignados(login)
        if modo == "arranque":
            texto = msg_arranque(
                alumno,
                fecha,
                abiertos,
                prs_de(login),
                disponibles(),
                prs_ajenos(login),
                aviso,
            )
        elif modo == "pulso":
            if hubo_actividad(eventos(login), fecha):
                print(f"{login}: ya tuvo actividad hoy — sin aviso")
                continue
            texto = msg_pulso(alumno, abiertos)
        else:
            texto = msg_cierre(alumno, fecha, abiertos, prs_de(login))
        publicar(f"Coach — {alumno['nombre']}", issue_coach(alumno, dry), texto, dry)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "modo", choices=["arranque", "pulso", "cierre", "revision", "asignado", "merge"]
    )
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--fecha", help="YYYY-MM-DD (pruebas)")
    ap.add_argument("--solo", help="login de un solo practicante")
    ap.add_argument("--pr", type=int)
    ap.add_argument("--issue", type=int)
    ap.add_argument("--reviewer", default="")
    ap.add_argument("--estado", default="commented")
    ap.add_argument("--autor", default="")
    ap.add_argument("--asignado", default="")
    ap.add_argument("--titulo", default="")
    a = ap.parse_args()
    fecha = dt.date.fromisoformat(a.fecha) if a.fecha else dt.datetime.now(TZ).date()

    if a.modo in {"arranque", "pulso", "cierre"}:
        modo_programado(a.modo, fecha, a.dry_run, a.solo)
    elif a.modo == "revision":
        if (
            a.autor in ROSTER
            and a.reviewer
            and a.reviewer != a.autor
            and not a.reviewer.endswith("[bot]")
        ):
            publicar(
                f"PR #{a.pr}",
                a.pr,
                msg_revision(a.autor, a.reviewer, a.estado),
                a.dry_run,
                "pr",
            )
    elif a.modo == "asignado":
        if a.asignado in ROSTER and a.issue and not a.titulo.startswith("📣 Coach"):
            publicar(
                f"Issue #{a.issue}",
                a.issue,
                msg_asignado(a.asignado, a.issue, a.titulo),
                a.dry_run,
            )
    elif a.modo == "merge" and a.autor in ROSTER:
        texto = msg_merge(
            a.autor, disponibles(), informes_de(a.autor), prs_ajenos(a.autor)
        )
        publicar(f"PR #{a.pr}", a.pr, texto, a.dry_run, "pr")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
