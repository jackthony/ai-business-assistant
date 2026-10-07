El sistema sigue un flujo donde el mensaje de Meta llega a la API, pasa por el canal adaptado, es procesado por el agente (que consulta memoria, RAG y LLMs), y finalmente un servicio envía la respuesta de vuelta a WhatsApp. (Aun no se llega a esa parte)

Estructura de Capas (src/):

- api/ (Punto de Entrada): Expone la aplicación FastAPI. Actualmente opera el endpoint /health y alojará el endpoint /webhook para recibir los eventos externos.
- channels/ (Abstracción de Canales): Implementa el patrón adapter para que el sistema sea canal-agnóstico. Hoy maneja WhatsApp (validación GET y recepción POST); mañana permitirá integrar plataformas como TikTok sin alterar la lógica de negocio.
- agents/ (Orquestación del Flujo): Alberga los grafos de LangGraph que controlan el estado, las decisiones y el rumbo de cada conversación.
- tools/ (Capacidades del Agente): Define las herramientas específicas que los agentes pueden ejecutar, como la consulta de catálogos o servicios disponibles.
- rag/ (Base de Conocimiento): Gestiona ChromaDB para realizar búsquedas semánticas de servicios y promociones, segmentadas estrictamente por organización (tenant).
- memory/ (Persistencia de Contexto): Mantiene el historial de las conversaciones. Está diseñado para usar SQLite en la fase actual y migrar a PostgreSQL en producción.
- models/ (Conectores de LLM): Administra las conexiones a los modelos de lenguaje locales, integrando DeepSeek para texto y Qwen para capacidades de visión.
- services/ (Efectos Secundarios): Se encarga de las integraciones con herramientas externas para ejecutar acciones, tales como Google Calendar, Google Sheets y el envío final de mensajes.
- infrastructure/ (Soporte Técnico): Centraliza la configuración global del sistema, la gestión de logs (registros) y las métricas para el control de costos de computación.
