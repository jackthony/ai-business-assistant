"""Bloque S7-B — reservar sin colisiones y sin duplicar (patrón "idempotent consumer").

Dos garantías distintas:
- COLISIÓN: dos personas distintas no pueden quedarse con el mismo horario.
- IDEMPOTENCIA: reintentar el MISMO request_id (Meta reenvía, el usuario reenvía,
  el sender reintenta) devuelve la misma reserva, no crea otra.

Aquí la "base de datos" es memoria para que el patrón se vea. En producción la
garantía real la da una restricción UNIQUE (request_id) y otra sobre (slot) en
la base: la comprobación en código sola no basta con dos procesos a la vez.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Reserva:
    request_id: str
    slot: str
    wa_id: str


@dataclass(frozen=True)
class ErrorReserva:
    codigo: str  # "slot_no_disponible" | "request_id_reutilizado"


class Agenda:
    def __init__(self, horarios_libres: list[str]) -> None:
        self._libres = set(horarios_libres)
        self._por_request: dict[str, Reserva] = {}

    def proponer(self, cuantos: int = 3) -> list[str]:
        """Hasta `cuantos` horarios que de verdad están libres (nunca inventados)."""
        return sorted(self._libres)[:cuantos]

    def reservar(
        self, request_id: str, slot: str, wa_id: str
    ) -> Reserva | ErrorReserva:
        previa = self._por_request.get(request_id)
        if previa is not None:
            if (previa.slot, previa.wa_id) == (slot, wa_id):
                return previa  # idempotente: misma petición, mismo resultado, cero efectos nuevos
            return ErrorReserva(
                "request_id_reutilizado"
            )  # mismo id con otros datos = bug del cliente
        if slot not in self._libres:
            return ErrorReserva("slot_no_disponible")
        self._libres.remove(slot)
        reserva = Reserva(request_id, slot, wa_id)
        self._por_request[request_id] = reserva
        return reserva
