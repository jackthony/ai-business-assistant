# Comprehensive Guide to AI Agent Engineering (guía de apoyo)

- **Autor:** Dmitriy Vasilyev · marzo 2026 · 138 pp · licencia **MIT**
- **Repo:** https://github.com/vasilyevdm/ai-agent-handbook (README + `.md` + `.pdf`)
- **PDF para alumnos:** copia en Google Drive → `02_ALUMNOS/` (lectura en celular)
- **Rol:** fuente de apoyo (nivel 3), **no canónica**. Se usa por partes, según la semana.

## Mapa parte → semana

| Parte | Tema | Semana |
|---|---|---|
| I. Foundations | qué es un agente, taxonomía, espectro | S4 |
| II. The Agent Loop | ReAct, variantes, terminación, errores | S5 |
| III. System Prompts | anatomía, ensamblado, anti-patrones | S5–S6 |
| IV/IV-B. Contexto, compactación y Context Rot | ventana, compactación, regla 40-60% | S5+, S13 |
| V. Memory Systems | jerarquía de memoria, episódica, user modeling | S5, S9–S10 |
| VI. Tool Architecture | tools, MCP, JIT loading, tool sprawl | S7 |
| VII. Sub-Agent Orchestration | por qué multiagente, topologías | S10 |
| VIII. Planning & Reasoning | plan/act, reflexión | S10 |
| IX. Human-in-the-Loop | modelos de permiso, aprobación, escalado | S9 |
| X. State Management | checkpoints, ejecución durable | S5, S14 |
| XI. Security | sandbox, inyección de prompts, credenciales | S12 |
| XII. Testing & Evaluation | benchmarks, testing, evals en producción | S12 |
| XIII. Deployment & Operations | deploy, optimización de costos, observabilidad | S13–S15 |
| XIV. Synthesis | arquitectura de referencia, 25 mandamientos, framework de decisión | S16 y lectura del monitor |

## Takeaways que coinciden con nuestros ADRs

1. "Start with one agent" → **ADR-007** (agente único primero).
2. "Use state machines for multi-agent… LangGraph" → **ADR-002**.
3. "Checkpoint everything. If you can't resume from a crash, you're not production-ready" → **ADR-005**.
4. "Fight context rot from day one… the 40-60% rule" → chats largos de WhatsApp (compactación).
5. "Human-in-the-loop is a feature, not a limitation" → **ADR-009**.
6. "Track costs per task" → **FinOps** (`program/00_PROJECT/roi_metrics.md`).

## Reglas de uso

- Lectura por partes, nunca completa dentro de un prompt.
- MIT: se puede compartir citando autor y repo; no se copia texto al repo (se referencia).
- Su "Decision Framework" es insumo; **no pisa los ADRs** del proyecto.
