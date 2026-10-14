# [S05 D1] Paso a paso guiado — Grafo mínimo con estado explícito (Issue #52)

> **Para quién:** practicante de 2.º año de AI Engineering, con Python básico y Git básico, que **no** conoce todavía LangGraph, `TypedDict` ni reducers. Este archivo te acompaña **mientras trabajas**; el contrato ([`S05_D1.md`](S05_D1.md)) dice **qué** debe quedar. Aquí aprendes **cómo abordarlo sin perderte**.
>
> **Dos numeraciones:** los «Paso N» de esta guía no son los pasos numerados de la sección 7 del contrato. Cuando aquí diga «sección 7, paso N» se refiere al contrato.
>
> **Reglas del juego:** no hay código de la solución aquí (si lo hubiera, no aprenderías). Hay explicación, pistas y puntos de control. Una sesión dura ~3 h; los tiempos son una guía. Todos los comandos son para Windows (cmd), desde la raíz del repo.

> **Revisión automática de tu avance:** desde tu primer commit haz `git push -u origin <tu-rama>`. El robot abre solo un **PR en borrador** y deja **un comentario que se actualiza en cada push**: cuántos archivos del contrato ya trabajaste, cuáles te faltan, si tocaste algo fuera de la sección 4 y cuál es tu siguiente paso, con pistas (no con la solución). Léelo antes de seguir con el paso siguiente; si no lo entiendes, usa `/pista`. Haz push **al terminar cada paso en verde**, no solo al final. Cuando acabes, marca el PR *Ready for review* y responde la sección 11.

## Mapa de la sesión

| Bloque | Tiempo | Resultado que puedes comprobar |
|---|---|---|
| Lectura + mini-conceptos | 30 min | Sabes explicar qué es un estado, un nodo y un reducer |
| Calentamiento (después del Paso 1) | 20 min | Un reducer de números funciona en un archivo suelto |
| Pasos 0–1 (terreno y dependencias; `pip install` puede tardar en PCs antiguas) | 35–40 min | `imports ok` y las 4 puertas en verde |
| Pasos 2–9 (T1–T8, una prueba por paso, y la implementación) | 100–120 min | `8 passed` |
| Paso 10 (sin LLM, CLI a mano, 4 puertas) | 15 min | `eco: hola` en tu terminal |
| Paso 11 (commits, push, PR) | 25 min | PR abierto con `Closes #52` |

## Mini-conceptos (léelos antes del Paso 1)

**1. Estado (`TypedDict`).**
- **Idea:** el estado es la «ficha» que viaja por el grafo; guarda todo lo que los nodos necesitan saber. Un `TypedDict` es un diccionario con claves y tipos declarados de antemano.
- **Analogía:** la ficha de admisión de una clínica: tiene casillas fijas (nombre, motivo, estado) y todos la leen y la actualizan.
- **Ejemplo (fuera del proyecto):**
```python
class Ficha(TypedDict):
    nombre: str
```
- **Profundiza:** <https://docs.python.org/3/library/typing.html#typing.TypedDict>

**2. Nodo.**
- **Idea:** una función que recibe el estado y devuelve **solo lo que cambia**, como dict. No modifica el estado de entrada.
- **Analogía:** una ventanilla que lee la ficha y devuelve una nota con los campos que corrigió.
- **Ejemplo:**
```python
duplicar = lambda s: {"n": s["n"] * 2}
```
- **Profundiza:** <https://langchain-ai.github.io/langgraph/concepts/low_level/>

**3. Reducer.**
- **Idea:** la regla que dice cómo se **combina** lo que devuelve un nodo con lo que ya había en un campo. Sin reducer, el valor nuevo **reemplaza** al viejo. Con `add_messages`, el valor nuevo se **añade** a la lista.
- **Analogía:** la libreta de una tienda: o borras la página y escribes encima (reemplazo), o anotas debajo de lo anterior (añadir).
- **Ejemplo:**
```python
from typing import Annotated
import operator
total: Annotated[int, operator.add]  # el nodo devuelve {"total": 5} y se SUMA
```
- **Profundiza:** <https://langchain-ai.github.io/langgraph/concepts/low_level/#reducers>

**4. Grafo con aristas.**
- **Idea:** conectas nodos con flechas. `START` y `END` son los extremos; compilas el grafo y lo ejecutas con `invoke(entrada)`.
- **Analogía:** un plano de recorrido: entrada → ventanilla → salida.
- **Ejemplo:** `START → echo → END` es todo el grafo de hoy.
- **Profundiza:** <https://langchain-ai.github.io/langgraph/concepts/low_level/#graphs>

**5. Prueba en rojo primero (TDD mínimo).**
- **Idea:** escribes la prueba, la ves **fallar por la razón correcta**, implementas lo mínimo y la ves pasar. Una prueba que nunca fue roja no demuestra nada.
- **Analogía:** calibrar una balanza vacía antes de pesar.
- **Ejemplo:**
```python
assert sumar(2, 3) == 5  # falla si `sumar` aún no existe
```
- **Profundiza:** <https://docs.pytest.org/en/stable/getting-started.html>

## Calentamiento (fuera del proyecto)

Hazlo **después del Paso 1** (ya tienes `.venv` y `langgraph` instalados). Crea `calentamiento.py` **fuera del repo** (por ejemplo en el Escritorio). Declara un `TypedDict` con un campo `total: Annotated[int, operator.add]` y un campo `nombre: str`. Pide a tu IA, o busca en la documentación, cómo armar un `StateGraph` de **un nodo** que devuelva `{"total": 5}`. Ejecútalo con `total=10` de entrada.

**Resultado esperado:** `total` termina en `15` (se sumó) y `nombre` llega intacto. Cambia el reducer por nada (solo `total: int`) y repite: ahora termina en `5` (reemplazó). Esa diferencia es la pregunta 1 del PR. Borra el archivo al terminar.

## Paso a paso

### Paso 0 — Prepara tu terreno
**Haz esto:** sigue los pasos 1–3 de la sección 7 del contrato: `git checkout main`, `git pull`, `git checkout -b issue-52-langgraph-core`, crea el entorno con `py -3.11 -m venv .venv` y actívalo.
**Por qué:** una rama por Issue (TBD) y un entorno aislado evitan mezclar tu trabajo con `main` y con otros proyectos de tu PC.
**Debes ver:** `Switched to a new branch 'issue-52-langgraph-core'`; el prompt empieza con `(.venv)`; `python --version` dice `Python 3.11.x`.
**Si falla:** si `py -3.11` no existe, instala Python 3.11 (no 3.12 ni 3.13). Si PowerShell bloquea la activación, usa cmd. Si sigue, abre el Issue con el error pegado.
**Punto de control:** ¿qué rama muestra `git branch --show-current`? Debe llevar el número 52.

### Paso 1 — Dependencias y línea base (sin escribir código todavía)
**Haz esto:** agrega las dos líneas de dependencias a `pyproject.toml` (contrato, sección 7, paso 4), instala con `python -m pip install -e ".[dev]"` y corre el comando de imports del paso 5. Después corre las 4 puertas (paso 6).
**Por qué:** las puertas verdes **antes** de tu código te dicen que, si algo se pone rojo después, fue tu cambio y no el entorno.
**Debes ver:** `imports ok` y las cuatro salidas verdes (`All checks passed!`, `Success: no issues found`, `N passed`, `No issues identified.`).
**Si falla:** `ImportError` en el comando de imports: no sigas; pega el error en el Issue. Si alguna puerta ya estaba roja sin tu código, anótalo en el Issue y no lo arregles aquí.
**Punto de control:** ¿las dos dependencias quedaron dentro de `[project] dependencies` y no en `optional-dependencies`? (abre `pyproject.toml` y compara con la línea `dependencies = [`; `findstr /N` solo te da números de línea).

> **Antes de los pasos 2–9:** crea los dos archivos de prueba vacíos y ve añadiendo una prueba por paso. En cada paso, la prueba se **escribe y se ve fallar** (rojo por `ModuleNotFoundError`). Cuando hayas escrito las ocho, recién implementas (el Paso 9 marca ese momento). Imports de `agents.*` a nivel de módulo.

### Paso 2 — T1: el estado tiene exactamente 5 campos
**Haz esto:** crea `tests\test_agent_graph.py` y escribe T1: pide los tipos de `AgentState` con `typing.get_type_hints(..., include_extras=True)` y comprueba las claves exactas y que los metadatos de `messages` incluyen `add_messages`. Corre el archivo.
**Por qué:** el estado es el contrato con las asignaciones siguientes; esta prueba impide que alguien agregue o renombre un campo sin darse cuenta.
**Debes ver:** error de colección `ModuleNotFoundError: No module named 'agents.state'` (eso es el rojo correcto).
**Si falla:** si el error es `SyntaxError` o `NameError` en tu prueba, corrígela primero: un rojo por la razón equivocada no vale.
**Punto de control:** ¿sabes por qué hace falta `include_extras=True`? (pista: sin él pierdes lo que va dentro de `Annotated`).

### Paso 3 — T2: el reducer añade, no reemplaza
**Haz esto:** en el mismo archivo escribe T2: invoca `build_graph()` con la entrada de 5 claves de la sección 5b y comprueba que salen 2 mensajes, el primero el `HumanMessage` original y el segundo un `AIMessage` con `eco: hola`.
**Por qué:** esta es la prueba que detecta la diferencia entre sumar y reemplazar; la que fallaría si usaras un reducer equivocado.
**Debes ver:** sigue en rojo por `ModuleNotFoundError` (aún no existe `agents.graph`).
**Si falla:** si no recuerdas los 5 campos de la entrada, mira la sección 5b; no los inventes.
**Punto de control:** ¿tu prueba verifica **el primer** mensaje además del segundo? Si solo mira el segundo, no detecta un reemplazo.

### Paso 4 — T3: intent y status de salida
**Haz esto:** escribe T3 con la misma entrada que T2 y comprueba `intent == "eco"` y `status == "respondido"`.
**Por qué:** `intent` y `status` son los campos que luego usarán otros nodos para decidir el camino; deben cambiar de forma predecible.
**Debes ver:** el mismo rojo por módulo inexistente.
**Si falla:** si te cuesta no repetir toda la entrada, piensa en una función auxiliar de prueba (esa decisión es tuya).
**Punto de control:** ¿qué valor de `status` entra y cuál sale? Debes poder decirlos de memoria.

### Paso 5 — T4: `phone` y `tenant` llegan intactos
**Haz esto:** escribe T4 con `phone="51900000001"` y comprueba que a la salida `phone` y `tenant` valen lo mismo que a la entrada.
**Por qué:** el nodo no devuelve esos campos (regla R4); si algún día los pierde, la conversación se mezclaría entre personas o negocios.
**Debes ver:** rojo por módulo inexistente.
**Si falla:** usa solo teléfonos ficticios del contrato; nunca uno real.
**Punto de control:** ¿por qué cambias el teléfono respecto de T2? (así la prueba no pasa por casualidad con el valor por defecto).

### Paso 6 — T5: tildes, ñ, ¿ y ?
**Haz esto:** escribe T5 con el texto `¿Cuánto cuesta el masaje?` y comprueba que la respuesta es exactamente `eco: ¿Cuánto cuesta el masaje?`.
**Por qué:** los mensajes reales de WhatsApp traen tildes y signos del español; el nodo no debe alterarlos.
**Debes ver:** rojo por módulo inexistente.
**Si falla:** si tu editor guarda el archivo en otra codificación, guárdalo como UTF-8.
**Punto de control:** ¿el archivo de pruebas está en UTF-8? (VS Code lo muestra abajo a la derecha).

### Paso 7 — T6: importar el grafo no carga ningún modelo
**Haz esto:** escribe T6: lanza un proceso **nuevo** de Python con `subprocess` y `sys.executable`, que importe `agents.graph` y revise `sys.modules`; la prueba comprueba código de salida `0` y que ningún módulo empieza por `ollama` ni `langchain_ollama`.
**Por qué:** pytest ya cargó muchos módulos en su proceso; solo un proceso limpio demuestra que tu grafo no depende de un LLM.
**Debes ver:** nada nuevo todavía: tu archivo sigue fallando en la colección por `agents.state` o `agents.graph`. T6 recién correrá cuando exista el grafo.
**Si falla:** si el hijo no encuentra `agents`, recuerda que `pythonpath = ["src"]` es de pytest, no del hijo: piensa cómo le pasas ese camino (pista 2 abajo).
**Punto de control:** ¿puedes explicar por qué importar en el mismo proceso no sería concluyente?

### Paso 8 — T7 y T8 (CLI) y primer rojo completo
**Haz esto:** crea `tests\test_agent_cli.py` y escribe T7 (`main(["--phone", "51900000000", "hola"])` devuelve `0` e imprime exactamente `eco: hola` + salto de línea, capturando stdout) y T8 (`main([])` lanza `SystemExit` con código `2`). Luego corre ambos archivos de prueba.
**Por qué:** la CLI es tu forma de probar el grafo a mano antes de conectarlo a WhatsApp; sus pruebas fijan el formato de salida.
**Debes ver:** `2 errors` (uno por archivo), cada uno `ModuleNotFoundError` que nombra `agents.state`, `agents.graph` o `agents.cli`.
**Si falla:** si ves otro error (por ejemplo de sintaxis), corrígelo; si ves `8 failed`, tus imports están dentro de las pruebas: también es válido siempre que sea `ModuleNotFoundError`.
**Punto de control:** ¿las 8 pruebas están escritas y todas rojas por módulo inexistente? Solo entonces sigues.

### Paso 9 — Implementa lo mínimo y ponlo en verde
**Haz esto:** crea `src\agents\state.py`, `src\agents\graph.py` y `src\agents\cli.py` según la sección 5 del contrato, **uno a la vez**, corriendo las pruebas tras cada archivo. Mira cuántas pasan en cada momento.
**Por qué:** ir archivo por archivo te enseña qué prueba depende de qué pieza; si lo haces todo junto no sabrás qué rompió qué.
**Debes ver:** tras `state.py`, el archivo de pruebas del grafo sigue con error de colección por `agents.graph`; tras `graph.py`, T1–T6 corren y pasan; tras `cli.py`, `8 passed`.
**Si falla:** lee el error de abajo hacia arriba: la última línea suele nombrar la causa. Si `mypy` marca `add_node` con `call-overload`, aplica solo la excepción que permite la sección 5b.
**Punto de control:** ¿tu `echo_node` devuelve solo `messages`, `intent` y `status`? Si devuelve `phone` o `tenant`, rompes la regla R4.

### Paso 10 — Sin LLM, CLI a mano y las 4 puertas
**Haz esto:** cierra Ollama si lo tienes abierto y comprueba con `tasklist | findstr /I ollama` (sin salida). Vuelve a correr las pruebas. Luego ejecuta los tres comandos de CLI de la sección 7, paso 10, y las 4 puertas del paso 11.
**Por qué:** esto es solo una comprobación de entorno (la independencia real del LLM la demuestra T6); además muestra que tu trabajo es determinista y que el CI estricto (las mismas 4 puertas) no te va a sorprender.
**Debes ver:** `8 passed`; `eco: hola`; `eco: ¿Cuánto cuesta?`; mensaje `usage:` y `2` en `echo %errorlevel%`; las cuatro puertas verdes.
**Si falla:** si la CLI no imprime nada, falta el bloque `if __name__ == "__main__":` con `sys.exit(main())`. Si las tildes salen raras, `chcp 65001`.
**Punto de control:** ¿`git diff --name-only main` lista exactamente las 6 rutas de la sección 4? Ni una más.

### Paso 11 — Commits pequeños, push y PR
**Haz esto:** `pre-commit install`; haz los 5 commits de la sección 7, paso 12 (uno por cambio); `git push -u origin issue-52-langgraph-core`; abre el PR contra `main` con `Closes #52`, la plantilla completa, el texto de la salida de `eco: hola` en un bloque de código y tus respuestas de la sección 11.
**Por qué:** commits pequeños dejan historia legible; el PR es la evidencia que el monitor revisa contra el contrato.
**Nota:** los commits de pruebas quedan en rojo a propósito (van antes de la implementación) y el PR se squashea. Usa `git add` solo con las rutas de cada commit, no `git add .`.
**Debes ver:** `set up to track 'origin/issue-52-langgraph-core'`; `guardian-tbd / reglas-tbd` y `CI estricto / calidad` en verde.
**Si falla:** si un hook reformatea un archivo, el commit falla: `git add` de ese archivo y repite el commit. Si el guardian rechaza, revisa el nombre de la rama y el `Closes #52`.
**Punto de control:** antes de abrir el PR, haz la Autoevaluación de abajo y ensaya con `/comprension`.

## Escalera de pistas (úsala solo cuando estés trabado, de arriba abajo)

**Paso 2 (T1).** Pista 1: `Annotated[tipo, metadato]` es un tipo con una etiqueta pegada; Python normalmente esconde la etiqueta. Pista 2: busca `get_type_hints` y su parámetro `include_extras` en <https://docs.python.org/3/library/typing.html#typing.get_type_hints>. Pista 3: pides los hints, comparas el conjunto de claves con el esperado y miras si `add_messages` está dentro de los metadatos de `messages`.

**Paso 3 (T2).** Pista 1: lo que sale es el estado final, y `messages` debe tener la lista completa de la conversación. Pista 2: busca `HumanMessage`, `AIMessage` en <https://python.langchain.com/docs/concepts/messages/>. Pista 3: invocas, guardas el resultado en una variable y comprueba longitud, tipo y contenido de cada posición.

**Paso 7 (T6).** Pista 1: un proceso hijo no hereda el `pythonpath` de pytest. Pista 2: busca `subprocess.run` (`capture_output`, `text`) en <https://docs.python.org/3/library/subprocess.html>; si el hijo no encuentra `agents`, comprueba con `python -c "import agents"` dentro del venv que el Paso 1 (`pip install -e`) quedó bien. Pista 3: ¿qué argumento de `python` permite ejecutar un texto corto, y qué atributo de `sys` lista los módulos cargados?

**Paso 8 (T7).** Pista 1: `print` escribe en la salida estándar, que se puede capturar. Pista 2: busca la fixture `capsys` en <https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html>. Pista 3: llamas a `main`, lees lo capturado con `capsys.readouterr()` y comparas con la línea esperada más salto de línea.

**Paso 8 (T8).** Pista 1: `argparse` sale con error cuando falta un argumento obligatorio y lo hace lanzando una excepción. Pista 2: busca `pytest.raises` y el atributo `code` de la excepción. Pista 3: abres el bloque de `raises(SystemExit)`, llamas `main([])` y luego comparas el código con `2`.

**Paso 9 (grafo).** Pista 1: un grafo se arma declarando el estado, registrando nodos, conectando aristas y compilando. Pista 2: busca `StateGraph`, `add_node`, `add_edge`, `START`, `END`, `compile` en <https://langchain-ai.github.io/langgraph/concepts/low_level/>. Pista 3: ¿qué recibe `StateGraph` al crearlo, qué dos aristas necesitas y qué método te da el grafo ejecutable? Para el nodo: ¿de dónde sale el texto (R1) y qué 3 claves exige R2?

**Paso 9 (CLI).** Pista 1: `argparse` convierte `sys.argv` en un objeto con atributos. Pista 2: busca `ArgumentParser`, `add_argument` (opciones con `--` y posicional) y `parse_args(argv)` en <https://docs.python.org/3/library/argparse.html>. Pista 3: ¿qué devuelve `parse_args`, qué valor por defecto lleva cada opción (sección 5c) y qué mensaje de la salida de `invoke` debes imprimir?

Si sigues trabado después de la Pista 3: comenta en el Issue con el error pegado como texto.

## Errores típicos de esta asignación

| Síntoma (lo que ves) | Causa probable | Qué hacer |
|---|---|---|
| `ModuleNotFoundError: No module named 'agents'` al correr la CLI | Estás fuera del entorno o fuera de la raíz del repo, o falta `pip install -e` | Activa `.venv`, ve a la raíz y repite el Paso 1 |
| `2 errors` al correr pytest tras implementar | Un `import` mal escrito en un archivo nuevo | Lee el nombre del módulo en el error; revisa `state.py`, `graph.py`, `cli.py` |
| `messages` sale con 1 solo elemento | El campo no tiene el reducer `add_messages` | Revisa `state.py` y el contrato 5a; T2 debe detectarlo |
| `mypy: call-overload` en `add_node` | Limitación conocida de tipos de LangGraph | Aplica solo la excepción permitida en 5b |
| `python -m agents.cli ...` no imprime nada y sale con `0` | Falta el bloque `if __name__ == "__main__":` | Agrégalo con `sys.exit(main())` |
| Tildes raras en la consola | Codificación de la ventana | `chcp 65001` y repite |
| `failed to import ... pytest` o puertas que no existen | `.[dev]` no instalado | `python -m pip install -e ".[dev]"` |
| `git commit` falla y modifica archivos | `ruff-format` reformateó | `git add` de esos archivos y repite el commit |

## Autoevaluación antes del PR

- [ ] Cada prueba (T1–T8) la escribí yo, la vi fallar y la vi pasar.
- [ ] Puedo explicar en voz alta, sin mirar, las 3 preguntas de comprensión del contrato (sección 11).
- [ ] Mi `git diff --name-only main` coincide con la sección 4 del contrato (6 rutas).
- [ ] Anoté en el PR cuántas interacciones usé con mi IA (máximo 12) y a quién consulté.
- [ ] Pegué en el PR el texto de la salida de `python -m agents.cli --phone 51900000000 "hola"`.

## Prompts sugeridos para tu IA (pequeños y verificables)

**Sí (pega solo lo puntual):**
1. «Explícame en 5 líneas qué hace un reducer en LangGraph con un ejemplo que sume números, no de mi proyecto.»
2. «Me sale este error de pytest (pego el texto completo). ¿Qué significa, sin darme el arreglo?»
3. «Aquí está la salida de `git diff --name-only main` y la lista de la sección 4. ¿Falta o sobra algo?»
4. «¿Qué diferencia hay entre `invoke` y `stream` en LangGraph? Solo el concepto.»
5. «Tengo esta prueba (pego T2). ¿Detectaría un reducer que reemplaza en vez de sumar? Dime por qué sí o no.»

**Prohibidos:**
- «Escríbeme `graph.py` / `AgentState` / la CLI»: el contrato te lo pide a ti y la sección 9 lo prohíbe.
- «Redacta mi PR y mis respuestas de comprensión»: la puerta de comprensión mide **tu** entendimiento.
