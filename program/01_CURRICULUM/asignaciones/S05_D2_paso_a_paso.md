# [S05 D2] Paso a paso guiado — Prompt por componentes y verificación de estilo (Issue #53)

> **Para quién:** practicante de 2.º año de AI Engineering, con Python básico y Git básico, que **no** conoce todavía los prompts por componentes, las expresiones regulares ni los modelos de Pydantic. Este archivo te acompaña **mientras trabajas**; el contrato ([`S05_D2.md`](S05_D2.md)) dice **qué** debe quedar. Aquí aprendes **cómo abordarlo sin perderte**.
>
> **Reglas del juego:** no hay código de la solución aquí (si lo hubiera, no aprenderías). Hay explicación, pistas y puntos de control. Una sesión dura ~3 h; los tiempos son una guía. Todos los comandos son para Windows (**cmd**, no PowerShell), desde la raíz del repo.
>
> **Punto de partida:** esta asignación se apoya en el agente real que ya está en `main` (RAG con citas, agendar con aprobación, derivación a una persona). El Paso 0 lo comprueba. Si tenías avanzado el contrato anterior (el del servicio de conversación y el grafo propio), **para y pregunta en el Issue #53**: parte de lo que hiciste se aprovecha.

> **Revisión automática de tu avance:** desde tu primer commit haz `git push -u origin <tu-rama>`. El robot abre solo un **PR en borrador** y deja **un comentario que se actualiza en cada push**: cuántos archivos del contrato ya trabajaste, cuáles te faltan, si tocaste algo fuera de la sección 4 y cuál es tu siguiente paso, con pistas (no con la solución). Léelo antes de seguir con el paso siguiente; si no lo entiendes, usa `/pista`. Haz push **al terminar cada paso en verde**, no solo al final. Cuando acabes, marca el PR *Ready for review* y responde la sección 11.

## Mapa de la sesión

| Bloque | Tiempo | Resultado que puedes comprobar |
|---|---|---|
| Lectura + mini-conceptos | 25 min | Sabes explicar por qué el prompt va en piezas y qué hace que una respuesta incumpla el estilo |
| Calentamiento | 15 min | Separas un texto por encabezados y cuentas sus líneas con texto |
| Pasos 0–2 (terreno, entorno, línea base; `pip install` puede tardar en PCs antiguas) | 30 min | `N passed` antes de tocar código |
| Pasos 3–8 (las 15 pruebas, en grupos) | 70 min | Las 15 pruebas escritas y el rojo completo (2 errores de colección) |
| Pasos 9–12 (código, conexión, regresión) | 50 min | `N+15 passed` y `True True` |
| Pasos 13–14 (4 puertas, commits y PR) | 30 min | PR abierto con `Closes #53` |

> Son ~3,5 h: si no alcanzas en una sesión, **para después del Paso 8** (rojo completo) y sigue en la siguiente.

## Mini-conceptos (léelos antes del Paso 0)

Para cada concepto: **Idea**, **Analogía**, **Ejemplo** (fuera de este proyecto) y **Profundiza**.

**1. Prompt por componentes.**
- **Idea:** en vez de un texto largo y enredado, el prompt se escribe en piezas con un propósito cada una (quién eres, cómo hablas, qué no haces, de dónde sacas los datos, qué recuerdas). El código las junta.
- **Analogía:** un manual de la tienda con capítulos: si cambia el horario, editas un capítulo, no reescribes el manual.
- **Ejemplo:** `piezas = ["Eres un guía.", "Hablas breve."]` y luego `"\n\n".join(piezas)`.
- **Profundiza:** `program/02_REFERENCE/agent-engineering-handbook.md`, Parte III.

**2. Verificar no es corregir.**
- **Idea:** una función de verificación mira un texto y dice **qué incumple**; no lo cambia. Quien decide qué hacer con el aviso es otra parte del sistema.
- **Analogía:** el revisor del examen marca con rojo los errores, no escribe las respuestas por ti.
- **Ejemplo:** `def es_corto(texto): return len(texto) <= 10` responde sí o no; no recorta nada.
- **Profundiza:** <https://docs.python.org/3/tutorial/controlflow.html#defining-functions>

**3. Expresión regular (`re`).**
- **Idea:** es un patrón para buscar texto: «un número, dos puntos, dos números», «una línea que empieza con `## `».
- **Analogía:** el buscar-y-reemplazar del procesador de texto, pero con comodines.
- **Ejemplo:**
```python
import re
re.findall(r"\d+", "tengo 3 gatos y 12 peces")  # ['3', '12']
```
- **Profundiza:** <https://docs.python.org/3/library/re.html>

**4. Modelo de Pydantic inmutable (`frozen`).**
- **Idea:** una clase que valida sus campos al crearse y, si es `frozen`, no se puede modificar después.
- **Analogía:** un formulario sellado: lo llenas una vez y ya no se corrige a mano.
- **Ejemplo:**
```python
from pydantic import BaseModel, ConfigDict
class Punto(BaseModel):
    model_config = ConfigDict(frozen=True)
    x: int
```
- **Profundiza:** <https://docs.pydantic.dev/latest/concepts/models/>

**5. Datos, no instrucciones (inyección de prompt).**
- **Idea:** lo que escribe la clienta llega dentro del prompt. Si el modelo lo trata como una orden («ignora tus reglas»), cualquiera puede manejar al bot. Por eso el prompt dice que ese texto es **dato**.
- **Analogía:** un cajero que lee en voz alta el papel que le entrega el cliente, sin obedecerlo si dice «dame todo el dinero».
- **Profundiza:** OWASP Top 10 para aplicaciones con LLM (<https://genai.owasp.org/>) y `program/03_ARCHITECTURE/decisions/ADR-009-harness-seguridad.md`.

## Calentamiento (fuera del proyecto)

Haz esto en el Escritorio, **fuera del repo**, en un archivo `practica_texto.py`:

1. Escribe en una variable un texto de tres secciones, cada una con un encabezado `## Nombre` y una o dos líneas debajo.
2. Con `re.findall`, obtén la lista de los nombres de los encabezados.
3. Con `re.split`, obtén el texto de cada sección. Cuenta cuántas líneas **con texto** (no en blanco) tiene cada una.

**Resultado esperado:** tres nombres y tres conteos. Luego investiga una pregunta: ¿qué devuelve `re.split` con el texto que hay **antes** del primer encabezado? Esa pregunta te servirá en el Paso 10. Borra el archivo al terminar.

## Paso a paso

### Paso 0 — Prepara tu terreno
**Haz esto:** en cmd, desde la raíz del repo:
```bat
git checkout main
git pull
dir src\agents\config.py
dir configs\hola_mujer\prompt.md
```
**Por qué:** esta asignación modifica `config.py` y reemplaza `prompt.md`. Si no están, tu copia de `main` está vieja o algo falló.
**Debes ver:** `Already up to date.` o commits nuevos; `dir` lista los dos archivos.
**Si falla:** si `dir` no encuentra alguno, **para**. Comenta en el Issue #53 con la salida pegada como texto (contrato, sección 12). No crees esos archivos tú mismo.
**Punto de control:** abre `configs\hola_mujer\prompt.md`: ¿cuántas reglas tiene y a cuál de las cinco piezas del contrato pertenece cada una?

### Paso 1 — Rama y entorno virtual
**Haz esto:**
```bat
git checkout -b issue-53-system-prompt
py -3.11 -m venv .venv
.venv\Scripts\activate
python --version
python -m pip install -e ".[dev]"
pre-commit install
```
**Por qué:** una rama por Issue (TBD) y un entorno aislado evitan mezclar tu trabajo con `main` y con otros proyectos de tu PC. `pre-commit` corre ruff en cada commit (AGENTS.md).
**Debes ver:** `Switched to a new branch 'issue-53-system-prompt'`; el prompt empieza con `(.venv)`; `Python 3.11.x`; `pip` termina con `Successfully installed ...`; `pre-commit installed at ...`.
**Si falla:** si `py -3.11` no existe, instala Python 3.11 (no 3.12 ni 3.13; ver `program/02_REFERENCE/stack-versiones.md`). Si PowerShell bloquea la activación, usa cmd. Si `pip` falla, pega el error completo en el Issue.
**Punto de control:** ¿qué te dice `git branch --show-current`? Debe llevar el número 53.

### Paso 2 — Línea base (sin tu código)
**Haz esto:**
```bat
pytest tests -q
```
**Por qué:** si algo ya está en rojo antes de tu código, sabrás que no lo causaste tú.
**Debes ver:** `N passed`, sin fallos. Anota N. Al terminar, el total debe ser N+15.
**Si falla:** para y repórtalo en el Issue (contrato, sección 12). No lo arregles en esta rama.
**Punto de control:** ¿cuál es tu N?

> **Antes de los pasos 3–8:** crea `tests\test_reply_style.py` y `tests\test_prompt_pieces.py` y ve añadiendo funciones **por grupos**. **No implementes nada hasta el Paso 9**: así lo pide el contrato (sección 6, nota «Rojo correcto»). Nombra cada función con su ID al inicio (`test_s1_...`, `test_p3_...`, `test_c1_...`) para poder aislarla con `-k`.

### Paso 3 — S1 a S4: lo que SÍ cumple el estilo (y lo vacío)
**Haz esto:** en `tests\test_reply_style.py`, escribe S1, S2, S3 y S4 (sección 6 del contrato): una respuesta normal, la cadena vacía, una cadena de solo espacios y saltos, y una de exactamente tres líneas. Importa `check_reply_style` de `agents.style`.
**Por qué:** antes de probar lo que incumple, fijas qué es una respuesta válida y qué cuenta como vacío.
**Debes ver:** si corres el archivo, `ModuleNotFoundError: No module named 'agents.style'` (rojo correcto: el módulo no existe aún).
**Si falla:** si el error es `SyntaxError` o `NameError`, corrígelo primero: un rojo por otra razón no vale.
**Punto de control:** ¿por qué una cadena de solo espacios cuenta como vacía y no como una respuesta de una línea?

### Paso 4 — S5 a S8: lo que NO cumple el estilo
**Haz esto:** escribe S5 (cuatro líneas), S6 (líneas en blanco que no cuentan), S7 (dos signos `?`) y S8 (ambos incumplimientos, **en el orden** `too_many_lines`, `too_many_questions`).
**Por qué:** S6 y S8 son las que revelan decisiones de diseño: ¿se cuentan las líneas en blanco? ¿en qué orden salen los códigos?
**Debes ver:** el mismo error de colección del paso anterior.
**Si falla:** si tu S8 compara con un orden distinto al del contrato, corrígelo: el contrato manda.
**Punto de control:** ¿cuántas líneas «con texto» tiene `"uno\n\ndos\n\nFuente: tres"` y por qué debe cumplir?

### Paso 5 — P2: la composición del prompt
**Haz esto:** en `tests\test_prompt_pieces.py`, escribe P2: crea un `PromptPieces` con los textos `a` a `e` y comprueba que `compose_system_prompt` devuelve exactamente la cadena de la fila P2. Importa de `agents.prompt`.
**Por qué:** es el contrato más pequeño de las piezas: orden y separador. Se prueba sin leer ningún archivo.
**Debes ver:** `ModuleNotFoundError: No module named 'agents.prompt'`.
**Si falla:** revisa que los campos se llamen como en la sección 5.2 (en inglés).
**Punto de control:** ¿qué pasaría si la composición usara una sola línea en vez de dos saltos de línea?

### Paso 6 — P3, P4 y P5: archivos mal formados
**Haz esto:** escribe P3 (falta `Memoria`; el error debe nombrarla), P4 (una pieza vacía) y P5 (un encabezado de más **y** dos encabezados intercambiados, en la misma función). Los archivos de prueba se crean en `tmp_path`. Te conviene una función auxiliar que escriba un archivo con los encabezados y textos que le pases.
**Por qué:** un cargador que acepta archivos mal formados deja pasar errores en silencio. Estas pruebas fijan que se rechazan con un mensaje útil.
**Debes ver:** el mismo error de colección.
**Si falla:** si no recuerdas cómo esperar una excepción y revisar su mensaje, mira la Escalera de pistas (Paso 6).
**Punto de control:** ¿por qué el mensaje de P3 debe nombrar `Memoria` en vez de decir solo «archivo inválido»?

### Paso 7 — P1, P6 y C1: el archivo real
**Haz esto:** escribe P1 (el archivo real carga las cinco piezas), P6 (el prompt compuesto cumple las reglas de contenido de la sección 5.3 y no tiene precios ni horas) y C1 (la configuración del tenant usa el prompt compuesto). Calcula la ruta del archivo real desde `__file__`.
**Por qué:** estas tres pruebas son las que vigilan tu `prompt_v1.md`: si mañana alguien le borra la regla de la cita `[1]`, P6 lo detecta.
**Debes ver:** el mismo error de colección.
**Si falla:** si tu ruta es absoluta (`C:\Users\...`), no funcionará en otra PC. Calcúlala desde el archivo de prueba.
**Punto de control:** ¿qué regla del contrato (sección 5.3) se rompería en silencio si no existiera P6?

### Paso 8 — El rojo completo
**Haz esto:**
```bat
pytest tests -q
```
**Por qué:** confirma que **las 15 pruebas están escritas** y que ninguna se implementó todavía.
**Debes ver:** `ERROR collecting tests/test_prompt_pieces.py` con `No module named 'agents.prompt'`, `ERROR collecting tests/test_reply_style.py` con `No module named 'agents.style'`, y `Interrupted: 2 errors during collection`.
**Si falla:** si el rojo es por otra causa, corrígela antes de seguir.
**Punto de control:** ¿cuántas funciones `test_` tienes entre los dos archivos? Deben ser 15.

### Paso 9 — Implementa `style.py`
**Haz esto:** crea `src\agents\style.py` con `check_reply_style` (sección 5.4). Luego:
```bat
pytest tests\test_reply_style.py -q
```
**Por qué:** es la pieza más chica y autónoma: te da el primer verde y el hábito de ir de rojo a verde.
**Debes ver:** `8 passed`.
**Si falla:** lee el error de abajo hacia arriba; la última línea suele nombrar la causa. Si falla S8, revisa el orden en que agregas los códigos.
**Punto de control:** ¿tu función lee algún archivo o llama a algo externo? No debe: es pura.

### Paso 10 — El prompt en cinco piezas y su cargador
**Haz esto:** en este orden:
- a. Crea `configs\hola_mujer\prompt_v1.md` partiendo `prompt.md` en las cinco piezas (sección 5.1 y 5.3). **La redacción es tuya**; no pierdas ninguna regla.
- b. Crea `src\agents\prompt.py` (sección 5.2).

Luego `pytest tests\test_prompt_pieces.py -q`.
**Por qué:** primero el contenido y después el código que lo lee: así ves si tu archivo cumple el formato.
**Debes ver:** pasan todas **menos C1** (falta conectar la configuración). P6 es la más exigente: si falla, el mensaje te dice qué frase falta.
**Si falla:** si el mensaje de P3 no nombra `Memoria`, revisa cómo armas el texto del error. Si P6 falla por una hora o un precio, quítalos: el prompt no lleva datos del negocio.
**Punto de control:** ¿qué regla de `prompt.md` fue la más difícil de ubicar en una pieza, y por qué la pusiste donde la pusiste?

### Paso 11 — Conecta la configuración y borra el prompt viejo
**Haz esto:**
- a. `src\agents\config.py`: que el campo `prompt` salga del archivo nuevo, compuesto (sección 5.5). Nada más en ese archivo.
- b. Recién ahora: `git rm configs\hola_mujer\prompt.md`.

Luego `pytest tests -q`.
**Por qué:** el orden importa. Si borras `prompt.md` antes de cambiar `config.py`, el agente deja de cargar su prompt.
**Debes ver:** `N+15 passed`, sin `failed` ni `error`.
**Si falla:** si falla `test_config_del_tenant` (en `tests\test_ollama.py`), tu prompt perdió `<fragmentos>` o `[1]`: vuelve a la sección 5.3.
**Punto de control:** ¿qué cambiaste en `config.py` y qué **no** cambiaste?

### Paso 12 — Regresión y la verificación a mano
**Haz esto:**
```bat
pytest tests\test_ollama.py tests\test_evals.py -q
python -c "from pathlib import Path; from agents.prompt import *; t = compose_system_prompt(load_prompt_pieces(Path('configs/hola_mujer/prompt_v1.md'))); print('[1]' in t, '<fragmentos>' in t)"
dir configs\hola_mujer\prompt.md
```
**Por qué:** las pruebas existentes (las de configuración y los 12 escenarios del agente) deben seguir verdes sin que las toques, y el comando comprueba con tus ojos lo más importante.
**Debes ver:** `19 passed`; `True True`; y `dir` dice que no encuentra `prompt.md`.
**Si falla:** si los evals fallan, tu prompt rompió algo del agente: revisa la sección 5.3.
**Punto de control:** ¿por qué los evals del agente siguen pasando aunque no tocaste el agente?

### Paso 13 — Las 4 puertas y la independencia de orden
**Haz esto:**
```bat
ruff check src tests && mypy src --ignore-missing-imports && pytest tests -q && bandit -r src -x tests -ll
pytest tests\test_reply_style.py -k s5 -q
pytest tests\test_prompt_pieces.py -k p2 -q
```
**Por qué:** es lo mismo que corre el CI estricto; si pasa aquí, no te sorprende en GitHub. Y una prueba que solo pasa en cierto orden no es confiable.
**Debes ver:** `All checks passed!` · `Success: no issues found in ... source files` · `N+15 passed` · `No issues identified.`; y después `1 passed, 7 deselected` y `1 passed, 6 deselected`.
**Si falla:** corrígelo antes de commitear. No apagues mypy ni ruff (contrato, sección 9). Si `ruff` te sugiere cambiar `"\n\n".join(...)`, haz lo que pide: está en las reglas del repo.
**Punto de control:** ¿pasó todo sin apagar ninguna regla (sin `--ignore`, sin `noqa` global)?

### Paso 14 — Commits pequeños, push y PR
**Haz esto:** haz los seis commits de la sección 7, paso 12 del contrato, **uno por cambio**: para cada uno, `git add` solo de sus rutas (nunca `git add .`) y luego `git commit -m` con el mensaje indicado. Después:
```bat
git push -u origin issue-53-system-prompt
```
Abre el PR contra `main` con `Closes #53`, la plantilla completa y tus respuestas de la sección 11 del contrato.
**Por qué:** commits pequeños dejan historia legible; el PR es la evidencia que el monitor revisa contra el contrato.
**Debes ver:** cada hook de pre-commit imprime `Passed`; `branch 'issue-53-system-prompt' set up to track 'origin/issue-53-system-prompt'`; en el PR, `guardian-tbd / reglas-tbd` y `CI estricto / calidad` en verde.
**Si falla:** si un hook modifica archivos, haz `git status --short`, `git add` de esos archivos y repite **el mismo** commit. No uses `--no-verify`. Si el guardián rechaza el PR, revisa el nombre de la rama y el `Closes #53`.
**Punto de control:** antes de abrir el PR, ¿respondiste las 4 preguntas de la sección 11 con tus palabras? Si no, ensaya con `/comprension`.

## Escalera de pistas (úsala solo cuando estés trabado, de arriba abajo)

**Paso 4 (S6 y S8).** Pista 1: piensa qué significa «línea con texto»: una línea que no está vacía después de quitar espacios. Pista 2: busca `splitlines` y `strip` en <https://docs.python.org/3/library/stdtypes.html#str.splitlines>. Pista 3: cuentas las líneas que, tras `strip()`, no quedan vacías; los códigos los agregas a una lista en el orden en que evalúas las reglas.

**Paso 6 (P3 a P5).** Pista 1: `pytest.raises` puede comprobar también el mensaje de la excepción. Pista 2: busca el parámetro `match` en <https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions>. Pista 3: dentro de `with pytest.raises(ValueError, match="..."):` llamas al cargador con tu archivo mal formado.

**Paso 7 (P6).** Pista 1: una expresión regular puede buscar «una `S`, una `/`, espacios opcionales y dígitos». Pista 2: busca `re.search` en <https://docs.python.org/3/library/re.html>; `\d` es un dígito y `\s*` son espacios opcionales. Pista 3: para la hora, el patrón es «uno o dos dígitos, dos puntos, dos dígitos»; combina los dos patrones con `|`.

**Paso 10 (el cargador).** Pista 1: el archivo es texto con encabezados; piensa en la práctica del calentamiento. Pista 2: busca `re.findall` y `re.split` con la bandera `re.MULTILINE` en <https://docs.python.org/3/library/re.html#re.MULTILINE>. Pista 3: primero comparas la lista de encabezados con la esperada (así detectas faltantes, sobrantes y orden); después separas los textos y creas el modelo; el texto antes del primer encabezado se descarta.

**Paso 10 (`PromptPieces`).** Pista 1: es una clase de Pydantic con cinco campos de texto. Pista 2: busca `ConfigDict(frozen=True)` y `field_validator` en <https://docs.pydantic.dev/latest/concepts/validators/>. Pista 3: un validador que se aplica a todos los campos y lanza `ValueError` si el texto, sin espacios, está vacío.

**Paso 11 (`config.py`).** Pista 1: hoy lee el archivo viejo con `read_text`. Pista 2: ya tienes una función que carga y otra que compone. Pista 3: el valor de `prompt` es lo que devuelve `compose_system_prompt` al darle lo que devuelve `load_prompt_pieces` sobre `prompt_v1.md`.

Si sigues trabado después de la Pista 3: comenta en el Issue #53 con el error pegado como texto.

## Errores típicos de esta asignación

| Síntoma (lo que ves) | Causa probable | Qué hacer |
|---|---|---|
| `dir src\agents\config.py` no encuentra el archivo | Tu copia de `main` está vieja | `git pull`; si sigue sin estar, para y comenta en el Issue #53 (Paso 0) |
| P6 falla: falta `[1]` o `<fragmentos>` | Al partir el prompt perdiste la regla de las fuentes | Vuelve a `prompt.md` y revisa la sección 5.3 |
| P6 falla por un precio o una hora | Copiaste un dato del negocio al prompt | Quítalo: los datos salen del RAG |
| El agente «no contesta» en los evals | El prompt dejó de pedir la cita `[1]` | Mira `validate_answer` en `src/agents/info.py` y la sección 5.3 |
| `FileNotFoundError` al correr las pruebas | Borraste `prompt.md` antes de cambiar `config.py` | Hazlo en el orden del Paso 11 |
| P3 pasa pero con un mensaje genérico | El error no nombra la pieza que falta | El contrato pide que el mensaje diga qué falta o sobra |
| S6 falla | Cuentas las líneas en blanco | «Línea con texto» es la que no queda vacía tras quitar espacios |
| S8 falla por el orden | Agregas los códigos en otro orden | Primero líneas, después preguntas |
| `git diff --name-only main` lista más de 7 rutas | Editaste otro archivo, o un hook cambió algo que no debía | Revisa la sección 4 del contrato y quita lo que sobra |
| `git commit` falla y modifica archivos | Un hook de formato reformateó | `git status --short`, `git add` de esos archivos, repite el mismo commit |
| `ruff` marca algo de `.join` o de f-strings | Regla del repo | Aplica lo que sugiere; no la apagues |
| Tildes raras en la consola | Codificación de la ventana | Ejecuta `chcp 65001` y repite |

## Autoevaluación antes del PR

- [ ] Cada prueba (P1–P6, C1, S1–S8) la escribí yo, la vi fallar y la vi pasar.
- [ ] Puedo explicar en voz alta, sin mirar, las 4 preguntas de comprensión del contrato (sección 11).
- [ ] `git diff --name-only main` coincide con las 7 rutas de la sección 4 del contrato.
- [ ] `git status --short` no muestra ningún archivo que no sea de la sección 4.
- [ ] Mi `prompt_v1.md` no tiene precios, horas ni datos del negocio.
- [ ] Anoté en el PR cuántas interacciones usé con mi IA (tope 10–15) y a quién consulté.
- [ ] El PR tiene `Closes #53`.

## Prompts sugeridos para tu IA (pequeños y verificables)

**Sí (pega solo lo puntual):**
1. «Explícame en 5 líneas qué es una expresión regular, con un ejemplo que no sea de mi proyecto.»
2. «Me sale este error de pytest (pego el texto completo). ¿Qué significa? No me des el arreglo.»
3. «Aquí está mi `prompt_v1.md`. Contra esta lista de reglas de contenido (pego la sección 5.3), ¿cuál falta? No lo reescribas.»
4. «¿Qué diferencia hay entre un dato y una instrucción dentro de un prompt? Solo el concepto, con un ejemplo de inyección.»
5. «Aquí está la salida de `git diff --name-only main` y la lista de 7 rutas de la sección 4. ¿Falta o sobra algo?»

**Prohibidos:**
- «Escríbeme el prompt completo, `prompt.py` o `style.py`»: el contrato te los pide a ti, y la sección 9 lo prohíbe.
- «Redacta mis respuestas de comprensión del PR»: la puerta de comprensión mide **tu** entendimiento.
