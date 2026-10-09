# Inducción — entender el para qué, el con qué y el por qué (arranque de S5)

> **Para quién:** Josue (lunes 12-oct) y Pilar y Allan (miércoles 14-oct). **Duración:** 90–120 min con el monitor, al empezar su semana. **Meta:** que al terminar puedas explicar, con tus palabras y sin leer, **a quién servimos, qué construimos, adónde llegamos, con qué herramientas y por qué trabajamos paso a paso así**. No es una clase para escuchar: se conversa, se dibuja y se responde.
>
> Un buen profesional de IA no es quien más código escribe: es quien entiende el problema del negocio, elige herramientas con criterio, deja evidencia y puede explicar por qué hizo cada cosa. Eso es lo que se evalúa aquí.

## Antes de la sesión (30 min, solo lectura)

1. `program/00_PROJECT/roadmap.md` — la visión, el alcance y los hitos.
2. `program/01_CURRICULUM/pack_contexto.md` — «Contexto base» (el negocio en 12 líneas y la ingeniería en 8).
3. `program/03_ARCHITECTURE/decisions/ADR-011-canal-agnostico.md` — el contrato que separa el canal del agente.
4. Corre `tools/onboarding/empezar.sh` (o `empezar.ps1` en Windows): así empiezas con tu carpeta ordenada y tu bitácora del día.

---

## Bloque 1 — El negocio y el problema real (20 min)

**Qué entender:** Hola Mujer es un negocio de salud y estética para mujeres en **Chimbote**. Ya probaron **ManyChat** y luego un agente en **n8n**: *al público no le gustó porque «no atiende como humano»*. El bot que construimos existe para corregir eso: recordar el hilo, hablar corto y claro, hacer **una pregunta por turno** y **derivar a una persona** cuando el tema es de salud.

**Los números que mandan:** 47 servicios en 13 categorías; el embudo medido fue **33 invitaciones → 2 horarios elegidos**: el cuello de botella está entre el CTA y la confirmación. Por eso el bot ofrece 2–3 horarios **reales** y se mide todo (`booking_rate`, `show_rate`, `sale_rate`).

**Actividad (10 min):** lee 3 conversaciones anonimizadas de `data/conversaciones/` y anota, por cada una, **tres cosas que haría una persona atenta y que un bot de menú no haría**.

**Pregunta de control:** ¿por qué un bot con menús rígidos pierde clientas aunque «funcione» técnicamente?

## Bloque 2 — La visión y el mapa: adónde vamos (15 min)

| Fase | Semanas | Qué se logra | Hito |
|---|---|---|---|
| 1. Fundamentos | S1–S3 | Git, tests, HTTP/REST, contratos | (hecho) |
| 2. Agente único | S4–S8 | FastAPI + webhook + LangGraph + RAG + citas + cierre | **HITO 1** (bot respondiendo, fin de S6) |
| 3. Multiagente | S9–S12 | Seguridad, HITL, OCR, supervisor, 2.º negocio (NeuraCode), voz | **HITO 2** (S9) · **HITO 3** (S12) |
| 4. Producción | S13–S16 | Proactivo, Postgres, Docker, deploy, E2E | **Demo final** (S16) |

**La visión en una frase:** un asistente de IA empresarial **multitenant** y **canal-agnóstico** (hoy WhatsApp, mañana TikTok u otro canal) que atiende como una persona, no alucina y deja trazabilidad. **La capa de agentes es el producto; el canal es un adaptador.**

**Y tú:** terminas como **AI engineer que ya operó un agente en producción real**, con evidencia verificable (commits, PRs, dashboards, informes). Más allá de S16 el bot queda corriendo con evaluaciones continuas, costos medidos por conversación y nuevos canales sin tocar los agentes.

**Actividad (5 min):** dibuja en una hoja la línea S4 → S16 con los 4 hitos y marca **dónde estás hoy** y **qué hito te toca construir primero**.

**Pregunta de control:** ¿por qué decimos que «el canal es un adaptador»? ¿Qué cambiaría si mañana pasamos de WhatsApp a TikTok?

## Bloque 3 — Qué construimos: el ciclo mensaje → respuesta (25 min)

```
 Clienta ──WhatsApp──▶ Meta ──webhook──▶ FastAPI (Integration Hub)
                                              │  valida firma · responde 200 rápido
                                              ▼
                              adaptador del canal  ──▶ InboundEvent   (contrato interno, ADR-011)
                                              │
                                              ▼
                                  grafo del agente (LangGraph)
                          memoria por teléfono · prompt por componentes · RAG · tools
                                              │  (acciones con efecto pasan por aprobación humana)
                                              ▼
                              OutboundReply ──▶ sender (httpx) ──▶ Meta ──▶ Clienta
```

**Ideas clave:**
- **Contrato interno** (`InboundEvent` / `OutboundReply`): los agentes **nunca** conocen el canal. Si cambia Meta, se cambia un adaptador, no el agente.
- **Un agente único primero** (ADR-007): se complica solo cuando hay evidencia de que hace falta (supervisor en S10).
- **Núcleo sin efectos secundarios ocultos:** lo que escribe en el mundo real (agendar, registrar, validar un pago) pasa por un **gate de confirmación** (ADR-009).
- **Monolito modular multitenant:** un solo servicio, con configuraciones separadas por negocio (Hola Mujer y NeuraCode). Los patrones de arquitectura que sí aplican están en `program/02_REFERENCE/ejemplos/patrones-arquitectura.md`.

**Actividad (10 min):** sin mirar el diagrama, redibújalo y explica en voz alta qué pasa si Meta reenvía el mismo mensaje dos veces (pista: idempotencia).

**Pregunta de control:** ¿por qué respondemos `200` rápido al webhook y procesamos después?

## Bloque 4 — Las herramientas y por qué esas (25 min)

| Herramienta | Qué problema resuelve | Qué pasaría sin ella |
|---|---|---|
| **Python 3.11** | Un solo runtime verificado para todo el stack | Cada PC con versiones distintas: «en mi máquina funciona» |
| **FastAPI** | Recibir webhooks y exponer endpoints con contratos validados y docs automáticas | Código manual de validación y sin OpenAPI |
| **Pydantic** | Validar datos en cada frontera (entrada, tools, salida) | Datos sucios llegando al agente |
| **httpx** | Llamadas HTTP async (enviar mensajes) y fáciles de simular en tests | Pruebas que llaman a Meta de verdad |
| **LangGraph** | Agente como grafo con estado, memoria y pausas (`interrupt`) | Un script gigante sin estado ni trazabilidad |
| **SQLite → Postgres** | Memoria persistente por teléfono | El bot «olvida» al reiniciar |
| **ChromaDB (RAG)** | Responder con datos reales (precios, servicios) en vez de inventarlos | Alucinaciones de precios |
| **Ollama / DeepSeek local** | Modelo propio: gratis, privado y sin enviar datos a terceros | Costo por token y datos de clientas fuera de casa |
| **Langfuse + OpenTelemetry** | Ver cada conversación: latencia, tokens y costo | Operar a ciegas |
| **pytest · ruff · mypy · bandit** | Las 4 puertas del CI: tests, estilo, tipos y seguridad | Errores que llegan a producción |
| **pre-commit** | Que ruff corra solo en cada commit | Commits con errores de estilo |
| **GitHub (Issues, PRs, Actions, Projects)** | Trabajo trazable: cada cambio tiene motivo, revisión y evidencia | Cambios sin historia ni responsable |
| **ngrok / cloudflared** | Exponer tu `localhost` para probar el webhook real | Probar solo con fixtures |
| **OpenCode / DeepSeek web (tu IA)** | Un asistente para dudas puntuales, con uso controlado | O dependes de él, o no lo usas bien |

**Actividad (10 min):** elige **tres** herramientas y explica a tu compañero «qué problema resuelve y qué pasaría sin ella», sin leer la tabla.

**Pregunta de control:** ¿por qué corre el modelo en local y no en una API de pago? ¿Qué decisión de negocio hay detrás?

## Bloque 5 — El método y su porqué (25 min)

Cada paso de cómo trabajamos existe por una razón. Si entiendes la razón, no lo haces «porque lo manda el monitor»; lo haces porque **es lo que haría un equipo profesional**.

| Paso | Qué haces | **Por qué** | Qué se rompe si lo saltas |
|---|---|---|---|
| 1. Issue | Trabajas sobre una tarea escrita con criterios | Todo cambio tiene un motivo y un «listo cuando» | Haces algo que nadie pidió |
| 2. `git pull` | Empiezas con `main` actualizado | El código viejo causa conflictos | Pierdes horas resolviendo choques |
| 3. Rama corta `issue-N-slug` | Aíslas tu trabajo | Cambios pequeños se revisan y se deshacen fácil | Un cambio enorme que nadie puede revisar |
| 4. Test primero (contract-first + TDD) | Escribes el criterio como test | El test es la especificación; demuestra que cumples | «Funciona» sin prueba |
| 5. Commits chicos y convencionales | `tipo(alcance): verbo` | Historial legible; se entiende qué y por qué | Historial inútil, difícil de auditar |
| 6. Las 4 puertas en local | `ruff`, `mypy`, `pytest`, `bandit` | Lo que pasa en tu PC = lo que pasa en el CI | El PR vuelve rojo y pierdes tiempo |
| 7. PR con `Closes #N` | Pides integrar con evidencia | Une cambio, Issue y revisión | Trabajo huérfano |
| 8. Preguntas de comprensión | Respondes con tus palabras | Demuestra que **entendiste**, no que alguien lo generó | Aprendes a copiar, no a razonar |
| 9. Review del monitor | Recibes feedback concreto | Es donde más se aprende | Repites el mismo error |
| 10. Merge squash | Un commit limpio en `main` | `main` siempre estable | `main` roto para todos |
| 11. Bitácora e informe | Anotas qué hiciste y qué aprendiste | Evidencia y reflexión; base de tu informe FPE | Nada que sustentar |

**Reglas que protegen al negocio:** nada de datos reales de clientas en el repo o en tu IA (fixtures anonimizados); nunca secretos en el código; el bot **nunca** opina de salud: deriva a una persona. **Tu IA:** un prompt = una tarea verificable, ~10–15 interacciones por sesión; tú ejecutas, verificas y firmas.

**Actividad (5 min):** elige un paso de la tabla y cuéntale al grupo **qué pasó alguna vez que lo saltaste** (en este proyecto o en tus estudios).

**Pregunta de control:** ¿por qué respondes las preguntas de comprensión «con tus palabras» aunque tu IA pueda contestarlas mejor?

## Cierre (10 min) — Tu mapa de una página

Entrega: `notas-estudio/mi-mapa.md` en tu carpeta de trabajo, con estas 5 secciones de 2–3 líneas cada una, **en tus palabras**:

1. **Para quién trabajo y qué problema resuelvo.**
2. **Qué construimos y cómo fluye un mensaje** (con tu diagrama).
3. **Adónde llegamos** (hitos, y qué parte me toca a mí).
4. **Qué herramientas uso y por qué esas.**
5. **Por qué trabajo con Issue → rama → test → PR → review, y qué aprendí de eso esta semana.**

Pega 5 líneas con lo esencial como comentario en tu Issue de inducción. El monitor lo revisa contigo y lo cierra.

## Banco de preguntas para la conversación (el monitor elige 5)

1. ¿Qué dijo el público de ManyChat/n8n y qué hace distinto este bot?
2. ¿Qué es el contrato `InboundEvent` y qué problema evita?
3. ¿Qué pasa si el mismo mensaje llega dos veces? ¿Y si el envío falla a medias?
4. ¿Por qué el modelo corre en local? ¿Qué se gana y qué se pierde?
5. ¿Por qué la acción de agendar pasa por un gate de confirmación?
6. ¿Qué mide el embudo y en qué punto estaba el cuello de botella?
7. ¿Por qué se escribe el test antes que el código?
8. ¿Cómo sabes que tu PR está «listo»? ¿Quién lo decide?
9. ¿Qué haces cuando te trabas? ¿En qué orden pides ayuda?
10. ¿Qué parte del proyecto te toca en el HITO 1 y por qué importa para el negocio?

## Glosario mínimo (se amplía en tu bitácora)

- **Webhook:** Meta nos *avisa* cuando llega un mensaje (en vez de que preguntemos cada rato: polling).
- **Idempotencia:** repetir la misma petición no cambia el resultado ni duplica efectos.
- **Contrato:** acuerdo escrito y validado sobre qué datos entran y salen de una pieza.
- **Adaptador (puertos y adaptadores):** pieza que traduce entre el mundo externo (WhatsApp) y nuestro núcleo.
- **Tenant:** un negocio dentro del sistema (Hola Mujer, NeuraCode), con sus datos separados.
- **RAG:** el modelo consulta una base de datos del negocio antes de responder, en vez de inventar.
- **Checkpoint / `thread_id`:** la «foto» del estado de una conversación y su identificador (el teléfono).
- **HITL (human-in-the-loop):** una persona aprueba antes de que ocurra un efecto real.
- **CI:** verificación automática en GitHub de que tu cambio cumple las reglas (las 4 puertas).
- **ADR:** documento corto que registra *por qué* se tomó una decisión de arquitectura.
- **TBD (trunk-based development):** ramas cortas que vuelven pronto a `main`.
- **FinOps:** medir y controlar el costo por conversación.
