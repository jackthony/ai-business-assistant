# LangGraph — conceptos y uso

- **Docs:** https://langchain-ai.github.io/langgraph/
- **Se usa:** S5–S14 (grafo principal, subgrafos, memoria, interrupt).

## Conceptos que dominar

- `StateGraph(AgentState)` + nodos + edges condicionales.
- `AgentState` con `Annotated[list, add_messages]`, `phone` (thread_id), `tenant`, `intent`, `status`.
- Checkpointers: `SqliteSaver` (dev, S5) → `PostgresSaver` (prod, S14).
- `interrupt()` para Human-in-the-Loop (S9): pausa asíncrona + reanudación.
- Subgrafos por agente (info, booking, checkout, safety) y supervisor router (S10).
- `thread_id` = número de teléfono del usuario (memoria por conversación).

## Reglas del proyecto

- Un nodo = una responsabilidad. Si el prompt crece, se divide.
- Las herramientas se definen con `@tool` + Pydantic (S7); nada de side effects ocultos.
- Todo grafo nuevo se prueba con pytest antes del PR.
