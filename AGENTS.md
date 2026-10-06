# AGENTS.md — instrucciones para cualquier agente de IA que trabaje en este repo

> Regla de oro: **pocos archivos, contexto mínimo.** Antes de actuar, lee este archivo y como máximo 2–3 archivos de la tarea. Nunca cargues el repo completo.

## Qué es este repo

`ai-business-assistant` — programa de prácticas **HealthTech Software & AI · SENATI 2026** + producto multitenant (Hola Mujer y NeuraCode) para WhatsApp: FastAPI + LangGraph + ChromaDB + Ollama (DeepSeek local). La gestión del programa (currículo, evaluación, ADRs) vive en `program/`; el código del producto en `src/` (desde S4).

## Protocolo de contexto (obligatorio)

1. Lee **siempre primero** `program/00_PROJECT/current_status.md`.
2. Luego solo 2–3 archivos de la tarea (Issue + arquitectura + módulo). Del plan (`program/01_CURRICULUM/16_week_plan.md`), solo el bloque de la semana en curso.
3. Nunca asumas contenido de archivos que no leíste. Si falta contexto, pídelo.
4. Responde en español, salvo código/comentarios en inglés.

## Modos

- **Tutor:** explica con ejemplos pequeños; no des la solución completa de un Issue.
- **Developer:** antes de escribir código, lista los archivos a tocar y propone el plan; espera aprobación.
- **Reviewer:** evalúa PRs contra la sección de revisión de este archivo.

## Reglas duras

- Nada clínico: el bot deriva a humano (safety_agent). Tú tampoco opinas de salud.
- Nunca inventes datos del negocio (precios, horarios, cursos): salen de `program/04_DOMAIN/` o del RAG.
- Nunca uses datos reales de clientes en ejemplos: fixtures anonimizados.
- Respeta los ADRs (`program/03_ARCHITECTURE/decisions/`): no propongas cambiar FastAPI/LangGraph/DeepSeek local sin justificarlo contra un ADR.
- **Regla de evidencia:** cita la fuente (archivo, doc oficial o URL). Un LLM no es autoridad: doc oficial > código reproducible > libro/curso > paper. Si un dato no está en el contexto, dilo; no lo inventes.

## Reglas de código (S4+)

- Python 3.11+, type hints, Pydantic v2 para contratos. Sin secretos en código (`.env` + `.env.example`).
- 1 Issue = 1 branch `(tbd|issue)-N-<slug>` = 1 PR. Commits pequeños en imperativo, referenciando `#NN`. TBD sin excepción (ADR-006): no hay ramas long-lived, `main` siempre desplegable.
- Lo hacen cumplir: `tbd-guardian` (bloquea PR con base≠`main`, rama fuera de `(tbd|issue)-N-<slug>`, sin `Closes #N`, o >6 commits), `tbd-enforcer` (revierte push directo a `main`, cierra PRs >48 h, borra ramas muertas) y el ruleset `main protegido (TBD)` (PR obligatorio, squash/lineal, check requerido `guardian-tbd / reglas-tbd`, push protection activo). Ramas de horas, no de días.
- Antes de pushear (local, obligatorio): `pre-commit install` (ruff + formateo automático en cada commit) y luego las 4 puertas: `ruff check src tests && mypy src --ignore-missing-imports && pytest tests -q && bandit -r src -x tests -ll`. El CI estricto corre las mismas 4 puertas; un push directo a `main` lo revierte `tbd-enforcer`.
- FastAPI async; tools `@tool` con schemas Pydantic estrictos; nodos de grafo = funciones puras; efectos secundarios en services.
- Java (S1–S3, exigencia SENATI): Java 17 + Maven + JUnit 5; mismos estándares de commits y PR.

## Ciclo de informes y progreso (automático — debes conocerlo)

- `digest-semanal` (viernes 17:00 Lima): crea un Issue con los **commits por día**, PRs e Issues abiertos de cada alumno.
- `informe-quincenal` (jueves noche + manual): crea/refresca el **borrador de informe FPE** por alumno (#11–#13) desde su actividad real (commits/PRs/Issues); el alumno completa horas, ATS, resultados y justificación.
- Progreso visible: board público `projects/3` (solo lectura) + expedientes en `program/05_EVALUATION/students/`.
- Si un practicante pregunta cómo empezar, cómo se trabaja con TBD o dónde ve su asignación: remitir a **`GUIA_PRACTICANTE.md`** (raíz).

## Reglas de review (PRs)

Orden: 1) ¿resuelve el Issue y sus criterios de aceptación? 2) ¿respeta arquitectura y ADRs? 3) código (nombres, manejo de errores, duplicación) 4) tests (¿cubren casos borde?) 5) seguridad (sin secretos, validación de entradas) 6) calidad de agente (prompts versionados, sin alucinación estructural).

Formato: `Resumen` (1–3 líneas) + `Hallazgos [BLOCKER]/[MAJOR]/[MINOR]` + `Preguntas de comprensión` + `Recomendación (Aprobar / Cambios menores / Rehacer)`. Directo con el código, respetuoso con la persona; no reescribas el PR, guía con pistas.

## Reglas de evaluación (apoyo al monitor)

- Puedes: redactar borradores de observación por criterio (`program/05_EVALUATION/rubric.md`), detectar patrones (errores recurrentes, PRs sin tests), redactar borradores de feedback semanal (1 logro + 1 mejora + 1 acción concreta) y de informes quincenales.
- **No puedes:** asignar la nota definitiva (la decide el monitor en el Excel) ni inventar evidencia (si falta el link o commit, dilo explícitamente).
