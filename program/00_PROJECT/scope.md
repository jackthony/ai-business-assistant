# Alcance

## Dentro del alcance

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

## Fuera del alcance

- Diagnóstico o consejo clínico (el bot deriva siempre a humano).
- Decisiones de precios/negocio sin validar con Hola Mujer o NeuraCode.
- Datos reales de clientes en repos o en contexto de IA (anonimizar siempre).
- Rediseñar scheduling/CRM propios: se integra lo existente (Cal.com, Sheets, ERP) cuando aplique.
- Compra de infraestructura cloud más allá de lo mínimo para el canal WhatsApp.
