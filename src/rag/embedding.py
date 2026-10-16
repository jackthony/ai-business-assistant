"""Puerto de embeddings y un adaptador léxico determinista para pruebas y desarrollo offline.

`LexicalEmbedder` NO es semántico: cuenta palabras con un hash estable (crc32, nunca `hash()`, que
cambia entre procesos y recupera ruido). Sirve para pruebas y para correr sin Ollama; en producción
se usa el embedder de Ollama (`models.ollama`).
"""

import math
import re
import unicodedata
import zlib
from typing import Protocol

STOPWORDS = frozenset(
    {
        *(
            "el",
            "la",
            "los",
            "las",
            "un",
            "una",
            "unos",
            "unas",
            "de",
            "del",
            "al",
            "y",
            "o",
        ),
        *("a", "en", "por", "para", "con", "que", "cual", "cuanto", "cuanta", "cuesta"),
        *("cuestan", "es", "son", "me", "mi", "tu", "su", "se", "lo", "hay", "tiene"),
        *("tienen", "quiero", "quisiera", "hola"),
    }
)


class Embedder(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...


def _tokens(text: str) -> list[str]:
    plain = unicodedata.normalize("NFKD", text.lower())
    plain = "".join(c for c in plain if not unicodedata.combining(c))
    return [t for t in re.findall(r"[a-z0-9]+", plain) if t not in STOPWORDS]


class LexicalEmbedder:
    def __init__(self, dims: int = 512) -> None:
        self.dims = dims

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._one(t) for t in texts]

    def _one(self, text: str) -> list[float]:
        vec = [0.0] * self.dims
        for tok in _tokens(text):
            vec[zlib.crc32(tok.encode("utf-8")) % self.dims] += 1.0
        norm = math.sqrt(sum(v * v for v in vec))
        if norm == 0:
            vec[0] = 1.0  # vector no nulo: sin palabras útiles queda lejos de todo
            return vec
        return [v / norm for v in vec]
