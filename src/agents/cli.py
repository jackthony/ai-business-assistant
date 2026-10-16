"""CLI para probar el grafo SIN WhatsApp (contrato S05 D1).

Uso: python -m agents.cli [--phone TEL] [--tenant ID] TEXTO
"""

import argparse
import sys

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from infrastructure.wiring import build_default_graph


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agents.cli")
    parser.add_argument("--phone", default="51900000000")
    parser.add_argument("--tenant", default="hola_mujer")
    parser.add_argument("texto")
    args = parser.parse_args(argv)

    entrada = {
        "messages": [HumanMessage(content=args.texto)],
        "phone": args.phone,
        "tenant": args.tenant,
        "intent": None,
        "status": "nuevo",
    }
    grafo = build_default_graph(args.tenant)
    config: RunnableConfig = {"configurable": {"thread_id": args.phone}}
    salida = grafo.invoke(entrada, config)
    print(salida["messages"][-1].content)
    if salida.get("__interrupt__"):
        # En producción aprueba una persona del equipo; aquí se simula para probar el flujo.
        ok = (
            input("Aprobación del equipo — ¿confirmar la cita? [s/N] ").strip().lower()
            == "s"
        )
        salida = grafo.invoke(Command(resume={"approved": ok}), config)
        print(salida["messages"][-1].content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
