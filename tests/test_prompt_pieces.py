import re
from pathlib import Path

import pytest

from agents.config import load_tenant_config
from agents.prompt import PromptPieces, compose_system_prompt, load_prompt_pieces

REAL = Path(__file__).resolve().parents[1] / "configs" / "hola_mujer" / "prompt_v1.md"
CINCO = ["Identidad", "Tono", "Límites", "Fuentes y citas", "Memoria"]


def escribir(tmp_path, encabezados, vacio=None):
    texto = "".join(f"## {h}\n{'' if h == vacio else 'texto'}\n\n" for h in encabezados)
    p = tmp_path / "p.md"
    p.write_text(texto, encoding="utf-8")
    return p


def test_p1_el_archivo_real_carga_las_cinco_piezas():
    piezas = load_prompt_pieces(REAL)
    assert all(v.strip() for v in piezas.model_dump().values())


def test_p2_la_composicion_respeta_orden_y_separador():
    p = PromptPieces(identity="a", tone="b", limits="c", sources="d", memory="e")
    assert compose_system_prompt(p) == "a\n\nb\n\nc\n\nd\n\ne"


def test_p3_falta_un_encabezado(tmp_path):
    with pytest.raises(ValueError, match="Memoria"):
        load_prompt_pieces(escribir(tmp_path, CINCO[:4]))


def test_p4_una_pieza_vacia_se_rechaza(tmp_path):
    with pytest.raises(ValueError):
        load_prompt_pieces(escribir(tmp_path, CINCO, vacio="Tono"))


def test_p5_encabezado_extra_o_en_otro_orden_se_rechaza(tmp_path):
    with pytest.raises(ValueError):
        load_prompt_pieces(escribir(tmp_path, [*CINCO, "Extra"]))
    with pytest.raises(ValueError):
        load_prompt_pieces(escribir(tmp_path, ["Tono", "Identidad", *CINCO[2:]]))


def test_p6_el_prompt_real_cumple_las_reglas_de_contenido():
    t = compose_system_prompt(load_prompt_pieces(REAL))
    for s in [
        "Hola Mujer",
        "<fragmentos>",
        "<pregunta>",
        "[1]",
        "datos",
        "especialista",
        "3 líneas",
        "una sola pregunta",
        "español peruano",
    ]:
        assert s in t
    assert not re.search(r"S/\s?\d", t) and not re.search(r"\b\d{1,2}:\d{2}\b", t)


def test_c1_la_configuracion_usa_el_prompt_compuesto():
    assert load_tenant_config("hola_mujer").prompt == compose_system_prompt(
        load_prompt_pieces(REAL)
    )
