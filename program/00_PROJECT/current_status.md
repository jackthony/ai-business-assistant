# Estatus del proyecto — 2026-10-06

- **Programa:** HealthTech Software & AI — SENATI 2026 (ciclo 3)
- **Fase:** Semana 4 — Producto (Issues #2–#4) con **cierre S3 acelerado integrado** · Q1 entregado; Q2 en curso
- **Informe FPE (CNIU-108) revisado:** registro diario con horas (LUN–SÁB + total), PEA de 151 operaciones (pendiente SINFO, Issue #6) y tarea significativa con proceso/herramientas/seguridad (ATS)/diagrama + firma del monitor. La demo del D3 (vie 9-oct) alimenta ese informe.
- **Investigación 6-oct completada:** precios Meta 1-oct-2026 verificados en estructura (service 1.000 gratis/número/mes, utility dentro de CSW siempre cobrado, FEP 7 días CTWA) — **falta solo confirmar las tarifas de Perú contra el panel Billing**; reglas de templates (aprobación <24 h, sin edición post-aprobación, opt-in) en `meta-pricing.md`; B/B/I Kapso vs n8n en `kapso-n8n.md` (decisión S10); OWASP GenAI 2026 (Top 10 LLM + Agent Control Standard) en source_map; Langfuse verificado (self-host gratis).
- **Aviso de privacidad (#7):** ✅ aprobado por el dueño (2026-10-06, Hola Mujer es negocio del monitor) — solo falta publicar el `PRIVACY_NOTICE_URL`.
- **TBD de aprendizaje (ADR-006 revisado 6-oct):** investigado GitHub Flow / TBD canónico / GitFlow — reglas duras mínimas (rama por Issue + `Closes #N` + commits convencionales + CI), cantidad de commits libre, PRs viven hasta 7 días; rigor creciente desde S7 (lead time <48 h).
- **GUIA_AGENTE.md creada (raíz):** instrucciones canónicas para la IA asistente de cada practicante — contexto mínimo, reglas a hacer cumplir (pull antes de iniciar, equipo, 4 puertas), **puerta de comprensión** (explica al LT con sus palabras antes de subir), catálogo de literatura (curaduría del LT ya integrada en source_map/cursos_de_refuerzo) y prohibiciones. La ciencia de agentes es el producto: se entiende, no se repite.
- **Pack de contexto y definiciones (6-oct, para practicantes y sus IAs de modelos gratis):** `pack_contexto.md` — negocio e ingeniería en formato corto + protocolo de **uso controlado de IA** (~10–15 interacciones/sesión, qué no pedir) + bloque por semana S4–S8 embebido automáticamente en cada Issue dominical; `stack-versiones.md` — Python **3.11** fijado (`.python-version`), deps con rangos, claves `.env`, comandos Windows y límites de las herramientas gratis (Actions ilimitado en repo público, Codespaces 60 h, ngrok, Ollama, DeepSeek web vs API, OpenCode). Issues #2/#3/#4 ya llevan el pack; #2 trae `pyproject.toml`/`.env.example` exactos para copiar.
- **Auditoría técnica del 6-oct (2 fases):** ~17 bugs reales corregidos en workflows/config (board GraphQL, enforcer, guardian, CI, releases, environments, repo settings); probado end-to-end con PR real + tag + dispatch; CodeQL: **Python se activa a mano** en cuanto el primer merge de Josue ponga código en `main` (la API rechaza idiomas ausentes).
- **Observabilidad 2026→2027 (nuevo `observabilidad-costos.md`):** estándar OpenTelemetry GenAI semconv (`open-telemetry/semantic-conventions-genai`, Apache-2.0) · Langfuse self-host gratis (Docker en la M5, S8) · evals S12 · FinOps S15 (costo por conversación) · GitHub Environments/Releases se activan en S14/S16 · Codespaces candidato para las PCs antiguas (120 h/mes gratis por usuario).
- **Antecedente de negocio integrado (hola-mujer.md + roadmap + `data/conversaciones/`):** ManyChat y n8n no gustaron ("no atiende como humano") → el agente aprende del **corpus real anonimizado** (few-shot S7, RAG objeciones S6, evals S12, baseline S13/S16) y atiende personalizado (memoria, tono, ≤3 líneas, 1 pregunta). Miras 2027 en roadmap: operación 24/7 con evals continuos, FinOps trimestral, expansión de canales vía ADR-011.
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
| Branch protection / rulesets | ✅ repo público (2026-10-06) → ruleset `main protegido (TBD)` activo: PR obligatorio, squash/lineal, checks requeridos `guardian-tbd / reglas-tbd` **y** `CI estricto / calidad` + push protection |
| DevSecOps (todo en GitHub) | ✅ CodeQL (default setup python+actions) · secret scanning + push protection · Dependabot (alerts + pip/actions semanal) · dependency-review en cada PR · acciones pineadas por SHA · GITHUB_TOKEN con permisos mínimos · **Environments `staging`/`produccion` con protection rules (produccion exige al monitor) · Codespaces listo (`.devcontainer`) · Releases automáticos por tag `v*`** |

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
- **#16** 🔄 Gestión: habilitar app Meta (webhook, templates, Billing). **Los chicos trabajan con fixtures hasta que #16 esté listo** (las pruebas reales de #3/#4 dependen de esto)

### Rutina semanal (no son Issues)
- **Domingo por la noche:** el workflow `crear-issues-semana` crea los Issues de la semana en el board desde el backlog (con lecturas + detalle); yo asigno el campo `Alumno`.

- **Josue (lun–mar–mié):** practica conmigo; cierre de su semana el miércoles (revisar PRs con DeepSeek reviewer + nota preliminar en Excel).
- **Pilar y Allan (mié–jue–vie):** cierre de su semana el viernes (revisar PRs + nota preliminar).
- **Sábado:** escuchar la sustentación quincenal (el informe lo redacta el alumno).
## Decisiones recientes (resumen)

- 11 ADRs vigentes: FastAPI · LangGraph · WhatsApp Cloud API · ChromaDB · memoria Sqlite→Postgres · TBD · agente único primero · **DeepSeek local first (ADR-008 — aplica al runtime M5; los practicantes usan PCs Windows con modelos chicos o DeepSeek web)** · harness/seguridad N1/N2/N3 · gobernanza de frameworks · canal-agnóstico (ADR-011).
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
