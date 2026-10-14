\# Mi mapa de una página — Inducción S5 evidencia del issue:42

\*\*Josue Marreros · 2026-10-13\*\*



\## 1. Para quién trabajo y qué problema resuelvo

\- \*\*Negocio:\*\* Servimos a \*Hola Mujer\*, un negocio de salud y estética para mujeres en Chimbote, con 47 servicios en 13 categorías (S/ 24.99–449.99).

\- \*\*Problema real:\*\* ManyChat y n8n fracasaron porque "no atienden como humano": menús rígidos, sin memoria ni empatía. El embudo medido lo prueba: \*\*33 invitaciones → 2 horarios elegidos\*\*; el cuello está entre el CTA y la confirmación.

\- \*\*Por qué existe este proyecto:\*\* Un asistente que recuerda el hilo (memoria por teléfono), habla corto y claro (≤3 líneas, 1 pregunta por turno), ofrece 2–3 horarios reales y deriva a Jioysi cuando el tema es de salud (nunca opina de salud).



\## 2. Qué construimos y cómo fluye un mensaje

\- \*\*Diagrama:\*\* `mapa-hitos-s5.png`

\- \*\*Flujo (mensaje → respuesta):\*\*

&#x20; `Clienta` ──▶ `WhatsApp/Meta` ──▶ `Webhook FastAPI (Integration Hub)` (valida firma · responde 200 rápido) ──▶ `adapter` ──▶ `InboundEvent` ──▶ `Grafo LangGraph (memoria · prompt · RAG · tools)` ──▶ `OutboundReply` ──▶ `sender (httpx)` ──▶ `Meta` ──▶ `Clienta`

\- \*\*El contrato interno:\*\* `InboundEvent`/`OutboundReply` independizan al agente del canal: "la capa de agentes es el producto; el canal es un adaptador". Si mañana pasamos a TikTok, agentes, RAG y memoria no cambian — solo un adapter nuevo en `src/channels/`.



\## 3. Adónde llegamos

\- \*\*Hitos:\*\*

&#x20; - \*\*HITO 1 (S6 D3):\*\* el bot responde precios/duraciones/servicios desde RAG real por WhatsApp.

&#x20; - \*\*HITO 2 (S9 D3):\*\* agente único completo — 4 agentes + handoff a humano (sin supervisor todavía; multiagente, OCR y voz vienen en S9–S12).

&#x20; - \*\*HITO 3 (S12 D3):\*\* NeuraCode (2.º negocio) atendiendo + notas de voz.

&#x20; - \*\*Demo final (S16 D3):\*\* producción proactiva con Postgres, Docker, evaluación E2E e informe SENATI.

\- \*\*Dónde estoy hoy:\*\* Semana 5 (S5), Fase 2 (Agente único, S4–S8).

\- \*\*Qué hito me toca primero:\*\* el \*\*HITO 1\*\*. Mi parte: el Integration Hub (FastAPI, mi Issue #2 — /health y CI), y sigue el adapter de WhatsApp (webhook + envío), LangGraph con memoria por teléfono y el RAG de servicios reales.



\## 4. Qué herramientas uso y por qué esas

\- \*\*FastAPI + Pydantic:\*\* recibir webhooks con contratos validados y docs automáticas; Pydantic valida los datos en cada frontera. Sin ellas: validación manual y datos sucios llegando al agente.

\- \*\*LangGraph + ChromaDB + memoria (SQLite→Postgres):\*\* LangGraph da estado y pausas al grafo; ChromaDB alimenta el RAG de servicios/precios reales; la memoria persistente (por teléfono) hace que el bot no "olvide" al reiniciar. Sin ellas: un script sin estado, precios inventados y conversaciones perdidas.

\- \*\*Ollama / DeepSeek local:\*\* el modelo corre en nuestra infraestructura — sin costo por token de API y sin enviar datos de clientas a terceros.



\## 5. Por qué trabajo con Issue → rama → test → PR → review

\- \*\*El porqué del método:\*\* cada cambio tiene motivo (Issue), aislamiento (rama corta), criterio demostrable (test primero), calidad (4 puertas: ruff, mypy, pytest, bandit) y revisión humana (PR con `Closes #N`); así `main` siempre está estable y queda evidencia verificable.

\- \*\*Qué aprendí esta semana:\*\* que ser AI engineer no es escribir código, sino entender el problema del negocio y elegir herramientas con criterio. Dos ideas que antes confundía: responder \*\*200 rápido\*\* (Meta no reintente por timeout) es distinto de la \*\*idempotencia\*\* (si Meta reenvía el mismo mensaje dos veces, no se duplica el efecto).
