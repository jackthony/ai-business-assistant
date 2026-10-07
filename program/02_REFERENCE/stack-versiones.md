# Stack y versiones — decisiones ya tomadas (no las re-decidas)

> Definido por el monitor con el contexto completo del programa. Si algo aquí contradice un tutorial de internet, **manda este documento**. Duda real → pregunta en el grupo antes de cambiar algo.

## Definiciones técnicas

| Pieza | Decisión | Por qué |
|---|---|---|
| **Python** | **3.11** (3.11.x) | El CI ya usa 3.11 y el stack (LangGraph, ChromaDB) está verificado ahí. No uses 3.12/3.13 aunque tu PC lo traiga. `.python-version` en el repo lo fija para pyenv. |
| Entorno | `venv` simple (`python -m venv .venv`) | Menos piezas que poetry/conda; el CI instala igual. |
| Toolchain (local = CI) | `ruff` `mypy` `pytest` `bandit` | Las 4 puertas obligatorias; el CI las instala sin pinear. |
| Web | FastAPI + Uvicorn | ADR-001. |
| HTTP cliente | `httpx` (async) | Estándar moderno; `requests` no. |
| Config | `python-dotenv` + `.env` (nunca al repo) | `.env.example` sí va al repo. |
| Grafo (S5+) | `langgraph` + `langchain-core` + `langchain-ollama` | ADR-002; se conecta a **Ollama en la M5**, no en tu PC. |
| RAG (S6+) | `chromadb` local + embeddings `nomic-embed-text` (o `bge-m3`) | ADR-004. |
| ETL (S6) | `openpyxl` para leer el Excel | Solo lectura; datos del negocio jamás al repo. |
| Formato/lint | Config por defecto de `ruff`; `mypy --ignore-missing-imports` | No inventar configuraciones propias todavía. |
| Contrato HTTP | **OpenAPI autogenerado** por FastAPI (`/docs`, `/openapi.json`) — fuente de verdad y pruebas manuales con `/docs` + `curl` | Postman/Insomnia/Bruno opcionales: sus colecciones no se versionan como contrato (pueden divergir). |
| Método de trabajo | **Contract-first en fronteras** (Pydantic primero) + **TDD pragmático** (test del criterio antes/junto a la implementación) — ver `estandares.md` §3 | No escribir specs a mano ni tests "de relleno" después. |

**Rangos de dependencias aceptados** (cuando los necesites, en `pyproject.toml`):
`fastapi>=0.115,<1` · `uvicorn[standard]>=0.30,<1` · `httpx>=0.27,<1` · `python-dotenv>=1,<2` · `langgraph>=0.2,<1` · `langchain-core>=0.3,<1` · `langchain-ollama>=0.2,<1` · `chromadb>=0.5,<1` · `openpyxl>=3.1,<4`

**Claves de `.env.example`** (S4): `APP_ENV` · `WHATSAPP_VERIFY_TOKEN` · `WHATSAPP_APP_SECRET` · `WHATSAPP_TOKEN` · `WHATSAPP_PHONE_NUMBER_ID` · `LOG_LEVEL` (opcional). Valores de ejemplo/vacíos, nunca reales.

**Comandos Windows** (PCs de practicantes):
```
py -3.11 -m venv .venv
.venv\Scripts\activate
python --version            # debe decir 3.11.x
pip install ruff mypy pytest bandit fastapi uvicorn httpx python-dotenv
ruff check src tests && mypy src --ignore-missing-imports && pytest tests -q && bandit -r src -ll
```

## Herramientas gratuitas y sus límites (no se paga nada)

| Herramienta | Límite gratis | Nuestro uso |
|---|---|---|
| GitHub Actions | Repo **público** → minutos **ilimitados** (runners estándar) | Todo el CI: gracias a esto el repo es público |
| Codespaces | 60 h/mes (cuenta personal, máquina 2-core) | Opcional, para PCs muy lentas |
| ngrok | 1 túnel, URL aleatoria por sesión | Probar el webhook en S4; alternativa sin cuenta: `cloudflared tunnel --url http://localhost:8000` |
| Ollama | Gratis, local | Modelos grandes SOLO en la M5 (runtime); en PC Windows solo 1.5b–3b para práctica |
| DeepSeek web | Gratis (chat) | Dudas puntuales sin tocar código |
| DeepSeek API | **Pagada** (cuenta del monitor) | Solo el reviewer del CI; jamás en la app |
| OpenCode | Modelos gratis | Asistente de código con **presupuesto por sesión** (ver protocolo en `pack_contexto.md`) |

## Sin decisión pendiente para el practicante

Si aparece una elección no listada (otra librería, otro gestor, otro modelo): **no improvises** — trabaja con lo definido y pregunta en el grupo. Nosotros lo decidimos y actualizamos este archivo.
