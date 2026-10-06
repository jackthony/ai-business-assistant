# Dominio: NeuraCode (tenant 2)

> Segundo tenant sobre el mismo núcleo. Completar los `TODO` con el negocio; no inventar datos.

## Conocido (del plan)

- **Academia de tecnología** (cursos, precios, temarios) — ingesta en S11 (#21).
- Comparte arquitectura con Hola Mujer; cambian system prompt, RAG y reglas (ADR de multitenant en `architecture.md`).
- Su línea receptora de WhatsApp define el tenant dinámicamente.
- Debe atender también notas de voz (HITO 3, S12).

## Por completar

- TODO: catálogo de cursos, temarios, precios y modalidades.
- TODO: proceso de inscripción/matrícula y requisitos.
- TODO: políticas de pago, descuentos y devoluciones.
- TODO: FAQs frecuentes.
- TODO: número(s) de WhatsApp / phone_number_id.

## Reglas de IA

- Respuestas solo desde el RAG de NeuraCode (namespace propio).
- No prometer descuentos ni fechas que no estén en la base.
