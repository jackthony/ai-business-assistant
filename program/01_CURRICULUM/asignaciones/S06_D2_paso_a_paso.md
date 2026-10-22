# [S06 D2] Paso a paso guiado — Ingesta reproducible y evaluación de la recuperación del RAG (Issue #157)

> **Para quién:** practicante de 2.º año de AI Engineering, con Python básico y Git básico, que **no** conoce todavía las funciones hash, la medición de un buscador ni la calibración de un umbral. Este archivo te acompaña **mientras trabajas**; el contrato ([`S06_D2.md`](S06_D2.md)) dice **qué** debe quedar. Aquí aprendes **cómo abordarlo sin perderte**.
>
> **Reglas del juego:** no hay código de la solución aquí (si lo hubiera, no aprenderías). Hay explicación, pistas y puntos de control. Una sesión dura ~3 h; los tiempos son una guía. Todos los comandos son para Windows (**cmd**, no PowerShell), desde la raíz del repo.
>
> **Punto de partida:** esta asignación se apoya en el RAG que ya está en `main` (`src/rag/`). El Paso 0 lo comprueba. Si ya habías empezado a escribir un `etl_servicios.py`, **para y pregunta en el Issue #157**: el contrato cambió porque esa pieza ya existe.

> **Revisión automática de tu avance:** desde tu primer commit haz `git push -u origin <tu-rama>`. El robot abre solo un **PR en borrador** y deja **un comentario que se actualiza en cada push**: cuántos archivos del contrato ya trabajaste, cuáles te faltan, si tocaste algo fuera de la sección 4 y cuál es tu siguiente paso, con pistas (no con la solución). Haz push **al terminar cada paso en verde**, no solo al final.

## Mapa de la sesión

| Bloque | Tiempo | Resultado que puedes comprobar |
|---|---|---|
| Lectura + mini-conceptos | 25 min | Sabes explicar qué es una huella y qué mide un caso de oro |
| Calentamiento | 10 min | Ves con tus ojos que `hash()` cambia entre procesos y `crc32` no |
| Paso 0 (terreno, entorno, línea base) | 25 min | `N passed` antes de tocar código |
| Pasos 1–3 (huella, ingesta, CLI) | 55 min | `8 passed` en `test_rag_ingest.py` |
| Pasos 4–5 (evaluación y umbral) | 45 min | `8 passed, 4 deselected` |
| Pasos 6–7 (tu archivo de oro y la calibración) | 40 min | `12 passed` en `test_rag_evaluate.py` |
| Pasos 8–9 (evidencia, 4 puertas, commits y PR) | 30 min | PR abierto con `Closes #157` |

> Son ~3,5 h: si no alcanzas en una sesión, **para después del Paso 3** (la ingesta funciona) y sigue en la siguiente.

## Mini-conceptos (léelos antes del Paso 0)

Para cada concepto: **Idea**, **Analogía**, **Ejemplo** (fuera de este proyecto) y **Profundiza**.

**1. Huella (hash criptográfico).**
- **Idea:** una función que convierte cualquier texto en una cadena corta de longitud fija. El mismo texto da siempre la misma cadena; si cambias una sola letra, la cadena cambia por completo.
- **Analogía:** el sello de lacre de una carta: si alguien la abrió, el sello ya no coincide.
- **Ejemplo:**
```python
import hashlib
hashlib.sha256("hola".encode("utf-8")).hexdigest()
```
- **Profundiza:** <https://docs.python.org/3/library/hashlib.html>

**2. Hash estable frente a `hash()` de Python.**
- **Idea:** la función incorporada `hash()` de un texto **cambia cada vez que arranca Python** (es una protección intencional). Sirve para diccionarios, no para identificar contenido. Para eso hay `hashlib` o `zlib.crc32`, que siempre dan lo mismo.
- **Analogía:** el número de turno del banco (cambia cada día) frente a tu DNI (siempre el mismo).
- **Ejemplo:** lo verás en el Calentamiento.
- **Profundiza:** <https://docs.python.org/3/reference/datamodel.html#object.__hash__>

**3. Casos de oro (golden set).**
- **Idea:** una lista corta de preguntas cuya respuesta correcta **ya conoces**. Corres tu buscador sobre ellas y cuentas aciertos. Si cambias algo y los aciertos bajan, lo notas al instante.
- **Analogía:** un examen con la clave de respuestas: sabes cuántas acertó el sistema sin adivinar.
- **Ejemplo:** `casos = [("capital de Perú", "Lima")]` y compruebas si tu buscador devuelve `"Lima"`.
- **Profundiza:** `program/02_REFERENCE/agent-engineering-handbook.md` (evaluación).

**4. Distancia y umbral.**
- **Idea:** el RAG mide qué tan lejos queda cada documento de la pregunta (0 = idéntico; más grande = más distinto). El **umbral** es la distancia máxima que aceptas: todo lo más lejano se descarta. Un umbral mal puesto hace que el bot calle de más o hable sobre ruido.
- **Analogía:** un colador: muy cerrado no deja pasar nada útil; muy abierto deja pasar piedras.
- **Ejemplo:** `distancias = [0.2, 0.5, 0.9]` con umbral `0.6` deja pasar las dos primeras.
- **Profundiza:** <https://docs.trychroma.com/>

**5. Typing `Protocol`.**
- **Idea:** describe «cualquier objeto que tenga estos métodos», sin heredar de nada. Sirve para que tu código acepte un almacén real o uno falso de prueba.
- **Analogía:** un enchufe: no importa la marca del aparato, solo que tenga la clavija correcta.
- **Ejemplo:**
```python
from typing import Protocol
class Saluda(Protocol):
    def hola(self) -> str: ...
```
- **Profundiza:** <https://docs.python.org/3/library/typing.html#typing.Protocol>

## Calentamiento (fuera del proyecto)

En cmd, con el entorno activado. Dos veces cada comando; compara las salidas:
```
python -c "print(hash('hola'))"
python -c "import zlib; print(zlib.crc32(b'hola'))"
```
Resultado esperado: el primero imprime **un número distinto cada vez**; el segundo imprime **siempre el mismo**. Ahora entiendes por qué `LexicalEmbedder` usa `crc32` y por qué el anti-caso `cofounder-agi` recupera ruido. Después prueba cómo cambia la huella:
```
python -c "import hashlib; print(hashlib.sha256(b'hola').hexdigest()); print(hashlib.sha256(b'hola.').hexdigest())"
```
Debes ver dos cadenas de 64 caracteres totalmente distintas por un solo punto de diferencia.

## Paso a paso

### Paso 0 — Prepara tu terreno
**Haz esto:** sigue los pasos 1 a 4 de la sección 7 del contrato: sincroniza `main`, comprueba que existe `src\rag\store.py`, crea la rama `issue-157-ingesta-evaluacion-rag`, crea el entorno, instala el proyecto y corre `pytest tests -q`. Anota N.
**Por qué:** sin una línea base verde no sabrás si algo que rompiste es tuyo o ya venía roto.
**Debes ver:** `N passed`, sin fallos.
**Si falla:** si `dir` no encuentra `store.py`, no empieces y comenta en el Issue con la salida pegada como texto. Si `python --version` no dice 3.11, usa `py -3.11`.
**Punto de control:** ¿puedes decir en una frase qué hacen `load_documents` y `ChromaStore.ingest`, sin mirar?

### Paso 1 — La huella: pruebas I1, I2 e I3
**Haz esto:** crea `tests\test_rag_ingest.py` con **solo** I1, I2 e I3. Córrelo: debe fallar con `ModuleNotFoundError: No module named 'rag.ingest'`. Crea `src\rag\ingest.py` con `IngestReport` y `corpus_fingerprint` (contrato 5.1). Vuelve a correr hasta ver `3 passed`.
**Por qué:** la huella es la pieza que decide si dos índices son «el mismo». Si depende del orden o ignora un campo, te mentirá sin avisar.
**Debes ver:** primero el rojo por módulo ausente; luego `3 passed`. Si pasa I1 pero falla I3, estás dejando fuera el campo `sensitive`.
**Si falla:** I1 rojo con dos huellas distintas = dependes del orden. Revisa la escalera de pistas (Paso 1).
**Punto de control:** ¿qué campos de un `Document` entran a la huella y cuál no? ¿Por qué `label` no?

### Paso 2 — Ingerir y reportar: pruebas I4 e I5
**Haz esto:** escribe I4 e I5 en el mismo archivo; mira que fallen porque falta `ingest_corpus`. Impleméntalo. En I5 usa una carpeta temporal (`tmp_path`) para que el índice esté **en disco** y lo abran dos almacenes distintos.
**Por qué:** I4 te amarra el informe a los datos reales; I5 prueba lo que importa en producción: reiniciar y volver a ingerir no debe duplicar documentos.
**Debes ver:** `5 passed`. Si I5 falla con `count` distinto de `documents`, estás agregando en vez de reconstruir.
**Si falla:** `Expected a name containing 3-512 characters` = el nombre de la colección es muy corto. Usa nombres como `test-i4`.
**Punto de control:** ¿qué hace `ChromaStore.ingest` con una colección que ya existía? ¿Dónde lo viste en el código?

### Paso 3 — La CLI: pruebas I6, I7 e I8
**Haz esto:** escribe I6, I7 e I8; luego `main(argv)` y el bloque `if __name__ == "__main__":`. Para leer lo que imprime tu CLI en las pruebas, usa la fixture `capsys` de pytest. Corre `pytest tests\test_rag_ingest.py -q` → `8 passed`.
**Por qué:** una CLI se prueba como una función: le pasas la lista de argumentos y miras el código de salida y lo que escribió.
**Debes ver:** `8 passed`. Luego, a mano: `python -m rag.ingest --chroma-path %TEMP%\chroma_prueba` dos veces, la misma línea.
**Si falla:** si I6 falla porque stdout trae dos líneas, tienes un `print` de depuración. Si I8 no lanza `SystemExit`, `argparse` no está recibiendo `choices`.
**Punto de control:** ¿por qué el mensaje de error va a `stderr` y no a `stdout`?

### Paso 4 — Evaluar la recuperación: pruebas E1, E2, E3 y E4
**Haz esto:** crea `tests\test_rag_evaluate.py` con un buscador falso (una clase de 4 líneas con un diccionario) y las pruebas E1–E4. Rojo por `rag.evaluate` ausente. Luego `src\rag\evaluate.py`: los modelos, `Searcher` y `evaluate_retrieval`.
**Por qué:** probar con un buscador falso te deja controlar exactamente qué «encuentra» y descubrir bugs sin depender de Chroma.
**Debes ver:** `pytest tests\test_rag_evaluate.py -q` → `4 passed` (solo has escrito E1–E4 hasta aquí).
**Si falla:** el caso fuera de alcance (E3) es el que más se escapa: «pasa» significa **cero resultados**, no «no encontré el esperado».
**Punto de control:** ¿qué significa `expected_doc_id=None` y por qué hace falta ese caso para detectar un RAG que contesta ruido?

### Paso 5 — El umbral y la calibración: pruebas E5, E6, E7 y E8
**Haz esto:** escribe E5–E8 y luego `suggest_max_distance` y `calibrate`. E5–E7 son aritmética pura; E8 usa tu buscador falso con distancias que tú controlas.
**Por qué:** separar «el peor acierto» del «mejor ruido» es el corazón de calibrar: si se cruzan, no existe umbral que sirva con ese embedder.
**Debes ver:** `pytest tests\test_rag_evaluate.py -q` → `8 passed` (o `8 passed, 4 deselected` si usas el `-k "test_e1_ or ... or test_e8_"` del contrato con las 12 ya escritas).
**Si falla:** en E8, revisa que para un caso con respuesta esperada uses la distancia **del documento esperado**, no la del primer resultado.
**Punto de control:** si el peor acierto está a 0.9 y el mejor ruido a 0.7, ¿qué devuelve `suggest_max_distance` y qué significa eso para el sistema?

### Paso 6 — Tu archivo de oro: pruebas E9 y E10
**Haz esto:** escribe E9 y E10. Crea `data\hola_mujer\rag_golden.json` (contrato 5.3) con al menos 10 preguntas **inventadas por ti**, como las escribiría una clienta. Mira `servicios.json` para sacar los `service_id` y los documentos del negocio (`NEG-ADDRESS`, `NEG-OPENING_HOURS`).
**Por qué:** los casos de oro son lo más valioso de la evaluación. Si los copias de un compañero o de una IA, no sabrás lo que mides.
**Debes ver:** E9 y E10 en verde. E11 y E12 todavía pueden fallar: eso es el siguiente paso.
**Si falla:** E9 te dice qué id esperado no existe; E10, que hay algo parecido a un teléfono o un correo en el archivo.
**Punto de control:** ¿cuáles son tus 2 preguntas fuera de alcance y por qué un negocio de salud y estética no debería poder contestarlas?

### Paso 7 — Calibración real y a iterar: pruebas E11 y E12
**Haz esto:** escribe E11 y E12 (usan el corpus real, el embedder léxico y **tu** archivo). Córrelas. Si fallan, lee qué preguntas no encuentran su documento y reformúlalas; no toques el código para que pasen.
**Por qué:** el embedder léxico solo compara palabras. Aprender a escribir preguntas que lo prueben bien (y ver cuáles lo confunden) es la lección de la sesión.
**Debes ver:** `pytest tests\test_rag_evaluate.py -q` → `12 passed`.
**Si falla:** `unreachable` no vacío = alguna pregunta ni siquiera trae su documento entre los 10 primeros; cambia la pregunta o revisa el id. `suggested` en `None` = el ruido y los aciertos se cruzan.
**Punto de control:** ¿qué preguntas tuyas fueron las más difíciles para el embedder léxico y qué tenían en común?

### Paso 8 — La evidencia y las 4 puertas
**Haz esto:** corre los dos comandos de una línea del paso 10 de la sección 7 del contrato y pega sus salidas (copiadas como texto) en el PR. Luego corre las 4 puertas con el comando exacto del contrato (paso 11) y la verificación de independencia de orden (paso 12).
**Por qué:** esa evidencia le da al monitor lo que necesita para calibrar con el embedder real, y a ti, el número con el que respondes la pregunta 2.
**Debes ver:** `All checks passed!` · `Success: no issues found...` · `N+20 passed` · `No issues identified.`
**Si falla:** si `mypy` marca el parámetro `searcher`, revisa que tu `Protocol` tenga la misma firma de `search` que `ChromaStore`.
**Punto de control:** ¿el umbral actual (0.6) es muy estricto, muy laxo o está bien para el embedder léxico? Respóndelo con tus números, no con una intuición.

### Paso 9 — Commits y PR
**Haz esto:** haz los commits del paso 13 del contrato (uno por cambio lógico, con `#157`), sube la rama y abre el PR con `Closes #157`, la plantilla completa, la evidencia y las 3 respuestas de la sección 11.
**Por qué:** un historial chico y ordenado se revisa en minutos; un solo commit gigante se revisa mal.
**Debes ver:** el PR en verde en `guardian-tbd / reglas-tbd` y `CI estricto / calidad`, y el comentario del robot sin «archivos fuera de contrato».
**Si falla:** si el robot dice que tocaste un archivo fuera de la sección 4, revierte ese archivo (`git restore`) antes de seguir.
**Punto de control:** ¿puedes explicar en voz alta, sin mirar, las 3 preguntas de la sección 11?

## Escalera de pistas (úsala solo cuando estés trabado, de arriba abajo)

**Paso 1 (huella que depende del orden o del proceso):**
- *Pista 1:* si dos listas con los mismos documentos en distinto orden dan huellas distintas, algo en tu cálculo depende del orden de la lista.
- *Pista 2:* busca en la documentación de Python `sorted` con el argumento `key`, y `hashlib.sha256`; recuerda que `sha256` recibe **bytes**, no texto.
- *Pista 3 (en palabras):* ordena los documentos por su identificador, convierte cada uno en una sola línea de texto con sus cinco campos separados por un carácter que no pueda aparecer en el texto, une las líneas y calcula la huella de ese bloque.

**Paso 2 (I5, duplicados en disco):**
- *Pista 1:* si ingerir dos veces deja más documentos que una vez, estás agregando en vez de reemplazar.
- *Pista 2:* revisa `ChromaStore.ingest` en `src/rag/store.py`: ya decide qué hacer con una colección existente. ¿Qué necesita tu función para aprovecharlo?
- *Pista 3 (en palabras):* tu función no debe tocar Chroma directamente; solo carga los documentos, se los pasa al almacén y arma el informe con lo que cargó.

**Paso 3 (la CLI):**
- *Pista 1:* `argparse` ya sabe validar opciones y terminar con código 2 si el valor no es válido.
- *Pista 2:* busca `choices` en la documentación de `argparse.ArgumentParser.add_argument`, y `print(..., file=sys.stderr)`.
- *Pista 3 (en palabras):* valida la carpeta antes de crear nada; si no existe, avisa por `stderr` y devuelve 1; si existe, arma el almacén, ingiere e imprime solo el JSON del informe.

**Paso 5 (calibrate):**
- *Pista 1:* son dos listas: las distancias de los aciertos y las del ruido; el resto es aritmética.
- *Pista 2:* en cada caso con respuesta esperada hay que buscar **ese documento** entre los resultados (no solo mirar el primero).
- *Pista 3 (en palabras):* recorre los casos; si el esperado es `None`, guarda la distancia del resultado más cercano; si no, guarda la distancia del documento esperado, o anota la pregunta como inalcanzable si no aparece.

**Paso 7 (E11/E12 fallan):**
- *Pista 1:* el embedder léxico compara palabras, no significados: «cuánto sale» y «precio» no se parecen.
- *Pista 2:* en E12 el mensaje de la aserción lista las preguntas que fallaron; mira qué palabras de la pregunta aparecen en el texto de su documento (`load_documents`).
- *Pista 3 (en palabras):* reformula la pregunta usando alguna palabra del nombre del servicio; si el ruido queda demasiado cerca, hazlo menos parecido a cualquier servicio del catálogo.

## Errores típicos de esta asignación

| Síntoma (lo que ves) | Causa probable | Qué hacer |
|---|---|---|
| `Expected a name containing 3-512 characters` | Nombre de colección demasiado corto en una prueba | Usa nombres como `test-i4`, de 3 o más caracteres |
| Una prueba pasa sola pero falla con las demás | Dos pruebas usan el mismo nombre de colección y Chroma comparte el almacén en memoria dentro del proceso | Un nombre distinto en cada prueba |
| La huella cambia entre dos corridas | Usaste `hash()` de Python, un `set` o algo con la fecha | `hashlib.sha256` sobre una lista **ordenada** |
| `ModuleNotFoundError: No module named 'rag.ingest'` aunque creaste el archivo | El archivo quedó en otra carpeta o con otro nombre | Debe ser `src\rag\ingest.py` (revisa con `dir src\rag`) |
| `stdout` trae más de una línea en I6 | Quedó un `print` de depuración | Quita los `print`; solo se imprime el JSON del informe |
| `FileNotFoundError: ... rag_golden.json` en E9–E12 | Todavía no creaste el archivo | Es esperado hasta el Paso 6 |
| `AssertionError` en E12 listando preguntas | Esas preguntas no encuentran su documento con el embedder léxico | Reformúlalas (Paso 7), no toques el código |
| `python -c "..."` falla con comillas | cmd entiende las comillas dobles por fuera | Comillas dobles por fuera y simples por dentro, como en el contrato |
| `%TEMP%` aparece literal | Estás en PowerShell | Usa **cmd** (Símbolo del sistema) |

## Autoevaluación antes del PR

- [ ] Cada prueba del contrato la escribí yo, la vi fallar y la vi pasar.
- [ ] Mis preguntas de oro las inventé yo; no copié las de nadie ni las de una IA.
- [ ] Puedo explicar en voz alta, sin mirar, las 3 preguntas de comprensión del contrato.
- [ ] Mi `git diff --name-only main` coincide con la sección 4 del contrato (5 archivos).
- [ ] Pegué en el PR la evidencia del paso 10 y mi conclusión sobre el umbral actual.
- [ ] Anoté en el PR cuántas interacciones usé con mi IA y a quién consulté.

## Prompts sugeridos para tu IA (pequeños y verificables)

**Buenos:**
1. «Explícame en 5 líneas qué es un hash y por qué `hash("a")` cambia entre ejecuciones de Python pero `hashlib.sha256` no. Usa un ejemplo con números, no con mi proyecto.»
2. «Pego este error de pytest como texto: [error]. Explícame qué significa y qué debería mirar, sin escribirme la solución.»
3. «¿Qué significa que un test use `capsys`? Dame un ejemplo mínimo con una función que imprime "hola", fuera de mi proyecto.»
4. «Pego la salida de `git diff --name-only main`. Compárala con esta lista de 5 archivos y dime si sobra o falta alguno.»
5. «Tengo estas dos listas de distancias [..] y [..]. ¿En qué casos no existe un umbral que las separe? Explícalo con palabras.»

**Prohibidos:**
- «Escribe `corpus_fingerprint` y `calibrate` por mí.» → no aprendes y el PR no es tuyo (sección 10 del contrato).
- «Inventa 12 preguntas de oro para el RAG de Hola Mujer.» → inventarlas como una clienta es parte de lo que se evalúa.
