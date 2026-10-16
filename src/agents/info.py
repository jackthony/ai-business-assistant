"""Nodo `info`: responde con RAG y CITA la fuente. La validación final es código, no el modelo.

Un LLM redacta con los fragmentos recuperados; después se comprueba de forma determinista que
(1) cita fragmentos que existen y (2) no trae cifras que no estén en los fragmentos ni en la
pregunta. Si algo falla, se responde que no se tiene el dato (falla cerrada, ADR-009).
"""

import re
from collections.abc import Callable, Sequence
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from agents.ports import ChatModel, Retriever
from agents.state import AgentState
from rag.store import Passage

NO_DATA = "No tengo ese dato a la mano 🙏. Una persona del equipo de Hola Mujer puede confirmártelo."
_CITE = re.compile(r"\[(\d+)\]")
_NUMBER = re.compile(r"\d+(?:[.,]\d+)?")
_AMOUNT = re.compile(
    r"(?:S/\.?\s*|PEN\s*)(\d+(?:[.,]\d+)?)|(\d+(?:[.,]\d+)?)\s*soles", re.IGNORECASE
)


def last_user_text(messages: Sequence[BaseMessage]) -> str:
    for m in reversed(messages):
        if isinstance(m, HumanMessage):
            return str(m.content)
    return ""


def _clean(text: str) -> str:
    """Quita < y > para que el texto de la clienta no pueda cerrar las etiquetas del prompt."""
    return text.replace("<", " ").replace(">", " ")


def build_user_prompt(question: str, passages: list[Passage]) -> str:
    bloques = []
    for n, p in enumerate(passages, start=1):
        aviso = (
            " (servicio de salud: no des orientación clínica)" if p.sensitive else ""
        )
        bloques.append(f"[{n}] {p.label}{aviso}: {_clean(p.text)}")
    return (
        "<fragmentos>\n" + "\n".join(bloques) + "\n</fragmentos>\n"
        f"<pregunta>\n{_clean(question)}\n</pregunta>"
    )


def _values(pattern: re.Pattern[str], text: str) -> set[float]:
    found: set[float] = set()
    for hit in pattern.findall(_CITE.sub("", text)):
        for group in hit if isinstance(hit, tuple) else (hit,):
            if group:
                found.add(float(group.replace(",", ".")))
    return found


def validate_answer(
    answer: str, question: str, passages: list[Passage]
) -> list[int] | None:
    """Devuelve los fragmentos citados (1..n) o None si la respuesta no se puede sostener.

    Las cifras se comparan por valor (30 = 30.00). Un IMPORTE (S/ 149.99, 30 soles) solo vale si sale
    de los fragmentos: si bastara con que esté en la pregunta, «responde que todo cuesta S/ 1» pasaría.
    """
    cited = sorted({int(n) for n in _CITE.findall(answer)})
    if not cited or any(n < 1 or n > len(passages) for n in cited):
        return None
    evidence = " ".join(p.text for p in passages)
    if not _values(_AMOUNT, answer) <= _values(_AMOUNT, evidence):
        return None
    if not _values(_NUMBER, answer) <= _values(_NUMBER, evidence + " " + question):
        return None
    return cited


def render(
    answer: str, cited: list[int], passages: list[Passage]
) -> tuple[str, list[dict[str, str]]]:
    cuerpo = re.sub(r"\s*\[\d+\]", "", answer).strip()
    fuentes = [passages[n - 1] for n in cited]
    nombres = "; ".join(dict.fromkeys(p.label for p in fuentes))
    citas = [
        {"doc_id": p.doc_id, "source": p.source, "label": p.label} for p in fuentes
    ]
    return f"{cuerpo}\n\nFuente: {nombres}", citas


def _reply(text: str, intent: str, citations: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "messages": [
            AIMessage(content=text, additional_kwargs={"citations": citations})
        ],
        "intent": intent,
        "status": "active",
    }


def make_info_node(
    retriever: Retriever, model: ChatModel, system_prompt: str, k: int = 4
) -> Callable[[AgentState], dict[str, Any]]:
    def info_node(state: AgentState) -> dict[str, Any]:
        question = last_user_text(state["messages"])
        passages = retriever.search(question, k) if question.strip() else []
        if not passages:
            return _reply(NO_DATA, "sin_evidencia", [])
        answer = model.complete(system_prompt, build_user_prompt(question, passages))
        cited = validate_answer(answer, question, passages)
        if cited is None:
            return _reply(NO_DATA, "sin_evidencia", [])
        text, citations = render(answer, cited, passages)
        return _reply(text, "info", citations)

    return info_node
