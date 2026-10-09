import os

# Seguridad: deserialización estricta del checkpoint (ver README §Seguridad).
os.environ.setdefault("LANGGRAPH_STRICT_MSGPACK", "true")

from langgraph.checkpoint.sqlite import SqliteSaver
from memoria_minima import config_de, construir_grafo


def test_la_memoria_sobrevive_a_un_reinicio(tmp_path):
    db = str(tmp_path / "memoria.db")
    cfg = config_de("51900000000")

    with SqliteSaver.from_conn_string(db) as saver:  # "proceso 1"
        grafo = construir_grafo(saver)
        salida = grafo.invoke({"historial": ["hola"]}, cfg)
    assert salida["historial"] == ["hola", "eco: hola"]

    with SqliteSaver.from_conn_string(
        db
    ) as saver:  # "proceso 2": reinicio, mismo archivo
        grafo = construir_grafo(saver)
        salida = grafo.invoke({"historial": ["¿precios?"]}, cfg)
    assert salida["historial"] == ["hola", "eco: hola", "¿precios?", "eco: ¿precios?"]


def test_cada_telefono_tiene_su_propio_hilo(tmp_path):
    db = str(tmp_path / "memoria.db")
    with SqliteSaver.from_conn_string(db) as saver:
        grafo = construir_grafo(saver)
        grafo.invoke({"historial": ["hola"]}, config_de("51900000001"))
        otra = grafo.invoke({"historial": ["buenas"]}, config_de("51900000002"))
    assert otra["historial"] == ["buenas", "eco: buenas"]
