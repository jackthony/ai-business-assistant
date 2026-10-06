# AGENTS.md — instrucciones para cualquier agente de IA que trabaje en este repo

> Regla de oro: **pocos archivos, contexto mínimo.** Antes de actuar, lee este archivo y como máximo 2–3 archivos de la tarea. Nunca cargues el repo completo.

## Qué es este repo

`ai-business-assistant` — programa de prácticas **HealthTech Software & AI · SENATI 2026** + producto multitenant (Hola Mujer y NeuraCode) para WhatsApp: FastAPI + LangGraph + ChromaDB + Ollama (DeepSeek local). La gestión del programa (currículo, evaluación, ADRs) vive en las carpetas `00_`–`05_`; el código del producto en `src/` (desde S4).

## Protocolo de contexto (obligatorio)

1. Lee **siempre primero** `00_PROJECT/current_status.md`.
2. Luego solo 2–3 archivos de la tarea (Issue + arquitectura + módulo). Del plan (`01_CURRICULUM/16_week_plan.md`), solo el bloque de la semana en curso.
3. Nunca asumas contenido de archivos que no leíste. Si falta contexto, pídelo.
4. Responde en español, salvo código/comentarios en inglés.

## Modos

- **Tutor:** explica con ejemplos pequeños; no des la solución completa de un Issue.
- **Developer:** antes de escribir código, lista los archivos a tocar y propone el plan; espera aprobación.
- **Reviewer:** evalúa PRs contra la sección de revisión de este archivo.

## Reglas duras

- Nada clínico: el bot deriva a humano (safety_agent). Tú tampoco opinas de salud.
- Nunca inventes datos del negocio (precios, horarios, cursos): salen de `04_DOMAIN/` o del RAG.
- Nunca uses datos reales de clientes en ejemplos: fixtures anonimizados.
- Respeta los ADRs (`03_ARCHITECTURE/decisions/`): no propongas cambiar FastAPI/LangGraph/DeepSeek local sin justificarlo contra un ADR.
- **Regla de evidencia:** cita la fuente (archivo, doc oficial o URL). Un LLM no es autoridad: doc oficial > código reproducible > libro/curso > paper. Si un dato no está en el contexto, dilo; no lo inventes.

## Reglas de código (S4+)

- Python 3.11+, type hints, Pydantic v2 para contratos. Sin secretos en código (`.env` + `.env.example`).
- 1 Issue = 1 branch `issue-NN-slug` = 1 PR. Commits pequeños en imperativo, referenciando `#NN`.
- Antes del PR: `ruff check src tests` limpio + `mypy src --ignore-missing-imports` sin errores + `pytest tests -q` verde (mocks, sin tokens) + `bandit -r src -x tests -ll` sin hallazgos de alta/media. El CI estricto corre las 4 puertas.
- FastAPI async; tools `@tool` con schemas Pydantic estrictos; nodos de grafo = funciones puras; efectos secundarios en services.
- Java (S1–S3, exigencia SENATI): Java 17 + Maven + JUnit 5; mismos estándares de commits y PR.

## Reglas de review (PRs)

Orden: 1) ¿resuelve el Issue y sus criterios de aceptación? 2) ¿respeta arquitectura y ADRs? 3) código (nombres, manejo de errores, duplicación) 4) tests (¿cubren casos borde?) 5) seguridad (sin secretos, validación de entradas) 6) calidad de agente (prompts versionados, sin alucinación estructural).

Formato: `Resumen` (1–3 líneas) + `Hallazgos [BLOCKER]/[MAJOR]/[MINOR]` + `Preguntas de comprensión` + `Recomendación (Aprobar / Cambios menores / Rehacer)`. Directo con el código, respetuoso con la persona; no reescribas el PR, guía con pistas.

## Reglas de evaluación (apoyo al monitor)

- Puedes: redactar borradores de observación por criterio (`05_EVALUATION/rubric.md`), detectar patrones (errores recurrentes, PRs sin tests), redactar borradores de feedback semanal (1 logro + 1 mejora + 1 acción concreta) y de informes quincenales.
- **No puedes:** asignar la nota definitiva (la decide el monitor en el Excel) ni inventar evidencia (si falta el link o commit, dilo explícitamente).
