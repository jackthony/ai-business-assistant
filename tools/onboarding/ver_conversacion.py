r"""Muestra una conversación del corpus sintético de forma legible.

Uso (Windows):  py -3.11 tools\onboarding\ver_conversacion.py conv_0001
Sin argumento lista los ids disponibles. Solo librería estándar.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

DATA = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "conversaciones"
    / "sinteticas_v1.jsonl"
)


def load_rows(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # consolas Windows
    if not DATA.exists():
        print(f"No encuentro {DATA}. Haz 'git pull' en main y vuelve a intentar.")
        return 1
    rows = load_rows(DATA)
    ids = sorted({r["conversacion_id"] for r in rows})
    if len(argv) < 2:
        print("Conversaciones disponibles:", ", ".join(ids))
        return 0
    wanted = argv[1]
    turns = [r for r in rows if r["conversacion_id"] == wanted]
    if not turns:
        print(f"No existe {wanted}. Disponibles: {', '.join(ids)}")
        return 1
    print(
        f"{wanted} · canal {turns[0]['canal']} · {len(turns)} turnos · origen {turns[0]['origen']}"
    )
    print("-" * 60)
    for r in turns:
        text = r["texto"]
        lines = len(text.splitlines()) or 1
        meta = ""
        if r["rol"] == "assistant":
            meta = f"  ({lines} líneas · {text.count('?')} preguntas)"
        print(f"[{r['turno']:02d}] {r['emisor']:<12} {r['ts']}{meta}")
        for ln in text.splitlines() or [""]:
            print(f"      {ln}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
