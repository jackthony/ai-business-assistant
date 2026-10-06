# SOURCE_MAP — base de conocimiento del proyecto (curaduría verificada 2026-10-06)

> Este es el mapa de qué se consulta, cuándo y con qué autoridad. No es una lista de links: es la política de context que usan el monitor, los practicantes y DeepSeek.
>
> **Orden de autoridad:** doc oficial/spec > código reproducible (repo real) > libro/curso > paper > afirmación de un LLM. Un LLM nunca es autoridad; toda afirmación técnica se verifica contra fuente primaria.

## Nivel 0 — Materiales entregados por el monitor (referenciados, no copiados)

| Material | Rol | Estado |
|---|---|---|
| `Hola Mujer · MVP WhatsApp ManyChat · Operativo (1).xlsx` (11 hojas) | KB-A: catálogo, reglas, config del negocio | ✅ verificada; resumida en `program/04_DOMAIN/hola-mujer.md`; bloqueantes en `hola-mujer.md` §Bloqueantes |
| **Conversaciones reales de la era ManyChat/n8n** (export del negocio) | Corpus de aprendizaje del agente (anonimizado en `data/conversaciones/`): few-shot, objeciones, evals, baseline | ✅ autorizado por el dueño (negocio propio); pendiente exportar y anonimizar |
| `Plan Maestro — HealthTech Software & AI — SENATI 2026 (EVALUABLE).xlsx` | Evaluación numérica (16 semanas × 3 alumnos) | vive en Drive (binario); fórmulas verificadas al migrar |
| Informe FPE SENATI (CNIU-108, `.pages`) | Formato institucional quincenal: registro diario, PEA, tarea significativa | esquema documentado en `current_status.md`/`operacion.md`; el archivo vive en Descargas/Drive |
| Docs originales del proyecto (README v1 y notas previas del monitor) | Material de arranque del programa | reemplazados por `program/` — fuera del repo, no se citan como fuente viva |
| `material-langchain/` (carpeta local, fuera de git) | Ejercicios del curso 1 ordenados por tema | mapeo en `program/01_CURRICULUM/cursos_de_refuerzo.md` |

## Nivel 1 — Autoridad técnica (docs oficiales)

| Fuente | Rol | Estado | Consultar cuando |
|---|---|---|---|
| LangGraph docs | Motor del grafo, checkpointers, interrupt | activo | diseño de estado, memoria, HITL (S5+) |
| OpenAI Agents SDK (docs) | Abstracciones agents/tools/handoffs | activo (0.x, MIT) | entender handoffs en S10 (no migrar: ADR-002/010) |
| MCP spec (`modelcontextprotocol.io`) | Protocolo tools/context | activo | desacoplar herramientas (S10+, opcional) |
| FastAPI docs | API async, BackgroundTasks, OpenAPI | activo | webhook y endpoints (S4+) |
| Pydantic v2 docs | Schemas, validación, tools | activo | contratos y tools (S5+) |
| Meta WhatsApp Cloud API | Canal: webhook, payloads, envío, precios | activo | S4–S16 (ver `whatsapp-cloud-api.md`); precios archivados en `meta-pricing.md` (captura 2026-10-06: Perú standalone desde 1-oct-2026, valores de referencia vía plivo.com/whatsapp/pricing/pe y formbeep.com/whatsapp-api-pricing — confirmar contra el panel Billing del WABA) |
| Ollama docs | Modelos locales (DeepSeek/Qwen) | activo | S4+ (ver `deepseek-local.md`) |
| Docker docs | Imagen y compose | activo | S14 |
| Trunk-Based Development | Flujo git/TBD | activo | S2+ (ver ADR-006) |
| OWASP GenAI Security Project (`genai.owasp.org`) — Top 10 LLM 2026 + **Agent Control Standard (ACS, 2026-09)** + Top 10 for Agentic Applications (ASI) | Seguridad ASI01–ASI10, mitigaciones, estándar de control de agentes | activo (dominio migró de owasp.org) | S12, S15 (ver ADR-009) |
| Anthropic — «Building Effective Agents» (Schluntz/Zhang, web) | Taxonomía workflows vs agentes: chaining, routing, parallel, orchestrator-workers, evaluator-optimizer; bloques base (retrieval/tools/memory) | activo — enlazar la web, no copiar (© Anthropic) | S5 chaining/paralelización · S10 routing/orchestrator · S12 evaluator/evals |

## Nivel 2 — Repos de ingeniería (leer código real, no copiar sin licencia)

| Repo | Rol | Estado | Consultar cuando |
|---|---|---|---|
| `openai/openai-agents-python` | Handoffs, guardrails de I/O, sessions, tracing | activo 0.x, MIT | S10: patrones a copiar como nodos; **no adoptar** (ADR-010) |
| `langchain-ai/langgraph` | Código fuente del motor; ejemplos | activo | bugs de concurrencia, `interrupt()` (S5+) |
| `microsoft/agent-framework` | Workflows, middleware, time-travel, .NET-first | activo 1.x, MIT | S10: comparación educativa únicamente |
| `strands-agents/sdk-python` | Hooks de ciclo de vida, límites de turno/tokens, evals | activo 1.x, Apache-2.0 | S10/S12: ideas de lifecycle y evaluación |
| `RichmondAlake/agent_harness_course` | Approval gates, tiers de permisos, tests de inyección | activo, **sin licencia → prohibido copiar código** | S9/S12: leer patrones; NO correr live (Oracle/MemoRizz) |
| `modelcontextprotocol/servers` | Servidores MCP de ejemplo | activo | S10–S12 (opcional) |
| `jackthony/IA-local` (lab interno, **MIT**, del monitor) | **Jev**: decisiones tipadas de 1 token con confianza calibrada (logprobs, ~1–2 s en CPU); labs de 11 patrones; CI zero-trust (Actions por SHA, escáner de secretos); compose endurecido; datasets con SHA-256 y licencias | activo | Jev → triage S9, router S10, evals S12; labs → S5–S10; compose/CI → S14/S4 |
| `david-lev/pywa` (**MIT**, 592★) | Framework Python para Cloud API con integración nativa FastAPI (`server=app, webhook_endpoint=...`): verify + parseo de webhooks + envío | activo (2026-10) | Issue #3 (webhook) y #4 (sender): leer su código como referencia, no copiar el framework |
| `fbsamples/whatsapp-api-examples` (oficial Meta, licencia de muestras) | Ejemplos oficiales de webhook GET (verify_token) y POST (messages/status) | activo | Issue #3: estructura del payload y verificación |

## Nivel 3 — Material educativo (conceptos)

| Fuente | Rol | Consultar |
|---|---|---|
| `Nicolepcx/ai-agents-the-definitive-guide` (CH01–CH12) | Eje conceptual del programa (ver `definitive-guide.md`). Libro O'Reilly publicado el 6-oct-2026 (376 pp, aún sin reseñas que lo validen → lectura guiada, no verdad) | semana a semana según matriz |
| «Comprehensive Guide to AI Agent Engineering» (Vasilyev, MIT, 138 pp) | Guía de apoyo de alumnos: loops, context rot, compaction, memoria, tools, HITL, seguridad, evals, costos (ver `agent-engineering-handbook.md`) | por partes, según matriz semanal |
| `Nicolepcx/transformers-the-definitive-guide` (CH01–CH12, Apache-2.0, notebooks Colab) | Consulta **opcional** de alumnos: CH09 agentes y CH11 despliegue de modelos; el stack del proyecto usa Ollama/LangGraph, no transformers | cuando un alumno quiera ver qué hay debajo del modelo (S12 evals o curiosidad) |
| `walkinglabs/learn-harness-engineering` (**MIT**, 19.4k★, sección `docs/es/`) | Harness engineering en **español**: por qué fallan agentes capaces (5 capas), brecha de verificación, Definition of Done verificable | activo | lecture-01 lectura obligatoria en S12; lectures 10–12 en S12/S14; conceptos en S9 (HITL) |
| «Microservices Patterns» (Chris Richardson) + microservices.io | El libro fue **liberado por el autor** (2026-10) → ya es referenciable. Patrones traducibles al monolito modular multitenant (schema por tenant, API gateway, transacciones) | activo, gratuito | S10 multitenant — lectura opcional de alumnos; microservices.io como resumen rápido |
| OpenTelemetry GenAI semantic conventions (`open-telemetry/semantic-conventions-genai`, Apache-2.0) | Estándar de trazas/métricas/eventos para LLM, agentes y MCP (2026→2027) | activo | S8 instrumentación + S12 evals + S15 FinOps (ver `observabilidad-costos.md`) |
| Langfuse docs + pricing (verificado 2026-10-06) | Telemetría/evals S8: **self-host gratis** (Docker en la M5) o cloud Hobby gratis (50k units, 2 users, 30 días) · Core $29/mes · Pro $199/mes | activo | S8 telemetría · S12 evals (ver `observabilidad-costos.md`) |
| Kapso (BSP dev-first) + n8n — comparativa B/B/I en `kapso-n8n.md` | Capas no-diferenciadoras: canal WhatsApp (plan B) y glue operativo | activo (precios verificados 2026-10-06) | S10 decisión B/B/I |
| Taller O'Reilly "Harness Engineering for Long-Running Agent Skills" (10-nov, Koenigstein) | Contenido avanzado (skills versionadas, repair loops). Intermedio-avanzado, requiere OpenRouter + Langfuse/LangSmith; sin precio suelto (solo suscripción O'Reilly USD 49/mes); repo "to come" | **No comprar para el monitor.** Si se asiste (trial): preparar Python 3.12 + OpenRouter + Langfuse self-host y lectura previa CH05/CH08/CH09/CH10 del libro. Autora verificada: Nicole Koenigstein (el "análisis forense" del doc de Agentes describe a Alake, no este evento) |

## Nivel 4 — Investigación (anexos opcionales S12+, jamás currículo)

- AgensFlow (arXiv:2605.27466, Koenigstein, preprint sin peer review, resultados auto-reportados).
- Benchmarks de evaluación de agentes (AgentVista, AHE, etc.) y papers de harness: solo lectura para el mes 3 si un practicante muestra interés. No se cargan en contexto de DeepSeek.
- `KevinKantule/cofounder-agi` (revisado 2026-10-06, **sin licencia → no copiar código**): ideas aprovechables (loop coder→reviewer→ejecución→corrección; auditoría de modelos reales por proveedor) y **anti-ejemplo de RAG falso** (embeddings = ruido por hash inestable) usado como caso de estudio en S6.

## Nivel 5 — Cursos Udemy (opcional para practicantes, verificado 2026-10)

3 cursos verificados (Hernández · 365 Careers ×2) con tabla completa y plan de refuerzo en `program/01_CURRICULUM/cursos_de_refuerzo.md` (no duplicar aquí).

**Gap global:** ninguno cubre Ollama ni WhatsApp. Plan de refuerzo con compras opcionales (máx. 1–2, ~$20–30 en oferta) en `program/01_CURRICULUM/cursos_de_refuerzo.md`; alternativas gratis: docs Meta/Ollama/ChatOllama, video de Dani Fuyà (WhatsApp + LangGraph, stack casi idéntico) y plantillas FastAPI de GitHub. Nunca son fuente de verdad; si contradicen una doc oficial, gana la doc.

## Kit de rescate (síntoma → fuente)

| Síntoma | Ir a |
|---|---|
| El bot olvida la conversación | CH10 + LangGraph checkpointers (`thread_id` = teléfono) |
| Tool con argumentos inválidos o alucinados | CH05 + Pydantic v2 |
| No deriva al agente correcto | CH02 + patrón handoff de `openai-agents-python` (S10) |
| Prompt injection / goal hijacking | OWASP ASI01/ASI02 + ADR-009 (permisos por nivel) |
| La acción se ejecuta dos veces al reanudar | Patrón `draft → review → apply` (ADR-009) |
| Errores al desplegar / fallback de modelos | CH07 + Docker docs + ADR-008 |
| Latencia o costo alto | CH11 + `program/00_PROJECT/roi_metrics.md` |
| Duda de framework | ADR-002 y ADR-010 (no se migra sin ADR nuevo) |
| Cliente pregunta "¿qué gano?" | `program/00_PROJECT/roi_metrics.md` (KPIs y benchmarks) |

## Reglas de curación

1. Máximo ~20 fuentes activas. Para agregar una, se quita o degrada otra.
2. Cada fuente tiene autoridad, estado y "cuándo consultar"; nada entra sin eso.
3. Revisión trimestral de estado (activo/deprecado). Si una fuente muere, se elimina del mapa.
4. Prohibido duplicar contenido dentro del repo: se enlaza la fuente, no se copia.
5. Evidencia antes de opinión: la misma regla que se enseña a los practicantes aplica al monitor y a la IA.
