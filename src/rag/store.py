"""Almacén vectorial sobre ChromaDB (ADR-004): ingesta reproducible y búsqueda con procedencia."""

from pathlib import Path

import chromadb
from chromadb.config import Settings
from pydantic import BaseModel, ConfigDict

from rag.documents import Document
from rag.embedding import Embedder


class Passage(BaseModel):
    model_config = ConfigDict(frozen=True)

    doc_id: str
    text: str
    label: str
    source: str
    sensitive: bool
    distance: float


class ChromaStore:
    """Un namespace por tenant. `ingest` reconstruye la colección: el índice sale solo de los datos."""

    def __init__(
        self,
        embedder: Embedder,
        namespace: str,
        path: Path | None = None,
        max_distance: float = 0.6,
    ) -> None:
        settings = Settings(anonymized_telemetry=False)
        self._client: chromadb.ClientAPI = (
            chromadb.PersistentClient(path=str(path), settings=settings)
            if path
            else chromadb.EphemeralClient(settings=settings)
        )
        self._embedder = embedder
        self._namespace = namespace
        self._max_distance = max_distance

    def ingest(self, docs: list[Document]) -> int:
        if self._namespace in {c.name for c in self._client.list_collections()}:
            self._client.delete_collection(self._namespace)
        col = self._client.create_collection(
            self._namespace, configuration={"hnsw": {"space": "cosine"}}
        )
        if docs:
            col.add(
                ids=[d.doc_id for d in docs],
                documents=[d.text for d in docs],
                embeddings=self._embedder.embed([d.text for d in docs]),  # type: ignore[arg-type]
                metadatas=[
                    {"label": d.label, "source": d.source, "sensitive": d.sensitive}
                    for d in docs
                ],
            )
        return len(docs)

    def search(self, query: str, k: int = 4) -> list[Passage]:
        col = self._client.get_collection(self._namespace)
        res = col.query(
            query_embeddings=self._embedder.embed([query]),  # type: ignore[arg-type]
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )
        ids, texts = res["ids"][0], (res["documents"] or [[]])[0]
        metas, dists = (res["metadatas"] or [[]])[0], (res["distances"] or [[]])[0]
        return [
            Passage(
                doc_id=i,
                text=t,
                label=str(m["label"]),
                source=str(m["source"]),
                sensitive=bool(m["sensitive"]),
                distance=float(d),
            )
            for i, t, m, d in zip(ids, texts, metas, dists, strict=True)
            if d <= self._max_distance
        ]
