# ai-business-assistant — Programa SENATI 2026 + Producto

Repositorio único (**público** desde 2026-10-06): **programa de prácticas** (currículo, evaluación, gestión) **+ producto** (`src/` desde S4) — HealthTech Software & AI · SENATI 2026 · ciclo 3 (Allan, Pilar y Josue). Sin correos, secretos ni datos reales de clientes.

- **Board de seguimiento (público, solo lectura para practicantes):** https://github.com/users/jackthony/projects/3 (campos Status, Semana, Alumno, Area, Complejidad) — también en la pestaña Projects del repo
- **Estado siempre vigente:** `program/00_PROJECT/current_status.md`

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

## Estructura

| Carpeta | Contenido |
|---|---|
| `program/00_PROJECT/` | **`current_status.md`** (leer siempre primero), `roadmap.md` (visión+alcance+fases), `operacion.md` (GitHub+ritmo) |
| `program/01_CURRICULUM/` | Syllabus, plan de 16 semanas y backlog de Issues #01–#39 |
| `program/02_REFERENCE/` | **`source_map.md`** (jerarquía de fuentes + kit de rescate) y guías por tema |
| `program/03_ARCHITECTURE/` | Arquitectura objetivo + ADRs en `decisions/` |
| `program/04_DOMAIN/` | Dominio de negocio: Hola Mujer y NeuraCode |
| `program/05_EVALUATION/` | Rúbrica y expedientes individuales de alumnos |
| `AGENTS.md` (raíz) | Instrucciones para cualquier agente de IA (protocolo, coding, review, evaluación) |

## Flujo de trabajo automatizado

| Workflow | Cuándo | Qué hace |
|---|---|---|
| `ci.yml` | cada PR | 4 puertas: `ruff` + `mypy` + `pytest` + `bandit` (job `calidad`) |
| `tbd-guardian.yml` | cada PR | TBD de aprendizaje: base=`main`, rama `(tbd\|issue)-N-<slug>`, `Closes #N`, commits convencionales (cantidad libre) |
| `ficha-pr.yml` | cada PR | ficha de revisión automática para el monitor (Issue que cierra, archivos, tests, criterios) |
| `deepseek-review.yml` | cada PR (opcional) | primer pase de review con DeepSeek API si `DEEPSEEK_API_KEY` está definido; la nota final la decide el monitor |
| `tbd-enforcer.yml` | push + cada 6 h | revierte push directo a `main`, avisa PRs >4 días y cierra >7 días, borra ramas muertas |
| `crear-issues-semana.yml` | domingo noche (21:00 Lima) + manual | crea los Issues de la semana con lecturas + detalle de la sesión |
| `digest-semanal.yml` | viernes | Issue resumen semanal por alumno |
| `informe-quincenal.yml` | cada noche dom–vie (21:00 Lima) + manual | borrador del informe FPE por alumno desde commits/PRs/Issues reales (Issues #11–#13 ya creados; se refresca solo) |

`main` está protegido por el ruleset **`main protegido (TBD)`**: PR obligatorio, historial lineal (squash), sin force-push, checks requeridos `guardian-tbd / reglas-tbd` y `CI estricto / calidad` (sin PR se puede mergear solo si ambas están verdes) y push protection activo.

## Para el practicante (nuevo aquí)

Lee **`GUIA_PRACTICANTE.md`** (raíz): descarga y preparación, TBD paso a paso, dónde ves tus asignaciones (board + Assigned to me), tus fuentes por semana y cómo se generan tus informes (digest viernes + borrador FPE que se refresca cada noche).

Resumen: `clone` → `pre-commit install` → tu Issue → rama `issue-N-<slug>` → commits chicos con tests → PR con `Closes #N` → CI verde (4 puertas) → merge squash.

## Cómo usarlo con DeepSeek local

1. Leer `program/00_PROJECT/current_status.md` **siempre**.
2. Cargar solo 2–3 archivos de la tarea en curso (nunca el repo completo).
3. El protocolo completo está en `AGENTS.md` (raíz del repo).
