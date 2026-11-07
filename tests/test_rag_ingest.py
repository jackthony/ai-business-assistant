# tests/test_rag_ingest.py
import json

import pytest
from conftest import DATA

from rag.documents import load_documents
from rag.embedding import LexicalEmbedder
from rag.ingest import corpus_fingerprint, ingest_corpus, main
from rag.store import ChromaStore


def test_i1_corpus_fingerprint_stability():
    docs = load_documents(DATA)
    fp1 = corpus_fingerprint(docs)
    fp2 = corpus_fingerprint(list(reversed(docs)))
    assert fp1 == fp2
    assert len(fp1) == 64
    assert all(c in "0123456789abcdef" for c in fp1)


def test_i2_corpus_fingerprint_text_change():
    docs = load_documents(DATA)
    fp_orig = corpus_fingerprint(docs)
    modified = docs[0].model_copy(update={"text": docs[0].text + " cambio"})
    docs_mod = [modified] + docs[1:]
    assert corpus_fingerprint(docs_mod) != fp_orig


def test_i3_corpus_fingerprint_sensitive_change():
    docs = load_documents(DATA)
    fp_orig = corpus_fingerprint(docs)
    modified = docs[0].model_copy(update={"sensitive": not docs[0].sensitive})
    docs_mod = [modified] + docs[1:]
    assert corpus_fingerprint(docs_mod) != fp_orig


def test_i4_ingest_corpus_basic(tmp_path):
    store = ChromaStore(LexicalEmbedder(), "test-i4", path=str(tmp_path))
    docs = load_documents(DATA)
    report = ingest_corpus(DATA, store, "hola_mujer")

    assert report.namespace == "hola_mujer"
    assert report.documents == len(docs)
    assert sum(report.by_kind.values()) == report.documents

    json_path = DATA / "servicios.json"
    with open(json_path, "r", encoding="utf-8") as f:
        content = json.load(f)
        items = content.get("items", content) if isinstance(content, dict) else content
        expected_services = sum(
            1 for item in items if isinstance(item, dict) and item.get("activo", True)
        )
        assert report.by_kind["servicio"] == expected_services

    assert report.fingerprint == corpus_fingerprint(docs)


def test_i5_ingest_corpus_idempotency(tmp_path):
    store1 = ChromaStore(LexicalEmbedder(), "test-i5", path=str(tmp_path))
    store2 = ChromaStore(LexicalEmbedder(), "test-i5", path=str(tmp_path))

    rep1 = ingest_corpus(DATA, store1, "hola_mujer")
    rep2 = ingest_corpus(DATA, store2, "hola_mujer")

    assert rep1.documents == rep2.documents
    assert rep1.fingerprint == rep2.fingerprint

    col = store2._client.get_collection("test-i5")
    assert col.count() == rep1.documents

    assert store2.search("direccion local", k=1)[0].doc_id == "NEG-ADDRESS"


def test_i6_main_cli_success(tmp_path, capsys):
    code1 = main(["--chroma-path", str(tmp_path)])
    assert code1 == 0

    code2 = main(["--chroma-path", str(tmp_path)])
    assert code2 == 0

    captured = capsys.readouterr()
    lines = [line for line in captured.out.strip().split("\n") if line]
    assert len(lines) == 2

    data1 = json.loads(lines[0])
    data2 = json.loads(lines[1])
    assert set(data1.keys()) == {"namespace", "documents", "by_kind", "fingerprint"}
    assert data1["documents"] == len(load_documents(DATA))
    assert data1["fingerprint"] == data2["fingerprint"]


def test_i7_main_cli_missing_data(tmp_path, capsys):
    code = main(["--data-dir", str(tmp_path / "nada"), "--chroma-path", str(tmp_path)])
    assert code == 1
    captured = capsys.readouterr()
    assert "no existe" in captured.err.lower()
    assert captured.out == ""


def test_i8_main_cli_invalid_embedder(tmp_path):
    with pytest.raises(SystemExit) as excinfo:
        main(["--embedder", "inventado", "--chroma-path", str(tmp_path)])
    assert excinfo.value.code == 2
