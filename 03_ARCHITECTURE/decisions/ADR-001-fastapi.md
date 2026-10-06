# ADR-001: FastAPI como backend

- **Fecha:** 2026-10-06
- **Estado:** aceptada

## Contexto

El proyecto necesita exponer un webhook para WhatsApp Cloud API y orquestar agentes en Python.

## Problema

¿Con qué framework construir el Integration Hub?

## Opciones

1. FastAPI (async, Pydantic, OpenAPI).
2. Flask (simple, sync).
3. Django (completo, pesado para este caso).

## Decisión

FastAPI. Async nativo (el webhook de Meta debe responder rápido), integración natural con Pydantic v2 y OpenAPI/Swagger para documentar.

## Consecuencias

- Los practicantes aprenden type hints y validación como base de todo.
- El envío saliente se hace con cliente HTTP async (`httpx`).
- OpenAPI/Swagger alimenta el criterio de documentación del S15.
