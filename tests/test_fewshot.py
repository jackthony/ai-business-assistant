from pathlib import Path

import pytest

from agents.config import load_tenant_config
from agents.fewshot import (
    FewShot,
    load_fewshots,
    render_fewshots,
    violations,
)

# Ruta raíz del repositorio calculada dinámicamente
RAIZ = Path(__file__).resolve().parents[1]
RUTA_FEWSHOTS = RAIZ / "configs" / "hola_mujer" / "fewshot_objeciones.json"


def base(**cambios) -> FewShot:
    datos = {
        "id": "ejemplo-uno",
        "tipo": "precio",
        "objecion": "Está caro",
        "respuesta": "Te entiendo 💛 Lo que tenemos está en [1]. ¿Te cuento las opciones?",
    }
    datos.update(cambios)
    return FewShot(**datos)


def test_f1_enough_examples_unique_ids():
    ejemplos = load_fewshots(RUTA_FEWSHOTS)
    assert len(ejemplos) >= 5, "Debe haber al menos 5 ejemplos reales"

    ids = [e.id for e in ejemplos]
    assert len(ids) == len(set(ids)), "Los IDs del archivo JSON deben ser únicos"


def test_f2_covers_required_types():
    ejemplos = load_fewshots(RUTA_FEWSHOTS)
    tipos_presentes = {e.tipo for e in ejemplos}

    for tipo_esperado in ["precio", "consulta", "descuento"]:
        assert tipo_esperado in tipos_presentes, (
            f"Falta el tipo '{tipo_esperado}' en los ejemplos reales"
        )


def test_f3_real_examples_have_no_violations():
    ejemplos = load_fewshots(RUTA_FEWSHOTS)
    for ej in ejemplos:
        v = violations(ej)
        assert v == [], f"El ejemplo real '{ej.id}' tiene violaciones: {v}"


def test_f4_render_format_is_exact():
    ej1 = FewShot(
        id="ejemplo-a",
        tipo="precio",
        objecion="Está caro",
        respuesta="Claro [1]. ¿Sí?",
    )
    ej2 = FewShot(
        id="ejemplo-b",
        tipo="consulta",
        objecion="Lo pienso",
        respuesta="Ok [1].",
    )

    resultado = render_fewshots([ej1, ej2])
    # Encabezado exacto exigido por el contrato §5.2
    esperado = (
        "Ejemplos de cómo responder a objeciones (solo muestran el tono; los datos salen siempre de <fragmentos>):\n\n"
        "Clienta: Está caro\n"
        "Hola Mujer: Claro [1]. ¿Sí?\n\n"
        "Clienta: Lo pienso\n"
        "Hola Mujer: Ok [1]."
    )
    assert resultado == esperado


def test_f5_duplicate_id_raises_naming_it(tmp_path):
    # El contrato requiere que esté envuelto en {"items": [...]} y textos >= 3 caracteres
    contenido_json = """{
        "items": [
            {"id": "dup-1", "tipo": "precio", "objecion": "Primer objecion", "respuesta": "Respuesta valida [1]."},
            {"id": "dup-1", "tipo": "consulta", "objecion": "Segunda objecion", "respuesta": "Respuesta valida dos [1]."}
        ]
    }"""

    archivo_tmp = tmp_path / "duplicados.json"
    archivo_tmp.write_text(contenido_json, encoding="utf-8")

    with pytest.raises(ValueError) as exc_info:
        load_fewshots(archivo_tmp)

    assert "dup-1" in str(exc_info.value)


def test_f6_detects_amounts_hours_citations():
    # 1. Base sin tocar -> sin violaciones
    assert violations(base()) == []

    # 2. Con importe
    ej_amount = base(respuesta="Cuesta S/ 50 [1].")
    assert violations(ej_amount) == ["amount"]

    # 3. Con importe alternativo
    ej_amount_soles = base(respuesta="Cuesta 50 soles [1].")
    assert violations(ej_amount_soles) == ["amount"]

    # 4. Con hora explícita
    ej_hour = base(respuesta="Te espero a las 15:30 [1].")
    assert violations(ej_hour) == ["hour"]

    # 5. Falta de cita [1]
    ej_nocit = base(respuesta="Te entiendo, tómate tu tiempo.")
    assert violations(ej_nocit) == ["no_citation"]


def test_f7_detects_style_and_code_order():
    # 1. Demasiadas líneas
    ej_lines = base(respuesta="a\nb\nc\nd [1]")
    assert violations(ej_lines) == ["too_many_lines"]

    # 2. Múltiples violaciones respetando el ORDEN exacto de códigos
    ej_multiples = base(respuesta="a\nb\nc\nd ¿uno? ¿dos? S/ 5 12:00")
    assert violations(ej_multiples) == [
        "too_many_lines",
        "too_many_questions",
        "no_citation",
        "amount",
        "hour",
    ]


def test_f8_prompt_v2_extends_v1():
    cfg = load_tenant_config("hola_mujer")

    # 1. prompt_v2 debe ser exactamente el prompt v1 + separador + los fewshots renderizados
    assert cfg.prompt_v2 == cfg.prompt + "\n\n" + render_fewshots(
        load_fewshots(RUTA_FEWSHOTS)
    )

    # 2. El prefijo de los ejemplos ("Clienta:") no debe filtrarse al prompt base v1
    assert "Clienta:" not in cfg.prompt

    # 3. Comprobaciones de contenido en los textos de configuración
    assert "[1]" in cfg.prompt
    assert "<fragmentos>" in cfg.prompt_v2
