"""Fixtures compartidas: datos reales del repo (anonimizados) con embedder léxico, sin red ni modelos."""

import itertools
from pathlib import Path

import pytest

from rag.documents import load_documents
from rag.embedding import LexicalEmbedder
from rag.store import ChromaStore

DATA = Path(__file__).resolve().parents[1] / "data" / "hola_mujer"
_ns = itertools.count()


class ScriptedModel:
    """ChatModel de prueba: devuelve una respuesta fija y guarda lo que recibió."""

    def __init__(self, answer: str = "") -> None:
        self.answer = answer
        self.calls: list[tuple[str, str]] = []

    def complete(self, system: str, user: str) -> str:
        self.calls.append((system, user))
        return self.answer


@pytest.fixture
def store() -> ChromaStore:
    s = ChromaStore(LexicalEmbedder(), f"test-{next(_ns)}")
    s.ingest(load_documents(DATA))
    return s
