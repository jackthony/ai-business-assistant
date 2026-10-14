#!/usr/bin/env python3
"""Genera el corpus sintético v2 de Hola Mujer (conversaciones inventadas, con semilla).

Las conversaciones son ficticias: no hay nombres, teléfonos ni textos reales. Lo que se
reproduce son patrones agregados del Excel operativo (hojas 03, 05, 07 y 09); cada parámetro
de `PARAMS` dice de qué hoja sale y si es *medido* o *supuesto*.

Uso: python tools/corpus/generar_sinteticas.py [--n-natural 80] [--n-cobertura 20] [--seed N]
Salida: data/conversaciones/sinteticas_v2.jsonl + INDICE_v2.md
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "conversaciones"
LIMA = timezone(timedelta(hours=-5))
SEED = 20261014

# Cada parámetro: valor + fuente + tipo ("medido" sale de una hoja; "supuesto" no tiene dato).
PARAMS: dict[str, dict[str, object]] = {
    "escenarios": {
        "valor": {
            "servicios": 15,
            "ubicacion": 7,
            "agenda": 6,
            "gestion_cita": 6,
            "ruido": 3,
        },
        "tipo": "medido (menos «ruido»)",
        "fuente": "03_EVENTOS.automation_flow: HM_WA_20_SERVICIOS=15, HM_WA_10_UBICACION=7, "
        "HM_WA_30_AGENDA=6, HM_WA_40_GESTION_CITA=6. «ruido»=3 es supuesto: 07 dice que "
        "aparecen proveedores, auto-reply y pruebas, sin conteo.",
    },
    "servicio": {
        "valor": {
            "vitaminas_hierro": 24,
            "moldeamiento": 7,
            "verrugas_lunares": 5,
            "glow": 3,
        },
        "tipo": "medido",
        "fuente": "07_APRENDIZAJES_INBOX «Servicios»: 39 vistas con servicio identificable.",
    },
    "canal_manychat": {
        "valor": 0.7,
        "tipo": "supuesto",
        "fuente": "Sin fuente: valor arbitrario (v1 usó 7/3, que tampoco está medido). El Excel no distingue canal por conversación.",
    },
    "p_horario_elegido": {
        "valor": round(2 / 33, 4),
        "tipo": "medido",
        "fuente": "07 «Agendamiento»: 33 invitaciones a agendar, 2 horarios elegidos.",
    },
    "p_seguimiento": {
        "valor": round(8 / 33, 4),
        "tipo": "medido",
        "fuente": "07 «Agendamiento»: 8 seguimientos sobre 33 invitaciones.",
    },
    "gestion_cita": {
        "valor": {"reprogramar": 6, "cancelar": 6},
        "tipo": "medido",
        "fuente": "03_EVENTOS.event_type: RESCHEDULED=6, CANCELLED=6.",
    },
    "p_ciudad_otra": {
        "valor": 0.25,
        "tipo": "supuesto",
        "fuente": "07 «Ubicación»: hay fricción por descubrir tarde que la atención es en Chimbote; "
        "la frecuencia no está medida.",
    },
    "p_nota_voz": {
        "valor": 0.2,
        "tipo": "supuesto",
        "fuente": "Las notas de voz aparecen en la muestra; la frecuencia no está medida.",
    },
    "p_duda_clinica": {
        "valor": 0.15,
        "tipo": "supuesto",
        "fuente": "07 «Seguridad clínica»: preguntas que requieren criterio humano; sin frecuencia.",
    },
    "p_pide_persona": {
        "valor": 0.2,
        "tipo": "supuesto",
        "fuente": "03_EVENTOS: HANDOFF_REQUESTED=19 de 47 eventos; no separa causas.",
    },
    "p_agenda_confirma": {
        "valor": 0.5,
        "tipo": "supuesto",
        "fuente": "Sin dato: cuántos clientes que piden agendar completan la coordinación.",
    },
}

# Catálogo aprobado (05_SERVICIOS, activo=YES). Glow no figura: el bot no da precio y escala.
CATALOGO: dict[str, dict[str, object]] = {
    "vitaminas_hierro": {
        "categoria": "1",
        "items": [("Hierro intravenoso", "89.99"), ("Cóctel de vitaminas", "149.99")],
        "frases": [
            "cuanto sale el hierro",
            "precio de las vitaminas",
            "info del hierro intravenoso",
        ],
    },
    "moldeamiento": {
        "categoria": "2",
        "items": [("Reducción de medidas", "59.99")],
        "frases": [
            "cuanto cuesta el moldeamiento corporal",
            "precio de reduccion de medidas",
        ],
    },
    "verrugas_lunares": {
        "categoria": "3",
        "items": [
            ("Eliminación de verrugas", "49.99"),
            ("Eliminación de lunares", "49.99"),
        ],
        "frases": ["precio para quitar verrugas", "cuanto sale sacar un lunar"],
    },
    "glow": {
        "categoria": "",
        "items": [],
        "frases": ["cuanto cuesta el glow", "info del protocolo glow"],
    },
}

DIRECCION = (
    "Atendemos en la Urb. Nicolás Garatea, Nuevo Chimbote, en el local de Oral Imagen, "
    "segundo piso. De 15:00 a 19:00, todos los días; los domingos y toda cita, previa coordinación."
)
OPCIONES = (
    "1) Info de servicios\n2) Sucursal y atención\n3) Que te responda una persona"
)
MENU = f"Mándame solo el número de tu consulta:\n{OPCIONES}"
CATEGORIAS = (
    "Escribe el número de lo que buscas:\n"
    "1. Terapias complementarias\n2. Estética corporal\n"
    "3. Procedimientos dermatocosméticos\n4. Hablar con una asesora"
)
NO_ENTENDI = (
    f"No entendí tu mensaje 😅\nSolo escribe el número de la opción:\n{OPCIONES}"
)
N8N_GENERICO = (
    "¡Hola, bienvenida! 😊 Gracias por escribirnos y por tu interés en nuestros servicios. "
    "Trabajamos terapias complementarias, estética corporal y procedimientos dermatocosméticos, "
    "y todos requieren una evaluación previa. ¿Sobre cuál te gustaría saber más?"
)
N8N_REPITE = (
    "¡Hola de nuevo! 😊 Gracias por tu mensaje. Te cuento que tenemos terapias complementarias, "
    "estética corporal y procedimientos dermatocosméticos, todos con evaluación previa. "
    "¿Quieres que te cuente de alguno en especial?"
)
ACUSES = ["ok", "gracias", "ok gracias", "lo voy a pensar", "listo"]
COBERTURA = (
    ["cita"] * 4
    + ["reprogramar"] * 3
    + ["cancelar"] * 3
    + ["clinica"] * 4
    + ["ciudad_otra"] * 3
    + ["n8n_repite"] * 3
)
RUIDO = {
    "proveedor": "Hola, ofrecemos insumos con descuento para consultorios, ¿con quién coordino?",
    "prueba": "PRUEBA",
    "auto_reply": "Gracias por contactarnos. En este momento no podemos atenderte.",
}


def _cuotas(pesos: dict[str, int], total: int) -> list[str]:
    """Reparte `total` según los pesos con el método del resto mayor (resultado exacto)."""
    suma = sum(pesos.values())
    base = {k: total * v // suma for k, v in pesos.items()}
    resto = sorted(pesos, key=lambda k: (total * pesos[k]) % suma, reverse=True)
    for k in resto[: total - sum(base.values())]:
        base[k] += 1
    return [k for k, n in base.items() for _ in range(n)]


class Conv:
    """Acumula los mensajes de una conversación con marcas de tiempo crecientes."""

    def __init__(self, rng: random.Random, canal: str) -> None:
        self.rng = rng
        self.canal = canal
        dia = datetime(2026, 8, 18, tzinfo=LIMA) + timedelta(days=rng.randint(0, 46))
        self.ts = dia.replace(hour=rng.randint(9, 21), minute=rng.randint(0, 59))
        self.msgs: list[tuple[str, str, str]] = []

    def add(self, emisor: str, texto: str, espera: tuple[int, int] = (4, 90)) -> None:
        self.ts += timedelta(seconds=self.rng.randint(*espera))
        self.msgs.append((emisor, texto, self.ts.isoformat()))

    @property
    def bot(self) -> str:
        return f"bot_{self.canal}"

    def saludo(self) -> str:
        h = self.ts.hour
        return (
            "Buenos días" if h < 12 else "Buenas tardes" if h < 19 else "Buenas noches"
        )

    def menu(self) -> None:
        self.add(
            self.bot, f"{self.saludo()} 👋 Gracias por escribirnos.\n{MENU}", (2, 6)
        )

    def humano(self, texto: str) -> None:
        self.add("humano", texto, (600, 14400))


def _p(nombre: str) -> float:
    return float(PARAMS[nombre]["valor"])  # type: ignore[arg-type]


def _derivar(c: Conv, motivo: str) -> None:
    """El cliente termina con una persona; el humano responde sin dar consejo clínico."""
    c.add("cliente", c.rng.choice(["3", "una persona porfa", "xfa con una persona"]))
    c.humano(
        "Hola linda, disculpa la espera 🙏 Soy Jioysi, la obstetra del equipo. ¿En qué te ayudo?"
    )
    if motivo == "clinica":
        c.add("cliente", "tengo una duda de si me conviene o si es para mi caso")
        c.humano(
            "Esa duda la resuelve la obstetra en la evaluación; por aquí no puedo opinar. "
            "Atendemos de 15:00 a 19:00, ¿qué día te viene bien?"
        )
    elif motivo == "glow":
        c.humano(
            "El protocolo Glow requiere evaluación previa, ahí te explican todo. ¿Qué día te viene bien?"
        )


HORARIOS = [
    ("mañana a las 4 porfa", 16),
    ("el jueves a las 5", 17),
    ("hoy a las 6 se puede?", 18),
    ("el viernes a las 3", 15),
]


def _elegir_horario(c: Conv) -> None:
    """El cliente propone una hora dentro del horario de atención y el humano la anota."""
    texto, hora = c.rng.choice(HORARIOS)
    c.add("cliente", texto)
    c.humano(f"Listo, te anoto a las {hora}:00 para tu evaluación 🙌 ¡Nos vemos!")


def _cerrar_agenda(c: Conv, forzar_cita: bool) -> str:
    """Tras la invitación a agendar: horario elegido, seguimiento o abandono (tasas medidas)."""
    r = c.rng.random()
    if forzar_cita or r < _p("p_horario_elegido"):
        _elegir_horario(c)
        return "cita"
    if r < _p("p_horario_elegido") + _p("p_seguimiento"):
        c.add(
            "humano",
            "Hola, ¿pudiste revisar el horario para tu evaluación? 😊",
            (86400, 90000),
        )
        return "seguimiento"
    c.add("cliente", c.rng.choice(ACUSES))
    return "abandono"


def _servicios(c: Conv, svc: str, force: str | None) -> str:
    rng = c.rng
    datos = CATALOGO[svc]
    frase = str(rng.choice(datos["frases"]))  # type: ignore[arg-type]
    if c.canal == "n8n":
        c.add("cliente", frase)
        c.add(c.bot, N8N_GENERICO, (2, 8))
        c.add(
            "cliente",
            "solo quiero saber el precio"
            if rng.random() < 0.5
            else "no era eso lo q pregunte",
        )
        c.add(c.bot, N8N_REPITE, (2, 8))
        c.add("cliente", rng.choice(ACUSES))
        return "n8n_sin_precio"
    if rng.random() < 0.5:
        c.add("cliente", rng.choice(["hola", "buenas", "hola buenas tardes"]))
        c.menu()
        c.add("cliente", frase)
    else:
        c.add("cliente", frase)
        c.menu()
    if rng.random() < _p("p_nota_voz"):
        c.add("cliente", "[nota de voz]")
        c.add(c.bot, NO_ENTENDI, (2, 6))
    if svc == "glow" or (force is None and rng.random() < _p("p_pide_persona")):
        _derivar(c, "glow" if svc == "glow" else "persona")
        return "handoff"
    c.add("cliente", "1")
    c.add(c.bot, CATEGORIAS, (2, 6))
    c.add("cliente", str(datos["categoria"]))
    items = datos["items"]
    detalle = " y ".join(f"{n} S/ {p}" for n, p in items)  # type: ignore[attr-defined]
    c.add(
        c.bot,
        f"Como referencia: {detalle}. Primero se hace una evaluación con la obstetra para ver qué "
        "te conviene 😊 ¿Quieres agendar tu evaluación?",
        (2, 6),
    )
    if force == "clinica" or (force is None and rng.random() < _p("p_duda_clinica")):
        c.add("cliente", "tengo una duda de si me conviene o si es para mi caso")
        c.humano(
            "Esa duda la resuelve la obstetra en la evaluación; por aquí no puedo opinar."
        )
        return "handoff_clinico"
    if force == "ciudad_otra" or (force is None and rng.random() < _p("p_ciudad_otra")):
        c.add(
            "cliente",
            rng.choice(["estoy en lima", "vivo en trujillo", "soy de chiclayo"]),
        )
        c.add(c.bot, DIRECCION, (2, 6))
        c.add("cliente", rng.choice(["ah ok, gracias", "uy queda lejos"]))
        return "ciudad_otra"
    return _cerrar_agenda(c, force == "cita")


def _ubicacion(c: Conv, force: str | None) -> str:
    rng = c.rng
    c.add(
        "cliente",
        rng.choice(
            ["donde quedan?", "en que distrito atienden", "a que hora atienden"]
        ),
    )
    if c.canal == "n8n":
        c.add(
            c.bot,
            "¡Hola! 😊 Atendemos en Chimbote. Para más detalles te contactará una asesora.",
            (2, 8),
        )
        c.add("cliente", rng.choice(ACUSES))
        return "n8n_ubicacion_vaga"
    c.menu()
    c.add("cliente", "2")
    c.add(c.bot, DIRECCION, (2, 6))
    if force == "ciudad_otra" or (force is None and rng.random() < _p("p_ciudad_otra")):
        c.add("cliente", rng.choice(["estoy en lima", "vivo en piura"]))
        return "ciudad_otra"
    c.add("cliente", rng.choice(["gracias", "ok gracias 😊"]))
    return "ubicacion_ok"


def _agenda(c: Conv, force: str | None) -> str:
    rng = c.rng
    c.add(
        "cliente",
        rng.choice(
            ["quiero agendar una cita", "se puede sacar cita?", "quiero una evaluación"]
        ),
    )
    if c.canal == "n8n":
        c.add(c.bot, N8N_GENERICO, (2, 8))
        c.add("cliente", "quiero agendar")
        c.add(c.bot, N8N_REPITE, (2, 8))
        return "n8n_repite"
    c.menu()
    _derivar(c, "persona")
    c.add(
        "cliente", rng.choice(["para el hierro", "para lunares", "para moldeamiento"])
    )
    c.humano("Perfecto 😊 Atendemos de 15:00 a 19:00, ¿qué día y hora te viene bien?")
    if force == "cita" or (force is None and rng.random() < _p("p_agenda_confirma")):
        _elegir_horario(c)
        return "cita"
    return "abandono"


def _gestion(c: Conv, tipo: str) -> str:
    c.add(
        "cliente",
        "quiero cambiar mi cita"
        if tipo == "reprogramar"
        else "quiero cancelar mi cita",
    )
    c.menu()
    _derivar(c, "persona")
    if tipo == "reprogramar":
        c.add(
            "cliente", c.rng.choice(["para el viernes a las 4", "mejor la otra semana"])
        )
        c.humano("Listo, tu cita queda reprogramada 🙌")
    else:
        c.humano("Listo, la cancelo. Cuando quieras reagendar me escribes 😊")
    return tipo


def _ruido(c: Conv, tipo: str) -> str:
    c.add("cliente", RUIDO[tipo])
    c.menu()
    return f"ruido_{tipo}"


def construir(
    rng: random.Random, escenario: str, canal: str, svc: str, force: str | None
) -> tuple[Conv, str]:
    """Devuelve la conversación y su desenlace."""
    c = Conv(rng, canal)
    if escenario == "servicios":
        return c, _servicios(c, svc, force)
    if escenario == "ubicacion":
        return c, _ubicacion(c, force)
    if escenario == "agenda":
        return c, _agenda(c, force)
    if escenario == "gestion_cita":
        tipo = (
            force
            if force in ("reprogramar", "cancelar")
            else rng.choice(["reprogramar", "cancelar"])
        )
        return c, _gestion(c, tipo)
    return c, _ruido(c, rng.choice(list(RUIDO)))


def generar(n_natural: int, n_cobertura: int, seed: int) -> list[dict[str, object]]:
    rng = random.Random(seed)
    pesos_esc: dict[str, int] = PARAMS["escenarios"]["valor"]  # type: ignore[assignment]
    pesos_svc: dict[str, int] = PARAMS["servicio"]["valor"]  # type: ignore[assignment]
    plan: list[tuple[str, str, str | None]] = []
    esc_list = _cuotas(pesos_esc, n_natural)
    svc_n = _cuotas(pesos_svc, esc_list.count("servicios"))
    rng.shuffle(esc_list)
    rng.shuffle(svc_n)
    for esc in esc_list:
        plan.append(("natural", esc, svc_n.pop() if esc == "servicios" else ""))
    cob = [COBERTURA[i % len(COBERTURA)] for i in range(n_cobertura)]
    svcs = [k for k in CATALOGO if k != "glow"]
    for i, f in enumerate(cob):
        esc = (
            "gestion_cita"
            if f in ("reprogramar", "cancelar")
            else "servicios"
            if f != "n8n_repite"
            else "agenda"
        )
        plan.append(("cobertura", esc, svcs[i % len(svcs)]))
    filas: list[dict[str, object]] = []
    for i, (split, esc, svc) in enumerate(plan, start=1):
        force = None if split == "natural" else cob[i - 1 - n_natural]
        if esc in ("gestion_cita", "ruido"):
            canal = "manychat"
        elif force == "n8n_repite":
            canal = "n8n"
        elif force is not None:
            canal = "manychat"
        else:
            canal = "manychat" if rng.random() < _p("canal_manychat") else "n8n"
        c, desenlace = construir(rng, esc, canal, svc, force)
        for turno, (emisor, texto, ts) in enumerate(c.msgs, start=1):
            filas.append(
                {
                    "conversacion_id": f"conv_v2_{i:04d}",
                    "turno": turno,
                    "rol": "user" if emisor == "cliente" else "assistant",
                    "texto": texto,
                    "ts": ts,
                    "canal": canal,
                    "origen": "sintetica",
                    "emisor": emisor,
                    "escenario": esc,
                    "desenlace": desenlace,
                    "split": split,
                }
            )
    return filas


def indice(filas: list[dict[str, object]], seed: int) -> str:
    convs = {f["conversacion_id"]: f for f in filas}
    por = Counter((f["split"], f["escenario"]) for f in convs.values())
    canal = Counter(f["canal"] for f in convs.values())
    desenlace = Counter(f["desenlace"] for f in convs.values())
    out = [
        "# Índice de conversaciones sintéticas (v2)",
        "",
        (
            f"Generado por `tools/corpus/generar_sinteticas.py` (semilla {seed}): {len(convs)} "
            f"conversaciones, {len(filas)} mensajes. **No editar a mano**: se regenera."
        ),
        "",
        (
            "> **Datos ficticios.** No hay chats, nombres ni teléfonos reales. Reproducen patrones "
            "agregados del Excel operativo; la tabla de abajo dice cuáles son *medidos* y cuáles "
            "*supuestos*. Sirven para probar el comportamiento del bot y armar evals, **no** para "
            "estimar conversión real (la hoja 07 lo descarta). El split `natural` sigue las "
            "frecuencias medidas; el `cobertura` fuerza caminos poco frecuentes (cita, cancelar, "
            "reprogramar, duda clínica, otra ciudad, n8n que repite)."
        ),
        "",
        "## Composición",
        "",
        "| split | escenario | conversaciones |",
        "|---|---|---|",
    ]
    out += [f"| {s} | {e} | {n} |" for (s, e), n in sorted(por.items())]
    out += [
        "",
        f"Canal: {dict(canal)}",
        "",
        "Desenlaces: " + ", ".join(f"{k} {v}" for k, v in sorted(desenlace.items())),
        "",
    ]
    out += [
        "## Parámetros y su fuente",
        "",
        "| parámetro | valor | tipo | fuente |",
        "|---|---|---|---|",
    ]
    for nombre, p in PARAMS.items():
        out.append(
            f"| `{nombre}` | `{json.dumps(p['valor'], ensure_ascii=False)}` | {p['tipo']} | {p['fuente']} |"
        )
    out.append("")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-natural", type=int, default=80)
    ap.add_argument("--n-cobertura", type=int, default=20)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR)
    a = ap.parse_args()
    filas = generar(a.n_natural, a.n_cobertura, a.seed)
    a.out_dir.mkdir(parents=True, exist_ok=True)
    jsonl = "\n".join(json.dumps(f, ensure_ascii=False) for f in filas) + "\n"
    (a.out_dir / "sinteticas_v2.jsonl").write_text(jsonl, encoding="utf-8")
    (a.out_dir / "INDICE_v2.md").write_text(indice(filas, a.seed), encoding="utf-8")
    print(
        f"{len({f['conversacion_id'] for f in filas})} conversaciones, {len(filas)} mensajes"
    )


if __name__ == "__main__":
    main()
