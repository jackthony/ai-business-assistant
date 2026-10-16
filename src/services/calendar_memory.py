"""Calendario en memoria: adaptador de prueba/desarrollo (el CALENDAR_ID real sigue PENDING)."""

import threading
from datetime import UTC, datetime

from tools.ports import Booking, SlotTaken


class InMemoryCalendar:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._by_key: dict[str, Booking] = {}
        self._by_start: dict[datetime, Booking] = {}

    def is_free(self, start: datetime) -> bool:
        with self._lock:
            return start.astimezone(UTC) not in self._by_start

    def book(
        self, key: str, phone: str, service_id: str, start: datetime
    ) -> tuple[Booking, bool]:
        slot = start.astimezone(UTC)
        with self._lock:
            if key in self._by_key:
                return self._by_key[key], False
            if slot in self._by_start:
                raise SlotTaken(slot.isoformat())
            booking = Booking(key=key, phone=phone, service_id=service_id, start=start)
            self._by_key[key] = booking
            self._by_start[slot] = booking
            return booking, True

    def bookings(self) -> list[Booking]:
        with self._lock:
            return list(self._by_key.values())
