# [S07 D2] Paso a paso guiado — Herramienta `consultar_servicio`

> **Para quién:** Allan (WhoAllan), que ya cerró la memoria persistente con LangGraph y ahora conoce el estado y el checkpointer, pero **no** las herramientas de LangChain. Este archivo te acompaña **mientras trabajas**; el contrato (`S07_D2.md`) dice **qué** debe quedar. Aquí aprendes **cómo abordarlo sin perderte**.
>
> **Reglas del juego:** no hay código de la solución aquí (si lo hubiera, no aprenderías). Hay explicación, pistas y puntos de control. Una sesión de práctica dura ~3 h; los tiempos son una guía, no una exigencia.

## Mapa de la sesión

| Bloque | Tiempo | Resultado que puedes comprobar |
|---|---|---|
| Calentamiento | 15 min | Una herramienta de juguete responde con `.invoke()` |
| Pasos 0–3 (T1–T3, el catálogo y la duración) | 60 min | La herramienta devuelve datos reales y oculta la duración |
| Pasos 4–6 (T4–T6, errores y bordes) | 50 min | Los errores vuelven como texto tipado, sin excepciones crudas |
| Pasos 7–9 (T7–T9, `ToolNode` y metadatos) | 40 min | La herramienta funciona dentro de un grafo |
| Cierre y PR | 25 min | PR abierto con `Closes #184` |

## Mini-conceptos (léelos antes del Paso 1)

**1. Herramienta (`StructuredTool`).** Es una función con nombre, descripción y un esquema de argumentos, que un modelo puede pedir que se ejecute. Analogía: un formulario con casillas fijas en la ventanilla. Ejemplo fuera del proyecto: `StructuredTool.from_function(func=suma, name="suma", args_schema=Suma)`. Profundiza: https://python.langchain.com/docs/concepts/tools/ (verifícalo en esa URL).

**2. `args_schema` con Pydantic v2.** El esquema valida los argumentos **antes** de que corra tu función; con `extra="forbid"` un argumento desconocido es error. Analogía: el guardia que revisa el DNI antes de dejarte pasar. Ejemplo: `class Suma(BaseModel): a: int = Field(ge=0)`.

**3. Errores de herramienta.** `ToolException` es la excepción que una herramienta lanza para decir «esto salió mal, y el modelo puede leerlo». Con `handle_tool_error` el error se convierte en texto en vez de romper. `handle_validation_error` hace lo mismo con los errores del esquema. Analogía: la ventanilla que dice «falta un sello» en vez de cerrar el banco. Ejemplo: `StructuredTool.from_function(..., handle_tool_error=True)`.

**4. `ToolNode`.** Es un nodo de LangGraph que lee las llamadas a herramientas del último `AIMessage`, las ejecuta y devuelve `ToolMessage`s (con `status` de éxito o error). Analogía: el cajero que atiende los pedidos que el mesero anotó. Ejemplo: `graph.add_node("tools", ToolNode([mi_tool]))`. Profundiza: https://langchain-ai.github.io/langgraph/ (busca «ToolNode»).

## Calentamiento (fuera del proyecto)

En un archivo suelto (bórralo después), crea una herramienta de juguete `saludar(nombre: str)` con un `args_schema` que exija entre 2 y 10 letras. Llama `.invoke({"nombre": "Ana"})` y luego `.invoke({"nombre": "A"})`. **Esperado:** la primera responde; la segunda lanza un error de validación (eso es lo que, hoy, tendrás que convertir en texto).

## Paso a paso

### Paso 0 — Prepara tu terreno
**Haz esto:** crea la rama `issue-184-consultar-servicio` desde `main` actualizado. Corre `pytest tests -q` y anota el total. Lee `tools_estrictas.py` y `src/tools/agendar.py` (sección 2 del contrato).
**Por qué:** necesitas el total de antes para comprobar que subes exactamente en 9, y ver cómo el repo ya arma una herramienta.
**Debes ver:** todas las pruebas en verde y un número total.
**Si falla:** si `main` no pasa, avisa en el Issue con el error pegado; no lo arregles tú.
**Punto de control:** ¿puedo decir en una frase en qué se parece mi herramienta a `agendar_cita` y en qué no (N1 contra N2)?

### Paso 1 — Escribe T1 y T2 (datos del catálogo y duración oculta)
**Haz esto:** crea `tests/test_consultar_tool.py`. Escribe `test_t1_...` y `test_t2_...` según la sección 6, cargando el catálogo real. Córrelas: deben fallar con `ModuleNotFoundError: No module named 'tools.consultar'`.
**Por qué:** una prueba que nunca vio rojo no demuestra nada.
**Debes ver:** el error de colección exacto de la sección 6.
**Si falla:** si el error es otro (por ejemplo, un import mal escrito), corrígelo hasta ver el rojo correcto.
**Punto de control:** ¿mi T2 falla por la razón que esperaba, o por un descuido mío?

### Paso 2 — Implementa el catálogo ampliado y la herramienta (T1, T2)
**Haz esto:** agrega los campos opcionales de la sección 5.1 a `Service`; crea `src/tools/consultar.py` con `ConsultarInput`, `ServiceInfo` y `make_consultar_tool`, lo mínimo para T1 y T2.
**Por qué:** el catálogo hoy descarta precio y duración (ignora campos extra); sin ampliarlo no hay qué consultar.
**Debes ver:** T1 y T2 en verde, y las 331 pruebas anteriores intactas.
**Si falla:** si se rompe una prueba antigua, revisa que tus campos nuevos tengan valor por defecto.
**Punto de control:** ¿mi T2 se mantendría verde si alguien cambiara el catálogo para poner 45 minutos pero sin verificar?

### Paso 3 — T3: la duración verificada sí se cita
**Haz esto:** escribe T3 con un catálogo propio de un solo servicio inventado; córrela en rojo (falla por el valor, no por import) y haz que pase.
**Por qué:** el caso contrario protege la regla de que ocultar no es borrar el dato.
**Debes ver:** T3 en verde sin tocar el catálogo real.
**Si falla:** revisa que construyas el `Service` con los campos nuevos y que tu condición use `duracion_verificada`.
**Punto de control:** ¿la decisión de ocultar está en un solo lugar del código?

### Paso 4 — T4: servicio inexistente
**Haz esto:** escribe T4, córrela en rojo, y haz que un id con buen formato que el catálogo no tiene produzca un texto que empiece con `service_unknown`, usando `ServiceUnknown` (hereda de `ToolException`) y la opción de la herramienta para manejar ese error.
**Por qué:** el modelo debe poder leer el error y reaccionar; una excepción cruda tumba el grafo.
**Debes ver:** T4 en verde.
**Si falla:** si ves la excepción propagarse, falta indicarle a la herramienta cómo manejarla; si el texto no empieza con el código, mira qué recibe tu manejador.
**Punto de control:** ¿qué verá el modelo exactamente cuando pida un servicio que no existe?

### Paso 5 — T5: entrada inválida
**Haz esto:** escribe T5 con los cuatro casos y haz que todos devuelvan texto que empiece con `invalid_input`.
**Por qué:** el esquema ya rechaza la basura, pero por defecto lanza `ValidationError`; hay que convertirlo en un mensaje legible.
**Debes ver:** T5 en verde.
**Si falla:** el argumento extra (`x`) solo falla si el esquema prohíbe extras; revisa la configuración del modelo Pydantic.
**Punto de control:** ¿cuál de mis cuatro casos es el menos obvio, y por qué lo cubrí?

### Paso 6 — T6: bordes
**Haz esto:** escribe T6: id con espacios alrededor, `ConsultarInput` de 40 y de 41 caracteres. Haz que pase.
**Por qué:** los bordes son donde se rompen los esquemas.
**Debes ver:** T6 en verde.
**Si falla:** revisa la opción de Pydantic que quita espacios y los límites de longitud.
**Punto de control:** ¿qué pasaría con 40 caracteres si el patrón no permitiera guiones?

### Paso 7 — T7: la herramienta dentro de un `ToolNode` (éxito)
**Haz esto:** arma un grafo mínimo (estado de mensajes, un nodo `ToolNode` desde `START`) y alimenta un `AIMessage` con una llamada inventada. Escribe T7 y córrela.
**Por qué:** así compruebas que la herramienta funciona como la usará el agente, sin necesitar un modelo.
**Debes ver:** un `ToolMessage` con `status == "success"`.
**Si falla:** si ves `ValueError` sobre falta de configuración, el `ToolNode` está corriendo fuera de un grafo compilado; llámalo desde el grafo.
**Punto de control:** ¿de dónde sale el `id` de la llamada y para qué sirve en el `ToolMessage`?

### Paso 8 — T8: `ToolNode`, error
**Haz esto:** escribe T8 reutilizando tu ayudante de grafo, con el id inexistente.
**Por qué:** debe verse la diferencia entre éxito y error en el `status`.
**Debes ver:** `status == "error"` y contenido que empieza con `service_unknown`.
**Si falla:** si el status sale como éxito, mira cómo trata `ToolException` tu herramienta.
**Punto de control:** ¿qué hará el modelo al ver un `ToolMessage` de error?

### Paso 9 — T9: metadatos y puertas
**Haz esto:** escribe T9 (nombre, `PERMISSION_LEVEL`, `metadata`). Luego corre las 4 puertas, el total (debe subir en 9) y cada ID aislado con `-k`.
**Por qué:** esos metadatos son lo que el arnés de seguridad leerá después (ADR-009).
**Debes ver:** todo verde y `git diff --name-only main` igual a la sección 4.
**Si falla:** si `ruff` o `mypy` se quejan, corrígelos sin cambiar las pruebas.
**Punto de control:** ¿puedo explicar sin mirar las 3 preguntas de comprensión?

## Escalera de pistas (úsala solo cuando estés trabado, de arriba abajo)

**Errores como texto (Pasos 4–5).**
- Pista 1: una herramienta puede avisar de un fallo sin romper el grafo si el framework convierte la excepción en un mensaje.
- Pista 2: busca `handle_tool_error` y `handle_validation_error` en la doc de herramientas de LangChain (https://python.langchain.com/docs/concepts/tools/, verifícalo allí) y en las firmas de `StructuredTool.from_function`.
- Pista 3: en palabras: un manejador para fallos de tu función (recibe la excepción, devuelve texto con el prefijo `service_unknown`) y otro para fallos de validación (recibe el error de Pydantic, devuelve texto con `invalid_input`); ambos se pasan al crear la herramienta.

**`ToolNode` en una prueba (Pasos 7–8).**
- Pista 1: `ToolNode` necesita correr dentro de un grafo, no suelto.
- Pista 2: `StateGraph`, `MessagesState`, `START` y `ToolNode` en https://langchain-ai.github.io/langgraph/.
- Pista 3: en palabras: un grafo con un solo nodo de herramientas conectado al inicio; lo invocas con un `AIMessage` que lleva la lista `tool_calls`; el último mensaje del resultado es el `ToolMessage`.

**Duración oculta (Pasos 2–3).**
- Pista 1: el catálogo ignora los campos que `Service` no declara.
- Pista 2: Pydantic v2, campos con valor por defecto.
- Pista 3: en palabras: añade los campos con `None` o `False` por defecto, y al armar la salida elige el valor de duración según la bandera de verificación.

## Errores típicos de esta asignación

| Síntoma (lo que ves) | Causa probable | Qué hacer |
|---|---|---|
| `ModuleNotFoundError: tools.consultar` tras implementar | Archivo en la carpeta equivocada | Debe estar en `src/tools/consultar.py` |
| `ValidationError` se escapa de `.invoke` | Falta el manejador de validación | Revisa la pista de errores como texto |
| `ValueError` al usar `ToolNode` suelto | No está dentro de un grafo compilado | Usa el grafo mínimo del Paso 7 |
| `duracion_min` sale 60 | Se devuelve el valor sin mirar la verificación | Condiciona por `duracion_verificada` |
| Pruebas antiguas fallan tras tocar `catalog.py` | Campos nuevos sin valor por defecto | Dale un valor por defecto a cada uno |

## Autoevaluación antes del PR

- [ ] Cada prueba del contrato la escribí yo, la vi fallar y la vi pasar.
- [ ] Puedo explicar en voz alta, sin mirar, las 3 preguntas de comprensión del contrato.
- [ ] Mi `git diff --name-only main` coincide con la sección 4 del contrato.
- [ ] Anoté en el PR cuántas interacciones usé con mi IA y a quién consulté.

## Prompts sugeridos para tu IA (pequeños y verificables)

1. «Explícame con un ejemplo que no sea de mi repo qué hace `ToolException` y cuándo se usa `handle_tool_error`.»
2. «Mi prueba dice `ModuleNotFoundError` y aún no creé el archivo; ¿es el rojo correcto? (pego solo el error)»
3. «Revisa esta lista de casos inválidos para un id de servicio: ¿qué borde me falta?» (pego solo la lista)
4. «Explícame qué devuelve un `ToolNode` cuando la herramienta falla y qué campo del mensaje lo indica.»

**Prohibidos:** «Escribe `consultar.py` completo» (pierdes lo que la asignación enseña) y «Dame las pruebas T1–T9 hechas» (las pruebas son tu evidencia de comprensión).
