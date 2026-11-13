# [S04 D2] Paso a paso guiado — Webhook de WhatsApp con fixtures (Issue #3)

> **Para quién:** practicante de 2.º año de AI Engineering, con Python básico y Git básico, que **no** conoce todavía la firma HMAC de un webhook ni cómo responde FastAPI «después». Este archivo te acompaña **mientras trabajas**; el contrato ([`S04_D2.md`](S04_D2.md)) dice **qué** debe quedar. Aquí aprendes **cómo abordarlo sin perderte**.
>
> **Reglas del juego:** no hay código de la solución aquí (si lo hubiera, no aprenderías). Hay explicación, pistas y puntos de control. Una sesión dura ~3 h; los tiempos son una guía. Los comandos son para Windows (**cmd**), desde la raíz del repo.
>
> **Buena noticia:** ya estudiaste el ejemplo `webhook-meta` (#34). La firma y la lectura del payload ya las viste funcionar; aquí las llevas al proyecto. Son **10 pruebas chicas**: avanza de una en una y celebra cada verde.

## Mapa de la sesión

| Bloque | Tiempo | Resultado que puedes comprobar |
|---|---|---|
| Calentamiento | 15 min | Firmas un texto a mano y ves cambiar el resultado |
| Paso 0 | 15 min | Rama creada y N anotado |
| Pasos 1–4 (W1, W3, W4, W5) | 60 min | Verificación, firma y conversión en verde |
| Pasos 5–6 (W6, W10) | 25 min | Lo ignorado y los hilos |
| Pasos 7–10 (W7, W8, W9, W2) | 50 min | Router completo y cableado |
| Cierre y PR | 25 min | PR abierto con `Closes #3` |

## Mini-conceptos (léelos antes del Paso 0)

**1. Verificación del webhook (GET).**
- **Idea:** al registrar tu URL, Meta hace un GET con un token que **tú** inventaste y un número `challenge`. Si el token coincide, le devuelves el `challenge` tal cual y Meta sabe que la URL es tuya.
- **Analogía:** el portero que dice «contraseña» y espera la respuesta acordada.
- **Ejemplo fuera del proyecto:** `"ok" if clave == "abc" else None`.
- **Profundiza:** https://developers.facebook.com/docs/graph-api/webhooks/getting-started (verifícalo ahí).

**2. Firma HMAC del cuerpo crudo (POST).**
- **Idea:** Meta mezcla el cuerpo del mensaje con un secreto compartido (el App Secret) y manda el resultado en `X-Hub-Signature-256`. Tú haces la misma mezcla y comparas. Si coincide, nadie lo cambió ni lo inventó.
- **Analogía:** un sello de lacre: solo quien tiene el sello lo reproduce igual.
- **Ejemplo fuera del proyecto:** `hmac.new(b"clave", b"hola", hashlib.sha256).hexdigest()`.
- **Profundiza:** `hmac.compare_digest` en https://docs.python.org/3/library/hmac.html y el ejemplo `firma_hmac.py`.

**3. Responder 200 y trabajar después.**
- **Idea:** si tardas, Meta reintenta. FastAPI te deja devolver la respuesta y ejecutar una tarea justo después con `BackgroundTasks`.
- **Analogía:** el mesero anota tu pedido, te dice «ya va» y luego lo lleva a cocina.
- **Ejemplo fuera del proyecto:** `tareas.add_task(enviar, "hola")` dentro de una ruta que recibe `tareas: BackgroundTasks`.
- **Profundiza:** https://fastapi.tiangolo.com/tutorial/background-tasks/

**4. Un hilo por canal y usuario (LangGraph).**
- **Idea:** el agente guarda la conversación bajo un `thread_id`. Aquí es `canal:usuario`, así que el mismo número en WhatsApp y en Telegram son conversaciones separadas. El canal nuevo no toca al agente (ADR-011).
- **Analogía:** dos buzones distintos aunque el vecino sea la misma persona.
- **Ejemplo fuera del proyecto:** `f"{canal}:{usuario}"`.
- **Profundiza:** https://langchain-ai.github.io/langgraph/ (sección de persistencia y `thread_id`).

## Calentamiento (fuera del proyecto)

En un archivo suelto (`calentamiento.py`), con `hmac` y `hashlib`, firma dos veces el texto `b"hola"` con la clave `b"clave"` y luego una tercera vez `b"hola!"`. **Resultado esperado:** las dos primeras salidas son iguales; la tercera es totalmente distinta. Esa es toda la idea de la firma. Bórralo después.

## Paso a paso

### Práctica desde el commit de TDD

Si el webhook ya está integrado en `main`, parte de la etiqueta `tdd-issue-3`. Contiene las pruebas W1–W10 y la base anterior al webhook. Desde PowerShell, con el entorno de Python 3.11 activado:

```powershell
git fetch origin tag tdd-issue-3
git switch -c practica/webhook-whatsapp tdd-issue-3
pytest tests/test_channel_whatsapp_webhook.py -q
```

El primer resultado esperado es `ModuleNotFoundError: No module named 'channels.whatsapp.webhook'`. Con las pruebas ya presentes, implementa una pieza a la vez según el orden de los pasos 1 a 10. Ejecuta la prueba de cada paso con `-k` y termina con las diez en verde. Conserva el resultado en rojo, el resultado final y tus respuestas de comprensión para la revisión del [Issue #3](https://github.com/jackthony/ai-business-assistant/issues/3).

En esta modalidad el entregable es la evidencia de tu práctica. La rama de ejercicio se compara contra `tdd-issue-3` y la integración de producto ya está en `main`.

### Paso 0 — Prepara tu terreno
**Haz esto:** sigue los pasos 1 a 4 de la sección 7 del contrato: `git checkout main`, `git pull`, `git checkout -b issue-3-webhook-whatsapp`, activa el entorno (`.venv\Scripts\activate`), corre `pytest tests -q` y **anota N**. Corre también `pytest program/02_REFERENCE/ejemplos/webhook-meta -q`.
**Por qué:** necesitas saber cuántas pruebas había antes para comprobar al final que subió exactamente en 10.
**Debes ver:** `N passed` y `10 passed` del ejemplo.
**Si falla:** pega la salida como texto en el Issue #3 (sección 12 del contrato).
**Punto de control:** ¿cuánto vale tu N?

### Paso 1 — La verificación: prueba W1
**Haz esto:** crea `tests\test_channel_whatsapp_webhook.py`. Pon arriba las constantes de prueba del contrato (sección 6) y escribe solo `test_w1_...`. Córrela: es normal que falle la colección con `ModuleNotFoundError: No module named 'channels.whatsapp.webhook'`. Crea `src\channels\whatsapp\webhook.py` con `verify_challenge` (5.1) hasta ver verde con `pytest tests\test_channel_whatsapp_webhook.py -q -k test_w1_`. Commit chico.
**Por qué:** es la pieza más simple; con ella ya viste el ciclo rojo → verde.
**Debes ver:** primero el rojo por el módulo que no existe; luego `1 passed`.
**Si falla:** si la colección falla por otra cosa (un import mal escrito), corrígela antes de seguir. Si un caso devuelve el `challenge` cuando no debía, repasa las tres condiciones de 5.1.
**Punto de control:** ¿qué devuelve la función cuando el token es vacío y el recibido también?

### Paso 2 — La firma: prueba W3
**Haz esto:** escribe `test_w3_...` con sus cinco casos (puedes firmar con una pequeña función auxiliar en el archivo de pruebas). Implementa `signature_is_valid` (5.2). Mira cómo lo hace `firma_hmac.py` del ejemplo, pero escríbelo con tus palabras.
**Por qué:** esta función es el candado del POST. Debe fallar cerrado: ante la duda, `False`.
**Debes ver:** `1 passed` con `-k test_w3_`.
**Si falla:** si el caso «sin prefijo» da `True`, comparaste solo los hex. Si el de «byte cambiado» da `True`, firmaste el cuerpo equivocado.
**Punto de control:** ¿por qué la firma es sobre `bytes` y no sobre un `dict`?

### Paso 3 — El mensaje de texto: prueba W4
**Haz esto:** escribe `test_w4_...` con el payload mínimo de la sección 6. Implementa `parse_payload` solo para texto (5.3).
**Por qué:** aquí conviertes el JSON de Meta al contrato interno `InboundEvent`, y así el agente no sabe de WhatsApp.
**Debes ver:** `1 passed`.
**Si falla:** `KeyError` o `TypeError` → recorriste mal el anidado `entry → changes → value → messages`. Relee `navegar_payload.py`.
**Punto de control:** ¿de qué campo sale el `user_id`?

### Paso 4 — Audio e imagen: prueba W5
**Haz esto:** escribe `test_w5_...` y amplía `parse_payload`: `audio` es `voice`, `image` es `media`, ambos sin contenido (ya viste el patrón en `parse_update` de Telegram).
**Por qué:** el agente debe poder decir «solo leo texto» sin que el servicio se caiga.
**Debes ver:** `1 passed`.
**Si falla:** si `mypy` se queja del tipo `str` en `InboundEvent`, es porque `type` solo admite tres valores literales (ver Pista del Paso 4).
**Punto de control:** ¿qué `content` llevan estos eventos?

### Paso 5 — Lo que se ignora: prueba W6
**Haz esto:** escribe `test_w6_...` con los cinco casos y haz que `parse_payload` **nunca lance** y devuelva `None` en todos.
**Por qué:** Meta manda muchos acuses (`statuses`) y reacciones; si tu código revienta, Meta reintenta y entras en un bucle.
**Debes ver:** `1 passed`.
**Si falla:** `IndexError` o `KeyError` salen sin capturar; mira cómo el ejemplo usa un `try` corto o `.get()`.
**Punto de control:** ¿qué pasa con un mensaje sin `from`?

### Paso 6 — Un teléfono, dos hilos: prueba W10
**Haz esto:** escribe `test_w10_...`: un evento de `parse_payload` y otro de `parse_update` de Telegram con el mismo número, y compara `thread_id_for` de cada uno. No hay código nuevo si W4 está bien: la prueba te muestra una decisión de diseño.
**Por qué:** entender que el hilo es `canal:usuario` explica por qué un canal nuevo no toca al agente.
**Debes ver:** `1 passed`.
**Si falla:** el `chat.id` de Telegram es un número entero; conviértelo como en la prueba de Telegram.
**Punto de control:** ¿qué mezclaría la conversación si el hilo fuera solo el teléfono?

### Paso 7 — Firma mala o ausente: prueba W7
**Haz esto:** escribe `test_w7_...` (modelo: G4 en `tests\test_channel_telegram.py`) usando `create_chat_app` con los tres parámetros nuevos de 5.5. Rojo por el parámetro desconocido. Implementa `build_whatsapp_router` solo con el POST y su 403, y haz el cableado de 5.5 en `src\api\chat_app.py`.
**Por qué:** es la prueba que demuestra que un atacante con tu URL no puede inventar mensajes.
**Debes ver:** `1 passed`.
**Si falla:** `TypeError` con `unexpected keyword argument` → falta el cableado de 5.5. Si el cuerpo llega vacío, leíste con `.json()` antes de `.body()`.
**Punto de control:** ¿qué debe pasar con `send` cuando la firma es mala?

### Paso 8 — Falla cerrado al construir: prueba W8
**Haz esto:** escribe `test_w8_...` y valida los secretos al construir el router.
**Por qué:** un servidor sin secreto no debe arrancar «abierto» sin que nadie lo note.
**Debes ver:** `1 passed`.
**Si falla:** el caso de solo espacios (`"  "`) suele olvidarse: piensa en `strip`.
**Punto de control:** ¿qué pasaría si fallara abierto con el secreto vacío?

### Paso 9 — POST válido y respuesta en segundo plano: prueba W9
**Haz esto:** escribe `test_w9_...` copiando la estructura de G5 (`build_graph`, `ScriptedModel`, `InMemorySaver`). Firma el cuerpo, haz POST y comprueba 200; luego POST de `statuses`. Implementa `process_whatsapp_event` y agéndalo con `BackgroundTasks`.
**Por qué:** es el recorrido completo: llega, valida, responde 200 y luego el agente contesta por la función inyectada.
**Debes ver:** `1 passed`; `send` se llamó una sola vez con `("51900000000", texto)`.
**Si falla:** si `send` nunca se llama, olvidaste agendar la tarea o usaste `TestClient` sin `with`. Si da 403, firmaste bytes distintos a los que mandas (mismo `cuerpo_bytes` en ambos).
**Punto de control:** ¿por qué `send` llega como parámetro y no se importa `sender.py`?

### Paso 10 — El GET por HTTP: prueba W2
**Haz esto:** escribe `test_w2_...` y agrega la ruta GET: los parámetros se llaman `hub.mode`, etc. (necesitas `alias`). Devuelve texto plano o 403.
**Por qué:** es lo que Meta usa al registrar tu URL.
**Debes ver:** `1 passed`.
**Si falla:** `422` → no hiciste el `alias`. Si el cuerpo viene entre comillas (`"987"`), devolviste JSON y no texto plano.
**Punto de control:** ¿qué secreto usa este GET y cuál el POST?

### Paso 11 — Puertas, diff y PR
**Haz esto:** las 4 puertas (`ruff check src tests && mypy src --ignore-missing-imports && pytest tests -q && bandit -r src -x tests -ll`), el total debe ser N + 10; `git diff --name-only main` con los 3 archivos de 4. Sube la rama y abre el PR con `Closes #3` y tus respuestas de la sección 11.
**Por qué:** así tu PR llega limpio a la revisión.
**Debes ver:** todo en verde.
**Si falla:** pega el error como texto en el Issue.
**Punto de control:** ¿puedes explicar en voz alta las 3 preguntas?

## Escalera de pistas (úsala solo cuando estés trabado, de arriba abajo)

**Paso 2 (la firma):**
- *Pista 1:* se calcula igual que Meta: HMAC-SHA256 del cuerpo con el secreto y se compara con la cabecera.
- *Pista 2:* `hmac.new`, `hexdigest` y `hmac.compare_digest` en https://docs.python.org/3/library/hmac.html; y `firma_hmac.py` del ejemplo.
- *Pista 3 (en palabras):* si falta cabecera, secreto o el prefijo, devuelve `False`; si no, calcula la firma esperada del cuerpo y compárala en tiempo constante con la cabecera.

**Paso 4 (los tipos del evento):**
- *Pista 1:* `InboundEvent.type` solo acepta tres palabras exactas; una variable de tipo `str` no basta para `mypy`.
- *Pista 2:* `typing.Literal` en https://docs.python.org/3/library/typing.html.
- *Pista 3 (en palabras):* decide primero el tipo del evento (`voice` o `media`) en una variable anotada con esas dos opciones, y después construye el evento una sola vez.

**Paso 5 (nunca lanzar):**
- *Pista 1:* un payload raro no debe tumbar el servicio.
- *Pista 2:* `try/except` con `KeyError`, `IndexError`, `TypeError` (y `ValueError` si el evento se rechaza por formato).
- *Pista 3 (en palabras):* intenta leer el primer mensaje; si algo falta o el tipo no es uno de los soportados, devuelve `None`.

**Paso 7 (leer el cuerpo y el 403):**
- *Pista 1:* la firma es sobre los bytes tal como llegaron.
- *Pista 2:* `await request.body()` y `Header(...)` en https://fastapi.tiangolo.com/tutorial/header-params/ (FastAPI convierte `x_hub_signature_256` en `X-Hub-Signature-256`).
- *Pista 3 (en palabras):* lee los bytes, valida con tu función, levanta `HTTPException` 403 si falla y solo entonces interpreta el JSON.

**Paso 9 (segundo plano):**
- *Pista 1:* la ruta devuelve su respuesta y FastAPI ejecuta la tarea después.
- *Pista 2:* `BackgroundTasks.add_task` en https://fastapi.tiangolo.com/tutorial/background-tasks/; compara con `process_telegram_event`.
- *Pista 3 (en palabras):* si hay evento, agenda la función que llama al despachador y, si hay respuesta con texto, usa la función `send` recibida; la ruta devuelve `{"ok": true}`.

**Paso 10 (el GET):**
- *Pista 1:* el nombre del parámetro tiene un punto, que no es válido en Python.
- *Pista 2:* `Query(alias=...)` en https://fastapi.tiangolo.com/tutorial/query-params-str-validations/ y `PlainTextResponse`.
- *Pista 3 (en palabras):* recibe los tres parámetros con alias, pregunta a `verify_challenge`; con texto devuelve texto plano, si no, 403.

## Errores típicos de esta asignación

| Síntoma (lo que ves) | Causa probable | Qué hacer |
|---|---|---|
| Todos los POST dan 403 | Firmaste con el verify token, o con bytes distintos a los enviados | Usa el App Secret y el mismo `cuerpo_bytes` en la firma y en `content=` |
| `422` en el GET | Faltó el `alias` de `hub.mode` | Usa `Query(alias=...)` |
| El GET devuelve `"987"` con comillas | Devolviste JSON | Devuelve `PlainTextResponse` |
| `-k test_w1_` ejecuta 2 pruebas | Hay nombres parecidos en otros archivos | Pon la ruta del archivo antes de `-k` |
| `mypy`: `incompatible type "str"` | `type` es un `Literal`, no cualquier `str` | Ver Pista del Paso 4 |
| `send` nunca se llama | No agendaste la tarea o falta `with TestClient(...)` | Revisa el Paso 9 |

## Autoevaluación antes del PR

- [ ] Cada prueba del contrato la escribí yo, la vi fallar y la vi pasar.
- [ ] Puedo explicar en voz alta, sin mirar, las 3 preguntas de comprensión del contrato.
- [ ] Mi `git diff --name-only main` coincide con la sección 4 del contrato.
- [ ] Anoté en el PR cuántas interacciones usé con mi IA y a quién consulté.

## Prompts sugeridos para tu IA (pequeños y verificables)

1. «Explícame en 5 líneas qué es HMAC-SHA256 y por qué se firma el cuerpo en bytes. No escribas código del proyecto.»
2. «Dame un ejemplo de 3 líneas de `Query(alias="a.b")` en FastAPI, fuera de mi repo.»
3. «Te pego mi prueba `test_w6_...`: dime qué caso borde falta, sin escribir el código.» (pega solo esa prueba)
4. «Este error de pytest, pegado como texto: ¿qué significa? Dime qué mirar, no la solución.»

**Prohibidos:** «escríbeme `webhook.py` completo» y «hazme las pruebas W1–W10»: te quitan justo lo que esta sesión quiere que aprendas.
