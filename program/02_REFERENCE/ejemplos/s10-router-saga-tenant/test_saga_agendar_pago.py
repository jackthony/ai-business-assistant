from saga_agendar_pago import Paso, ejecutar_saga


def armar(fallar_en: str | None = None):
    estado = {"slot": False, "pago": False, "confirmado": False}

    def hacer(nombre: str):
        def _f():
            if fallar_en == nombre:
                raise RuntimeError("boom")
            estado[nombre] = True

        return _f

    def deshacer(nombre: str):
        def _f():
            estado[nombre] = False

        return _f

    pasos = [Paso(n, hacer(n), deshacer(n)) for n in ("slot", "pago", "confirmado")]
    return pasos, estado


def test_todo_ok_deja_los_tres_pasos_hechos():
    pasos, estado = armar()
    r = ejecutar_saga(pasos)
    assert r.ok
    assert estado == {"slot": True, "pago": True, "confirmado": True}


def test_si_falla_el_pago_se_libera_el_horario():
    pasos, estado = armar(fallar_en="pago")
    r = ejecutar_saga(pasos)
    assert not r.ok
    assert estado == {
        "slot": False,
        "pago": False,
        "confirmado": False,
    }  # no queda nada a medias
    assert r.log == ["OK slot", "FALLO pago: RuntimeError", "DESHECHO slot"]


def test_si_falla_confirmar_se_deshace_en_orden_inverso():
    pasos, estado = armar(fallar_en="confirmado")
    r = ejecutar_saga(pasos)
    assert not r.ok
    assert r.log[-2:] == ["DESHECHO pago", "DESHECHO slot"]
    assert not any(estado.values())


def test_si_falla_el_primer_paso_no_hay_nada_que_deshacer():
    pasos, _ = armar(fallar_en="slot")
    r = ejecutar_saga(pasos)
    assert not r.ok
    assert r.log == ["FALLO slot: RuntimeError"]
