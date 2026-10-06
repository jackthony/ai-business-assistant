# Pack de contexto por fase — qué cargar y cómo usar tu IA sin quemar tokens

> Para practicantes y sus asistentes de IA (OpenCode con modelos gratis). Regla de oro: **cargar poco, puntual y verificado**. El trabajo exacto de tu semana está en tu Issue de GitHub; aquí está el CONTEXTO mínimo para entenderlo de verdad. Si un documento no está listado, no lo abras.

## Contexto base (léelo una vez por semana, ~15 min)

**El negocio — Hola Mujer en 12 líneas:**
1. Es un negocio de servicios de salud y estética para mujeres, con atención en **Chimbote** (la ubicación causa fricción: pregunta la ciudad temprano).
2. El objetivo del bot: informar servicios, **agendar**, recordar y **derivar a Jioysi** (humana) — sin guardar **nunca** datos clínicos.
3. Antes usaron ManyChat y luego un agente con n8n: **al público no le gustó porque "no atiende como humano"**. Este proyecto existe para corregir eso.
4. Por eso el bot debe: saludar por nombre, recordar el hilo (memoria por teléfono), mensajes **≤3 líneas**, **1 pregunta por turno**, español peruano empático.
5. El **corpus de conversaciones reales** (era ManyChat/n8n, anonimizado, en `data/conversaciones/`) es el activo más importante: de ahí salen ejemplos y mejoras.
6. Hay **47 servicios** en 13 categorías, precios S/ 24.99–449.99; el bot jamás inventa un precio: los saca del RAG.
7. El embudo medido: 33 invitaciones → 2 horarios elegidos. El cuello está entre el CTA y la confirmación; el bot debe ofrecer 2–3 horarios reales.
8. Varias promociones del Excel están inactivas o con fechas raras: se validan con el negocio antes de cargarlas.
9. Regla de seguridad clínica: si el tema es médico/emergencia, pausar y derivar a Jioysi con resumen no clínico.
10. El tenant se llama `hola_mujer` (pronto habrá un 2.º negocio: NeuraCode — por eso el diseño es multitenant).
11. Tono de venta: un CTA concreto por mensaje, explicación breve, nunca bloques largos; un "gracias/ok" puede ser abandono silencioso.
12. Todo se mide: `booking_rate`, `show_rate`, `sale_rate`, satisfacción. Si no se mide, no cuenta.

**La ingeniería en 8 líneas:**
1. El canal (WhatsApp hoy; mañana otro) entra por un **webhook** → se convierte al contrato **`InboundEvent`** (ADR-011): los agentes nunca saben de qué canal vino.
2. FastAPI es el **Integration Hub** (ADR-001); LangGraph es el **grafo** del agente (ADR-002).
3. Arquitectura en carpetas: `src/channels/` (canales), `src/agents/` (agentes), `src/services/`, `configs/` (prompts versionados), `tests/`.` 
4. **Un agente único primero**; multiagente recién en S10 (ADR-007).
5. El **modelo corre local** (Ollama, DeepSeek local-first, ADR-008) — gratis y privado. En tu PC solo modelos chicos o mocks; el runtime grande vive en la M5 del monitor.
6. Trabajamos con **TBD de aprendizaje** (ADR-006): rama corta `issue-N-slug` → commits convencionales → PR con `Closes #N` → CI verde → merge squash. El guardian lo verifica.
7. Las 4 puertas (`ruff`, `mypy`, `pytest`, `bandit`) son obligatorias en cada PR; sin secretos ni datos reales en tests (fixtures anonimizados).
8. Las escrituras reales (agendar, registrar lead) pasan por un **gate de confirmación** (ADR-009) y todo se observa con trazas (S8+).

**Los ADRs en una línea** (lee solo el que toque tu semana): 001 FastAPI · 002 LangGraph · 003 WhatsApp Cloud API directo · 004 RAG con ChromaDB · 005 memoria sqlite→postgres · 006 TBD de aprendizaje · 007 agente único primero · 008 DeepSeek local-first · 009 harness de seguridad · 010 frameworks de referencia · 011 canal-agnóstico.

## Uso controlado de tu IA (protocolo — aplícalo en toda la fase)

1. **Antes de abrir la IA:** lee este pack y tu Issue (~30 min). Sin eso, tu prompt va a ser vago y el modelo va a gastar contexto adivinando.
2. **Un prompt = una tarea** con salida verificable: "implementa `X` en el archivo `Y` para cumplir `Z`; después su test". Nada de pedidos gigantes.
3. **Adjunta solo los archivos listados** (en OpenCode, nombra la ruta exacta). Nunca "lee todo el repo" ni pegues documentos completos.
4. **Prohibido pedir:** "hazme el Issue entero", "commitea tú", "resume el repo", "escribe el informe". Eso es el engaño académico que el diagnóstico detecta (nota 0 en ese criterio).
5. **Presupuesto por sesión (3 h): ~10–15 interacciones útiles de IA.** Si llegas a 20 sin commits verificables, algo va mal: para, reformula el objetivo en una frase y vuelve.
6. **Señal de desperdicio:** el modelo repite, pide más contexto o inventa APIs. Corta → 1 reformulación puntual → si sigue: DeepSeek web para la duda conceptual, o pregunta al monitor en el grupo.
7. **Tú ejecutas y verificas todo** antes de commitear (las 4 puertas locales). **La IA no firma nada: el commit y la explicación son tuyos.**
8. **Nada de datos reales** del negocio en el chat de IA: usa el corpus anonimizado; si dudas, no lo pegues.
9. **Nunca pegues secretos** (tokens, claves, `.env`) en ningún chat ni código.
10. **Cierra la sesión** con 5 líneas: qué entendí, qué probé, qué me falta. Eso alimenta tu informe FPE (y no dice "lo hizo la IA").

---

## Semana 4 — Producto: el ciclo mensaje → respuesta

- **Negocio en foco:** cada mensaje de una clienta entra por el webhook y una respuesta del negocio sale por el sender. Es la puerta de entrada: si esto no funciona, nada más importa.
- **Lee antes (repo):** tu Issue (`#2`/`#3`/`#4` en GitHub) · `program/02_REFERENCE/whatsapp-cloud-api.md` (§Puntos clave) · `program/03_ARCHITECTURE/decisions/ADR-011-canal-agnostico.md` · `program/02_REFERENCE/stack-versiones.md`.
- **Fuentes externas:** la FORMA del payload real en `fbsamples/whatsapp-api-examples` o `david-lev/pywa` (solo mirar, no copiar) · quickstart de ngrok o `cloudflared tunnel`.
- **No cargues:** el plan completo · ADRs que no sean de tu semana · el Excel del negocio (para #2/#3/#4 no hacen falta sus datos).
- **Con tu IA, ejemplo bueno:** "Implementa `parse_message(payload)` en `src/channels/whatsapp/webhook.py` según el contrato `InboundEvent` de ADR-011: devuelve wa_id, texto y tipo; ignora `statuses`. Genera también su test con `tests/fixtures/webhook_text.json`. Sin llamadas reales a Meta."
- **Mal pedido:** "ármame el webhook de WhatsApp" (sin contrato, sin archivos, sin tests).
- **Listo cuando:** criterios de tu Issue + CI verde + las preguntas de comprensión respondidas en tu PR.

## Semana 5 — LangGraph core: grafo, prompt, memoria

- **Negocio en foco:** el bot debe **hablar como Hola Mujer**: ≤3 líneas, 1 pregunta por turno, español peruano empático, nunca inventar precios.
- **Lee antes (repo):** tu Issue (`#04`/`#05`/`#06`) · `program/02_REFERENCE/agent-engineering-handbook.md` (Partes II–III) · `ADR-002` y `ADR-008` · secciones del prompt/tono en `program/04_DOMAIN/hola-mujer.md`.
- **Fuentes externas:** documentación oficial de LangGraph (conceptos StateGraph/checkpoint), nada más.
- **No cargues:** ETL/Chroma (S6) ni agentes (S7): no los necesitas aún.
- **Con tu IA:** pide el grafo mínimo con su test de CLI por partes; para el prompt, pide componentes separados (identidad, tono, límites) — nunca un monolito.
- **Listo cuando:** grafo compilando y respondiendo por CLI, prompt versionado en `configs/hola_mujer/prompt_v1.md`, memoria por teléfono sobrevive reinicio.

## Semana 6 — RAG + HITO 1: el bot conoce el negocio

- **Negocio en foco:** el bot responde con los **47 servicios reales y sus precios** (S/ 24.99–449.99) sacados de la fuente, jamás inventados. El **corpus real** (`data/conversaciones/`) es la fuente prioritaria de ejemplos y objeciones.
- **Lee antes (repo):** tus Issues (`#07`/`#08`/`#09`) · `ADR-004` · `data/conversaciones/README.md` · `program/04_DOMAIN/hola-mujer.md` (§Catálogo y §Promociones — validar cuáles están activas).
- **Fuentes externas:** solo si falta corpus, dataset Bitext de customer support (licencia CDLA).
- **No cargues:** features fuera del hito; el Excel completo (el ETL lee la hoja, no la pegues en chats).
- **Con tu IA:** pide que te explique el anti-caso `cofounder-agi` (vectores aleatorios por `hash()`) y cómo se delata un retrieval sin relevancia.
- **Listo cuando:** 10/10 respuestas verificadas contra la fuente + demo en vivo (hito 1) + release `hito-1`.

## Semana 7 — Tools + Agentes 1 y 2

- **Negocio en foco:** dos fricciones reales medidas: la ubicación (guardrail Chimbote) y el cuello 33→2 (ofrecer **2–3 horarios reales**, cero colisiones).
- **Lee antes (repo):** tus Issues (`#10`/`#11`/`#12`) · `ADR-007` · handbook (Parte VI: diseñar la ACI/tools).
- **No cargues:** pagos (S10), recordatorios (S13): fuera de fase.
- **Con tu IA:** schemas Pydantic estrictos con tests de argumentos inválidos; revisión de colisiones caso por caso.
- **Listo cuando:** 0 precios inventados, guardrail probado, tool-calling local funcionando, 0 colisiones en 10 pruebas.

## Semana 8 — Cierre de venta, lead y telemetría

- **Negocio en foco:** pedir nombre, DNI (8 dígitos) y celular peruano para agendar; **jamás** datos clínicos; una fila por lead; toda escritura real pasa por el gate de confirmación (ADR-009).
- **Lee antes (repo):** tus Issues (`#13`/`#14`/`#25`) · `ADR-009` y `ADR-005` · `program/02_REFERENCE/observabilidad-costos.md`.
- **Fuentes externas:** docs de Langfuse self-host (Docker) solo para levantarlo en la M5.
- **Con tu IA:** mock de Sheets para los tests; pruebas de idempotencia (mismo `request_id` no duplica).
- **Listo cuando:** flujo info→cita→datos completo, dashboard con 3 métricas, release `q4`.

---

S9–S16: su bloque se añade al inicio de cada quincena (los Issues dominicales lo incluirán automáticamente).
