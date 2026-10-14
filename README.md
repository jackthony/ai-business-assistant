# ai-business-assistant — Programa SENATI 2026 + Producto

Repositorio único (**público** desde 2026-10-06): **programa de prácticas** (currículo, evaluación, gestión) **+ producto** (`src/` desde S4) — HealthTech Software & AI · SENATI 2026 · ciclo 3 (Allan, Pilar y Josue). Sin correos, secretos ni datos reales de clientes.

- **Board de seguimiento (público, solo lectura para practicantes):** https://github.com/users/jackthony/projects/3 (campos Status, Semana, Alumno, Area, Complejidad) — también en la pestaña Projects del repo
- **Wiki (mapa del programa, fuentes y ruta):** https://github.com/jackthony/ai-business-assistant/wiki · **Discusiones (preguntas, lecturas guiadas, retro):** https://github.com/jackthony/ai-business-assistant/discussions
- **Estado siempre vigente:** `program/00_PROJECT/current_status.md` (semana en curso, Issues, riesgos y próximo paso). Este README describe lo **estable** (cómo está armado el repo y cómo se trabaja); lo que cambia cada semana vive en ese archivo.

## Empieza aquí (practicantes) — antes de tocar nada

Trabaja **siempre** en una carpeta ordenada, no en Descargas. Un solo comando la crea, clona el repo, prepara el entorno y te deja tu bitácora del día (corre el mismo cada día de práctica):

- **Windows:** `powershell -ExecutionPolicy Bypass -File tools\onboarding\empezar.ps1`
- **macOS/Linux:** `bash tools/onboarding/empezar.sh`

Dejará `senati-2026/` con `ai-business-assistant/` (aquí se programa), `bitacora/`, `evidencias/`, `informes/` y `notas-estudio/`. Detalle y el porqué de cada cosa: [`tools/onboarding/README.md`](tools/onboarding/README.md) y [`GUIA_PRACTICANTE.md`](GUIA_PRACTICANTE.md). Tu primera semana empieza con la **inducción** (`program/01_CURRICULUM/induccion_s5.md`): el negocio, la visión y el porqué de cada paso.

## Regla de oro

| Artefacto | Rol |
|---|---|
| **Este repo** (`ai-business-assistant`) | Fuente canónica: programa (currículo, ADRs, evaluación) + producto (`src/` desde S4) |
| **Excel EVALUABLE** | Notas numéricas y seguimiento quincenal (Drive; binario) |
| **Google Drive** | Distribución: Excel, PDFs e informes SENATI |

Nada del plan se duplica fuera de este repo: si un artefacto contradice a otro, gana este repo.

## Las tres bases de conocimiento (no confundir)

| Base | Qué es | Dónde vive | Quién la usa |
|---|---|---|---|
| **1. KB-P · Proyecto** | Currículo, arquitectura, ADRs, rúbrica, expedientes. Curada a mano. Fuente canónica. | **Este repo** | Monitor + practicantes + DeepSeek (2–3 archivos por tarea) |
| **2. KB-A · Agentes** | Datos de negocio para RAG: 47 servicios, promociones, cursos. Un namespace por tenant. | Repo de código: `data/` + ChromaDB (`configs/hola_mujer`, `configs/neuracode`) | El bot en runtime — **nunca** se usa para gestionar el programa |
| **3. KB-T · Transitoria** | 2–3 archivos por tarea (current_status + Issue + módulo/documento). | Se arma al momento en DeepSeek/IDE | El monitor y los practicantes al programar o evaluar |

Reglas: **KB-A nunca contiene docs del programa**; **KB-P nunca contiene precios/listas reales de clientes** (eso va al Excel operativo — versionado en `data/` de este repo desde que GitHub sustituye a Google Drive); **KB-T nunca incluye el repo completo**. Mezclarlas rompe seguridad, calidad del RAG y la memoria de DeepSeek.

## Inspiración y créditos

Este repo se construyó a partir de dos fuentes de inspiración directa del monitor, además de las referencias técnicas curadas en [`source_map.md`](program/02_REFERENCE/source_map.md) (orden de autoridad: doc oficial > código reproducible > libro/curso > paper > un LLM):

- **[`jackthony/IA-local`](https://github.com/jackthony/IA-local)** (lab propio, MIT): decisiones tipadas de 1 token con confianza calibrada (**Jev**, ver [`jev-pattern.md`](program/02_REFERENCE/jev-pattern.md)) y CI zero-trust (acciones fijadas por SHA, escáner de secretos).
- **[AI Agents: The Definitive Guide](https://github.com/Nicolepcx/ai-agents-the-definitive-guide)** (Nicolepcx, CH01–CH12): eje conceptual del programa ([`definitive-guide.md`](program/02_REFERENCE/definitive-guide.md)); se estudia como lectura guiada, no como verdad.

Otras referencias de ingeniería consultadas (se **leen**, no se copian; sin licencia = no se copia código): Anthropic *Building Effective Agents*, *12-Factor Agents*, *Cosmic Python*, OWASP GenAI, LangGraph, `walkinglabs/learn-harness-engineering`, `zhanymkanov/fastapi-best-practices`, `david-lev/pywa`, [`unclebob/swarm-forge`](https://github.com/unclebob/swarm-forge) (SwarmForge de Robert C. Martin: agentes con roles para el SDLC), entre otras. Lista completa, con licencia y «cuándo consultar», en [`source_map.md`](program/02_REFERENCE/source_map.md) y en la [wiki](https://github.com/jackthony/ai-business-assistant/wiki/Fuentes-y-referencias).

## Alcance: de un agente a multiagente

El producto **será multiagente, pero no desde el inicio** ([ADR-007](program/03_ARCHITECTURE/decisions/ADR-007-agente-unico-primero.md)). Primero un agente con RAG y tools confiables, medido y probado; el supervisor llega cuando haya métricas que justifiquen dividir responsabilidades.

| Fase | Semanas | Qué se construye | Se pasa a la siguiente cuando |
|---|---|---|---|
| Agente único | S4–S9 | Webhook, grafo LangGraph, RAG, tools (citas), safety y handoff humano como nodos/tools del **mismo** grafo | **HITO 2** (S9): 12/12 escenarios E2E, handoff real, latencia y contención medidas |
| Supervisor | S10 D2 del [plan](program/01_CURRICULUM/16_week_plan.md) | Router: clasificador por reglas primero, LLM solo para mensajes ambiguos; deriva a info / citas / checkout / safety | ≥13/15 mensajes ruteados bien, fallback a LLM, trazas del ruteo |
| Multitenant | S10 D3 – S11 del plan | El mismo grafo atiende Hola Mujer y NeuraCode con prompt, namespace RAG y tools propios | 2 números, sin fugas de datos entre tenants |
| Evals y costo | S12, S15 | Evals por escenario; costo por conversación (FinOps) | decisión de seguir, fusionar o dividir agentes con datos |

Destino de diseño: [`architecture.md`](program/03_ARCHITECTURE/architecture.md) (supervisor → `info_agent`, `booking_agent`, `checkout_agent`, `safety_agent`).

**Por qué en este orden** (fuentes primarias, abiertas y verificadas el 2026-10-14):

- Anthropic, [*Building effective agents*](https://www.anthropic.com/engineering/building-effective-agents) (19-dic-2024): recomienda «finding the simplest solution possible, and only increasing complexity when needed»; el *routing* sirve cuando hay categorías distintas que conviene tratar por separado.
- Anthropic, [*How we built our multi-agent research system*](https://www.anthropic.com/engineering/multi-agent-research-system) (13-jun-2025): un orquestador con subagentes superó en 90,2 % a un solo agente en su evaluación interna, pero gasta «about 15× more tokens than chats» y es mal ajuste cuando los agentes necesitan compartir el mismo contexto. Es una medición propia de Anthropic sobre investigación, no sobre atención al cliente.
- LangChain, README de [`langgraph-supervisor-py`](https://github.com/langchain-ai/langgraph-supervisor-py) (MIT): su propio equipo recomienda hoy el patrón supervisor «directly via tools» en lugar de la librería, por el control sobre el contexto. Por eso S10 D2 del plan compara la librería contra el router propio.

**Lo que esto implica para nosotros** (inferencia del equipo, no cita): una conversación de WhatsApp es secuencial y comparte contexto entre pasos (info → cita → pago), así que el multiagente aquí es sobre todo **ruteo y aislamiento de responsabilidades** (seguridad clínica, pagos), no subagentes paralelos. El costo extra de tokens se mide en FinOps (S15) antes de aceptarlo. Lista completa de fuentes y su estado en [`source_map.md`](program/02_REFERENCE/source_map.md).

## Estructura

| Carpeta / archivo | Contenido |
|---|---|
| `program/00_PROJECT/` | **`current_status.md`** (leer siempre primero), `roadmap.md` (visión+alcance+fases), `operacion.md` (GitHub+ritmo), `roi_metrics.md` |
| `program/01_CURRICULUM/` | Plan de 16 semanas, backlog de Issues, inducción S5, pack de contexto, ruta de fundamentos y **`asignaciones/`** (un contrato determinista `S##_D#.md` + guía paso a paso por cada Issue de producción) |
| `program/02_REFERENCE/` | **`source_map.md`** (jerarquía de fuentes + kit de rescate), `stack-versiones.md` y guías por tema; `ejemplos/` con bloques guiados y tests |
| `program/03_ARCHITECTURE/` | Arquitectura objetivo, `estandares.md` + ADRs en `decisions/` |
| `program/04_DOMAIN/` | Dominio de negocio: Hola Mujer y NeuraCode |
| `program/05_EVALUATION/` | Rúbrica y expedientes individuales de alumnos |
| `src/` | Producto, por capas (`api`, `agents`, `channels`, `infrastructure`, `memory`, `models`, `rag`, `services`, `tools`). El núcleo no conoce canales ni HTTP (`estandares.md` §2) |
| `tests/` | Pruebas del producto y de la automatización (`tests/ops/`) |
| `configs/` | Configuración por negocio (tenant); ver `configs/README.md` |
| `data/conversaciones/` | Corpus de conversaciones anonimizado para few-shot, RAG y evals (hoy `sinteticas_v1.jsonl`; ver su `README.md`) |
| `tools/` | `onboarding/` (preparar tu carpeta y bitácora) y `asignaciones/` (verificadores de contratos) |
| `docs/` | `ARCHITECTURE.md` y `CONTEXT.md` |
| `wiki/` | Fuente de la wiki pública (se publica sola al llegar a `main`) |
| `bitacora/` | Bitácoras de los practicantes |
| `.github/` | Workflows, scripts de automatización (`scripts/`), roster del coach (`coach.json`) y plantillas |
| `.opencode/commands/` | Comandos del asistente de IA del practicante (`/asignacion`, `/paso`, `/pista`, `/revisar`, `/comprension`) |
| `AGENTS.md` (raíz) | Instrucciones para cualquier agente de IA (protocolo, coding, review, evaluación) |
| `GUIA_PRACTICANTE.md` · `GUIA_AGENTE.md` (raíz) | Guía del practicante y de su asistente de IA |

## Flujo de trabajo automatizado

**Calidad y reglas de rama (cada PR)**

| Workflow | Cuándo | Qué hace |
|---|---|---|
| `ci.yml` (job `calidad`) | cada PR | 4 puertas: `ruff` + `mypy` + `pytest` + `bandit`, más el chequeo de capas de `estandares.md`. `ruff` va con la misma versión que el hook local (`pyproject.toml` y `.pre-commit-config.yaml`) |
| `tbd-guardian.yml` (job `reglas-tbd`) | cada PR | base=`main`, rama `(tbd\|issue)-N-<slug>`, `Closes #N` y commits estrictos `tipo(alcance): verbo` (≤72 caracteres; tipos `feat\|fix\|docs\|test\|refactor\|ci\|chore\|perf\|style`). Más de 6 commits solo avisa. Exime a Dependabot |
| `tbd-enforcer.yml` | push + cada 6 h | revierte push directo a `main`, avisa PRs >4 días, cierra PRs >7 días y borra ramas muertas |
| `release.yml` | push de tag (`v*`, `hito-*`, `q*`) | publica el Release con notas generadas |

**Revisión del trabajo de los practicantes**

| Workflow | Cuándo | Qué hace |
|---|---|---|
| `pr-borrador.yml` | `git push` de una rama `issue-N-*` de un alumno | abre un PR en **borrador** con `Closes #N`, para que la revisión empiece desde el primer push |
| `revision-guiada.yml` | cada push del PR (también en borrador) | **Tutor** (DeepSeek): un comentario que se actualiza con archivos del contrato trabajados y faltantes, desvíos, siguiente paso y pistas. No da la solución. Solo alumnos |
| `revisor-contrato.yml` | cada PR de un alumno | **Compuerta del contrato**: (1) check determinista sin clave (archivos fuera de la sección 4, prohibiciones de la 9, dependencias nuevas, archivos y pruebas faltantes); (2) con el PR listo, un revisor **Claude** (`ANTHROPIC_API_KEY`) cuyo veredicto se valida en código. El script y los contratos se leen de `main`, no de la rama del PR. No aplica al monitor ni a bots |
| `ficha-pr.yml` | cada PR | ficha de revisión para el monitor (Issue que cierra, archivos, tests, criterios) |
| `deepseek-review.yml` | cada PR (opcional) | primer pase de review con DeepSeek si `DEEPSEEK_API_KEY` está definido; la nota final la decide el monitor |

**Ciclo semanal y seguimiento**

| Workflow | Cuándo | Qué hace |
|---|---|---|
| `crear-issues-semana.yml` | domingo 21:00 Lima + manual | crea el tracker y los Issues de la semana con lecturas y detalle de la sesión |
| `lectura-semanal.yml` | domingo 22:30 Lima + manual | publica la «Lectura guiada» de la semana en Discussions |
| `coach.yml` | lun–sáb: 08:00, 14:00 y 17:30 Lima | avisos que @mencionan al practicante en sus días de práctica: qué hacer y dónde mirar |
| `board-sync.yml` | eventos + cada noche | sincroniza el board (Alumno, Semana, Área, Complejidad, Status) con labels, assignees y PRs |
| `issue-on-create.yml` · `issue-orden.yml` | cada Issue nuevo | lo agregan al board y lo dejan completo: hito, tracker padre y bloqueos |
| `issue-closed.yml` | cada Issue cerrado | reabre solo el Issue que se cierra sin PR mergeado ni justificación |
| `digest-semanal.yml` | viernes 17:00 Lima | Issue resumen semanal por alumno, con commits por día |
| `informe-quincenal.yml` | dom–vie 21:00 Lima + manual | borrador del informe FPE por alumno desde commits, PRs e Issues reales; se refresca solo |

**Comunicación al equipo**

| Workflow | Cuándo | Qué hace |
|---|---|---|
| `equipo-avisa.yml` | un alumno abre, termina o mergea un PR | avisa al equipo con @menciones y, al mergear, desbloquea los Issues que dependían de ese |
| `discusion-avisa.yml` | discusión nueva | menciona al resto del equipo para que le llegue la notificación |
| `wiki-sync.yml` | push a `main` | publica `wiki/` en la wiki del repo |

`main` está protegido por el ruleset **`main protegido (TBD)`**: PR obligatorio, historial lineal (squash), sin force-push, checks requeridos `guardian-tbd / reglas-tbd` y `CI estricto / calidad` (sin PR se puede mergear solo si ambas están verdes) y push protection activo.

## Para el practicante (nuevo aquí)

Lee **`GUIA_PRACTICANTE.md`** (raíz): descarga y preparación, TBD paso a paso, dónde ves tus asignaciones (board + Assigned to me), tus fuentes por semana y cómo se generan tus informes (digest viernes + borrador FPE que se refresca cada noche).

Cada Issue de producción tiene un **contrato** en `program/01_CURRICULUM/asignaciones/` (`S##_D#.md`, con su guía paso a paso): fija el QUÉ (archivos, contrato, pruebas, criterio de «hecho»); el CÓMO es tuyo. Las pruebas se escriben **antes** que el código.

Resumen: `clone` → `pre-commit install` → tu Issue y su contrato → rama `issue-N-<slug>` → pruebas primero, commits chicos → `git push` (el robot abre tu PR en borrador y te deja la revisión guiada) → marca el PR como listo (corre la compuerta del contrato) → CI verde (4 puertas) → merge squash.

## Cómo usarlo con un asistente de IA (DeepSeek local, OpenCode)

1. Leer `program/00_PROJECT/current_status.md` **siempre**.
2. Cargar solo 2–3 archivos de la tarea en curso (nunca el repo completo).
3. El protocolo completo está en `AGENTS.md` (raíz del repo); el asistente de un practicante carga además `GUIA_AGENTE.md`. Con OpenCode, los comandos de `.opencode/commands/` lo encaminan por el contrato del día.
