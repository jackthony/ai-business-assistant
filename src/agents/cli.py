"""CLI para probar el grafo SIN el canal (antes de tocar WhatsApp).

Uso:  python -m agents.cli 51900000000
"""

import sys

from langgraph.checkpoint.sqlite import SqliteSaver

from agents.graph import build_graph, config_for


def main(phone: str) -> None:
    with SqliteSaver.from_conn_string("data/agente.db") as saver:
        grafo = build_graph(saver)
        print(
            f"Agente mínimo listo (teléfono: {phone}). Escribe 'salir' para terminar."
        )
        while True:
            texto = input("Tú> ").strip()
            if texto.lower() in {"salir", "exit", "quit"}:
                break
            salida = grafo.invoke({"messages": [texto]}, config_for(phone))
            ultimo = salida["messages"][-1]
            print(f"Agente> {getattr(ultimo, 'content', ultimo)}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "51900000000")
