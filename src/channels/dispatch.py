import time
from collections.abc import Callable
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph

from channels.contract import InboundEvent, OutboundReply

UNSUPPORTED = "Por ahora solo puedo leer mensajes de texto 🙏. ¿Me lo puedes escribir?"


def thread_id_for(event: InboundEvent) -> str:
    return f"{event.channel}:{event.user_id}"


def handle_inbound(
    event: InboundEvent,
    graph: CompiledStateGraph,
    clock: Callable[[], float] = time.perf_counter,
) -> OutboundReply | None:
    start_time = clock()

    # R1: Validar tipos de contenido soportados (texto no vacío)
    if event.type != "text" or not event.content or not event.content.strip():
        end_time = clock()
        first_response_ms = round((end_time - start_time) * 1000.0, 1)
        return OutboundReply(
            text=UNSUPPORTED,
            channel_metadata={
                "first_response_ms": first_response_ms,
                "citations": [],
                "pending_approval": False,
                "unsupported": True,
            },
        )

    thread_id = thread_id_for(event)
    config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

    # R6: Consultar estado de forma limpia (sin try-except ciego para que escalen errores reales)
    current_state = graph.get_state(config)
    has_state = bool(current_state and current_state.values)

    if has_state:
        val = current_state.values
        if val.get("status") == "handoff_requested" or val.get("handoff_active"):
            return None

    state_input: dict[str, Any] = {
        "messages": [HumanMessage(content=event.content)],
        "phone": event.user_id,
        "tenant": event.tenant,
    }

    # Solo el primer mensaje del hilo lleva intent=None y status="nuevo"
    if not has_state:
        state_input["intent"] = None
        state_input["status"] = "nuevo"

    # Capturar IDs previos para R3
    existing_msg_ids = set()
    if has_state and current_state and "messages" in current_state.values:
        existing_msg_ids = {
            msg.id
            for msg in current_state.values["messages"]
            if hasattr(msg, "id") and msg.id
        }

    result = graph.invoke(state_input, config=config)

    end_time = clock()
    first_response_ms = round((end_time - start_time) * 1000.0, 1)

    # R3: Filtrar y tomar el último AIMessage nuevo
    messages = result.get("messages", [])
    new_ai_messages = [
        msg
        for msg in messages
        if isinstance(msg, AIMessage) and (not msg.id or msg.id not in existing_msg_ids)
    ]

    if not new_ai_messages:
        if messages:
            last_msg = messages[-1]
            response_text = getattr(last_msg, "content", str(last_msg))
            citations = getattr(last_msg, "additional_kwargs", {}).get("citations", [])
        else:
            return None
    else:
        last_ai_msg = new_ai_messages[-1]
        response_text = last_ai_msg.content
        citations = last_ai_msg.additional_kwargs.get("citations", [])

    # R4: pending_approval True si ocurre interrupción o handoff
    pending_approval = "__interrupt__" in result or bool(
        result.get("pending_approval", False)
    )

    channel_metadata = {
        "first_response_ms": first_response_ms,
        "citations": citations,
        "pending_approval": pending_approval,
    }

    return OutboundReply(
        text=response_text,
        channel_metadata=channel_metadata,
    )
