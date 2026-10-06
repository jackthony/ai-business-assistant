# Gestión DevOps en GitHub — repo único

> **Decisión 2026-10-06:** todo vive en `jackthony/ai-business-assistant` (programa + producto). Transparencia total con los practicantes: ver el ciclo completo (planificar → Issue → branch → PR → CI → release) **es** el aprendizaje. Se aplican aquí las prácticas profesionales de GitHub (nivel certificación).

## Estructura

| Zona | Contenido | Desde |
|---|---|---|
| `00_`–`09_` | Programa: currículo, ADRs, evaluación, expedientes, source map | hoy |
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
| Project board (Todo / In Progress / Done) | ✅ [projects/3](https://github.com/users/jackthony/projects/3) — vinculado al repo, Issues #2–#4 dentro |
| Branch protection / rulesets en `main` | pendiente: requiere GitHub Pro para repo privado (o pasar a público en S16) |
| CI: `ruff` + `pytest` (mocks) + `mypy`/`bandit` recomendados | S4 D1 (Issue #01) |
| CD + environments con aprobación | S14 |
| Secret scanning / push protection / CodeQL | al pasar a público (S16) o con Pro |

## Trazabilidad (evidencia SENATI y liderazgo)

- **Issues** = backlog #01–#39; un Issue por sesión con criterios de aceptación.
- **PRs** = evidencia individual; cierran con `Closes #NN`; review del monitor (DeepSeek como reviewer).
- **Milestones** = HITO 1 / 2 / 3 / Demo final; **Releases** = uno por hito con notas.
- **Labels** = semana (`week:S5` se creará al usarla), `tipo:*`, `alumno:*`, `blocked`, `hito`, `senati`.

## Seguimiento del avance (híbrido)

**Automático (GitHub lo hace solo):**
- CI en cada PR: verde/rojo bloquea el merge (nadie avanza con tests rotos).
- Project board: el estado cambia solo al abrir/cerrar Issues y PRs (Projects → AI Business Assistant — SDLC).
- Milestones: barra de avance % por HITO.
- **Digest semanal** (`.github/workflows/digest-semanal.yml`): cada viernes crea un Issue resumen por alumno (PRs movidos, Issues abiertos). Se prueba con *Actions → Digest semanal → Run workflow*.
- Dependabot y alertas de seguridad: solas.

**Del monitor (seguimiento y rumbo, ~30 min el Día 3):**
- Revisar el digest + los PRs de la semana (DeepSeek como revisor técnico primero): comprensión, calidad y criterios del Issue.
- Nota preliminar en `EVALUACION` del Excel (se calcula sola).
- Dar feedback y desbloquear; 1–2 líneas por alumno en su expediente.
- Quincenal: escuchar la sustentación y marcar "Revisado por monitor" en `SEGUIMIENTO_QUINCENAL`.

**Del alumno:** registro diario, **informe quincenal SENATI**, sustentación y evidencia en PRs.

Regla: la automatización dice **dónde** mirar; el monitor decide **cómo va**.

## Acceso

- Practicantes: colaboradores con push vía PR (branch corta por Issue; `main` protegido desde que el plan lo permita).
- Todo visible para el equipo (transparencia deliberada).
- **Nunca entra al repo:** tokens/secretos (GitHub Secrets), datos reales de clientes (fixtures anonimizados), ni notas numéricas (Ley 29733 — viven en el Excel de Drive).

## Fuera de GitHub (Google Drive — solo distribución)

| Artefacto | Por qué |
|---|---|
| Excel EVALUABLE (notas numéricas) | Binario editado a mano cada semana |
| PDFs para leer en celular | Distribución a alumnos sin fricción |
| Informes SENATI Word/PDF | Entregables formales a la institución |

Regla: si algo cambia en GitHub y tiene copia en Drive, la copia se regenera; nunca se edita la copia.

## Acciones pendientes

1. Project board: ✅ creado ([projects/3](https://github.com/users/jackthony/projects/3)); agregar cada semana los Issues nuevos.
2. Publicar el bloque final de sesiones S13–S16 (`16_week_plan.md`).
3. S4: `src/`, CI, `docs/CONTEXT.md` y `docs/ARCHITECTURE.md` dentro de este mismo repo (Issue #2).
4. Agregar a Allan, Pilar y Josue como colaboradores cuando se tengan sus usuarios de GitHub.
5. Digest semanal: ✅ probado en vivo (Issue #1); corre solo cada viernes.
