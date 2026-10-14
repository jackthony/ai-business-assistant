# [S## D#] Título de la asignación — contrato determinista

> **Principio:** esta asignación fija el **QUÉ** (entradas, archivos, contrato, pruebas, comandos, criterio de «hecho»). El **CÓMO** — la implementación y las decisiones de diseño — es tuyo: ahí es donde aprendes. Si algo aquí es ambiguo, **no lo adivines**: pregunta en el Issue (sección 12).

## 1. Objetivo
Una sola frase, verificable.

## 2. Antes de empezar (máx. 3 archivos, con minutos)
- `ruta/exacta.md` — qué buscar ahí (N min)

## 3. Entradas (lo que YA existe en el repo)
Lista de rutas existentes (verifícalas con `dir` / `ls` antes de empezar). Lo que falte, lo creas tú y está marcado en la sección 4.

## 4. Archivos que debes crear o modificar (y nada más)
| Ruta exacta | Acción (crear / modificar) | Para qué |
|---|---|---|

## 5. Contrato (no se negocia)
Nombres públicos, campos, firmas y reglas de comportamiento que otras piezas esperan. Solo el contrato, **sin escribir la implementación**.

## 6. Pruebas obligatorias (las escribes PRIMERO, deben fallar antes de implementar)
| ID | Qué verifica | Entrada | Salida esperada |
|---|---|---|---|
| T1 | | | |

## 7. Pasos en orden
1. `git checkout main` y `git pull` → salida esperada: `Already up to date` o los commits nuevos.
2. `git checkout -b issue-N-slug`
3. Escribir las pruebas T1..Tn → `pytest tests -q` debe mostrar **rojo** por la razón correcta.
4. Implementar lo mínimo hasta ponerlas en verde.
5. Las 4 puertas: `ruff check src tests && mypy src --ignore-missing-imports && pytest tests -q && bandit -r src -x tests -ll` → todas en verde.
6. Commits chicos con convención `tipo(alcance): verbo imperativo` (≤72 caracteres, sin punto final).
7. PR con `Closes #N` y la plantilla completa (incluye las preguntas de comprensión).

## 8. Hecho cuando (checklist verificable)
- [ ] criterio medible 1
- [ ] CI en verde (`guardian-tbd / reglas-tbd` y `CI estricto / calidad`)

## 9. No hagas
Límites explícitos (p. ej. sin servicios reales en pruebas, sin adelantarte a la semana siguiente, sin datos reales).

## 10. Presupuesto de IA
Qué sí le pides a tu asistente (tareas pequeñas y verificables), qué no, y el tope de ~10–15 interacciones por sesión. Tú ejecutas, verificas y firmas.

## 11. Preguntas de comprensión (las respondes en el PR, con tus palabras)
1. Pregunta.
   **Tu respuesta debe mencionar:** (a) … (b) … (c) …
2. …
3. …

## 12. Si te trabas (en este orden)
1. Relee la sección 2 y el ejemplo guiado indicado.
2. Corre el ejemplo guiado y compara con tu código.
3. Comenta en el Issue: qué intentaste y el error **pegado como texto** (no captura borrosa).
4. Pide ayuda a un compañero (Josue es mentor interno) o al monitor.
