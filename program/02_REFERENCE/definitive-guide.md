# AI Agents — The Definitive Guide (referencia principal)

- **Repo:** https://github.com/Nicolepcx/ai-agents-the-definitive-guide
- **Libro:** O'Reilly — AI Agents: The Definitive Guide (B0GTYKTZHG)
- **Estructura:** carpetas `CH01`…`CH12` con notebooks Colab por capítulo.
- **Regla de uso:** se estudia **por capítulo según la semana**; no se clona entero en contexto. Los notebooks se corren en Colab; el código ya está en ellos.

## Matriz capítulo → semana

| Cap. | Título | Prioridad | Semana |
|---|---|---|---|
| CH01 | From LLMs to Agents: The Foundational Blueprint | Alta | S4 |
| CH02 | Architectures and Patterns (CoT, ReAct, HITL, Hierarchical, Swarms) | Alta | S5–S7 |
| CH03 | Advanced Planning, Reasoning, and Scalable Execution (ART+RULER, TreeQuest) | Media | S10 |
| CH04 | Models Behind the Agents (Supervisor Agent Team) | Alta | S10 |
| CH05 | Prototypes to Production: Contracts, Tools, Reliable Execution (MCP, Pydantic) | Alta | S7–S9 |
| CH06 | Secure Execution and Tool Governance (A2A+MCP, E2B) | Alta | S12 |
| CH07 | Deploying Agents in Real Products (hardening, inference backends, fallback) | Alta | S14–S15 |
| CH08 | Foundational Evaluation & Observation (OWASP ASI 2026, eval harness) | Alta | S12 |
| CH09 | Customized/Advanced Evaluation (AgentVista, Langfuse, LangSmith) | Alta | S12–S13 |
| CH10 | Agent Memory: Persistence (LangGraph memory, topologies) | Alta | S5, S9–S10 |
| CH11 | From Compute to Cost (cost estimator, memory footprint/GPU) | Media | S13–S14 |
| CH12 | Threat Modeling for AI Agents (LlamaFirewall) | Alta | S12, S15 |

## Mapeo curado (usar solo esto)

- S4 → CH01 · S5 → CH02 (CoT/ReAct) + CH10 (memoria) · S6 → CH02 (HITL) 
- S7–S9 → CH05 (tools, reliability) · S10 → CH04 (supervisor) + CH03 · 
- S11 → CH10 (memoria avanzada) · S12 → CH06, CH08, CH09, CH12 · S13 → CH09, CH11 · 
- S14–S15 → CH07, CH11, CH12 · S16 → repaso CH07–CH09 para defensa.
