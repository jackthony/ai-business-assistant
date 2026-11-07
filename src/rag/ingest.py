import argparse
import hashlib
import sys
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from rag.documents import Document, load_documents
from rag.embedding import Embedder, LexicalEmbedder
from rag.store import ChromaStore

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "hola_mujer"


class IngestReport(BaseModel):
    model_config = ConfigDict(frozen=True)
    namespace: str
    documents: int
    by_kind: dict[str, int]
    fingerprint: str


def corpus_fingerprint(docs: list[Document]) -> str:
    hasher = hashlib.sha256()
    sorted_docs = sorted(docs, key=lambda d: d.doc_id)
    serialized_docs = []
    for doc in sorted_docs:
        # Usar separador \x1f y asegurar concatenación robusta
        payload = f"{doc.doc_id}\x1f{doc.kind}\x1f{doc.source}\x1f{doc.sensitive}\x1f{doc.text}"
        serialized_docs.append(payload)

    full_corpus_str = "\n".join(serialized_docs)
    hasher.update(full_corpus_str.encode("utf-8"))
    return hasher.hexdigest()


def ingest_corpus(data_dir: Path, store: ChromaStore, namespace: str) -> IngestReport:
    if not data_dir.exists():
        raise FileNotFoundError(f"El directorio de datos no existe: {data_dir}")

    docs = load_documents(data_dir)

    # store.ingest ya reconstruye/actualiza el índice de forma autónoma
    store.ingest(docs)

    by_kind: dict[str, int] = {}
    for doc in docs:
        by_kind[doc.kind] = by_kind.get(doc.kind, 0) + 1

    fp = corpus_fingerprint(docs)

    return IngestReport(
        namespace=namespace, documents=len(docs), by_kind=by_kind, fingerprint=fp
    )


def main(argv: list[str] | None = None) -> int:
    base_dir = Path(__file__).resolve().parents[2]

    parser = argparse.ArgumentParser(description="CLI para ingesta de corpus RAG")
    parser.add_argument(
        "--data-dir",
        type=str,
        default=str(DATA_DIR),
        help="Directorio con los datos fuente",
    )
    parser.add_argument(
        "--chroma-path",
        type=str,
        default=".chroma",
        help="Ruta de almacenamiento de ChromaDB",
    )
    parser.add_argument(
        "--tenant", type=str, default="hola_mujer", help="Tenant del proyecto"
    )
    parser.add_argument(
        "--embedder",
        type=str,
        default="lexical",
        choices=["lexical", "ollama"],
        help="Tipo de embedder a utilizar",
    )

    args = parser.parse_args(argv)

    data_path = Path(args.data_dir)
    if not data_path.exists():
        print(f"Error: El directorio de datos no existe: {data_path}", file=sys.stderr)
        return 1

    namespace_file = base_dir / "configs" / args.tenant / "rag.namespace"
    if namespace_file.exists():
        namespace = namespace_file.read_text(encoding="utf-8").strip()
    else:
        namespace = args.tenant

    embedder: Embedder

    if args.embedder == "ollama":
        try:
            from models.ollama import OllamaEmbedder

            embedder = OllamaEmbedder()
        except ImportError:
            raise ImportError("No se pudo importar OllamaEmbedder desde models.ollama")
    else:
        embedder = LexicalEmbedder()

    store = ChromaStore(embedder, namespace, path=args.chroma_path)

    report = ingest_corpus(data_path, store, namespace)
    print(report.model_dump_json())
    return 0


if __name__ == "__main__":
    sys.exit(main())
