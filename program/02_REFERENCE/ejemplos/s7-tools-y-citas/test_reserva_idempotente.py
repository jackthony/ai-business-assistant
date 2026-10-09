from reserva_idempotente import Agenda, ErrorReserva, Reserva

LIBRES = [
    "2026-10-12T10:00",
    "2026-10-12T11:00",
    "2026-10-12T15:00",
    "2026-10-13T09:00",
]


def test_propone_solo_horarios_libres_y_como_maximo_tres():
    agenda = Agenda(LIBRES)
    assert agenda.proponer() == LIBRES[:3]
    assert set(agenda.proponer()) <= set(LIBRES)


def test_reservar_quita_el_horario_de_las_propuestas():
    agenda = Agenda(LIBRES)
    assert isinstance(agenda.reservar("req-1", LIBRES[0], "51900000001"), Reserva)
    assert LIBRES[0] not in agenda.proponer(10)


def test_mismo_request_id_no_duplica():
    agenda = Agenda(LIBRES)
    primera = agenda.reservar("req-1", LIBRES[0], "51900000001")
    segunda = agenda.reservar("req-1", LIBRES[0], "51900000001")
    assert primera == segunda
    assert len(agenda.proponer(10)) == len(LIBRES) - 1  # se consumió UN solo horario


def test_dos_personas_no_se_quedan_el_mismo_horario():
    agenda = Agenda(LIBRES)
    agenda.reservar("req-1", LIBRES[0], "51900000001")
    assert agenda.reservar("req-2", LIBRES[0], "51900000002") == ErrorReserva(
        "slot_no_disponible"
    )


def test_request_id_reutilizado_con_otros_datos_es_error():
    agenda = Agenda(LIBRES)
    agenda.reservar("req-1", LIBRES[0], "51900000001")
    assert agenda.reservar("req-1", LIBRES[1], "51900000001") == ErrorReserva(
        "request_id_reutilizado"
    )


def test_horario_que_no_existe_no_se_reserva():
    assert Agenda(LIBRES).reservar(
        "req-1", "2099-01-01T00:00", "51900000001"
    ) == ErrorReserva("slot_no_disponible")
