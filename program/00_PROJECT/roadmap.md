# Roadmap — visión, alcance y fases

## Visión (por qué)

Construir un **asistente de IA empresarial multitenant para WhatsApp** (Hola Mujer + NeuraCode), **canal-agnóstico** (ADR-011): hoy Meta/WhatsApp, mañana TikTok u otra plataforma — la capa de agentes es el producto, el canal es un adapter. Software y contexto corriendo en local (DeepSeek), como producto real que además sirve de vehículo de formación para 3 practicantes SENATI durante 16 semanas (salen como AI engineers; el monitor lidera un proyecto en producción completo).

## Objetivos

1. **Producto:** agente que informa, agenda, cierra ventas, recibe comprobantes (Yape/Plin), deriva a humano y se reactiva — sin alucinar, con trazabilidad.
2. **Formación:** llevar a los practicantes de fundamentos (Java/POO/Git) a un sistema multiagente en producción (FastAPI + LangGraph + RAG + multimodal).
3. **Método:** TBD (Trunk-Based Development), Issues como unidad de trabajo, PRs como evidencia, DeepSeek local como tutor/coder/reviewer.

## Criterios de éxito

- Los 3 practicantes sustentan 16 semanas de evidencia verificable (commits/PRs/Issues).
- Hola Mujer atendiendo WhatsApp con RAG real (47 servicios) y handoff humano.
- NeuraCode como segundo tenant sobre la misma base.
- Demo final E2E desplegada + informe SENATI completo.

## Alcance — dentro

- 48 sesiones (16 semanas × 3 días) y Issues #01–#39 del backlog.
- Backend propio: FastAPI + LangGraph + ChromaDB + memoria persistente.
- Canal WhatsApp Cloud API (Meta) — única dependencia de nube obligatoria.
- Conversación natural y humanizada (sin menús rígidos); regla explícita de **cuándo escalar a humano** (safety_agent + HITL).
- Multitenant: Hola Mujer y NeuraCode sobre el mismo núcleo con configs separadas.
- Multimodal por fases: voz (faster-whisper, S11) y comprobantes por imagen (Qwen2.5-VL, S10); video se evalúa después.
- Comprensión de campañas: capturar el origen del chat (click-to-WhatsApp/ads) para saber qué anuncio trae clientes.
- Reutilizar plataformas existentes (Google Calendar, Sheets, ERP) e integrar donde aporten; construir solo el núcleo diferenciador.
- **FinOps**: costo por conversación medido desde S4; LLM local y ventana de servicio 24 h de WhatsApp como palancas.
- Evaluación semanal/quincenal + informes SENATI.
- KB-A (negocio) vive en el Excel/Sheets operativo → se convierte a JSON/RAG; **nunca** se mezcla con KB-P (este repo).

## Alcance — fuera

- Diagnóstico o consejo clínico (el bot deriva siempre a humano).
- Decisiones de precios/negocio sin validar con Hola Mujer o NeuraCode.
- Datos reales de clientes en repos o en contexto de IA (anonimizar siempre).
- Rediseñar scheduling/CRM propios: se integra lo existente (Cal.com, Sheets, ERP) cuando aplique.
- Compra de infraestructura cloud más allá de lo mínimo para el canal WhatsApp.

## Fases

| Fase | Semanas | Foco | Entregable |
|---|---|---|---|
| 1. Fundamentos | S1–S3 | Java/POO, Git, tests, HTTP/REST y contratos (exigencia SENATI) | 3 apps consola + repos profesionales + mapa de integraciones |
| 2. Agente único | S4–S8 | FastAPI, webhook Meta, LangGraph, RAG Chroma, citas, cierre | HITO 1: bot respondiendo por WhatsApp (S6) |
| 3. Multiagente | S9–S12 | Safety/HITL, OCR, supervisor router, multitenant NeuraCode, voz, seguridad y evaluación | HITO 2 (S9) y HITO 3 (S12) |
| 4. Producción | S13–S16 | Proactivo, Postgres, Docker, deploy, fallbacks, E2E | Demo final + transferencia (S16) |

## Hitos

- **HITO 1 (S6 D3):** bot Hola Mujer responde precios/duraciones/servicios desde RAG real.
- **HITO 2 (S9 D3):** agente único completo (4 agentes + handoff, sin supervisor todavía).
- **HITO 3 (S12 D3):** NeuraCode atendiendo + notas de voz.
- **Demo final (S16 D3):** E2E, informe SENATI y transferencia.

> El detalle diario vigente (v2, 48 sesiones) está en `program/01_CURRICULUM/16_week_plan.md`.
