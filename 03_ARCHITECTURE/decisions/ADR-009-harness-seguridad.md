# ADR-009: Harness de confiabilidad y seguridad

- **Fecha:** 2026-10-06
- **Estado:** aceptada

## Contexto

El bot ejecuta tools con efectos reales (agendar, validar comprobantes, registrar leads). La fiabilidad compuesta cae con cada paso (heurística: p^n; y un validador imperfecto puede empeorar el sistema si `v·r/f ≤ p/(1-p)` — la semilla de Lusser del CH05). OWASP Agentic 2026 define ASI01–ASI10. Un benchmark reproducido (agent_harness_course) muestra **31.2% de inyecciones indirectas activando tools**; y al reanudar un checkpoint de LangGraph un efecto puede re-ejecutarse (doble cobro/cita).

## Decisión

Harness mínimo obligatorio para todo lo que toque al usuario:

1. **Permisos por niveles:** N1 automático (RAG, precios, disponibilidad) · N2 con aprobación/HITL (agendar, registrar lead, validar pago) · N3 **nunca** expuesto al LLM (borrar datos, modificar precios base).
2. **Efectos con gating:** `draft_effects → human_review (interrupt) → apply_effects`; nada con efecto secundario antes del interrupt.
3. **Validación determinista primero:** Pydantic/regex en cada tool (f≈0); LLM-as-a-Judge solo offline o para contenido ambiguo.
4. **RAG íntegro:** nunca re-ingerir salidas del bot; provenance por documento en Chroma (ASI06).
5. **Intent gate:** validar esquema + rate limit antes de ejecutar cada tool; logs inmutables sin datos personales.
6. **Action log + undo** para toda escritura.

## Consecuencias

- S9 (#16–#18) y S12 (#26) incluyen tests de inyección y de re-ejecución; son criterio de aceptación.
- Prohibida la caché semántica por similitud de texto: claves por `service_id`/intención.
- `RichmondAlake/agent_harness_course` se usa como lectura de patrones (sin licencia → no copiar código).
- Referencias: OWASP ASI Top 10 2026 (PDF genai.owasp.org/download/52117/), GenAI LLM Top 10 2026, Agent Control Standard.
