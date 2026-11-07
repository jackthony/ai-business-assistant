import json
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from agents.style import check_reply_style


class FewShot(BaseModel):
    model_config = {"frozen": True}
    id: str = Field(pattern=r"^[a-z0-9-]{3,40}$")
    tipo: Literal["precio", "consulta", "descuento", "otra"]
    objecion: str = Field(min_length=3)
    respuesta: str = Field(min_length=3)


def load_fewshots(path: Path) -> list[FewShot]:
    """Carga los ejemplos desde un JSON, valida con Pydantic y detecta IDs duplicados."""
    contenido = json.loads(path.read_text(encoding="utf-8"))
    items = contenido.get("items", [])

    vistos = set()
    fewshots = []
    for item in items:
        fs = FewShot(**item)
        if fs.id in vistos:
            raise ValueError(f"ID duplicado encontrado en fewshots: {fs.id}")
        vistos.add(fs.id)
        fewshots.append(fs)

    return fewshots


def violations(shot: FewShot) -> list[str]:
    """Evalúa las violaciones de estilo y contenido de un FewShot."""
    codigos = []

    # 1. Estilo base (reutilizando agents/style.py)
    estilo_fallos = check_reply_style(shot.respuesta)
    if estilo_fallos:
        codigos.extend(estilo_fallos)

    # 2. Falta de cita [1]
    if "[1]" not in shot.respuesta:
        codigos.append("no_citation")

    # 3. Detección de montos / importes monetarios (S/ o soles)
    patron_amount = r"S/\s*\d+|\b\d+\s*soles\b"
    if re.search(patron_amount, shot.respuesta, re.IGNORECASE):
        codigos.append("amount")

    # 4. Detección de horas explícitas (H:MM o HH:MM)
    patron_hour = r"\b\d{1,2}:\d{2}\b"
    if re.search(patron_hour, shot.respuesta):
        codigos.append("hour")

    return codigos


def render_fewshots(shots: list[FewShot]) -> str:
    """Renderiza la sección de pocos ejemplos siguiendo el formato exacto del contrato §5.2."""
    header = "Ejemplos de cómo responder a objeciones (solo muestran el tono; los datos salen siempre de <fragmentos>):"
    bloques = [header]
    for shot in shots:
        bloques.append(f"Clienta: {shot.objecion}\nHola Mujer: {shot.respuesta}")
    return "\n\n".join(bloques)
