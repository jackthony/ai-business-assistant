import json
from pathlib import Path

import pytest

from agents.conversation_service import ConversationService
from agents.llm_port import ChatMessage

_FIXTURE_RUTA = Path(__file__).resolve().parent / "fixtures" / "first_messages_v1.json"
_FIXTURE = json.loads(_FIXTURE_RUTA.read_text(encoding="utf-8"))


def test_s1_respuesta_valida_se_devuelve(fake_llm) -> None:
    fake_llm.reply = "Hola, ¿en qué te ayudo?"
    mensajes = [ChatMessage(role="user", text="Hola")]
    servicio = ConversationService(llm=fake_llm, system="SYS")
    resultado = servicio.respond(mensajes)
    assert resultado.status == "respondido"
    assert resultado.text == "Hola, ¿en qué te ayudo?"
    assert resultado.reasons == []
    assert len(fake_llm.calls) == 1


def test_s2_respuesta_invalida_pasa_a_revision(fake_llm) -> None:
    fake_llm.reply = "a\nb\nc\nd"
    mensajes = [ChatMessage(role="user", text="Hola")]
    servicio = ConversationService(llm=fake_llm, system="SYS")
    resultado = servicio.respond(mensajes)
    assert resultado.status == "revision_humana"
    assert resultado.text is None
    assert resultado.reasons == ["too_many_lines"]


def test_s3_el_sistema_llega_sin_cambios(fake_llm) -> None:
    fake_llm.reply = "Respuesta cualquiera"
    mensajes = [ChatMessage(role="user", text="Hola")]
    servicio = ConversationService(llm=fake_llm, system="SYS")
    servicio.respond(mensajes)
    assert fake_llm.calls[0][0] == "SYS"


@pytest.mark.parametrize("fila", _FIXTURE, ids=[f["conversacion_id"] for f in _FIXTURE])
def test_t_primer_mensaje_de_conversacion(fake_llm, fila) -> None:
    fake_llm.reply = "Hola, ¿en qué te puedo ayudar?"
    mensajes = [ChatMessage(role="user", text=fila["texto"])]
    servicio = ConversationService(llm=fake_llm, system="SYS")
    resultado = servicio.respond(mensajes)
    assert resultado.status == "respondido"
    assert resultado.text == fake_llm.reply
    assert resultado.reasons == []
    assert fake_llm.calls[0][1][-1].text == fila["texto"]
