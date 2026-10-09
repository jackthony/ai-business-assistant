import pytest
from aislamiento_tenant import TenantDesconocido, coleccion_rag, resolver_tenant

PERMITIDOS = frozenset({"hola_mujer", "neuracode"})


def test_cada_tenant_tiene_su_propia_coleccion():
    assert coleccion_rag("hola_mujer", PERMITIDOS) == "hola_mujer__servicios"
    assert coleccion_rag("neuracode", PERMITIDOS) != coleccion_rag(
        "hola_mujer", PERMITIDOS
    )


@pytest.mark.parametrize(
    "candidato",
    [
        "",
        "otro_negocio",
        "HOLA_MUJER",
        "hola_mujer; drop",
        "../neuracode",
        "hola-mujer",
        "a",
    ],
)
def test_tenant_desconocido_o_con_forma_rara_es_error(candidato):
    with pytest.raises(TenantDesconocido):
        resolver_tenant(candidato, PERMITIDOS)


def test_el_error_no_repite_el_valor_recibido():
    with pytest.raises(TenantDesconocido) as info:
        resolver_tenant("../neuracode", PERMITIDOS)
    assert "neuracode" not in str(info.value)
