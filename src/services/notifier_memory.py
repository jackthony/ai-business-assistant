"""Notificador en memoria: adaptador de prueba/desarrollo (el canal de Jioysi sigue PENDING)."""

import logging
import threading

from agents.ports import HandoffAlert

log = logging.getLogger("handoff")


class InMemoryNotifier:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._sent: dict[str, HandoffAlert] = {}

    def notify(self, alert: HandoffAlert) -> None:
        with self._lock:
            if alert.key in self._sent:
                return  # mismo motivo, mismo aviso: no se repite
            self._sent[alert.key] = alert
        # Sin el texto de la clienta: puede traer datos de salud.
        log.warning(
            "DERIVACIÓN %s%s (canal de alerta real pendiente)",
            alert.reason,
            " URGENTE" if alert.urgent else "",
        )

    def sent(self) -> list[HandoffAlert]:
        with self._lock:
            return list(self._sent.values())
