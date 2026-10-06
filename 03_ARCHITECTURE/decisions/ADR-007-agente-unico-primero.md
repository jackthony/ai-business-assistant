# ADR-007: Un agente sólido antes de multiagente

- **Fecha:** 2026-10-06
- **Estado:** aceptada

## Contexto

El plan v1 introduce supervisor y multiagente pronto (S9–S10) tras un solo agente aún frágil.

## Problema

¿Cuándo pasar a multiagente?

## Opciones

1. Multiagente temprano (varios especialistas desde el inicio).
2. Agente único bien instrumentado primero; multiagente cuando el dominio lo exija.
3. Multiagente desde el día 1 con LangGraph puro.

## Decisión

Opción 2. Primero un agente con RAG y tools confiables (S4–S8, HITO 1), con observabilidad y pruebas; el supervisor/subgrafos llegan cuando haya métricas que justifiquen dividir responsabilidades.

## Consecuencias

- La re-secuencia v2 revisará las semanas de multiagente para que no llegue antes de tiempo.
- Evalúa el costo/beneficio: más agentes = más latencia y puntos de fallo (CH11).
