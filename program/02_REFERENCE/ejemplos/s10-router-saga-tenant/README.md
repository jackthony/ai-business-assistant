# Ejemplo — Router, saga y aislamiento por tenant (S10: Issues #15, #19, #20)

**Qué aprendes:** tres patrones de arquitectura (ver `../patrones-arquitectura.md`) en su versión mínima:
1. **Router** (#19): reglas rápidas primero; el LLM solo para lo ambiguo; **seguridad siempre gana**; cada decisión deja traza.
2. **Saga con compensación** (#15): agendar + cobrar sin dejar nada a medias; si un paso falla se deshace lo hecho **en orden inverso**.
3. **Aislamiento por tenant** (#20): el nombre del recurso (colección RAG) sale de una lista cerrada, nunca del mensaje.
**Qué NO hace:** no lee comprobantes (OCR es tu #15), no tiene supervisor LLM real (el fallback se inyecta), no carga `configs/{tenant}`, no toca Chroma.

| Archivo | Rol |
|---|---|
| `router.py` | `clasificar_rapido` + `construir_router(fallback_llm)` (LangGraph con aristas condicionales) |
| `saga_agendar_pago.py` | `Paso(hacer, deshacer)` + `ejecutar_saga` con log |
| `aislamiento_tenant.py` | `resolver_tenant` y `coleccion_rag` |
| `test_*.py` | 13 ruteos (incluye el de seguridad que gana a "precio"), compensación en orden inverso, 7 tenants inválidos |

```bash
pip install "langgraph>=1,<2" pytest
pytest program/02_REFERENCE/ejemplos/s10-router-saga-tenant -q     # debe dar 29 passed
```

## Qué mirar en cada bloque

- **Router:** el test `test_respuesta_basura_del_llm_cae_a_humano…` — si el LLM devuelve algo que no es una ruta, **no** se rutea a donde diga el modelo. El Issue pide ≥13/15 mensajes bien ruteados: arma tu tabla de 15 con casos tuyos (incluye ambiguos y de riesgo) y registra la traza `ruta`/`via`.
- **Saga:** la compensación debe poder correr dos veces sin daño (idempotente). Con una base real, cada `deshacer` es una operación segura de repetir.
- **Tenant:** un tenant desconocido es **error**, no "usa hola_mujer por defecto". El mensaje de error no repite el valor recibido.

## Contraste con otros frameworks (clase de 30 min de #19)

| Concepto | `openai-agents-python` | LangGraph (nuestro) |
|---|---|---|
| Ruteo / handoff | `routing.py`: un agente "toma el control" | Arista condicional hacia el nodo del agente elegido |
| Agente como herramienta | `agents_as_tools.py` | Subgrafo invocado desde un nodo |
| Flujo en pasos | `deterministic.py` | Aristas fijas entre nodos |

Se compara el *patrón*; seguimos en LangGraph por ADR-010.

## Errores comunes

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| Un mensaje con dolor y precio va a "info" | Revisaste intenciones antes que seguridad | Seguridad **primero** |
| Se queda un horario bloqueado tras un pago fallido | Faltó la compensación | Un `deshacer` por cada paso con efecto |
| Una clienta ve datos de otro negocio | Armaste el nombre de colección con el texto del usuario | `resolver_tenant` contra lista cerrada |

## Preguntas de comprensión (responde en tu PR)

1. ¿Por qué las reglas van antes que el LLM en el router? ¿Qué ganas en costo, latencia y auditoría?
2. En la saga, ¿por qué se deshace en **orden inverso**?
3. ¿Qué riesgo concreto evita `resolver_tenant` y por qué no se muestra el valor inválido en el error?

Fuentes leídas: `openai/openai-agents-python` (MIT) `routing.py` y `deterministic.py`; patrones *Saga* y *Tenant isolation* de `microservices.io`; ADR-009/ADR-010.
