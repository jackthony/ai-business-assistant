# Plan 16 semanas — canónico (v2 vigente)

> **Estado:** v2 vigente (2026-10-06). Este archivo es la fuente canónica del plan; el Excel queda solo para evaluación (nota preliminar que llena el monitor). **Los informes quincenales SENATI y el registro diario los elabora cada alumno**; el monitor da seguimiento (board, PRs, digest) y rumbo. Detalle de las 48 sesiones: Bloques 1–4 abajo.

## Reglas del curso

- **Jornadas:** 3 días oficiales/semana; D1 comprender/diseñar · D2 construir · D3 verificar/documentar/sustentar. No hay tareas obligatorias fuera de esos días.
- **Flujo TBD (ADR-006):** cada sesión arranca de un Issue del backlog → branch `(tbd|issue)-N-<slug>` desde `main` → commits chicos → PR con tests y evidencia → CI verde (4 puertas: `ruff`+`mypy`+`pytest`+`bandit`) → merge squash. El push directo a `main` lo revierte `tbd-enforcer`.
- **Evaluación por criterios:** los tests del PR deben cubrir los **criterios de aceptación del Issue** (casos borde incluidos); el monitor evalúa criterios vs evidencia. Buenas prácticas siempre: type hints, mocks, sin secretos, sin datos reales.
- **Reportes SENATI:** registro diario de horas + informe quincenal con tarea significativa (proceso, herramientas, seguridad ATS, diagrama). Borradores automatizados por `informe-quincenal`. Nota numérica: Excel EVALUABLE + `program/05_EVALUATION/rubric.md`.
- **Stack:** S1–S3 Java 17 + Maven + JUnit 5 (exigencia SENATI) · S4–S16 Python 3.11+, FastAPI, LangGraph, ChromaDB, Whisper local, visión local, Docker. LLM principal: DeepSeek local (Ollama); nube solo WhatsApp Cloud API.

### Histórico v1 (referencia)

> Plan original: Java S1–S3, CI/CD tarde, OCR en S8, HITO 3 en S11. Superado por v2 (abajo); el delta está en "Cambios clave vs v1". No citar del histórico.

## Plan v2 (vigente desde 2026-10-06)

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

S1–S3 se mantienen (Java/Git/HTTP). Plan completo: **S1–S16** (abajo).

## Materiales por semana (fuentes para apoyarse — siempre en `program/02_REFERENCE/source_map.md`)

| Semana | Fuentes primarias (las leen los alumnos) |
|---|---|
| S1–S3 | explicación del monitor + `cursos_de_refuerzo.md` (opcional) |
| S4 | `whatsapp-cloud-api.md` (webhook) + `deepseek-local.md` + repos N2 `pywa`/`fbsamples` (Issue #3/#4) |
| S5 | `langgraph.md` + docs LangGraph + Anthropic «Building Effective Agents» (chaining/paralelización) + matriz semanal en `definitive-guide.md` |
| S6 | `hola-mujer.md` (RAG real) + `agent-engineering-handbook.md` (RAG/memoria) |
| S7 | `langgraph.md` (tools Pydantic) + matriz `definitive-guide.md` |
| S8 | docs Langfuse (telemetría) + `roi_metrics.md` |
| S9 | ADR-009 + `agent-engineering-handbook.md` (HITL/seguridad) + harness lecture-01 (es) |
| S10 | ADR-010 + comparativa Langfuse + microservices.io (multitenant) + Anthropic (routing/orchestrator) |
| S11 | docs Ollama/faster-whisper + `deepseek-local.md` |
| S12 | harness-engineering lectures 10–12 (es) + Anthropic (evaluator-optimizer) + ADR-009 |
| S13 | `agent-engineering-handbook.md` (proactivo/contexto) + `meta-pricing.md` (costo de templates proactivos) |
| S14 | docs Docker + harness lecture-11/12 + ADR-008 |
| S15 | `roi_metrics.md` (FinOps) + `meta-pricing.md` (tarifas reales por categoría) + CI/pre-commit |
| S16 | `rubric.md` + defensa (ADRs) |

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

### Semana 4 — Producto + cierre S3 acelerado (backlog #01–#03 = GitHub #2–#4)

> Contexto real: la arquitectura empresarial ya está definida (Excel operativo + `program/04_DOMAIN/hola-mujer.md`); lo faltante de S3 (HTTP/webhook, contratos, Build/Buy/Integrate) se ve aquí en versión acelerada integrada a los 3 días, y se ahonda en S5–S10. D3 (jue 8-oct): demo; viernes 9-oct: pulir el informe con el borrador automático; **presentación sábado 10-oct** (formato FPE: tarea significativa con proceso, herramientas, seguridad ATS y diagrama). Regla TBD (la hace cumplir `tbd-guardian`): Issue → branch `(tbd|issue)-N-<slug>` desde `main` → `Closes #N` → ≤6 commits → PR → CI verde → merge.
>
> **Meta de la quincena (informe SENATI 10-oct):** Josue lidera #2, Pilar #3 y Allan #4 — cada uno presenta su Issue como tarea más significativa. El workflow `informe-quincenal` genera/refresca el borrador automático del registro semanal desde GitHub **cada noche (mar–vie)** (ya creados: #11 Allan, #12 Pilar, #13 Josue); el alumno completa horas/ATS/reflexión y lo pasa al Word FPE. Las pruebas reales contra Meta dependen de la gestión #16; mientras, trabajan con fixtures.

**D1 — S3 acelerado + Issue #01 (setup + CI)**
- Tareas: leer `program/02_REFERENCE/whatsapp-cloud-api.md` y los esquemas reales de 01_CONTACTOS/02_CITAS/03_EVENTOS (Excel); explicar webhook vs polling, status codes e idempotencia (`request_id`); crear `src/`, `pyproject.toml`, `.env.example`, FastAPI `/health`, ngrok. El CI de 4 puertas (`ruff`+`mypy`+`pytest`+`bandit`) ya está montado: hoy es que el primer PR con `src/` quede verde.
- Criterios: [ ] explican el webhook y el esquema de eventos del negocio; [ ] `/health` 200 local y por ngrok; [ ] CI verde en el PR; [ ] sin secretos.
- Evidencia: PR + captura + explicación oral (alimenta el informe).

**D2 — Issue #02 (webhook Meta)**
- Tareas: GET verificación (`hub.verify_token`/`challenge`); POST parse de `entry[0].changes[0].value.messages` mapeando a los campos reales (contact_id, teléfono, texto); responder 200 <1 s; test con fixture realista.
- Criterios: [ ] challenge correcto; [ ] fixture parseado a los campos del negocio; [ ] 200 rápido; [ ] logs sin datos sensibles.
- Evidencia: PR + tests + curl.

**D3 — Issue #03 (sender + demo) + Build/Buy/Integrate + cierre Q2**
- Tareas: `whatsapp_sender.py` async + test mock; demo E2E real (mensaje → eco); explicar el mapa B/B/I ya definido (ManyChat/n8n se reemplazan; Calendar/Sheets se reutilizan); métrica de primera respuesta.
- Criterios: [ ] respuesta real a número de prueba; [ ] mock en CI; [ ] latencia logueada; [ ] Issues #01–#03 cerrados; [ ] informe Q2: tarea significativa + proceso + herramientas + seguridad (ATS) + diagrama.
- Evidencia: video + PRs + informe FPE.

---

## Detalle de sesiones — Bloque 2 (S5–S8)

### Semana 5 — LangGraph core (Issues #04–#06)

**D1 — Issue #04: StateGraph + AgentState**
- Objetivo: pasar de scripts a un grafo con estado explícito.
- Actividades: definir `AgentState` (`messages` con `Annotated[list, add_messages]`, `phone`, `tenant`, `intent`, `status`); instanciar el grafo mínimo (nodo eco) y probar conversación por CLI antes de tocar WhatsApp; leer handbook Parte II (loop).
- Entregable: PR #04 con grafo mínimo + test.
- Criterios: [ ] AgentState tipado; [ ] grafo compila y responde en CLI; [ ] test del flujo básico; [ ] CI verde.
- Evidencia: PR + test + captura de ejecución.
- Foco de evaluación: comprensión, calidad técnica.

**D2 — Issue #05: System Prompt Hola Mujer v1**
- Objetivo: que el bot hable como el negocio.
- Actividades: construir el prompt por componentes (identidad, tono, límites, tools, memoria) — nunca monolito; reglas: mensajes ≤3 líneas, máx 1 pregunta por turno, español peruano empático; conectar **ChatOllama (DeepSeek local)** al grafo; 10 conversaciones de prueba; handbook Parte III.
- Entregable: PR #05 + prompt versionado en `configs/hola_mujer/prompt_v1.md`.
- Criterios: [ ] prompt por componentes y versionado; [ ] respuestas ≤3 líneas; [ ] no inventa precios (deriva al RAG); [ ] 10 pruebas registradas con ajustes.
- Evidencia: PR + transcripciones + diff del prompt.
- Foco de evaluación: calidad técnica, mejora.

**D3 — Issue #06: Memoria con SqliteSaver**
- Objetivo: el bot recuerda la conversación entre mensajes y reinicios.
- Actividades: `SqliteSaver` con `thread_id` = teléfono; probar continuidad en el 2.º mensaje; reiniciar el server y verificar persistencia; anotar el riesgo de context rot en chats largos (handbook Parte IV-B) como insumo para S13.
- Entregable: PR #06.
- Criterios: [ ] recuerda tras reinicio; [ ] hilos separados por teléfono; [ ] test de continuidad; [ ] CI verde.
- Evidencia: PR + demo corta.
- Foco de evaluación: calidad técnica, evidencia.

### Semana 6 — RAG + HITO 1 (Issues #07–#09)

**D1 — Issue #07: Reglas conversacionales + few-shot**
- Objetivo: manejo de objeciones con el formato correcto.
- Actividades: few-shot con objeciones reales ("está caro", "lo consulto", "¿hay descuento?"); regla de formato; comparar prompt v1 vs v2 con las mismas 10 conversaciones; handbook Parte III (anti-patrones).
- Entregable: PR #07 + prompt v2.
- Criterios: [ ] ≥5 ejemplos few-shot; [ ] objeciones resueltas sin inventar; [ ] formato cumplido en 10/10.
- Evidencia: PR + tabla antes/después.

**D2 — Issue #08: Ingesta Excel → JSON → ChromaDB**
- Objetivo: el bot conoce los 47 servicios reales.
- Actividades: `etl_servicios.py` (05_SERVICIOS → JSON limpio: nombre, precio, duración, categoría); embeddings locales (nomic-embed-text o bge-m3) → ChromaDB namespace `hola_mujer`; tool de búsqueda; verificar 10 preguntas contra la fuente. **Caso de estudio (anti-ejemplo):** `cofounder-agi` — su "memoria RAG" usa vectores aleatorios sembrados con `hash()` (inestable entre procesos): parece memoria semántica pero recupera ruido. Discutir cómo se delata. Si falta corpus de conversaciones de prueba: dataset Bitext de customer support (licencia CDLA, verificado por SHA-256) — referencia `jackthony/IA-local`.
- Criterios: [ ] ETL reproducible y versionado; [ ] colección con los 47 servicios; [ ] 10/10 respuestas verificadas contra el JSON; [ ] sin datos personales; [ ] explican el anti-caso y cómo se detecta (retrieval sin relevancia).
- Evidencia: PR + dataset JSON + resultados.

**D3 — Issue #09: HITO 1 + cierre Q3**
- Objetivo: bot real respondiendo en WhatsApp + demostración quincenal.
- Actividades: conectar webhook → grafo → RAG; demo en vivo (precios, duraciones, promos); medir latencia de primera respuesta y respuestas correctas (meta ≥8/10); demo quincenal + informe SENATI Q3; el monitor llena Excel S5–S6.
- Entregable: release `hito-1` + video demo + informe Q3.
- Criterios: [ ] flujo WhatsApp → RAG → respuesta real; [ ] métricas del hito registradas; [ ] informe Q3 subido; [ ] release publicado.
- Evidencia: video + release + informe.
- **HITO 1 ✅**

### Semana 7 — Tools + Agentes 1 y 2 (Issues #10–#12)

**D1 — Issue #10: Agente 1 Info & RAG + guardrail Chimbote**
- Objetivo: respuestas comerciales confiables y con fuente.
- Actividades: nodo especialista de información con contrato de salida (respuesta breve + precio + ubicación Chimbote + CTA); guardrail de ubicación (fuera de Chimbote → respuesta definida); búsqueda híbrida keyword+vector; 10 casos de evaluación.
- Criterios: [ ] 10/10 respuestas con respaldo del RAG; [ ] cero precios inventados; [ ] guardrail de ubicación probado; [ ] CI verde.
- Evidencia: PR + tabla de 10 casos.
- Foco de evaluación: calidad técnica, criterio.

**D2 — Issue #11: Pydantic tools estrictas**
- Objetivo: tools que no aceptan basura.
- Actividades: `@tool consultar_servicio()` con schemas Pydantic V2 (entrada/salida), errores tipados; tests válido/inválido/borde; verificar tool-calling con el modelo local (si falla, cambiar a `qwen2.5-coder`); handbook Parte VI (diseñar la ACI, no solo el prompt).
- Criterios: [ ] 100% de args validados; [ ] tests de los 3 tipos; [ ] tool-calling funcionando con el modelo local; [ ] CI verde.
- Evidencia: PR + tests.
- Foco de evaluación: calidad técnica, autonomía.

**D3 — Issue #12: Agente 2 Citas y disponibilidad**
- Objetivo: proponer horarios reales y evitar colisiones.
- Actividades: leer disponibilidad (`02_CITAS` / Google Calendar mock); nodo que propone 2–3 opciones reales; confirmación básica; idempotencia con `request_id`; pruebas de colisión.
- Criterios: [ ] propone solo horarios libres (0 colisiones en 10 pruebas); [ ] mismo `request_id` no duplica cita; [ ] conversación completa probada.
- Evidencia: PR + escenarios.
- Foco de evaluación: comprensión, calidad técnica.

### Semana 8 — Cierre de venta + telemetría (Issues #13, #14, #25)

**D1 — Issue #13: Agente 3 Cierre y registro de lead**
- Objetivo: pedir datos y formalizar la intención de compra.
- Actividades: nodo que solicita nombre, DNI y teléfono con validación (DNI 8 dígitos, celular PE); estados del cierre (`waiting_data`, `ready_to_book`); tests de datos inválidos; nunca pedir datos clínicos.
- Criterios: [ ] valida DNI/teléfono; [ ] flujo info → cita → datos completo; [ ] sin datos clínicos; [ ] CI verde.
- Evidencia: PR + transcripción.
- Foco de evaluación: comprensión, comunicación.

**D2 — Issue #14: registrar_lead_sheet()**
- Objetivo: persistir el lead real sin duplicados.
- Actividades: tool que escribe en Google Sheets/DB (mock en CI); idempotencia + log de auditoría; prueba real con fila de prueba; **gate N2**: la escritura requiere confirmación (harness, ADR-009).
- Criterios: [ ] una fila por lead (sin duplicados); [ ] mock en CI (sin credenciales); [ ] log sin datos sensibles; [ ] gate de confirmación activo.
- Evidencia: PR + captura de la hoja.
- Foco de evaluación: evidencia, calidad técnica.

**D3 — Issue #25: Telemetría temprana + cierre Q4**
- Objetivo: ver el sistema por dentro antes de crecer.
- Actividades: Langfuse (self-host/local) o LangSmith: trazas por nodo, latencia, tokens; dashboard mínimo (primera respuesta, contención, errores por nodo); demo quincenal + informe SENATI Q4; Excel S7–S8.
- Entregable: release `q4` + informe Q4.
- Criterios: [ ] trazas por conversación visibles; [ ] dashboard con 3 métricas; [ ] error inducido detectado en trazas; [ ] informe subido.
- Evidencia: captura del dashboard + informe.
- Foco de evaluación: aprendizaje y mejora, evidencia. **Observabilidad temprana: es la base para el multiagente.**

---

## Detalle de sesiones — Bloque 3 (S9–S12)

### Semana 9 — Safety + HITL/harness + HITO 2 (Issues #16–#18)

**D1 — Issue #16: Agente 4 Safety & triage clínico**
- Objetivo: el bot nunca improvisa en salud.
- Actividades: clasificador de riesgo **de 1 token con confianza calibrada** (patrón Jev de `jackthony/IA-local`: Choice + logprobs + umbral), no texto libre; nodo que congela el flujo (`status=handoff_requested`); respuestas puente definidas ("ya te contacta una especialista"); 15 casos (10 normales, 5 de riesgo).
- Entregable: PR #16 + tabla de 15 casos.
- Criterios: [ ] 5/5 casos de riesgo congelados; [ ] 0/10 falsos positivos en normales; [ ] respuesta puente sin diagnóstico; [ ] CI verde.
- Evidencia: PR + tabla + transcripciones.
- Foco de evaluación: criterio, seguridad, comprensión.

**D2 — Issue #17: HITL con interrupt + permisos N1/N2/N3**
- Objetivo: cuando el bot se congela, avisa a Jioysi y un humano reanuda.
- Actividades: `interrupt()` de LangGraph; alerta a Jioysi (WhatsApp/Email) dentro del SLA del negocio (10 min, `04_CONFIG`); clasificar tools por nivel (N1 auto: RAG/precios/disponibilidad · N2 aprobación: agendar/registrar/validar pago · N3 nunca: borrar/precios base); patrón `draft → review → apply`; probar reanudación sin re-ejecutar efectos.
- Entregable: PR #17.
- Criterios: [ ] pausa y reanuda con `Command(resume=)`; [ ] alerta real recibida por Jioysi (prueba); [ ] tools clasificadas N1/N2/N3; [ ] efecto no se duplica al reanudar (test).
- Evidencia: PR + captura de alerta + test de re-ejecución.
- Foco de evaluación: calidad técnica, criterio.

**D3 — Issue #18: HITO 2 — agente único completo + handoff**
- Objetivo: demostrar el asistente completo y confiable (sin supervisor todavía).
- Actividades: flujo E2E real (info → cita → datos → pago/handoff); batería de 12 escenarios (2 de handoff, 1 de re-ejecución); release `hito-2`; medir contención y latencia.
- Criterios: [ ] 12/12 escenarios según lo esperado; [ ] handoff real a Jioysi; [ ] métricas del hito; [ ] release publicado.
- Evidencia: video + release + tabla de escenarios.
- **HITO 2 ✅**

### Semana 10 — OCR + supervisor + multitenant (Issues #15, #19, #20)

**D1 — Issue #15: OCR de pagos (Yape/Plin)**
- Objetivo: leer comprobantes y validar el caso feliz sin humano.
- Actividades: recibir imagen del webhook; visión local (Qwen2.5-VL en Ollama) → JSON (monto, fecha, destinatario, operación); tool `validar_comprobante()` con Pydantic + reglas (monto ≥ precio, fecha ≤24 h); dudas → N2; 8 casos (válido, borroso, monto insuficiente, captura dudosa...).
- Criterios: [ ] extrae campos en ≥6/8 casos; [ ] reglas de negocio aplicadas; [ ] dudas → handoff; [ ] datos del comprobante no se persisten completos.
- Evidencia: PR + matriz de 8 casos.
- Foco de evaluación: calidad técnica, criterio.

**D2 — Issue #19: Supervisor router + clase de frameworks**
- Objetivo: orquestar agentes y comparar arquitecturas con criterio.
- Actividades: clasificador rápido (reglas/intención) primero y supervisor LLM para ambiguos; deriva a info/citas/checkout/safety; trazas del ruteo; clase 30 min: panorama (OpenAI Agents SDK, MS Agent Framework, Strands — handoffs, hooks, workflows) con la comparativa de Langfuse y por qué seguimos en LangGraph (ADR-010); comparar la lib `langgraph-supervisor` y el triage de 1 token de Jev contra el router propio. **Contraste en vivo:** el `prompt_supervisor.txt` del SOC del curso 1 intenta imponer el flujo por texto ("no vuelvas a ejecutar", "máximo 3 delegaciones") — frágil; la lección: la estructura vive en el grafo, no en el prompt.
- Criterios: [ ] ≥13/15 mensajes ruteados bien; [ ] fallback a LLM en ambiguos; [ ] trazas muestran el ruteo; [ ] nota de la comparativa entregada.
- Evidencia: PR + tabla de ruteo + nota.
- Foco de evaluación: comprensión, criterio.

**D3 — Issue #20: Multitenant base + cierre Q5**
- Objetivo: NeuraCode vive en el mismo núcleo.
- Actividades: resolver tenant por `phone_number_id`; `configs/{hola_mujer,neuracode}` con prompt, namespace RAG y tools permitidas; cargar tenant `neuracode` con prompt v0; demo quincenal + informe SENATI Q5; Excel S9–S10.
- Criterios: [ ] mismo grafo atiende 2 números con prompts distintos; [ ] sin fugas de datos entre tenants; [ ] informe Q5 subido; [ ] release `q5`.
- Evidencia: PR + demo + informe.
- Foco de evaluación: calidad técnica, evidencia.

### Semana 11 — NeuraCode + voz (Issues #21–#23)

**D1 — Issue #21: Ingesta de cursos NeuraCode**
- Objetivo: el tenant 2 responde con datos reales.
- Actividades: ETL de cursos/temarios/precios → JSON → ChromaDB namespace `neuracode`; prompt de negocio NeuraCode (tono academia); 10 preguntas verificadas.
- Criterios: [ ] colección cargada; [ ] 10/10 verificadas contra fuente; [ ] aislamiento por namespace.
- Evidencia: PR + dataset + resultados.

**D2 — Issue #22: Whisper local (notas de voz)**
- Objetivo: entender audios de WhatsApp.
- Actividades: descargar media de Meta (`type=audio`) y transcribir con faster-whisper (`language="es"`); inyectar la transcripción al grafo como mensaje; 5 audios de prueba (uno con ruido, uno largo).
- Criterios: [ ] ≥4/5 transcripciones correctas; [ ] el audio entra por el mismo grafo; [ ] tiempo de transcripción registrado; [ ] sin conservar audios de prueba.
- Evidencia: PR + tabla de transcripciones.
- Foco de evaluación: calidad técnica, mejora.

**D3 — Issue #23: Normalización de audio y contexto**
- Objetivo: que la transcripción llegue limpia y contextualizada.
- Actividades: limpiar muletillas, detectar intención principal, marcar dudas; fallback si la transcripción es ininteligible ("¿me lo escribes, por favor?"); pruebas A/B contra el texto equivalente.
- Criterios: [ ] mismo resultado que el texto equivalente en ≥4/5 casos; [ ] fallback probado; [ ] tests; [ ] CI verde.
- Evidencia: PR + comparativas.

### Semana 12 — HITO 3 + seguridad + evals (Issues #24, #26, #27)

**D1 — Issue #24: HITO 3 — NeuraCode + multimodal**
- Objetivo: demostrar el segundo tenant con voz e imagen.
- Actividades: demo NeuraCode (cursos) + nota de voz + comprobante; métricas del hito; release `hito-3`.
- Criterios: [ ] NeuraCode responde con datos reales; [ ] audio y comprobante funcionan E2E; [ ] métricas registradas; [ ] release publicado.
- Evidencia: video + release.
- **HITO 3 ✅**

**D2 — Issue #26: Seguridad OWASP + inyección**
- Objetivo: blindar antes de crecer.
- Actividades: sanitización + input guardrails (ASI01 goal hijacking, ASI02 tool misuse); suite de inyección (≥15 ataques: "ignora tus instrucciones...", payloads en RAG, enlaces); rate limit; verificar tiers N1/N2/N3; logs sin datos sensibles.
- Criterios: [ ] ≥14/15 ataques bloqueados o contenidos; [ ] ninguna tool N3 expuesta; [ ] suite corre en CI; [ ] incidentes documentados.
- Evidencia: PR + reporte de la suite.
- Foco de evaluación: seguridad, criterio.

**D3 — Issue #27: Evals offline + cierre Q6**
- Objetivo: medir calidad con datos, no con opiniones.
- Actividades: set de ≥20 casos (fidelidad RAG, relevancia, tono, handoff correcto); LLM-as-a-Judge local offline (`deepseek-r1:14b`) con rúbrica y, en paralelo, decisiones tipadas calibradas (Jev: Choice/Score con logprobs) comparando costo/calidad; aplicar la heurística de validadores (Lusser: `v·r/f > p/(1-p)`) para decidir qué jueces valen; demo quincenal + informe SENATI Q6; Excel S11–S12.
- Criterios: [ ] ≥20 casos evaluados; [ ] puntuación antes/después de una mejora de prompt; [ ] juez descartado si no supera el umbral de Lusser; [ ] informe Q6 + release `q6`.
- Evidencia: PR + reporte de evals.
- Foco de evaluación: evaluación, aprendizaje y mejora.

---

## Detalle de sesiones — Bloque 4 (S13–S16)

### Semana 13 — Proactivo + analytics (Issues #28–#30)

**D1 — Issue #28: Módulo proactivo de reactivación**
- Objetivo: recuperar chats abandonados sin ser invasivo.
- Actividades: background task (FastAPI) o cron que detecta conversaciones inactivas >2 h en los checkpoints (patrón heartbeat, handbook Parte II); respetar la ventana de 24 h o usar template aprobada por Meta; 5 casos de prueba (activo, inactivo, ya cerrado, en handoff, recién activo).
- Criterios: [ ] detecta inactivos sin falsos positivos en 5 casos; [ ] respeta ventana/template de Meta; [ ] no reactiva si `handoff_requested`; [ ] test con reloj simulado.
- Evidencia: PR + tabla de casos.
- Foco de evaluación: calidad técnica, criterio.

**D2 — Issue #29: Mensajes de seguimiento personalizados**
- Objetivo: seguimiento con contexto, no spam.
- Actividades: mensaje generado según el último estado (pidió precio, eligió horario, dudó del pago); máximo 1 seguimiento por conversación; tono humano y breve; prompt versionado; pruebas A/B.
- Criterios: [ ] el mensaje cita el contexto correcto en 5/5; [ ] 1 solo envío por chat; [ ] sin inventar promociones.
- Evidencia: PR + transcripciones.
- Foco de evaluación: calidad técnica, mejora.

**D3 — Issue #30: Analytics de conversión**
- Objetivo: medir recuperación y embudo.
- Actividades: dashboard del embudo (conversación → lead → cita → pago) con telemetría + Sheets; tasa de recuperación de abandonados; comparación contra baseline (ManyChat/primeras 2 semanas).
- Criterios: [ ] embudo con 4 etapas visible; [ ] tasa de recuperación calculada; [ ] dataset anonimizado listo para el informe.
- Evidencia: PR + captura del dashboard.
- Foco de evaluación: evidencia, criterio.

### Semana 14 — Producción: Postgres + Docker + deploy (Issues #31–#33)

**D1 — Issue #31: Migración a PostgresSaver**
- Objetivo: memoria de producción con concurrencia.
- Actividades: `docker compose` con Postgres local; migrar de SqliteSaver a PostgresSaver; verificar continuidad de hilos; prueba de 10 conversaciones simultáneas; plan de migración de datos existentes (o corte aceptado).
- Criterios: [ ] la conversación continúa tras migrar; [ ] 10 conversaciones sin mezclar hilos; [ ] compose documentado; [ ] CI con servicio Postgres.
- Evidencia: PR + tests.
- Foco de evaluación: calidad técnica, autonomía.

**D2 — Issue #32: Dockerfile**
- Objetivo: imagen reproducible y segura.
- Actividades: Dockerfile multi-stage, usuario no root, sin secretos; `.dockerignore`; build local y run con env de prueba; tamaño razonable.
- Criterios: [ ] build limpio; [ ] la imagen responde `/health`; [ ] sin secretos en capas; [ ] tamaño documentado.
- Evidencia: PR + build log.
- Foco de evaluación: calidad técnica.

**D3 — Issue #33: Deploy webhook 24/7 + cierre Q7**
- Objetivo: producción real.
- Actividades: desplegar (Render/VPS/Railway) con Postgres; registrar la URL en Meta; secrets en el proveedor; smoke test E2E real; rollback documentado; demo quincenal + **informe Q7 (lo redacta el alumno)**; Excel S13–S14.
- Criterios: [ ] webhook verificado en Meta y el bot responde desde la nube; [ ] un reinicio preserva la memoria; [ ] rollback probado; [ ] informe Q7 subido por el alumno.
- Evidencia: URL + video + checklist.
- Foco de evaluación: robustez, evidencia.

### Semana 15 — E2E + fallbacks + FinOps + docs (Issues #34–#36)

**D1 — Issue #34: Integración y reconciliación E2E**
- Objetivo: ningún dato se pierde entre sistemas.
- Actividades: verificar Calendar, Sheets y (si existe) ERP con reintentos e idempotencia; reconciliación si Sheets falla después de agendar; 3 escenarios de fallo parcial.
- Criterios: [ ] 0 citas perdidas en 10 pruebas con fallos inyectados; [ ] reintentos con backoff; [ ] alerta si el fallo es definitivo.
- Evidencia: PR + escenarios.
- Foco de evaluación: calidad técnica, criterio.

**D2 — Issue #35: Fallbacks de modelos + FinOps**
- Objetivo: seguir funcionando si un modelo cae y saber cuánto cuesta.
- Actividades: fallback local (p. ej. `qwen2.5-coder` ↔ `deepseek`) con detector de timeout/fallo; medir **costo por conversación** (cómputo local + mensajes Meta) y compararlo con alternativas cloud; registrar el resultado real en `program/00_PROJECT/roi_metrics.md`.
- Criterios: [ ] conmutación probada (apagar un modelo a propósito); [ ] degradación visible en logs; [ ] costo por conversación calculado con datos reales.
- Evidencia: PR + tabla de costos.
- Foco de evaluación: criterio, evidencia.

**D3 — Issue #36: Refactor SOLID + documentación**
- Objetivo: repo presentable y mantenible.
- Actividades: limpieza SOLID, eliminar código muerto, docstrings, OpenAPI/Swagger completo, README final con arquitectura y cómo correr; actualizar `docs/ARCHITECTURE.md` con las decisiones reales.
- Criterios: [ ] las 4 puertas del CI verdes (`ruff`+`mypy`+`pytest`+`bandit`); [ ] Swagger cubre todos los endpoints; [ ] README final; [ ] sin TODOs huérfanos.
- Evidencia: PR + docs.
- Foco de evaluación: mejora, evidencia.

### Semana 16 — Capstone + defensa + transferencia (Issues #37–#39)

**D1 — Issue #37: Pruebas E2E completas**
- Objetivo: correr la batería completa como release candidate.
- Actividades: suite E2E con los 4 agentes + voz + OCR + handoff + proactivo (≥20 escenarios); regresión de seguridad (inyección) y de evals (≥20 casos); bug bash y corrección de lo crítico.
- Criterios: [ ] suite completa verde; [ ] regresión de seguridad y evals sobre umbral; [ ] incidencias críticas corregidas; [ ] tag `rc-1`.
- Evidencia: resultados + issues creados/cerrados.
- Foco de evaluación: calidad técnica, aprendizaje y mejora.

**D2 — Issue #38: Defensa técnica**
- Objetivo: preparar la presentación individual y colectiva.
- Actividades: arquitectura, decisiones (ADRs), métricas de telemetría y ROI, demo guionizada; cada alumno prepara su parte y su retrospectiva; ensayo general.
- Criterios: [ ] presentación lista (15 min); [ ] cada alumno explica 2 decisiones técnicas; [ ] métricas actualizadas.
- Evidencia: slides + ensayo.
- Foco de evaluación: comunicación.

**D3 — Issue #39: Demo final + transferencia + cierre Q8**
- Objetivo: entregar el sistema funcionando y transferirlo.
- Actividades: demo E2E ante Hola Mujer/NeuraCode; entrega del repo, accesos y runbook; **informe final SENATI (lo redacta cada alumno)** + acta en `program/05_EVALUATION/`; release `v1.0`; retrospectiva del programa.
- Criterios: [ ] demo en producción real; [ ] runbook y accesos entregados; [ ] release `v1.0` publicado; [ ] informes finales subidos por los alumnos; [ ] retrospectiva documentada.
- Evidencia: release + runbook + informes.
- **Demo final ✅**
