# DeepSeek local — motor principal (M5 Pro, 24 GB)

## Modelos (Ollama, Metal en macOS)

| Rol | Modelo sugerido | Tamaño Q4 aprox. | Uso |
|---|---|---|---|
| Código (principal) | `deepseek-coder-v2:16b` | ~10 GB | Implementar Issues, refactors |
| Alternativa con mejor tool-calling | `qwen2.5-coder:14b` | ~9 GB | Agentes con tools Pydantic |
| Razonamiento/evaluación | `deepseek-r1:14b` | ~9 GB | Reviewer, LLM-as-a-Judge |
| Visión/OCR comprobantes | `qwen2.5vl:7b` | ~6 GB | Capturas Yape/Plin/BCP |
| Embeddings RAG | `nomic-embed-text` o `bge-m3` | ~1 GB | ChromaDB |
| Voz | `faster-whisper` (large-v3-turbo) | ~1.5 GB | Transcripción notas de voz |

**Regla de hardware:** 24 GB son suficientes, pero cargar **un modelo grande a la vez**. Voz y visión se procesan en secuencia, no en paralelo con el LLM principal.

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
