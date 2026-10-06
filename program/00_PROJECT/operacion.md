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
| Ruleset `main protegido (TBD)`: PR obligatorio, squash/lineal, sin force-push, check `guardian-tbd / reglas-tbd` + push protection | ✅ activo |
| Guardianes TBD por workflow (`tbd-guardian` / `tbd-enforcer`) | ✅ en operación |
| CI estricto: `ruff` + `mypy` + `pytest` + `bandit` (4 puertas, `.github/workflows/ci.yml`) | ✅ montado; entra con el Issue #2 |
| Pre-commit local (`.pre-commit-config.yaml`: ruff + formateo + hooks base) | ✅ en raíz; cada practicante corre `pre-commit install` |
| CD + environments con aprobación | S14 |
| CodeQL | S16 (opcional) |

### Trazabilidad (evidencia SENATI)

- **Issues** = backlog #01–#39 (un Issue por sesión con criterios de aceptación; el workflow `crear-issues-semana` los crea cada martes).
- **PRs** = evidencia individual; cierran con `Closes #NN`; review del monitor (DeepSeek como reviewer).
- **Milestones** = hitos; **Releases** = uno por hito con notas.

### Automatizaciones (workflows)

| Workflow | Cuándo | Qué hace |
|---|---|---|
| `ci.yml` | cada PR | 4 puertas: ruff, mypy, pytest, bandit |
| `tbd-guardian.yml` | cada PR | base=`main`, rama `(tbd\|issue)-N-<slug>`, `Closes #N`, ≤6 commits |
| `tbd-enforcer.yml` | push + cada 6 h | revierte push directo a `main`, cierra PRs >48 h, borra ramas muertas |
| `digest-semanal.yml` | viernes | Issue resumen semanal por alumno (✅ probado) |
| `informe-quincenal.yml` | jueves noche + manual | borrador FPE por alumno desde commits/PRs/Issues (✅ #11–#13 creados) |
| `crear-issues-semana.yml` | martes + manual | crea los Issues de la semana desde el backlog y los agrega al board (✅ probado) |

## Seguimiento del avance (híbrido)

**Automático:** CI bloquea merge en rojo · el board cambia solo con Issues/PRs · milestones muestran % · digest e informe se generan solos.

**Del monitor (~30 min el Día 3):** revisar digest + PRs (DeepSeek primero) → nota preliminar en Excel → feedback y desbloqueo → 1–2 líneas por alumno en su expediente. Quincenal: escuchar la sustentación y marcar "Revisado por monitor".

**Del alumno:** registro diario, informe quincenal SENATI, sustentación y evidencia en PRs.

Regla: la automatización dice **dónde** mirar; el monitor decide **cómo va**.

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

- **Día 3 (viernes):** 1) llenar las 3 filas semanales en el Excel `EVALUACION` (30 min, criterios 1–5) · 2) revisar PRs (DeepSeek como reviewer, `AGENTS.md` §Review) · 3) anotar patrones en `program/05_EVALUATION/students/` · 4) actualizar `current_status.md`.

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
