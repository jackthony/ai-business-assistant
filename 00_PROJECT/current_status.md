# Estatus del proyecto — 2026-10-06

- **Programa:** HealthTech Software & AI — SENATI 2026 (ciclo 3)
- **Fase:** Semana 4 — Nace el producto (Issues #2–#4) · Q1 entregado por los alumnos; Q2 en curso
- **Repo único:** https://github.com/jackthony/ai-business-assistant
- **Board:** https://github.com/jackthony/projects/3
- **Issue actual:** #2 (setup FastAPI + CI)

## Practicantes

- Allan Zerpa (zerpaallan@gmail.com)
- Pilar Aguilar (pilaraguilar.2502@gmail.com) — acceso confirmado al plan maestro e informe quincenal
- Josue Marreros (josuea.marrerosplasencia@gmail.com)

## Estado por área

| Área | Estado |
|---|---|
| Plan 16 semanas (48 sesiones) | ✅ v2 completo en `01_CURRICULUM/16_week_plan.md` |
| GitHub: plantillas Issue/PR, CODEOWNERS, labels, milestones, Dependabot | ✅ aplicado |
| Board + digest semanal | ✅ [projects/3](https://github.com/jackthony/projects/3); digest probado (Issue #1), corre cada viernes |
| CI/CD | ⏳ CI entra con el Issue #2 (S4 D1); CD + environments en S14 |
| Evaluación | ✅ Excel EVALUABLE (16×3, fórmulas verificadas); rúbrica y expedientes en `05_EVALUATION/` |
| Drive de distribución | ✅ `ciclo-3-pilar-alan-josue/SENATI-2026-GoogleDrive/` listo para arrastrar |
| Material de alumnos | ✅ guía PDF (Vasilyev, MIT); cursos verificados en `01_CURRICULUM/cursos_de_refuerzo.md` |
| Decisiones | ✅ 10 ADRs (`03_ARCHITECTURE/decisions/`) + `02_REFERENCE/source_map.md` curado |
| Código producto (`src/`) | ⏳ arranca con el Issue #2 |
| Branch protection/rulesets | ⏳ requiere GitHub Pro o repo público (S16) |

## Inventario de tareas (todas)

### Producto (GitHub, board projects/3)
- **Esta semana:** #2 Setup + CI · #3 Webhook Meta · #4 Sender + demo E2E + cierre Q2
- **Backlog S5–S16:** `01_CURRICULUM/issues_backlog.md` (los Issues se crean cada lunes; referencia estable por título `[S## D#]`)
- **Hitos:** HITO 1 (S6) · HITO 2 (S9) · HITO 3 (S12) · Demo final (S16)

### Gestión (creadas 2026-10-06 en el board)
- **#5** Colaboradores: agregar a Allan/Pilar/Josue el **2026-10-07**
- **#6** PEA SINFO: mapear códigos al recibirlos
- **#7** Ley 29733: validar con abogado (no tocar datos reales aún)
- **#8** Branch protection: activar cuando el plan lo permita

### Rutina semanal (no son Issues)
- **Lunes:** crear en el board los Issues de la semana.
- **Viernes (Día 3):** leer digest + revisar PRs (DeepSeek reviewer) + nota preliminar en Excel + escuchar la sustentación quincenal (el informe lo redacta el alumno).

## Decisiones recientes (resumen)

- 10 ADRs vigentes: FastAPI · LangGraph · WhatsApp Cloud API · ChromaDB · memoria Sqlite→Postgres · TBD · agente único primero · DeepSeek local first · harness/seguridad N1/N2/N3 · gobernanza de frameworks.
- Repo único `ai-business-assistant` con transparencia total (ver `00_PROJECT/github_devops.md`).
- Nota semanal = **preliminar/formativa**; la oficial se consolida por quincena.
- Guía MIT (Vasilyev) adoptada como apoyo; cursos Udemy verificados; malla Java archivada; Excel migrado a `(EVALUABLE).xlsx`.

## Riesgos abiertos

- PEA SINFO pendiente (bloquea columnas del seguimiento quincenal).
- Ley 29733 sin validar: prohibido tocar datos reales de clientes.
- `main` sin protección hasta GitHub Pro o repo público (S16).
- Operación actual ManyChat + n8n no cumple el objetivo: el reemplazo arranca en S4.

## Próximo paso

1. Mañana 2026-10-07: agregar colaboradores (#5).
2. Cerrar Issues #2–#4 (S4) con demo E2E y cierre Q2.
3. Reunión tarea por tarea: elegir la primera del inventario y detallarla.
