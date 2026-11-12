# #253 · Límite de texto de Telegram

## Comportamiento

Un POST autenticado de Telegram con texto privado de más de 1000 caracteres recibe HTTP 200 con `{"ok": true}`. El webhook descarta ese texto antes de llamar al agente o al emisor. Un texto de exactamente 1000 caracteres se procesa completo.

## Archivos

- `src/channels/telegram.py`

## Pruebas

- `tests/test_channel_telegram.py`
- `pytest -q tests/test_channel_telegram.py` con solicitudes ficticias y emisor simulado.
