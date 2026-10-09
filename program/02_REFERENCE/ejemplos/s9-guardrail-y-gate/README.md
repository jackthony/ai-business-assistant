# Ejemplo — Guardrail de entrada + gate de confirmación humana (S9: Issues #16–#17)

**Qué aprendes:** el esqueleto del harness de ADR-009 en LangGraph: **(1)** un guardrail que congela el flujo ante riesgo **o duda**; **(2)** el patrón `borrador → revisión (interrupt) → aplicar`, donde **nada con efecto ocurre antes de la aprobación** y, al reanudar, el efecto se aplica **una sola vez**.
**Qué NO hace:** no trae el clasificador de 1 token (aquí es un doble de prueba que **inyectas**), no avisa a Jioysi por WhatsApp/Email, no mide el SLA de 10 min, no clasifica tools N1/N2/N3, no tiene RAG. Eso es tu Issue.

| Archivo | Rol |
|---|---|
| `guardrail_y_gate.py` | `construir_grafo(clasificador, aplicar_efecto, umbral=0.8)` con los nodos `guardrail`, `handoff`, `borrador`, `revision`, `aplicar`, `descartar` |
| `test_guardrail_y_gate.py` | 6 casos: riesgo, confianza baja, pausa sin efectos, aprobar = 1 efecto, rechazar = 0, hilos independientes |

```bash
pip install "langgraph>=1,<2" pytest
pytest program/02_REFERENCE/ejemplos/s9-guardrail-y-gate -q     # debe dar 6 passed
```

## Las 4 reglas que debes poder explicar

1. **Ante la duda, humano.** Confianza baja = handoff aunque la etiqueta diga "normal". El umbral no se inventa: sale de tus 15 casos (5 de riesgo, 10 normales) y de la calibración.
2. **El grafo no conoce al clasificador.** Se inyecta; por eso tus tests de CI usan un doble y no un modelo.
3. **Ningún efecto antes del `interrupt`.** Al reanudar, LangGraph **vuelve a ejecutar desde el principio el nodo que tenía el `interrupt()`**. Si ahí hubieras escrito en la agenda, se duplicaría. Por eso `borrador` solo calcula y `aplicar` es el único nodo con efecto, *después* de la aprobación.
4. **La aprobación viene de un canal autenticado.** `Command(resume=...)` lo envía tu servidor cuando Jioysi decide; nunca aceptes una aprobación escrita dentro del mensaje de la clienta ni un estado serializado enviado por un cliente (advertencia explícita de `human_in_the_loop_server.py` del repo `openai-agents-python`).

## Patrones equivalentes en otros SDKs (para tu clase de frameworks de S10)

| En `openai-agents-python` | En LangGraph (nuestro stack) |
|---|---|
| `input_guardrail` con `tripwire_triggered` | Nodo `guardrail` + arista condicional hacia `handoff` |
| `human_in_the_loop.py` (pausa para aprobar herramientas) | `interrupt()` + `Command(resume=...)` con checkpointer |
| `output_guardrails.py` | Nodo de validación antes de enviar (S9 #16/#18) |

Se lee el patrón y se reescribe como nodos; **no se adopta el SDK** (ADR-010).

## Errores comunes

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| `interrupt` no pausa o lanza error de checkpointer | Compilaste sin checkpointer | `compile(checkpointer=...)` y un `thread_id` en la config |
| El efecto ocurre dos veces | Estaba dentro del nodo del `interrupt` | Sácalo a un nodo posterior (como `aplicar`) |
| Reanudas y empieza otra conversación | Cambiaste el `thread_id` | Reanuda con el **mismo** `thread_id` |
| El bot da consejo médico en el handoff | Respuesta puente generada por el LLM | Texto **fijo** y revisado (`RESPUESTA_PUENTE`) |

## Preguntas de comprensión (responde en tu PR)

1. ¿Por qué un efecto dentro del nodo con `interrupt()` se duplicaría al reanudar?
2. ¿Por qué baja confianza va a handoff aunque la etiqueta sea "normal"? ¿Qué cuesta un falso positivo y qué un falso negativo en salud?
3. ¿Quién puede ejecutar `Command(resume=...)` y cómo comprueba tu servidor que es Jioysi?

Fuentes leídas: `openai/openai-agents-python` (MIT) `examples/agent_patterns/` (`input_guardrails.py`, `human_in_the_loop*.py`), ADR-009 y la documentación oficial de LangGraph (*Interrupts*).
