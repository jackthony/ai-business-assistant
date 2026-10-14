"""CLI para probar el grafo SIN WhatsApp (contrato S05 D1).

Uso: python -m agents.cli [--phone TEL] [--tenant ID] TEXTO
"""

import argparse
import sys

from langchain_core.messages import HumanMessage

from agents.graph import build_graph


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
    salida = build_graph().invoke(entrada)
    print(salida["messages"][-1].content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
