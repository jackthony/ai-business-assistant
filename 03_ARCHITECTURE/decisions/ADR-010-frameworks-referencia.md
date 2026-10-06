# ADR-010: Ecosistema de frameworks — LangGraph se queda

- **Fecha:** 2026-10-06
- **Estado:** aceptada

## Contexto

Ecosistema verificado 2026-10: OpenAI Agents SDK (0.x, MIT: handoffs, guardrails I/O, sessions, tracing), Microsoft Agent Framework (1.x, MIT, sucesor de AutoGen/Semantic Kernel: workflows, middleware, time-travel, .NET-first), Strands Agents (1.x, Apache-2.0: hooks de ciclo de vida, límites de turno/tokens, evals), más CrewAI/PydanticAI/Google ADK. La comparativa de Langfuse (2026) confirma que no existe framework único.

## Decisión

- **Motor del proyecto: LangGraph** (ADR-002 vigente): control fino de estado, checkpointers, `interrupt()` y portabilidad total a modelos locales (Ollama).
- Alternativas = **referencias de patrones, nunca migración**: copiar handoffs/guardrails/sessions (OpenAI SDK) y hooks/lifecycle (Strands) como nodos o tools propias.
- Una sola clase de panorama en S10 (guion: comparativa de Langfuse). No se enseña ningún framework alternativo a fondo.
- Cualquier migración futura exige un **ADR nuevo** con evidencia de que LangGraph no cumple un requisito concreto.

## Consecuencias

- Se evita el "framework hopping" (una de las causas de cancelación de proyectos agentic según Gartner: >40% para fin-2027).
- El tiempo de práctica se dedica al producto, no a comparar SDKs.
