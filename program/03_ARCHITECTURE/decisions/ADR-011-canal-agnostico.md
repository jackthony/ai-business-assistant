# ADR-011: Canal-agnóstico — la capa de agentes no conoce el canal

- **Fecha:** 2026-10-06
- **Estado:** aceptada

## Contexto

Hoy el producto se integra con WhatsApp (Meta Cloud API, ADR-003). El negocio evalúa en el futuro TikTok u otras plataformas de mensajería/venta. El valor del programa es la **capa de agentes** (LangGraph + RAG + memoria + harness); el canal es un medio, no el producto.

## Problema

¿Dónde vive la lógica del canal: dentro de los agentes o detrás de una frontera explícita?

## Opciones

1. Agentes acoplados a WhatsApp (importar SDK de Meta en nodos del grafo).
2. **Adapters de canal + contrato interno de mensajes** (los agentes hablan solo el contrato interno).
3. Construir adapters para varias plataformas desde S4 (alcance prematuro).

## Decisión

Opción 2. La capa de agentes recibe y emite un **contrato interno canónico**:

```python
class InboundEvent(BaseModel):
    tenant: str
    user_id: str          # id estable por canal (teléfono en WhatsApp)
    type: Literal["text", "media", "voice"]
    content: str | None
    channel: str          # "whatsapp" hoy; "tiktok" mañana

class OutboundReply(BaseModel):
    text: str | None
    media: bytes | None
    template_id: str | None   # plantillas aprobadas por canal
    channel_metadata: dict
```

- `src/channels/` contiene **un adapter por canal** (hoy solo `whatsapp`: verificación GET, parseo POST, envío — Issues #3/#4). Los agentes **nunca** importan SDKs del canal.
- Una plataforma nueva (TikTok u otra) = un adapter nuevo + su ADR; `src/agents/`, `src/tools/`, `src/rag/` y `src/memory/` no se tocan.

## Consecuencias

- Mapear por canal: identidad de usuario, media, plantillas y ventanas de respuesta (24 h en WhatsApp).
- Costos por canal: FinOps mide costo por conversación **por canal** (Meta: ver `program/02_REFERENCE/meta-pricing.md`).
- HITL, evidencia y seguridad (ADR-009) operan sobre el contrato interno: son canal-agnósticos.
- El demo E2E (S4) ya prueba el contrato interno con el adapter de WhatsApp.
