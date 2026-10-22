# [S06 D3] Paso a paso guiado — Contrato de canal, despachador y canales web y Telegram (Issue #158)

> **Para quién:** practicante de 2.º año de AI Engineering, con Python básico y Git básico, que **no** conoce todavía los adaptadores de canal, los webhooks con secreto ni las tareas de fondo de FastAPI. Este archivo te acompaña **mientras trabajas**; el contrato ([`S06_D3.md`](S06_D3.md)) dice **qué** debe quedar. Aquí aprendes **cómo abordarlo sin perderte**.
>
> **Reglas del juego:** no hay código de la solución aquí (si lo hubiera, no aprenderías). Hay explicación, pistas y puntos de control. Una sesión dura ~3 h; los tiempos son una guía. Todos los comandos son para Windows (**cmd**, no PowerShell), desde la raíz del repo.
>
> **Punto de partida:** esta asignación se apoya en el agente real que ya está en `main` (RAG con citas, derivación a una persona). El Paso 0 lo comprueba. Es una asignación grande: **son 9 archivos**. Si no alcanzas en una sesión, para después del Paso 4 (el despachador funciona) y sigue en la siguiente.

> **Revisión automática de tu avance:** desde tu primer commit haz `git push -u origin <tu-rama>`. El robot abre solo un **PR en borrador** y deja **un comentario que se actualiza en cada push**: cuántos archivos del contrato ya trabajaste, cuáles te faltan y cuál es tu siguiente paso, con pistas. Haz push **al terminar cada paso en verde**.

## Mapa de la sesión

| Bloque | Tiempo | Resultado que puedes comprobar |
|---|---|---|
| Lectura + mini-conceptos | 30 min | Sabes explicar qué es un adaptador de canal y por qué el bot derivado no debe volver a hablar |
| Calentamiento | 15 min | Pruebas una ruta de FastAPI con `TestClient` |
| Paso 0 (terreno, entorno, línea base) | 25 min | `N passed` antes de tocar código |
| Pasos 1–4 (contrato y despachador) | 85 min | `3 passed` y `5 passed` |
| Pasos 5–7 (web y Telegram) | 70 min | `3 passed` y `6 passed` |
| Pasos 8–9 (puertas, commits, PR) | 25 min | PR abierto con `Closes #158` |

> Son ~4 h: **para después del Paso 4** si no alcanzas, y retoma con el Paso 5.

## Mini-conceptos (léelos antes del Paso 0)

Para cada concepto: **Idea**, **Analogía**, **Ejemplo** (fuera de este proyecto) y **Profundiza**.

**1. Adaptador de canal y contrato interno.**
- **Idea:** el agente solo entiende un formato propio de mensajes (`InboundEvent` entra, `OutboundReply` sale). Cada canal (web, Telegram, WhatsApp) tiene un adaptador que traduce su formato al nuestro y al revés.
- **Analogía:** un adaptador de enchufe de viaje: el aparato (el agente) no cambia; cambias el adaptador según el país.
- **Ejemplo:** una función que recibe `{"txt": "hola"}` de un sistema y devuelve `{"text": "hola"}` para el tuyo.
- **Profundiza:** `program/03_ARCHITECTURE/decisions/ADR-011-canal-agnostico.md`.

**2. Hilo, estado y checkpointer.**
- **Idea:** el grafo guarda el estado de cada conversación bajo un `thread_id`. Ese estado incluye `status`. Si una clienta fue derivada a una persona, su `status` queda en `handoff_requested` y el bot debe callar.
- **Analogía:** el expediente de cada paciente en un archivador: el nombre del cajón es el `thread_id`.
- **Ejemplo:** un diccionario `{"ana": [...], "bea": [...]}` donde cada clave guarda su historial.
- **Profundiza:** `program/02_REFERENCE/ejemplos/langgraph-memoria/README.md`.

**3. Validar en la frontera.**
- **Idea:** todo dato que viene de afuera (un id, un texto) se revisa **una vez**, al entrar. Lo que pasa esa revisión ya es confiable para el resto del sistema.
- **Analogía:** el control de seguridad del aeropuerto: se revisa en la entrada, no en cada pasillo.
- **Ejemplo:**
```python
from pydantic import BaseModel, Field
class Codigo(BaseModel):
    valor: str = Field(pattern=r"^[a-z]{3}$")
```
- **Profundiza:** <https://docs.pydantic.dev/latest/concepts/fields/>

**4. Webhook con secreto y respuesta rápida.**
- **Idea:** un webhook es una URL pública a la que un servicio (Telegram) te manda mensajes. Como cualquiera puede escribirle, se exige un **secreto** en un encabezado. Y se responde 200 enseguida para que el servicio no reintente; el trabajo lento se hace después.
- **Analogía:** el portero que pide la contraseña y te abre de inmediato; el pedido se prepara en la cocina.
- **Ejemplo:** `hmac.compare_digest(b"abc", b"abc")` compara en tiempo constante y devuelve `True`.
- **Profundiza:** <https://fastapi.tiangolo.com/tutorial/background-tasks/> y <https://core.telegram.org/bots/api>

**5. Inyectar lo que toca la red.**
- **Idea:** en vez de que tu código llame directo a Telegram, recibe una función `send` por parámetro. En producción es la real; en las pruebas es una lista que guarda lo que habría enviado.
- **Analogía:** un simulador de vuelo: mismos mandos, sin avión.
- **Ejemplo:** `enviados = []` y una función que hace `enviados.append(texto)`.
- **Profundiza:** `program/02_REFERENCE/ejemplos/patrones-arquitectura.md`.

## Calentamiento (fuera del proyecto)

En un archivo suelto (bórralo después), crea una app de FastAPI con **una** ruta `GET /hola` que devuelva `{"ok": true}`, y pruébala sin levantar ningún servidor con `TestClient`:
```
python -c "from fastapi import FastAPI; from fastapi.testclient import TestClient; app = FastAPI(); app.add_api_route('/hola', lambda: {'ok': True}); print(TestClient(app).get('/hola').json())"
```
Resultado esperado: `{'ok': True}`. Así se prueba un canal entero sin red. Después pega una ruta con un cuerpo `POST` y mira qué responde FastAPI (`422`) cuando el cuerpo está incompleto.

## Paso a paso

### Paso 0 — Prepara tu terreno
**Haz esto:** sigue los pasos 1 a 4 de la sección 7 del contrato: sincroniza `main`, comprueba que existen `src\agents\graph.py` y que `src\channels` solo trae `__init__.py`, crea la rama `issue-158-canal-web-telegram`, crea el entorno, instala el proyecto y corre `pytest tests -q`. Anota N.
**Por qué:** sin línea base no sabrás si lo que rompes es tuyo; y si `src\channels` ya tiene archivos, alguien avanzó y hay que coordinar.
**Debes ver:** `N passed`, sin fallos.
**Si falla:** si `graph.py` no existe, no empieces y comenta en el Issue con la salida como texto. Si `python --version` no dice 3.11, usa `py -3.11`.
**Punto de control:** ¿puedes decir qué hace `build_graph` y qué recibe, sin mirar?

### Paso 1 — El contrato interno: pruebas C1, C2 y C3
**Haz esto:** crea `tests\test_channel_contract.py` con C1, C2 y C3. Rojo: `No module named 'channels.contract'`. Crea `src\channels\contract.py` con `ID_PATTERN`, `MAX_CONTENT_CHARS`, `InboundEvent` y `OutboundReply` (sección 5.1) hasta ver `3 passed`.
**Por qué:** el contrato es lo único que ven los agentes. Si acepta ids raros hoy, un `thread_id` raro mañana.
**Debes ver:** el rojo por módulo ausente; luego `3 passed`.
**Si falla:** en C2, `"123\n"` debe rechazarse: tu patrón tiene que anclar el final. Si C1 no lanza al asignar, falta que el modelo sea inmutable (`frozen`).
**Punto de control:** ¿por qué el `user_id` se valida aquí y no en cada canal?

### Paso 2 — Hilo y respuesta con cita: pruebas D1 y D2
**Haz esto:** crea `tests\test_channel_dispatch.py` con D1 y D2. Para D2 arma el grafo como indica la sección 6 (fixture `store`, `ScriptedModel`, `InMemorySaver`) y controla el tiempo con un `clock` falso de dos valores. Luego `src\channels\dispatch.py` con `thread_id_for` y la parte de `handle_inbound` que invoca el grafo y arma la respuesta.
**Por qué:** si controlas el reloj, la latencia deja de ser «un número cualquiera» y pasa a ser verificable.
**Debes ver:** `2 passed`.
**Si falla:** `No checkpointer set` = armaste el grafo sin `InMemorySaver()` como último argumento. `StopIteration` = llamas a `clock()` más de dos veces.
**Punto de control:** ¿de dónde sale la lista `citations` de los metadatos?

### Paso 3 — Lo que no es texto: prueba D3
**Haz esto:** escribe D3 (voz, texto en blanco y media) y agrega la regla R1 al despachador.
**Por qué:** una nota de voz que llega al modelo como texto vacío produce respuestas absurdas. Se corta antes, con un mensaje claro, y el modelo ni se entera.
**Debes ver:** `3 passed` (D1–D3) en el archivo.
**Si falla:** si el modelo se llamó, tu comprobación va después de invocar el grafo; debe ir antes.
**Punto de control:** ¿por qué `"   "` cuenta como «sin texto»?

### Paso 4 — El bot derivado calla: pruebas D4 y D5
**Haz esto:** escribe D4 y D5. D4 manda `CLINICA` y luego `PREGUNTA` dos veces; D5 mezcla usuarios y canales. Implementa R2 y R3: lee el estado del hilo **antes** de invocar y manda `intent` y `status` solo si no había estado; para saber cuál es «la respuesta nueva», compara los `id` de los mensajes de antes y de después.
**Por qué:** es la trampa central. Si en cada mensaje mandas `status="nuevo"`, descongelas a una clienta que debía atender una persona.
**Debes ver:** `5 passed` (D1–D5).
**Si falla:** D4 rojo con una respuesta en el segundo mensaje = estás mandando `status` siempre. D5 rojo en el último = el `thread_id` no incluye el canal.
**Punto de control:** ¿qué pasaría con un hilo derivado si `thread_id_for` devolviera solo el `user_id`?

### Paso 5 — El canal web: pruebas W1, W2 y W3
**Haz esto:** crea `tests\test_channel_web.py` con W1–W3 (usa `TestClient` sobre `create_chat_app`). Luego `src\channels\web.py` (`ChatRequest`, `ChatResponse`, `build_web_router`) y `src\api\chat_app.py` con `GET /health` y el router web.
**Por qué:** FastAPI valida el cuerpo con tus modelos y responde `422` solo; tú escribes las reglas una vez. La ruta es `async`, pero el grafo es síncrono: no puede bloquear el servidor.
**Debes ver:** `3 passed`.
**Si falla:** W2 con `200` en vez de `422` = el modelo `ChatRequest` no tiene los límites. W3 con texto en la segunda respuesta = mismo error del Paso 4.
**Punto de control:** ¿qué le pasa al servidor si el grafo tarda 20 segundos y la ruta no libera el bucle?

### Paso 6 — Traducir un update de Telegram: pruebas G1, G2 y G3
**Haz esto:** crea `tests\test_channel_telegram.py` con una función auxiliar que arme *updates* y las pruebas G1–G3. Impleméntalas en `parse_update` dentro de `src\channels\telegram.py`.
**Por qué:** el adaptador es una función pura: entra un diccionario de Telegram, sale un `InboundEvent` o `None`. Lo fácil de probar es lo que no toca la red.
**Debes ver:** `3 passed` por ahora (G1–G3).
**Si falla:** mypy se queja del tipo de `type` en el `InboundEvent`: anota una variable con el mismo `Literal` del contrato.
**Punto de control:** ¿por qué un mensaje de un grupo se ignora en este canal?

### Paso 7 — El webhook: pruebas G4, G5 y G6
**Haz esto:** escribe G4–G6 y completa `build_telegram_router` y la conexión en `create_chat_app`. G4 prueba que sin secreto no pasa nada; G5 que con secreto responde 200 y `send` recibe el texto; G6 que web y Telegram dan la misma respuesta del mismo agente.
**Por qué:** es la parte de seguridad. El secreto se compara en tiempo constante y el envío se inyecta, así que el token nunca vive en el repo.
**Debes ver:** `6 passed` en `test_channel_telegram.py`.
**Si falla:** `send` vacío en G5 = el procesamiento en segundo plano no se está ejecutando; `TestClient` espera las tareas de fondo antes de devolver la respuesta. `403` con el secreto correcto = el nombre del encabezado.
**Punto de control:** ¿qué ganas respondiendo 200 antes de llamar al modelo?

### Paso 8 — Las 4 puertas y la independencia de orden
**Haz esto:** corre `pytest tests\test_health.py tests\test_handoff.py tests\test_agent_info.py -q` (no rompiste nada), las 4 puertas con el comando exacto del contrato (paso 11) y las dos pruebas aisladas del paso 12.
**Por qué:** una prueba que solo pasa si otra corrió antes es una prueba frágil.
**Debes ver:** `All checks passed!` · `Success: no issues found...` · `N+17 passed` · `No issues identified.`
**Si falla:** si bandit marca algo, léelo con calma: lo más probable es que hayas dejado un secreto o una dirección `0.0.0.0` en el código.
**Punto de control:** `git diff --name-only main`: ¿son exactamente 9 rutas y ninguna es de `src/agents/`?

### Paso 9 — Commits, PR y (opcional) la demo
**Haz esto:** haz los commits del paso 14 del contrato, sube la rama y abre el PR con `Closes #158`, la plantilla y las 3 respuestas de la sección 11. La demostración del paso 13 se hace con el monitor en la M5, no en tu PC.
**Por qué:** commits chicos se revisan en minutos.
**Debes ver:** el PR en verde en `guardian-tbd / reglas-tbd` y `CI estricto / calidad`.
**Si falla:** si el robot dice «archivo fuera de contrato», revierte ese archivo con `git restore` antes de seguir.
**Punto de control:** ¿puedes explicar en voz alta, sin mirar, las 3 preguntas de comprensión?

## Escalera de pistas (úsala solo cuando estés trabado, de arriba abajo)

**Paso 4 (D4 y D5, el bot derivado vuelve a hablar):**
- *Pista 1:* el estado del hilo se guarda entre mensajes. Lo que mandas en el segundo mensaje se mezcla con lo que ya estaba, y lo nuevo gana.
- *Pista 2:* en `tests/test_handoff.py` mira la clase `Env`: qué manda `say` en el primer mensaje y qué en los siguientes, y qué método usa para saber si el hilo ya tiene estado (`get_state`).
- *Pista 3 (en palabras):* antes de invocar, pregunta al grafo si el hilo ya tiene valores. Si no los tiene, la entrada incluye `intent` y `status` iniciales; si ya los tiene, solo mensajes, teléfono y tenant.

**Paso 4 (cuál es la respuesta nueva):**
- *Pista 1:* el resultado trae toda la conversación, no solo lo último.
- *Pista 2:* los mensajes que guarda LangGraph tienen un `id`. Mira cuáles ids había antes de invocar.
- *Pista 3 (en palabras):* guarda el conjunto de ids de antes; después, recorre el resultado de atrás hacia adelante y toma el primer mensaje de la IA cuyo id no esté en ese conjunto; si no hay ninguno, el bot calló.

**Paso 5 (la ruta no bloquea):**
- *Pista 1:* una ruta `async` que llama a una función lenta y síncrona congela a todos los demás usuarios.
- *Pista 2:* busca `asyncio.to_thread` en la documentación de Python.
- *Pista 3 (en palabras):* delega la llamada al despachador a un hilo aparte y espera su resultado con `await`.

**Paso 7 (el webhook):**
- *Pista 1:* FastAPI puede ejecutar una función **después** de enviar la respuesta.
- *Pista 2:* busca `BackgroundTasks` en la documentación de FastAPI y `hmac.compare_digest` en la de Python (recibe bytes).
- *Pista 3 (en palabras):* revisa el encabezado primero; si no coincide, error 403; si coincide, traduce el update; si hay evento, agenda en segundo plano «despachar y enviar» y devuelve `{"ok": true}` en el acto.

## Errores típicos de esta asignación

| Síntoma (lo que ves) | Causa probable | Qué hacer |
|---|---|---|
| `ValueError: No checkpointer set` | Armaste el grafo de prueba sin checkpointer | Pasa `InMemorySaver()` como último argumento de `build_graph` |
| D4 o W3: el bot contesta en el segundo mensaje | Mandas `status="nuevo"` en todos los mensajes | Solo si el hilo no tenía estado (regla R2) |
| `StopIteration` en D2 | Llamas a `clock()` más de dos veces | Una al empezar y una al terminar |
| `TypeError` por `regex` en `Field` | En Pydantic v2 el argumento se llama `pattern` | Usa `Field(pattern=...)` |
| W2 devuelve `200` con un id raro | El modelo de la petición no usa `ID_PATTERN` | Importa la constante del contrato y úsala en `ChatRequest` |
| G5: `send` quedó vacío | La tarea de fondo no se ejecuta (olvidaste agendarla) | Revisa que uses `BackgroundTasks` y que la función llame a `send` |
| G4/G5 devuelven `403` siempre | Nombre del encabezado distinto o comparas con `str` y `bytes` mezclados | Usa `SECRET_HEADER` del módulo y compara ambos como bytes |
| mypy: `Argument "type" ... incompatible type "str"` | Pasas un `str` donde el contrato pide un `Literal` | Anota la variable con `Literal["text", "media", "voice"]` |
| `422` en tu `curl` de la demo | Las comillas del JSON en cmd | Escapa las comillas dobles internas como en el contrato |
| El servidor responde a otros equipos de la red | Levantaste con `0.0.0.0` | Usa siempre `127.0.0.1` |

## Autoevaluación antes del PR

- [ ] Cada prueba del contrato la escribí yo, la vi fallar y la vi pasar.
- [ ] Puedo explicar en voz alta, sin mirar, las 3 preguntas de comprensión del contrato.
- [ ] Mi `git diff --name-only main` coincide con la sección 4 del contrato (9 archivos) y no toca `src/agents/`.
- [ ] No hay ningún token, secreto real ni teléfono real en el código, las pruebas ni el PR.
- [ ] Anoté en el PR cuántas interacciones usé con mi IA y a quién consulté.

## Prompts sugeridos para tu IA (pequeños y verificables)

**Buenos:**
1. «Explícame en 5 líneas qué hace `BackgroundTasks` de FastAPI con un ejemplo de una ruta que devuelve "ok" y luego imprime un mensaje. No uses mi proyecto.»
2. «Pego este error de pytest como texto: [error]. Explícame qué significa y qué debería mirar, sin escribirme la solución.»
3. «¿Por qué es mejor `hmac.compare_digest` que `==` para comparar un secreto? Explícalo con un ejemplo corto.»
4. «Pego la salida de `git diff --name-only main`. Compárala con esta lista de 9 archivos y dime si sobra o falta alguno.»
5. «¿Qué significa que una ruta sea `async def` si la función que llama es síncrona? Dame un ejemplo mínimo fuera de mi proyecto.»

**Prohibidos:**
- «Escribe `handle_inbound` y el webhook de Telegram por mí.» → no aprendes y el PR no es tuyo (sección 10 del contrato).
- «Dame un token de bot de Telegram de ejemplo para probar.» → ningún token ni secreto real entra al repo; el de las pruebas es una cadena inventada.
