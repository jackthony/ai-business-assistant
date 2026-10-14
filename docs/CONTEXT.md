Este repositorio contiene un asistente de IA empresarial para WhatsApp desarrollado en HealthTech Software & AI (SENATI 2026). El sistema da servicio actualmente a dos organizaciones (Hola Mujer y NeuraCode) y está diseñado mediante un patrón adapter para permitir la migración a otros canales de comunicación en el futuro.

Componentes Técnicos y Estructura:

- Backend: Construido con FastAPI.
- Orquestación de Agentes: Implementada con LangGraph.
- Base de Datos (RAG): Utiliza ChromaDB.
- Modelo de Lenguaje: Ejecuta DeepSeek de forma local.
- Organización del proyecto: El código fuente reside en src/, mientras que la documentación del programa se encuentra en program/.
Estado del Proyecto y Seguridad
- Progreso actual: Se completó el servicio mínimo con el endpoint /health (Issue #2) y el siguiente paso es la implementación del webhook (Issue #3).
- Seguridad: El repositorio está libre de datos reales de clientes y credenciales; las variables de entorno se gestionan de forma segura a través de .env.example solo con nombres de referencia.

## Comandos rápidos (Windows PowerShell)

```powershell
# Entorno
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# Las 4 puertas
ruff check src tests
mypy src
pytest tests -q
bandit -r src -x tests -ll

# Correr la API
uvicorn api.main:app --reload

# Exponer con ngrok (pruebas de webhook)
ngrok http 8000
```
