# Gestión DevOps del programa en GitHub

> Todo lo vivo del programa se gestiona como un equipo de ingeniería real: GitHub para texto, código y trazabilidad; Google Drive solo para lo que GitHub no maneja bien.

## Repositorios

| Repo | Contenido | Visibilidad | Acceso alumnos |
|---|---|---|---|
| `senati-ai-agents-context` | Currículo, ADRs, rúbrica, expedientes, guías | Privado | Solo lectura |
| `ai-business-assistant` (se crea en S4) | Código del producto | Privado | Escritura vía PR (`main` protegido) |

## Trazabilidad (SENATI y liderazgo)

- **Issues** = backlog #01–#39; un Issue por sesión con criterios de aceptación.
- **Project (kanban)** = planificación semanal: Todo / In Progress / Review / Done.
- **Milestones** = HITO 1 (S6), HITO 2 (S9), HITO 3 (S11), Demo final (S16).
- **Labels** = `week:S5`, `type:feature|bug|docs`, `alumno:allan|pilar|josue`, `blocked`.
- **PRs** = evidencia individual: plantilla de PR + review del monitor (DeepSeek como reviewer); cierran Issues con `Closes #NN`.

## Protección y calidad (TBD — ADR-006)

- `main` protegido: sin push directo; PR obligatorio; CI verde obligatorio; 1 review.
- CI en Actions desde S4 D1: `ruff` + `pytest` (mocks, sin tokens); `mypy`/`bandit` recomendados.
- CD desde S14: deploy al pasar `main` (webhook 24/7).
- **Releases** = un release por HITO con notas (evidencia directa para informes SENATI).

## Seguridad

- Secretos en GitHub Secrets (nunca en el repo); environments para producción.
- Dependabot activo en el repo de código; CodeQL opcional.
- Prohibido subir datos reales de clientes a Issues/PRs/repos: fixtures anonimizados.

## Qué vive fuera de GitHub (Google Drive)

| Artefacto | Por qué |
|---|---|
| Excel EVALUABLE (notas) | Binario editado a mano cada semana; git no diffea bien binarios |
| PDFs para leer en celular | Distribución a alumnos sin fricción |
| Informes SENATI Word/PDF | Entregables formales a la institución |

Regla: si algo cambia en GitHub y tiene copia en Drive, la copia se regenera; nunca se edita la copia.

## Acciones pendientes

1. Crear `ai-business-assistant` (tras aprobar la v2) con protecciones, plantillas de Issue/PR, CI y Project.
2. Agregar a los 3 practicantes como colaboradores cuando se tengan sus usuarios de GitHub (lectura al repo de contexto; escritura al de código).
3. Subir a `05_EVALUATION/` el acta/PDF de cada quincena cerrada.
