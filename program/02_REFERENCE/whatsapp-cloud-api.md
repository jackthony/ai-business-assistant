# Meta WhatsApp Cloud API — canal

- **Docs:** https://developers.facebook.com/docs/whatsapp/cloud-api
- **Se usa:** S4–S16. Es el **único componente cloud obligatorio** del proyecto.

## Puntos clave

1. **Verificación webhook (GET):** `hub.mode`, `hub.verify_token`, `hub.challenge`. Devolver el challenge.
2. **Recepción (POST):** el texto viene en `entry[0].changes[0].value.messages[0]`; el remitente en `...contacts[0].wa_id`. Los audios llegan como `type: audio` (media id) y las imágenes como `type: image`.
3. **Envío:** `POST /{phone-number-id}/messages` con `type: text|template`.
4. **Dev local:** ngrok para exponer FastAPI y registrar la URL en Meta for Developers.
5. **Plantillas:** los mensajes proactivos (S13) requieren template messages aprobadas.

## Reglas del proyecto

- Responder siempre `200` rápido y procesar async (Meta reintenta si no).
- Nunca loggear teléfonos completos ni contenido de clientes reales: usar datos de prueba.
- Los tokens van en `.env` (jamás en git); secretos con nombres `META_*`.

## Precios/cobros

- Modelo actual (por mensaje entregado) y tarifas Perú: ver **`meta-pricing.md`** (archivo de referencia, captura 2026-10-06). Afecta FinOps (S15) y los mensajes proactivos (S13).
- Diseño canal-agnóstico: los agentes no tocan Meta; ver ADR-011.
