# [S07 D3] Paso a paso guiado — El agente propone horarios libres y pruebas de colisión (Issue #185)

> **Para quién:** practicante de 2.º año de AI Engineering, con Python básico y Git básico, que **no** conoce todavía las piezas nuevas de esta asignación. Este archivo te acompaña **mientras trabajas**; el contrato (`program/01_CURRICULUM/asignaciones/S07_D3.md`) dice **qué** debe quedar. Aquí aprendes **cómo abordarlo sin perderte**.
>
> **Reglas del juego:** no hay código de la solución aquí (si lo hubiera, no aprenderías). Hay explicación, pistas y puntos de control. Una sesión de práctica dura ~3 h; los tiempos son una guía, no una exigencia.

## Mapa de la sesión

| Bloque | Tiempo | Resultado que puedes comprobar |
|---|---|---|
| Calentamiento y lectura | 30 min | Sabes dónde pregunta abierto hoy el nodo y qué hace `_offer` |
| Pasos 1–4 (O1–O7) | 75 min | La oferta funciona y las 8 pruebas en rojo pasan a verde |
| Pasos 5–6 (O8–O10) | 45 min | Colisión tras ofrecer, conversación completa e idempotencia |
| Cierre y PR | 30 min | PR abierto con `Closes #185` |

## Mini-conceptos (léelos antes del Paso 0)

**1. Ofrecer es leer; reservar es escribir.** Proponer horarios solo consulta el calendario. Reservar cambia el mundo y por eso va después de la aprobación. *Analogía:* mirar la pizarra de turnos de una peluquería no ocupa ningún turno. *Ejemplo (fuera del proyecto):* `libres = [h for h in range(9, 12) if h not in ocupadas]`. *Profundiza:* `program/02_REFERENCE/ejemplos/s7-tools-y-citas/README.md`.

**2. `interrupt()` y `Command(resume=...)`.** `interrupt(valor)` detiene el grafo y guarda su estado; el grafo se retoma con `Command(resume=respuesta)` y el mismo `thread_id`. Necesita un checkpointer (en pruebas, `InMemorySaver`). *Analogía:* poner un marcador y cerrar el libro. *Ejemplo:* `g.invoke(Command(resume={"ok": True}), {"configurable": {"thread_id": "t1"}})`. *Profundiza:* <https://langchain-ai.github.io/langgraph/> (busca *human-in-the-loop* y *persistence*; verifícalo ahí).

**3. Nodo puro.** Dado el mismo estado, devuelve lo mismo y no escribe en ningún lado. Reanudar un checkpoint puede volver a ejecutarlo; si fuera impuro, repetiría efectos. *Ejemplo:* `def doble(x): return x * 2`.

**4. Idempotencia.** Repetir la misma petición produce el mismo resultado sin duplicar. Aquí lo da una clave calculada con teléfono, servicio y hora (`idempotency_key`). *Analogía:* tocar el timbre dos veces no llama a dos porteros.

## Calentamiento (fuera del proyecto)

En un archivo suelto: una lista de horas `[15, 16, 17, 18]`, un conjunto de ocupadas `{15, 16}` y un generador que devuelva las **2 primeras libres**. Resultado esperado: `[17, 18]`. Bórralo después. Idea: filtrar de forma perezosa y cortar al llegar a N.

## Paso a paso

### Paso 0 — Prepara tu terreno
**Haz esto:** rama `issue-185-oferta-horarios` desde `main`; corre `pytest tests -q` y anota el total (línea base). Lee en `src/agents/booking.py` `_alternatives`, `_offer` y la rama «falta fecha u hora» de `draft_node`; y el helper `Env` de `tests/test_booking_flow.py`.
**Por qué:** sin línea base no puedes demostrar que el total subió exactamente en 10.
**Debes ver:** todo en verde y un número de pruebas anotado.
**Si falla:** ruta inexistente o prueba en rojo en `main` → repórtalo en el Issue con el error pegado.
**Punto de control:** ¿puedes decir en voz alta qué responde hoy el agente si falta la hora y qué cambia el contrato?

### Paso 1 — Oferta con calendario vacío: prueba O1
**Haz esto:** crea `tests/test_booking_offers.py` con los imports a nivel de módulo (`Env` viene de `test_booking_flow`), un par de helpers pequeños para armar las fechas y leer las líneas `• `, y la prueba `test_o1_...`. Córrela en rojo. Implementa lo mínimo en `src/agents/booking.py`. Verde. Commit pequeño.
**Por qué:** es el caso base; todo lo demás es una variación.
**Debes ver:** en rojo, `AssertionError` por falta de `Tengo libre`; después, 3 líneas con `fmt_slot`.
**Si falla:** `ImportError` → revisa el nombre del módulo y que estés en la raíz del repo; ese no es el rojo correcto.
**Punto de control:** ¿tu cambio sigue mostrando «Atendemos de 15:00 a 19:00»?

### Paso 2 — Lo ocupado no se ofrece: prueba O2
**Haz esto:** escribe `test_o2_...` reservando directo en el calendario dos horarios; córrela, observa si ya pasa o falla; ajusta lo mínimo.
**Por qué:** es la regla central: cero colisiones.
**Debes ver:** las líneas saltan lo reservado y pasan al día siguiente.
**Si falla:** revisa que la reserva ajena use la hora con zona Lima.
**Punto de control:** ¿quién decide qué está libre, tu nodo o el puerto del calendario?

### Paso 3 — Falta solo la hora: prueba O3
**Haz esto:** `test_o3_...` con el modelo falso que devuelve fecha y `null` de hora.
**Por qué:** el contrato dice «fecha u hora»; no solo «ambas».
**Debes ver:** las mismas 3 líneas y `booking_needs_info`.
**Si falla:** revisa la condición de la rama (¿mira ambos campos?).
**Punto de control:** ¿qué pasa si dan fecha y hora completas? El comportamiento no debe cambiar.

### Paso 4 — No escribe ni pausa: prueba O4
**Haz esto:** `test_o4_...`: sin `__interrupt__`, calendario vacío, `status == "active"`, 3 líneas y cada horario ofrecido aún libre.
**Por qué:** ofrecer no reserva.
**Debes ver:** verde (con tu implementación ya debería pasar; si no, algo escribe).
**Si falla:** busca llamadas a `book` en tu cambio: no debe haber.
**Punto de control:** ¿por qué esta prueba protege el nodo puro?

### Paso 5 — Día lleno: prueba O5
**Haz esto:** `test_o5_...` reservando los 4 inicios del lunes.
**Por qué:** verifica el cambio de día y el orden cronológico.
**Debes ver:** la primera línea es el martes a las 3:00 pm.
**Si falla:** ¿estás usando `upcoming_starts` con el «ahora» del reloj inyectado?
**Punto de control:** ¿de dónde sale «ahora»: `datetime.now()` o `deps.clock()`?

### Paso 6 — Quedan solo 2: prueba O6
**Haz esto:** `test_o6_...`: reserva todos los inicios de `upcoming_starts(NOW)` salvo los dos últimos.
**Por qué:** «de 2 a 3»: con 2 libres hay 2 líneas, no se rellena.
**Debes ver:** exactamente 2 líneas, las dos últimas del horizonte.
**Si falla:** revisa si fuerzas siempre 3.
**Punto de control:** ¿cuál es el máximo de líneas y quién lo fija?

### Paso 7 — Nada libre: prueba O7
**Haz esto:** `test_o7_...`: todos reservados. Compara con `FAIL`.
**Por qué:** el caso límite: sin oferta no se inventa nada.
**Debes ver:** el texto `FAIL`, `booking_failed`, sin `• `.
**Si falla:** ¿tu rama vacía reutiliza `_offer`, que ya maneja ese caso?
**Punto de control:** ¿por qué es mejor derivar a una persona que inventar un horario?

### Paso 8 — Choque tras ofrecer: prueba O8
**Haz esto:** `test_o8_...` con dos respuestas del modelo falso: primero falta todo, luego fecha y hora del lunes 3 pm. Entre ambos turnos, reserva ese horario directo.
**Por qué:** entre la oferta y la elección el horario puede ocuparse.
**Debes ver:** «ya está ocupado», sin pausa, nueva lista sin ese horario; en el calendario solo la reserva ajena.
**Si falla:** si pasa de entrada, es correcto: ya describe comportamiento existente.
**Punto de control:** ¿qué distingue esta validación de la del nodo de commit?

### Paso 9 — Conversación completa: prueba O9
**Haz esto:** `test_o9_...`: turno 1 (oferta), turno 2 (martes 4 pm → `__interrupt__`), luego `env.resume({"approved": True})`.
**Por qué:** demuestra el flujo entero con `interrupt()` y `Command(resume=...)` sobre el mismo `thread_id`.
**Debes ver:** una sola cita, HM-FAC-001, martes 20/10 16:00 Lima, y `booking_confirmed`.
**Si falla:** revisa que uses `Env.resume` (mismo `thread_id`) y el orden de las respuestas del modelo falso.
**Punto de control:** ¿qué pasaría sin checkpointer?

### Paso 10 — Mismo `request_id` no duplica: prueba O10
**Haz esto:** `test_o10_...`: tras O9 (repite los pasos dentro de la misma función), invoca `env.deps.tool` dos veces con los mismos argumentos.
**Por qué:** la clave de idempotencia evita la cita doble.
**Debes ver:** `already_booked` en ambas y 1 sola cita.
**Si falla:** ¿pasaste `start` como texto ISO con zona?
**Punto de control:** ¿qué datos entran en la clave?

### Paso 11 — Puertas, commits y PR
**Haz esto:** cada ID aislado con `pytest tests -q -k test_o1_` (…`test_o10_`); las 4 puertas; el total subió en 10; `git diff --name-only main` = 2 rutas. PR con `Closes #185` y las respuestas de comprensión.
**Por qué:** es el criterio de «hecho».
**Debes ver:** todo verde y las 2 rutas.
**Si falla:** pega el error como texto en el Issue.
**Punto de control:** ¿puedes responder sin mirar las 3 preguntas del contrato?

## Escalera de pistas (úsala solo cuando estés trabado, de arriba abajo)

**Rama «falta fecha u hora» (O1–O3).** Pista 1: ya existe una pieza que lista horarios libres tras un choque; la oferta proactiva es la misma idea con otro motivo. Pista 2: mira `_offer` y `_alternatives` en `src/agents/booking.py` y la doc de LangGraph (<https://langchain-ai.github.io/langgraph/>, nodos como funciones del estado). Pista 3: en la rama que hoy hace la pregunta abierta, usa esa pregunta como introducción de la lista de horarios, sin tocar el resto del nodo.

**Reanudar (O9).** Pista 1: el grafo se pausó y hay que decirle con qué respuesta seguir. Pista 2: `Command(resume=...)` e `InMemorySaver` en la doc (sección *human-in-the-loop*; verifícalo). Pista 3: usa el helper `resume` de `Env` en vez de llamar al grafo con un mensaje nuevo.

**Reservas de prueba (O2, O5–O7).** Pista 1: el calendario en memoria acepta reservas ajenas con cualquier clave. Pista 2: mira `InMemoryCalendar.book`. Pista 3: arma un helper que reserve un inicio con una clave inventada distinta cada vez.

## Errores típicos de esta asignación

| Síntoma (lo que ves) | Causa probable | Qué hacer |
|---|---|---|
| `ImportError: cannot import name 'Env'` | Ejecutas desde otra carpeta o el módulo no se llama `test_booking_flow` | Corre pytest desde la raíz del repo |
| La oferta incluye un horario ocupado | Comparas sin zona horaria | Usa los datetimes con zona Lima y el puerto del calendario |
| `test_falta_fecha_u_hora_pregunta_con_el_horario` se rompe | Cambiaste el texto de la pregunta | Mantén la pregunta tal cual y agrega la lista después |
| La conversación no reanuda | `thread_id` distinto o falta checkpointer | Usa el `Env` y su `resume` |
| Siempre 3 líneas aunque queden 2 | Rellenas la lista | Ofrece solo los libres que existan |

## Autoevaluación antes del PR

- [ ] Cada prueba del contrato la escribí yo, la vi fallar y la vi pasar.
- [ ] Puedo explicar en voz alta, sin mirar, las 3 preguntas de comprensión del contrato.
- [ ] Mi `git diff --name-only main` coincide con la sección 4 del contrato.
- [ ] Anoté en el PR cuántas interacciones usé con mi IA y a quién consulté.

## Prompts sugeridos para tu IA (pequeños y verificables)

1. «Explícame `interrupt()` y reanudar con un ejemplo de aprobar un gasto, sin código de mi repo.»
2. «Este es el error de pytest (pego el texto): ¿qué significa? No me des el arreglo.»
3. «Mis casos de colisión son: [lista]. ¿Qué escenario de calendario lleno o ocupado me falta?»
4. «Compara mi `git diff --name-only main` con estas 2 rutas permitidas.»

**Prohibidos:** «escribe el cambio de `src/agents/booking.py` o las pruebas O1–O10» (es lo que se evalúa) y «redacta mi PR y mis commits» (firmas tú lo que subes).
