# Fuentes y referencias

Dos grupos, para no confundir de dónde sale cada cosa:
1. **Con las que nació el proyecto** (materiales y cursos del monitor).
2. **Referencias técnicas del programa** (curaduría del [`source_map.md`](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/source_map.md): docs oficiales, libros y repos de ingeniería).

Orden de autoridad: **doc oficial/spec > código reproducible > libro/curso > paper > un LLM**. Se enlaza, no se copia. Máx. ~20 fuentes activas: si el monitor agrega una, se degrada otra.

> 💬 **Cómo se practican:** cada semana hay una **Lectura guiada** en [Discusiones](Discusiones) con preguntas sobre estas fuentes. Responde con tus palabras y cita la fuente (archivo, doc oficial o URL).

## 1 · Con las que nació el proyecto (materiales del monitor)
| Fuente | Qué es | Dónde se usa |
|---|---|---|
| Curso *LangChain, LangGraph y Agentes IA* — Santiago Hernández (Udemy, ES) | Columna vertebral desde S5: checkpointer, interrupt, supervisor, RAG; ejercicios y proyecto SOC multiagente como referencia | S5–S10 ([veredicto y mapeo](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/cursos_de_refuerzo.md)) |
| Cursos *AI Engineer Bootcamp* e *Intro to AI Agents* — 365 Careers | Nivelación y panorama conceptual | S1–S4, apoyo |
| Video *WhatsApp AI Support Agent with RAG & Memory* — Dani Fuyà (YouTube) | Stack casi idéntico al del proyecto | S4 (webhook y envío) |
| Video *Domina la IA Local* — MoureDev (YouTube, ES) y docs de Ollama | Modelos locales con Ollama | S4+ ([deepseek-local](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/deepseek-local.md)) |
| [jackthony/IA-local](https://github.com/jackthony/IA-local) | Lab propio del monitor: decisiones tipadas con confianza calibrada (Jev) y CI zero-trust | S10+ ([jev-pattern](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/jev-pattern.md)) |
| Materiales del negocio Hola Mujer: catálogo y reglas (Excel operativo) y conversaciones de la era ManyChat/n8n (corpus anonimizado, Ley 29733) | El negocio real que el bot debe atender; de ahí salen precios, tono y corpus | [hola-mujer.md](https://github.com/jackthony/ai-business-assistant/blob/main/program/04_DOMAIN/hola-mujer.md) · [corpus sintético](https://github.com/jackthony/ai-business-assistant/blob/main/data/conversaciones/INDICE.md) |
| Kapso y n8n (comparativa) | Canal de WhatsApp (plan B) y glue operativo | [kapso-n8n.md](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/kapso-n8n.md) |
| Plan Maestro SENATI 2026 e Informe FPE (CNIU-108) | Evaluación y formato institucional | [plan](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/16_week_plan.md) |

> ¿Usaste otra fuente para crear el proyecto y no la ves aquí? Se agrega con su «cuándo consultar», según la regla del `source_map`.

## 2 · Referencias técnicas del programa
| Fuente | Qué aporta | Úsala cuando |
|---|---|---|
| [Anthropic — «Building Effective Agents»](https://www.anthropic.com/engineering/building-effective-agents) | Empezar simple: workflow antes que agente; patrones composables (chaining, routing, evaluator) | S5, S10, S12 |
| [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) (Dex Horthy) | Agentes que duran: prompts propios y versionados, contexto explícito, tools como salidas estructuradas | S5–S7 |
| [Cosmic Python](https://www.cosmicpython.com/) — *Architecture Patterns with Python* | Puertos y adaptadores: núcleo de agentes limpio de canales y servicios (base de [`estandares.md`](https://github.com/jackthony/ai-business-assistant/blob/main/program/03_ARCHITECTURE/estandares.md)) | todas las semanas de código |
| [OWASP GenAI Security Project](https://genai.owasp.org/) | Top 10 LLM, Top 10 Agentic Applications: seguridad de agentes | S9, S12 |
| [LangGraph (docs)](https://langchain-ai.github.io/langgraph/) y [código](https://github.com/langchain-ai/langgraph) | Estado, grafo, checkpointers, interrupt | S5+ |
| [AI Agents: The Definitive Guide](https://github.com/Nicolepcx/ai-agents-the-definitive-guide) | Eje conceptual por capítulos (ver [`definitive-guide.md`](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/definitive-guide.md)); lectura guiada, no verdad | todas |
| «Comprehensive Guide to AI Agent Engineering» (Vasilyev) | Loops, context rot, memoria, tools, HITL, seguridad, evals, costos (ver [handbook](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/agent-engineering-handbook.md)) | por parte, según tu Issue |
| [Learn Harness Engineering](https://github.com/walkinglabs/learn-harness-engineering) (en español) | Por qué fallan agentes capaces; Definition of Done verificable | S9, S12, S14 |
| [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices) | Estructura y convenciones FastAPI | S4–S5 |
| [Microservices Patterns](https://microservices.io/) | Patrones traducibles al monolito modular multitenant | S10 |
| [jackthony/IA-local](https://github.com/jackthony/IA-local) | Lab del monitor: decisiones tipadas con confianza calibrada (Jev), CI zero-trust ([`jev-pattern.md`](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/jev-pattern.md)) | S10+ |
| [Trunk-Based Development](https://trunkbaseddevelopment.com/) | El flujo git del programa ([ADR-006](https://github.com/jackthony/ai-business-assistant/blob/main/program/03_ARCHITECTURE/decisions/)) | desde S2 |

## Fundamentos (para el *porqué*)
[`ruta_fundamentos.md`](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/ruta_fundamentos.md): 5 niveles con fuentes top (3Blue1Brown, Karpathy, d2l.ai, fast.ai, Jurafsky & Martin, Hugging Face Course, Raschka, Huyen, Ng…). **No es tarea extra**: es tu recurso cuando el Issue pida profundidad. Cursos opcionales: [`cursos_de_refuerzo.md`](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/cursos_de_refuerzo.md).

## Referencias del proyecto (leer antes de preguntar)
[LangGraph](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/langgraph.md) · [DeepSeek local](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/deepseek-local.md) · [WhatsApp Cloud API](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/whatsapp-cloud-api.md) · [Precios Meta](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/meta-pricing.md) · [Proveedores de WhatsApp](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/proveedores-whatsapp.md) (borrador) · [Versiones y herramientas](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/stack-versiones.md) · [Observabilidad y costos](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/observabilidad-costos.md) · [Hola Mujer (negocio)](https://github.com/jackthony/ai-business-assistant/blob/main/program/04_DOMAIN/hola-mujer.md)

## Kit de rescate: síntoma → fuente
| Síntoma | Ve a |
|---|---|
| El bot olvida la conversación | LangGraph checkpointers (`thread_id` = teléfono) |
| Tool con argumentos inválidos | Pydantic v2 + capítulo de tools de la guía |
| Prompt injection / goal hijacking | OWASP + [ADR-009](https://github.com/jackthony/ai-business-assistant/blob/main/program/03_ARCHITECTURE/decisions/) |
| Latencia o costo alto | [`roi_metrics.md`](https://github.com/jackthony/ai-business-assistant/blob/main/program/00_PROJECT/roi_metrics.md) |
| Duda de framework | ADR-002 y ADR-010 (no se migra sin ADR nuevo) |

Tabla completa: sección «Kit de rescate» de [`source_map.md`](https://github.com/jackthony/ai-business-assistant/blob/main/program/02_REFERENCE/source_map.md).
