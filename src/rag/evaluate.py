import json
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, ConfigDict

from rag.store import Passage


class Searcher(Protocol):
    def search(self, query: str, k: int = 4) -> list[Passage]: ...


class GoldenCase(BaseModel):
    model_config = ConfigDict(frozen=True)
    question: str
    expected_doc_id: str | None = None


class CaseResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    question: str
    expected_doc_id: str | None
    found_doc_ids: list[str]
    passed: bool


class RetrievalReport(BaseModel):
    model_config = ConfigDict(frozen=True)
    total: int
    passed: int
    failures: list[CaseResult]

    @property
    def ok(self) -> bool:
        return self.total > 0 and not self.failures


class Calibration(BaseModel):
    model_config = ConfigDict(frozen=True)
    in_scope_max: float | None
    out_scope_min: float | None
    suggested: float | None
    unreachable: list[str]


def load_golden(path: Path) -> list[GoldenCase]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("items", [])

    cases: list[GoldenCase] = []
    for item in items:
        if isinstance(item, dict):
            cases.append(GoldenCase(**item))
        else:
            raise TypeError(f"Caso golden inválido (debe ser diccionario): {item}")
    return cases


def suggest_max_distance(
    in_scope_scores: list[float], out_scope_scores: list[float]
) -> float | None:
    if not in_scope_scores or not out_scope_scores:
        return None

    in_max = max(in_scope_scores)
    out_min = min(out_scope_scores)

    if in_max >= out_min:
        return None

    return round((in_max + out_min) / 2.0, 3)


def calibrate(searcher: Searcher, cases: list[GoldenCase], k: int = 10) -> Calibration:
    in_scores: list[float] = []
    out_scores: list[float] = []
    unreachable: list[str] = []

    for case in cases:
        passages = searcher.search(case.question, k=k)
        if case.expected_doc_id is None:
            for p in passages:
                out_scores.append(p.distance)
        else:
            matched = [p for p in passages if p.doc_id == case.expected_doc_id]
            if matched:
                best_dist = min(p.distance for p in matched)
                in_scores.append(best_dist)
            else:
                unreachable.append(case.question)

    suggested = suggest_max_distance(in_scores, out_scores)

    return Calibration(
        in_scope_max=round(max(in_scores), 3) if in_scores else None,
        out_scope_min=round(min(out_scores), 3) if out_scores else None,
        suggested=suggested,
        unreachable=unreachable,
    )


def evaluate_retrieval(
    searcher: Searcher, cases: list[GoldenCase], k: int = 4
) -> RetrievalReport:
    total = len(cases)
    passed = 0
    failures: list[CaseResult] = []

    for case in cases:
        passages = searcher.search(case.question, k=k)
        found_doc_ids = [p.doc_id for p in passages]

        is_passed = False
        if case.expected_doc_id is None:
            if not found_doc_ids:
                is_passed = True
        else:
            if case.expected_doc_id in found_doc_ids:
                is_passed = True

        if is_passed:
            passed += 1
        else:
            failures.append(
                CaseResult(
                    question=case.question,
                    expected_doc_id=case.expected_doc_id,
                    found_doc_ids=found_doc_ids,
                    passed=False,
                )
            )

    return RetrievalReport(total=total, passed=passed, failures=failures)
