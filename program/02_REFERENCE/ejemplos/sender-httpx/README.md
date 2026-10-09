# Ejemplo — Envío saliente con httpx (Issue #4)

**Qué aprendes:** hacer un POST async que reintenta **solo** si no hubo respuesta (fallo de red), mide la latencia y se prueba **sin tocar Meta** usando `httpx.MockTransport`.
**Qué NO hace:** no define la clase `WhatsAppSender`, no lee tokens de `.env`, no decide qué hacer con un 5xx, no mide el "tiempo de primera respuesta" webhook → send. Eso es tu Issue.

## Archivos

| Archivo | Rol |
|---|---|
| `cliente_con_reintento.py` | `post_con_reintento` (reintento + latencia) y `cuerpo_texto` (forma del cuerpo de la Cloud API) |
| `test_cliente_con_reintento.py` | 5 tests: éxito, petición bien armada, reintento tras caída, agotar reintentos, 4xx sin reintento |

```bash
pytest program/02_REFERENCE/ejemplos/sender-httpx -q     # debe dar 5 passed
```

## Cómo se manda un mensaje (Cloud API)

`POST https://graph.facebook.com/<versión>/<WHATSAPP_PHONE_NUMBER_ID>/messages`
Cabeceras: `Authorization: Bearer <WHATSAPP_TOKEN>` y `Content-Type: application/json`.
Cuerpo: ver `cuerpo_texto`. La versión de la Graph API la fija la doc oficial vigente: **no la hardcodees en varios sitios**, ponla en una constante/setting.

Un mensaje de **texto libre** solo se puede enviar dentro de la ventana de 24 h desde el último mensaje de la clienta; fuera de ella hace falta un *template* aprobado (`program/02_REFERENCE/meta-pricing.md` §Templates). Por eso tu demo con fixtures no necesita templates, pero el bot real sí.

## Paso a paso sugerido

1. Corre los tests del ejemplo y léelos: dicen qué se espera del reintento.
2. Escribe **primero** el test de tu `WhatsAppSender.send_text` con `MockTransport` (URL, cabeceras y cuerpo exactos), luego tu clase en `src/channels/whatsapp/sender.py` apoyándote en este bloque.
3. Inyecta el `httpx.AsyncClient` (no lo crees dentro de `send_text`): así el test pasa un cliente con transporte falso.
4. Registra latencia y `wa_id` enmascarado en el log; nunca el token ni el texto del cliente.
5. Demo E2E: si #16 aún no está listo, usa el `MockTransport` en la demo local (fixture → parser → sender) y grábala; no inventes llamadas "reales".

## Errores comunes

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| El mensaje llega duplicado | Reintentaste un 4xx/5xx o reintentas sin límite | Reintenta solo `TransportError` y con tope |
| Tu test hace una llamada real | Creaste el cliente dentro de la función | Inyecta el cliente con `MockTransport` |
| `401` / `190` de Meta | Token vencido o mal copiado | Revisa `WHATSAPP_TOKEN` en tu `.env` local (nunca en el repo) |
| `131047` (re-engagement) | Pasaron >24 h sin mensaje de la clienta | Necesitas un template aprobado |

## Preguntas de comprensión (responde en tu PR)

1. ¿Por qué no se reintenta un `400`? ¿Qué pasaría con un mensaje de WhatsApp si se reintenta un `5xx` ciegamente?
2. ¿Qué ventaja da inyectar el `AsyncClient` en lugar de crearlo dentro de la función?
3. ¿Qué mide `latencia_ms` y por qué el programa la quiere en `roi_metrics.md`?

Fuentes leídas: documentación oficial de `httpx` (Transports → `MockTransport`) y el flujo de envío de `pywa` (MIT).
