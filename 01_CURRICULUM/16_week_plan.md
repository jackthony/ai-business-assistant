# Plan 16 semanas — canónico (v2, en revisión)

> **Estado:** v2 propuesta (2026-10-06). Este archivo es la fuente canónica del plan; el Excel queda solo para evaluación. El detalle de sesiones se publica por bloques: **Bloque 1 (S1–S4) abajo**; S5–S16 en siguientes entregas. La tabla v1 se conserva solo como histórico.

### Histórico v1 (referencia)

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

---

## Detalle de sesiones — Bloque 1 (S1–S4)

### Semana 1 — Java + POO HealthTech (práctica individual, sin Issues)

**D1 — Comprender y modelar**
- Objetivo: entender el reto antes de programar; modelar el dominio Hola Mujer (versión simplificada y anonimizada).
- Actividades: Discovery del caso; identificar clases, atributos, métodos y reglas; esquema de clases (UML simple o papel); crear proyecto Java 17 + Maven que compile.
- Entregable: esquema de clases + proyecto que compila.
- Criterios: [ ] ≥5 clases con responsabilidades claras; [ ] `mvn compile` limpio; [ ] explica cada clase sin leer el código.
- Evidencia: esquema (foto/README) + salida de `mvn compile`.
- Foco de evaluación: comprensión del problema, modelado, autonomía.

**D2 — Construir comportamiento y reglas**
- Objetivo: implementar el modelo con reglas de negocio.
- Actividades: encapsulación real, composición, enums, `List`, validaciones y excepciones propias; pruebas manuales parciales; bitácora de errores y solución.
- Entregable: app de consola que ejecuta el flujo principal.
- Criterios: [ ] atributos privados con validación; [ ] enum y List usados con criterio; [ ] ≥3 validaciones/excepciones propias; [ ] corre y muestra el flujo.
- Evidencia: salida de ejecución + bitácora.
- Foco de evaluación: calidad técnica, aprendizaje y mejora.

**D3 — Verificar, documentar y sustentar**
- Objetivo: cerrar con evidencia y defensa individual.
- Actividades: refactor; casos válido/inválido/borde (≥3) ejecutados; README (qué resuelve, cómo correr, decisiones, uso de IA); mini demo ≤5 min.
- Entregable: proyecto listo para profesionalizar en S2 + demo.
- Criterios: [ ] 3 tipos de casos documentados con resultado; [ ] README completo; [ ] declara prompts de IA usados y qué ajustó; [ ] defiende sin leer el código.
- Evidencia: README + capturas + demo.
- Foco de evaluación: evidencia/documentación, comunicación.

### Semana 2 — Git/GitHub + JUnit + PR (nace el repo personal)

**D1 — Repo profesional**
- Objetivo: versionar como profesional.
- Actividades: subir el proyecto a GitHub (cuenta personal), `.gitignore`, branch de trabajo, ≥6 commits atómicos, README; glosario del dominio (≥5 términos) en `docs/`.
- Entregable: repo remoto ordenado.
- Criterios: [ ] ≥6 commits con mensajes claros; [ ] `.gitignore` correcto; [ ] branch usada y mergeada; [ ] glosario acordado.
- Evidencia: link del repo + `git log --oneline`.
- Foco de evaluación: evidencia, mejora.

**D2 — JUnit 5 + refactor (y primer CI)**
- Objetivo: convertir casos manuales en tests.
- Actividades: ≥6 tests JUnit 5; refactor con tests verdes; (recomendado) workflow `mvn -q test` en GitHub Actions.
- Entregable: suite de tests + CI.
- Criterios: [ ] ≥6 tests pasan; [ ] refactor sin romper; [ ] (recomendado) Actions verde en el repo.
- Evidencia: salida `mvn test` + pestaña Actions.
- Foco de evaluación: calidad técnica, evidencia.

**D3 — PR + cierre Q1**
- Objetivo: practicar review y defensa.
- Actividades: PR con descripción y criterios; review cruzado (cada alumno revisa el PR de otro); demo quincenal; informe SENATI Q1 (tarea más significativa); el monitor llena Excel S1–S2.
- Entregable: PR mergeado + informe Q1.
- Criterios: [ ] PR con checklist; [ ] review respondido; [ ] demo sustentada; [ ] informe subido.
- Evidencia: PR + informe + Excel.

### Semana 3 — HTTP/JSON/REST + contratos + Build/Buy/Integrate

**D1 — HTTP y JSON**
- Objetivo: entender cómo se comunican los sistemas.
- Actividades: métodos, status codes, headers, JSON; práctica con Postman/curl contra APIs públicas (sin datos sensibles); colección con ≥5 requests.
- Entregable: colección Postman documentada.
- Criterios: [ ] ≥5 requests con respuesta interpretada; [ ] identifica status y errores; [ ] explica request/response.
- Evidencia: colección exportada + notas.
- Foco de evaluación: comprensión, diagnóstico.

**D2 — Contratos de integración**
- Objetivo: diseñar los contratos que usará el bot.
- Actividades: definir JSONs de contacto, solicitud de cita y error; modelar endpoints; comparar polling vs webhook; idempotencia inicial (`request_id`).
- Entregable: carpeta `contracts/` con 3 JSONs + mini documento.
- Criterios: [ ] esquemas completos y consistentes; [ ] errores modelados; [ ] justifica webhook; [ ] explica idempotencia.
- Evidencia: carpeta + doc + sustentación.
- Foco de evaluación: calidad técnica, comunicación.

**D3 — Mapa Build/Buy/Integrate**
- Objetivo: decidir qué se compra, integra y construye.
- Actividades: mapear ManyChat/n8n actuales y su reemplazo; reutilización (Calendar, Sheets, ERP); decisión con riesgos.
- Entregable: diagrama + tabla de decisión.
- Criterios: [ ] cada pieza clasificada (buy/integrate/build); [ ] riesgos identificados; [ ] defendido ante el monitor.
- Evidencia: diagrama + doc.
- Foco de evaluación: criterio, autonomía.

### Semana 4 — Nace el producto (Issues #01–#03) · repo: `ai-business-assistant`

**Reglas de la semana:** todo por Issue → branch corta `issue-NN-slug` → PR con plantilla → CI verde → merge. `main` siempre desplegable.

**D1 — Issue #01: Setup + CI**
- Objetivo: el repo compila, sirve `/health` y tiene CI.
- Actividades: crear `src/{api,agents,tools,rag,memory,channels,models,services,infrastructure}`, `tests/`, `pyproject.toml`/`requirements.txt`, `.env.example`; FastAPI `/health`; ngrok; `docs/CONTEXT.md` + `docs/ARCHITECTURE.md`; workflow CI (`ruff` + `pytest`).
- Entregable: PR #01 mergeado con CI verde.
- Criterios: [ ] `/health` responde 200 local y por ngrok; [ ] CI corre y pasa en el PR; [ ] sin secretos (`.env` ignorado); [ ] docs creados.
- Evidencia: PR + run de CI + captura ngrok.
- Foco de evaluación: calidad técnica, evidencia.

**D2 — Issue #02: Webhook Meta**
- Objetivo: recibir mensajes reales de WhatsApp.
- Actividades: GET verificación (`hub.verify_token`/`challenge`); POST parse del payload (`entry[0].changes[0].value.messages`), extraer `wa_id` y texto; responder 200 rápido; test con fixture realista.
- Entregable: PR #02 con tests.
- Criterios: [ ] GET devuelve el challenge; [ ] POST extrae teléfono y texto del fixture; [ ] responde 200 en <1 s; [ ] logs sin datos sensibles.
- Evidencia: PR + tests + curl/Postman.
- Foco de evaluación: comprensión, calidad técnica.

**D3 — Issue #03: Respuesta saliente + demo E2E + cierre Q2**
- Objetivo: cerrar el ciclo mensaje → respuesta.
- Actividades: `whatsapp_sender.py` async (httpx) + test con mock; demo E2E (mensaje real → eco del bot); métrica base de tiempo de primera respuesta; cerrar #01–#03; demo quincenal + informe SENATI Q2; Excel S3–S4.
- Entregable: PR #03 + video demo + informe Q2.
- Criterios: [ ] respuesta real por Meta a número de prueba; [ ] test con mock (CI sin tokens); [ ] latencia logueada; [ ] Issues #01–#03 cerrados.
- Evidencia: video + PRs + informe.
- Foco de evaluación: comunicación, mejora, evidencia.
