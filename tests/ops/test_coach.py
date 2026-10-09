"""Pruebas de los mensajes y reglas del coach (sin red)."""

import datetime as dt
import importlib.util
import pathlib

_RUTA = pathlib.Path(__file__).resolve().parents[2] / ".github" / "scripts" / "coach.py"
_spec = importlib.util.spec_from_file_location("coach", _RUTA)
assert _spec is not None and _spec.loader is not None
co = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(co)

JOSUE = co.ROSTER["adbon-dm1"]
PILAR = co.ROSTER["estefanyP-hub"]
LUNES, MIERCOLES, VIERNES, SABADO = (dt.date(2026, 10, d) for d in (5, 7, 9, 10))
ISSUE = {"number": 3, "title": "Webhook", "url": "https://example.test/3"}


def test_dias_de_practica_segun_el_roster():
    assert co.practica_hoy(JOSUE, LUNES) and not co.practica_hoy(JOSUE, VIERNES)
    assert co.practica_hoy(PILAR, VIERNES) and not co.practica_hoy(PILAR, LUNES)
    assert co.dia_n(PILAR, VIERNES) == (3, 3)
    assert co.dia_n(JOSUE, LUNES) == (1, 3)


def test_arranque_menciona_y_dice_donde_mirar():
    txt = co.msg_arranque(PILAR, VIERNES, [ISSUE], [], [], [], None)
    assert "@estefanyP-hub" in txt
    assert "#3" in txt and "git pull origin main" in txt
    assert co.BOARD in txt and "review-requested" in txt


def test_arranque_numera_los_pasos_sin_saltos():
    txt = co.msg_arranque(PILAR, VIERNES, [ISSUE], [], [ISSUE], [], None)
    assert "**1." in txt and "**2." in txt and "**3." in txt and "**4." not in txt


def test_dia_sin_practica_solo_manda_el_aviso():
    txt = co.msg_arranque(
        JOSUE, VIERNES, [ISSUE], [], [], [], "Mañana es la presentación"
    )
    assert "Mañana es la presentación" in txt
    assert "Antes de codear" not in txt


def test_aviso_de_calendario_se_agrega():
    assert "📌 **Aviso:** hola" in co.msg_arranque(
        PILAR, VIERNES, [], [], [], [], "hola"
    )


def test_pulso_avisa_al_monitor():
    txt = co.msg_pulso(PILAR, [ISSUE])
    assert "@estefanyP-hub" in txt and f"@{co.MONITOR}" in txt


def test_cierre_pide_abrir_pr_si_no_hay_y_marca_el_ultimo_dia():
    sin_pr = co.msg_cierre(PILAR, VIERNES, [ISSUE], [])
    assert "ábrelo" in sin_pr and "último día" in sin_pr
    con_pr = co.msg_cierre(PILAR, MIERCOLES, [ISSUE], [ISSUE])
    assert "preguntas de comprensión" in con_pr and "último día" not in con_pr


def test_actividad_cuenta_solo_este_repo_y_hoy_en_lima():
    # 2026-10-09 03:00 UTC = jueves 22:00 Lima, NO es el viernes
    ev = [
        {
            "type": "PushEvent",
            "repo": {"name": co.REPO},
            "created_at": "2026-10-09T03:00:00Z",
        }
    ]
    assert co.hubo_actividad(ev, dt.date(2026, 10, 8))
    assert not co.hubo_actividad(ev, VIERNES)
    ajeno = [
        {
            "type": "PushEvent",
            "repo": {"name": "otro/repo"},
            "created_at": "2026-10-09T15:00:00Z",
        }
    ]
    assert not co.hubo_actividad(ajeno, VIERNES)
    watch = [
        {
            "type": "WatchEvent",
            "repo": {"name": co.REPO},
            "created_at": "2026-10-09T15:00:00Z",
        }
    ]
    assert not co.hubo_actividad(watch, VIERNES)


def test_revision_distingue_estados_y_quien_revisa():
    txt = co.msg_revision("WhoAllan", "jackthony", "CHANGES_REQUESTED")
    assert (
        "pidió cambios" in txt and "el monitor" in txt and "listo para revisar" in txt
    )
    assert "tu compañero" in co.msg_revision("WhoAllan", "estefanyP-hub", "approved")
    assert "aprobó" in co.msg_revision("WhoAllan", "jackthony", "APPROVED")


def test_asignado_da_los_primeros_pasos():
    txt = co.msg_asignado("WhoAllan", 4, "Sender")
    assert "@WhoAllan" in txt and "issue-4-" in txt and "Closes #4" in txt


def test_merge_propone_informe_pull_y_apoyo():
    txt = co.msg_merge("WhoAllan", [ISSUE], [ISSUE], [ISSUE])
    assert (
        "tu PR se mergeó" in txt
        and "informe" in txt
        and "Jala el siguiente" in txt
        and "Apoya" in txt
    )


def test_todos_los_dias_de_practica_son_validos():
    for alumno in co.ALUMNOS:
        assert alumno["dias"] and all(0 <= d <= 4 for d in alumno["dias"])
