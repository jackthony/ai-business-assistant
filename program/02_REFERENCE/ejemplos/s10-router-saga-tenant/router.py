"""Bloque S10-A — router: reglas rápidas primero, LLM solo para lo ambiguo.

Orden de decisión (barato -> caro):
1. SEGURIDAD primero: si hay una señal clínica, la ruta es `safety`, siempre,
   aunque el mensaje también hable de precios o citas.
2. Una sola intención clara por reglas -> esa ruta (`via="regla"`, sin llamar a ningún modelo).
3. Cero o varias intenciones -> el fallback (`via="llm"`), que se INYECTA.
Cada decisión deja una traza (`ruta`, `via`) para poder auditar el ruteo.
En LangGraph el "handoff" de otros SDKs es esto: una arista condicional.
"""

import re
from collections.abc import Callable
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

REGLAS: dict[str, re.Pattern[str]] = {
    "info": re.compile(
        r"\b(precio|cu[aá]nto|cuesta|costo|servicios?|promo\w*)\b", re.IGNORECASE
    ),
    "citas": re.compile(
        r"\b(cita|agendar|reservar|horarios?|disponib\w*|reprogramar)\b", re.IGNORECASE
    ),
    "checkout": re.compile(
        r"\b(pagu\w*|yape|plin|comprobante|transferencia)\b", re.IGNORECASE
    ),
}
SEGURIDAD = re.compile(
    r"\b(dolor|sangr\w*|embaraz\w*|al[eé]rgi\w*|emergencia|mareo|fiebre)\b",
    re.IGNORECASE,
)

RUTAS = ("info", "citas", "checkout", "safety")
FallbackLLM = Callable[[str], str]


def clasificar_rapido(texto: str) -> str | None:
    """Ruta si las reglas lo deciden sin ambigüedad; None si hay que preguntar al LLM."""
    if SEGURIDAD.search(texto):
        return "safety"
    coincidencias = [ruta for ruta, patron in REGLAS.items() if patron.search(texto)]
    return coincidencias[0] if len(coincidencias) == 1 else None


class Estado(TypedDict, total=False):
    mensaje: str
    ruta: str
    via: str
    visitados: list[str]


def construir_router(fallback_llm: FallbackLLM) -> Any:
    def decidir(estado: Estado) -> dict[str, Any]:
        rapida = clasificar_rapido(estado["mensaje"])
        if rapida is not None:
            return {"ruta": rapida, "via": "regla"}
        ruta = fallback_llm(estado["mensaje"])
        # El LLM puede devolver basura: lo que no es una ruta conocida cae a un humano, no a una ruta inventada.
        return {"ruta": ruta if ruta in RUTAS else "safety", "via": "llm"}

    def elegir(estado: Estado) -> str:
        return estado["ruta"]

    def nodo(nombre: str) -> Callable[[Estado], dict[str, Any]]:
        # Nodos de juguete: en tu Issue son los agentes reales (info, citas, checkout, safety).
        return lambda estado: {"visitados": [*estado.get("visitados", []), nombre]}

    g = StateGraph(Estado)
    g.add_node("decidir", decidir)  # type: ignore[call-overload]
    for ruta in RUTAS:
        g.add_node(ruta, nodo(ruta))  # type: ignore[call-overload]
        g.add_edge(ruta, END)
    g.add_edge(START, "decidir")
    g.add_conditional_edges("decidir", elegir, list(RUTAS))
    return g.compile()
