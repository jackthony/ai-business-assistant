"""Documentos del RAG: qué datos de `data/hola_mujer/` entran y cómo se redactan.

Solo entra lo aprobado: servicios activos, promociones con `usable_en_rag` y datos del negocio
`CONFIRMED` de una lista corta. La duración no se escribe mientras `duracion_verificada` sea falso,
y de un servicio `sensible_clinico` solo se redacta nombre, precio y reserva (nada clínico).
"""

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

# Claves de negocio que el bot puede decir tal cual (todas deben estar CONFIRMED).
BUSINESS_KEYS = {
    "ADDRESS": ("Dirección", "La dirección de Hola Mujer es: {v}."),
    "MAP_URL": ("Ubicación en el mapa", "Ubicación de Hola Mujer en Google Maps: {v}"),
    "OPENING_HOURS": ("Horario de atención", "Horario de atención de Hola Mujer: {v}."),
}


class Document(BaseModel):
    model_config = ConfigDict(frozen=True)

    doc_id: str
    text: str
    label: str  # cómo se nombra la fuente ante la clienta
    source: str  # procedencia exacta (archivo#id), para auditoría
    kind: Literal["servicio", "promocion", "negocio"]
    sensitive: bool = False


class _Servicio(BaseModel):
    model_config = ConfigDict(extra="ignore")

    service_id: str
    categoria: str
    nombre: str
    descripcion_corta: str | None = None
    precio_pen: float
    reserva_pen: float | None = None
    duracion_min: int | None = None
    duracion_verificada: bool = False
    sesiones_totales: int | None = None
    activo: bool = True
    sensible_clinico: bool = False


class _Promocion(BaseModel):
    model_config = ConfigDict(extra="ignore")

    promo_id: str
    nombre: str
    descripcion: str | None = None
    precio_pen: float
    usable_en_rag: bool = False


class _Dato(BaseModel):
    model_config = ConfigDict(extra="ignore")

    clave: str
    valor: str | float | None = None
    estado: str


def _items(path: Path) -> list[dict[str, object]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items: list[dict[str, object]] = data["items"]
    return items


def _precio(valor: float) -> str:
    return f"S/ {valor:.2f}"


def service_document(s: _Servicio) -> Document:
    partes = [f"{s.nombre} ({s.categoria})."]
    if s.sensible_clinico:
        partes.append("Es un servicio de salud: la orientación la da una especialista.")
    elif s.descripcion_corta:
        partes.append(s.descripcion_corta)
    partes.append(f"Precio: {_precio(s.precio_pen)}.")
    if s.reserva_pen:
        partes.append(f"Reserva para separar la cita: {_precio(s.reserva_pen)}.")
    if s.sesiones_totales and s.sesiones_totales > 1:
        partes.append(f"Paquete de {s.sesiones_totales} sesiones.")
    if s.duracion_verificada and s.duracion_min:
        partes.append(f"Duración: {s.duracion_min} minutos.")
    return Document(
        doc_id=s.service_id,
        text=" ".join(partes),
        label=s.nombre,
        source=f"servicios.json#{s.service_id}",
        kind="servicio",
        sensitive=s.sensible_clinico,
    )


def promo_document(p: _Promocion) -> Document:
    detalle = f" {p.descripcion}" if p.descripcion else ""
    return Document(
        doc_id=f"PROMO-{p.promo_id}",
        text=f"Promoción {p.nombre}.{detalle} Precio: {_precio(p.precio_pen)}.",
        label=f"Promoción {p.nombre}",
        source=f"promociones.json#{p.promo_id}",
        kind="promocion",
    )


def load_documents(data_dir: Path) -> list[Document]:
    docs: list[Document] = []
    for raw in _items(data_dir / "servicios.json"):
        s = _Servicio.model_validate(raw)
        if s.activo:
            docs.append(service_document(s))
    for raw in _items(data_dir / "promociones.json"):
        p = _Promocion.model_validate(raw)
        if p.usable_en_rag:
            docs.append(promo_document(p))
    for raw in _items(data_dir / "negocio.json"):
        d = _Dato.model_validate(raw)
        if d.clave in BUSINESS_KEYS and d.estado == "CONFIRMED" and d.valor:
            label, plantilla = BUSINESS_KEYS[d.clave]
            docs.append(
                Document(
                    doc_id=f"NEG-{d.clave}",
                    text=plantilla.format(v=d.valor),
                    label=label,
                    source=f"negocio.json#{d.clave}",
                    kind="negocio",
                )
            )
    return docs
