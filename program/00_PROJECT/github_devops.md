# Gestión DevOps en GitHub — repo único

> **Decisión 2026-10-06:** todo vive en `jackthony/ai-business-assistant` (programa + producto). Transparencia total con los practicantes: ver el ciclo completo (planificar → Issue → branch → PR → CI → release) **es** el aprendizaje. Se aplican aquí las prácticas profesionales de GitHub (nivel certificación).

## Estructura

| Zona | Contenido | Desde |
|---|---|---|
| `program/00_PROJECT`–`05_EVALUATION` | Programa: currículo, ADRs, evaluación, expedientes, source map | hoy |
| `src/`, `tests/`, `configs/`, `data/`, `docs/` | Producto: FastAPI + LangGraph, configs por tenant, datasets KB-A | S4 |
| `.github/` | Plantillas de Issue/PR, CODEOWNERS, Dependabot, CI/CD | plantillas hoy · CI S4 · CD S14 |

## Prácticas aplicadas (estado)

| Práctica | Estado |
|---|---|
| Plantilla de Issue (formulario de tarea por sesión) | ✅ aplicada |
| Plantilla de PR con checklist (tests, sin secretos, evidencia) | ✅ aplicada |
| CODEOWNERS (review del monitor) | ✅ aplicada |
| Labels: `tipo:*`, `alumno:*`, `blocked`, `hito`, `senati` | ✅ aplicadas |
| Milestones: HITO 1 (S6), HITO 2 (S9), HITO 3 (S12), Demo final (S16) | ✅ aplicados |
| Dependabot (pip + GitHub Actions) | ✅ aplicado (actúa con el código en S4) |
| Project board | ✅ [projects/3](https://github.com/users/jackthony/projects/3) — campos Status/Semana/Alumno/Area/Complejidad; Issues #2–#4 dentro |
| Branch protection / rulesets en `main` | ✅ ruleset nativo `main protegido (TBD)` ACTIVO (repo público 2026-10-06): PR obligatorio, squash/lineal, sin force-push, check `guardian-tbd / reglas-tbd` + guardianes por workflow (`tbd-guardian`/`tbd-enforcer`) |
| CI estricto: `ruff` + `mypy` + `pytest` + `bandit` (4 puertas) | ✅ workflow montado (`.github/workflows/ci.yml`); se activa con el primer PR de código (los practicantes crean `src/` en el Issue #2) |
| Pre-commit local (ruff + formateo antes de cada commit) | ✅ `.pre-commit-config.yaml` en la raíz; cada practicante corre `pre-commit install` (Issue #2) |
| CD + environments con aprobación | S14 |
| Secret scanning / push protection / CodeQL | ✅ push protection activo (público); CodeQL en S16 (opcional) |

## Trazabilidad (evidencia SENATI y liderazgo)

- **Issues** = backlog #01–#39; un Issue por sesión con criterios de aceptación.
- **PRs** = evidencia individual; cierran con `Closes #NN`; review del monitor (DeepSeek como reviewer).
- **Milestones** = HITO 1 / 2 / 3 / Demo final; **Releases** = uno por hito con notas.
- **Labels** = semana (`week:S5` se creará al usarla), `tipo:*`, `alumno:*`, `blocked`, `hito`, `senati`.

## Seguimiento del avance (híbrido)

**Automático (GitHub lo hace solo):**
- CI en cada PR: verde/rojo bloquea el merge (nadie avanza con tests rotos).
- Project board: el estado cambia solo al abrir/cerrar Issues y PRs (board projects/3 con campos Status/Semana/Alumno/Area/Complejidad).
- Milestones: barra de avance % por HITO.
- **Digest semanal** (`.github/workflows/digest-semanal.yml`): ✅ probado (Issue #1); cada viernes crea un Issue resumen por alumno (PRs movidos, Issues abiertos).
- **Borradores de informe FPE** (`.github/workflows/informe-quincenal.yml`): jueves por la noche crea/refresca 1 Issue-borrador por alumno (ya generados: #11 Allan, #12 Pilar, #13 Josue).
- **Creación de Issues de la semana** (`.github/workflows/crear-issues-semana.yml`): el martes crea los 3 Issues de la semana desde `issues_backlog.md` y los agrega al board.
- Dependabot y alertas de seguridad: solas.

**Del monitor (seguimiento y rumbo, ~30 min el Día 3):**
- Revisar el digest + los PRs de la semana (DeepSeek como revisor técnico primero): comprensión, calidad y criterios del Issue.
- Nota preliminar en `EVALUACION` del Excel (se calcula sola).
- Dar feedback y desbloquear; 1–2 líneas por alumno en su expediente.
- Quincenal: escuchar la sustentación y marcar "Revisado por monitor" en `SEGUIMIENTO_QUINCENAL`.

**Del alumno:** registro diario, **informe quincenal SENATI**, sustentación y evidencia en PRs.

Regla: la automatización dice **dónde** mirar; el monitor decide **cómo va**.

## Acceso

- Practicantes: colaboradores con push vía PR (rama corta por Issue); los guardianes TBD por workflow hacen cumplir el flujo.
- Todo visible para el equipo (transparencia deliberada).
- **Nunca entra al repo:** tokens/secretos (GitHub Secrets), datos reales de clientes (fixtures anonimizados), ni notas numéricas (Ley 29733 — viven en el Excel de Drive).

## Fuera de GitHub (Google Drive — solo distribución)

| Artefacto | Por qué |
|---|---|
| Excel EVALUABLE (notas numéricas) | Binario editado a mano cada semana |
| PDFs para leer en celular | Distribución a alumnos sin fricción |
| Informes SENATI Word/PDF | Entregables formales a la institución |

Regla: si algo cambia en GitHub y tiene copia en Drive, la copia se regenera; nunca se edita la copia.

## Estado actual

- Board ✅ projects/3 con campos Semana/Alumno/Área/Complejidad; plan v2 ✅ en `16_week_plan.md`; digest semanal ✅ probado.
- Colaboradores ✅ invitados (Allan, Pilar, Josue); CI estricto ✅ montado; guardianes TBD ✅ en operación.
- S4 en curso: `src/` + `docs/CONTEXT.md`/`ARCHITECTURE.md` los crean los practicantes (Issue #2).
- Estado siempre vigente: `program/00_PROJECT/current_status.md`.
