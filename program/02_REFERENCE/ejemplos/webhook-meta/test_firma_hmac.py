from firma_hmac import firma_valida, firmar

SECRETO = "secreto-de-prueba"  # valor falso: el real vive en WHATSAPP_APP_SECRET (.env, nunca al repo)
CUERPO = b'{"object":"whatsapp_business_account"}'


def test_firma_correcta_es_valida():
    assert firma_valida(CUERPO, firmar(CUERPO, SECRETO), SECRETO)


def test_cuerpo_alterado_invalida_la_firma():
    cabecera = firmar(CUERPO, SECRETO)
    assert not firma_valida(CUERPO + b" ", cabecera, SECRETO)


def test_secreto_equivocado_invalida_la_firma():
    assert not firma_valida(CUERPO, firmar(CUERPO, "otro-secreto"), SECRETO)


def test_sin_cabecera_o_sin_secreto_falla_cerrado():
    assert not firma_valida(CUERPO, None, SECRETO)
    assert not firma_valida(CUERPO, "", SECRETO)
    assert not firma_valida(CUERPO, firmar(CUERPO, ""), "")


def test_cabecera_sin_prefijo_o_con_basura_no_revienta():
    assert not firma_valida(CUERPO, "no-es-una-firma", SECRETO)
    assert not firma_valida(
        CUERPO, "sha256=ñandú", SECRETO
    )  # no ASCII: no debe lanzar TypeError
