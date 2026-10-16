"""Puerto del calendario: lo que la herramienta de agendar necesita, sin saber quién lo guarda."""

from datetime import datetime
from typing import Protocol

from pydantic import AwareDatetime, BaseModel, ConfigDict


class Booking(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: str
    phone: str
    service_id: str
    start: AwareDatetime


class SlotTaken(Exception):
    """El horario ya lo tiene otra cita (otra clave de idempotencia)."""


class Calendar(Protocol):
    def is_free(self, start: datetime) -> bool: ...

    def book(
        self, key: str, phone: str, service_id: str, start: datetime
    ) -> tuple[Booking, bool]:
        """Agenda de forma idempotente: misma clave = misma cita (`created=False`)."""
        ...
