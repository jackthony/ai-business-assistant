# Build / Buy / Integrate — Kapso vs n8n (referencia para la decisión S10)

> Contexto (ADR-011): la capa de agentes (FastAPI + LangGraph + RAG) es **el producto**; el canal es un adapter. Este doc compara las 2 opciones de compra/integración candidatas para las **capas no diferenciadoras**: el canal WhatsApp y el glue operativo. Decisión formal: S10 (revisión B/B/I del plan). Captura: 2026-10-06.

## Kapso — BSP "WhatsApp for developers" (verificado)

- Qué es: Business Solution Provider (BSP) que envuelve la WhatsApp Cloud API con **API + CLI + MCP + agent skills**, sandbox numbers, connection links (multi-tenant) y human handoff.
- Precios (Meta fees aparte, **sin markup**): Free $0 (2.000 msgs/mes, 1 número, sandbox) · Pro **$25/mes** (100.000 msgs, 3 números) · Platform $299/mes (1M msgs, 50 números) · Enterprise custom.
- Encaja si: queremos salir a producción rápido SIN administrar WABA/webhook/templates a mano, y sin depender de un BSP con markup (Wati +20%, Twilio $0,005/msg, etc.).
- No encaja si: queremos control 100% del pipeline (ADR-002 LangGraph) — Kapso da canal + inbox, no los agentes.
- Ficha: https://kapso.com · docs.kapso.ai · pricing verificado 2026-10-06.

## n8n — automatización de workflows

- Qué es: orquestador low-code (fair-code, Sustainable Use License). **Self-host gratis** (Docker en la M5) o cloud de pago (~$24/mes tier starter — verificar al momento de decidir). +400 integraciones; tiene nodos WhatsApp/LangChain.
- Encaja si: necesitamos glue operativo NO-diferenciador (ej.: sincronizar Sheets→CRM, alertas internas, reportes del monitor) sin codear cada integración.
- No encaja si: lo usamos como "cerebro" del bot — pierde LangGraph (checkpointers, interrupt, evals) y rompe ADR-002/ADR-010. El grafo de conversación es nuestro.

## Recomendación preliminar (para validar en S10)

| Capa | Build (nosotros) | Integrate (API directa) | Buy (SaaS) |
|---|---|---|---|
| Agentes + RAG + memoria | ✅ ADR-002/004/006 | — | — |
| Canal WhatsApp | ✅ Cloud API directa (ya diseñado en S4) | — | Kapso como **plan B** si la gestión #16 se atasca |
| Telemetría (S8) | Langfuse **self-host** en la M5 (gratis, open source; cloud Hobby gratis 50k units) | — | Langfuse Cloud solo si el volumen lo justifica |
| Glue operativo interno | scripts Python | — | n8n self-host solo para lo no-diferenciador |

Regla: **nada de lo anterior reemplaza el motor del proyecto** (LangGraph + DeepSeek local). Kapso/n8n entran solo donde compran tiempo sin ceder el core.
