# #247 · Mensajes de WhatsApp en lote

## Comportamiento

Un POST firmado puede traer varios mensajes. Recorre todas las entradas, cambios y mensajes en el orden del cuerpo. Omite estados y mensajes mal formados. Confirma con HTTP 200 y procesa los mensajes válidos después del acuse.

Si falla el procesamiento de un mensaje, registra el tipo de error y sigue con los demás. No incluyas identificadores, texto ni credenciales en ese registro. Se conserva la verificación de la firma sobre el cuerpo completo y la función de análisis de un solo evento.

## Archivos

- `src/channels/whatsapp/webhook.py`

## Pruebas

- `tests/test_channel_whatsapp_webhook.py`
- `pytest -q tests/test_channel_whatsapp_webhook.py` con números, credenciales y envíos ficticios.
- Un lote con tres mensajes válidos en varias entradas y cambios produce tres envíos en orden, incluso si trae estados o mensajes mal formados entre ellos.
- Si el primer envío falla, el webhook mantiene el 200 y los siguientes se procesan.
