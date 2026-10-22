"""Prompt por componentes: cinco piezas con propósito propio que el código compone."""

import re
from pathlib import Path

from pydantic import BaseModel, ConfigDict, field_validator

HEADINGS = ["Identidad", "Tono", "Límites", "Fuentes y citas", "Memoria"]


class PromptPieces(BaseModel):
    model_config = ConfigDict(frozen=True)

    identity: str
    tone: str
    limits: str
    sources: str
    memory: str

    @field_validator("*")
    @classmethod
    def _not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("la pieza no puede estar vacía")
        return v


def load_prompt_pieces(path: Path) -> PromptPieces:
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    names, bodies = parts[1::2], parts[2::2]
    if names != HEADINGS:
        faltan = [h for h in HEADINGS if h not in names]
        sobran = [n for n in names if n not in HEADINGS]
        raise ValueError(
            f"encabezados incorrectos: faltan {faltan}, sobran {sobran}, orden {names}"
        )
    a, b, c, d, e = (x.strip() for x in bodies)
    return PromptPieces(identity=a, tone=b, limits=c, sources=d, memory=e)


def compose_system_prompt(pieces: PromptPieces) -> str:
    return (
        f"{pieces.identity}\n\n{pieces.tone}\n\n{pieces.limits}\n\n"
        f"{pieces.sources}\n\n{pieces.memory}"
    )
