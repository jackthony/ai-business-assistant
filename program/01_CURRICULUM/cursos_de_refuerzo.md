# Cursos de refuerzo (opcional para practicantes)

> Nunca son fuente de verdad; si contradicen una doc oficial, gana la doc. Comprar solo en oferta.

## Cursos ya comprados — veredicto 2026-10

| Curso | Uso en el programa | Veredicto |
|---|---|---|
| 1. LangChain, LangGraph y Agentes IA — Santiago Hernández (ES, 17h50m, 4.7★) | Columna vertebral desde S5 | Único con LangGraph profundo (checkpointer, interrupt, supervisor) + Chroma/FAISS locales + proyecto FastAPI. Gap: sin Ollama/WhatsApp |
| 2. AI Engineer Bootcamp — 365 Careers (EN, 29h46m, 4.5★) | Nivelación S1–S4 y fundamentos | Módulo LangGraph real (sin interrupt); poca profundidad por tema; código a veces desactualizado |
| 3. Intro to AI Agents — 365 Careers (EN, 2h11m) | Contexto conceptual | Solo panorama; menciona frameworks, no enseña grafos |

## Gaps que los 3 cursos no cubren

1. **WhatsApp Cloud API con Python** — gratis: docs Meta + video "WhatsApp AI Support Agent with RAG & Memory" (Dani Fuyà, EN, 34 min, stack casi idéntico al nuestro) + plantilla `botdev-community/whatsapp-bot-starter` (FastAPI). Curso opcional en oferta (~$10): "Chatbot WhatsApp API, Python" (Yudner Paredes, ES, 2.5h) o AnderCode (ES, 4h).
2. **Ollama / LLM local** — gratis: docs Ollama + docs ChatOllama + video MoureDev "Domina la IA Local" (ES, 1h12). Curso opcional en oferta (~$10–15): "IA generativa en local con Ollama" (Apasoft, ES, 12.5h; ver primero su clase gratis de 54 min).

**Recomendación:** máximo 1–2 compras extra (~$20–30) y solo si hace falta. Con los 3 comprados + docs oficiales + este repo se cubre el programa.

## Orden sugerido por fase

- **S1–S3:** nada de IA; Java/Git (curso 2 solo como apoyo individual).
- **S4:** WhatsApp + FastAPI (docs Meta + video Fuyà).
- **S5–S6:** curso 1 → secciones LangGraph y RAG; handbook Partes I–V.
- **S7–S8:** curso 1 → agentes y herramientas; handbook Parte VI.
- **S9–S11:** handbook Partes VII–IX; repaso de HITL/checkpoints del curso 1.
- **S12:** handbook Partes XI–XII (seguridad y evals).
- **S13–S16:** handbook Parte XIII; proyectos finales del curso 1.

## Material descargado del curso 1 (2026-10-06)

- Ejercicios de Gmail (Tema 6: `agente_ia_langchain*.py`) y **proyecto SOC multiagente** (`soc_multiagent.zip`: supervisor, agentes, dashboard, webhook) — referencia directa para S7–S10.
- `sistema_multiagente.py` usa la lib `langgraph-supervisor`; compararla en S10 con el router propio (ADR-002).
- `agente_ia_langgraph.py` (Gmail con `create_react_agent` + `MemorySaver` + `thread_id`) → espejo exacto del patrón de S5 (#04–#06).
- `herramientas*.py` (Tool de PythonREPL, `@tool`, `bind_tools` + `tool_calls`, `content_and_artifact`) → S7 #11; el patrón `content_and_artifact` (datos por fuera del contexto) es una buena práctica.
- SOC `prompt_supervisor.txt` (flujo de 3 pasos impuesto por texto: "NO volver a un agente ya ejecutado", "máximo 3 delegaciones") → **contraste en S10 #19**: imponer la FSM por prompt es frágil; en LangGraph la estructura vive en el grafo/código (misma lección de IA-local).
- `app (2).py` (chatbot multi-usuario con memoria por categorías: personal/profesional/preferencias/tareas/hechos) → S5 D3 y S13 (memoria del usuario).
- `peticion_powershell.txt` → ejemplo real de pruebas de webhook (GET /health, POST payload) útil para S4 D2–D3.
- Nota: los ejemplos del curso usan `gpt-4o`/OpenAI → adaptar a `ChatOllama` (DeepSeek local) al seguirlos.
- **Material local ordenado (fuera de git):** `ciclo-3-pilar-alan-josue/material-langchain/` — 4 carpetas (gmail, herramientas, SOC, memoria) con `LEEME.md` que mapea cada archivo a la sesión del plan.
