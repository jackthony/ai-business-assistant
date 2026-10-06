# Alcance

## Dentro del alcance

- 48 sesiones (16 semanas × 3 días) y Issues #01–#39 del backlog.
- Backend propio: FastAPI + LangGraph + ChromaDB + memoria persistente.
- Canal WhatsApp Cloud API (Meta) — única dependencia de nube obligatoria.
- Multitenant: Hola Mujer y NeuraCode sobre el mismo núcleo con configs separadas.
- Multimodal local: transcripción de voz (faster-whisper) y visión para comprobantes (Qwen2.5-VL).
- Evaluación semanal/quincenal + informes SENATI.

## Fuera del alcance

- Diagnóstico o consejo clínico (el bot deriva siempre a humano).
- Decisiones de precios/negocio sin validar con Hola Mujer o NeuraCode.
- Datos reales de clientes en repos o en contexto de IA (anonimizar siempre).
- Rediseñar scheduling/CRM propios: se integra lo existente (Cal.com, Sheets, ERP) cuando aplique.
- Compra de infraestructura cloud más allá de lo mínimo para el canal WhatsApp.
