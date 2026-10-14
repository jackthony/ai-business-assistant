"""Pseudonimiza las hojas operativas de Hola Mujer (contactos, citas, eventos, muestra inbox).

El repo es público: aquí NO entran nombres, teléfonos, ids de plataforma ni enlaces. Todo lo
demás se conserva tal cual (fechas, etapas, flujos, estados, notas, errores y huecos del Excel)
para que los alumnos trabajen con la forma real de los datos, incluidos sus defectos.

Uso: python tools/datos/pseudonimizar_operativo.py RUTA_AL_EXCEL.xlsx [--out data/hola_mujer/operativo]
Requiere: pip install -e ".[etl]"
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "hola_mujer" / "operativo"
CAPTURA = "2026-10-14"
GUIA = "EJEMPLO_NO_USAR"
SIN_ID = "C-SIN-ID"


def _celda(v: Any) -> Any:
    if isinstance(v, datetime):
        return v.isoformat(timespec="seconds")
    if isinstance(v, float) and v.is_integer():
        return int(v)
    if isinstance(v, str):
        v = v.strip()
    return None if v in ("", None) else v


def _filas(ws: Any) -> list[dict[str, Any]]:
    filas = ws.iter_rows(values_only=True)
    cab = [str(c) for c in next(filas)]
    out = []
    for fila in filas:
        if any(v not in (None, "") for v in fila):
            out.append(
                {k: _celda(v) for k, v in zip(cab, fila, strict=False) if k != "None"}
            )
    return [f for f in out if f.get("contact_id", f.get("sample_id")) != GUIA]


class Alias:
    """id de plataforma -> C001, C002… en orden de aparición (estable para un mismo Excel)."""

    def __init__(self, prefijo: str = "C") -> None:
        self._m: dict[str, str] = {}
        self._p = prefijo

    def __call__(self, valor: Any) -> str:
        if valor is None:
            return SIN_ID
        clave = str(valor)
        return self._m.setdefault(clave, f"{self._p}{len(self._m) + 1:03d}")

    def reemplazar(self, texto: str) -> str:
        for real, alias in self._m.items():
            texto = texto.replace(real, alias)
        return texto


def _limpiar_texto(texto: Any, alias: Alias) -> Any:
    if not isinstance(texto, str):
        return texto
    return re.sub(r"\d{9,}", "[ID]", alias.reemplazar(texto))


def construir(wb: Any) -> dict[str, list[dict[str, Any]]]:
    alias = Alias()
    contactos = [
        {
            "contact_id": alias(f["contact_id"]),
            **{
                k: v
                for k, v in f.items()
                if k not in {"contact_id", "nombre", "telefono_e164"}
            },
            "tiene_nombre": f.get("nombre") is not None,
            "tiene_telefono": f.get("telefono_e164") is not None,
        }
        for f in _filas(wb["01_CONTACTOS"])
    ]
    citas = []
    alias_cita = Alias(
        "A"
    )  # el cita_id de la hoja es un uid de reserva de la plataforma
    for f in _filas(wb["02_CITAS"]):
        f = {
            **f,
            "cita_id": alias_cita(f["cita_id"]) if f.get("cita_id") else None,
            "contact_id": alias(f.get("contact_id")) if f.get("contact_id") else None,
        }
        for col in ("created_at", "updated_at"):
            if isinstance(
                f.get(col), float
            ):  # serial de Excel guardado como número (defecto real)
                f[col] = (
                    datetime(1899, 12, 30, tzinfo=UTC) + timedelta(days=f[col])
                ).isoformat(timespec="seconds")
        citas.append(f)
    eventos = []
    for f in _filas(wb["03_EVENTOS"]):
        f = {
            **f,
            "contact_id": alias(f["contact_id"]),
            "event_id": _limpiar_texto(f["event_id"], alias),
            "cita_id": _limpiar_texto(f.get("cita_id"), alias),
        }
        eventos.append(f)
    # Segunda pasada: alias ya conocidos de todos los contactos en ids derivados.
    for e in eventos:
        e["event_id"] = _limpiar_texto(e["event_id"], alias)
        e["cita_id"] = _limpiar_texto(e["cita_id"], alias)
    muestra = _filas(wb["09_MUESTRA_INBOX_11D"])
    return {
        "contactos": contactos,
        "citas": citas,
        "eventos": eventos,
        "muestra_inbox": muestra,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("excel", type=Path)
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    args = ap.parse_args()
    import openpyxl  # solo el ETL lo necesita; el CI no instala el extra [etl]

    wb = openpyxl.load_workbook(args.excel, data_only=True)
    args.out.mkdir(parents=True, exist_ok=True)
    for nombre, items in construir(wb).items():
        doc = {
            "fuente": "Excel operativo ManyChat (pseudonimizado)",
            "captura": CAPTURA,
            "n": len(items),
            "items": items,
        }
        (args.out / f"{nombre}.json").write_text(
            json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"{nombre}: {len(items)} filas")


if __name__ == "__main__":
    main()
