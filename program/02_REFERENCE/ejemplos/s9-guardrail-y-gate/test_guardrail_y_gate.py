import os

os.environ.setdefault("LANGGRAPH_STRICT_MSGPACK", "true")

from guardrail_y_gate import RESPUESTA_PUENTE, construir_grafo
from langgraph.types import Command


def clasificador_falso(texto: str):
    """Doble de prueba: en tu Issue aquí va el clasificador de 1 token con confianza."""
    if "dolor de pecho" in texto:
        return "riesgo", 0.99
    if "no sé" in texto:
        return "normal", 0.40  # normal pero dudoso -> debe ir a humano igual
    return "normal", 0.95


def armar():
    efectos: list[dict] = []
    grafo = construir_grafo(clasificador_falso, efectos.append)
    return grafo, efectos


def cfg(hilo: str):
    return {"configurable": {"thread_id": hilo}}


def test_riesgo_se_congela_y_no_produce_efectos_ni_pausa():
    grafo, efectos = armar()
    out = grafo.invoke({"mensaje": "tengo dolor de pecho", "slot": "10:00"}, cfg("a"))
    assert out["estado"] == "handoff_requested"
    assert out["respuesta"] == RESPUESTA_PUENTE
    assert "__interrupt__" not in out
    assert efectos == []


def test_confianza_baja_tambien_va_a_humano():
    grafo, efectos = armar()
    out = grafo.invoke({"mensaje": "no sé si me conviene", "slot": "10:00"}, cfg("b"))
    assert out["estado"] == "handoff_requested"
    assert efectos == []


def test_normal_pausa_en_el_gate_sin_efectos_antes_de_aprobar():
    grafo, efectos = armar()
    out = grafo.invoke(
        {"mensaje": "quiero agendar un facial", "slot": "10:00"}, cfg("c")
    )
    assert "__interrupt__" in out  # esperando a Jioysi
    assert efectos == []  # NADA ocurrió todavía


def test_aprobar_aplica_el_efecto_exactamente_una_vez():
    grafo, efectos = armar()
    grafo.invoke({"mensaje": "quiero agendar un facial", "slot": "10:00"}, cfg("d"))
    out = grafo.invoke(Command(resume="aprobar"), cfg("d"))
    assert out["estado"] == "aplicado"
    assert efectos == [
        {"accion": "agendar", "slot": "10:00"}
    ]  # una sola vez, no duplicado al reanudar


def test_rechazar_no_aplica_nada():
    grafo, efectos = armar()
    grafo.invoke({"mensaje": "quiero agendar un facial", "slot": "10:00"}, cfg("e"))
    out = grafo.invoke(Command(resume="rechazar"), cfg("e"))
    assert out["estado"] == "descartado"
    assert efectos == []


def test_hilos_independientes_no_se_mezclan():
    grafo, efectos = armar()
    grafo.invoke({"mensaje": "agendar", "slot": "10:00"}, cfg("f1"))
    grafo.invoke({"mensaje": "agendar", "slot": "11:00"}, cfg("f2"))
    grafo.invoke(Command(resume="aprobar"), cfg("f2"))
    assert efectos == [
        {"accion": "agendar", "slot": "11:00"}
    ]  # solo el hilo aprobado produjo efecto
