"""Herramienta `agendar_cita` (nivel N2, ADR-009): validación determinista + escritura idempotente.

El LLM nunca fija la clave de idempotencia ni el `service_id`: la clave sale de (teléfono, servicio,
horario), así que repetir la llamada (reintento, reanudación de un checkpoint) no duplica la cita.
La aprobación humana ocurre ANTES, en el grafo; aquí solo se valida y se escribe.
"""

import hashlib
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, Literal

from langchain_core.tools import StructuredTool
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

from rag.catalog import ServiceCatalog
from tools.ports import Calendar, SlotTaken
from tools.schedule import Schedule

PERMISSION_LEVEL = "N2"
Problem = Literal["service_unknown", "past", "not_in_schedule", "slot_busy"]


class AgendarInput(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    phone: str = Field(pattern=r"^\d{8,15}$", description="Teléfono solo con dígitos")
    service_id: str = Field(min_length=3, max_length=40)
    start: AwareDatetime = Field(description="Inicio de la cita, con zona horaria")


class AgendarResult(BaseModel):
    status: Literal["created", "already_booked", "rejected"]
    reason: Problem | None = None
    key: str | None = None


def idempotency_key(inp: AgendarInput) -> str:
    raw = f"{inp.phone}|{inp.service_id}|{inp.start.astimezone(UTC).isoformat()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def check_request(
    inp: AgendarInput,
    catalog: ServiceCatalog,
    schedule: Schedule,
    calendar: Calendar,
    now: datetime,
) -> Problem | None:
    """Primer problema que impide agendar, o None. Todo determinista."""
    if catalog.get(inp.service_id) is None:
        return "service_unknown"
    if inp.start <= now:
        return "past"
    if not schedule.is_slot_start(inp.start):
        return "not_in_schedule"
    if not calendar.is_free(inp.start):
        return "slot_busy"
    return None


def make_agendar_tool(
    calendar: Calendar,
    catalog: ServiceCatalog,
    schedule: Schedule,
    clock: Callable[[], datetime],
) -> StructuredTool:
    def agendar_cita(
        phone: str, service_id: str, start: AwareDatetime
    ) -> dict[str, Any]:
        """Agenda una cita. Idempotente: repetirla con los mismos datos no crea otra."""
        inp = AgendarInput(phone=phone, service_id=service_id, start=start)
        key = idempotency_key(inp)
        problem = check_request(inp, catalog, schedule, calendar, clock())
        if problem and problem != "slot_busy":
            return AgendarResult(status="rejected", reason=problem).model_dump()
        # `slot_busy` puede ser NUESTRA cita de un intento anterior: lo decide la clave, no `is_free`.
        try:
            _, created = calendar.book(key, inp.phone, inp.service_id, inp.start)
        except SlotTaken:
            return AgendarResult(status="rejected", reason="slot_busy").model_dump()
        return AgendarResult(
            status="created" if created else "already_booked", key=key
        ).model_dump()

    return StructuredTool.from_function(
        func=agendar_cita,
        name="agendar_cita",
        args_schema=AgendarInput,
        metadata={"permission_level": PERMISSION_LEVEL},
    )
