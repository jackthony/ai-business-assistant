# Ejemplo — Grafo mínimo con memoria por teléfono (Issues #04–#06, S5)

**Qué aprendes:** los 4 conceptos que sostienen todo el agente: **estado** (`TypedDict`), **reducer** (`operator.add`: añadir en vez de pisar), **checkpointer** (`SqliteSaver`) y **`thread_id`** (un hilo por teléfono). La memoria sobrevive a un reinicio porque vive en un archivo SQLite.
**Qué NO hace:** no usa LLM, no tiene prompt de Hola Mujer, no maneja varios nodos ni herramientas. El nodo solo hace eco, para que veas la mecánica sin ruido.

## Archivos

| Archivo | Rol |
|---|---|
| `memoria_minima.py` | `Estado`, nodo `responder`, `construir_grafo(checkpointer)`, `config_de(telefono)` |
| `test_memoria_minima.py` | Sobrevive a un reinicio (abre el mismo `.db` dos veces) y aísla hilos por teléfono |

## Antes de correrlo (una sola vez, en tu venv)

```bash
pip install "langgraph>=1,<2" langgraph-checkpoint-sqlite
pytest program/02_REFERENCE/ejemplos/langgraph-memoria -q     # debe dar 2 passed
```

> Verificado el 2026-10-08 con Python 3.11.16, `langgraph 1.2.14`, `langgraph-checkpoint-sqlite 3.1.1`, `pytest 9.1.1` (2 passed; `ruff`, `bandit` limpios). Ojo: `stack-versiones.md` aún acota `langgraph<1` (con ese tope pip instala la serie 0.6, no la 1.x que se verificó aquí); la decisión de subir el tope es del monitor. Si con tu versión no pasan, no los "arregles" con tu IA a ciegas: avisa al monitor, puede ser que la API cambió y hay que actualizar el ejemplo y `stack-versiones.md`.

## Seguridad (obligatoria, no opcional)

El checkpoint se guarda serializado. Si alguien modifica el `.db`, una deserialización laxa podría ejecutar código. La doc de `langgraph-checkpoint-sqlite` pide fijar `LANGGRAPH_STRICT_MSGPACK=true` (o pasar una lista explícita `allowed_msgpack_modules`). El test lo activa; en tu servicio ponlo en el entorno/`.env.example`. Además: **el `.db` de memoria nunca va al repo** (`.gitignore`) porque contendrá conversaciones de clientas.

## Paso a paso sugerido

1. Corre los tests y léelos: son la especificación de la memoria.
2. Dibuja en papel (para tu informe FPE): `START → responder → END`, y dónde se guarda el checkpoint tras cada nodo.
3. Cambia el nodo `eco` por tu llamada al modelo (S5 D1) **sin tocar** el estado ni el `thread_id`; en tu Issue el prompt va en `configs/hola_mujer/prompt_v1.md`, separado en identidad, tono y límites.
4. Para producción real (S14) el `SqliteSaver` se cambia por un checkpointer de Postgres (ADR-005): por eso `construir_grafo` recibe el checkpointer por parámetro y no lo crea.

## Errores comunes

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| La conversación "olvida" lo anterior | Cambiaste el `thread_id` entre mensajes, o el estado no tiene reducer | Usa siempre el teléfono como `thread_id` y `Annotated[list, operator.add]` |
| `database is locked` | Dos procesos escribiendo el mismo `.db` | En local usa un solo proceso; en prod se pasa a Postgres |
| `mypy` marca `add_node` con `call-overload` | Limitación de tipos de `langgraph` 1.x con `mypy` 2.x (falla incluso con un `TypedDict` simple) | Silencia **solo esa línea** con `# type: ignore[call-overload]` y un comentario, como en `memoria_minima.py`; no apagues mypy |
| Dos clientas ven mensajes mezclados | `thread_id` fijo o vacío | `thread_id = wa_id` de cada `InboundEvent` |

## Preguntas de comprensión (responde en tu PR)

1. ¿Qué pasaría con el historial si quitas el reducer `operator.add`?
2. ¿Por qué el `thread_id` es el teléfono y no un id aleatorio por mensaje?
3. ¿Por qué `construir_grafo` recibe el checkpointer en vez de crearlo adentro?
4. ¿Qué riesgo cubre `LANGGRAPH_STRICT_MSGPACK` y por qué el `.db` no se sube al repo?

Fuentes leídas: `langchain-ai/langgraph` (MIT) · `libs/checkpoint-sqlite/README.md` (sección *Security*) y documentación oficial de persistencia de LangGraph.
