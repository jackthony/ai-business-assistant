# Estatus del proyecto — 2026-10-14

- **Programa:** HealthTech Software & AI — SENATI 2026 (ciclo 3)
- **Fase:** Semana 5 — LangGraph core (tracker #51; Issues de producción #52–#54). Los Issues de S4 #3 (webhook, Pilar) y #4 (envío, Allan) **siguen abiertos**; #2 (setup FastAPI + CI, Josue) está cerrado.
- **Alcance (decisión del monitor, 2026-10-14):** solo **Hola Mujer**. NeuraCode es otro proyecto: se adapta recién cuando Hola Mujer esté terminado, validado y evaluado con su ciclo completo de evals. Multitenant y NeuraCode salieron del plan (S10 D3, S11 D1 y S12 D1 ahora son evals y el hito multimodal de Hola Mujer).
- **Código del producto (`src/`):** `/health` (#2) y el agente único en construcción (serie #140–#143, la hace el monitor con Claude). Ya en `main`: **#140** nodo `info` con RAG sobre `data/hola_mujer/` y citas. En curso: **#141** herramienta `agendar_cita` idempotente (N2: propone → aprobación humana con `interrupt` → escribe). Siguen: #142 derivación a una persona, #143 evals de los 12 escenarios del HITO 2. Pendientes del negocio que limitan el agente: `CALENDAR_ID` y la duración por servicio (la rejilla de 60 min es provisional). `channels/` y `memory/` siguen vacíos.
- **Bloqueo principal:** **#52 (Josue)**. El PR #81 se mergeó fuera de contrato (tocó archivos que no están en la sección 4 y metió el checkpointer y su dependencia, que la sección 9 prohíbe) y se **revirtió** (#86). #52 está reabierto: Josue lo rehace con `program/01_CURRICULUM/asignaciones/S05_D1.md` y su paso a paso. **#53 (Pilar) y #54 (Allan) no arrancan hasta que #52 esté en `main`**; mientras tanto avanzan con sus estudios guiados (#34–#38) y la inducción (#43, #44).
- **Informe quincenal: presentación sábado 2026-10-17.** Borradores automáticos: #12 (Pilar), #13 (Josue), #50 (Allan); se refrescan cada noche. La quincena anterior (presentación 10-oct) tuvo #11 y el tracker #27.

## Qué cambió desde 2026-10-06 (todo en `main`)

- **Contratos deterministas de S5** (`program/01_CURRICULUM/asignaciones/`, #57): un contrato `S05_D#.md` y una guía paso a paso por Issue. Validados **ejecutándolos** con una solución de referencia (D1 en #96, D2 y D3 en #100); cada uno tenía algún texto que contradecía la práctica y ya está corregido.
- **Revisión del trabajo de los practicantes en capas:**
  - `pr-borrador` + `revision-guiada` (DeepSeek, #59): PR en borrador desde el primer push y un comentario tutor que se actualiza. No bloquea.
  - `revisor-contrato` (#88): compuerta con check determinista (`contrato_check.py`) y revisor Claude (`revisor_agente.py`, secreto `ANTHROPIC_API_KEY`), solo en PRs de alumnos y con el PR listo. La clave se **probó contra la API real** y la prueba corrigió un bug (#94: la API rechazaba `temperature`, y el error se habría confundido con una caída). La revisión guiada ignora a cualquier bot (#90).
  - **Pendiente:** `revisor-contrato` aún **no** es un check requerido del ruleset. Se agrega después de ver su comentario en el primer PR real de un alumno (agregarlo antes bloquearía todos los PRs).
- **`ruff` alineado** entre el hook local y el CI (#98): misma versión (0.16.x) en `pyproject.toml` y `.pre-commit-config.yaml`; los alumnos fueron avisados en sus Issues de coach (#47–#49).
- **Coach, board y comunicación:** coach proactivo (arranque, pulso y cierre) y `board-sync` (#39); wiki y Discussions con avisos al equipo (#61, #64); todo Issue nace con hito, tracker y bloqueos (#66); el guardián TBD exime a Dependabot (#79); créditos e inspiración del proyecto en el README y `source_map.md` (#68, #82).
- **Ejemplos guiados y setup:** bloques con tests para S4–S5 (`program/02_REFERENCE/ejemplos/`), cierre del setup #2 con `configs/` y diagramas (#33), inducción S5 (#42).
- **Documentación:** README, este archivo y las guías actualizados al 2026-10-14 (#101).
- **Negocio y datos (2026-10-14):** dirección, mapa y horario de Hola Mujer confirmados (#104, #106). Catálogo, promociones, datos del negocio y vocabularios normalizados a JSON en `data/hola_mujer/` con su ETL y una auditoría del Excel (#116); corpus sintético v2 de 100 conversaciones con su generador y la fuente de cada parámetro (#114).
- **README:** camino de un agente a multiagente con criterios de salida y fuentes primarias verificadas (#108); alcance solo Hola Mujer (#110, #113).

## Practicantes

- Josue Marreros — GitHub `adbon-dm1` · alta carga + mentor interno (practica lun–mié)
- Pilar Aguilar — GitHub `estefanyP-hub` · media (practica mié–vie)
- Allan Zerpa — GitHub `WhoAllan` · media (practica mié–vie)

El estado de las invitaciones como colaboradores está en el Issue #5 (sigue abierto). Los días de práctica y el roster viven en `.github/coach.json`.

## Estado por área

| Área | Estado |
|---|---|
| Plan 16 semanas (48 sesiones) | ✅ v2 en `program/01_CURRICULUM/16_week_plan.md` |
| Asignaciones S5 (contratos + guías) | ✅ D1–D3 validados ejecutándolos (#96, #100) |
| GitHub: plantillas, CODEOWNERS, labels, milestones, Dependabot | ✅ aplicado |
| Board + digest + coach | ✅ [projects/3](https://github.com/users/jackthony/projects/3); `board-sync` automático; digest cada viernes |
| CI/CD | ✅ CI estricto activo (4 puertas + chequeo de capas); CD y environments en S14 |
| Revisión automática | ✅ guardián TBD · ficha · DeepSeek (tutor y primer pase) · `revisor-contrato` (determinista + Claude). ⏳ falta volverlo check requerido tras su primera prueba real |
| Rama principal | ✅ ruleset `main protegido (TBD)`: PR obligatorio, squash/lineal, checks requeridos `reglas-tbd` y `calidad` (por nombre de job), push protection |
| DevSecOps (todo en GitHub) | ✅ CodeQL · secret scanning + push protection · Dependabot · dependency-review · acciones pineadas por SHA · `GITHUB_TOKEN` con permisos mínimos · Environments `staging`/`produccion` (producción exige al monitor) · Codespaces (`.devcontainer`) · Releases por tag |
| Evaluación | ✅ Excel EVALUABLE; rúbrica y expedientes en `program/05_EVALUATION/` |
| Decisiones | ✅ 11 ADRs (`program/03_ARCHITECTURE/decisions/`) + `program/02_REFERENCE/source_map.md` |
| Código producto (`src/`) | ⏳ solo `/health`; webhook (#3), envío (#4) y grafo (#52) pendientes |

## Gestión abierta (sin novedad registrada en este archivo desde 2026-10-06)

Issues del monitor: **#5** colaboradores · **#6** mapear códigos PEA (SINFO) · **#7** política mínima de datos del bot (el aviso de privacidad fue aprobado por el dueño el 2026-10-06; falta publicar `PRIVACY_NOTICE_URL`) · **#10** bloqueantes de `04_CONFIG` · **#16** habilitar la app de Meta (webhook, templates, Billing). Dirección, mapa y horario ya están confirmados; siguen pendientes `CALENDAR_ID`, plantillas de WhatsApp, `EMERGENCY_PROTOCOL`, `DEFAULT_APPOINTMENT_MINUTES` y la URL del aviso de privacidad. Los precios de Meta (`program/02_REFERENCE/meta-pricing.md`) siguen **pendientes de validar** contra el panel Billing. Hasta que #16 esté listo, los practicantes trabajan con fixtures.

## Decisiones vigentes

- 11 ADRs: FastAPI · LangGraph · WhatsApp Cloud API · ChromaDB · memoria Sqlite→Postgres · TBD · agente único primero · DeepSeek local first (ADR-008: aplica al runtime M5; los practicantes usan PCs Windows con modelos chicos o DeepSeek web) · harness/seguridad N1/N2/N3 · gobernanza de frameworks · canal-agnóstico (ADR-011).
- TBD de aprendizaje (ADR-006 revisado): rama por Issue + `Closes #N` + commits convencionales estrictos + CI; los PRs viven hasta 7 días.
- Repo único `ai-business-assistant`, público, con transparencia total (`program/00_PROJECT/operacion.md`).
- Build/Buy/Integrate de canal (Kapso, n8n): revisión en S10 (`program/02_REFERENCE/kapso-n8n.md`). El núcleo de agentes sigue siendo propio.
- Nota semanal = **preliminar/formativa**; la oficial se consolida por quincena.

## Riesgos abiertos

- **#52 bloquea la semana:** Josue tiene 6 archivos y 8 pruebas por delante; sin su merge, #53 y #54 no pueden empezar.
- **Informe quincenal del 2026-10-17:** los borradores dependen de la evidencia real de cada alumno (commits, PRs, Issues). Al 2026-10-14 Pilar y Allan tienen 0 commits, PRs e Issues cerrados en la quincena: su trabajo de estudio (#34–#38, #43, #44) no deja rastro en GitHub y sus borradores salen vacíos.
- **Canal de WhatsApp real para Hola Mujer:** hechos confirmados (2026-10-14): negocio **no verificado**, límite estándar, **sin proveedor conectado**, hoy usa la app WhatsApp Business. Recomendación: seguir en canal provisional (Telegram + chat web) en S6–S8 y evaluar la **coexistencia** (app + API en el mismo número): primero Jack (único con acceso) ve en WhatsApp Manager si el número real es elegible (solo lo muestra Meta; criterios a mirar: si exige negocio verificado, si Perú está soportado y la versión mínima de la app; ver `proveedores-whatsapp.md` §7) y luego probar el flujo técnico con un número de prueba; si exige verificación, queda el canal provisional. No se toca el número de producción.
- **Datos del Excel por confirmar con Jioysi:** duraciones (todas 60 min, parece valor por defecto), vigencia de las 3 promociones y la lista de servicios sensibles; las hojas `00_EMPEZAR` y la oculta tienen datos de personas.
- `revisor-contrato` no ha corrido sobre un PR real de alumno: sus capas están probadas por tests y con la API real, no con un caso de punta a punta.
- PEA SINFO pendiente (bloquea columnas del seguimiento quincenal).
- Ley 29733 sin validar: prohibido tocar datos reales de clientes (el corpus de `data/conversaciones/` es anonimizado).
- Operación actual ManyChat + n8n no cumple el objetivo: el reemplazo se construye en S4–S6.

## Próximo paso

1. Josue rehace #52 siguiendo `S05_D1.md`: rama `issue-52-langgraph-core`, pruebas T1–T8 primero y solo las 6 rutas de la sección 4.
2. Con el primer PR real de un alumno: leer el comentario «🛡️ Revisor del contrato», confirmar que la capa Claude corrió y, si todo va bien, agregar `revisor-contrato` a los checks requeridos del ruleset.
3. Al mergear #52: Pilar (#53) y Allan (#54) arrancan en paralelo.
4. Sábado 2026-10-17: sustentación de la quincena; el informe lo redacta cada alumno sobre su borrador.
5. Deuda conocida: `pre-commit run --all-files` destapa formato y espacios finales fuera de `src/` y `tests/` (`tools/`, `.github/scripts`, docs) que el CI no revisa.
