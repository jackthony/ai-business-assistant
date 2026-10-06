# Estatus del proyecto — 2026-10-06

- **Programa:** HealthTech Software & AI — SENATI 2026 (ciclo 3)
- **Fase:** Semana 4 — Producto (Issues #2–#4) con **cierre S3 acelerado integrado** · Q1 entregado; Q2 en curso
- **Informe FPE (CNIU-108) revisado:** registro diario con horas (LUN–SÁB + total), PEA de 151 operaciones (pendiente SINFO, Issue #6) y tarea significativa con proceso/herramientas/seguridad (ATS)/diagrama + firma del monitor. La demo del viernes alimenta ese informe.
- **Repo único:** https://github.com/jackthony/ai-business-assistant
- **Board:** https://github.com/users/jackthony/projects/3 — público desde 2026-10-06 (practicantes solo lectura; lo ven en la pestaña Projects del repo). Asignaciones: campo `Alumno` + assignee en cada Issue (#2 Josue · #3 Pilar · #4 Allan · #11–#13 informes)
- **Issue actual:** #2 (setup FastAPI + CI) — hoy lo arranca Josue por la mañana; Allan y Pilar se suman por la noche

## Practicantes

- Allan Zerpa — GitHub `WhoAllan` (invitación pendiente de aceptar)
- Pilar Aguilar — GitHub `estefanyP-hub`; acceso confirmado al plan maestro e informe quincenal (invitación pendiente de aceptar)
- Josue Marreros — GitHub `adbon-dm1` ✅ aceptó la invitación (2026-10-06)

**Distribución de carga:** Josue = alta + mentor interno (primero le explica al monitor y luego apoya a Allan y Pilar); Allan y Pilar = media. La asignación se gestiona con los campos `Alumno` y `Complejidad` del board y los labels `complejidad:*`.

## Estado por área

| Área | Estado |
|---|---|
| Plan 16 semanas (48 sesiones) | ✅ v2 completo en `program/01_CURRICULUM/16_week_plan.md` |
| GitHub: plantillas Issue/PR, CODEOWNERS, labels, milestones, Dependabot | ✅ aplicado |
| Board + digest semanal | ✅ [projects/3](https://github.com/jackthony/projects/3); digest probado (Issue #1), corre cada viernes con commits por día + bloque DORA |
| CI/CD | ⏳ CI entra con el Issue #2 (S4 D1); CD + environments en S14 |
| Evaluación | ✅ Excel EVALUABLE (16×3, fórmulas verificadas); rúbrica y expedientes en `program/05_EVALUATION/` |
| Drive de distribución | ✅ `ciclo-3-pilar-alan-josue/SENATI-2026-GoogleDrive/` listo para arrastrar |
| Material de alumnos | ✅ guía PDF (Vasilyev, MIT); cursos verificados en `program/01_CURRICULUM/cursos_de_refuerzo.md` |
| Decisiones | ✅ 11 ADRs (`program/03_ARCHITECTURE/decisions/`) + `program/02_REFERENCE/source_map.md` curado |
| Código producto (`src/`) | ⏳ arranca con el Issue #2 |
| Branch protection / rulesets | ✅ repo público (2026-10-06) → ruleset `main protegido (TBD)` activo + guardianes por workflow (`tbd-guardian`/`tbd-enforcer`) + push protection |

## Inventario de tareas (todas)

### Producto (GitHub, board projects/3)
- **Esta semana:** #2 Setup + CI · #3 Webhook Meta · #4 Sender + demo E2E + cierre Q2
- **Backlog S5–S16:** `program/01_CURRICULUM/issues_backlog.md` (los Issues se crean cada lunes; referencia estable por título `[S## D#]`)
- **Hitos:** HITO 1 (S6) · HITO 2 (S9) · HITO 3 (S12) · Demo final (S16)

### Gestión (creadas 2026-10-06 en el board)
- **#5** 🔄 1/3 aceptada (Josue ✅); faltan Allan y Pilar
- **#6** PEA SINFO: mapear códigos al recibirlos
- **#7** Ley 29733: validar con abogado (no tocar datos reales aún)
- **#8** ✅ cerrado: ruleset nativo `main protegido (TBD)` activo (repo público) + guardianes TBD por workflow como refuerzo

### Rutina semanal (no son Issues)
- **Martes:** el workflow `crear-issues-semana` crea los Issues de la semana en el board desde el backlog; yo asigno el campo `Alumno`.
- **Viernes (Día 3):** leer digest + revisar PRs (DeepSeek reviewer) + nota preliminar en Excel + escuchar la sustentación quincenal (el informe lo redacta el alumno).

## Decisiones recientes (resumen)

- 11 ADRs vigentes: FastAPI · LangGraph · WhatsApp Cloud API · ChromaDB · memoria Sqlite→Postgres · TBD · agente único primero · DeepSeek local first · harness/seguridad N1/N2/N3 · gobernanza de frameworks · **canal-agnóstico (ADR-011)**.
- Repo único `ai-business-assistant` con transparencia total (ver `program/00_PROJECT/operacion.md`).
- Canal y Build/Buy/Integrate: se evaluará usar herramientas SaaS listas (**Kapso, n8n**) para capas no diferenciadoras según alcance; el núcleo (capa de agentes) sigue siendo propio (ADR-011). Decisión en el cierre B/B/I (S4 D3) y revisión en S10.
- Guía MIT (Vasilyev) adoptada como apoyo; cursos Udemy verificados; malla Java archivada; Excel migrado a `(EVALUABLE).xlsx`.
- Precios Meta archivados en `program/02_REFERENCE/meta-pricing.md` — **pendiente de validar** contra el panel Billing (el monitor indica precios y condiciones distintas desde el 1-oct-2026).
- Nota semanal = **preliminar/formativa**; la oficial se consolida por quincena.

## Riesgos abiertos

- PEA SINFO pendiente (bloquea columnas del seguimiento quincenal).
- Ley 29733 sin validar: prohibido tocar datos reales de clientes.
- `main` con rulesets nativos activos (repo público desde 2026-10-06; sin correos, secretos ni datos reales).
- Operación actual ManyChat + n8n no cumple el objetivo: el reemplazo arranca en S4.

## Próximo paso

1. Hoy 2026-10-06 (S4 D1): Josue arranca #2 por la mañana; Allan y Pilar se suman por la noche (Josue les explica lo avanzado).
2. Que Allan y Pilar acepten la invitación de GitHub (Josue ya aceptó ✅). **Al aceptar:** reasignar #3/#4 y #11/#12 (GitHub no permite asignar a usuarios sin aceptar).
3. Cerrar Issues #2–#4 (S4) con demo E2E y cierre Q2.
4. **Informe quincenal S3–S4: presentación sábado 10-oct** — cada alumno presenta su Issue como tarea significativa; los borradores automáticos ya existen (#11 Allan, #12 Pilar, #13 Josue) y se refrescan con cada corrida de `informe-quincenal`.
