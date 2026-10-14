"""Normaliza a JSON los datos del negocio Hola Mujer que viven en el Excel operativo.

Entra: 05_SERVICIOS, 06_PROMOCIONES, 04_CONFIG y los vocabularios (validaciones de lista).
No entra nada que contenga personas: contactos, citas, eventos, muestra del inbox, la hoja
oculta ni 00_EMPEZAR. El Excel no está en el repo; se pasa por argumento.

Uso: python tools/datos/normalizar_hola_mujer.py RUTA_AL_EXCEL.xlsx [--out data/hola_mujer]
Requiere: pip install -e ".[etl]"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "hola_mujer"
ARCHIVO = "Hola Mujer · MVP WhatsApp ManyChat · Operativo.xlsx"
CAPTURA = "2026-10-14"

# Categorías donde el bot no debe opinar: deriva a la obstetra (heurística; confirmar con Jioysi).
CATEGORIAS_SENSIBLES = {
    "Obstetricia y embarazo",
    "Planificación familiar",
    "Prevención y tamizaje",
    "Prevención y salud femenina",
    "Salud íntima y ginecológica",
}

# Valores confirmados por el monitor que el Excel aún marca PENDING.
CONFIRMADOS = {
    "ADDRESS": (
        "Urb. Nicolás Garatea, Nuevo Chimbote, en el local de Oral Imagen, segundo piso",
        "Referencia en Google Maps: Av. Agraria G-9 (dirección de Oral Imagen).",
    ),
    "MAP_URL": (
        "https://maps.app.goo.gl/hFWGtDwK8dhwxQHE7",
        "Enlace entregado por el monitor.",
    ),
    "OPENING_HOURS": (
        (
            "Todos los días 15:00-19:00 (America/Lima); mañanas sin atención; domingo y toda cita, "
            "previa coordinación"
        ),
        "No hay una persona fija en el consultorio.",
    ),
}
FUENTE_CONFIRMADOS = "monitor, 2026-10-14"


class Servicio(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_id: str = Field(pattern=r"^HM-[A-Z]+-\d{3}$")
    linea: str
    categoria: str
    categoria_slug: str
    nombre: str = Field(min_length=3)
    descripcion_corta: str = Field(min_length=10)
    precio_pen: float = Field(gt=0)
    reserva_pen: float = Field(ge=0)
    duracion_min: int = Field(gt=0)
    duracion_verificada: bool
    permite_sesiones: bool
    sesiones_totales: int | None = Field(default=None, ge=1)
    espacio_entre_sesiones: int | None = Field(default=None, ge=1)
    activo: bool
    requiere_evaluacion: bool
    cta: str | None
    categoria_manychat: str | None
    sensible_clinico: bool

    @model_validator(mode="after")
    def _coherente(self) -> Servicio:
        if self.reserva_pen > self.precio_pen:
            raise ValueError(f"{self.service_id}: la reserva supera el precio")
        if not self.permite_sesiones and self.sesiones_totales not in (None, 1):
            raise ValueError(f"{self.service_id}: sesiones sin permite_sesiones")
        return self


class Promocion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    promo_id: str
    nombre: str
    descripcion: str
    precio_pen: float = Field(gt=0)
    duracion_min: int = Field(gt=0)
    sesiones_totales: int = Field(ge=1)
    reserva_pen: float = Field(ge=0)
    fecha_inicio_raw: str
    fecha_fin_raw: str
    fechas_ambiguas: bool
    activo: bool
    usable_en_rag: bool

    @model_validator(mode="after")
    def _inactiva_no_se_usa(self) -> Promocion:
        if self.usable_en_rag and (not self.activo or self.fechas_ambiguas):
            raise ValueError(
                f"{self.promo_id}: promoción inactiva o con fechas ambiguas"
            )
        return self


class Hecho(BaseModel):
    model_config = ConfigDict(extra="forbid")

    clave: str
    valor: str | None
    estado: str
    responsable: str
    nota: str | None
    fuente: str


def _slug(texto: str) -> str:
    base = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")


def _si(v: object) -> bool:
    return str(v).strip().upper() == "YES"


def _txt(v: object) -> str | None:
    t = re.sub(r"\s+", " ", str(v)).strip() if v not in (None, "") else ""
    return t or None


def _int(v: object) -> int | None:
    return None if v in (None, "") else int(float(str(v)))


def _tabla(ws: Any) -> list[dict[str, Any]]:
    filas = [
        r for r in ws.iter_rows(values_only=True) if any(c not in (None, "") for c in r)
    ]
    cab = [str(c) if c is not None else f"_{i}" for i, c in enumerate(filas[0])]
    return [dict(zip(cab, r, strict=False)) for r in filas[1:]]


def servicios(ws: Any) -> list[Servicio]:
    filas = _tabla(ws)
    duraciones = {int(float(f["duracion_min"])) for f in filas}
    uniforme = (
        len(duraciones) == 1
    )  # todas iguales: parece un valor por defecto, sin verificar
    salida = []
    for f in filas:
        cat = str(_txt(f["categoria_servicio"]))
        prefijo = str(f["service_id"]).split("-")[1]
        salida.append(
            Servicio(
                service_id=str(f["service_id"]).strip(),
                linea=prefijo,
                categoria=cat,
                categoria_slug=_slug(cat),
                nombre=str(_txt(f["nombre"])),
                descripcion_corta=str(_txt(f["descripcion_corta"])),
                precio_pen=round(float(f["precio_pen"]), 2),
                reserva_pen=round(float(f["reserva_pen"]), 2),
                duracion_min=int(float(f["duracion_min"])),
                duracion_verificada=not uniforme,
                permite_sesiones=_si(f["permite_sesiones"]),
                sesiones_totales=_int(f["sesiones_totales"]),
                espacio_entre_sesiones=_int(f["espacio_entre_sesiones"]),
                activo=_si(f["activo"]),
                requiere_evaluacion=_si(f["requiere_evaluacion"]),
                cta=_txt(f["cta"]),
                categoria_manychat=_txt(f["categoria"]),
                sensible_clinico=cat in CATEGORIAS_SENSIBLES,
            )
        )
    ids = [s.service_id for s in salida]
    if len(set(ids)) != len(ids):
        raise ValueError("service_id repetidos en 05_SERVICIOS")
    return sorted(salida, key=lambda s: s.service_id)


def _fecha_raw(v: object) -> str:
    return v.strftime("%Y-%m-%d") if isinstance(v, datetime) else str(v).strip()


def promociones(ws: Any) -> list[Promocion]:
    """Solo el primer bloque (hasta el primer encabezado repetido); el resto es un catálogo viejo."""
    salida = []
    for f in _tabla(ws):
        if f["promo_id"] == "service_id":
            break
        if not f["promo_id"] or f["categoria"] != "PROMOCION":
            continue
        activo = _si(f["activo"])
        # Excel convirtió textos dd/mm a fecha mm/dd en unos y los dejó como texto en otros.
        ambiguas = isinstance(f["fecha_incio"], datetime) or isinstance(
            f["fecha_fin"], datetime
        )
        salida.append(
            Promocion(
                promo_id=str(f["promo_id"]).strip(),
                nombre=str(_txt(f["promo_nombre"])),
                descripcion=str(_txt(f["promo_descripcion"])),
                precio_pen=round(float(f["promo_precio"]), 2),
                duracion_min=int(float(f["promo_duracion_min"])),
                sesiones_totales=int(float(f["sesiones_totales"])),
                reserva_pen=round(float(f["reserva_pen"]), 2),
                fecha_inicio_raw=_fecha_raw(f["fecha_incio"]),
                fecha_fin_raw=_fecha_raw(f["fecha_fin"]),
                fechas_ambiguas=ambiguas,
                activo=activo,
                usable_en_rag=False,
            )
        )
    return salida


def negocio(ws: Any) -> list[Hecho]:
    salida = []
    for f in _tabla(ws):
        clave = str(f["config_key"]).strip()
        valor, estado, nota = (
            _txt(f["value"]),
            str(f["status"]).strip(),
            _txt(f["notes"]),
        )
        fuente = f"04_CONFIG ({CAPTURA})"
        if clave in CONFIRMADOS:
            valor, extra = CONFIRMADOS[clave]
            estado, fuente = "CONFIRMED", FUENTE_CONFIRMADOS
            nota = extra
        salida.append(
            Hecho(
                clave=clave,
                valor=None
                if valor in ("POR_CONFIRMAR", "PENDIENTE_APROBACION")
                else valor,
                estado=estado,
                responsable=str(f["owner"]).strip(),
                nota=nota,
                fuente=fuente,
            )
        )
    return salida


def vocabularios(wb: Any) -> dict[str, object]:
    """Listas permitidas (validaciones del Excel) + valores observados fuera de lista."""

    def lista(hoja: str, rango_ini: str) -> list[str]:
        for d in wb[hoja].data_validations.dataValidation:
            if str(d.sqref).startswith(rango_ini):
                return [x.strip() for x in str(d.formula1).strip('"').split(",")]
        raise KeyError(f"{hoja} {rango_ini}")

    return {
        "etapas_contacto": lista("01_CONTACTOS", "J2"),
        "tipo_cliente": lista("01_CONTACTOS", "G2"),
        "intenciones": lista("01_CONTACTOS", "H2"),
        "canales": lista("01_CONTACTOS", "F2"),
        "estados_cita": lista("02_CITAS", "J11"),
        "estados_recordatorio": lista("02_CITAS", "L11"),
        "estados_sync": lista("02_CITAS", "P11"),
        "tipos_evento": lista("03_EVENTOS", "F2"),
        "resultados_evento": lista("03_EVENTOS", "H2"),
        "cta": lista("05_SERVICIOS", "N2"),
        "estados_config": lista("04_CONFIG", "C2"),
        "observados_fuera_de_lista": {
            "tipos_evento": ["CANCELLED_MISMATCH"],
            "estados_cita": ["CANCELADO"],
            "canales": ["Whatsapp"],
            "service_id_sin_catalogo": ["GLUTEOS"],
        },
    }


def _envolver(items: list[BaseModel], hoja: str, nota: str) -> dict[str, object]:
    return {
        "meta": {"fuente": f"{ARCHIVO}, hoja {hoja}", "captura": CAPTURA, "nota": nota},
        "items": [i.model_dump() for i in items],
    }


def _escribir(ruta: Path, datos: object) -> None:
    ruta.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("excel", type=Path)
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    a = ap.parse_args()
    try:
        import openpyxl
    except ImportError:
        sys.exit('Falta openpyxl: pip install -e ".[etl]"')
    wb = openpyxl.load_workbook(a.excel, data_only=True)
    a.out.mkdir(parents=True, exist_ok=True)
    srv = servicios(wb["05_SERVICIOS"])
    pro = promociones(wb["06_PROMOCIONES"])
    neg = negocio(wb["04_CONFIG"])
    _escribir(
        a.out / "servicios.json",
        _envolver(
            list(srv),
            "05_SERVICIOS",
            "duracion_verificada=false: todas las duraciones son 60 min, parece un valor por defecto. "
            "espacio_entre_sesiones: unidad sin confirmar (probable días).",
        ),
    )
    _escribir(
        a.out / "promociones.json",
        _envolver(
            list(pro),
            "06_PROMOCIONES",
            "Las 3 están activo=NO y con fechas ambiguas: no se usan en el RAG hasta que el negocio confirme.",
        ),
    )
    _escribir(
        a.out / "negocio.json",
        _envolver(
            list(neg),
            "04_CONFIG",
            "ADDRESS, MAP_URL y OPENING_HOURS confirmados por el monitor.",
        ),
    )
    _escribir(a.out / "vocabularios.json", vocabularios(wb))
    print(f"{len(srv)} servicios, {len(pro)} promociones, {len(neg)} datos de negocio")


if __name__ == "__main__":
    main()
