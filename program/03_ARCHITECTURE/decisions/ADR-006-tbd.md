# ADR-006: Trunk-Based Development y un solo repo de producto

- **Fecha:** 2026-10-06 (revisado 2026-10-06: se relaja a "TBD de aprendizaje")
- **Estado:** aceptada

## Contexto

3 practicantes construyen un mismo producto multitenant. SENATI requiere evidencia individual.

## Problema

¿Un repo por alumno o un repo compartido? ¿Qué estrategia de branching?

## Opciones

1. 3 repos de alumno sobre template común.
2. 1 repo producto + branches cortas por Issue + PRs.
3. GitFlow con branches largas.

## Decisión

Opción 2. TBD real: branch `issue-NN-slug` desde `main`, vida de horas/pocos días, PR con review y merge. La evidencia individual son los PRs y commits firmados por cada alumno.

## Revisión 2026-10-06 — alternativas investigadas (fuentes: docs.github.com GitHub Flow · trunkbaseddevelopment.com · Atlassian Gitflow)

| Modelo | Qué es | Veredicto |
|---|---|---|
| **TBD estricto (lo anterior)** | ≤6 commits, PR se cierra a las 48 h, ramas de horas | ❌ Demasiada fricción para practicantes con 3 días/semana (un PR de mié→vie ya pasa 48 h) |
| **GitHub Flow** | Rama corta por cambio → commit/push **libre** → PR (draft si quieres feedback temprano) → merge → borrar rama | ✅ Es prácticamente TBD sin los límites auto-impuestos; la única diferencia real con TBD es desde dónde se publica el release (para nosotros: release from trunk, S14) |
| **GitFlow** | develop/feature/release/hotfix, branches long-lived | ❌ Pensado para releases versionados de equipos grandes; sobrecarga para 4 personas y contradice "main siempre desplegable" |
| **Commit directo a trunk** | TBD de equipos muy pequeños | ❌ Perderíamos los PRs = evidencia individual SENATI y la revisión |

**Decisión revisada — "TBD de aprendizaje" (GitHub Flow con ramas cortas):**

- **Reglas duras (las verifica `tbd-guardian`):** branch `(tbd|issue)-N-<slug>` desde `main` · `Closes #N` en el PR · mensajes de commit en convención · CI verde (checks obligatorios).
- **Guías, no bloqueos:** sin límite de commits (el squash une todo igual) · el PR puede vivir hasta **7 días** (`tbd-enforcer` avisa a los 4 días) · push directo a `main` se revierte solo para los practicantes.
- **Cómo suben sus commits (mecánica GitHub Flow):** `git pull origin main` → rama por Issue → `git add/commit/push` **cuantas veces quieran** (cada push corre el CI y respalda su trabajo) → PR (draft si aún no está listo) → responden el review con más commits → squash merge → la rama muere sola.
- Rigor creciente: S4–S6 flexibles (aprendizaje del flujo); desde S7 se exige PR ≤3 días y se evalúa lead time (DORA, ver `operacion.md`).

## Consecuencias

- `main` siempre desplegable; integración frecuente.
- Branches viven máximo una semana (7 días); el cierre de PR a los 4 días es un recordatorio, no un castigo.
- El template inicial evita 3 arquitecturas incompatibles.
