# Cómo trabajamos

## El flujo (TBD de aprendizaje)
**1 Issue = 1 rama `issue-N-<slug>` = 1 PR.** Commits `tipo(alcance): verbo imperativo` (≤72 caracteres, referenciando `#N`), `Closes #N` en el PR. No hay ramas largas: `main` siempre desplegable. Detalle y porqués: [`AGENTS.md`](https://github.com/jackthony/ai-business-assistant/blob/main/AGENTS.md) y [ADR-006](https://github.com/jackthony/ai-business-assistant/blob/main/program/03_ARCHITECTURE/decisions/).

## Tu asignación
- **Contrato** `S##_D#.md`: el QUÉ (archivos, pruebas, «No hagas», preguntas de comprensión). **Paso a paso** `S##_D#_paso_a_paso.md`: el CÓMO sin spoilers (mini-conceptos, un paso por prueba, escalera de pistas). Índice: [asignaciones/README](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/asignaciones/README.md).
- **Las pruebas se escriben antes** y se ven fallar por la razón correcta.
- **Presupuesto de IA:** tu asistente explica, pregunta y revisa; **no escribe el código del contrato**.

## Revisión automática de tu avance
Al hacer `git push` de tu rama, el robot abre un **PR en borrador** y deja **un comentario «🧭 Revisión guiada»** que se actualiza en cada push: archivos del contrato trabajados y faltantes, desvíos y siguiente paso (con pistas, sin solución). Haz push **al terminar cada paso en verde**. Cuando acabes: *Ready for review*.

## Las 4 puertas antes de pushear
`ruff check src tests && mypy src --ignore-missing-imports && pytest tests -q && bandit -r src -x tests -ll`. El CI estricto corre las mismas.

## Puerta de comprensión
Antes del PR respondes con tus palabras las preguntas de la sección 11 de tu contrato. Si no puedes, vuelves a la lectura. Ensáyalas con `/comprension` y compártelas en [Discusiones](Discusiones).

## Estándares de ingeniería
Puertos y adaptadores, código limpio, seguridad por diseño: [`estandares.md`](https://github.com/jackthony/ai-business-assistant/blob/main/program/03_ARCHITECTURE/estandares.md). Decisiones tomadas: [ADRs](https://github.com/jackthony/ai-business-assistant/blob/main/program/03_ARCHITECTURE/decisions/) (no se cambian FastAPI/LangGraph/DeepSeek local sin justificarlo contra un ADR).
