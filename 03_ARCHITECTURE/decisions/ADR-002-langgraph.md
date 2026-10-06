# ADR-002: LangGraph como motor de orquestación

- **Fecha:** 2026-10-06
- **Estado:** aceptada

## Contexto

El asistente tiene flujos con estado: informar → agendar → validar pago → derivar a humano.

## Problema

¿Cómo modelar la conversación como máquina de estados persistente y auditable?

## Opciones

1. LangGraph (grafos con estado, checkpointers, interrupt).
2. Scripts con `while` + if/else.
3. CrewAI / AutoGen (orquestación multi-agente de alto nivel).

## Decisión

LangGraph. Es el patrón estándar para FSM conversacionales con memoria, `interrupt()` para HITL y subgrafos por especialista; el stack de la guía O'Reilly (CH02, CH05, CH10) lo usa de punta a punta.

## Consecuencias

- Estado explícito (`AgentState`) y trazabilidad por nodo.
- Persistencia intercambiable: SqliteSaver (dev) → PostgresSaver (prod).
- Prohibido introducir otro framework de agentes sin un ADR nuevo.
