# Ejemplo — Tools estrictas y citas sin duplicados (S7: Issues #10–#12)

**Qué aprendes:** (1) una tool que **valida sus argumentos** con Pydantic V2 y devuelve **errores tipados** en vez de reventar o inventar; (2) reservar horarios **sin colisiones** y **sin duplicar** aunque llegue el mismo `request_id` dos veces (patrón *idempotent consumer*).
**Qué NO hace:** no usa el RAG ni el Excel real (el catálogo es falso), no habla con Google Calendar, no decide el texto de la respuesta, no conecta el modelo local. Eso es tu Issue.

| Archivo | Rol |
|---|---|
| `tools_estrictas.py` | `consultar_servicio`: `ConsultaServicio` (con `extra="forbid"`), `ServicioOut`, `ErrorTool` |
| `reserva_idempotente.py` | `Agenda.proponer / reservar` con `request_id` |
| `test_*.py` | Válido / inválido / borde (los 3 tipos que pide el Issue #11) y 0 colisiones (#12) |

```bash
pip install "pydantic>=2,<3" pytest
pytest program/02_REFERENCE/ejemplos/s7-tools-y-citas -q     # debe dar 15 passed
```

## Paso a paso sugerido

1. Corre los tests y léelos: son la especificación de cada garantía.
2. **#11:** escribe primero tus tests de la tool con los tres tipos de caso; tu tool toma el precio **del RAG**, nunca de memoria del modelo (criterio "0 precios inventados").
3. **#12:** tus horarios libres salen de `02_CITAS`/Calendar (mock en CI). En producción la unicidad la garantiza la base (`UNIQUE(request_id)` y `UNIQUE(slot)`), no solo el `if` del código: con dos procesos a la vez el `if` solo no alcanza.
4. Antes de dar por buena la tool con el modelo local, pruébala con un `tool-calling` real; si el modelo no la invoca bien, ver el plan (`qwen2.5-coder`).

## Errores comunes

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| El modelo manda un argumento extra y "funciona" | El esquema ignora campos desconocidos | `extra="forbid"` + test |
| La tool lanza `ValidationError` al agente | Dejaste pasar la excepción | Captúrala y devuelve `ErrorTool` (el agente la explica) |
| Dos citas para la misma persona | Reintento sin `request_id` | Genera el `request_id` en el borde (webhook) y propágalo |
| 10 pruebas sin colisión pero fallan en producción | Probaste en serie | Añade una prueba concurrente cuando uses base real |

## Preguntas de comprensión (responde en tu PR)

1. ¿Por qué devolver `ErrorTool` en vez de lanzar la excepción? ¿Qué hace el agente con cada una?
2. ¿Qué diferencia hay entre **colisión** (dos personas, un horario) e **idempotencia** (la misma petición dos veces)?
3. ¿Por qué `request_id` reutilizado con otros datos es un error y no se acepta en silencio?

Fuentes leídas: documentación oficial de Pydantic V2 (*Strict mode*, `extra`), patrón *Idempotent consumer* de `microservices.io`, y ADR-009 (validación determinista primero).
