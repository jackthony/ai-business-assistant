# [S05 D2] Paso a paso guiado — System prompt por componentes y verificación de respuesta (Issue #53)

> **Para quién:** practicante de 2.º año de AI Engineering, con Python básico y Git básico, que **no** conoce todavía `Protocol`, Pydantic, `LangGraph` como grafo de conversación ni las verificaciones por reglas. Este archivo te acompaña **mientras trabajas**; el contrato ([`S05_D2.md`](S05_D2.md)) dice **qué** debe quedar. Aquí aprendes **cómo abordarlo sin perderte**.
>
> **Reglas del juego:** no hay código de la solución aquí (si lo hubiera, no aprenderías). Hay explicación, pistas y puntos de control. Esta asignación es larga: los bloques de abajo suman unas 4 h 30 en total. Si a las 2 h 30 no estás en el Paso 19, comenta en el Issue y avisa al monitor, que decide qué pasa a la siguiente sesión. Los tiempos son una guía. Todos los comandos son para Windows (cmd), desde la raíz del repo.

> **Revisión automática de tu avance:** desde tu primer commit haz `git push -u origin <tu-rama>`. El robot abre solo un **PR en borrador** y deja **un comentario que se actualiza en cada push**: cuántos archivos del contrato ya trabajaste, cuáles te faltan, si tocaste algo fuera de la sección 4 y cuál es tu siguiente paso, con pistas (no con la solución). Léelo antes de seguir con el paso siguiente; si no lo entiendes, usa `/pista`. Haz push **al terminar cada paso en verde**, no solo al final. Cuando acabes, marca el PR *Ready for review* y responde la sección 11.

## Mapa de la sesión

| Bloque | Tiempo | Resultado que puedes comprobar |
|---|---|---|
| Lectura + mini-conceptos | 30 min | Sabes explicar qué es un `Protocol`, un doble de prueba y una verificación por reglas |
| Calentamiento | 15 min | Una clase falsa cumple la misma forma que una real en un archivo suelto |
| Pasos 0–2 (terreno, dependencias, fixture) | 30 min | `10 True True` y las 4 puertas en verde antes de tu código |
| Pasos 3–19 (P1–P3, V1–V9, S1–S3, T1–T10, W1, una prueba por paso) | 110 min | Todas en rojo por `ModuleNotFoundError` |
| Pasos 20–26 (prompt y módulos hasta verde) | 40 min | `35 passed` |
| Paso 27 (corrida manual, 10 filas) | 15 min | Tabla de 10 filas lista para el PR |
| Pasos 28–29 (puertas, commits, PR) | 25 min | PR abierto con `Closes #53` |

## Mini-conceptos (léelos antes del Paso 0)

**1. Protocol (puerto).**
- **Idea:** un `Protocol` describe **qué forma** deben tener los objetos (qué métodos y qué firma), sin decir de dónde vienen. Cualquier clase con esa forma sirve.
- **Analogía:** el enchufe de tres patas: cualquier cargador con esa forma entra en la pared, sin importar la marca.
- **Ejemplo (fuera del proyecto):**
```python
from typing import Protocol
class Cargable(Protocol):
    def cargar(self, watts: int) -> str: ...
```
- **Profundiza:** <https://docs.python.org/3/library/typing.html#typing.Protocol>

**2. Doble de prueba (fake).**
- **Idea:** una clase sencilla que reemplaza a una real en la prueba. No usa red ni modelo: guarda lo que recibe en una lista y devuelve un texto fijo, así puedes comprobar qué le llegó.
- **Analogía:** el simulador de vuelo: parece un avión, no vuela, y te deja practicar sin riesgo.
- **Ejemplo (fuera del proyecto):**
```python
class Falso:
    respuesta = "ok"
    llamadas = []
```
- **Profundiza:** <https://docs.pytest.org/en/stable/how-to/fixtures.html>

**3. Modelo de datos con Pydantic (`BaseModel`).**
- **Idea:** una clase con campos tipados. Pydantic valida los datos al crearla: si pasas un número donde va un texto, falla de inmediato. En este proyecto los contratos (`ChatMessage`, `VerificationResult`, `ConversationResult`) son `BaseModel`.
- **Analogía:** un formulario con casillas que solo acepta lo que corresponde a cada casilla.
- **Ejemplo (fuera del proyecto; importa `from pydantic import BaseModel`):**
```python
class Persona(BaseModel):
    nombre: str
    edad: int
```
- **Profundiza:** <https://docs.pydantic.dev/latest/concepts/models/>

**4. f-string y plantillas de texto.**
- **Idea:** una f-string inserta valores dentro de un texto con `{nombre}`. Para un prompt, cada pieza se une en un orden fijo; el orden importa porque el modelo lee de arriba abajo.
- **Analogía:** la carta de un restaurante con espacios en blanco: el nombre del plato va siempre en el mismo lugar.
- **Ejemplo (fuera del proyecto):**
```python
nombre = "Ana"
print(f"Hola {nombre}, bienvenida")
```
- **Profundiza:** <https://docs.python.org/3/reference/lexical_analysis.html#f-strings>

**5. Verificación por reglas.**
- **Idea:** una respuesta pasa por una lista de reglas simples (contar líneas, contar signos, buscar patrones). Cada regla que falla deja un código; si no falla ninguna, la respuesta es válida. No adivina nada: aplica reglas.
- **Analogía:** el control de calidad de una etiqueta: revisas peso, tamaño y ortografía, y anotas qué falló.
- **Ejemplo (fuera del proyecto):**
```python
import re
re.search(r"\d+\s*kg", "pesa 5 kg") is not None  # True
```
- **Profundiza:** <https://docs.python.org/3/library/re.html>

## Calentamiento (fuera del proyecto)

Crea `calentamiento.py` **fuera del repo** (por ejemplo en el Escritorio). Define un `Protocol` con un método `generar(self, texto: str) -> str`. Luego escribe una clase que cumpla esa forma y devuelva siempre `"ok: "` seguido del texto recibido usando una f-string. Crea una instancia, llama al método con `"hola"` e imprime el resultado. Busca en la documentación cómo escribir un método de clase si no lo recuerdas.

**Resultado esperado:** la consola muestra `ok: hola`. Después añade una segunda clase que cumpla la forma pero guarde cada texto recibido en una lista y devuelva `"fake"`. Imprime la lista: debe contener lo que le enviaste. Esa lista es la idea de `FakeLLM` del contrato. Borra el archivo al terminar.

## Paso a paso

### Paso 0 — Prepara tu terreno (prerrequisito #52)
**Haz esto:** sigue los pasos 1 y 2 de la sección 7 del contrato: `git checkout main`, `git pull`, `git ls-tree -r --name-only main src/agents`, `dir src\agents\state.py`, `git checkout -b issue-53-system-prompt`. Después crea el entorno con `py -3.11 -m venv .venv` (si ya lo tienes de S05 D1, solo actívalo con `.venv\Scripts\activate`).
**Por qué:** esta asignación importa `AgentState` de `src/agents/state.py`, que lo creó #52. Si #52 no está en `main`, tu rama no tiene nada sobre lo que construir.
**Debes ver:** `git ls-tree` lista exactamente cuatro líneas: `src/agents/__init__.py`, `src/agents/cli.py`, `src/agents/graph.py` y `src/agents/state.py`. `dir` muestra el archivo `state.py` con su tamaño. `Switched to a new branch 'issue-53-system-prompt'`. El prompt empieza con `(.venv)` y `python --version` dice `Python 3.11.x`.
**Si falla:** si falta alguna de las cuatro líneas, o `dir` dice que no existe, **para**: comenta en el Issue #53 con la salida pegada como texto. Si `py -3.11` no existe, instala Python 3.11 (no 3.12 ni 3.13).
**Punto de control:** ¿qué número lleva la rama que muestra `git branch --show-current`? Debe ser el 53, no el 52 ni el 05 del backlog viejo.

### Paso 1 — Dependencias y línea base (sin escribir código todavía)
**Haz esto:** agrega `"langchain-ollama>=1,<2",` dentro de `dependencies` de `pyproject.toml`, justo debajo de `"langchain-core>=1,<2",`, con cuatro espacios de sangría (contrato, sección 7, paso 3). Verifica con `findstr /N "langgraph langchain-core langchain-ollama" pyproject.toml` e instala con `python -m pip install -e ".[dev]"`. Luego corre las 4 puertas (contrato, sección 7, paso 4). Al final ejecuta `pre-commit install`.
**Por qué:** las puertas verdes **antes** de tu código te dicen que, si algo se pone rojo después, fue tu cambio y no el entorno.
**Debes ver:** `findstr` muestra tres líneas, una por paquete, sin repetidos. Python imprime `ok` con `import langgraph, langchain_core, langchain_ollama`. Las cuatro puertas en verde: `All checks passed!`, `Success: no issues found`, `N passed` sin `failed`, `No issues identified.`. `pre-commit installed at`.
**Si falla:** `ModuleNotFoundError` al importar `langchain_ollama`: pega el error en el Issue #53. Si alguna puerta ya estaba roja sin tu código, anótalo en el Issue y no lo arregles aquí. No cambies los topes de versión.
**Punto de control:** ¿las tres dependencias quedaron dentro de `[project] dependencies` y no en `optional-dependencies`?

### Paso 2 — Fixture con los 10 primeros mensajes (no es prueba, prepara T1–T10)
**Haz esto:** revisa que existan `data\conversaciones\README.md` y `data\conversaciones\sinteticas_v1.jsonl` (`dir data\conversaciones`). Crea `tests\fixtures\first_messages_v1.json`: una **lista JSON** de 10 objetos con `conversacion_id` y `texto`, de `conv_0001` a `conv_0010`. El `texto` es el de la **primera fila con `rol` = `user`** de cada conversación (en `conv_0004` es la de turno 2). Copia el texto tal cual, en UTF-8. Verifica con el comando del paso 6 de la sección 7 del contrato.
**Por qué:** T1–T10 prueban con mensajes reales del corpus sintético, no con frases que tú inventas; así el fixture es la misma entrada en todas las pruebas.
**Debes ver:** `10 True True` en el comando de verificación.
**Si falla:** si falta el JSONL, **no lo reconstruyas**: comenta en el Issue #53. Si sale `False`, corrige el fixture, no el comando. Si un `texto` no está marcado como `sintetica` en `origen`, para y avisa en el Issue.
**Punto de control:** ¿tu fixture tiene solo 10 objetos y ninguno trae teléfono ni nombre?

### Paso 3 — P1: el archivo real se carga en cinco piezas
**Haz esto:** crea `tests\conftest.py` con la clase `FakeLLM` y la fixture `fake_llm` de la sección 5 del contrato ("Pruebas de apoyo"). Crea `tests\test_prompt_pieces.py` y escribe P1: importa `load_prompt_pieces` desde `agents.prompt`, calcula la ruta a `configs\hola_mujer\prompt_v1.md` desde `__file__` y comprueba que el resultado tiene los 5 campos no vacíos. Corre el archivo.
**Por qué:** la prueba fija el primer contrato del prompt: cinco piezas con nombre. Calcular la ruta desde `__file__` evita depender de desde dónde ejecutas pytest.
**Debes ver:** rojo por `ModuleNotFoundError` que nombra el primer módulo que falta (`agents.llm_port` o `agents.prompt`: tu `conftest.py` importa el puerto).
**Si falla:** si el error es `SyntaxError` o `NameError` en tu prueba, corrígela primero.
**Punto de control:** ¿por qué la ruta sale de `__file__` y no de un texto escrito a mano como `"configs/..."`?

### Paso 4 — P2: una sección que falta se reporta por nombre
**Haz esto:** en el mismo archivo escribe P2. Usa `tmp_path` para crear una copia temporal del archivo real **sin** la sección `## Memoria`. Espera un `ValueError` y comprueba que el mensaje contiene `Memoria`. Corre el archivo.
**Por qué:** un error que dice qué falta te ahorra media hora buscando. Esta prueba fija ese mensaje.
**Debes ver:** sigue en rojo por `ModuleNotFoundError` de `agents.prompt`.
**Si falla:** si no sabes cómo crear un archivo temporal, busca `tmp_path` (ver pista 2 abajo).
**Punto de control:** ¿tu prueba fallaría si el mensaje dijera solo «falta una sección»? Debe fallar: exige el nombre.

### Paso 5 — P3: la composición conserva el orden
**Haz esto:** escribe P3 con un `PromptPieces` cuyos campos son `IDENT`, `TONO`, `LIMITES`, `HERR` y `MEM` (los valores del contrato). Comprueba que el texto contiene las cinco cadenas y que sus posiciones van en el orden IDENT < TONO < LIMITES < HERR < MEM. Corre el archivo.
**Por qué:** el modelo lee el prompt de arriba abajo; si el orden se cambia por accidente, el comportamiento cambia sin que nadie lo note.
**Debes ver:** rojo por `ModuleNotFoundError` de `agents.prompt`.
**Si falla:** si `PromptPieces` te parece raro, recuerda el mini-concepto 3: es un `BaseModel` con cinco campos de texto.
**Punto de control:** ¿compruebas las **posiciones**, no solo que las cinco cadenas aparecen?

### Paso 6 — V1: respuesta válida pasa
**Haz esto:** crea `tests\test_verification.py`. Importa `verify_response` desde `agents.verification` a nivel de módulo. Escribe V1 con el texto de la tabla del contrato: `ok=True` y `reasons=[]`. Corre el archivo.
**Por qué:** la prueba más simple fija el caso feliz; si una regla nueva rechaza textos buenos, V1 lo detecta.
**Debes ver:** `ModuleNotFoundError` que nombra `agents.verification`.
**Si falla:** si el archivo tiene un error de codificación, guárdalo como UTF-8 (los signos `¿` deben verse bien).
**Punto de control:** ¿el texto de V1 tiene menos de 3 líneas no vacías y un solo `?`?

### Paso 7 — V2: más de 3 líneas se rechaza
**Haz esto:** escribe V2 con `"a\nb\nc\nd"`. Espera `ok=False` y `reasons=["too_many_lines"]`. Corre el archivo.
**Por qué:** la regla de 3 líneas es del negocio (`program/04_DOMAIN/hola-mujer.md`); un mensaje largo en WhatsApp se lee mal.
**Debes ver:** sigue en rojo por el mismo `ModuleNotFoundError`.
**Si falla:** si confundes `\n` con dos caracteres, revisa en la prueba que estés usando una cadena normal, no una cruda.
**Punto de control:** ¿cuántas líneas tiene `"a\nb\nc\nd"`? Debes poder contarlas sin ejecutar.

### Paso 8 — V3: las líneas vacías no cuentan
**Haz esto:** escribe V3 con `"Hola\n\n\n\n¿Qué día?"`. Son dos líneas no vacías: espera `ok=True`, `reasons=[]`. Corre el archivo.
**Por qué:** un modelo a veces mete saltos de línea de más; si esos cuentan como líneas, rechazarías respuestas correctas.
**Debes ver:** rojo por `ModuleNotFoundError`.
**Si falla:** revisa que el texto tenga exactamente los saltos del contrato.
**Punto de control:** ¿una línea con solo espacios cuenta como vacía según el contrato? (Léelo otra vez: «sin espacios en blanco, no tiene caracteres».)

### Paso 9 — V4: más de una pregunta se rechaza
**Haz esto:** escribe V4 con `"¿Qué día? ¿A qué hora?"`. Espera `ok=False` y `reasons=["too_many_questions"]`. Corre el archivo.
**Por qué:** la regla es «máximo 1 pregunta por turno»: dos preguntas juntas confunden a la clienta.
**Debes ver:** rojo por `ModuleNotFoundError`.
**Si falla:** si el error no es `ModuleNotFoundError`, revisa tu prueba (`NameError`, un typo en el texto esperado) y luego la escalera de pistas.
**Punto de control:** ¿el `¿` de apertura cuenta como pregunta según el contrato? (No: solo cuenta el `?`.)

### Paso 10 — V5: precio con `S/` (3 casos)
**Haz esto:** escribe V5 como una prueba parametrizada (`pytest.mark.parametrize`) con tres textos: `"Cuesta S/25."`, `"Cuesta S/. 25."` y `"Cuesta S/ 25."`. En cada caso espera `ok=False` y `reasons=["invented_price"]`. Corre el archivo.
**Por qué:** en esta versión no hay base de datos de precios; un precio que el modelo inventa es el error más grave del bot.
**Debes ver:** rojo por `ModuleNotFoundError`. Cuenta los tres casos en el total.
**Si falla:** si no sabes parametrizar, busca `pytest.mark.parametrize` (pista 2 abajo).
**Punto de control:** ¿tu prueba cubre el punto opcional y el espacio opcional de `S/.`?

### Paso 11 — V6: precio con `soles`, `$` o `PEN` (5 casos)
**Haz esto:** amplía la parametrización con cinco textos: `"Cuesta 120 soles."`, `"Son 120 nuevos soles."`, `"Cuesta 24,50 soles."`, `"Cuesta $25."` y `"Cuesta PEN 25."`. Espera `ok=False` y `reasons=["invented_price"]` en cada caso. Corre el archivo.
**Por qué:** un precio puede escribirse de varias formas; si solo detectas una, el modelo inventará con otra.
**Debes ver:** rojo por `ModuleNotFoundError`.
**Si falla:** revisa que `24,50` tenga coma, no punto, en el texto de la prueba.
**Punto de control:** ¿cuál de los cinco casos sería el más fácil de dejar pasar sin querer? (Pista para la implementación.)

### Paso 12 — V7: texto vacío con cualquier espacio en blanco (3 casos)
**Haz esto:** escribe V7 parametrizada con `"   "`, `"\n\n"` y `"\t"`. En cada caso espera `ok=False` y `reasons=["empty"]`. Corre el archivo.
**Por qué:** un texto que solo tiene espacios no es una respuesta; no debe enviarse a la clienta.
**Debes ver:** rojo por `ModuleNotFoundError`.
**Si falla:** si el error no es `ModuleNotFoundError`, revisa tu prueba y luego la escalera de pistas.
**Punto de control:** según el contrato, si `empty` aplica, ¿puede aparecer junto con otro motivo? (Léelo en la sección 5.)

### Paso 13 — V8: varios motivos en orden
**Haz esto:** escribe V8 con `"a\nb\nc\nd ¿q?\n¿r?"`. Espera `ok=False` y `reasons=["too_many_lines","too_many_questions"]`, en ese orden. Corre el archivo.
**Por qué:** el orden de los motivos es parte del contrato: quien lee el registro de revisión espera siempre el mismo orden.
**Debes ver:** rojo por `ModuleNotFoundError`.
**Si falla:** si el error no es `ModuleNotFoundError`, revisa tu prueba y luego la escalera de pistas.
**Punto de control:** ¿tu prueba compara la lista completa o solo que contenga los dos códigos? Debe comparar la lista completa y en orden.

### Paso 14 — V9: números que no son precio no disparan la regla
**Haz esto:** escribe V9 con `"Puedo el martes 13 a las 10.\n¿Te sirve?"`. Espera `ok=True`, `reasons=[]`. Corre el archivo.
**Por qué:** una regla demasiado amplia rechaza horas y fechas; el bot no podría agendar nada.
**Debes ver:** rojo por `ModuleNotFoundError`.
**Si falla:** si el error no es `ModuleNotFoundError`, revisa tu prueba y luego la escalera de pistas.
**Punto de control:** ¿por qué `10.` no es un precio, aunque tenga un número y un punto?

### Paso 15 — S1: la respuesta válida se devuelve
**Haz esto:** crea `tests\test_conversation_service.py`. Importa `ConversationService` desde `agents.conversation_service` a nivel de módulo. Escribe S1: `fake_llm.reply="Hola, ¿en qué te ayudo?"`, mensajes `[user "Hola"]`. Espera `status="respondido"`, `text` igual al `reply`, `reasons=[]` y una sola llamada. Corre el archivo.
**Por qué:** el servicio es el único que llama al modelo; si S1 falla, nada del bot funciona.
**Debes ver:** rojo por `ModuleNotFoundError` que nombra `agents.conversation_service`. Si ves `fixture 'fake_llm' not found`, falta `tests\conftest.py` (Paso 3).
**Si falla:** revisa que `conftest.py` esté en `tests\`, no en otra carpeta.
**Punto de control:** ¿tu prueba mira el número de llamadas, o solo el texto?

### Paso 16 — S2: respuesta inválida pasa a revisión
**Haz esto:** escribe S2 con `fake_llm.reply="a\nb\nc\nd"`. Espera `status="revision_humana"`, `text=None` y `reasons=["too_many_lines"]`. Corre el archivo.
**Por qué:** cuando el texto no pasa, **no** se envía; la prueba fija que el servicio no lo deja pasar.
**Debes ver:** rojo por `ModuleNotFoundError`.
**Si falla:** si el error no es `ModuleNotFoundError`, revisa tu prueba y luego la escalera de pistas.
**Punto de control:** ¿qué pasa con `text` cuando `status` es `revision_humana`? Debes decirlo de memoria.

### Paso 17 — S3: el sistema llega sin cambios al modelo
**Haz esto:** escribe S3 con `ConversationService(llm=fake_llm, system="SYS")` y un turno. Espera `calls[0][0] == "SYS"`. Corre el archivo.
**Por qué:** el servicio no debe reescribir el prompt; si lo hace, lo que revisas en el archivo no es lo que lee el modelo.
**Debes ver:** rojo por `ModuleNotFoundError`.
**Si falla:** si el error no es `ModuleNotFoundError`, revisa tu prueba y luego la escalera de pistas.
**Punto de control:** ¿`calls` guarda la tupla `(system, messages)`? ¿En qué posición está el sistema?

### Paso 18 — T1 a T10: el primer mensaje de cada conversación del fixture
**Haz esto:** escribe **una** prueba parametrizada que recorra el fixture `first_messages_v1.json` (conversaciones `conv_0001` a `conv_0010`). Cada caso, con su ID, hace lo mismo que T1: `fake_llm.reply="Hola, ¿en qué te puedo ayudar?"`, mensajes `[user <texto>]`, y espera `status="respondido"`, `text` igual al `reply`, y que el último mensaje enviado al modelo tenga el `texto` del fixture. Los IDs son: T1 (`conv_0001`), T2 (`conv_0002`), T3 (`conv_0003`), T4 (`conv_0004`), T5 (`conv_0005`), T6 (`conv_0006`), T7 (`conv_0007`), T8 (`conv_0008`), T9 (`conv_0009`) y T10 (`conv_0010`). Corre el archivo.
**Por qué:** T1–T10 prueban con los mensajes reales del corpus; si el servicio cambia el texto del usuario, lo ves con diez casos.
**Debes ver:** rojo por `ModuleNotFoundError`. Los diez casos aparecen en el total (`35` al final). No confundas estos T1–T10 con los T1–T8 de S05 D1: son de otro archivo. El primer mensaje de `conv_0004` es solo «3» (una opción de menú): es correcto.
**Si falla:** si el fixture no se encuentra, calcula la ruta desde `__file__` como en P1.
**Punto de control:** ¿puedes decir qué ID es `conv_0004` y por qué su mensaje es de turno 2?

### Paso 19 — W1: el grafo de conversación con LLM falso (2 casos)
**Haz esto:** crea `tests\test_conversation_graph.py`. Importa `build_conversation_graph` desde `agents.conversation_graph` y `HumanMessage` de `langchain_core.messages`. Escribe W1 con dos casos. Caso a: `reply="Hola, ¿en qué te ayudo?"`: `len(messages)==2`, `messages[1]` es un `AIMessage` con ese contenido, `status=="respondido"`. Caso b: `reply="a\nb\nc\nd"`: `status=="revision_humana"` y `len(messages)==1`. En ambos, `intent is None`, `phone` y `tenant` sin cambios y una sola llamada al falso. Corre el archivo.
**Por qué:** W1 prueba que el grafo pasa por el servicio y el nodo sin que tú ejecutes un modelo.
**Debes ver:** rojo por `ModuleNotFoundError` que nombra `agents.conversation_graph`.
**Si falla:** si ves otro error, revisa la sección 5 («Grafo de conversación») del contrato.
**Punto de control:** ¿la entrada del grafo tiene las 5 claves del contrato de S05 D1 y ninguna extra?

### Paso 20 — Escribe el prompt v1 por componentes
**Haz esto:** crea la carpeta con `mkdir configs\hola_mujer` y el archivo `configs\hola_mujer\prompt_v1.md`. Primera línea `# Prompt Hola Mujer v1`, luego las cinco secciones `##` en orden (`Identidad`, `Tono`, `Límites`, `Herramientas`, `Memoria`) con lo que pide la sección 5 del contrato. Guárdalo en UTF-8. Verifica con `findstr /B "##" configs\hola_mujer\prompt_v1.md`.
**Por qué:** el prompt es texto que el modelo lee; cada sección tiene un trabajo: quién es, cómo habla, qué no hace.
**Debes ver:** exactamente cinco líneas `##` en el orden del contrato. Ningún precio, horario ni cifra de negocio en el texto (las reglas «máximo 3 líneas» y «máximo 1 pregunta» sí van escritas).
**Si falla:** si las tildes se ven raras en cmd, es la consola; el archivo está bien si está en UTF-8.
**Punto de control:** ¿hay algún número de precio en el prompt? Debe haber cero.

### Paso 21 — P1 a P3 en verde: `prompt.py`
**Haz esto:** crea `src\agents\prompt.py` con `PromptPieces` (`BaseModel`), `load_prompt_pieces` y `compose_system_prompt`, según la sección 5 del contrato. Corre `pytest tests\test_prompt_pieces.py -q`.
**Por qué:** P1–P3 son la primera pieza verde: prueba que lees y compones bien antes de seguir.
**Debes ver:** `3 passed` (si el error nombra `agents.llm_port`, crea antes ese archivo: es el Paso 22).
**Si falla:** lee el error de abajo hacia arriba: la última línea suele nombrar la causa. Si P2 falla, mira el mensaje del `ValueError`.
**Punto de control:** ¿`compose_system_prompt` une las piezas en el orden `identity`, `tone`, `limits`, `tools`, `memory`?

### Paso 22 — `llm_port.py`: el puerto del LLM
**Haz esto:** crea `src\agents\llm_port.py` con `ChatMessage` (`BaseModel` con `role` y `text`) y `LLMPort` (`Protocol` con `generate`), tal como está en la sección 5 del contrato. No tiene prueba propia: lo usan todas las demás. Corre `pytest tests\test_prompt_pieces.py -q` para confirmar que sigue verde.
**Por qué:** el servicio depende de la **forma** `LLMPort`, no de Ollama. Por eso las pruebas pueden usar un falso.
**Debes ver:** `3 passed` en P1–P3 sin cambios.
**Si falla:** `SyntaxError` en `Literal`: revisa que importes `Literal` desde `typing`.
**Punto de control:** ¿`llm_port.py` importa `langchain_ollama`? No debe hacerlo.

### Paso 23 — V1 a V9 en verde: `verification.py`
**Haz esto:** crea `src\agents\verification.py` con `VerificationResult` y `verify_response`. Aplica las reglas en el orden del contrato (`empty`, `too_many_lines`, `too_many_questions`, `invented_price`). Corre `pytest tests\test_verification.py -q`.
**Por qué:** es el guardián del negocio: lo que no pasa aquí no llega a la clienta.
**Debes ver:** `17 passed` (V1–V9, con los casos de V5, V6 y V7).
**Si falla:** si V5 o V6 fallan, revisa las formas de precio de la sección 5 una por una, no todas juntas.
**Punto de control:** ¿un texto vacío devuelve solo `["empty"]` y nada más?

### Paso 24 — S1 a S3 y T1 a T10 en verde: `conversation_service.py`
**Haz esto:** crea `src\agents\conversation_service.py` con `ConversationResult` y `ConversationService`. `respond` llama a `llm.generate` **una** vez y aplica `verify_response`. Corre `pytest tests\test_conversation_service.py -q`.
**Por qué:** el servicio es el único que habla con el modelo y el único que decide si la respuesta sale.
**Debes ver:** `13 passed`.
**Si falla:** si una prueba dice que hubo dos llamadas, revisa que no llames al modelo también en la verificación.
**Punto de control:** ¿`text` es `None` cuando el estado es `revision_humana`?

### Paso 25 — W1 en verde: `respond_node.py` y `conversation_graph.py`
**Haz esto:** crea `src\agents\respond_node.py` con `make_respond_node(service)`: convierte `HumanMessage` a `user` y `AIMessage` a `assistant`, llama a `service.respond` y devuelve la actualización de la sección 5. Crea `src\agents\conversation_graph.py` con `build_conversation_graph(service)`: un grafo `START → respond → END` con el `AgentState` de `src\agents\state.py`. Corre `pytest tests\test_conversation_graph.py -q`. Si mypy marca `add_node` con `call-overload`, mira la fila de esa limitación en `program/02_REFERENCE/ejemplos/langgraph-memoria/README.md`.
**Por qué:** el nodo solo traduce y devuelve cambios; la llamada al modelo queda en el servicio (regla de `AGENTS.md`).
**Debes ver:** `2 passed` en W1. `mypy src --ignore-missing-imports` sin errores nuevos.
**Si falla:** si el nodo devuelve `intent`, `phone` o `tenant`, rompes la regla del contrato: bórralos del `return`.
**Punto de control:** ¿`src\agents\graph.py` (el eco de S05 D1) sigue exactamente igual que antes? Debe seguir igual.

### Paso 26 — `ollama_adapter.py`: el único módulo que importa `langchain_ollama`
**Haz esto:** crea `src\agents\ollama_adapter.py` con `OllamaAdapter(model, base_url)` que implementa `generate` y devuelve solo el texto de la respuesta. No lee `.env`. No lo importes desde ningún test.
**Por qué:** así las pruebas siguen sin red, y cambiar de modelo solo toca este archivo.
**Debes ver:** `findstr /S /C:"ollama_adapter" tests\*.py` no devuelve nada. Las pruebas siguen en `35 passed` (sin contar aún la corrida manual).
**Si falla:** si un test importa el adaptador, quítalo: la regla es estricta.
**Punto de control:** ¿qué pasa si Ollama no responde? La excepción sube al llamador; no se convierte en `revision_humana`.

### Paso 27 — Corrida manual de las 10 filas (fuera del repo)
**Haz esto:** con un script local **fuera** de la carpeta del proyecto, pasa el `texto` de cada fila del fixture por `build_conversation_graph`, con un `ConversationService` que use `OllamaAdapter` y el texto de `compose_system_prompt`. El `model` y el `base_url` salen del Issue #53. Anota una tabla de 10 filas: `conv`, respuesta (sin datos personales), `≤3 líneas`, `≤1 pregunta`, `precio` y ajuste hecho.
**Por qué:** las pruebas usan un falso; esta corrida muestra cómo se comporta un modelo real con tu prompt.
**Debes ver:** 10 filas en la tabla. Si no tienes Ollama accesible, pon `fake` en la columna de respuesta y avisa en el Issue #53.
**Si falla:** si el Issue no trae `model` ni `base_url`, **para y pregunta** en el Issue. No pegues mensajes del corpus en servicios externos.
**Punto de control:** ¿tu script está fuera del repo y no lo vas a subir?

### Paso 28 — Las 4 puertas completas
**Haz esto:** corre las cuatro puertas (`ruff check src tests`, `mypy src --ignore-missing-imports`, `pytest tests -q`, `bandit -r src -x tests -ll`) y `pytest tests\test_agent_graph.py tests\test_agent_cli.py -q`.
**Por qué:** el CI estricto corre las mismas puertas; mejor verlas rojas aquí.
**Debes ver:** `All checks passed!`, `Success: no issues found`, `35 passed` (más los de S05 D1, `8 passed`), `No issues identified.`.
**Si falla:** si `ruff` marca algo en tu código, corrígelo; si `bandit` marca un `assert` en tests, es ruido de `tests` (ya excluido con `-x tests`).
**Punto de control:** ¿las pruebas de S05 D1 siguen en `8 passed`?

### Paso 29 — Commits pequeños, push y PR
**Haz esto:** haz `git add` **solo** de las rutas de la sección 4 del contrato, una por commit. **Nunca** `git add .` ni `git add -A`: el JSONL del corpus no está excluido. Antes de cada commit revisa `git diff --cached --name-only`. Usa commits como `chore(deps): agregar langchain-ollama (#53)` y `feat(agents): agregar verificacion de respuesta (#53)`. Luego `git push -u origin issue-53-system-prompt` y abre el PR contra `main` con `Closes #53`, la plantilla completa, la tabla del Paso 27 y tus respuestas de la sección 11 del contrato.
**Por qué:** commits pequeños dejan historia legible; el PR es la evidencia que el monitor revisa contra el contrato.
**Debes ver:** `branch 'issue-53-system-prompt' set up to track 'origin/issue-53-system-prompt'`; `guardian-tbd / reglas-tbd` y `CI estricto / calidad` en verde.
**Si falla:** si un hook reformatea un archivo, el commit falla: `git add` de ese archivo y repite. Si el guardian rechaza, revisa el nombre de la rama y el `Closes #53`.
**Punto de control:** antes de abrir el PR, haz la Autoevaluación de abajo y ensaya con `/comprension`.

## Escalera de pistas (úsala solo cuando estés trabado, de arriba abajo)

**Paso 4 (P2).** Pista 1: un `ValueError` con mensaje claro es una excepción que tú lanzas con un texto que dice qué falta. Pista 2: busca `tmp_path` y `pathlib` en <https://docs.pytest.org/en/stable/how-to/tmp_path.html> y <https://docs.python.org/3/library/pathlib.html>. Pista 3: copias el texto del archivo real a `tmp_path`, quitas el bloque de `## Memoria` y pides la carga desde esa copia.

**Paso 10 (V5).** Pista 1: una expresión regular busca un patrón dentro de un texto, no una palabra exacta. Pista 2: busca `re.search` y las clases `\d` y `\s` en <https://docs.python.org/3/library/re.html>. Pista 3: escribes un patrón por cada forma del contrato (a), cuentas que el punto y los espacios son opcionales y pruebas los tres casos en la consola antes de usarlo.

**Paso 13 (V8).** Pista 1: el orden de la lista de motivos sale del orden en que tú revisas las reglas. Pista 2: mira cómo se construye una lista en <https://docs.python.org/3/tutorial/datastructures.html>. Pista 3: revisas las reglas en el orden de la tabla del contrato y agregas el código de cada una que falle.

**Paso 24 (S1–S3).** Pista 1: el servicio es un objeto que guarda el `llm` y el `system` al crearse. Pista 2: busca cómo `ConversationService.respond` llama a `generate` y cuántas veces se llama. Pista 3: `respond` pide la respuesta una vez, la verifica y arma el resultado según `ok`.

**Paso 25 (W1).** Pista 1: un grafo se arma declarando el estado, registrando nodos, conectando aristas y compilando. Pista 2: busca `StateGraph`, `add_node`, `add_edge`, `START`, `END`, `compile` en <https://langchain-ai.github.io/langgraph/concepts/low_level/>. Pista 3: el nodo recibe el estado, traduce los mensajes, llama al servicio y devuelve solo lo que cambia; el grafo tiene una sola arista de entrada y una de salida.

Si sigues trabado después de la Pista 3: comenta en el Issue #53 con el error pegado como texto.

## Errores típicos de esta asignación

| Síntoma (lo que ves) | Causa probable | Qué hacer |
|---|---|---|
| `ModuleNotFoundError: No module named 'agents.prompt'` (o `verification`, etc.) al correr pytest | Es el rojo esperado en los Pasos 3–19 | Sigue con la siguiente prueba; en los pasos 21–25 desaparece al crear el módulo |
| `fixture 'fake_llm' not found` | Falta `tests\conftest.py` o está en otra carpeta | Crea `tests\conftest.py` (Paso 3) |
| `ModuleNotFoundError: No module named 'langchain_ollama'` | `pyproject.toml` no tiene la línea nueva o no instalaste | Repite el Paso 1 (`python -m pip install -e ".[dev]"`) |
| `FileNotFoundError` en P1 o T1 | La ruta está escrita a mano y no desde `__file__` | Calcula la ruta desde `__file__` |
| `messages` sale con 1 solo elemento en W1 | `messages` no tiene el reducer `add_messages` | Revisa `src\agents\state.py` (S05 D1) sin modificarlo |
| `mypy: call-overload` en `add_node` | Limitación conocida de tipos de LangGraph | Aplica solo la excepción de la fila correspondiente del ejemplo `langgraph-memoria` |
| El texto de la clienta sale con `eco:` | Usaste el grafo de S05 D1 en lugar del nuevo | Usa `build_conversation_graph` en tus pruebas y tu corrida manual |
| Tildes raras en la consola | Codificación de la ventana | `chcp 65001` y repite |
| `git commit` falla y modifica archivos | `ruff-format` reformateó | `git add` de esos archivos y repite el commit |

## Autoevaluación antes del PR

- [ ] Cada prueba (P1–P3, V1–V9, S1–S3, T1–T10, W1) la escribí yo, la vi fallar y la vi pasar.
- [ ] Puedo explicar en voz alta, sin mirar, las 3 preguntas de comprensión del contrato (sección 11).
- [ ] Mi `git diff --name-only main` coincide con la sección 4 del contrato, sin `src\agents\graph.py` ni `cli.py`.
- [ ] Mi prompt no tiene ningún precio, horario ni cifra.
- [ ] Anoté en el PR cuántas interacciones usé con mi IA (máximo 12) y a quién consulté.

## Prompts sugeridos para tu IA (pequeños y verificables)

**Sí (pega solo lo puntual):**
1. «Explícame en 5 líneas qué es un `Protocol` de Python con un ejemplo de cafetera o de cargador, no de mi proyecto.»
2. «Me sale este error de pytest (pego el texto completo). ¿Qué significa, sin darme el arreglo?»
3. «Aquí está la salida de `git diff --name-only main` y la lista de la sección 4. ¿Falta o sobra algo?»
4. «Tengo esta prueba (pego V2). ¿Qué regla de la sección 5 verifica? Solo dime qué mira, no la implementación.»
5. «¿Qué diferencia hay entre `re.search` y `re.match` en Python? Un ejemplo con números, no de mi proyecto.»

**Prohibidos:**
- «Escríbeme `verification.py` / `ConversationService` / el grafo»: el contrato te lo pide a ti y la sección 9 lo prohíbe.
- «Redacta mi PR y mis respuestas de comprensión»: la puerta de comprensión mide **tu** entendimiento.
