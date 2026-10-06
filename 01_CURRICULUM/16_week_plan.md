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

## Plan v2 (propuesta 2026-10-06 — en revisión)

Cambios clave vs v1: CI/CD desde S4 D1; telemetría temprana (#25 → S8); OCR de pagos (#15 → S10) recién después del agente único; supervisor (#19) y multitenant (#20) en S10; NeuraCode (#21 → S11); HITO 3 (#24 → S12); seguridad + evals/Lusser en S12; FinOps en S15.

| Semana | Foco | Issues |
|---|---|---|
| 4 | Repo único + FastAPI + CI + webhook + sender + métricas base | #01–#03 |
| 5 | LangGraph core + system prompt + SqliteSaver | #04–#06 |
| 6 | Reglas/few-shot + RAG + **HITO 1** | #07–#09 |
| 7 | Pydantic tools + citas | #10–#12 |
| 8 | Cierre/lead + registro + telemetría temprana | #13, #14, #25 |
| 9 | Safety + HITL/harness + **HITO 2: agente único completo** | #16–#18 |
| 10 | OCR pagos + supervisor router + multitenant (clase de frameworks) | #15, #19, #20 |
| 11 | Ingesta NeuraCode + Whisper local + normalización de audio | #21–#23 |
| 12 | **HITO 3** + OWASP/inyección + evals (LLM-as-a-Judge + Lusser) | #24, #26, #27 |
| 13 | Proactivo + follow-ups + analytics | #28–#30 |
| 14 | PostgresSaver + Docker + deploy | #31–#33 |
| 15 | E2E + fallbacks locales + FinOps/costos + refactor/docs | #34–#36 |
| 16 | Capstone + defensa + demo final | #37–#39 |

S1–S3 se mantienen (Java/Git/HTTP). El detalle sesión por sesión se publica por bloques: **S1–S4 primero**, luego S5–S8, S9–S12 y S13–S16.
