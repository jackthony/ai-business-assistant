# SOURCE_MAP — base de conocimiento del proyecto (curaduría verificada 2026-10-06)

> Este es el mapa de qué se consulta, cuándo y con qué autoridad. No es una lista de links: es la política de context que usan el monitor, los practicantes y DeepSeek.
>
> **Orden de autoridad:** doc oficial/spec > código reproducible (repo real) > libro/curso > paper > afirmación de un LLM. Un LLM nunca es autoridad; toda afirmación técnica se verifica contra fuente primaria.

## Nivel 1 — Autoridad técnica (docs oficiales)

| Fuente | Rol | Estado | Consultar cuando |
|---|---|---|---|
| LangGraph docs | Motor del grafo, checkpointers, interrupt | activo | diseño de estado, memoria, HITL (S5+) |
| OpenAI Agents SDK (docs) | Abstracciones agents/tools/handoffs | activo (0.x, MIT) | entender handoffs en S10 (no migrar: ADR-002/010) |
| MCP spec (`modelcontextprotocol.io`) | Protocolo tools/context | activo | desacoplar herramientas (S10+, opcional) |
| FastAPI docs | API async, BackgroundTasks, OpenAPI | activo | webhook y endpoints (S4+) |
| Pydantic v2 docs | Schemas, validación, tools | activo | contratos y tools (S5+) |
| Meta WhatsApp Cloud API | Canal: webhook, payloads, envío, precios | activo | S4–S16 (ver `whatsapp-cloud-api.md`) |
| Ollama docs | Modelos locales (DeepSeek/Qwen) | activo | S4+ (ver `deepseek-local.md`) |
| Docker docs | Imagen y compose | activo | S14 |
| Trunk-Based Development | Flujo git/TBD | activo | S2+ (ver ADR-006) |
| OWASP Top 10 Agentic 2026 + GenAI LLM Top 10 2026 | Seguridad ASI01–ASI10, mitigaciones | activo | S12, S15 (ver ADR-009) |

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

## Nivel 3 — Material educativo (conceptos)

| Fuente | Rol | Consultar |
|---|---|---|
| `Nicolepcx/ai-agents-the-definitive-guide` (CH01–CH12) | Eje conceptual del programa (ver `definitive-guide.md`). Libro O'Reilly publicado el 6-oct-2026 (376 pp, aún sin reseñas que lo validen → lectura guiada, no verdad) | semana a semana según matriz |
| «Comprehensive Guide to AI Agent Engineering» (Vasilyev, MIT, 138 pp) | Guía de apoyo de alumnos: loops, context rot, compaction, memoria, tools, HITL, seguridad, evals, costos (ver `agent-engineering-handbook.md`) | por partes, según matriz semanal |
| Langfuse — comparativa de frameworks (actualizada 2026) | Guion de la clase de panorama S10 | una sola clase, 20–30 min |
| Taller O'Reilly "Harness Engineering for Long-Running Agent Skills" (10-nov, Koenigstein) | Contenido avanzado (skills versionadas, repair loops). Intermedio-avanzado, requiere OpenRouter + Langfuse/LangSmith; sin precio suelto (solo suscripción O'Reilly USD 49/mes); repo "to come" | **No comprar para el monitor.** Si hay curiosidad: trial gratuito y ver 2 h |

## Nivel 4 — Investigación (anexos opcionales S12+, jamás currículo)

- AgensFlow (arXiv:2605.27466, Koenigstein, preprint sin peer review, resultados auto-reportados).
- Benchmarks de evaluación de agentes (AgentVista, AHE, etc.) y papers de harness: solo lectura para el mes 3 si un practicante muestra interés. No se cargan en contexto de DeepSeek.
- `KevinKantule/cofounder-agi` (revisado 2026-10-06, **sin licencia → no copiar código**): ideas aprovechables (loop coder→reviewer→ejecución→corrección; auditoría de modelos reales por proveedor) y **anti-ejemplo de RAG falso** (embeddings = ruido por hash inestable) usado como caso de estudio en S6.

## Nivel 5 — Cursos Udemy (opcional para practicantes, verificado 2026-10)

| Curso | Datos | Veredicto |
|---|---|---|
| 1. LangChain, LangGraph y Agentes IA (Santiago Hernández) | 9 secciones · 149 lecciones · 17h50m · 4.7★ (1.208) · español · actualizado sep-2026 | **Opción #1.** Único con LangGraph profundo (checkpointer, interrupt/HITL, supervisor) + Chroma/FAISS locales + proyecto FastAPI. Gap: sin Ollama ni WhatsApp |
| 2. The AI Engineer Course 2026 (365 Careers) | 77 secciones · 445 lecciones · 29h46m · 4.5★ (25.9k) · inglés · actualizado ago-2026 | Complemento para nivelar: módulo LangGraph real (sin interrupt) + Chroma local/Pinecone. Reseñas negativas: desactualización y poca profundidad |
| 3. Intro to AI Agents and Agentic AI (365 Careers) | 2h11m · 4.5★ (90k) · inglés | Contexto de negocio (2 h): conceptual, n8n, menciona frameworks sin código de grafo |

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
