# Ruta semanal

El plan completo (16 semanas, 48 sesiones) vive en [`16_week_plan.md`](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/16_week_plan.md); las fuentes por semana, en su tabla «Materiales por semana». Esta página es el **mapa corto** de lo que viene. Los Issues de la semana aparecen solos el domingo por la noche.

## Ahora: Semana 5 — LangGraph core
| Sesión | Issue | Alumno | Tema | Contrato · Guía |
|---|---|---|---|---|
| D1 | [#52](https://github.com/jackthony/ai-business-assistant/issues/52) | Josue | Grafo mínimo con estado explícito (`AgentState`, nodo eco, CLI) | [contrato](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/asignaciones/S05_D1.md) · [guía](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/asignaciones/S05_D1_paso_a_paso.md) |
| D2 | [#53](https://github.com/jackthony/ai-business-assistant/issues/53) | Pilar | Prompt por componentes + LLM tras un puerto + verificación | [contrato](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/asignaciones/S05_D2.md) · [guía](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/asignaciones/S05_D2_paso_a_paso.md) |
| D3 | [#54](https://github.com/jackthony/ai-business-assistant/issues/54) | Allan | Memoria persistente por teléfono (`SqliteSaver`, `thread_id`) | [contrato](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/asignaciones/S05_D3.md) · [guía](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/asignaciones/S05_D3_paso_a_paso.md) |

> ⛔ **#53 y #54 dependen de #52**: usan sus archivos. Hasta que Josue lo mergee en `main`, Pilar y Allan hacen sus lecturas y los estudios guiados. Al mergearse #52, el equipo recibe un aviso automático ([Avisos y dependencias](Avisos-y-dependencias)).

**Lecturas de la semana:** `langgraph.md`, docs de LangGraph, Anthropic «Building Effective Agents», matriz semanal de `definitive-guide.md` → [Fuentes y referencias](Fuentes-y-referencias).

## Después
| Semana | Tema | Fuentes primarias |
|---|---|---|
| S6 | RAG + **HITO 1** (canal provisional + datos sintéticos; el canal real de WhatsApp lo configura el monitor más adelante). Aquí se retoman #3 webhook y #4 envío | `hola-mujer.md`, `agent-engineering-handbook.md` |
| S7 | Tools con Pydantic + Agentes 1 y 2 | `langgraph.md`, `definitive-guide.md` |
| S8 | Cierre de venta + telemetría | `observabilidad-costos.md`, docs Langfuse, `roi_metrics.md` |
| S9–S12 | Safety, HITL/harness (HITO 2), multitenant, NeuraCode, voz, seguridad y evals (HITO 3) | ADR-009, ADR-010, harness engineering |
| S13–S16 | Proactivo, producción (Postgres + Docker), E2E + FinOps, capstone y defensa | Docker, `meta-pricing.md`, `rubric.md` |

## Cola «Pull»
Cuando terminas antes, tomas el siguiente Issue de tu cola, apoyas el PR de un compañero (`apoyo`) o propones algo con la plantilla «Propuesta». Nada de esperar sin hacer nada.
