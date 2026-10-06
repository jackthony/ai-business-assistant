# Arquitectura objetivo — AI Business Assistant (multitenant)

> Estado: borrador v1 (alineado al plan S4–S16). Se valida/actualiza en la re-secuencia v2.

## Visión general

```
WhatsApp Cloud API (nube, único obligatorio)
        │ webhook GET/POST
        ▼
FastAPI (Integration Hub)  ──  canales/whatsapp/  (extrae texto, audio, imagen)
        │
        ▼
LangGraph StateGraph  ──  memoria (SqliteSaver dev → PostgresSaver prod)
        │
        ├── preprocessor   (voz → texto, imagen → JSON)
        ├── supervisor     (clasifica intención → rutea)
        ├── info_agent     (RAG ChromaDB: servicios, precios, promos)
        ├── booking_agent  (disponibilidad → propone horarios)
        ├── checkout_agent (valida comprobante → registra lead)
        └── safety_agent   (congela bot → handoff humano)
        │
        ▼
Respuesta WhatsApp / Tools (Sheets, Calendar, DB)
```

## AgentState (base)

```python
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]   # historial
    phone: str                                # thread_id / tenant lookup
    tenant: str                               # "hola_mujer" | "neuracode"
    intent: str
    status: Literal["active", "handoff_requested", "waiting_payment"]
```

## Multitenant

- `configs/hola_mujer/` y `configs/neuracode/`: system prompt, RAG namespace, reglas y tools permitidas.
- El tenant se resuelve por el número receptor (phone_number_id) del webhook.

## Repo único

- `jackthony/ai-business-assistant`: programa (carpetas `00_`–`09_`) + producto desde S4: `src/{api,agents,tools,rag,memory,channels,models,services,infrastructure}`, `tests/`, `configs/`.
- Branches cortas por Issue (TBD), `main` protegido. PRs = evidencia SENATI.

## Harness (confiabilidad alrededor del agente — ADR-009)

- **Permisos por nivel:** N1 automático (info/RAG/disponibilidad) · N2 con aprobación/HITL (agendar, validar comprobante, registrar lead) · N3 nunca expuesto (borrar, precios base).
- **Efectos con gating:** `draft_effects → human_review (interrupt) → apply_effects` — evita dobles cobros/citas al reanudar un checkpoint.
- **Validación determinista primero** (Pydantic/regex en tools); LLM-as-a-Judge solo offline.
- **Decisiones rápidas (patrón Jev, MIT):** clasificar/rutear con salida tipada de 1 token + logprobs y umbral de confianza; bajo el umbral → handoff. Aplica a triage (#16), router (#19) y evals (#27) — ver `program/02_REFERENCE/jev-pattern.md`.
- **RAG íntegro:** provenance por documento; jamás re-ingerir salidas del bot (ASI06).
- **Intent gate + action log:** validar esquema/rate-limit antes de cada tool; toda escritura con log y undo.
- **Métricas de ROI** instrumentadas desde S4 (ver `program/00_PROJECT/roi_metrics.md`).

## Datos y límites

- HealthTech: nada clínico; safety_agent deriva a humano (Jioysi).
- Nunca datos reales de clientes en desarrollo: fixtures anonimizados.
