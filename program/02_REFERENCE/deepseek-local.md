# DeepSeek local — motor principal del producto

## Máquinas del equipo (dos perfiles distintos)

| Máquina | Rol | Qué corre |
|---|---|---|
| **M5 Pro** (24 GB, macOS) — del monitor | **Runtime del producto** (desde S5): Ollama + voz + visión; review del monitor | Los modelos grandes de abajo |
| **PCs Windows de los practicantes** (más antiguas) | **Desarrollo diario**: FastAPI, tests, git (S4 no requiere LLM para #2/#3/#4) | Solo modelos chicos (según RAM) o **DeepSeek web gratis** |

**Regla:** los modelos grandes (14b/16b) **no corren** en las PCs de los chicos. El grafo del producto se conecta a Ollama **en la M5**, no en sus máquinas. Para dudas/tutoría en sus PCs:

- ≤8 GB RAM: `qwen2.5-coder:1.5b` o `deepseek-r1:1.5b` (completar, dudas simples).
- 16 GB RAM: `qwen2.5-coder:3b` o `deepseek-r1:7b`.
- Si nada corre fluido: **DeepSeek web gratis (chat.deepseek.com)** con el protocolo de contexto de abajo — sin API key, sin costo.

## Modelos del runtime (Ollama, Metal en macOS — M5 Pro)

| Rol | Modelo sugerido | Tamaño Q4 aprox. | Uso |
|---|---|---|---|
| Código (principal) | `deepseek-coder-v2:16b` | ~10 GB | Implementar Issues, refactors |
| Alternativa con mejor tool-calling | `qwen2.5-coder:14b` | ~9 GB | Agentes con tools Pydantic |
| Razonamiento/evaluación | `deepseek-r1:14b` | ~9 GB | Reviewer, LLM-as-a-Judge |
| Visión/OCR comprobantes | `qwen2.5vl:7b` | ~6 GB | Capturas Yape/Plin/BCP |
| Embeddings RAG | `nomic-embed-text` o `bge-m3` | ~1 GB | ChromaDB |
| Voz | `faster-whisper` (large-v3-turbo) | ~1.5 GB | Transcripción notas de voz |

**Regla de hardware:** 24 GB son suficientes, pero cargar **un modelo grande a la vez**. Voz y visión se procesan en secuencia, no en paralelo con el LLM principal. (Aplica a la M5, no a las PCs Windows de los practicantes.)

## Protocolo de contexto (obligatorio)

1. Leer `program/00_PROJECT/current_status.md`.
2. Cargar solo el Issue + 2–3 archivos de la tarea (ej.: `issues_backlog.md` + `architecture.md` + el módulo a tocar).
3. Nunca cargar el repo completo ni sus 45+ archivos. Si falta contexto, pedirlo selectivamente.

## Modos de uso

- **Tutor:** explica conceptos al practicante (S1–S3 en especial).
- **Developer:** implementa Issues con propuesta previa de archivos a tocar y espera aprobación.
- **Reviewer:** evalúa PRs contra `AGENTS.md` (sección review).

## Nube vs local

- Local: todo el pipeline LLM, RAG, memoria, voz, visión.
- Nube (inevitable): WhatsApp Cloud API. Opcional: APIs pagas de visión/LLM si el hardware no da — decisión caso a caso.
