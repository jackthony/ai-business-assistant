"""La memoria sobrevive al reinicio y cada teléfono tiene su hilo (tu AgentState)."""

import os

os.environ.setdefault("LANGGRAPH_STRICT_MSGPACK", "true")

from langgraph.checkpoint.sqlite import SqliteSaver

from agents.graph import build_graph, config_for


def _contenidos(mensajes) -> list[str]:
    """Los mensajes son objetos HumanMessage: devuelve solo el texto."""
    return [getattr(m, "content", m) for m in mensajes]


def test_la_memoria_sobrevive_a_un_reinicio(tmp_path):
    db = str(tmp_path / "agente.db")
    cfg = config_for("51900000000")

    with SqliteSaver.from_conn_string(db) as saver:  # "proceso 1"
        grafo = build_graph(saver)
        grafo.invoke({"messages": ["hola"]}, cfg)

    with SqliteSaver.from_conn_string(db) as saver:  # "proceso 2": reinicio
        grafo = build_graph(saver)
        salida = grafo.invoke({"messages": ["¿precios?"]}, cfg)

    assert _contenidos(salida["messages"]) == [
        "hola",
        "eco: hola",
        "¿precios?",
        "eco: ¿precios?",
    ]


def test_cada_telefono_tiene_su_propio_hilo(tmp_path):
    db = str(tmp_path / "agente.db")
    with SqliteSaver.from_conn_string(db) as saver:
        grafo = build_graph(saver)
        grafo.invoke({"messages": ["hola"]}, config_for("51900000001"))
        otra = grafo.invoke({"messages": ["buenas"]}, config_for("51900000002"))
    assert _contenidos(otra["messages"]) == ["buenas", "eco: buenas"]
