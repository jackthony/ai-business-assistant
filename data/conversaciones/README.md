# Corpus de conversaciones reales (Hola Mujer) — para aprender a atender como humano

> Este es **el activo del agente**: las conversaciones reales de la era ManyChat/n8n. De aquí salen los few-shot (S7), el prompt (S5–S6), las objeciones del RAG (S6) y los datasets de evals (S12).
>
> **Reglas duras:** todo **anonimizado** — sin teléfonos reales (usar `+51 9XX-XXX-XXX` o IDs sintéticos), sin nombres reales (reemplazar por `CLIENTE_01`…), sin datos clínicos, sin DNI ni comprobantes. El dueño del negocio autoriza su uso en este repo (negocio propio).

## Formato (JSONL, un mensaje por línea)

```jsonl
{"conversacion_id": "conv_0001", "turno": 1, "rol": "user", "texto": "Hola, quiero saber precios de lunares", "ts": "2026-07-14T10:02:00-05:00", "canal": "manychat"}
{"conversacion_id": "conv_0001", "turno": 2, "rol": "assistant", "texto": "¡Hola! Gracias por escribirnos. Los precios van desde S/ 24.99. ¿Quieres agendar una evaluación?", "ts": "2026-07-14T10:02:11-05:00", "canal": "manychat"}
```

- `canal`: `manychat` o `n8n` — así medimos qué falló en cada era y demostramos la mejora.
- Incluir solo las conversaciones que el negocio autorice; el resto se usa en local sin commitear.

## Cómo se usa en el programa

| Semana | Uso |
|---|---|
| S5 D2 | Leer 10 conversaciones para calibrar el prompt v1 (tono, ≤3 líneas, 1 pregunta) |
| S6 D1/D2 | Extraer objeciones reales ("está caro", "lo consulto") → few-shot y RAG |
| S7 D2 | Tabla antes/después: prompt v1 vs v2 sobre las mismas 10 conversaciones |
| S12 | Dataset de evals (LLM-as-judge local) con casos reales anonimizados |
| S13/S16 | Baseline ManyChat/n8n vs agente nuevo (embudo: conversación → lead → cita → pago) |

**Para exportar desde ManyChat:** export de contactos + historial; desde n8n: export del workflow/executions (si quedó). El monitor/negocio los convierte a este formato.
