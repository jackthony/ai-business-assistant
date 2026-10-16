"""Catálogo de servicios: resuelve el `service_id` con código, no con el modelo."""

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from rag.embedding import tokenize


class Service(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    service_id: str
    nombre: str
    activo: bool = True
    sensible_clinico: bool = False


class ServiceCatalog:
    def __init__(self, services: list[Service]) -> None:
        self._by_id = {s.service_id: s for s in services if s.activo}
        self._tokens = {sid: set(tokenize(s.nombre)) for sid, s in self._by_id.items()}

    @classmethod
    def from_file(cls, path: Path) -> "ServiceCatalog":
        items = json.loads(path.read_text(encoding="utf-8"))["items"]
        return cls([Service.model_validate(i) for i in items])

    def get(self, service_id: str) -> Service | None:
        return self._by_id.get(service_id)

    def find(self, query: str) -> list[Service]:
        """Servicios cuyo nombre contiene TODAS las palabras de la consulta.

        Si uno solo coincide exacto con la consulta, gana; si no, devuelve todos los candidatos
        (más de uno = ambiguo: hay que preguntar a la clienta).
        """
        q = set(tokenize(query))
        if not q:
            return []
        found = [sid for sid, toks in self._tokens.items() if q <= toks]
        exact = [sid for sid in found if self._tokens[sid] == q]
        return [self._by_id[sid] for sid in (exact if len(exact) == 1 else found)]
