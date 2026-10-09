# Ejemplo — Webhook de Meta (Issue #3)

**Qué aprendes:** (1) verificar que un POST realmente viene de Meta y (2) leer el payload anidado de WhatsApp sin que `statuses` o un tipo nuevo te tumben el servicio.
**Qué NO hace:** no define `InboundEvent`, no crea rutas FastAPI, no fija el tenant ni normaliza texto. Eso es tu Issue.

## Archivos (carga solo estos con tu IA, ~100 líneas en total)

| Archivo | Rol |
|---|---|
| `firma_hmac.py` | `firmar` y `firma_valida` (HMAC-SHA256, tiempo constante, falla cerrado) |
| `navegar_payload.py` | `leer_mensaje` y `es_solo_estado` sobre el JSON anidado |
| `fixtures/*.json` | Payloads anónimos con la forma real: texto, imagen, `statuses` (números falsos) |
| `test_*.py` | Comportamiento esperado: corre estos tests **primero** |

```bash
pytest program/02_REFERENCE/ejemplos/webhook-meta -q     # debe dar 10 passed
```

## Los dos GET/POST que Meta te manda

| Método | Para qué | Qué debes hacer |
|---|---|---|
| `GET /webhook?hub.mode=subscribe&hub.verify_token=…&hub.challenge=…` | Handshake al configurar el webhook | Si `hub.verify_token` == `WHATSAPP_VERIFY_TOKEN` devuelve `hub.challenge` (texto plano, 200); si no, 403 |
| `POST /webhook` | Cada mensaje o acuse | (1) **Lee el cuerpo crudo como bytes**, (2) valida `X-Hub-Signature-256` con `WHATSAPP_APP_SECRET` → si falla, 403, (3) responde **200 rápido** y procesa después |

> Dos secretos distintos, no los mezcles: el **verify token** solo sirve en el GET (lo inventas tú); el **App Secret** firma los POST (lo da Meta en el panel de la app). Mezclarlos es el error más común (incluso en el ejemplo oficial de Meta, ver `../README.md` §Lección).

## Paso a paso sugerido para tu Issue (usa estos bloques como referencia)

1. Corre los tests del ejemplo y léelos: son la especificación de cada bloque.
2. En tu `src/channels/whatsapp/`, escribe **primero** tus tests (con tus fixtures en `tests/fixtures/`) y luego tu código; adapta los bloques a tus nombres y al contrato `InboundEvent`.
3. En tu ruta `POST`: `cuerpo = await request.body()` **antes** de parsear JSON (la firma es sobre los bytes originales; si re-serializas el JSON, la firma ya no coincide).
4. Registra en logs solo `wa_id` enmascarado (`51900***000`), nunca el texto ni el teléfono completo.
5. Prueba a mano con `curl` y con el `/docs` de FastAPI; para firmar un POST de prueba usa `firmar()` de este ejemplo en un `python -c`.

## Errores comunes (si te pasa X, haz Y)

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| Meta dice "no se pudo validar la URL" | Tu GET devuelve JSON o un número, no el `hub.challenge` en texto plano | Devuelve `PlainTextResponse(challenge)` |
| Todos tus POST reales dan 403 | Firmaste con el verify token, o parseaste y re-serializaste el cuerpo | Usa `WHATSAPP_APP_SECRET` y los bytes crudos |
| `KeyError: 'messages'` en producción | Llegó un `statuses` | Usa `es_solo_estado` / `.get()` y responde 200 |
| Meta reintenta el mismo mensaje | Tardaste o devolviste 5xx | 200 inmediato; guarda `msg["id"]` para ignorar duplicados (idempotencia) |

## Preguntas de comprensión (responde en tu PR, con tus palabras)

1. ¿Por qué `firma_valida` usa `compare_digest` en lugar de `==`?
2. ¿Por qué falla cerrado si `WHATSAPP_APP_SECRET` está vacío? ¿Qué pasaría si fallara abierto?
3. ¿Por qué hay que validar la firma sobre los **bytes crudos** y no sobre el `dict` ya parseado?
4. ¿Qué dos secretos distintos intervienen y cuál se usa en GET vs POST?

Fuentes leídas: `pywa` (MIT) `webhook_update_validator` y el ejemplo `signature-validation-with-webhooks-payloads` de `fbsamples` (con bug, ver `../README.md`). Documentación oficial de Meta: *Webhooks → Payload validation*.
