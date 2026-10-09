# Patrones de arquitectura (microservicios y sistemas distribuidos) aplicados a este proyecto

> Es el vocabulario de un arquitecto de soluciones / de IA. **No vamos a partir el bot en microservicios**: es un **monolito modular multitenant** (ADR-001, ADR-010). Pero los *problemas* que esos patrones resuelven aparecen igual —mensajes duplicados, llamadas que fallan, operaciones en dos sitios, negocios que no deben mezclarse— y sus soluciones se traducen casi 1 a 1. Fuente: *Microservices Patterns* (Chris Richardson, liberado por el autor) y `microservices.io` como resumen rápido (`source_map.md`).

## Cuáles sí, dónde y con qué ejemplo

| Patrón (nombre del catálogo) | Problema real del proyecto | Dónde se aplica | Ejemplo con tests |
|---|---|---|---|
| **API Gateway / Integration Hub** | Un solo punto de entrada que valida y enruta | FastAPI como hub (ADR-001), S4 #2 | `/health` de #2 |
| **Anti-corruption layer / Adapter** | Que lo de Meta no contamine el núcleo del agente | `src/channels/whatsapp/` ↔ `InboundEvent` (ADR-011), S4 #3–#4 | `webhook-meta/` |
| **Idempotent consumer** | Meta reenvía el mismo mensaje; el usuario reenvía; el sender reintenta | Descartar `wamid` repetidos (S4 #3) y `request_id` en citas (S7 #12) | `s7-tools-y-citas/reserva_idempotente.py` |
| **Retry + timeout (+ circuit breaker)** | Meta o la red fallan a ratos | Sender (S4 #4); en S13–S14 añadir *circuit breaker* si falla de seguido | `sender-httpx/` |
| **Health check API** | Saber si el servicio vive y si sus dependencias responden | `/health` (S4), ampliado con dependencias en S14 | `/health` de #2 |
| **Distributed tracing / observabilidad** | Ver por dónde pasó cada conversación y cuánto costó | Langfuse + OpenTelemetry GenAI (S8, `observabilidad-costos.md`) | — (S8) |
| **Saga (con compensación)** | Agendar + cobrar son dos efectos sin transacción común | Cita + pago Yape/Plin (S10 #15) | `s10-router-saga-tenant/saga_agendar_pago.py` |
| **Tenant isolation (database/schema-per-tenant)** | Hola Mujer y NeuraCode en el mismo núcleo sin mezclarse | Colección RAG y memoria por tenant (S10 #20, ASI06) | `s10-router-saga-tenant/aislamiento_tenant.py` |
| **Externalized configuration** | Prompts, tools y namespaces por negocio sin tocar código | `configs/{tenant}/` (S10 #20) | `aislamiento_tenant.py` |
| **Transactional outbox** | Guardar la cita y avisar (recordatorio 24 h/2 h) sin perder uno de los dos | Recordatorios (S13): guardar el evento en la misma escritura que la cita | — (S13) |
| **Strangler fig** | Reemplazar ManyChat/n8n sin apagarlos de golpe | Migración gradual del canal (roadmap) | — |

## Cuáles no (todavía) y por qué

- **Un servicio por agente / event bus / CQRS / event sourcing:** complejidad sin necesidad con 3 practicantes y un negocio; ADR-007 manda *agente único primero*. Si en S10+ algo crece, se extrae con el patrón *strangler*, no antes.
- **Service mesh, sidecar, service discovery:** son para decenas de servicios. Aquí es un contenedor.

## Cómo usarlo en tu PR (para tu informe FPE)

Cuando uses un patrón, nómbralo y di **qué falla sin él**. Ejemplo: "*Idempotent consumer*: sin él, si Meta reenvía el mensaje, la clienta recibe dos respuestas y se crean dos citas". Esa frase vale más que el código.

**Pregunta de comprensión transversal:** de la tabla de arriba, elige dos patrones y explica con tus palabras (1) qué pasaría en producción sin ellos y (2) por qué los aplicamos dentro de un monolito en lugar de separar servicios.
