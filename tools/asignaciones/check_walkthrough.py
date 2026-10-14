#!/usr/bin/env python3
"""Check a step-by-step walkthrough against its contract. Usage: check_walkthrough.py SPEC.md WALKTHROUGH.md
Prints JSON {"ok": bool, "errors": [str]}."""

import json
import re
import sys

spec = open(sys.argv[1], encoding="utf-8").read()
walk = open(sys.argv[2], encoding="utf-8").read()
errs: list[str] = []

m = re.search(r"^## 6\..*?(?=^## 7\.)", spec, re.S | re.M)
ids = re.findall(r"^\|\s*([A-Z]\d+)\s*\|", m.group(0), re.M) if m else []
if not ids:
    errs.append("no se pudieron leer los IDs de pruebas de la sección 6 del contrato")
for i in ids:
    if not re.search(r"\b" + i + r"\b", walk):
        errs.append(f"la prueba {i} del contrato no aparece en el paso a paso")

for h in [
    "Mapa de la sesión",
    "Mini-conceptos",
    "Calentamiento",
    "Escalera de pistas",
    "Errores típicos",
    "Autoevaluación",
    "Prompts sugeridos",
]:
    if h not in walk:
        errs.append(f"falta la sección «{h}»")

steps = re.findall(r"^### Paso \d+", walk, re.M)
if len(steps) < 6:
    errs.append(f"pocos pasos ({len(steps)}); se esperan al menos 6")
for label in [
    "**Haz esto:**",
    "**Por qué:**",
    "**Debes ver:**",
    "**Si falla:**",
    "**Punto de control:**",
]:
    if walk.count(label) < len(steps):
        errs.append(
            f"el campo {label} aparece {walk.count(label)} veces y hay {len(steps)} pasos"
        )

for blk in re.finditer(r"```(\w*)\n(.*?)```", walk, re.S):
    lang, body = blk.group(1), blk.group(2)
    lines = [ln for ln in body.splitlines() if ln.strip()]
    if lang == "python" and len(lines) > 3:
        errs.append("bloque python de más de 3 líneas (posible solución regalada)")
    if (
        lang == "python"
        and re.search(r"^\s*def .+:\s*$", body, re.M)
        and len(lines) > 1
    ):
        errs.append(
            "bloque python con una función definida (posible solución regalada)"
        )

if len(walk.splitlines()) > 420:
    errs.append("demasiado largo (>420 líneas): condensa")

print(json.dumps({"ok": not errs, "errors": errs}, ensure_ascii=False))
