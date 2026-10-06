# ADR-008: DeepSeek local como motor principal

- **Fecha:** 2026-10-06
- **Estado:** aceptada

## Contexto

El programa se ejecuta en un M5 Pro con 24 GB de RAM unificada. Se busca minimizar costos y dependencia de APIs.

> **Nota (2026-10-06):** este ADR aplica al **runtime del producto** (la M5 del monitor). Los practicantes desarrollan en **PCs Windows más antiguas**: ahí corren solo modelos chicos de Ollama (1.5b–3b) o DeepSeek web gratis para dudas — nunca los modelos grandes. Ver `program/02_REFERENCE/deepseek-local.md`.

## Problema

¿Qué LLM usa el proyecto y las herramientas de tutoría?

## Opciones

1. APIs cloud (OpenAI/Anthropic) como motor principal.
2. DeepSeek local (Ollama) como principal + nube solo donde sea inevitable.
3. Híbrido sin política clara.

## Decisión

Opción 2. Motor principal: DeepSeek local en Ollama (ver `program/02_REFERENCE/deepseek-local.md`). Nube inevitable: WhatsApp Cloud API. Voz (faster-whisper) y visión (Qwen2.5-VL) locales; si el hardware no da, se evalúa nube caso a caso con un ADR.

## Consecuencias

- El plan v2 ya reemplazó Whisper API → faster-whisper y GPT-4o Vision → Qwen2.5-VL (hecho 2026-10-06); el fallback de S15 será entre modelos locales.
- Un modelo pesado a la vez; latencia a considerar en la UX del bot.
- Conectividad: el pipeline completo debe poder probarse offline (salvo webhook Meta).
