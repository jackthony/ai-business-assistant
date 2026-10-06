# Arquitectura objetivo — AI Business Assistant (multitenant)

> Estado: v2 — alineada con `program/01_CURRICULUM/16_week_plan.md` (S4–S16).

## Visión general

```
WhatsApp Cloud API (nube, único obligatorio)  ──  adapter en src/channels/whatsapp
        │ webhook GET/POST
        ▼
FastAPI (Integration Hub)  ──  contrato interno InboundEvent (ADR-011, canal-agnóstico)
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

## Canal-agnóstico (ADR-011)

- La capa de agentes habla solo el **contrato interno** (`InboundEvent` / `OutboundReply`); los adapters de canal traducen. Hoy: WhatsApp (Cloud API). Futuro: TikTok u otro = adapter nuevo, sin tocar `agents/`.
- Costos por canal: FinOps mide costo por conversación **por canal** (Meta: `program/02_REFERENCE/meta-pricing.md`).

## Repo único

- `jackthony/ai-business-assistant`: programa (`program/00_PROJECT`–`05_EVALUATION`) + producto desde S4 (`src/`, `tests/`, `configs/`, `data/`, `docs/`).
- Branches cortas por Issue (TBD) — guardianes `tbd-guardian`/`tbd-enforcer` en `.github/workflows/`. PRs = evidencia SENATI.

## Estructura de carpetas del producto (v1 — la crea el Issue #2, crece por semanas)

```
src/
  api/            # app FastAPI: routers, /health, /webhook (Issue #2/#3)
  channels/       # adapters de canal: hoy whatsapp (verificación GET, parseo POST, envío); mañana tiktok (ADR-011)
  agents/         # grafos LangGraph: agente único primero; supervisor recién S10 (ADR-007)
  tools/          # tools @tool con schemas Pydantic estrictos (S7)
  rag/            # ChromaDB: ingesta, retriever, un namespace por tenant (S6)
  memory/         # checkpointer: SqliteSaver dev → PostgresSaver prod (S14)
  models/         # clientes Ollama (DeepSeek, Qwen2.5-VL) + fallback (S15)
  services/       # efectos secundarios: Calendar, Sheets, sender saliente (Issue #4)
  infrastructure/ # config, logging, métricas (FinOps desde S4)
tests/            # unit + integración (mocks; sin llamadas reales a modelos ni APIs)
configs/          # hola_mujer/ y neuracode/: system prompt, reglas, tools permitidas
data/             # KB-A en JSON (anonimizado) — nunca datos reales
docs/             # CONTEXT.md + ARCHITECTURE.md (los escriben los practicantes)
```

Reglas del código (obligatorias, verificadas por CI):

- Un módulo = una responsabilidad; imports absolutos desde `src/`.
- Cada módulo tiene tests que cubren los **criterios de aceptación de su Issue** (casos borde incluidos).
- Nada clínico: el bot deriva a humano (`safety_agent`, ADR-009).
- Sin secretos: `.env` + `.env.example`; las 4 puertas del CI corren en cada PR (`ruff`+`mypy`+`pytest`+`bandit`).

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
