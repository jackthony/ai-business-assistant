# Estado actual del proyecto

- **Fecha:** 2026-10-06
- **Programa:** HealthTech Software & AI — SENATI 2026 (ciclo 3)
- **Fase:** Semana 1 — Fundamentos Java/POO + Git
- **Estado:** IN_PROGRESS
- **Issue actual:** ninguno del backlog #01–#39 (arrancan en S4). Trabajo S1: 3 apps consola individuales contextualizadas a Hola Mujer.

## Practicantes

- Allan Zerpa (zerpaallan@gmail.com)
- Pilar Aguilar (pilaraguilar.2502@gmail.com) — acceso confirmado al plan maestro e informe quincenal
- Josue Marreros (josuea.marrerosplasencia@gmail.com)

## Decisiones recientes

- ADR-006 TBD: 1 repo producto multitenant + branches cortas por Issue; PRs como evidencia.
- ADR-008 DeepSeek local first (M5 Pro, 24 GB): nube solo WhatsApp Cloud API; voz/visión local si el hardware da.
- ADR-009 Harness de seguridad: permisos N1/N2/N3, gating `draft→review→apply`, validación determinista primero.
- ADR-010 Frameworks: LangGraph se queda; OpenAI SDK / MS Agent Framework / Strands solo como referencias de patrones.
- Curaduría de fuentes 2026 completada (`02_REFERENCE/source_map.md`): Koenigstein verificada (taller avanzado, no comprar), 3 cursos Udemy clasificados como opcionales, OWASP ASI 2026 integrado.
- Se archivó la malla Java/Spring como plan de evaluación; el plan vigente es IA/WhatsApp S1–S16.
- Excel maestro migrado a `(EVALUABLE).xlsx` con evaluación automática 16×3 (fórmulas verificadas).

## Problemas abiertos

- **Operación actual en producción: ManyChat + n8n.** Flujos rígidos de botones; clientes no completan el recorrido y no se logra el objetivo. El proyecto los reemplaza progresivamente con el agente conversacional.
- PEA oficial de 4.º ciclo (SINFO) aún no llega: columnas PEA pendientes en el seguimiento quincenal.
- Re-secuencia v2 de las 48 sesiones pendiente (mover OCR/Whisper/NeuraCode, adelantar evaluación; motor DeepSeek local).
- Repo de código `ai-business-assistant` aún no creado (template + CONTEXT.md/ARCHITECTURE.md).
- Validar Ley 29733 (protección de datos, Perú) con abogado antes de tocar datos reales de clientes.

## Próximo paso

1. Re-secuenciar las 48 sesiones (v2) y aprobarlas como canónicas en `01_CURRICULUM/16_week_plan.md`.
2. Crear repo de código template con `CONTEXT.md` + `ARCHITECTURE.md` y arrancar Semana 1.
