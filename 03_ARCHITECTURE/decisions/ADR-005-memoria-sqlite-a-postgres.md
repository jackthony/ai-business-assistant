# ADR-005: Memoria — SqliteSaver en dev, PostgresSaver en prod

- **Fecha:** 2026-10-06
- **Estado:** aceptada

## Contexto

LangGraph necesita persistir el estado de cada conversación (thread_id = teléfono).

## Problema

¿Dónde guardar checkpoints en cada etapa?

## Opciones

1. SqliteSaver desde el inicio y para siempre.
2. PostgresSaver desde el inicio.
3. SqliteSaver en desarrollo → PostgresSaver en producción.

## Decisión

Opción 3. Sqlite permite arrancar sin infraestructura (S5); Postgres entra en S14 con Docker y soporta concurrencia real.

## Consecuencias

- La migración (#31) es un Issue explícito del plan: mismo checkpointer API, distinto backend.
- Prohibido guardar datos personales reales en la DB de desarrollo (fixtures anonimizados).
