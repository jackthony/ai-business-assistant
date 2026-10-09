# Ejemplos guiados — bloques de construcción por Issue

> Para practicantes y sus IAs. Cada carpeta es **un bloque pequeño, ejecutable y con tests** que enseña UNA técnica que tu Issue necesita. **No resuelven tu Issue**: tú conectas los bloques al contrato `InboundEvent`/`OutboundReply` (ADR-011), a tus rutas y a tus fixtures. Si copias y pegas sin entender, la puerta de comprensión de tu PR te lo va a pedir explicado con tus palabras.

## Cómo usarlos (con tu IA, sin gastar tokens)

1. Lee tu Issue y el bloque de tu semana en `program/01_CURRICULUM/pack_contexto.md`.
2. Abre **solo** la carpeta de tu Issue de esta lista (README + 1 archivo `.py` + su test). No cargues las demás.
3. Corre el test del ejemplo **antes** de tocar nada, para ver el comportamiento esperado:
   ```bash
   pytest program/02_REFERENCE/ejemplos/<carpeta> -q
   ```
4. Pide a tu IA, un prompt = una tarea: "adapta el bloque `X` a mi `src/...` respetando el contrato Y; escribe su test". Nunca "hazme el Issue".
5. Responde en tu PR las preguntas de comprensión del Issue **y** las del README del ejemplo que usaste.

## Índice

| Carpeta | Para el Issue | Técnica que enseña |
|---|---|---|
| [`webhook-meta/`](webhook-meta/README.md) | #3 (S4 D2) | Verificar la **firma** `X-Hub-Signature-256` con HMAC (comparación en tiempo constante) y leer el payload anidado de WhatsApp sin romperse con `statuses`/tipos nuevos |
| [`sender-httpx/`](sender-httpx/README.md) | #4 (S4 D3) | Cliente `httpx` async con **1 reintento solo ante fallo de red**, medición de latencia y tests con `MockTransport` (cero llamadas reales a Meta) |
| [`langgraph-memoria/`](langgraph-memoria/README.md) | #04–#06 (S5) | Un `StateGraph` mínimo con memoria por `thread_id` (teléfono) en SQLite que **sobrevive un reinicio**, con deserialización estricta |
| [`s7-tools-y-citas/`](s7-tools-y-citas/README.md) | #10–#12 (S7) | Tool con args validados por Pydantic V2 y errores tipados; reservar sin colisiones ni duplicados con `request_id` (*idempotent consumer*) |
| [`s9-guardrail-y-gate/`](s9-guardrail-y-gate/README.md) | #16–#17 (S9) | Guardrail que congela ante riesgo o duda + gate `borrador → interrupt → aplicar` (ningún efecto antes de aprobar; una sola aplicación al reanudar) |
| [`s10-router-saga-tenant/`](s10-router-saga-tenant/README.md) | #15, #19, #20 (S10) | Router reglas→LLM con seguridad primero; saga con compensación (cita + pago); aislamiento por tenant |
| [`patrones-arquitectura.md`](patrones-arquitectura.md) | todos | Patrones de microservicios que SÍ aplican a nuestro monolito modular (y cuáles no), con el ejemplo de cada uno |
| [`pr-ejemplo.md`](pr-ejemplo.md) | todos | Cómo se ve un PR completo: "Qué y por qué", preguntas respondidas, evidencia y las 4 puertas |

## Fuentes de las que se aprendió (versiones fijadas)

Todo lo de aquí está **escrito de cero** para este programa; las fuentes solo se leyeron:

| Fuente | Versión leída | Licencia | Qué se tomó |
|---|---|---|---|
| `david-lev/pywa` | `108c8ff` (2026-10-08) | MIT | Cómo valida la firma del webhook (`webhook_update_validator`) y el flujo verify + parseo |
| `fbsamples/whatsapp-api-examples` | `de70ee9` | Licencia de muestras de Meta (no se copia) | Forma del payload de webhook y el ejemplo de validación de firma |
| `langchain-ai/langgraph` · `libs/checkpoint-sqlite` | rama `main` (2026-10) | MIT | Uso de `SqliteSaver` y la advertencia de seguridad `LANGGRAPH_STRICT_MSGPACK` |
| `openai/openai-agents-python` · `examples/agent_patterns` | `125efa0` | MIT | Patrones (guardrails, human-in-the-loop, routing, deterministic) para leerlos y reescribirlos como nodos de LangGraph; el SDK no se adopta (ADR-010) |
| *Microservices Patterns* (Richardson) / `microservices.io` | — | libro liberado por el autor | Catálogo de patrones (idempotent consumer, saga, tenant isolation…) |

## Lección de lectura crítica (úsala con tu IA)

El ejemplo oficial de Meta `signature-validation-with-webhooks-payloads/app.py` **tiene un bug de indentación**: el `return 'INVALID SIGNATURE HASH', 403` queda fuera del `if`, así que rechaza *todos* los POST (aunque la firma sea correcta). Además compara con `!=` (no es tiempo constante) y usa el *verify token* como clave, cuando la clave real de la firma es el **App Secret** (`WHATSAPP_APP_SECRET`). Moraleja: un ejemplo "oficial" también se prueba antes de confiar en él; por eso aquí todo trae test.
