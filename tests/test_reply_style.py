from agents.style import check_reply_style


def test_s1_normal():
    assert check_reply_style("El taller cuesta S/ 149.99. ¿Quieres agendar?") == []


def test_s2_vacia():
    assert check_reply_style("") == ["empty"]


def test_s3_espacios():
    assert check_reply_style("  \n  ") == ["empty"]


def test_s4_tres_lineas():
    assert check_reply_style("uno\ndos\ntres") == []


def test_s5_cuatro_lineas():
    assert check_reply_style("uno\ndos\ntres\ncuatro") == ["too_many_lines"]


def test_s6_en_blanco_no_cuentan():
    assert check_reply_style("uno\n\ndos\n\nFuente: tres") == []


def test_s7_dos_preguntas():
    assert check_reply_style("¿Qué servicio? ¿Qué día?") == ["too_many_questions"]


def test_s8_ambos():
    assert check_reply_style("a\nb\nc\nd ¿uno? ¿dos?") == [
        "too_many_lines",
        "too_many_questions",
    ]
