# tests/test_rag_evaluate.py
import re

from conftest import DATA

from rag.documents import load_documents
from rag.embedding import LexicalEmbedder
from rag.evaluate import (
    GoldenCase,
    calibrate,
    evaluate_retrieval,
    load_golden,
    suggest_max_distance,
)
from rag.store import ChromaStore, Passage


class FakeSearcher:
    def __init__(self, responses: dict[str, list[Passage]]):
        self.responses = responses

    def search(self, query: str, k: int = 4) -> list[Passage]:
        passages = self.responses.get(query, [])
        return passages[:k]


def test_e1_evaluate_retrieval_success():
    passages_a = [
        Passage(
            doc_id="DOC-1",
            text="x",
            label="x",
            source="x",
            sensitive=False,
            distance=0.2,
        )
    ]
    passages_b = [
        Passage(
            doc_id="DOC-2",
            text="x",
            label="x",
            source="x",
            sensitive=False,
            distance=0.3,
        )
    ]
    searcher = FakeSearcher({"pregunta 1": passages_a, "pregunta 2": passages_b})
    cases = [
        GoldenCase(question="pregunta 1", expected_doc_id="DOC-1"),
        GoldenCase(question="pregunta 2", expected_doc_id="DOC-2"),
    ]
    report = evaluate_retrieval(searcher, cases, k=4)
    assert report.ok is True
    assert report.total == 2
    assert report.passed == 2
    assert len(report.failures) == 0


def test_e2_evaluate_retrieval_failure():
    passages_a = [
        Passage(
            doc_id="DOC-1",
            text="x",
            label="x",
            source="x",
            sensitive=False,
            distance=0.2,
        )
    ]
    passages_b = [
        Passage(
            doc_id="DOC-99",
            text="x",
            label="x",
            source="x",
            sensitive=False,
            distance=0.3,
        )
    ]
    searcher = FakeSearcher({"pregunta 1": passages_a, "pregunta 2": passages_b})
    cases = [
        GoldenCase(question="pregunta 1", expected_doc_id="DOC-1"),
        GoldenCase(question="pregunta 2", expected_doc_id="DOC-2"),
    ]
    report = evaluate_retrieval(searcher, cases, k=4)
    assert report.ok is False
    assert report.passed == 1
    assert len(report.failures) == 1
    assert report.failures[0].question == "pregunta 2"
    assert "DOC-99" in report.failures[0].found_doc_ids


def test_e3_evaluate_retrieval_none_expected():
    searcher_ok = FakeSearcher({"fuera 1": []})
    rep_ok = evaluate_retrieval(
        searcher_ok, [GoldenCase(question="fuera 1", expected_doc_id=None)], k=4
    )
    assert rep_ok.ok is True

    searcher_fail = FakeSearcher(
        {
            "fuera 2": [
                Passage(
                    doc_id="DOC-1",
                    text="x",
                    label="x",
                    source="x",
                    sensitive=False,
                    distance=0.2,
                )
            ]
        }
    )
    rep_fail = evaluate_retrieval(
        searcher_fail, [GoldenCase(question="fuera 2", expected_doc_id=None)], k=4
    )
    assert rep_fail.ok is False


def test_e4_evaluate_retrieval_k_sensitivity():
    passages = [
        Passage(
            doc_id="DOC-WRONG",
            text="x",
            label="x",
            source="x",
            sensitive=False,
            distance=0.1,
        ),
        Passage(
            doc_id="DOC-RIGHT",
            text="x",
            label="x",
            source="x",
            sensitive=False,
            distance=0.2,
        ),
    ]
    searcher = FakeSearcher({"test": passages})
    cases = [GoldenCase(question="test", expected_doc_id="DOC-RIGHT")]

    rep_k1 = evaluate_retrieval(searcher, cases, k=1)
    assert rep_k1.passed == 0

    rep_k2 = evaluate_retrieval(searcher, cases, k=2)
    assert rep_k2.passed == 1


def test_e5_suggest_max_distance_normal():
    in_scores = [0.2, 0.5]
    out_scores = [0.9, 1.0]
    threshold = suggest_max_distance(in_scores, out_scores)
    assert threshold == 0.7


def test_e6_suggest_max_distance_overlap():
    assert suggest_max_distance([0.2, 0.95], [0.9, 1.0]) is None
    assert suggest_max_distance([0.9], [0.9]) is None


def test_e7_suggest_max_distance_empty():
    assert suggest_max_distance([], [0.9]) is None
    assert suggest_max_distance([0.2], []) is None


def test_e8_calibrate():
    passages = {
        "q1": [
            Passage(
                doc_id="DOC-1",
                text="x",
                label="x",
                source="x",
                sensitive=False,
                distance=0.4,
            )
        ],
        "q2": [
            Passage(
                doc_id="DOC-OTHER",
                text="x",
                label="x",
                source="x",
                sensitive=False,
                distance=0.5,
            ),
            Passage(
                doc_id="DOC-2",
                text="x",
                label="x",
                source="x",
                sensitive=False,
                distance=0.6,
            ),
        ],
        "q3": [
            Passage(
                doc_id="DOC-OUT",
                text="x",
                label="x",
                source="x",
                sensitive=False,
                distance=1.0,
            ),
            Passage(
                doc_id="DOC-OUT2",
                text="x",
                label="x",
                source="x",
                sensitive=False,
                distance=1.2,
            ),
        ],
        "q4": [
            Passage(
                doc_id="DOC-FAIL",
                text="x",
                label="x",
                source="x",
                sensitive=False,
                distance=0.3,
            )
        ],
    }
    searcher = FakeSearcher(passages)
    cases = [
        GoldenCase(question="q1", expected_doc_id="DOC-1"),
        GoldenCase(question="q2", expected_doc_id="DOC-2"),
        GoldenCase(question="q3", expected_doc_id=None),
        GoldenCase(question="q4", expected_doc_id="DOC-NONEXISTENT"),
    ]
    res = calibrate(searcher, cases, k=4)
    assert res.in_scope_max == 0.6
    assert res.out_scope_min == 1.0
    assert res.suggested == 0.8
    assert res.unreachable == ["q4"]


def test_e9_load_golden():
    cases = load_golden(DATA / "rag_golden.json")
    valid_doc_ids = {d.doc_id for d in load_documents(DATA)}

    assert isinstance(cases, list)
    assert len(cases) >= 10

    none_expected_count = sum(1 for c in cases if c.expected_doc_id is None)
    assert none_expected_count >= 2

    expected_ids = {c.expected_doc_id for c in cases if c.expected_doc_id is not None}
    assert len(expected_ids) >= 6

    questions = {c.question for c in cases}
    assert len(questions) == len(cases)

    for c in cases:
        if c.expected_doc_id is not None:
            assert c.expected_doc_id in valid_doc_ids


def test_e10_golden_no_pii_or_phone():
    with open(DATA / "rag_golden.json", "r", encoding="utf-8") as f:
        content = f.read()

    assert "@" not in content
    assert not re.search(r"\bdni\b", content, re.IGNORECASE)
    assert not re.search(r"\b(\+?51)?9\d{8}\b", content)


def test_e11_calibrate_with_real_store(tmp_path):
    store = ChromaStore(
        LexicalEmbedder(), "test-e11", path=str(tmp_path), max_distance=2.0
    )
    store.ingest(load_documents(DATA))
    cases = load_golden(DATA / "rag_golden.json")

    res = calibrate(store, cases, k=4)
    assert res.unreachable == []
    assert res.suggested is not None
    assert res.in_scope_max < res.suggested < res.out_scope_min


def test_e12_evaluate_retrieval_with_calibrated_store(tmp_path):
    store_cal = ChromaStore(
        LexicalEmbedder(), "test-e12-cal", path=str(tmp_path), max_distance=2.0
    )
    store_cal.ingest(load_documents(DATA))
    cases = load_golden(DATA / "rag_golden.json")

    res_cal = calibrate(store_cal, cases, k=4)

    store_eval = ChromaStore(
        LexicalEmbedder(),
        "test-e12-eval",
        path=str(tmp_path),
        max_distance=res_cal.suggested,
    )
    store_eval.ingest(load_documents(DATA))

    report = evaluate_retrieval(store_eval, cases, k=4)
    fail_msgs = [
        f"Q: {f.question}, Expected: {f.expected_doc_id}, Found: {f.found_doc_ids}"
        for f in report.failures
    ]
    assert report.ok is True, "\n".join(fail_msgs)
