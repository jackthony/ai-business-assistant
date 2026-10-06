# Dominio: Hola Mujer (tenant 1)

> Fuente canónica de datos: `Hola Mujer · MVP WhatsApp ManyChat · Operativo (1).xlsx` (11 hojas, verificado 2026-10-06). El repo guarda solo **esquemas y reglas**, nunca datos personales: contactos, citas y muestra de inbox se usan anonimizados.

## Propósito oficial (00_EMPEZAR)

Automatizar ubicación, servicios, agenda, recordatorios y derivación a **Jioysi** sin guardar datos clínicos. Público: mujeres; tono empático y humano.

## Configuración del negocio (04_CONFIG)

| Clave | Valor | Estado |
|---|---|---|
| BUSINESS_NAME | Hola Mujer | CONFIRMED |
| TIMEZONE | America/Lima | CONFIRMED |
| HANDOFF_SLA_MINUTES | 10 | PROPOSED |
| REMINDER_24H / REMINDER_2H | activos | PROPOSED (sujeto a plantillas aprobadas) |
| ADDRESS · MAP_URL · OPENING_HOURS | POR_CONFIRMAR | ⛔ PENDIENTE (Jioysi) |
| CALENDAR_ID · WA_TEMPLATE_* · PRIVACY_NOTICE_URL | POR_CONFIRMAR | ⛔ PENDIENTE |
| EMERGENCY_PROTOCOL | pendiente de aprobación | ⛔ PENDIENTE (Jioysi) |

**Bloqueantes del negocio** (los resuelve el negocio, no el equipo): dirección/mapa/horario (guardrail de ubicación y S3), `CALENDAR_ID` (Agente 2, #12), plantillas WA aprobadas (recordatorios S13), aviso de privacidad (Issue #7) y protocolo de emergencia (seguridad clínica).

## Catálogo (05_SERVICIOS)

- **47 servicios** en 13 categorías: Estética facial (8) · Prevención y tamizaje (7) · Estética corporal (5) · Salud íntima y ginecológica (4) · Dermatocosmética (4) · Planificación familiar (4) · Obstetricia (3) · Prevención y salud femenina (3) · Terapias complementarias (3) · Capilar (2) · Academy (2) · Postquirúrgico (1) · Clínico-estéticos (1).
- Precios: **S/ 24.99 – 449.99**. Campos: `service_id` (HM-CAP-*, HM-CORP-*, …), `precio_pen`, `reserva_pen`, `duracion_min`, `permite_sesiones`, `activo`, `requiere_evaluacion`, `cta`.
- El ETL de S6 (#08) lee esta hoja → JSON → ChromaDB.

## Promociones (06_PROMOCIONES)

- Campos: `promo_id` (LUNARES, MOLDEA, GLUTEOS…), precios, sesiones, vigencia. Ojo: varias con `activo=NO` y fechas inconsistentes → validar con el negocio antes de cargar al RAG.

## Reglas de negocio (07_APRENDIZAJES_INBOX — 14 reglas)

1. **Identidad:** usar `contact_id`/`event_id`; no deduplicar por nombre (220 filas ≠ 212 contactos ≠ 218 chats).
2. **Asignación:** todo chat con dueño (AUTOMATION o Jioysi); sin dueño no hay SLA.
3. **NEW vs RETURNING:** lookup por `contact_id`; NEW = sin cita/venta previa.
4. **Tipo de contacto:** clasificar PATIENT_LEAD / PROVIDER / AUTO_REPLY / TEST / SOCIAL / OTHER antes de vender.
5. **Agendamiento:** en la muestra, 33 invitaciones → 2 horarios elegidos: el cuello está entre el CTA y la confirmación → ofrecer 2–3 horarios reales y medir cada transición.
6. **Servicios top de la muestra:** 24 vitamina/hierro, 7 moldeamiento, 5 verrugas/lunares, 3 Glow → priorizar FAQ y pruebas ahí.
7. **Ubicación:** fricción por enterarse tarde de que la atención es en Chimbote → preguntar ciudad temprano y enviar mapa de un clic (depende de 04_CONFIG).
8. **Tono de venta:** una pregunta por turno, una explicación breve, un CTA concreto; no copiar bloques largos.
9. **Horario:** timestamps exactos en America/Lima; separar horario laboral / fuera de horario.
10. **Cierres suaves:** "gracias"/"ok" puede ser abandono silencioso → ofrecer un siguiente paso pequeño; detener si rechaza.
11. **Seguridad clínica:** pausar, etiquetar, asignar y notificar a Jioysi con resumen no clínico (protocolo pendiente de aprobación por Jioysi).
12. **Pruebas:** etiqueta `HM_TEST`; excluir de métricas.
13. **Métricas objetivo:** `booking_rate`, `show_rate`, `sale_rate`, `satisfaction`.
14. **Conclusión del negocio:** la muestra mejora reglas pero no calcula conversión real → validar con eventos estructurados y recalibrar con datos reales.

## Agenda y eventos (02_CITAS / 03_EVENTOS)

- Citas: `cita_id`, `service_id`, sesiones, inicio/fin, timezone, `estado_cita`, `calendar_event_id`, recordatorios 24 h/2 h, `motivo_cambio`, `sync_status`.
- Eventos: `INBOUND_MESSAGE` / `HANDOFF_REQUESTED` con flujos ManyChat actuales (`MVP_ROUTER`, `HM_WA_10_UBICACION`, `HM_WA_20_SERVICIOS`, `HM_90_ESCALAR_A_HUMANO`) → reemplazo progresivo por el agente.

## Plan del negocio (08_PLAN_IMPLEMENTACION)

16 pasos; **paso 0 DONE**, 1–15 TODO. Los pasos 2 (catálogo aprobado) y 10 (Calendar + `request_id` idempotente) son precondiciones de nuestros #08 y #12. El negocio ya tiene su roadmap: nuestro programa lo ejecuta de forma profesional.

## Por completar (dependencias del negocio)

- Dirección/mapa/horario (Jioysi) · catálogo final aprobado · CALENDAR_ID · plantillas WA · aviso de privacidad · protocolo de emergencia.
- FAQs y objeciones reales (alimentar el few-shot de #07).
- Pagos: Yape / Plin / BCP (capturas de comprobante) — validar montos y políticas.

## Reglas de IA

- Nunca responder temas médicos: pausar y derivar (safety_agent, SLA 10 min).
- Precios y duraciones **solo** desde RAG; si no está en la base, no inventar.
