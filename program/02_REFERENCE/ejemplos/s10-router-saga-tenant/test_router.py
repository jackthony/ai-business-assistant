import pytest
from router import RUTAS, clasificar_rapido, construir_router

# (mensaje, ruta esperada, via esperada)
CASOS = [
    ("¿Cuánto cuesta la limpieza facial?", "info", "regla"),
    ("¿Qué promociones tienen?", "info", "regla"),
    ("Quiero agendar una cita", "citas", "regla"),
    ("¿Qué horarios tienen disponibles el lunes?", "citas", "regla"),
    ("Necesito reprogramar mi cita", "citas", "regla"),
    ("Ya pagué por Yape, te envío el comprobante", "checkout", "regla"),
    ("Hice la transferencia", "checkout", "regla"),
    ("Tengo mucho dolor y sangrado", "safety", "regla"),
    ("Estoy embarazada, ¿puedo hacerme un facial?", "safety", "regla"),
    (
        "Cuánto cuesta y tengo una alergia fuerte",
        "safety",
        "regla",
    ),  # seguridad gana aunque pregunte precio
    ("Hola", "info", "llm"),  # sin señal -> el fallback decide
    (
        "Quiero saber el precio y agendar",
        "citas",
        "llm",
    ),  # dos intenciones -> el fallback decide
    ("ok gracias", "info", "llm"),
]


def fallback_falso(texto: str) -> str:
    return "citas" if "agendar" in texto else "info"


@pytest.mark.parametrize(("mensaje", "ruta", "via"), CASOS)
def test_ruteo(mensaje, ruta, via):
    salida = construir_router(fallback_falso).invoke({"mensaje": mensaje})
    assert (salida["ruta"], salida["via"]) == (ruta, via)
    assert salida["visitados"] == [
        ruta
    ]  # el grafo realmente pasó por el agente elegido


def test_reglas_no_llaman_al_llm():
    llamadas: list[str] = []

    def espia(texto: str) -> str:
        llamadas.append(texto)
        return "info"

    construir_router(espia).invoke({"mensaje": "Quiero agendar una cita"})
    assert llamadas == []


def test_respuesta_basura_del_llm_cae_a_humano_no_a_una_ruta_inventada():
    salida = construir_router(lambda _: "borrar_base_de_datos").invoke(
        {"mensaje": "Hola"}
    )
    assert salida["ruta"] == "safety"


def test_clasificar_rapido_devuelve_none_si_es_ambiguo():
    assert clasificar_rapido("hola") is None
    assert clasificar_rapido("precio y agendar") is None
    assert set(RUTAS) == {"info", "citas", "checkout", "safety"}
