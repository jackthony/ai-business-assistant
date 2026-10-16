# [S05 D3] Paso a paso guiado — Memoria persistente con SqliteSaver (Issue #54)

> **Para quién:** practicante de 2.º año de AI Engineering, con Python básico y Git básico, que **no** conoce todavía LangGraph, checkpointers, SQLite ni los context managers (`with`). Este archivo te acompaña **mientras trabajas**; el contrato ([`S05_D3.md`](S05_D3.md)) dice **qué** debe quedar. Aquí aprendes **cómo abordarlo sin perderte**.
>
> **Reglas del juego:** no hay código de la solución aquí (si lo hubiera, no aprenderías). Hay explicación, pistas y puntos de control. Una sesión dura ~3 h; los tiempos son una guía. Todos los comandos son para Windows (**cmd**, no PowerShell), desde la raíz del repo.
>
> **Punto de partida:** esta asignación se apoya en el agente real que ya está en `main` (RAG con citas, agendar con aprobación, derivación a una persona). El Paso 0 lo comprueba. Si tenías avanzado el contrato anterior (el del grafo de eco), **para y pregunta en el Issue #54**: parte de lo que hiciste se aprovecha.

> **Revisión automática de tu avance:** desde tu primer commit haz `git push -u origin <tu-rama>`. El robot abre solo un **PR en borrador** y deja **un comentario que se actualiza en cada push**: cuántos archivos del contrato ya trabajaste, cuáles te faltan, si tocaste algo fuera de la sección 4 y cuál es tu siguiente paso, con pistas (no con la solución). Léelo antes de seguir con el paso siguiente; si no lo entiendes, usa `/pista`. Haz push **al terminar cada paso en verde**, no solo al final. Cuando acabes, marca el PR *Ready for review* y responde la sección 11.

## Mapa de la sesión

| Bloque | Tiempo | Resultado que puedes comprobar |
|---|---|---|
| Lectura + mini-conceptos | 20 min | Sabes explicar qué guarda un checkpointer, para qué sirve el `thread_id` y por qué no se pisa el estado guardado |
| Calentamiento | 15 min | Un dato guardado en un archivo SQLite sigue ahí tras cerrar y reabrir |
| Pasos 0–3 (terreno, entorno, línea base; `pip install` puede tardar en PCs antiguas) | 30–35 min | `N passed` antes de tocar código |
| Pasos 4–12 (T1–T9, una prueba por paso) | 90 min | Las 9 pruebas escritas; el rojo completo se comprueba en el Paso 12 |
| Pasos 13–15 (código, modo estricto, orden) | 50 min | `N+9 passed` |
| Pasos 16–17 (4 puertas, commits y PR) | 30 min | PR abierto con `Closes #54` |

> Son ~4 h de trabajo: si no alcanzas en una sesión, **para después del Paso 12** (rojo completo, 9 pruebas escritas) y sigue en la siguiente. Es un buen punto de corte.

## Mini-conceptos (léelos antes del Paso 0)

Para cada concepto: **Idea**, **Analogía**, **Ejemplo** (fuera de este proyecto) y **Profundiza**.

**1. Checkpointer (persistencia).**
- **Idea:** es quien guarda el estado del grafo en un lugar durable después de cada paso. Si el programa se apaga, el estado sigue en el archivo.
- **Analogía:** el guardado automático de un videojuego: apagas la consola, vuelves, y retomas en el último punto guardado.
- **Ejemplo** (con `import json` arriba):
```python
with open("ficha.json", "w", encoding="utf-8") as f:
    json.dump({"visitas": 2}, f)
```
- **Profundiza:** <https://langchain-ai.github.io/langgraph/concepts/persistence/>

**2. `thread_id` (hilo).**
- **Idea:** es la etiqueta que dice a qué conversación pertenece una invocación. Mismo `thread_id`, mismo historial; distinto `thread_id`, historial separado.
- **Analogía:** el número de expediente de un consultorio: reúne todas las visitas de una persona, y dos personas nunca comparten número.
- **Ejemplo:** `carpetas = {"ana": [], "luis": []}` y luego `carpetas["ana"].append("hola")`. La lista de `"luis"` sigue vacía.
- **Profundiza:** <https://langchain-ai.github.io/langgraph/concepts/persistence/>

**3. Context manager (`with`).**
- **Idea:** `with` abre un recurso, te lo da mientras estás dentro del bloque y lo cierra al salir, aunque haya un error.
- **Analogía:** alquilar una bicicleta: la recoges al entrar al bloque y la devuelves al salir, te hayas caído o no.
- **Ejemplo:**
```python
with open("notas.txt", "w", encoding="utf-8") as f:
    f.write("hola")
```
- **Profundiza:** <https://docs.python.org/3/reference/compound_stmts.html#the-with-statement>

**4. SQLite como archivo.**
- **Idea:** SQLite es una base de datos que vive en **un solo archivo** (`.db`), sin servidor. Si borras el archivo, borras la memoria.
- **Analogía:** una libreta de bolsillo, frente a una biblioteca con personal (un servidor de base de datos).
- **Ejemplo:**
```python
import sqlite3
con = sqlite3.connect("agenda.db")
con.close()
```
- **Profundiza:** <https://docs.python.org/3/library/sqlite3.html>

**5. `tmp_path` de pytest.**
- **Idea:** `tmp_path` es una carpeta temporal y única que pytest crea para cada prueba. Así cada prueba escribe sus archivos sin tocar el repo ni a otras pruebas.
- **Analogía:** una mesa de trabajo alquilada solo para tu examen, que se limpia al salir.
- **Ejemplo:** `ruta = tmp_path / "notas.txt"` apunta a una carpeta nueva en cada ejecución (la barra `/` une carpeta y nombre de archivo).
- **Profundiza:** <https://docs.pytest.org/en/stable/how-to/tmp_path.html>

**6. No pisar el estado guardado.**
- **Idea:** cada vez que invocas el grafo, lo que pasas en la entrada **se escribe** sobre el estado del hilo. Si en cada mensaje vuelves a mandar `status="nuevo"`, borras lo que el hilo ya tenía guardado.
- **Analogía:** una ficha de paciente con la casilla «derivado a especialista». Si cada visita alguien reescribe la ficha entera con la casilla vacía, la derivación se pierde.
- **Ejemplo** (fuera de este proyecto):
```python
ficha = {"nombre": "Ana", "derivada": True}
ficha.update({"nombre": "Ana", "derivada": False})  # ¿qué pasó con "derivada"?
```
- **Profundiza:** <https://langchain-ai.github.io/langgraph/concepts/persistence/>

## Calentamiento (fuera del proyecto)

Haz esto en el Escritorio, **fuera del repo**, en un archivo `practica_sqlite.py`:

1. Abre un archivo `practica.db` con `sqlite3.connect`.
2. Crea una tabla con una columna de texto e inserta una fila con el valor `hola`. Guarda los cambios (`commit`) y cierra la conexión.
3. Vuelve a abrir `practica.db` en otro proceso (otra ejecución del script) y lee la fila.

**Resultado esperado:** la fila `hola` sigue ahí. Luego investiga una pregunta: ¿`with sqlite3.connect(...)` cierra la conexión o solo guarda los cambios? La respuesta está en la documentación de `sqlite3`. Esa diferencia te servirá en el Paso 11. Borra el archivo al terminar.

## Paso a paso

### Paso 0 — Prepara tu terreno
**Haz esto:** en cmd, desde la raíz del repo:
```bat
git checkout main
git pull
dir src\infrastructure\wiring.py
dir tests\conftest.py
```
**Por qué:** esta asignación modifica `wiring.py` y usa lo que `conftest.py` ya trae (`store` y `ScriptedModel`). Si no están, tu copia de `main` está vieja o algo falló.
**Debes ver:** `Already up to date.` o commits nuevos; `dir` lista los dos archivos.
**Si falla:** si `dir` no encuentra alguno, **para**. Comenta en el Issue #54 con la salida pegada como texto (contrato, sección 12). No crees esos archivos tú mismo para seguir.
**Punto de control:** ¿cuál es la función de `wiring.py` que hoy crea la memoria en RAM, y cómo la reconociste?

### Paso 1 — Rama y entorno virtual
**Haz esto:**
```bat
git checkout -b issue-54-memoria-persistente
py -3.11 -m venv .venv
.venv\Scripts\activate
python --version
```
**Por qué:** una rama por Issue (TBD) y un entorno aislado evitan mezclar tu trabajo con `main` y con otros proyectos de tu PC.
**Debes ver:** `Switched to a new branch 'issue-54-memoria-persistente'`; el prompt empieza con `(.venv)`; `python --version` dice `Python 3.11.x`.
**Si falla:** si `py -3.11` no existe, instala Python 3.11 (no 3.12 ni 3.13; ver `program/02_REFERENCE/stack-versiones.md`). Si PowerShell bloquea la activación, usa cmd. Si sigue fallando, pega el error en el Issue.
**Punto de control:** ¿qué te dice `git branch --show-current`? Debe llevar el número 54.


### Paso 2 — Dependencia y hook de pre-commit
**Haz esto:** abre `pyproject.toml`. Dentro de `dependencies`, junto a `"langgraph>=1,<2",`, agrega `"langgraph-checkpoint-sqlite>=3,<4",`. No dupliques `langgraph`. Luego, en cmd:
```bat
findstr /N "langgraph" pyproject.toml
python -m pip install -e ".[dev]"
python -c "from langgraph.checkpoint.sqlite import SqliteSaver; print('OK')"
pre-commit install
```
**Por qué:** `SqliteSaver` vive en un paquete aparte; sin esa línea no puedes importarlo. `pre-commit` corre ruff en cada commit (AGENTS.md).
**Debes ver:** `findstr` muestra exactamente dos líneas (`langgraph` y `langgraph-checkpoint-sqlite`); `OK`; una línea que empieza por `pre-commit installed at`.
**Si falla:** `ModuleNotFoundError` en el comando de `OK`: revisa que la línea esté dentro de `dependencies` y repite `pip install`. Si `pip` falla, pega el error completo en el Issue.
**Punto de control:** ¿las dos dependencias quedaron dentro de `[project] dependencies` y no en otra sección?


### Paso 3 — Línea base (sin tu código)
**Haz esto:** en cmd, con `(.venv)` activo:
```bat
pytest tests -q
```
**Por qué:** si algo ya está en rojo antes de tu código, sabrás que no lo causaste tú.
**Debes ver:** `N passed`, sin fallos. Anota N. Al terminar, el total debe ser N+9.
**Si falla:** para y repórtalo en el Issue (contrato, sección 12). No lo arregles en esta rama.
**Punto de control:** ¿cuál es tu N?

> **Antes de los pasos 4–10:** crea `tests\test_memory_checkpoint.py` (vacío) y ve añadiendo **una función por paso**. Cada una se escribe y se ve fallar. **No implementes nada hasta el Paso 11**: así lo pide el contrato (sección 6, nota «Rojo correcto»). Nombra cada función con su ID al inicio (`test_t1_...`, `test_t2_...`…) para poder aislarla con `-k`.



> **Antes de los pasos 4–12:** crea `tests\test_memory_checkpoint.py` (vacío) y ve añadiendo **una función por paso**. Cada una se escribe y se ve fallar. **No implementes nada hasta el Paso 13**: así lo pide el contrato (sección 6, nota «Rojo correcto»). Nombra cada función con su ID al inicio (`test_t1_...`, `test_t2_...`…) para poder aislarla con `-k`. Las pruebas **no** escriben su propio índice ni su propio modelo: reutilizan el fixture `store` y la clase `ScriptedModel` que ya están en `tests\conftest.py` (mira cómo las usan `tests\test_agent_info.py` y `tests\test_handoff.py`; no las modifiques). Te conviene escribir dos funciones auxiliares en tu archivo, una que arme el grafo con el `saver` y otra que haga una invocación siguiendo la sección 5.5.

### Paso 4 — T1: dos mensajes del mismo teléfono, el historial crece
**Haz esto:** escribe T1. Dentro de **un solo** `with open_checkpointer(db)`, arma el grafo y haz dos invocaciones con el teléfono `51900000000`, ambas con la pregunta de precio. Comprueba la salida de la segunda invocación. La fila T1 de la sección 6 del contrato dice la salida exacta; la forma de la entrada está en la sección 5.5 (¡el segundo mensaje no lleva `intent` ni `status`!).
**Por qué:** el checkpointer debe recordar el hilo dentro de la misma sesión, sin que tú pases el historial a mano.
**Debes ver:** si corres el archivo ahora, error de colección `ModuleNotFoundError` (rojo correcto: aún no existen los módulos de `memory`). Recuerda escribir al inicio del archivo los imports de la sección 6 del contrato; sin ellos no hay esa causa.
**Si falla:** si el error es `SyntaxError` o `NameError` en tu prueba, corrígela primero: un rojo por otra razón no vale.
**Punto de control:** ¿cuántos mensajes debe tener la salida, de qué tipo es cada uno y cuál es el primero?

### Paso 5 — T2: el historial sobrevive a un reinicio
**Haz esto:** escribe T2 con un archivo `.db` dentro de `tmp_path`. Simula dos «procesos»: el primero abre el `with`, invoca `"hola"` y sale del bloque; el segundo abre un `with` nuevo sobre el **mismo** archivo, arma el grafo otra vez e invoca `"¿precios?"` con el mismo teléfono. Comprueba ambas salidas (fila T2 de la sección 6).
**Por qué:** es la prueba de persistencia real: el «reinicio» es cerrar la conexión y volver a abrir el archivo.
**Debes ver:** nada nuevo: el archivo entero sigue con el mismo error de colección. Escribe la función; el rojo se comprueba una vez en el Paso 10.
**Si falla:** si tu prueba guarda el historial en una variable de Python en vez de en el archivo, no está probando un reinicio. Corrígela.
**Punto de control:** ¿qué cambia entre el «proceso 1» y el «proceso 2» de tu prueba, y qué se mantiene igual?


### Paso 6 — T3: dos teléfonos no comparten hilo
**Haz esto:** escribe T3 con el mismo archivo. El teléfono `51900000001` envía la pregunta de precio; después el `51900000002` envía `"¿Cuál es la dirección del local?"`. Comprueba que la salida del segundo teléfono es **exactamente** la que indica la fila T3 de la sección 6 (no basta con «no contiene la pregunta de precio»).
**Por qué:** dos personas no pueden ver la conversación de otra. Esa es la regla de aislamiento por `thread_id`.
**Debes ver:** nada nuevo: el archivo entero sigue con el mismo error de colección. Escribe la función; el rojo se comprueba una vez en el Paso 10.
**Si falla:** si usas un teléfono distinto a los tres sintéticos (`51900000000`, `51900000001`, `51900000002`), cámbialo ahora. Nunca uses un número real.
**Punto de control:** ¿por qué esta prueba fallaría si los dos teléfonos usaran el mismo hilo?


### Paso 7 — T4: teléfono vacío o solo espacios se rechaza
**Haz esto:** escribe T4. Llama a la función de configuración con `""` y con `"   "`, y comprueba que en los dos casos se lanza `ValueError` (fila T4 de la sección 6). Son **dos** bloques `pytest.raises` dentro de **una** misma función: el contrato cuenta una función por prueba.
**Por qué:** un hilo sin identificador mezcla conversaciones de personas distintas. Es mejor fallar que mezclar.
**Debes ver:** nada nuevo: el archivo entero sigue con el mismo error de colección. Escribe la función; el rojo se comprueba una vez en el Paso 10.
**Si falla:** si no recuerdas cómo esperar una excepción en pytest, mira la Escalera de pistas (Paso 7).
**Punto de control:** ¿por qué un texto hecho solo de espacios cuenta como vacío?


### Paso 8 — T5: `.env.example` declara el modo estricto
**Haz esto:** escribe T5. Lee `.env.example` desde la raíz del repo, calculando la ruta **desde el archivo de prueba** (no con una ruta fija tipo `C:\...`). Comprueba que contiene la línea exacta `LANGGRAPH_STRICT_MSGPACK=true` (fila T5 de la sección 6).
**Por qué:** deja documentado que el modo estricto es parte del proyecto, sin guardar valores reales.
**Debes ver:** el mismo error de colección del paso anterior. Como el archivo entero no se puede colectar, T5 aún no corre.
**Si falla:** si tu ruta es absoluta (`C:\Users\...`), no funcionará en otra PC. Usa una ruta relativa al archivo de prueba.
**Punto de control:** ¿desde qué carpeta calculas la raíz del repo, y por qué no desde la carpeta donde está tu cmd?


### Paso 9 — T6: `*.db` está ignorado por Git
**Haz esto:** escribe T6. Lee `.gitignore` desde la raíz del repo y comprueba que contiene la línea exacta `*.db` (fila T6 de la sección 6).
**Por qué:** un `.db` de conversaciones nunca debe subir a un repo público.
**Debes ver:** el mismo error de colección del paso anterior.
**Si falla:** si la línea tiene espacios sobrantes o está escrita distinto, la comparación exacta no coincide. Mírala con `type .gitignore`.
**Punto de control:** ¿por qué confiar en `.gitignore` es mejor que recordar «no subir cosas»?


### Paso 10 — T7: la ruta la decide quien llama
**Haz esto:** escribe T7. Abre `open_checkpointer` con `str(tmp_path / "chat.db")`, haz una invocación con `51900000000` y comprueba que `chat.db` existe dentro de `tmp_path` (fila T7 de la sección 6). 
**Por qué:** la función no decide dónde guardar; quien la llama sí. Así las pruebas nunca ensucian el repo.
**Debes ver:** nada nuevo: el archivo entero sigue con el mismo error de colección. Escribe la función; el rojo completo se comprueba en el Paso 12.
**Si falla:** si el archivo aparece dentro del repo en vez de `tmp_path`, tu prueba tiene una ruta fija. Corrígela.
**Punto de control:** ¿cuántas funciones `test_t*` tienes y cómo se llama cada una?


### Paso 11 — T8: el congelado por derivación sobrevive a un reinicio
**Haz esto:** escribe T8 con un archivo `.db` en `tmp_path`. «Proceso 1»: abre el `with`, arma el grafo e invoca `"Quiero hablar con una persona"` con `51900000000`; comprueba que el estado queda en `handoff_requested`. «Proceso 2»: abre un `with` nuevo sobre el mismo archivo, arma el grafo otra vez **con un modelo de prueba nuevo** e invoca la pregunta de precio. Comprueba lo que dice la fila T8 de la sección 6: sigue congelado, la lista creció **solo en 1** mensaje y el modelo nuevo no fue llamado.
**Por qué:** cuando el bot deriva a una persona, tiene que **callar** hasta que alguien lo libere. Si la memoria se perdiera al reiniciar, el bot volvería a contestar sobre un tema que debía atender una especialista. Es la razón de seguridad de tener memoria durable.
**Debes ver:** nada nuevo: el archivo entero sigue con el mismo error de colección. Escribe la función; el rojo completo se comprueba en el Paso 12.
**Si falla:** si tu segunda invocación vuelve a mandar `intent` y `status`, pisarás el estado guardado y el bot hablará: relee el mini-concepto 6 y la sección 5.5.
**Punto de control:** ¿qué dato guardado en el archivo impide que el bot conteste en el «proceso 2», y quién podría liberarlo?

### Paso 12 — T9: la CLI con `--db` recuerda entre corridas
**Haz esto:** escribe T9. Reemplaza `cli.build_default_graph` con `monkeypatch.setattr` por una función `(tenant, checkpointer=None)` que devuelva el grafo armado con ese `checkpointer` (mira cómo lo hace `tests\test_agent_cli.py`, pero esa recibe un solo argumento). Llama `cli.main` tres veces con el mismo `--phone` y `--db`: la pregunta de precio, `"Quiero hablar con una persona"` y otra vez la pregunta de precio. Después abre el `.db` y comprueba lo que dice la fila T9 de la sección 6. Cuando termines, corre el conjunto completo:
```bat
pytest tests -q
```
**Por qué:** la CLI es la forma de ver la memoria funcionando a mano. Y la tercera corrida demuestra que la CLI tampoco pisa el estado guardado.
**Debes ver:** `ERROR collecting tests/test_memory_checkpoint.py`, `ModuleNotFoundError: No module named 'memory.thread_config'` (o `'memory.sqlite_checkpointer'`) y `Interrupted: 1 error during collection`. Ese es el rojo completo y correcto: las 9 pruebas escritas, ninguna implementada.
**Si falla:** si el rojo es por otra causa (`SyntaxError`, `NameError`), corrígela antes de seguir. Si tu prueba usa un teléfono real, cámbialo ahora.
**Punto de control:** ¿cuántas funciones `test_t*` tienes y cómo se llama cada una?

### Paso 13 — Implementa lo mínimo y pon todo en verde
**Haz esto:** en este orden, siguiendo la sección 5 del contrato, **uno a la vez**:
- a. `src\memory\thread_config.py` (§5.1).
- b. `src\memory\sqlite_checkpointer.py` (§5.2).
- c. `src\infrastructure\wiring.py`: solo el parámetro `checkpointer` opcional (§5.3).
- d. `src\agents\cli.py`: la opción `--db` (§5.4).
- e. `.gitignore`: agrega `*.db` al final.
- f. `.env.example`: agrega `LANGGRAPH_STRICT_MSGPACK=true` con salto de línea al final.

Luego corre `pytest tests -q`.

**Por qué:** ir archivo por archivo te enseña qué pieza necesita cada prueba.
**Debes ver:** mientras falte algún módulo, el archivo sigue con `ERROR collecting`. Cuando estén los seis archivos, `N+9 passed`, sin `failed` ni `error`.
**Si falla:** lee el error de abajo hacia arriba; la última línea suele nombrar la causa. Si la CLI rompe una prueba **existente** (`test_agent_cli.py`), es que sin `--db` cambiaste cómo llama a `build_default_graph` o intentas leer el estado de un grafo sin memoria: relee la sección 5.4.
**Punto de control:** ¿qué cambiaste en `wiring.py` y qué **no** cambiaste (`graph.py`, `AgentState`, los nodos)?

### Paso 14 — Modo estricto activo (T1–T9 con la variable)
**Haz esto:** en **la misma** ventana de cmd, antes de correr Python o pytest:
```bat
set LANGGRAPH_STRICT_MSGPACK=true
python -c "import langgraph.checkpoint.serde._msgpack as m; print(m.STRICT_MSGPACK_ENABLED)"
pytest tests -q
pytest tests\test_agent_graph.py tests\test_agent_cli.py -q
```
**Por qué:** la librería lee esa variable **al importarse**. Si la pones después, tu proceso no está en modo estricto y la prueba no demuestra nada.
**Debes ver:** `True`; después `N+9 passed`; y `6 passed` en la regresión de las pruebas existentes, sin tocarlas.
**Si falla:** si imprime `False`, cierra esa ventana, abre otra y repite desde `set`. `set` dura solo en la ventana donde lo escribiste.
**Punto de control:** ¿por qué la regla de seguridad vive en el entorno y no en el código (contrato, §5.2)?


### Paso 15 — Independencia de orden: T2 sola
**Haz esto:**
```bat
pytest tests\test_memory_checkpoint.py -k t2 -q
```
**Por qué:** una prueba de reinicio que depende de las demás no es confiable: si cambia el orden, se rompe.
**Debes ver:** `1 passed, 8 deselected`.
**Si falla:** si T2 depende de un archivo que creó otra prueba, dale su propio `tmp_path`.
**Punto de control:** ¿hay algún nombre de archivo fijo en tu T2?


### Paso 16 — Las 4 puertas
**Haz esto:** copia el comando exacto de la sección 7, paso 11 del contrato, o este:
```bat
ruff check src tests && mypy src --ignore-missing-imports && pytest tests -q && bandit -r src -x tests -ll
```
**Por qué:** es lo mismo que corre el CI estricto; si pasa aquí, no te sorprende en GitHub.
**Debes ver:** `All checks passed!` · `Success: no issues found in ... source files` · `N+9 passed` · `No issues identified.`
**Si falla:** corrígelo antes de commitear. No apagues mypy ni ruff (contrato, sección 9).
**Punto de control:** ¿pasó todo sin apagar ninguna regla (sin `--ignore`, sin `noqa` global)?


### Paso 17 — Commits pequeños, push y PR
**Haz esto:** haz los siete commits de la sección 7, paso 12 del contrato, **uno por cambio**: para cada uno, `git add` solo de sus rutas (nunca `git add .`; el commit de pruebas queda en rojo a propósito y el PR se squashea) y luego `git commit -m` con el mensaje indicado. Después:
```bat
git push -u origin issue-54-memoria-persistente
```
Abre el PR contra `main` con `Closes #54`, la plantilla completa y tus respuestas de la sección 11 del contrato.

**Por qué:** commits pequeños dejan historia legible; el PR es la evidencia que el monitor revisa contra el contrato.
**Debes ver:** cada hook de pre-commit imprime `Passed`; `branch 'issue-54-memoria-persistente' set up to track 'origin/issue-54-memoria-persistente'`; en el PR, `guardian-tbd / reglas-tbd` y `CI estricto / calidad` en verde.
**Si falla:** si un hook modifica archivos, haz `git status --short`, `git add` de esos archivos y repite **el mismo** commit. No uses `--no-verify`. Si el guardián rechaza el PR, revisa el nombre de la rama y el `Closes #54`.
**Punto de control:** antes de abrir el PR, ¿respondiste las 3 preguntas de la sección 11 con tus palabras? Si no, ensaya con `/comprension`.


## Escalera de pistas (úsala solo cuando estés trabado, de arriba abajo)

**Paso 5 (T2).** Pista 1: un objeto que se crea con `with` puede cerrarse y volverse a abrir; el archivo es lo único que sobrevive al cierre. Pista 2: busca `SqliteSaver` y `from_conn_string` en <https://langchain-ai.github.io/langgraph/concepts/persistence/> y en <https://pypi.org/project/langgraph-checkpoint-sqlite/>. Pista 3: en cada «proceso» abres el `with` con la misma ruta, armas el grafo y lo invocas con el mismo `thread_id`; compara las listas de mensajes de cada salida.

**Paso 7 (T4).** Pista 1: `strip()` quita espacios al principio y al final de un texto. Pista 2: busca cómo esperar una excepción en <https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions> (`pytest.raises`). Pista 3: pruebas cada valor malo dentro de un bloque `with pytest.raises(ValueError):` y compruebas que la excepción aparece.

**Paso 8 (T5).** Pista 1: `Path(__file__)` es la ruta de tu archivo de prueba. Pista 2: busca `resolve` y `parents` en <https://docs.python.org/3/library/pathlib.html>. 

**Paso 10 (T7).** Pista 1: `tmp_path` se comporta como una carpeta y `/` une carpeta con nombre de archivo. Pista 2: revisa <https://docs.pytest.org/en/stable/how-to/tmp_path.html>. Pista 3: construyes la ruta del `.db` dentro de `tmp_path`, la pasas a `open_checkpointer`, haces una invocación y compruebas que el archivo existe.

**Paso 11 (T8).** Pista 1: el estado `status` queda guardado en el archivo igual que los mensajes; en el «proceso 2» ya existe cuando llegas. Pista 2: relee la sección 5.5 del contrato y el mini-concepto 6. Pista 3: en el «proceso 2» tu invocación lleva solo `messages`, `phone` y `tenant`; para saber si el hilo ya existe, pregunta por su estado guardado antes de armar la entrada.

**Paso 13 (checkpointer).** Pista 1: el checkpointer es un objeto que la librería crea a partir de la ruta de un archivo; piensa en el `with` del mini-concepto 3. Pista 2: busca `SqliteSaver` y `from_conn_string` en <https://langchain-ai.github.io/langgraph/concepts/persistence/>. Pista 3: ¿qué debe devolver `open_checkpointer` según la sección 5.2 y qué método de `SqliteSaver` lo entrega? ¿Qué argumento de la compilación recibe el saver? ¿Qué forma tiene la configuración de la sección 5.1?

**Paso 14 (modo estricto).** Pista 1: la librería `langgraph` lee la variable cuando se importa; debe existir en la ventana antes de ese import. Pista 2: revisa <https://docs.python.org/3/library/os.html#os.environ>. Pista 3: en la misma ventana de cmd, primero escribes `set` y después ejecutas Python; si cambias de ventana, empiezas de nuevo.

Si sigues trabado después de la Pista 3: comenta en el Issue #54 con el error pegado como texto.

## Errores típicos de esta asignación

| Síntoma (lo que ves) | Causa probable | Qué hacer |
|---|---|---|
| `dir src\infrastructure\wiring.py` no encuentra el archivo | Tu copia de `main` está vieja | `git pull`; si sigue sin estar, para y comenta en el Issue #54 (Paso 0) |
| `No module named 'langgraph.checkpoint.sqlite'` | La dependencia no está en `pyproject.toml` o no se instaló | Revisa el Paso 2 y repite `python -m pip install -e ".[dev]"` |
| `STRICT_MSGPACK_ENABLED` imprime `False` | La variable se definió en otra ventana o después de importar | Cierra la ventana, abre otra, repite desde `set` (Paso 14) |
| `database is locked` | Dos conexiones abiertas al mismo `.db` a la vez | Cada `with` debe cerrarse antes de abrir otro sobre el mismo archivo |
| En T2, el «proceso 2» solo ve 2 mensajes | El `thread_id` no coincide o no se pasó la configuración a la invocación | Revisa la sección 5.4 del contrato |
| En T1, la salida tiene 2 mensajes en vez de 4 | El historial se pasa a mano, o el checkpointer no se pasó al grafo | Entrada solo con el mensaje nuevo; revisa §5.3 y §5.5 |
| En T8, el bot contesta en el «proceso 2» (o T9 deja 6 mensajes) | Mandaste `intent=None` y `status="nuevo"` en un mensaje que no era el primero del hilo y pisaste el congelado | Sección 5.5: esos dos valores solo van en el primer mensaje del hilo |
| Se rompe `test_agent_cli.py` (error «No checkpointer set») | La CLI consulta el estado guardado aunque no se pasó `--db` | Solo se consulta con `--db` (§5.4) |
| En T3, aparece `"hola"` en la salida del segundo teléfono | Los dos teléfonos usan el mismo hilo | Revisa cómo se construye la configuración por teléfono (§5.1) |
| T4 no lanza `ValueError` con `"   "` | Falta quitar espacios antes de comparar | Mira la Escalera, Paso 7 |
| T5 o T6 fallan con «línea no encontrada» | La línea tiene espacios sobrantes, está escrita distinto o el archivo no termina en salto de línea | Mira el archivo con `type` y compara carácter a carácter |
| `git status` muestra un `.db` | `.gitignore` no tiene `*.db` o no se guardó | Revisa el paso 11.d y `git check-ignore -v` sobre el archivo |
| `git diff --name-only main` lista más de 8 rutas | Editaste otro archivo, o un hook cambió algo que no debía | Revisa la sección 4 del contrato y quita lo que sobra |
| `git commit` falla y modifica archivos | Un hook de formato reformateó | `git status --short`, `git add` de esos archivos, repite el mismo commit |
| Tildes raras en la consola | Codificación de la ventana | Ejecuta `chcp 65001` y repite |

## Autoevaluación antes del PR

- [ ] Cada prueba (T1–T9) la escribí yo, la vi fallar y la vi pasar.
- [ ] Puedo explicar en voz alta, sin mirar, las 3 preguntas de comprensión del contrato (sección 11).
- [ ] `git diff --name-only main` coincide con las 8 rutas de la sección 4 del contrato.
- [ ] `git status --short` no muestra ningún `.db` ni `.env`.
- [ ] Anoté en el PR cuántas interacciones usé con mi IA (tope 10–15) y a quién consulté.
- [ ] El PR tiene `Closes #54`.

## Prompts sugeridos para tu IA (pequeños y verificables)

**Sí (pega solo lo puntual):**
1. «Explícame en 5 líneas qué es un context manager y por qué `with` cierra el recurso, con un ejemplo que no sea de mi proyecto.»
2. «Me sale este error de pytest (pego el texto completo). ¿Qué significa? No me des el arreglo.»
3. «Aquí está la salida de `git diff --name-only main` y la lista de 8 rutas de la sección 4. ¿Falta o sobra algo?»
4. «¿Qué diferencia hay entre `thread_id` y un id de usuario en un sistema de chat? Solo el concepto.»
5. «Tengo esta prueba T3 (la pego). ¿Detectaría que dos teléfonos comparten hilo? Dime sí o no y por qué.»
6. «¿Por qué volver a mandar un valor inicial en cada invocación puede borrar lo que ya estaba guardado? Explícamelo con un ejemplo que no sea de mi proyecto.»

**Prohibidos:**
- «Escríbeme `thread_config.py`, `sqlite_checkpointer.py` o los cambios de `wiring.py` y de la CLI completos»: el contrato te los pide a ti, y la sección 9 lo prohíbe.
- «Redacta mis respuestas de comprensión del PR»: la puerta de comprensión mide **tu** entendimiento.
