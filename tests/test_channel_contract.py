import pytest
from pydantic import ValidationError

from channels.contract import InboundEvent, OutboundReply


def test_c1_inbound_event_immutable():
    event = InboundEvent(
        tenant="hola_mujer",
        user_id="user_123",
        type="text",
        content="hola",
        channel="web",
    )
    assert event.tenant == "hola_mujer"
    assert event.user_id == "user_123"
    assert event.type == "text"
    assert event.content == "hola"
    assert event.channel == "web"

    with pytest.raises(ValidationError):
        event.content = "cambio"  # type: ignore[misc]


def test_c2_inbound_validation_matrix():
    # 3 Aceptaciones válidas (incluyendo el borde exacto de 64 chars para user_id)
    event_ok1 = InboundEvent(
        tenant="hola_mujer",
        user_id="user_1",
        type="text",
        content="Hola",
        channel="web",
    )
    event_ok2 = InboundEvent(
        tenant="tenant123",
        user_id="x" * 64,
        type="voice",
        content=None,
        channel="telegram",
    )
    event_ok3 = InboundEvent(
        tenant="abc",
        user_id="user-id_99",
        type="media",
        content="A" * 1000,
        channel="whatsapp",
    )
    assert event_ok1.tenant == "hola_mujer"
    assert event_ok2.type == "voice"
    assert event_ok3.content is not None

    # Rechazos estrictos de la fila
    invalid_cases = [
        {
            "tenant": "hola_mujer",
            "user_id": "",
            "type": "text",
            "content": "Hola",
            "channel": "web",
        },  # user_id vacío
        {
            "tenant": "hola_mujer",
            "user_id": "a b",
            "type": "text",
            "content": "Hola",
            "channel": "web",
        },  # espacio
        {
            "tenant": "hola_mujer",
            "user_id": "x" * 65,
            "type": "text",
            "content": "Hola",
            "channel": "web",
        },  # > 64 chars
        {
            "tenant": "hola_mujer",
            "user_id": "../etc",
            "type": "text",
            "content": "Hola",
            "channel": "web",
        },  # path traversal
        {
            "tenant": "hola_mujer",
            "user_id": "a;b",
            "type": "text",
            "content": "Hola",
            "channel": "web",
        },  # punto y coma
        {
            "tenant": "hola_mujer",
            "user_id": "123\n",
            "type": "text",
            "content": "Hola",
            "channel": "web",
        },  # salto de línea
        {
            "tenant": "hola_mujer",
            "user_id": "123",
            "type": "image",
            "content": "Hola",
            "channel": "web",
        },  # type image no permitido
        {
            "tenant": "hola_mujer",
            "user_id": "123",
            "type": "text",
            "content": "Hola",
            "channel": "WhatsApp",
        },  # channel con mayúscula
        {
            "tenant": "Hola Mujer",
            "user_id": "123",
            "type": "text",
            "content": "Hola",
            "channel": "web",
        },  # tenant con espacio y mayúscula
        {
            "tenant": "hola_mujer",
            "user_id": "123",
            "type": "text",
            "content": "A" * 1001,
            "channel": "web",
        },  # content > 1000
    ]

    for case in invalid_cases:
        with pytest.raises(ValidationError):
            InboundEvent(**case)


def test_c3_outbound_reply_structure():
    # 1ª entrada: Defaults
    reply_default = OutboundReply(text="Hola")
    assert reply_default.text == "Hola"
    assert reply_default.template_id is None
    assert reply_default.channel_metadata == {}

    # 2ª entrada: template_id y channel_metadata
    reply_advanced = OutboundReply(
        template_id="confirmacion_cita",
        channel_metadata={"k": 1},
    )
    assert reply_advanced.text is None
    assert reply_advanced.template_id == "confirmacion_cita"
    assert reply_advanced.channel_metadata == {"k": 1}

    with pytest.raises(ValidationError):
        reply_advanced.text = "otro"  # type: ignore[misc]
