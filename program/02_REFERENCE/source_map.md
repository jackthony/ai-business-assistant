# SOURCE_MAP — base de conocimiento del proyecto (curaduría verificada 2026-10-06)

> Este es el mapa de qué se consulta, cuándo y con qué autoridad. No es una lista de links: es la política de context que usan el monitor, los practicantes y DeepSeek.
>
> **Orden de autoridad:** doc oficial/spec > código reproducible (repo real) > libro/curso > paper > afirmación de un LLM. Un LLM nunca es autoridad; toda afirmación técnica se verifica contra fuente primaria.
>
> **Columna «Última verificación»** (niveles 1–3): `fecha · método`. Del más fuerte al más débil: **ejecutado** (el paquete se instaló y los ejemplos pasaron) > **abierta** (alguien leyó la fuente en esa fecha) > **enlace responde / existe (git)** (solo se comprobó que la URL abre, o que el repo existe con `git ls-remote`; el contenido no se releyó) > **curaduría** (se listó en la curaduría del 2026-10-06; el método no quedó registrado) > **reseña secundaria** > **pendiente**. Una fecha de curaduría no prueba que la doc siga vigente, y **un enlace presente no significa fuente verificada**: solo indica dónde buscar; el estado real es el de la columna. Antes de enseñar con una fuente, mira su fila.

## Inspiración directa del proyecto (indicada por el monitor)

| Fuente | Qué inspiró | Licencia / uso |
|---|---|---|
| [`jackthony/IA-local`](https://github.com/jackthony/IA-local) (lab propio) | Patrón **Jev** (decisiones tipadas de 1 token con confianza calibrada), labs de 11 patrones, CI zero-trust (Actions por SHA, escáner de secretos) | MIT, del monitor — ver `jev-pattern.md` |
| [`Nicolepcx/ai-agents-the-definitive-guide`](https://github.com/Nicolepcx/ai-agents-the-definitive-guide) (CH01–CH12) | Eje conceptual del programa: capítulos y matriz semanal en `definitive-guide.md` | Lectura guiada, no verdad; citar, no copiar |

> Si el monitor agrega otra inspiración directa, se añade aquí con su licencia y se refleja en el README y en la wiki (regla de curación: ~20 fuentes activas).

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

| Fuente | Rol | Estado | Consultar cuando | Última verificación |
|---|---|---|---|---|
| [LangGraph docs](https://langchain-ai.github.io/langgraph/) | Motor del grafo, checkpointers, interrupt | activo | diseño de estado, memoria, HITL (S5+) | 2026-10-08 · ejecutado (paquete 1.2.14 + ejemplos); 2026-10-16 enlace responde (monitor), contenido sin releer; `docs.langchain.com/oss/python/langgraph/overview` sin confirmar |
| [OpenAI Agents SDK (docs)](https://openai.github.io/openai-agents-python/) | Abstracciones agents/tools/handoffs | activo (0.x, MIT) | entender handoffs en S10 (no migrar: ADR-002/010) | 2026-10-06 · curaduría |
| [MCP spec](https://modelcontextprotocol.io) (`modelcontextprotocol.io`) | Protocolo tools/context | activo | desacoplar herramientas (S10+, opcional) | 2026-10-06 · curaduría |
| [FastAPI docs](https://fastapi.tiangolo.com/) | API async, BackgroundTasks, OpenAPI | activo | webhook y endpoints (S4+) | 2026-10-08 · ejecutado (paquete 0.143.0); texto de la doc sin releer |
| [Pydantic v2 docs](https://docs.pydantic.dev/latest/) | Schemas, validación, tools | activo | contratos y tools (S5+) | 2026-10-06 · curaduría |
| [Meta WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api) | Canal: webhook, payloads, envío, precios | activo | S4–S16 (ver `whatsapp-cloud-api.md`); precios archivados en `meta-pricing.md` (captura 2026-10-06: Perú standalone desde 1-oct-2026, valores de referencia vía plivo.com/whatsapp/pricing/pe y formbeep.com/whatsapp-api-pricing — confirmar contra el panel Billing del WABA) | 2026-10-06 · curaduría; precios sin validar (panel Billing) |
| [Ollama docs](https://docs.ollama.com) | Modelos locales (DeepSeek/Qwen) | activo | S4+ (ver `deepseek-local.md`) | 2026-10-06 · curaduría |
| [Docker docs](https://docs.docker.com) | Imagen y compose | activo | S14 | 2026-10-06 · curaduría |
| [Trunk-Based Development](https://trunkbaseddevelopment.com) | Flujo git/TBD | activo | S2+ (ver ADR-006) | 2026-10-06 · curaduría |
| [OWASP GenAI Security Project](https://genai.owasp.org) (`genai.owasp.org`) — Top 10 LLM 2026 + **Agent Control Standard (ACS, 2026-09)** + Top 10 for Agentic Applications (ASI) | Seguridad ASI01–ASI10, mitigaciones, estándar de control de agentes | activo (dominio migró de owasp.org) | S12, S15 (ver ADR-009) | 2026-10-06 · curaduría |
| [Anthropic — «Building Effective Agents»](https://www.anthropic.com/research/building-effective-agents) (Schluntz/Zhang, web) | Taxonomía workflows vs agentes: chaining, routing, parallel, orchestrator-workers, evaluator-optimizer; bloques base (retrieval/tools/memory) | activo — enlazar la web, no copiar (© Anthropic) | S5 chaining/paralelización · S10 routing/orchestrator · S12 evaluator/evals | 2026-10-16 · enlace responde (200); contenido sin releer |
| [Anthropic — «How we built our multi-agent research system»](https://www.anthropic.com/engineering/multi-agent-research-system) (web, 13-jun-2025) | Orquestador + subagentes: +90,2 % vs un agente (eval interna), ~15× tokens, mal ajuste con contexto compartido | activo, verificado 2026-10-14 — enlazar, no copiar | S10 (supervisor) · S15 (costo) | 2026-10-14 · abierta; 2026-10-16 enlace responde (200) |
| [`langchain-ai/langgraph-supervisor-py`](https://github.com/langchain-ai/langgraph-supervisor-py) (README, MIT) | Supervisor como librería; el README recomienda hoy el patrón «directly via tools» por el control del contexto | activo, verificado 2026-10-14 | S10 D2 (comparar contra el router propio) | 2026-10-14 · README abierto; 2026-10-16 existe (git) |
| [Cognition — «Don't Build Multi-Agents»](https://cognition.ai/blog/dont-build-multi-agents) (blog, jun-2025) | Crítica al multiagente por pérdida de contexto compartido | **pendiente**: no abrió desde el entorno del asistente (2026-10-14); leer el original antes de citarlo | S10 (criterio de entrada a multiagente) | pendiente · no abrió el 2026-10-14; sin verificar |
| [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) (`github.com/humanlayer/12-factor-agents`, Dex Horthy) | Agentes que duran: prompts propios y versionados, contexto explícito, tools como salidas estructuradas, agentes chicos, control de flujo propio | activo — verificar licencia antes de copiar | S5+ (nodos y tools) · S10 (supervisor) · S12 (evals) | 2026-10-16 · existe (git); licencia sin verificar |
| «Architecture Patterns with Python» — [Cosmic Python](https://www.cosmicpython.com) (Percival & Gregory, `cosmicpython.com`) | Puertos y adaptadores en Python: cómo mantener el núcleo (agentes) limpio de canales y servicios — base de `estandares.md` | activo — verificar licencia antes de copiar código | S4+ (estructura) · S7 (tools como puertos) · S14 | 2026-10-06 · curaduría; licencia sin verificar |
| [`zhanymkanov/fastapi-best-practices`](https://github.com/zhanymkanov/fastapi-best-practices) (guía comunitaria) | Convenciones FastAPI para proyectos medianos: estructura, dependencias, testing | activo — leer, no copiar texto | S4–S5 (estructura de `api/`) | 2026-10-16 · existe (git) |
| **Ruta de fundamentos curada** (`program/01_CURRICULUM/ruta_fundamentos.md`) | Índice de fuentes top para NLP, LLMs, transformers, ML y DL (oficiales/reconocidos), con nivel, autor y mapa semana→tema | activo — solo estas fuentes para fondo teórico | cuando un Issue pida el porqué (S5+) | 2026-10-06 · curaduría |

## Nivel 2 — Repos de ingeniería (leer código real, no copiar sin licencia)

| Repo | Rol | Estado | Consultar cuando | Última verificación |
|---|---|---|---|---|
| [`openai/openai-agents-python`](https://github.com/openai/openai-agents-python) | Handoffs, guardrails de I/O, sessions, tracing | activo 0.x, MIT | S10: patrones a copiar como nodos; **no adoptar** (ADR-010) | 2026-10-16 · existe (git) |
| [`langchain-ai/langgraph`](https://github.com/langchain-ai/langgraph) | Código fuente del motor; ejemplos | activo | bugs de concurrencia, `interrupt()` (S5+) | 2026-10-16 · existe (git) |
| [`microsoft/agent-framework`](https://github.com/microsoft/agent-framework) | Workflows, middleware, time-travel, .NET-first | activo 1.x, MIT | S10: comparación educativa únicamente | 2026-10-16 · existe (git) |
| [`strands-agents/sdk-python`](https://github.com/strands-agents/sdk-python) | Hooks de ciclo de vida, límites de turno/tokens, evals | activo 1.x, Apache-2.0 | S10/S12: ideas de lifecycle y evaluación | 2026-10-16 · existe (git) |
| [`RichmondAlake/agent_harness_course`](https://github.com/RichmondAlake/agent_harness_course) | Approval gates, tiers de permisos, tests de inyección | activo, **sin licencia → prohibido copiar código** | S9/S12: leer patrones; NO correr live (Oracle/MemoRizz) | 2026-10-16 · abierta (README: companion del taller O'Reilly de Alake); sin licencia |
| [`unclebob/swarm-forge`](https://github.com/unclebob/swarm-forge) (SwarmForge, Robert C. Martin) | Coordinación multiagente para el SDLC: roles en secuencia (especificaciones Gherkin → implementación con TDD → limpieza DRY/CRAP → mutation testing → QA, con arquitecto como compuerta final), cada agente en su `git worktree` y una «constitución» de prompts por proyecto; backend configurable por rol | activo; **verificado solo en reseñas secundarias** (README oficial no leído) y **sin archivo de licencia confirmado → leer, no copiar** | S9/S12: patrones de harness para el SDLC con agentes (ADR-009, ADR-010); no se adopta | 2026-10-16 · existe (git); README oficial sin leer; sin licencia confirmada |
| [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) | Servidores MCP de ejemplo | activo | S10–S12 (opcional) | 2026-10-16 · existe (git) |
| [`jackthony/IA-local`](https://github.com/jackthony/IA-local) (lab interno, **MIT**, del monitor) | **Jev**: decisiones tipadas de 1 token con confianza calibrada (logprobs, ~1–2 s en CPU); labs de 11 patrones; CI zero-trust (Actions por SHA, escáner de secretos); compose endurecido; datasets con SHA-256 y licencias | activo | Jev → triage S9, router S10, evals S12; labs → S5–S10; compose/CI → S14/S4 | 2026-10-16 · abierta (LICENSE MIT y README leídos) |
| [`david-lev/pywa`](https://github.com/david-lev/pywa) (**MIT**, 592★) | Framework Python para Cloud API con integración nativa FastAPI (`server=app, webhook_endpoint=...`): verify + parseo de webhooks + envío | activo (2026-10) | Issue #3 (webhook) y #4 (sender): leer su código como referencia, no copiar el framework | 2026-10-16 · existe (git) |
| [`fbsamples/whatsapp-api-examples`](https://github.com/fbsamples/whatsapp-api-examples) (oficial Meta, licencia de muestras) | Ejemplos oficiales de webhook GET (verify_token) y POST (messages/status) | activo | Issue #3: estructura del payload y verificación | 2026-10-16 · existe (git) |

## Nivel 3 — Material educativo (conceptos)

| Fuente | Rol | Estado | Consultar | Última verificación |
|---|---|---|---|---|
| [`Nicolepcx/ai-agents-the-definitive-guide`](https://github.com/Nicolepcx/ai-agents-the-definitive-guide) (CH01–CH12) | Eje conceptual del programa (ver `definitive-guide.md`). Libro O'Reilly publicado el 6-oct-2026 (376 pp, aún sin reseñas que lo validen → lectura guiada, no verdad) | — | semana a semana según matriz | 2026-10-16 · existe (git); libro salió 2026-10-06, sin reseñas |
| «Comprehensive Guide to AI Agent Engineering» (Vasilyev, MIT, 138 pp) | Guía de apoyo de alumnos: loops, context rot, compaction, memoria, tools, HITL, seguridad, evals, costos (ver `agent-engineering-handbook.md`) | — | por partes, según matriz semanal | 2026-10-06 · curaduría |
| [`Nicolepcx/transformers-the-definitive-guide`](https://github.com/Nicolepcx/transformers-the-definitive-guide) (CH01–CH12, Apache-2.0, notebooks Colab) | Consulta **opcional** de alumnos: CH09 agentes y CH11 despliegue de modelos; el stack del proyecto usa Ollama/LangGraph, no transformers | — | cuando un alumno quiera ver qué hay debajo del modelo (S12 evals o curiosidad) | 2026-10-16 · existe (git) |
| [`walkinglabs/learn-harness-engineering`](https://github.com/walkinglabs/learn-harness-engineering) (**MIT**, 19.4k★, sección `docs/es/`) | Harness engineering en **español**: por qué fallan agentes capaces (5 capas), brecha de verificación, Definition of Done verificable | activo | lecture-01 lectura obligatoria en S12; lectures 10–12 en S12/S14; conceptos en S9 (HITL) | 2026-10-16 · existe (git) |
| «Microservices Patterns» (Chris Richardson) + [microservices.io](https://microservices.io) | El libro fue **liberado por el autor** (2026-10) → ya es referenciable. Patrones traducibles al monolito modular (schema por tenant, API gateway, transacciones) | activo, gratuito | S10 modularidad — lectura opcional de alumnos; microservices.io como resumen rápido | 2026-10-06 · curaduría |
| OpenTelemetry GenAI semantic conventions ([`open-telemetry/semantic-conventions-genai`](https://github.com/open-telemetry/semantic-conventions-genai), Apache-2.0) | Estándar de trazas/métricas/eventos para LLM, agentes y MCP (2026→2027) | activo | S8 instrumentación + S12 evals + S15 FinOps (ver `observabilidad-costos.md`) | 2026-10-16 · existe (git) |
| [Langfuse docs](https://langfuse.com/docs) + pricing (verificado 2026-10-06) | Telemetría/evals S8: **self-host gratis** (Docker en la M5) o cloud Hobby gratis (50k units, 2 users, 30 días) · Core $29/mes · Pro $199/mes | activo | S8 telemetría · S12 evals (ver `observabilidad-costos.md`) | 2026-10-06 · precios verificados |
| Kapso (BSP dev-first) + n8n — comparativa B/B/I en `kapso-n8n.md` | Capas no-diferenciadoras: canal WhatsApp (plan B) y glue operativo | activo (precios verificados 2026-10-06) | S10 decisión B/B/I | 2026-10-06 · precios verificados |
| Taller O'Reilly "Harness Engineering for Long-Running Agent Skills" (10-nov, Koenigstein) | Contenido avanzado (skills versionadas, repair loops). Intermedio-avanzado, requiere OpenRouter + Langfuse/LangSmith; sin precio suelto (solo suscripción O'Reilly USD 49/mes); repo "to come" | — | **No comprar para el monitor.** Si se asiste (trial): preparar Python 3.12 + OpenRouter + Langfuse self-host y lectura previa CH05/CH08/CH09/CH10 del libro. Autora verificada: Nicole Koenigstein (el "análisis forense" del doc de Agentes describe a Alake, no este evento) | 2026-10-06 · curaduría |

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
6. **Frescura antes de enseñar:** al preparar cada semana del plan, las fuentes que usará esa semana se re-verifican (idealmente **ejecutando** el ejemplo con las versiones de `stack-versiones.md`) y se actualiza su fila de «Última verificación». Una fuente sin fecha o en `pendiente` no se cita como autoridad. Las APIs de LangChain/LangGraph cambian entre series mayores: un tutorial o curso anterior a la serie 1.x vale como concepto, no como código.
