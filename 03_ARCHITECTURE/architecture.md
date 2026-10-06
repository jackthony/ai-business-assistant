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

## Repos

- **1 repo producto** `ai-business-assistant` (pendiente de crear): `src/{api,agents,tools,rag,memory,channels,models,services,infrastructure}`, `tests/`, `configs/`.
- Branches cortas por Issue (TBD). PRs = evidencia SENATI.

## Datos y límites

- HealthTech: nada clínico; safety_agent deriva a humano (Jioysi).
- Nunca datos reales de clientes en desarrollo: fixtures anonimizados.
