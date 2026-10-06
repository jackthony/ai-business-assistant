# Syllabus — reglas del programa

## Jornadas

- 3 días oficiales por semana. No hay tareas obligatorias fuera de esos días.
- Regla diaria: **Día 1** comprender/diseñar · **Día 2** construir · **Día 3** verificar/documentar/sustentar.

## Flujo de trabajo (TBD — ver ADR-006)

1. Cada sesión arranca de un **Issue** del backlog (`issues_backlog.md`) con criterios de aceptación.
2. Branch corta `issue-NN-slug` desde `main`, vida de horas o pocos días.
3. Commits pequeños y trazables; PR con tests y evidencia; review del monitor (DeepSeek ayuda como reviewer).
4. Merge a `main` (siempre desplegable). Cerrar Issue con link a commits/PR.

## Reportes SENATI

- Registro diario de actividades y horas reales en el Informe de Formación Práctica (individual).
- Cada dos semanas: tarea más significativa sustentada + informe quincenal.
- El monitor evalúa en el Excel `(EVALUABLE).xlsx` según `05_EVALUATION/rubric.md`.

## Stack

- S1–S3: Java 17 + Maven (exigencia SENATI) + Git/GitHub + JUnit 5.
- S4–S16: Python 3.11+, FastAPI, LangGraph, ChromaDB, Whisper local, visión local, Docker.
- Motor LLM principal: DeepSeek local (Ollama); nube solo para WhatsApp Cloud API.
