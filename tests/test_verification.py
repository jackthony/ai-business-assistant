import pytest

from agents.verification import verify_response


def test_v1_respuesta_valida() -> None:
    resultado = verify_response("Hola\nTengo horarios de mañana.\n¿Te sirve?")
    assert resultado.ok is True
    assert resultado.reasons == []


def test_v2_mas_de_3_lineas() -> None:
    resultado = verify_response("a\nb\nc\nd")
    assert resultado.ok is False
    assert resultado.reasons == ["too_many_lines"]


def test_v3_lineas_vacias_no_cuentan() -> None:
    resultado = verify_response("Hola\n\n\n\n¿Qué día?")
    assert resultado.ok is True
    assert resultado.reasons == []


def test_v4_mas_de_1_pregunta() -> None:
    resultado = verify_response("¿Qué día? ¿A qué hora?")
    assert resultado.ok is False
    assert resultado.reasons == ["too_many_questions"]


@pytest.mark.parametrize(
    "texto",
    [
        "Cuesta S/25.",
        "Cuesta S/. 25.",
        "Cuesta S/ 25.",
    ],
)
def test_v5_precio_s(texto: str) -> None:
    resultado = verify_response(texto)
    assert resultado.ok is False
    assert resultado.reasons == ["invented_price"]


@pytest.mark.parametrize(
    "texto",
    [
        "Cuesta 120 soles.",
        "Son 120 nuevos soles.",
        "Cuesta 24,50 soles.",
        "Cuesta $25.",
        "Cuesta PEN 25.",
    ],
)
def test_v6_precio_otras_formas(texto: str) -> None:
    resultado = verify_response(texto)
    assert resultado.ok is False
    assert resultado.reasons == ["invented_price"]


@pytest.mark.parametrize(
    "texto",
    [
        "   ",
        "\n\n",
        "\t",
    ],
)
def test_v7_texto_vacio(texto: str) -> None:
    resultado = verify_response(texto)
    assert resultado.ok is False
    assert resultado.reasons == ["empty"]


def test_v8_varios_motivos_en_orden() -> None:
    resultado = verify_response("a\nb\nc\nd ¿q?\n¿r?")
    assert resultado.ok is False
    assert resultado.reasons == ["too_many_lines", "too_many_questions"]


def test_v9_numeros_no_son_precio() -> None:
    resultado = verify_response("Puedo el martes 13 a las 10.\n¿Te sirve?")
    assert resultado.ok is True
    assert resultado.reasons == []
