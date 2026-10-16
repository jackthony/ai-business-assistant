"""Fixtures compartidas: datos reales del repo (anonimizados) con embedder léxico, sin red ni modelos."""

import itertools
from pathlib import Path

import pytest

from rag.documents import load_documents
from rag.embedding import LexicalEmbedder
from rag.store import ChromaStore

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hola_mujer"
CONFIGS = ROOT / "configs" / "hola_mujer"
_ns = itertools.count()


class ScriptedModel:
    """ChatModel de prueba: devuelve una respuesta fija y guarda lo que recibió."""

    def __init__(self, *answers: str) -> None:
        self.answers = answers or ("",)
        self.calls: list[tuple[str, str]] = []

    def complete(self, system: str, user: str) -> str:
        self.calls.append((system, user))
        return self.answers[min(len(self.calls), len(self.answers)) - 1]


@pytest.fixture
def store() -> ChromaStore:
    s = ChromaStore(LexicalEmbedder(), f"test-{next(_ns)}")
    s.ingest(load_documents(DATA))
    return s
