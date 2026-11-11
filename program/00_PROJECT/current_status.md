# Estatus del proyecto — 2026-11-11

- **Programa:** HealthTech Software & AI — SENATI 2026 (ciclo 3)
- **Fase:** semana 9 según el calendario. S06 está en `main` (#192, #193, #197). S07–S09 se reorientó a extender y endurecer el agente existente (#234). El foco de integración es **WhatsApp local con datos ficticios**: #3 (Pilar), #184 (Allan) y #185 (Josue) tienen contrato y guía en `main` (#228). #183 tiene contrato y pruebas iniciales para la práctica de ubicación; sigue abierto sin asignar, al igual que #210–#212 y #224–#226.
- **Alcance (decisión del monitor, 2026-10-14):** solo **Hola Mujer**. NeuraCode es otro proyecto: se adapta recién cuando Hola Mujer esté terminado, validado y evaluado con su ciclo completo de evals. Multitenant y NeuraCode salieron del plan (S10 D3, S11 D1 y S12 D1 ahora son evals y el hito multimodal de Hola Mujer).
- **Código del producto (`src/`):** `/health` (#2), el grafo base de S5 D1 (#52, Josue) y el **agente único del HITO 2** (serie #140–#143, la hace el monitor con Claude), ya en `main`: **#140** RAG con citas, **#141** agendar idempotente con aprobación humana, **#142** derivación a una persona, y el código de **#143** (evals de los 12 escenarios: `python -m evals.run`, guía en `program/05_EVALUATION/hito2_evals.md`). Además, ya en `main`: **#192** (ingesta reproducible con huella SHA-256 y evaluación/calibración de la recuperación), **#193** (contrato de canal `InboundEvent`/`OutboundReply`, despachador y canales web y Telegram sobre el mismo agente: el código del HITO 1) y **#197** (few-shot de objeciones, `prompt_v2` sin activar y comparador v1/v2). 349 pruebas de repo en verde tras incorporar las diez del webhook local (#240). **#143 sigue abierto:** falta la corrida real `--live` en la M5 con DeepSeek y calibrar `RAG_MAX_DISTANCE`. El calendario y los avisos son **simulados** (en memoria) por decisión del monitor; `CALENDAR_ID`, la duración por servicio (la rejilla de 60 min es provisional), `JIOYSI_ALERT_CHANNEL` y `EMERGENCY_PROTOCOL` se resuelven con Jioysi al final, y hasta entonces el bot no debe usarse con clientas reales. El webhook local de WhatsApp se integró en #240; el #3 sigue abierto para la práctica TDD de Pilar. Sigue pendiente la memoria persistente (#54, Allan). La memoria sigue siendo `InMemorySaver` (el PR #222 aún no se fusiona).
- **Informe quincenal: presentación sábado 2026-11-14.** Borradores #12 (Pilar), #13 (Josue) y #221 (Allan), regenerados y verificados en la [corrida 42938135326](https://github.com/jackthony/ai-business-assistant/actions/runs/42938135326). El informe de Allan incluye #222. #50 quedó como histórico. El generador valida los tres Issues por número antes de escribir (#232) y los expedientes tienen seguimiento con evidencia, sin nota.
- **Pendiente del HITO 1** (lo coordina el monitor): la demo en vivo en la M5, el video, la medición de respuestas correctas, el informe Q3, el release `hito-1` y la corrida `--live` de #156 (tabla v1/v2).

## Qué cambió desde 2026-10-22 (todo en `main`)

- **S06 de Josue, mergeada el 28-oct**, con revisión contra cada contrato (check determinista, 4 puertas y pruebas por ID):
  - **PR #192** (Issue #157, 20 pruebas).
  - **PR #193** (Issue #158, 17 pruebas). El monitor agregó un ajuste en `src/channels/dispatch.py` (commit `9e6af74`) por R2/R3 de `S06_D3`: el corte previo dejaba fuera del hilo los mensajes de una clienta derivada y podía devolverle su propio texto.
  - **PR #197** (Issue #156, 13 pruebas). Es su #186 reempaquetado, porque el mensaje de commit medía 87 caracteres; se mergeó por rebase para conservar su autoría.
  - Las revisiones de #192 y #193 dejaron preguntas de comprensión pendientes.
- **Dependabot (28-oct)**, en el orden que recomendó la auditoría de Josue (#169). Los PRs posteriores #214–#218 se cerraron sin fusionar:
  - **#187** (`setup-python` 7.1.0; SHA verificado contra el tag y comentario de versión corregido).
  - **#188** (`starlette>=1.9.0`).
  - **#189** (`langgraph>=1.2.17`).
  - **#190** (`langchain-core>=1.7.0`; su conflicto con #189 se resolvió con un merge de main).
  - `ruff` (#164) sigue fuera de Dependabot.
- **Informe quincenal con interacción y PRs por REST** (#196, #199). Ver arriba.
- **Orquestador (#203, nuevo):** ciclo revisar → planificar → accionar → comprobar.
  - La sesión principal solo orquesta y publica: comentarios, pushes y merges.
  - El trabajo lo hacen subagentes Haiku (`escaner` y `verificador`) y Sonnet (`revisor` y `arreglador`), con harnesses en `.claude/agents/`.
  - Scripts deterministas en `tools/orquestador/`; playbook en `program/00_PROJECT/orquestador.md`.

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

**Estado al 2026-11-10:**

- **Josue:** S06 en `main` (#192, #193, #197). Tiene asignado #185, contrato S07 D3: oferta de horarios sin reservar. Le falta responder las preguntas de comprensión de #192 y #193.
- **Pilar:** #201 cerró sin fusionarse porque la base quedó en `main` con #178; sus ocho commits de octubre constan como evidencia. #53 cerró con explicación. Tiene asignado #3, contrato S04 D2: reproduce el rojo desde la etiqueta `tdd-issue-3` y empieza por el challenge GET con datos ficticios.
- **Allan:** #126 (Issue #4) está en `main`. En el PR #222 de memoria persistente (#54) pasan las nueve pruebas; la [revisión](https://github.com/jackthony/ai-business-assistant/pull/222#issuecomment-6783915941) pide ajustar la firma de `checkpointer` y completar la comprensión. Tiene #184 (S07 D2) como siguiente asignación tras #54.

El estado de las invitaciones como colaboradores está en el Issue #5 (sigue abierto). Los días de práctica y el roster viven en `.github/coach.json`.

## Alerta de seguridad (2026-10-22)

- **LiteLLM 1.107.0 comprometido:** no lo usamos (solo una línea de documentación lo descarta). Lo que sí concierne: tokens de GitHub CLI robados; los practicantes usan `gh`, así que ante duda deben rotar su token (`gh auth logout` y `gh auth login`).
- **Starlette «BadHost» (CISA KEV):** `pyproject.toml` exige `starlette>=1.9.0,<2` (piso de seguridad 1.0.1 en #176, subido por Dependabot en #188).
- **Checkpointers SQLite/Redis de LangGraph (SQL injection → ejecución de código):** hoy solo `InMemorySaver`. El contrato `S05_D3` (#54) exige validar el `thread_id` en `config_for_phone` (T4) y no usar texto de la clienta como clave de filtro.
- **ChromaDB CVE-2026-45829:** afecta al servidor; usamos el cliente en proceso. Sin acción.
- **⏳ Pendiente del monitor, solo se ve en la M5:** Ollama debe estar en 0.35.0 o superior (RCE por `/api/pull`, CVE-2026-103663). Ejecutar `ollama --version` y `netstat -ano | findstr 11434` (que escuche solo en 127.0.0.1) y anotar el resultado aquí.
- **Dependabot:** `ruff` queda fuera de sus PRs automáticos (#164): se sube a mano junto con el `rev` de `.pre-commit-config.yaml`, como en #98.

## Estado por área

| Área | Estado |
|---|---|
| Plan 16 semanas (48 sesiones) | ✅ v2 en `program/01_CURRICULUM/16_week_plan.md` |
| Asignaciones (contratos + guías) | D1–D3 de S5 y S6 validados; #3, #184 y #185 publicados (#228). #183 tiene contrato breve y etiqueta `tdd-issue-183`. |
| GitHub: plantillas, CODEOWNERS, labels, milestones, Dependabot | ✅ aplicado |
| Board + digest + coach | ✅ [projects/3](https://github.com/users/jackthony/projects/3); `board-sync` automático; digest cada viernes |
| CI/CD | ✅ CI estricto activo (4 puertas + chequeo de capas); CD y environments en S14 |
| Revisión automática | #230 atribuye los PRs del robot al alumno; probado contra #222. El PR #244 agrega una compuerta obligatoria de contrato y pruebas previas a los cambios de producto. Pendiente comprobar la revisión del PR del robot en Actions con un nuevo evento del alumno. `revision-ia` sigue requiriendo aprobación. |
| Rama principal | ✅ ruleset `main protegido (TBD)`: PR obligatorio, squash/lineal, checks requeridos `reglas-tbd` y `calidad` (por nombre de job), push protection |
| DevSecOps (todo en GitHub) | ✅ CodeQL · secret scanning + push protection · Dependabot · dependency-review · acciones pineadas por SHA · `GITHUB_TOKEN` con permisos mínimos · Environments `staging`/`produccion` (producción exige al monitor) · Codespaces (`.devcontainer`) · Releases por tag |
| Evaluación | ✅ Excel EVALUABLE; rúbrica y expedientes en `program/05_EVALUATION/` |
| Decisiones | ✅ 11 ADRs (`program/03_ARCHITECTURE/decisions/`) + `program/02_REFERENCE/source_map.md` |
| Código producto (`src/`) | ✅ agente del HITO 2, RAG con ingesta/evaluación (#192), canales web y Telegram (#193), few-shot v2 sin activar (#197). ✅ webhook local de WhatsApp (#240). ⏳ memoria persistente (#54) |

## Gestión abierta (sin novedad registrada en este archivo desde 2026-10-06)

Issues del monitor: **#5** colaboradores · **#6** mapear códigos PEA (SINFO) · **#7** política mínima de datos del bot (el aviso de privacidad fue aprobado por el dueño el 2026-10-06; falta publicar `PRIVACY_NOTICE_URL`) · **#10** bloqueantes de `04_CONFIG` · **#16** habilitar la app de Meta (webhook, templates, Billing). Dirección, mapa y horario ya están confirmados; siguen pendientes `CALENDAR_ID`, plantillas de WhatsApp, `EMERGENCY_PROTOCOL`, `DEFAULT_APPOINTMENT_MINUTES` y la URL del aviso de privacidad. Los precios de Meta (`program/02_REFERENCE/meta-pricing.md`) siguen **pendientes de validar** contra el panel Billing. Hasta que #16 esté listo, los practicantes trabajan con fixtures.

## Decisiones vigentes

- 11 ADRs: FastAPI · LangGraph · WhatsApp Cloud API · ChromaDB · memoria Sqlite→Postgres · TBD · agente único primero · DeepSeek local first (ADR-008: aplica al runtime M5; los practicantes usan PCs Windows con modelos chicos o DeepSeek web) · harness/seguridad N1/N2/N3 · gobernanza de frameworks · canal-agnóstico (ADR-011).
- TBD de aprendizaje (ADR-006 revisado): rama por Issue + `Closes #N` + commits convencionales estrictos + CI; los PRs viven hasta 7 días.
- Repo único `ai-business-assistant`, público, con transparencia total (`program/00_PROJECT/operacion.md`).
- Build/Buy/Integrate de canal (Kapso, n8n): revisión en S10 (`program/02_REFERENCE/kapso-n8n.md`). El núcleo de agentes sigue siendo propio.
- Nota semanal = **preliminar/formativa**; la oficial se consolida por quincena.

## Riesgos abiertos

- **Informe quincenal del 14-nov:** cada alumno completa horas, ATS y sustentación sobre los borradores #12, #13 y #221. El monitor evalúa.
- **WhatsApp:** el sender ya está en `main` (#126); el webhook local se integró en #240 y #3 conserva la práctica TDD de Pilar. El [laboratorio Docker](../02_REFERENCE/ejemplos/webhook-meta/README.md) (#237) permite probar el sender y el ejemplo. La implementación pasó W1–W10 y HTTP por loopback con catálogo ficticio y envío simulado. La prueba no valida reintentos de Meta ni entrega real.
- **Persistencia (#54):** el PR #222 no se fusiona hasta que Allan corrija el contrato, responda las preguntas de comprensión y se verifique el nuevo head.
- **Las preguntas de oro de #192 son casi nombres de servicios**, así que la calibración de `bge-m3` saldría optimista.
- **El webhook de Telegram con textos de más de 1000 caracteres** lanza `ValidationError` → 500 → Telegram reintenta. Es un hueco del contrato `S06_D3`.
- **Canal de WhatsApp real para Hola Mujer:** hechos confirmados (2026-10-14): negocio **no verificado**, límite estándar, **sin proveedor conectado**, hoy usa la app WhatsApp Business. Recomendación: seguir en canal provisional (Telegram + chat web) en S6–S8 y evaluar la **coexistencia** (app + API en el mismo número): primero Jack (único con acceso) ve en WhatsApp Manager si el número real es elegible (solo lo muestra Meta; criterios a mirar: si exige negocio verificado, si Perú está soportado y la versión mínima de la app; ver `proveedores-whatsapp.md` §7) y luego probar el flujo técnico con un número de prueba; si exige verificación, queda el canal provisional. No se toca el número de producción.
- **Datos del Excel por confirmar con Jioysi:** duraciones (todas 60 min, parece valor por defecto), vigencia de las 3 promociones y la lista de servicios sensibles; las hojas `00_EMPEZAR` y la oculta tienen datos de personas.
- **Revisiones en espera:** la atribución de #222 ya funciona localmente (#230). El monitor decide sobre las corridas pendientes de `revision-ia`.
- PEA SINFO pendiente (bloquea columnas del seguimiento quincenal).
- Ley 29733 sin validar: prohibido tocar datos reales de clientes (el corpus de `data/conversaciones/` es anonimizado).
- Operación actual ManyChat + n8n no cumple el objetivo: el reemplazo se construye en S4–S6.

## Próximo paso

1. Pilar: partir de `tdd-issue-3`, reproducir el rojo, implementar por pasos y comprobar W1–W10 y HTTP en Docker para la práctica #3. Allan: resolver #222 y luego #184. Josue: empezar #185 y responder en #192/#193.
2. Presentación del informe quincenal: sábado 14-nov, Issues #12, #13 y #221.
3. Monitor: confirmar el texto comercial definitivo para fuera de Chimbote, el diseño de estado para leads sintéticos (#210/#211) y la política de preguntas ambiguas de safety (#224). Se mantienen los avisos y el calendario simulados.
4. Monitor: decidir sobre las corridas en `revision-ia`. En la M5: `--live` de #156 y #143, calibración de `RAG_MAX_DISTANCE`, verificar Ollama y preparar demo, video y releases de los hitos.
5. Integraciones: resolver con Jioysi y Meta las dependencias de #16 antes de probar con números, credenciales, calendario o alertas reales.
