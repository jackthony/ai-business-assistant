"""Horario de atención y rejilla de citas, leídos de `configs/<tenant>/schedule.json`."""

import json
from collections.abc import Iterator
from datetime import datetime, time, timedelta, timezone
from pathlib import Path

from pydantic import BaseModel, ConfigDict, field_validator

# Perú no tiene horario de verano: un offset fijo es exacto y evita depender de la base IANA
# (que en Windows exige instalar `tzdata`).
LIMA = timezone(timedelta(hours=-5), "America/Lima")


class Schedule(BaseModel):
    model_config = ConfigDict(extra="ignore")

    open: time
    close: time
    slot_minutes: int

    @field_validator("slot_minutes")
    @classmethod
    def _positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("slot_minutes debe ser > 0")
        return v

    def is_slot_start(self, start: datetime) -> bool:
        """¿Cae exacto en la rejilla y la cita termina antes del cierre?"""
        local = start.astimezone(LIMA)
        if local.second or local.microsecond:
            return False
        minutes = local.hour * 60 + local.minute
        opens = self.open.hour * 60 + self.open.minute
        closes = self.close.hour * 60 + self.close.minute
        return (
            minutes >= opens
            and (minutes - opens) % self.slot_minutes == 0
            and minutes + self.slot_minutes <= closes
        )

    def upcoming_starts(self, after: datetime, days: int = 7) -> Iterator[datetime]:
        """Inicios de cita válidos estrictamente posteriores a `after`, en orden."""
        start_day = after.astimezone(LIMA).date()
        for offset in range(days + 1):
            cursor = datetime.combine(
                start_day + timedelta(days=offset), self.open, tzinfo=LIMA
            )
            while self.is_slot_start(cursor):
                if cursor > after:
                    yield cursor
                cursor += timedelta(minutes=self.slot_minutes)


def load_schedule(path: Path) -> Schedule:
    return Schedule.model_validate(json.loads(path.read_text(encoding="utf-8")))
