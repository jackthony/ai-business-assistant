"""Bloque S10-B — saga con compensación (agendar + cobrar sin dejar medio hecho).

Problema: "reservar horario" y "registrar pago" son dos efectos en dos sitios
distintos; no hay una transacción que cubra ambos. Si el pago falla, el horario
quedaría bloqueado para siempre.
Patrón saga: cada paso tiene su compensación (deshacer). Si un paso falla, se
compensan los pasos ya hechos en orden INVERSO. Es la versión "action log + undo"
de ADR-009. La compensación debe ser idempotente: puede ejecutarse dos veces.
"""

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class Paso:
    nombre: str
    hacer: Callable[[], None]
    deshacer: Callable[[], None]


@dataclass
class ResultadoSaga:
    ok: bool
    log: list[str] = field(default_factory=list)


def ejecutar_saga(pasos: list[Paso]) -> ResultadoSaga:
    hechos: list[Paso] = []
    log: list[str] = []
    for paso in pasos:
        try:
            paso.hacer()
        except Exception as error:  # noqa: BLE001 - cualquier fallo dispara la compensación
            log.append(f"FALLO {paso.nombre}: {type(error).__name__}")
            for previo in reversed(hechos):
                previo.deshacer()
                log.append(f"DESHECHO {previo.nombre}")
            return ResultadoSaga(ok=False, log=log)
        hechos.append(paso)
        log.append(f"OK {paso.nombre}")
    return ResultadoSaga(ok=True, log=log)
