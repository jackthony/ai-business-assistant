"""CLI para probar el grafo SIN WhatsApp (contrato S05 D1).

Uso: python -m agents.cli [--phone TEL] [--tenant ID] [--db RUTA] TEXTO
"""

import argparse
import sys
from typing import Any

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from infrastructure.wiring import build_default_graph
from memory.sqlite_checkpointer import open_checkpointer
from memory.thread_config import config_for_phone


def _run(
    grafo: Any, args: argparse.Namespace, config: RunnableConfig, persistent: bool
) -> int:
    entrada: dict[str, Any] = {
        "messages": [HumanMessage(content=args.texto)],
        "phone": args.phone,
        "tenant": args.tenant,
        "intent": None,
        "status": "nuevo",
    }
    # Con memoria, si el hilo ya existe NO se pasan intent ni status:
    # pisarían el estado guardado (regla 5.5 del contrato).
    if persistent and grafo.get_state(config).values:
        del entrada["intent"]
        del entrada["status"]
    salida = grafo.invoke(entrada, config)
    print(salida["messages"][-1].content)
    if salida.get("__interrupt__"):
        # En producción aprueba una persona del equipo; aquí se simula.
        ok = (
            input("Aprobación del equipo — ¿confirmar la cita? [s/N] ").strip().lower()
            == "s"
        )
        salida = grafo.invoke(Command(resume={"approved": ok}), config)
        print(salida["messages"][-1].content)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agents.cli")
    parser.add_argument("--phone", default="51900000000")
    parser.add_argument("--tenant", default="hola_mujer")
    parser.add_argument("--db", default=None)
    parser.add_argument("texto")
    args = parser.parse_args(argv)

    if args.db:
        db_config = config_for_phone(args.phone)
        with open_checkpointer(args.db) as saver:
            grafo = build_default_graph(args.tenant, checkpointer=saver)
            return _run(grafo, args, db_config, persistent=True)

    grafo = build_default_graph(args.tenant)
    config: RunnableConfig = {"configurable": {"thread_id": args.phone}}
    return _run(grafo, args, config, persistent=False)


if __name__ == "__main__":
    sys.exit(main())
