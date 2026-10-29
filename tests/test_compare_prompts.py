import json
import re

from agents.config import load_tenant_config
from evals.compare_prompts import (
    CORPUS,
    StyleSummary,
    main,
    pick_conversations,
    render_comparison,
    style_summary,
)


def test_m1_pick_conversations():
    c1 = pick_conversations(CORPUS, 10)
    c2 = pick_conversations(CORPUS, 10)

    # (a) Largo exacto
    assert len(c1) == 10
    # (b) Reproducibilidad
    assert c1 == c2
    # (c) Todos distintos
    assert len(set(c1)) == len(c1)

    # Validar que provengan estrictamente de filas con rol == "user" del corpus oficial
    textos_user = {
        json.loads(linea)["texto"].strip()
        for linea in CORPUS.read_text(encoding="utf-8").splitlines()
        if linea.strip() and json.loads(linea).get("rol") == "user"
    }

    assert set(c1) <= textos_user

    # (d y e) Reglas de contenido
    for texto in c1:
        t_lower = texto.lower()
        assert not t_lower.startswith(("hola", "buen", "["))
        assert not re.search(r"\d{9}", texto)


def test_m2_style_summary():
    respuestas = [
        "Hola. ¿Sí?",
        "a\nb\nc\nd",
        "¿uno? ¿dos?",
        "",
        "a\nb\nc\nd ¿uno? ¿dos?",
    ]
    resumen = style_summary(respuestas)
    assert resumen.total == 5
    assert resumen.compliant == 1
    assert resumen.too_many_lines == 2
    assert resumen.too_many_questions == 2
    assert resumen.empty == 1


def test_m3_render_comparison():
    s1 = StyleSummary(
        total=10, compliant=7, too_many_lines=2, too_many_questions=1, empty=0
    )
    s2 = StyleSummary(
        total=10, compliant=9, too_many_lines=1, too_many_questions=0, empty=0
    )
    resultado = render_comparison(s1, s2)

    esperado = (
        "| Métrica | v1 | v2 |\n"
        "|---|---|---|\n"
        "| Respuestas | 10 | 10 |\n"
        "| Cumplen el estilo | 7 | 9 |\n"
        "| Más de 3 líneas | 2 | 1 |\n"
        "| Más de 1 pregunta | 1 | 0 |\n"
        "| Vacías | 0 | 0 |"
    )
    assert resultado == esperado


def test_m4_main_empty_or_invalid_args(capsys):
    llamadas = []

    def runner_falso(prompt, texto):
        llamadas.append((prompt, texto))
        return "Respuesta"

    codigo = main([], runner=runner_falso)
    assert codigo == 2
    assert len(llamadas) == 0
    err = capsys.readouterr().err
    assert "--live" in err


def test_m5_main_live_execution(capsys):
    llamadas = []

    def runner_falso(prompt, texto):
        llamadas.append((prompt, texto))
        return "Claro [1]. ¿Sí?"

    codigo = main(["--live", "--n", "4"], runner=runner_falso)
    assert codigo == 0
    # 4 preguntas x 2 prompts (v1 y v2) = 8 llamadas
    assert len(llamadas) == 8

    cfg = load_tenant_config("hola_mujer")
    prompts_vistos = {p for p, _ in llamadas}
    assert prompts_vistos == {cfg.prompt, cfg.prompt_v2}

    # Validar que las preguntas corridas con v1 y v2 sean las mismas en el mismo orden
    texts_v1 = [t for p, t in llamadas if p == cfg.prompt]
    texts_v2 = [t for p, t in llamadas if p == cfg.prompt_v2]
    assert texts_v1 == texts_v2

    out = capsys.readouterr().out
    assert "| Cumplen el estilo | 4 | 4 |" in out
