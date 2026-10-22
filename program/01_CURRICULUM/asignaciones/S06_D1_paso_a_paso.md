# [S06 D1] Paso a paso guiado — Ejemplos para objeciones, prompt v2 y comparación de estilo (Issue #156)

> **Para quién:** practicante de 2.º año de AI Engineering, con Python básico y Git básico, que **no** conoce todavía el few-shot prompting, las expresiones regulares ni cómo comparar dos versiones de un prompt. Este archivo te acompaña **mientras trabajas**; el contrato ([`S06_D1.md`](S06_D1.md)) dice **qué** debe quedar. Aquí aprendes **cómo abordarlo sin perderte**.
>
> **Reglas del juego:** no hay código de la solución aquí (si lo hubiera, no aprenderías). Hay explicación, pistas y puntos de control. Una sesión dura ~3 h; los tiempos son una guía. Todos los comandos son para Windows (**cmd**, no PowerShell), desde la raíz del repo.
>
> **Punto de partida:** esta asignación **depende de #53** (el prompt por componentes y `check_reply_style`). El Paso 0 comprueba que ya está en `main`. Si no está, **no empieces**: comenta en el Issue #156 y espera; no escribas tú esas piezas.

> **Revisión automática de tu avance:** desde tu primer commit haz `git push -u origin <tu-rama>`. El robot abre solo un **PR en borrador** y deja **un comentario que se actualiza en cada push**: cuántos archivos del contrato ya trabajaste, cuáles te faltan, si tocaste algo fuera de la sección 4 y cuál es tu siguiente paso, con pistas. Haz push **al terminar cada paso en verde**, no solo al final.

## Mapa de la sesión

| Bloque | Tiempo | Resultado que puedes comprobar |
|---|---|---|
| Lectura + mini-conceptos | 25 min | Sabes explicar qué enseña un ejemplo (few-shot) y qué no debe traer |
| Calentamiento | 10 min | Detectas con una expresión regular un importe y una hora |
| Paso 0 (terreno, #53, entorno, línea base) | 25 min | `N passed` antes de tocar código |
| Pasos 1–2 (validador, carga y render) | 45 min | `4 passed` (F4–F7) |
| Paso 3 (tus ejemplos) | 40 min | `7 passed` (F1–F7) |
| Paso 4 (`prompt_v2`) | 15 min | `8 passed`, y las pruebas de #53 siguen en verde |
| Pasos 5–6 (mensajes, resumen, tabla y CLI) | 45 min | `5 passed` (M1–M5) |
| Pasos 7–8 (corrida real, puertas, commits y PR) | 30 min | PR abierto con `Closes #156` |

> Son ~3,5 h: si no alcanzas, **para después del Paso 4** y sigue en la siguiente. La corrida real del Paso 7 se hace con el monitor.

## Mini-conceptos (léelos antes del Paso 0)

Para cada concepto: **Idea**, **Analogía**, **Ejemplo** (fuera de este proyecto) y **Profundiza**.

**1. Few-shot prompting.**
- **Idea:** al prompt le agregas unos pocos ejemplos de «pregunta → buena respuesta». El modelo los imita en tono y forma, sin reentrenarlo.
- **Analogía:** el nuevo en la tienda que primero escucha a la asesora con experiencia atender a tres clientas.
- **Ejemplo:** para clasificar reseñas, muestras tres: «Me encantó → positiva», «Llegó roto → negativa», «Es normal → neutra».
- **Profundiza:** `program/02_REFERENCE/agent-engineering-handbook.md`, Parte III.

**2. Los ejemplos enseñan tono, no datos.**
- **Idea:** el modelo copia lo que ve. Si un ejemplo dice «cuesta S/ 50», puede repetir ese precio aunque ya no sea cierto. Los datos reales llegan siempre desde el RAG (`<fragmentos>`).
- **Analogía:** enseñar a una asesora **cómo** saludar, no el precio del día: el precio cambia.
- **Ejemplo:** un ejemplo bueno dice «Con gusto te cuento las opciones»; uno malo, «Cuesta 50 soles».
- **Profundiza:** `src/agents/info.py` (`validate_answer`).

**3. Expresión regular (`re`).**
- **Idea:** un patrón para buscar texto: «un número, dos puntos, dos números» describe una hora.
- **Analogía:** el buscar del procesador de texto, pero con comodines.
- **Ejemplo:**
```python
import re
bool(re.search(r"\d{1,2}:\d{2}", "a las 15:30"))
```
- **Profundiza:** <https://docs.python.org/3/library/re.html>

**4. Comparar con una variable controlada.**
- **Idea:** para saber si v2 mejora a v1, corres las **mismas** preguntas con los dos y comparas. Si cambiaran las preguntas, no sabrías si cambió el prompt o la pregunta.
- **Analogía:** probar dos recetas con los mismos ingredientes y el mismo horno.
- **Ejemplo:** dos listas de respuestas, una por versión, y cuentas cuántas cumplen una regla en cada una.
- **Profundiza:** `data/conversaciones/README.md` (cómo se usa el corpus en S6/S7).

**5. Probar con un ejecutor falso.**
- **Idea:** tu CLI recibe una función `runner` (en producción habla con el modelo; en las pruebas es una de mentira que anota cómo la llamaron). Así pruebas la lógica sin Ollama.
- **Analogía:** ensayar una obra con un actor suplente antes del estreno.
- **Ejemplo:** `llamadas = []` y una función que hace `llamadas.append(texto)` y devuelve `"ok"`.
- **Profundiza:** `tests/conftest.py` (`ScriptedModel` es el mismo truco).

## Calentamiento (fuera del proyecto)

En cmd, con el entorno activado:
```
python -c "import re; print(bool(re.search(r'S/\s*\d', 'cuesta S/ 50')), bool(re.search(r'\d{1,2}:\d{2}', 'te espero')))"
python -c "from agents.style import check_reply_style; print(check_reply_style('a\nb\nc\nd'), check_reply_style('¿uno? ¿dos?'))"
```
Resultado esperado: `True False` y luego `['too_many_lines'] ['too_many_questions']`. Con eso ya tienes las dos herramientas de la sesión: buscar texto con un patrón y verificar el estilo con la función de #53.

## Paso a paso

### Paso 0 — Prepara tu terreno (y comprueba #53)
**Haz esto:** sigue los pasos 1 a 4 de la sección 7 del contrato: sincroniza `main`, comprueba que existen `prompt_v1.md`, `prompt.py` y `style.py` y que `check_reply_style('hola')` imprime `[]`, crea la rama `issue-156-fewshot-objeciones`, crea el entorno, instala el proyecto y corre `pytest tests -q`. Anota N.
**Por qué:** esta asignación se apoya en el trabajo de otra compañera. Si falta, no es un problema tuyo: es una dependencia que hay que esperar.
**Debes ver:** `N passed`, sin fallos, y los tres archivos listados.
**Si falla:** si falta cualquiera de los tres, para y comenta en el Issue #156 con la salida pegada como texto. No los escribas tú.
**Punto de control:** ¿qué hace `check_reply_style` y qué códigos devuelve?

### Paso 1 — El validador de reglas: pruebas F6 y F7
**Haz esto:** crea `tests\test_fewshot.py` con una función auxiliar que construye un `FewShot` válido y con F6 y F7. Rojo: `No module named 'agents.fewshot'`. Crea `src\agents\fewshot.py` con `FewShot` y `violations` (contrato 5.2) hasta ver `2 passed`.
**Por qué:** el validador es la regla de oro de tus ejemplos. Hazlo primero con ejemplos de mentira y después lo usas con los reales.
**Debes ver:** `2 passed`.
**Si falla:** F7 rojo con los códigos en otro orden: el orden es primero estilo, luego `no_citation`, `amount` y `hour`. Si F6 no detecta `50 soles`, tu patrón del importe solo busca `S/`.
**Punto de control:** ¿por qué la falta de `[1]` es un incumplimiento y no un detalle?

### Paso 2 — Cargar y mostrar: pruebas F4 y F5
**Haz esto:** escribe F4 (formato exacto de `render_fewshots`) y F5 (id repetido en un archivo de `tmp_path`). Implementa `render_fewshots` y `load_fewshots`.
**Por qué:** el formato exacto importa: ese texto se pega al prompt que ve el modelo. Un espacio de más es un cambio de comportamiento.
**Debes ver:** `4 passed` (F4–F7).
**Si falla:** F4 se compara carácter por carácter; copia el encabezado exacto del contrato. En F5 el mensaje de error tiene que **nombrar** el id.
**Punto de control:** ¿qué cambia para el modelo si `render_fewshots` pierde la línea de encabezado?

### Paso 3 — Tus ejemplos: pruebas F1, F2 y F3
**Haz esto:** escribe F1, F2 y F3. Crea `configs\hola_mujer\fewshot_objeciones.json` con **al menos 5** ejemplos inventados por ti: «está caro», «lo consulto con mi esposo», «¿hay descuento?»… cada respuesta cálida, breve, con `[1]`, sin importes ni horas. Si F3 falla, su mensaje te dice qué ejemplo y qué regla.
**Por qué:** redactar como una asesora de Hola Mujer es la parte creativa y evaluable de la asignación.
**Debes ver:** `7 passed` (F1–F7).
**Si falla:** F2 pide los tres tipos `precio`, `consulta` y `descuento`. F3 con `no_citation` = olvidaste el `[1]`; con `too_many_questions` = hay más de un signo `?` de cierre (el `¿` de apertura no cuenta).
**Punto de control:** lee uno de tus ejemplos en voz alta: ¿lo diría una persona de verdad?

### Paso 4 — El prompt v2: prueba F8
**Haz esto:** escribe F8. Modifica **solo** `src\agents\config.py`: agrega el campo `prompt_v2` y calcúlalo como dice el contrato 5.3. Luego corre `pytest tests\test_fewshot.py tests\test_ollama.py tests\test_prompt_pieces.py -q`.
**Por qué:** `prompt` sigue siendo v1 a propósito. Cambiar el prompt activo cambia lo que le dicen a las clientas; eso se decide con evidencia, no en esta asignación.
**Debes ver:** todo en verde (F1–F8 y las pruebas de #53).
**Si falla:** si falla `C1` de #53 (`test_c1_...`), cambiaste el `prompt` activo por error. Si falla `test_config_del_tenant`, perdiste `<fragmentos>` o `[1]` del prompt.
**Punto de control:** ¿por qué `prompt_v2` empieza con el v1 completo y no lo reemplaza?

### Paso 5 — Elegir mensajes y resumir estilo: pruebas M1 y M2
**Haz esto:** crea `tests\test_compare_prompts.py` con M1 y M2. Rojo: `No module named 'evals.compare_prompts'`. Crea `src\evals\compare_prompts.py` con `CORPUS`, `StyleSummary`, `pick_conversations` y `style_summary`.
**Por qué:** para comparar dos prompts necesitas las mismas preguntas siempre. Un corpus ordenado y reglas fijas hacen que cualquiera repita tu experimento.
**Debes ver:** `2 passed`.
**Si falla:** M1 con menos de 10 mensajes = descartas de más o no estás leyendo todas las filas de la clienta. M1 con saludos = revisa el prefijo en minúsculas.
**Punto de control:** ¿por qué se ordena por `(conversacion_id, turno)` antes de elegir?

### Paso 6 — La tabla y la CLI: pruebas M3, M4 y M5
**Haz esto:** escribe M3 (tabla exacta), M4 (sin `--live`) y M5 (con `--live` y un ejecutor falso). Implementa `render_comparison`, `make_live_runner` (no se prueba) y `main`.
**Por qué:** probar la CLI con un ejecutor falso te deja verificar que cada pregunta corre con **los dos** prompts y que la tabla sale bien, sin Ollama.
**Debes ver:** `5 passed` (M1–M5). Y a mano: el comando del paso 9 del contrato imprime una tabla de 7 líneas.
**Si falla:** M5 con 4 llamadas en vez de 8 = solo corres un prompt. M4 con código 0 = no estás comprobando `--live` antes de empezar.
**Punto de control:** ¿qué mide la tabla y qué **no** mide?

### Paso 7 — La corrida real, con el monitor
**Haz esto:** con el monitor, en la M5 (Ollama encendido), corre `python -m evals.compare_prompts --live`. Pega en el PR, como texto, la tabla y dos respuestas completas (v1 y v2) a la misma pregunta.
**Por qué:** hasta aquí todo fue con ejecutores falsos; esta corrida es el único momento en que habla el modelo real. Tu conclusión sale de **sus** números.
**Debes ver:** una tabla con números reales. Si v2 empeora el estilo, también es un resultado válido.
**Si falla:** si Ollama no responde, no inventes números: anota el error y avisa en el Issue.
**Punto de control:** si repites la corrida y el resultado cambia un poco, ¿qué te dice sobre el modelo?

### Paso 8 — Puertas, commits y PR
**Haz esto:** corre las 4 puertas (paso 11 del contrato), la independencia de orden (paso 12), haz los commits del paso 13 y abre el PR con `Closes #156`, la plantilla y las 3 respuestas de la sección 11.
**Por qué:** commits chicos se revisan en minutos; un commit gigante se revisa mal.
**Debes ver:** `N+13 passed`, el CI en verde y el robot sin «archivos fuera de contrato».
**Si falla:** si el robot dice que tocaste algo fuera de la sección 4, revierte ese archivo con `git restore`.
**Punto de control:** ¿puedes explicar en voz alta, sin mirar, las 3 preguntas de comprensión?

## Escalera de pistas (úsala solo cuando estés trabado, de arriba abajo)

**Paso 1 (el orden de los códigos de `violations`):**
- *Pista 1:* la función devuelve una lista; el orden en que agregas los códigos es el orden de la lista.
- *Pista 2:* empieza con lo que devuelve `check_reply_style(shot.respuesta)` (ya es una lista) y luego agrega los tuyos.
- *Pista 3 (en palabras):* arranca con los códigos de estilo; después, uno por uno y en este orden, agrega `no_citation` si falta `[1]`, `amount` si el patrón del importe coincide y `hour` si el de la hora coincide.

**Paso 2 (el formato del render):**
- *Pista 1:* cada ejemplo son dos líneas y los ejemplos se separan con una línea en blanco.
- *Pista 2:* mira `"\n\n".join(...)` en la documentación de `str.join`.
- *Pista 3 (en palabras):* arma una lista de bloques de dos líneas cada uno, únelos con una línea en blanco, y antepón el encabezado seguido de otra línea en blanco.

**Paso 5 (los mensajes elegidos):**
- *Pista 1:* primero filtra, luego ordena, luego recorre y para cuando tengas `n`.
- *Pista 2:* `sorted` con `key` aceptando una tupla `(conversacion_id, turno)`; y un `set` para recordar los textos ya vistos (en minúsculas).
- *Pista 3 (en palabras):* quédate con las filas de la clienta del escenario de servicios, ordénalas, y para cada una descarta la que tiene pocas palabras, empieza con un saludo o un corchete, o ya viste; cuando junten `n`, corta.

**Paso 6 (la CLI con ejecutor inyectable):**
- *Pista 1:* `main` recibe dos cosas: la lista de argumentos y, aparte, el ejecutor. Si no le pasan ejecutor, usa el real.
- *Pista 2:* `argparse` con `action="store_true"` para `--live`; y `print(..., file=sys.stderr)` para el aviso.
- *Pista 3 (en palabras):* si no hay `--live`, avisa por `stderr` y sal con 2 sin tocar el ejecutor; si lo hay, elige el ejecutor, elige las preguntas, corre cada una con el prompt v1 y luego con el v2, resume cada lista e imprime la tabla.

## Errores típicos de esta asignación

| Síntoma (lo que ves) | Causa probable | Qué hacer |
|---|---|---|
| `ModuleNotFoundError: No module named 'agents.style'` | #53 todavía no está en tu `main` | Haz `git pull`; si sigue sin estar, espera: no lo escribas tú |
| F3 falla con `no_citation` | Una respuesta no lleva `[1]` | Agrega la marca `[1]` donde remitas a la información |
| F3 falla con `amount` o `hour` | Escribiste un precio u hora en un ejemplo | Quítalos: los datos salen de los fragmentos |
| F3 falla con `too_many_questions` | Tienes dos signos `?` en una respuesta | Deja una sola pregunta |
| F4 falla por un espacio | El formato se compara carácter por carácter | Copia el encabezado exacto del contrato y revisa los saltos de línea |
| Falla `C1` o `test_config_del_tenant` | Cambiaste `prompt` en vez de agregar `prompt_v2` | Deja `prompt` como lo carga #53 y agrega el campo nuevo |
| M1 devuelve menos de 10 mensajes | Filtras de más o lees solo las primeras filas | Recorre todo el archivo y filtra al final |
| M5 hace 4 llamadas | Corres solo uno de los dos prompts | Cada pregunta se corre con `cfg.prompt` y con `cfg.prompt_v2` |
| `UnicodeDecodeError` al leer el corpus | Falta la codificación al abrir el archivo | Lee con `encoding="utf-8"` |
| La línea `python -c` de la tabla falla en cmd | Comillas mal anidadas | Comillas dobles por fuera, simples por dentro |

## Autoevaluación antes del PR

- [ ] Cada prueba del contrato la escribí yo, la vi fallar y la vi pasar.
- [ ] Mis ejemplos los redacté yo; ninguno trae precios, horas ni datos de personas.
- [ ] `prompt` sigue siendo v1 y `prompt_v2` es un campo aparte; no toqué `wiring.py`.
- [ ] Puedo explicar en voz alta, sin mirar, las 3 preguntas de comprensión del contrato.
- [ ] Mi `git diff --name-only main` coincide con la sección 4 del contrato (6 archivos).
- [ ] Pegué en el PR la tabla de la corrida real y dos respuestas completas.
- [ ] Anoté en el PR cuántas interacciones usé con mi IA y a quién consulté.

## Prompts sugeridos para tu IA (pequeños y verificables)

**Buenos:**
1. «Explícame en 5 líneas qué es el few-shot prompting con un ejemplo de clasificar reseñas. No uses mi proyecto.»
2. «Pego este error de pytest como texto: [error]. Explícame qué significa y qué debería mirar, sin escribirme la solución.»
3. «Este es uno de mis ejemplos de respuesta: [texto]. ¿Suena cálido y breve? Dime qué cambiarías, pero no lo reescribas.»
4. «¿Qué hace `re.search(r"\d{1,2}:\d{2}", texto)`? Explícalo con 3 ejemplos de texto que coinciden y 3 que no.»
5. «Pego la salida de `git diff --name-only main`. Compárala con esta lista de 6 archivos y dime si sobra o falta alguno.»

**Prohibidos:**
- «Escribe 5 ejemplos de objeciones para Hola Mujer.» → redactarlos es lo que se evalúa; si los escribe la IA, el PR no es tuyo (sección 10 del contrato).
- «Activa el prompt v2 en el agente para que todos lo usen.» → cambiar el prompt activo es una decisión del monitor con la evidencia de la tabla, fuera de esta asignación.
