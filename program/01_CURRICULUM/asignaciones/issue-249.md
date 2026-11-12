# #249 · Deduplicación local de mensajes de WhatsApp

## Comportamiento

Cada POST firmado conserva su acuse HTTP 200. Tras el acuse, omite los mensajes cuyo ID ya esté en curso o se haya procesado con éxito en la misma instancia del webhook, incluso entre lotes. Los IDs distintos y los mensajes sin ID siguen su flujo habitual.

Si el procesamiento falla, una nueva entrega puede reintentarlo. El registro conserva hasta 4096 IDs completados en orden de finalización y se pierde al reiniciar.

## Archivos

- `src/channels/whatsapp/webhook.py`

## Pruebas

- `tests/test_channel_whatsapp_webhook.py`
- `pytest -q tests/test_channel_whatsapp_webhook.py` con POST firmados y envíos simulados.
- Un ID repetido dentro de un lote, en otro POST o durante el envío en curso provoca un solo envío exitoso. Un ID distinto genera su propio envío. Un fallo simulado permite reintentar el mismo ID.
