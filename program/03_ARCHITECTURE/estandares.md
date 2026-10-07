# Estándares de ingeniería — cómo se construye AQUÍ, por qué, y de quién nos guiamos

> **Propósito:** inducir a los practicantes y a sus asistentes de IA a construir de una sola forma, con un stack decidido y seguro, para que el producto **dure años** — no solo la semana. Complementa `architecture.md` (la forma), `stack-versiones.md` (las versiones) y los ADRs (el porqué de cada decisión). Si algo lo contradice, mandan estos documentos.

## 1. El stack y por qué (decisiones cerradas, no se debaten en un PR)

| Pieza | Por qué esta |
|---|---|
| **Python 3.11** | El ecosistema de IA más maduro; LangGraph/Chroma verificados; un solo lenguaje para todo el equipo. |
| **FastAPI** | Async nativo (el webhook responde <1 s), tipado con Pydantic y OpenAPI = **contratos** gratis. |
| **LangGraph** | Grafo con estado explícito: se ve, se traza y se interrumpe; una cadena oculta no se depura. |
| **ChromaDB local** | RAG sin servicios pagados y **las conversaciones no salen de la máquina** (privacidad del negocio). |
| **SQLite → Postgres** | Empezar simple, con ruta de migración clara (ADR-005). |
| **Ollama local (DeepSeek)** | Privacidad + costo cero en runtime (ADR-008); la API pagada solo existe en el CI del repo. |
| **Pydantic v2** | Todo lo que cruza una frontera se valida: menos errores y menos superficie de inyección. |
| **ruff + mypy + pytest + bandit** | Calidad automatizada = se puede cambiar código sin miedo. Eso es lo que hace **perdurar** un sistema. |

Regla: nada nuevo al stack sin responder *"¿por qué no alcanza lo que ya tenemos?"* — si cambia la arquitectura, va con ADR.

## 2. Arquitectura limpia AQUÍ (puertos y adaptadores, versión corta)

**Guía base: _Architecture Patterns with Python_ ("Cosmic Python", Percival & Gregory)** — puertos y adaptadores pensados para Python. **NO** seguimos la "Clean Architecture de libro" (capas ceremoniales de la era Java): aquí cada capa extra debe pagar su costo.

- **Dirección de dependencias:** `api` → `services`/`agents` → **puertos**. Los *adapters* (`channels/`, `models/`, `infrastructure/`, `services/`) implementan los puertos. El núcleo (`agents/`, `tools/`, `rag/`) **no sabe** qué es Meta, Ollama, Sheets ni HTTP.
- **Contratos como frontera:** todo cruce entre capas pasa por un contrato validado — `InboundEvent` (ADR-011), schemas Pydantic de entrada/salida de tools. Un contrato es la promesa que permite cambiar un lado sin romper el otro.
- **Un módulo = una responsabilidad**; imports absolutos desde `src.`; prohibido el cajón de sastre `utils.py`.
- **Multitenant:** la configuración vive en `configs/<tenant>/`; el núcleo no tiene `if tenant == ...`.
- **¿Por qué así?** Para poder cambiar WhatsApp por TikTok, Ollama por otro modelo, Excel por un ERP — **sin tocar los agentes**. Eso es lo que permite que esto siga vivo en 2027.
- Anti-patrón a reconocer (caso de estudio `cofounder-agi`): código que *parece* hacer algo (memoria con `hash()` inestable) pero no tiene contrato ni tests → recupera ruido. Se delata con un test de relevancia.

**Prohibido en el núcleo:** llamar APIs de canal desde un nodo del grafo · lógica de negocio en el router · estado en variables globales.

## 3. Código limpio AQUÍ (adaptado a este proyecto, sin dogma)

**Guías: PEP 8 y PEP 20 (Zen of Python) como ley** — ruff las automatiza — más las convenciones de **FastAPI ("Bigger Applications")** y `fastapi-best-practices`.

- **Idioma:** identificadores y nombres de archivos **en inglés**; textos al usuario, prompts y reglas de negocio **en español peruano**. Consistencia > preferencia personal.
- Funciones **pequeñas y de un solo propósito** (temprano return, sin anidar 4 niveles).
- **Tipos en todo** (mypy en cero); errores explícitos y tipados; `except:` desnudo = PR rechazado.
- Comentarios solo para el **porqué** no obvio; el código dice el cómo. Sin código muerto.
- **Tests = especificación:** un test por criterio de aceptación del Issue + casos borde; mocks para todo lo externo (sin llamadas reales a modelos ni APIs).
- Abstracción recién con **2–3 usos reales** (YAGNI). Primero funciona → luego limpio → siempre probado.
- Un PR se lee como una carta: commits convencionales, diff mínimo, evidencia (captura/log), preguntas respondidas.

**Cómo trabajamos el código (contratos y tests):**

- **Contract-first en las fronteras:** primero el contrato (schema Pydantic: `InboundEvent`, schemas de tools) y su test; después el parseo/implementación. La frontera se congela y cada lado puede cambiar sin romper al otro.
- **TDD pragmático en el núcleo:** el test del criterio de aceptación se escribe **antes** (o junto) a la implementación: rojo → verde → limpio. No es dogma de cobertura: el test *define* lo que se pidió.
- **HTTP: OpenAPI generado** por FastAPI (`/docs`, `/openapi.json`) es el contrato y la documentación **vivos**. Pruebas manuales con `/docs` + `curl`; Postman/Insomnia/Bruno son opcionales y sus colecciones **no** son fuente de verdad (pueden divergir). Prohibido mantener specs escritas a mano que nadie actualiza.

## 4. Seguridad por diseño (la razón del harness)

**Guías: OWASP GenAI (Top 10 LLM + Agentic Security Initiative) + ADR-009** — ver `source_map.md`.

- **Secretos:** solo en `.env`/GitHub Secrets. Nunca en código, logs, fixtures, capturas ni chats de IA. Push protection y secret scanning están activos: si lo intentas, rebota.
- **Datos:** corpus anonimizado; nombres/teléfonos reales jamás en tests; **lo clínico no se guarda** → el agente deriva a Jioysi (safety).
- **Escrituras con gate (N2):** agendar/registrar lead = `draft_effects → confirmación → apply_effects` (ADR-009) — evita dobles citas al reanudar un checkpoint.
- **Prompt injection:** el mensaje de la clienta es **dato**, nunca instrucción del sistema; las tools tienen argumentos validados y listas permitidas (nunca comandos libres); jamás ejecutar código generado por el modelo.
- **Permisos mínimos:** tokens con los scopes justos (ej.: `BOARD_PAT` = solo projects), acciones de CI **pineadas por SHA**, `GITHUB_TOKEN` read-only por defecto.
- **Dependencias y licencias:** Dependabot + dependency-review activos; de un repo ajeno se **lee** (con su licencia a la vista), no se copia (regla de `source_map.md`).
- **IA externa:** la API de DeepSeek se usa solo para el review de PRs (código que ya es del repo). Las conversaciones de clientas no salen de la máquina local.

## 5. De quién nos guiamos (fuentes canónicas y qué tomamos de cada una)

| Fuente | Qué tomamos | Qué NO |
|---|---|---|
| **12-Factor Agents** (Dex Horthy, `humanlayer/12-factor-agents`) | El agente es software: prompts propios y versionados, contexto explícito, tools como salidas estructuradas, agentes chicos, control de flujo propio | frameworks "mágicos" que esconden el flujo |
| **Anthropic — «Building Effective Agents»** | Empezar simple (workflow antes que agente); patrones composables (chaining, routing, evaluator) solo cuando el problema los pida | multiagente temprano / sobre-ingeniería |
| **Cosmic Python** (Percival & Gregory) | Puertos y adaptadores en Python, capa de servicios liviana, dependencias hacia adentro | capas ceremoniales de la Clean Architecture clásica |
| **FastAPI docs** («Bigger Applications») + `fastapi-best-practices` | Estructura de routers/dependencies/lifespan para proyectos medianos | micro-frameworks alternativos |
| **PEP 8 / PEP 20 + ruff + mypy** | Legibilidad y tipos automatizados como ley | debates manuales de estilo |
| **OWASP GenAI + ASI** (ya en `source_map`, S12/S15) | Riesgos de agentes y sus mitigaciones | — |
| **Trunk-Based Development** (Google, ya en `source_map`) | Rama corta, PR pequeño, `main` siempre desplegable (ADR-006) | ramas long-lived |
| **ADRs (formato Nygard)** | Toda decisión de arquitectura con contexto y consecuencias | decisiones invisibles o "porque lo dijo la IA" |

## 6. El resumen que le das a tu IA (pégalo en tu primer prompt de diseño)

> "Construimos Python 3.11 + FastAPI + LangGraph + Chroma local + Ollama; puertos y adaptadores (el núcleo no conoce canales ni servicios); contratos Pydantic en cada frontera; inglés en el código, español peruano en los textos; tests por criterio del Issue; seguridad desde el diseño (sin secretos, sin datos reales, escrituras con confirmación, texto del usuario = dato nunca instrucción). Antes de proponer código nuevo, dime qué pieza reutilizo y por qué no basta."

**Por qué todo esto perdura:** contratos + tests + CI → cambiar sin miedo · ADRs → cualquiera retoma el proyecto en meses · seguridad por diseño → el negocio puede venderlo · un solo stack y estilo → 3 practicantes + IAs sin pisarse · local-first → costo variable cero hasta que el negocio lo pida.
