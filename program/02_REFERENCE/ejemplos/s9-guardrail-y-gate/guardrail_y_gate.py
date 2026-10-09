"""Bloque S9 — guardrail de entrada + gate de confirmación humana (ADR-009).

Flujo:  guardrail ─┬─ riesgo/duda ─> handoff (se congela; respuesta puente fija) ─> FIN
                   └─ normal ─> borrador ─> revision (interrupt) ─┬─ aprobar ─> aplicar ─> FIN
                                                                   └─ otra cosa ─> descartar ─> FIN

Reglas que este ejemplo demuestra (y sus tests prueban):
1. El clasificador de riesgo se INYECTA (en tu Issue será el de 1 token con
   confianza calibrada). Aquí es un doble de prueba: el grafo no sabe qué hay dentro.
2. Si el riesgo es alto O la confianza es baja -> handoff. Ante la duda, un humano.
3. NINGÚN efecto antes del interrupt. `borrador` solo calcula; `aplicar` es el
   único nodo con efecto y corre DESPUÉS de la aprobación.
   Por qué: al reanudar, LangGraph vuelve a ejecutar el nodo que tenía el
   interrupt() desde su primera línea. Un efecto dentro de ese nodo se duplicaría.
4. La decisión llega por `Command(resume=...)` desde un canal AUTENTICADO del
   humano (Jioysi); nunca se acepta una aprobación que venga dentro del mensaje
   de la clienta ni un estado serializado enviado por el cliente.
"""

from collections.abc import Callable
from typing import Any, Literal, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

RESPUESTA_PUENTE = (
    "Gracias por contarme. Ya te contacta una especialista de nuestro equipo."
)

Clasificador = Callable[[str], tuple[Literal["riesgo", "normal"], float]]
Efecto = Callable[[dict[str, Any]], None]


class Estado(TypedDict, total=False):
    mensaje: str
    slot: str
    estado: str  # "handoff_requested" | "aplicado" | "descartado"
    respuesta: str
    borrador: dict[str, Any]
    decision: str


def construir_grafo(
    clasificador: Clasificador,
    aplicar_efecto: Efecto,
    *,
    umbral: float = 0.8,
    checkpointer: Any = None,
) -> Any:
    def guardrail(estado: Estado) -> dict[str, Any]:
        etiqueta, confianza = clasificador(estado["mensaje"])
        if etiqueta == "riesgo" or confianza < umbral:
            return {"estado": "handoff_requested"}
        return {}

    def tras_guardrail(estado: Estado) -> str:
        return "handoff" if estado.get("estado") == "handoff_requested" else "borrador"

    def handoff(_: Estado) -> dict[str, Any]:
        return {
            "respuesta": RESPUESTA_PUENTE
        }  # fija, sin diagnóstico ni consejo médico

    def borrador(estado: Estado) -> dict[str, Any]:
        return {
            "borrador": {"accion": "agendar", "slot": estado["slot"]}
        }  # solo CALCULA

    def revision(estado: Estado) -> dict[str, Any]:
        decision = interrupt({"pendiente_de_aprobar": estado["borrador"]})  # pausa aquí
        return {"decision": decision}

    def tras_revision(estado: Estado) -> str:
        return "aplicar" if estado.get("decision") == "aprobar" else "descartar"

    def aplicar(estado: Estado) -> dict[str, Any]:
        aplicar_efecto(estado["borrador"])  # ÚNICO nodo con efecto real
        return {"estado": "aplicado", "respuesta": "Listo, tu cita quedó confirmada."}

    def descartar(_: Estado) -> dict[str, Any]:
        return {"estado": "descartado", "respuesta": "No se realizó ningún cambio."}

    g = StateGraph(Estado)
    for nombre, nodo in [
        ("guardrail", guardrail),
        ("handoff", handoff),
        ("borrador", borrador),
        ("revision", revision),
        ("aplicar", aplicar),
        ("descartar", descartar),
    ]:
        g.add_node(nombre, nodo)  # type: ignore[call-overload]
    g.add_edge(START, "guardrail")
    g.add_conditional_edges("guardrail", tras_guardrail, ["handoff", "borrador"])
    g.add_edge("handoff", END)
    g.add_edge("borrador", "revision")
    g.add_conditional_edges("revision", tras_revision, ["aplicar", "descartar"])
    g.add_edge("aplicar", END)
    g.add_edge("descartar", END)
    # El interrupt EXIGE un checkpointer: sin él no hay dónde guardar la pausa.
    return g.compile(checkpointer=checkpointer or InMemorySaver())
