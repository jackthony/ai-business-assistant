# Estado actual del proyecto

- **Fecha:** 2026-10-06
- **Programa:** HealthTech Software & AI — SENATI 2026 (ciclo 3)
- **Fase:** Semana 4 — Nace el producto · Q1 entregado por los alumnos; Q2 en curso
- **Estado:** IN_PROGRESS
- **Issue actual:** #2 (setup FastAPI + CI). Issues de S4 creados en GitHub: #2–#4 (los IDs del backlog #01–#39 van +1 en GitHub por el Issue #1 del digest).

## Practicantes

- Allan Zerpa ((privado))
- Pilar Aguilar ((privado)) — acceso confirmado al plan maestro e informe quincenal
- Josue Marreros ((privado))

## Decisiones recientes

- ADR-006 TBD: 1 repo producto multitenant + branches cortas por Issue; PRs como evidencia.
- ADR-008 DeepSeek local first (M5 Pro, 24 GB): nube solo WhatsApp Cloud API; voz/visión local si el hardware da.
- ADR-009 Harness de seguridad: permisos N1/N2/N3, gating `draft→review→apply`, validación determinista primero.
- ADR-010 Frameworks: LangGraph se queda; OpenAI SDK / MS Agent Framework / Strands solo como referencias de patrones.
- Guía «Comprehensive Guide to AI Agent Engineering» (Vasilyev, MIT) adoptada como apoyo de alumnos; mapa semanal en `02_REFERENCE/agent-engineering-handbook.md` y PDF en Drive → `02_ALUMNOS/`.
- **Repo único `ai-business-assistant`** (antes `senati-ai-agents-context`): programa + producto por decisión de transparencia; prácticas GitHub aplicadas (plantilla de Issue/PR, CODEOWNERS, labels, milestones, Dependabot) — ver `00_PROJECT/github_devops.md`.
- Cursos de refuerzo verificados y planificados en `01_CURRICULUM/cursos_de_refuerzo.md` (3 comprados; gaps WhatsApp/Ollama con opciones gratis u opcionales ~$10–15).
- Curaduría de fuentes 2026 completada (`02_REFERENCE/source_map.md`): Koenigstein verificada (taller avanzado, no comprar), 3 cursos Udemy clasificados como opcionales, OWASP ASI 2026 integrado.
- Se archivó la malla Java/Spring como plan de evaluación; el plan vigente es IA/WhatsApp S1–S16.
- Excel maestro migrado a `(EVALUABLE).xlsx` con evaluación automática 16×3 (fórmulas verificadas).

## Problemas abiertos

- **Operación actual en producción: ManyChat + n8n.** Flujos rígidos de botones; clientes no completan el recorrido y no se logra el objetivo. El proyecto los reemplaza progresivamente con el agente conversacional.
- PEA oficial de 4.º ciclo (SINFO) aún no llega: columnas PEA pendientes en el seguimiento quincenal.
- S4 en ejecución: `src/`, CI, webhook y sender (Issues #2–#4); branch protection/rulesets pendientes (GitHub Pro o repo público en S16).
- Project board creado y vinculado al repo: https://github.com/users/jackthony/projects/3 (Issues #2–#4 dentro).
- Usuarios de GitHub de Allan, Pilar y Josue: se solicitan el 2026-10-07; luego se agregan como colaboradores.
- Validar Ley 29733 (protección de datos, Perú) con abogado antes de tocar datos reales de clientes.

## Próximo paso

1. Cerrar Issues #2–#4 (setup+CI, webhook, sender + demo E2E) y el informe Q2 del alumno.
2. Crear el Project board (tras el refresh de scopes) y agregar los Issues de la semana.
3. Agregar a los 3 practicantes como colaboradores cuando compartan sus usuarios (2026-10-07).
