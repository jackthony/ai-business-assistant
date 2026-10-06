# ADR-003: WhatsApp Cloud API (Meta) como único canal cloud

- **Fecha:** 2026-10-06
- **Estado:** aceptada

## Contexto

El negocio real vive en WhatsApp. Existe ManyChat operando hoy, pero se busca eliminar la rigidez de sus botones.

## Problema

¿Construir el canal o integrar el existente?

## Opciones

1. WhatsApp Cloud API oficial de Meta.
2. ManyChat como capa (mantener botones).
3. Librerías no oficiales (Baileys, etc.).

## Decisión

WhatsApp Cloud API directa. Es política de la plataforma, estable y con webhooks; ManyChat se reemplaza progresivamente (el material queda como referencia de flujos).

## Consecuencias

- Es la única dependencia de nube del proyecto (excepción acordada a "todo local").
- ngrok en desarrollo; deploy en S14. Requiere tokens en `.env` y plantillas aprobadas para mensajes proactivos.
