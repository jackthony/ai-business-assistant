# Dominio: Hola Mujer (tenant 1)

> Fuente de datos: Excel operativo de la empresa. Completar los `TODO` con el negocio; no inventar datos.

## Conocido (del plan)

- Negocio local en **Chimbote**. Público: mujeres; tono empático y humano.
- **47 servicios** en Excel `05_SERVICIOS` (nombre, precio, duración) → a JSON para RAG.
- Agenda en pestaña `02_CITAS`; promociones en `06_PROMOCIONES`.
- Reglas clínicas/seguridad en `07_APRENDIZAJES_INBOX`.
- Excel operativo verificado (2026-10-06): `Hola Mujer · MVP WhatsApp ManyChat · Operativo (1).xlsx` con hojas: `00_EMPEZAR` · `01_CONTACTOS` · `02_CITAS` · `03_EVENTOS` · `04_CONFIG` · `05_SERVICIOS` · `06_PROMOCIONES` · `07_APRENDIZAJES_INBOX` · `08_PLAN_IMPLEMENTACION` · `09_MUESTRA_INBOX_11D` · `MANYCHAT_SERVICE_SHEET`.
- Pagos por **Yape / Plin / BCP** (capturas de comprobante).
- Handoff humano a **Jioysi** (derivación por consultas médicas, reclamos o casos complejos).
- Operación previa en ManyChat (botones rígidos) — se reemplaza por el agente.

## Por completar

- TODO: catálogo exacto de servicios y vigencias de precios.
- TODO: horarios de atención reales y capacidad por servicio.
- TODO: políticas de reprogramación/cancelación y de pagos.
- TODO: FAQs frecuentes y objeciones comerciales.
- TODO: número(s) de WhatsApp y phone_number_id de Meta.

## Reglas de IA

- Nunca responder temas médicos: derivar (safety_agent).
- Precios y duraciones **solo** desde RAG; si no está en la base, no inventar.
