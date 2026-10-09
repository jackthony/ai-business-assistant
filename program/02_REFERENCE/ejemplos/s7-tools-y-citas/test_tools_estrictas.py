import pytest
from tools_estrictas import ErrorTool, ServicioOut, consultar_servicio


def test_servicio_valido_devuelve_datos_del_catalogo():
    r = consultar_servicio({"service_id": "facial-basico"})
    assert isinstance(r, ServicioOut)
    assert r.precio_soles == 80.0


def test_espacios_alrededor_se_limpian():
    assert isinstance(
        consultar_servicio({"service_id": "  facial-basico "}), ServicioOut
    )


@pytest.mark.parametrize(
    "args",
    [
        {},  # falta el campo
        {"service_id": ""},  # vacío
        {"service_id": "FACIAL BASICO"},  # formato inválido
        {"service_id": "a" * 41},  # demasiado largo
        {"service_id": 123},  # tipo equivocado
        {
            "service_id": "facial-basico",
            "precio": 1,
        },  # argumento extra: el modelo inventó un campo
    ],
)
def test_argumentos_invalidos_devuelven_error_tipado_sin_lanzar(args):
    r = consultar_servicio(args)
    assert isinstance(r, ErrorTool)
    assert r.codigo == "argumentos_invalidos"


def test_servicio_inexistente_no_inventa_precio():
    r = consultar_servicio({"service_id": "botox-fantasma"})
    assert isinstance(r, ErrorTool)
    assert r.codigo == "servicio_no_encontrado"
