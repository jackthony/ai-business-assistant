from contextlib import AbstractContextManager

from langgraph.checkpoint.sqlite import SqliteSaver


def open_checkpointer(db_path: str) -> AbstractContextManager[SqliteSaver]:
    """Abre la memoria persistente en el archivo db_path (úsala con `with`)."""
    return SqliteSaver.from_conn_string(db_path)
