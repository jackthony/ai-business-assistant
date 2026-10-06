# Plan 16 semanas (baseline v1 — pendiente de re-secuencia v2)

> **Estado:** v1 congelada el 2026-10-06. El detalle diario vive en el Excel, hoja `PLAN_16_SEMANAS`. Al aprobar la v2, este archivo se vuelve canónico con las 48 sesiones completas y el Excel queda solo para evaluación.

| Semana | Foco | Issues | Hito |
|---|---|---|---|
| 1 | Java + POO HealthTech (modelado → implementación → sustentación) | — | — |
| 2 | Git/GitHub profesional + JUnit 5 + PR + cierre quincenal | — | — |
| 3 | HTTP/JSON/REST, contratos de integración y mapa Build/Buy/Integrate | — | — |
| 4 | FastAPI (Integration Hub): setup, webhook Meta GET/POST, envío saliente | #01–#03 | — |
| 5 | LangGraph Core: StateGraph, system prompt Hola Mujer, memoria SqliteSaver | #04–#06 | — |
| 6 | Reglas conversacionales/few-shot, ingesta Excel + RAG ChromaDB | #07–#09 | **HITO 1** (D3) |
| 7 | Agente 1 Info+RAG, Pydantic tools, Agente 2 Citas | #10–#12 | — |
| 8 | Agente 3 Cierre/lead, registro en Sheets/DB, OCR de pagos (Yape/Plin) | #13–#15 | — |
| 9 | Agente 4 Safety/triage, Human-in-the-Loop (interrupt) | #16–#18 | **HITO 2** (D3) |
| 10 | Supervisor router, multitenant base, ingesta cursos NeuraCode | #19–#21 | — |
| 11 | Whisper local (voz), normalización de audio, Multimodal NeuraCode | #22–#24 | **HITO 3** (D3) |
| 12 | Telemetría, seguridad OWASP/guardrails, evaluaciones LLM-as-a-Judge | #25–#27 | — |
| 13 | Re-engagement proactivo + seguimiento personalizado + analytics | #28–#30 | — |
| 14 | PostgresSaver, Docker, deploy (webhook 24/7) | #31–#33 | — |
| 15 | Integración E2E, estrés/fallbacks, refactor + documentación | #34–#36 | — |
| 16 | Capstone: pruebas E2E, defensa técnica, demo final y transferencia | #37–#39 | **Demo final** |

## Temas de la re-secuencia v2 (propuesta pendiente de aprobación)

- Mover OCR de pagos (S8) y NeuraCode (S10) más tarde; consolidar agente único antes de multiagente.
- Adelantar observabilidad/evaluación (S12 → antes) y seguridad.
- Reemplazar dependencias cloud en el plan: Whisper API → faster-whisper; GPT-4o Vision → Qwen2.5-VL; fallback OpenAI/Anthropic → modelos locales.
