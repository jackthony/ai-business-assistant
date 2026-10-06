# Observabilidad, métricas y costos — stack 2026 → 2027 (verificado 2026-10-06)

> Para el bot que va a producción (y se vende), observabilidad no es un extra: es cómo se prueba que funciona, cuánto cuesta y dónde falla antes de que lo note el cliente.

## El estándar: OpenTelemetry GenAI semantic conventions

- Las convenciones semánticas de GenAI ahora viven en `open-telemetry/semantic-conventions-genai` (Apache-2.0, activo): **spans, métricas y eventos** para LLMs, **agentes**, **MCP** y proveedores (OpenAI, Anthropic…). Es el estándar que el ecosistema adopta en 2026→2027.
- Langfuse es OpenTelemetry-nativo (ingiere OTel; lo dijimos en la verificación de precios). Regla: **instrumentamos con conceptos OTel** (trazas, spans, sesiones, tokens, costos), el backend es Langfuse — si mañana cambia el backend, la instrumentación queda.

## Stack por fase (qué adoptamos cuándo)

| Fase | Qué | Con qué |
|---|---|---|
| **S4 (ya activo)** | Logs + métricas básicas: latencia de primera respuesta y reintentos del sender (#4); DORA (lead time, CFR) en el digest; CI + CodeQL + secret scanning como "observabilidad del código" | stdout estructurado + GitHub Actions |
| **S8 (#25)** | Trazas por nodo del grafo, sesiones por `thread_id` (teléfono), tokens por conversación, latencia, errores por nodo; dashboard mínimo (primera respuesta, contención, errores) | **Langfuse self-host** (Docker en la M5 — gratis) · SDK Python sobre LangGraph |
| **S12** | Evals offline (LLM-as-judge con `deepseek-r1:14b` local), datasets versionados, alertas de degradación | Langfuse datasets/evals + OWASP GenAI 2026 |
| **S14** | Ambientes de GitHub (`staging`/`produccion` con protection rules), dashboards por ambiente, DF/MTTR, release | GitHub Environments + Langfuse dashboards |
| **S15** | FinOps: **costo por conversación** = cómputo local (electricidad M5) + mensajes Meta (tarifas `meta-pricing.md`); fallback de modelos medido | OTel + `roi_metrics.md` |
| **S16** | SLOs finales + defensa: latencia p50/p95, % respuestas correctas, costo/conversación, handoff rate | dashboards + informe |

## Costos (verificados 2026-10-06)

| Componente | Costo |
|---|---|
| Langfuse **self-host** (Docker en la M5) | **$0** (open source) |
| Langfuse Cloud | Hobby gratis (50k units, 2 users, 30 días) · Core $29/mes · Pro $199/mes |
| Meta mensajes | tablas de `meta-pricing.md` (service 1.000 gratis/mes por número; utility/marketing cobrados; FEP gratis) |
| LLM (Ollama local) | $0 licencia; solo electricidad |
| Alternativas descartadas por ahora | LangSmith (de pago, lock-in mayor), Helicone/LiteLLM (gateway útil solo multi-proveedor cloud), OpenMeter (billing de uso — no aplica aún) |

## Métricas del negocio (además de DORA — en `roi_metrics.md`)

- **Primera respuesta** (<2 s en grafo; Meta cobra solo delivered), **contención** (% resuelto sin humano), **conversión** (conversación → lead → cita → pago), **handoff rate** (a Jioysi), **costo por conversación**.
- DORA del equipo (ya automático en el digest): lead time PR→merge, CFR, y desde S14 DF/MTTR.

## Lo que GitHub ya nos da gratis (auditoría 6-oct)

- **Activo:** Actions logs + badges, CodeQL, secret scanning + push protection, Dependabot (alerts + updates), Security overview (Security tab = el dashboard DevSecOps), Projects (gestión), Insights (actividad del repo), ruleset con checks obligatorios.
- **A activar cuando toque:** **Environments** con protection rules y secrets por ambiente (S14) · **Releases** con notas generadas (S16, release `hito-1` en S6) · **Codespaces** (opcional: dev environment en la nube — candidato para las PCs antiguas de los practicantes; 2-core gratis hasta 120 h/mes por usuario; decisión del monitor) · Actions cache para pip (acelera el CI).
