"""Detección determinista de lo que el bot NO atiende: salud y pedido de hablar con una persona.

Código antes que modelo (ADR-009): un patrón que falla en silencio es mejor que un LLM que opina de
salud. La lista es conservadora (ante la duda, deriva) y se mide con los evals (#143); el clasificador
de 1 token con logprobs del plan (S9 D1) puede sumarse después sin cambiar este contrato.
"""

import re
import unicodedata
from dataclasses import dataclass
from typing import Literal

Reason = Literal["clinical", "human_requested"]

# Síntomas, medicación y consejo de salud: el bot no opina nunca.
CLINICAL_RE = re.compile(
    r"\b("
    r"dolor|duele\w*|sangr\w+|hemorrag\w+|fiebre|infeccion\w*|inflamacion|mareo\w*|nausea\w*|"
    r"vomit\w+|sintoma\w*|picazon|comezon|ardor|flujo\s+(?:raro|anormal|con\s+olor)|"
    r"medicament\w+|medicina\w*|pastilla\w*|dosis|receta\w*|antibiotic\w+|diagnostic\w+|"
    r"contraindicaci\w+|efectos?\s+secundarios?|"
    r"embarazada|lactando|dar\s+de\s+lactar|"
    r"es\s+normal|es\s+seguro|es\s+peligroso|(?:puedo|debo|deberia)\s+(?:tomar|usar|aplicar)|"
    r"que\s+(?:hago|me\s+recomiendas?|me\s+recomienda)|"
    r"me\s+siento\s+mal|salio\s+positivo|tengo\s+(?:un\s+)?(?:bulto|herida|mancha)"
    r")\b"
)

# Pedido explícito de una persona.
HUMAN_RE = re.compile(
    r"\b("
    r"(?:hablar|comunicarme|conversar|contactarme)\s+con\s+(?:una?\s+|la\s+|el\s+)?"
    r"(?:persona|humano|asesor\w*|encargad\w*|especialista|doctor\w*|alguien|operador\w*|ejecutiv\w*)|"
    r"(?:pasame|comunicame|ponme)\s+con\s+\w+|"
    r"(?:persona|atencion)\s+(?:real|humana)|"
    r"que\s+me\s+(?:atienda|llame|escriba)\s+(?:una\s+)?(?:persona|alguien|especialista)"
    r")\b"
)

# Urgencia: la persona que recibe la alerta debe verla primero.
URGENT_RE = re.compile(
    r"\b(emergencia|hemorrag\w+|sangrado\s+abundante|desmay\w+|convulsi\w+|no\s+puedo\s+respirar|"
    r"mucho\s+dolor|dolor\s+(?:fuerte|intenso)|duele\w*\s+(?:mucho|demasiado|muchisimo)|quiero\s+morir\w*|hacerme\s+dano|suicid\w+)\b"
)


@dataclass(frozen=True)
class Signal:
    reason: Reason
    urgent: bool = False


def _plain(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def classify(text: str) -> Signal | None:
    """Señal de derivación o None. Salud gana sobre «quiero una persona»."""
    plain = _plain(text)
    urgent = bool(URGENT_RE.search(plain))
    if urgent or CLINICAL_RE.search(plain):
        return Signal("clinical", urgent)
    if HUMAN_RE.search(plain):
        return Signal("human_requested")
    return None
