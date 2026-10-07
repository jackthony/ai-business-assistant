# Operación — gestión GitHub + ritmo del líder

> Todo vive en `jackthony/ai-business-assistant` (**público** desde 2026-10-06): programa + producto. Transparencia total: ver el ciclo completo (planificar → Issue → branch → PR → CI → release) **es** el aprendizaje. Estado siempre vigente: `program/00_PROJECT/current_status.md`.

## Gestión en GitHub

| Práctica | Estado |
|---|---|
| Plantillas de Issue y PR con checklist | ✅ aplicadas |
| CODEOWNERS (review del monitor) | ✅ aplicada |
| Labels (`tipo:*`, `alumno:*`, `week:S*`, `blocked`, `hito`, `senati`) | ✅ aplicadas |
| Milestones: HITO 1 (S6) · HITO 2 (S9) · HITO 3 (S12) · Demo final (S16) | ✅ aplicados |
| Dependabot (pip + Actions) | ✅ aplicado |
| Board [projects/3](https://github.com/users/jackthony/projects/3) con campos Status/Semana/Alumno/Area/Complejidad — **público** (practicantes solo lectura), enlazado al repo | ✅ activo |
| Ruleset `main protegido (TBD)`: PR obligatorio, squash/lineal, sin force-push, required checks **por nombre de job**: `reglas-tbd` **y** `calidad` (⚙️ NO usar "workflow / job": con ese formato quedan "Expected" para siempre) + push protection | ✅ activo |

## DevSecOps — toda la seguridad en GitHub (sin Google Drive)

| Capa | Qué está activo | Dónde se ve |
|---|---|---|
| Calidad | 4 puertas en CI (ruff, mypy, pytest, bandit) — check obligatorio para mergear | Actions → `CI estricto` |
| Reglas TBD | `tbd-guardian` (rama/`Closes #N`/**commits convencionales**; cantidad de commits libre) + `tbd-enforcer` (revierte push directo, cierra PRs >7 días) | Actions |
| SAST | CodeQL (default setup, python + actions) — corre en PRs y en `main` | Security → Code scanning |
| Secretos | Secret scanning + **push protection** (bloquea el push si detecta un token) | Security → Secret scanning |
| Dependencias | Dependabot alerts + Dependabot updates (pip semanal, github-actions semanal) | Security → Dependabot |
| Suministro | `dependency-review-action` en cada PR (bloquea vulnerabilidades high) | Actions → `CI estricto` |
| Auditoría | Todo con `persist-credentials: false` y acciones pineadas por SHA | `.github/workflows/*.yml` |

### Secretos, tokens y acceso (política)

- **Environments (activados 2026-10-06):** `staging` (deploy desde ramas custom, libre) y `produccion` (solo `main`, **exige aprobación del monitor**) — los secrets `META_*` de producción van al environment `produccion` en S14.

- **Secrets del repo** (Settings → Secrets → Actions): `DEEPSEEK_API_KEY` (opcional, review en CI), `BOARD_PAT` (opcional, sync del board), `META_*` (desde que #16 esté listo). Nunca en código ni en docs: solo `.env.example` con los nombres.
- **GITHUB_TOKEN**: permisos mínimos declarados por workflow (`contents: read`, `pull-requests: write`, `issues: write` según necesita); nada más.
- **Acceso humano**: monitor = Admin; practicantes = Write pero `main` protegido (todo entra por PR con checks). Dependabot/CodeQL = apps autorizadas.
- **Datos reales del negocio (KB-A)**: por decisión del dueño (2026-10-06) **todo vive en GitHub** — el Excel operativo se versiona en `data/` de este repo (GitHub sustituye a Google Drive). Regla de higiene que se mantiene: en **código y tests** solo fixtures anonimizados; los nombres reales de clientes no se meten en datos de prueba.
| Guardianes TBD por workflow (`tbd-guardian` / `tbd-enforcer`) | ✅ en operación |
| CI estricto: `ruff` + `mypy` + `pytest` + `bandit` (4 puertas, `.github/workflows/ci.yml`) | ✅ montado; entra con el Issue #2 |
| Pre-commit local (`.pre-commit-config.yaml`: ruff + formateo + hooks base) | ✅ en raíz; cada practicante corre `pre-commit install` |
| CD + environments con aprobación | S14 |
| CodeQL | S16 (opcional) |

### Trazabilidad (evidencia SENATI)

#### Estructura de Projects (todo conectado, nada suelto)
- **Trackers con sub-issues:** cada semana tiene su tracker (`[S##] Semana N — tracker: …`) y los 3 Issues del día cuelgan como sub-issues (#25 → #2/#3/#4 y siguientes automáticos). Trackers permanentes: **#26 Gestión** (→#5–#8/#10/#16) y **#27 Informes FPE** por quincena (→#11–#13).
- **Milestones:** HITO 1 (S6), HITO 2 (S9), HITO 3 (S12), Demo final (S16) — asignados automáticamente según la semana.
- **Views del board:** Tabla por Semana · Board por Estado · Roadmap (+ la vista original).
- **Labels:** `tipo:` (feature/bug/docs/infra/gestion) · `alumno:` (allan/pilar/josue) · `week:S##` · `hito` · `senati` · flujo pull (`disponible`/`apoyo`/`propuesta`).
- Regla: todo Issue nuevo lleva tracker padre, milestone y label — si algo queda suelto, el monitor lo reubica en su revisión.

- **Issues** = backlog #01–#39 (un Issue por sesión con criterios de aceptación; el workflow `crear-issues-semana` los crea cada domingo por la noche, listos para el lunes de Josue y el miércoles de Pilar).
- **PRs** = evidencia individual; cierran con `Closes #NN`; review del monitor (DeepSeek como reviewer).
- **Milestones** = hitos; **Releases** = uno por hito con notas.

### Automatizaciones (workflows)

| Workflow | Cuándo | Qué hace |
|---|---|---|
| `ci.yml` | cada PR | 4 puertas: ruff, mypy, pytest, bandit + 5.º chequeo determinista: el núcleo no importa canales/servicios/HTTP (`estandares.md` §2) |
| `tbd-guardian.yml` | cada PR | base=`main`, rama `(tbd\|issue)-N-<slug>`, `Closes #N`, commits convencionales (cantidad libre) |
| `ficha-pr.yml` | cada PR | ficha de revisión automática (Issue que cierra, archivos, tests, criterios) + checkbox mecánico de estándares (capas, secretos, src sin tests) |
| `release.yml` | push de tag (`v*`/`hito-*`/`q*`) | publica el Release con notas generadas — tags del plan: `hito-1` (S6), `q4` (S8), `hito-2` (S9), `q5` (S10), `hito-3` (S12), `q6` (S12), `v1.0` (S16) |
| `issue-on-create.yml` | cada Issue nuevo | lo agrega al board con `Semana` (del título `[S## D#]`) y `Alumno` (del assignee) — soporta el flujo pull |
| `issue-closed.yml` | cada Issue cerrado | los Issues no se cierran sin terminar (PR mergeado) ni justificar: si un practicante cierra sin eso, se **reabre solo** |
| `deepseek-review.yml` | cada PR | primer pase de review con DeepSeek API (activo con `DEEPSEEK_API_KEY`): revisa TBD, CI, arquitectura y **estándares** (`estandares.md`); la nota final la decide el monitor |
| `tbd-enforcer.yml` | push + cada 6 h | revierte push directo a `main`, avisa PRs >4 días y cierra >7 días, borra ramas muertas |
| `digest-semanal.yml` | viernes | Issue resumen semanal por alumno (✅ probado) |
| `informe-quincenal.yml` | cada noche dom–vie (21:00 Lima) + manual | borrador FPE por alumno desde commits/PRs/Issues (✅ #11–#13 creados; se refresca solo) |
| `crear-issues-semana.yml` | domingo noche (21:00 Lima) + manual | crea el **tracker semanal** `[S##]` + los Issues del día `[S## D#]` (lecturas + detalle + pack + estándares), los enlaza como **sub-issues** del tracker, les pone **milestone** por hito (S4–6→HITO 1, S7–9→HITO 2, S10–12→HITO 3, S13–16→Demo) y el board los sincroniza solo |

## Seguimiento del avance (híbrido)

**Automático:** CI bloquea merge en rojo · el board cambia solo con Issues/PRs · milestones muestran % · digest e informe se generan solos.

**Del monitor (~30 min al cierre de cada alumno):** revisar digest + PRs (DeepSeek primero) → nota preliminar en Excel → feedback y desbloqueo → 1–2 líneas por alumno en su expediente. Quincenal: escuchar la sustentación y marcar "Revisado por monitor".

**Del alumno:** registro diario, informe quincenal SENATI, sustentación y evidencia en PRs (guía completa: `GUIA_PRACTICANTE.md` en la raíz).

Regla: la automatización dice **dónde** mirar; el monitor decide **cómo va**.

## Métricas DORA (liderazgo)

Miden la salud del delivery del equipo, no a personas.

| Métrica | Definición | En este repo | Meta | Activa |
|---|---|---|---|---|
| Deployment Frequency | despliegues a producción por periodo | releases publicadas | ≥1 por quincena | S14 (con CD) |
| Lead Time for Changes | primer commit → producción | proxy: PR abierto → merge | **S4–S6: <3 días · S7+: <48 h** (rigor creciente, ADR-006) | desde S4 |
| Change Failure Rate | % de cambios que degradan el servicio | proxy: reverts + PRs abandonados sin merge | <15% | desde S4 |
| Time to Restore Service | caída → recuperación | incidentes en producción | <1 h | S14+ |

- Los **proxies se calculan solos** en cada `digest-semanal` (bloque «DORA» al inicio del Issue).
- DORA plenas (DF/MTTR reales) desde que exista CD (S14). Si el cliente pregunta por resultados, se exponen en `roi_metrics.md`.

## Acceso y límites

- Practicantes: colaboradores con push vía PR (rama corta por Issue); los guardianes hacen cumplir el flujo.
- **Nunca entra al repo:** tokens/secretos (GitHub Secrets), datos reales de clientes (fixtures anonimizados), ni notas numéricas (Ley 29733 — viven en el Excel de Drive).

## Fuera de GitHub (Google Drive — solo distribución)

- Excel EVALUABLE (notas numéricas), PDFs para celular, informes SENATI Word/PDF.
- Si algo cambia en GitHub y tiene copia en Drive, la copia se regenera; nunca se edita la copia.

## Ritmo operativo del líder

### Ciclo diario (3 días/semana)

- Arranque (10 min): cada practicante dice qué hará hoy, qué espera y qué le bloquea.
- El día se ejecuta contra **un Issue** del backlog, no contra "avanzar".
- Cierre: commit/PR con evidencia y actualización del Issue.

### Ciclo semanal

- **Cierre de cada alumno en su último día de práctica (Josue: miércoles; Pilar y Allan: viernes):** 1) llenar sus 3 filas semanales en el Excel `EVALUACION` (30 min, criterios 1–5) · 2) revisar PRs (DeepSeek como reviewer, `AGENTS.md` §Review) · 3) anotar patrones en `program/05_EVALUATION/students/` · 4) actualizar `current_status.md`.
- **Viernes:** leer el digest semanal (commits por día + DORA) y confirmar que los borradores FPE estén listos para la sustentación del sábado.

### Ciclo quincenal

- El **alumno** sustenta la tarea más significativa y presenta su **informe quincenal SENATI** (FPE CNIU-108): por qué eligió la tarea, proceso, equipos/herramientas, seguridad/ATS y diagrama; el monitor escucha, da rumbo, firma y marca "Revisado por monitor".
- Revisar `SEGUIMIENTO_QUINCENAL` del Excel y ajustar el plan si un tema no quedó sólido.
- **Automatizado:** `informe-quincenal` crea/refresca 1 Issue-borrador por alumno con el registro semanal armado desde commits/PRs/Issues reales (✅ #11 Allan, #12 Pilar, #13 Josue). El alumno completa horas/ATS/reflexión y lo pasa al Word FPE; su expediente en `students/` es el respaldo.

### Reglas del líder

1. No resolver el bloqueo por el practicante: dar pistas, exigir evidencia, dejar que cierre.
2. No cambiar el plan ni el stack a mitad de semana; toda decisión va a un ADR.
3. La evaluación se llena con evidencia (commits/PRs/demos), no con percepción.
4. Si el monitor no sabe algo: decirlo. Modelar la regla de evidencia (fuente primaria > opinión).

### Trampas de primera vez

- Prometer más alcance del que 3 practicantes pueden sostener.
- Adoptar cada framework nuevo que suena mejor (ver ADR-010).
- Hacer el trabajo "porque es más rápido" — a los 2 meses no saben nada.
- Confundir el conocimiento del negocio (KB-A) con el del programa (KB-P).
