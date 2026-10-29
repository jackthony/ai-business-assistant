from conftest import ScriptedModel
from langgraph.checkpoint.memory import InMemorySaver

from agents.graph import build_graph
from channels.contract import InboundEvent, OutboundReply
from channels.dispatch import UNSUPPORTED, handle_inbound, thread_id_for
from services.notifier_memory import InMemoryNotifier

# Constantes literales exactas de la §6
RESPUESTA = "El Taller PRP Facial + Capilar cuesta S/ 149.99 [1]."
PREGUNTA = "¿Cuánto cuesta el taller PRP facial?"
CLINICA = "Me duele mucho después del tratamiento, ¿es normal?"


def test_d1_thread_id_format():
    event_web = InboundEvent(
        tenant="hola_mujer", user_id="u99", type="text", content="hola", channel="web"
    )
    event_tg = InboundEvent(
        tenant="hola_mujer",
        user_id="u99",
        type="text",
        content="hola",
        channel="telegram",
    )
    assert thread_id_for(event_web) == "web:u99"
    assert thread_id_for(event_tg) == "telegram:u99"


def test_d2_dispatch_execution_and_metrics(store):
    model = ScriptedModel(RESPUESTA)
    graph = build_graph(
        store, model, "SISTEMA", InMemoryNotifier(), None, InMemorySaver()
    )

    times = [10.0, 10.25]

    def clock():
        return times.pop(0)

    event = InboundEvent(
        tenant="hola_mujer",
        user_id="u123",
        type="text",
        content=PREGUNTA,
        channel="web",
    )

    reply = handle_inbound(event, graph=graph, clock=clock)

    assert isinstance(reply, OutboundReply)
    assert "S/ 149.99" in reply.text
    assert reply.text.endswith("Fuente: Taller PRP Facial + Capilar")
    assert reply.channel_metadata["first_response_ms"] == 250.0
    assert reply.channel_metadata["citations"][0]["doc_id"] == "HM-ACA-001"
    assert reply.channel_metadata["pending_approval"] is False
    assert len(model.calls) == 1


def test_d3_handle_inbound_unsupported_cases(store):
    model = ScriptedModel(RESPUESTA)
    graph = build_graph(
        store, model, "SISTEMA", InMemoryNotifier(), None, InMemorySaver()
    )

    for event in [
        InboundEvent(
            tenant="hola_mujer",
            user_id="u123",
            type="voice",
            content=None,
            channel="web",
        ),
        InboundEvent(
            tenant="hola_mujer",
            user_id="u123",
            type="text",
            content="   ",
            channel="web",
        ),
        InboundEvent(
            tenant="hola_mujer",
            user_id="u123",
            type="media",
            content=None,
            channel="web",
        ),
    ]:
        reply = handle_inbound(event, graph=graph)
        assert reply.text == UNSUPPORTED
        assert reply.channel_metadata.get("unsupported") is True
        assert len(model.calls) == 0


def test_d4_handle_inbound_first_message_intent(store):
    model = ScriptedModel(RESPUESTA)
    graph = build_graph(
        store, model, "SISTEMA", InMemoryNotifier(), None, InMemorySaver()
    )

    # 1. Mensaje clínico (activa handoff / contiene "especialista")
    event1 = InboundEvent(
        tenant="hola_mujer", user_id="u123", type="text", content=CLINICA, channel="web"
    )
    reply1 = handle_inbound(event1, graph=graph)
    assert "especialista" in reply1.text
    assert len(model.calls) == 0

    # 2. Siguiente mensaje en hilo congelado por handoff -> None
    event2 = InboundEvent(
        tenant="hola_mujer",
        user_id="u123",
        type="text",
        content=PREGUNTA,
        channel="web",
    )
    reply2 = handle_inbound(event2, graph=graph)
    assert reply2 is None

    # 3. Tercer mensaje en hilo congelado -> None (modelo nunca llamado)
    reply3 = handle_inbound(event2, graph=graph)
    assert reply3 is None
    assert len(model.calls) == 0


def test_d5_handle_inbound_handoff_isolation(store):
    model = ScriptedModel(RESPUESTA)
    graph = build_graph(
        store, model, "SISTEMA", InMemoryNotifier(), None, InMemorySaver()
    )

    # 1. Clinica de ana en web (activa handoff para ana:web)
    event_ana_web_1 = InboundEvent(
        tenant="hola_mujer", user_id="ana", type="text", content=CLINICA, channel="web"
    )
    handle_inbound(event_ana_web_1, graph=graph)

    # 2. Pregunta de bea en web (hilo distinto, responde OK con precio)
    event_bea = InboundEvent(
        tenant="hola_mujer", user_id="bea", type="text", content=PREGUNTA, channel="web"
    )
    reply_bea = handle_inbound(event_bea, graph=graph)
    assert reply_bea is not None
    assert "S/ 149.99" in reply_bea.text

    # 3. Pregunta de ana en telegram (canal distinto, hilo distinto, responde OK con precio)
    event_ana_tg = InboundEvent(
        tenant="hola_mujer",
        user_id="ana",
        type="text",
        content=PREGUNTA,
        channel="telegram",
    )
    reply_ana_tg = handle_inbound(event_ana_tg, graph=graph)
    assert reply_ana_tg is not None
    assert "S/ 149.99" in reply_ana_tg.text

    # 4. Pregunta de ana en web (mismo hilo congelado por handoff -> None)
    event_ana_web_2 = InboundEvent(
        tenant="hola_mujer", user_id="ana", type="text", content=PREGUNTA, channel="web"
    )
    reply_ana_web_2 = handle_inbound(event_ana_web_2, graph=graph)
    assert reply_ana_web_2 is None
