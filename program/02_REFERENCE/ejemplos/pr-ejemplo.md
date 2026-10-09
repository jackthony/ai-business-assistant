# Cómo se ve un PR completo (plantilla de referencia)

> Es un PR **ficticio** del tipo del Issue #3, para que veas el nivel de detalle esperado. Compara con `.github/pull_request_template.md`.

**Título:** `feat(webhook): verificar firma y parsear mensajes entrantes (#3)`
**Rama:** `issue-3-webhook-meta` → `main` · **Cierra:** `Closes #3`

## Qué y por qué

- Añade `GET /webhook` (verificación con `hub.verify_token`) y `POST /webhook` (valida `X-Hub-Signature-256` sobre los bytes crudos, responde 200 y entrega un `InboundEvent`).
- Se ignoran los `statuses`: no son mensajes de la clienta y Meta los envía en cada entrega.
- El tenant queda fijo en `hola_mujer` (multitenant real en S10; hay un `TODO(S10)` en el código).
- No se tocó nada fuera de `src/channels/whatsapp/`, `src/api/routers/` y `tests/`.

## Preguntas de comprensión (con mis palabras)

1. **`hub.verify_token` / `hub.challenge`:** Meta hace un GET al configurar el webhook para comprobar que la URL es mía; yo devuelvo el `challenge` solo si el token coincide.
2. **200 en <1 s y procesar después:** si tardo, Meta asume fallo y reintenta, y llegarían mensajes duplicados.
3. **Mismo mensaje dos veces:** guardo el `id` del mensaje y descarto los repetidos (idempotencia).

## Evidencia

- `pytest -q` → `12 passed` · `ruff check`, `mypy`, `bandit` sin hallazgos (captura en el PR).
- Prueba manual con `curl` (verificación + POST firmado con `firmar()` de un script) — salida pegada abajo.

## Checklist

- [x] Rama `issue-N-slug` desde `main` actualizado (`git pull` antes de empezar)
- [x] Commits convencionales (`feat(webhook): …`, `test(webhook): …`)
- [x] Sin secretos ni datos reales (fixtures con números falsos)
- [x] Las 4 puertas en verde en local y en CI
- [x] Dije en el PR qué parte hice con ayuda de IA y la expliqué con mis palabras

## Lo que el monitor mira primero

1. ¿Responde las preguntas **con sus palabras** o copió la respuesta de la IA?
2. ¿Los tests prueban el criterio del Issue (token malo → 403, status ignorado, firma inválida → 403) o son de relleno?
3. ¿Respetó el contrato `InboundEvent` y la regla de que el núcleo no conoce el canal?
