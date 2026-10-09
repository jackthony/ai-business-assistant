# AGENTS.md — instrucciones para cualquier agente de IA que trabaje en este repo

> Regla de oro: **pocos archivos, contexto mínimo.** Antes de actuar, lee este archivo y como máximo 2–3 archivos de la tarea. Nunca cargues el repo completo.

## Qué es este repo

`ai-business-assistant` — programa de prácticas **HealthTech Software & AI · SENATI 2026** + producto multitenant (Hola Mujer y NeuraCode) para WhatsApp: FastAPI + LangGraph + ChromaDB + Ollama (DeepSeek local). La gestión del programa (currículo, evaluación, ADRs) vive en `program/`; el código del producto en `src/` (desde S4). El runtime (Ollama con modelos grandes) corre en la **M5 del monitor**; los practicantes desarrollan en **PCs Windows antiguas** (modelos chicos o DeepSeek web para dudas — `program/02_REFERENCE/deepseek-local.md`). Al darles instrucciones usa comandos Windows (`.venv\Scripts\activate`, `copy`, `py -3.11`).

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
- 1 Issue = 1 branch `(tbd|issue)-N-<slug>` = 1 PR. Commits en convención estricta (`tipo(alcance): verbo imperativo`, ≤72 chars, 1 cambio por commit, sin punto final; tipos: feat|fix|docs|test|refactor|ci|chore|perf|style — la valida `tbd-guardian`); referenciando `#NN`. TBD sin excepción (ADR-006): no hay ramas long-lived, `main` siempre desplegable.
- **Pull, no solo push:** el que termina antes jala el siguiente Issue del backlog (sin dueño), apoya PRs de compañeros (`apoyo`) o propone algo nuevo con la plantilla "Propuesta" (`propuesta`). Cualquier Issue sin `Alumno`/assignee está disponible; el board se sincroniza solo (`issue-on-create.yml`). **Los Issues asignados a otro compañero no se tocan**: solo con permiso del monitor o proactividad justificada (impacto mal medido/bloqueo) explicada en el Issue/PR. Las propuestas las triagea el monitor: aceptar → backlog/semana + desglose de criterios; rechazar → cerrar con motivo claro.
- Lo hacen cumplir: `tbd-guardian` (bloquea PR con base≠`main`, rama fuera de `(tbd|issue)-N-<slug>`, sin `Closes #N`; >6 commits solo avisa), `tbd-enforcer` (revierte push directo a `main`, cierra PRs >7 días, borra ramas muertas) y el ruleset `main protegido (TBD)` (PR obligatorio, squash/lineal, checks requeridos `guardian-tbd / reglas-tbd` y `CI estricto / calidad`, push protection activo). TBD de aprendizaje (ADR-006 revisado): reglas duras mínimas, el resto son guías.
- Antes de pushear (local, obligatorio): `pre-commit install` (ruff + formateo automático en cada commit) y luego las 4 puertas: `ruff check src tests && mypy src --ignore-missing-imports && pytest tests -q && bandit -r src -x tests -ll`. El CI estricto corre las mismas 4 puertas; un push directo a `main` lo revierte `tbd-enforcer`.
- FastAPI async; tools `@tool` con schemas Pydantic estrictos; nodos de grafo = funciones puras; efectos secundarios en services.
- Java (S1–S3, exigencia SENATI): Java 17 + Maven + JUnit 5; mismos estándares de commits y PR.

## Ciclo de informes y progreso (automático — debes conocerlo)

- `crear-issues-semana` (domingo 21:00 Lima + manual): crea los Issues de la semana (título `[S## D#]`) con lecturas + detalle de la sesión; idempotente por título.
- `digest-semanal` (viernes 17:00 Lima): crea un Issue con los **commits por día**, PRs e Issues abiertos de cada alumno.
- `coach` (lun–sáb): avisos que @mencionan al practicante en sus días de práctica (arranque 08:00, pulso 14:00 solo si no hay actividad, cierre 17:30 Lima) y al recibir revisión, asignación o merge; siempre dicen dónde mirar. Config y roster en `.github/coach.json`; lógica en `.github/scripts/coach.py`.
- `board-sync` (eventos + nightly): sincroniza el board con labels/assignees/PRs (`.github/scripts/board_sync.py`); **tras crear o mover Issues/PRs, sincroniza el board** (`board_sync.py --all`) y revisa que se vea bien.
- `informe-quincenal` (cada noche dom–vie 21:00 Lima + manual): crea/refresca el **borrador de informe FPE** por alumno (#11–#13) desde su actividad real (commits/PRs/Issues); el alumno completa horas, ATS, resultados y justificación.
- Progreso visible: board público `projects/3` (solo lectura) + expedientes en `program/05_EVALUATION/students/`.
- **Cierre de Issues:** solo con PR mergeado (`Closes #N`) o justificación escrita; si un practicante cierra sin eso, `issue-closed` lo reabre y comenta. El monitor cierra directo cuando corresponda.
- **Material para practicantes y sus asistentes (OpenCode con modelos gratis):** contexto mínimo por fase en `program/01_CURRICULUM/pack_contexto.md` (incluye el protocolo de uso controlado de IA: ~10–15 interacciones por sesión, adjuntar solo lo puntual), definiciones ya tomadas en `program/02_REFERENCE/stack-versiones.md` (Python 3.11, límites de las herramientas gratis) y **estándares de ingeniería** en `program/03_ARCHITECTURE/estandares.md` (stack con porqué, puertos y adaptadores, código limpio adaptado, seguridad por diseño, fuentes canónicas: 12-Factor Agents, Anthropic, Cosmic Python, OWASP). Carga solo lo que el pack indique — nunca el repo completo.
- Si un practicante pregunta cómo empezar, cómo se trabaja con TBD o dónde ve su asignación: remitir a **`GUIA_PRACTICANTE.md`** (raíz). Si actúas como **asistente de un practicante**, carga además **`GUIA_AGENTE.md`** (raíz): qué enseñar y hacer cumplir, catálogo de literatura, puerta de comprensión y prohibiciones.

## Reglas de review (PRs)

Orden: 1) ¿resuelve el Issue y sus criterios de aceptación? 2) ¿respeta arquitectura y ADRs? 3) código (nombres, manejo de errores, duplicación) 4) tests (¿cubren casos borde?) 5) seguridad (sin secretos, validación de entradas) 6) calidad de agente (prompts versionados, sin alucinación estructural).

Formato: `Resumen` (1–3 líneas) + `Hallazgos [BLOCKER]/[MAJOR]/[MINOR]` + `Preguntas de comprensión` + `Recomendación (Aprobar / Cambios menores / Rehacer)`. Directo con el código, respetuoso con la persona; no reescribas el PR, guía con pistas.

## Reglas de evaluación (apoyo al monitor)

- Puedes: redactar borradores de observación por criterio (`program/05_EVALUATION/rubric.md`), detectar patrones (errores recurrentes, PRs sin tests), redactar borradores de feedback semanal (1 logro + 1 mejora + 1 acción concreta) y de informes quincenales.
- **No puedes:** asignar la nota definitiva (la decide el monitor en el Excel) ni inventar evidencia (si falta el link o commit, dilo explícitamente).
