# Estatus del proyecto — 2026-10-06

- **Programa:** HealthTech Software & AI — SENATI 2026 (ciclo 3)
- **Fase:** Semana 4 — Producto (Issues #2–#4) con **cierre S3 acelerado integrado** · Q1 entregado; Q2 en curso
- **Informe FPE (CNIU-108) revisado:** registro diario con horas (LUN–SÁB + total), PEA de 151 operaciones (pendiente SINFO, Issue #6) y tarea significativa con proceso/herramientas/seguridad (ATS)/diagrama + firma del monitor. La demo del viernes alimenta ese informe.
- **Repo único:** https://github.com/jackthony/ai-business-assistant
- **Board:** https://github.com/jackthony/projects/3
- **Issue actual:** #2 (setup FastAPI + CI)

## Practicantes

- Allan Zerpa ((privado))
- Pilar Aguilar ((privado)) — acceso confirmado al plan maestro e informe quincenal
- Josue Marreros ((privado))

**Distribución de carga:** Josue = alta + mentor interno (primero le explica al monitor y luego apoya a Allan y Pilar); Allan y Pilar = media. La asignación se gestiona con los campos `Alumno` y `Complejidad` del board y los labels `complejidad:*`.

## Estado por área

| Área | Estado |
|---|---|
| Plan 16 semanas (48 sesiones) | ✅ v2 completo en `program/01_CURRICULUM/16_week_plan.md` |
| GitHub: plantillas Issue/PR, CODEOWNERS, labels, milestones, Dependabot | ✅ aplicado |
| Board + digest semanal | ✅ [projects/3](https://github.com/jackthony/projects/3); digest probado (Issue #1), corre cada viernes |
| CI/CD | ⏳ CI entra con el Issue #2 (S4 D1); CD + environments en S14 |
| Evaluación | ✅ Excel EVALUABLE (16×3, fórmulas verificadas); rúbrica y expedientes en `program/05_EVALUATION/` |
| Drive de distribución | ✅ `ciclo-3-pilar-alan-josue/SENATI-2026-GoogleDrive/` listo para arrastrar |
| Material de alumnos | ✅ guía PDF (Vasilyev, MIT); cursos verificados en `program/01_CURRICULUM/cursos_de_refuerzo.md` |
| Decisiones | ✅ 10 ADRs (`program/03_ARCHITECTURE/decisions/`) + `program/02_REFERENCE/source_map.md` curado |
| Código producto (`src/`) | ⏳ arranca con el Issue #2 |
| Branch protection/rulesets nativos | ✅ suplidos por guardianes TBD por workflow (`tbd-guardian` + `tbd-enforcer`); rulesets quedan para Pro/público (S16) |

## Inventario de tareas (todas)

### Producto (GitHub, board projects/3)
- **Esta semana:** #2 Setup + CI · #3 Webhook Meta · #4 Sender + demo E2E + cierre Q2
- **Backlog S5–S16:** `program/01_CURRICULUM/issues_backlog.md` (los Issues se crean cada lunes; referencia estable por título `[S## D#]`)
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
- Repo único `ai-business-assistant` con transparencia total (ver `program/00_PROJECT/github_devops.md`).
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
