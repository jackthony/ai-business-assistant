# Reglas de código (repo producto)

## General

- Python 3.11+; type hints en todo lo público; Pydantic v2 para contratos.
- Sin secretos en código: `.env` + `.env.example`; tokens `META_*`, `OLLAMA_*`.
- Sin `print` para debug: logging estructurado; logs sin datos personales.
- Nada de código muerto ni TODOs sin Issue asociado.

## Flujo TBD

- 1 Issue = 1 branch `issue-NN-slug` = 1 PR. Branches de horas o pocos días.
- Commits pequeños, en imperativo, referenciando `#NN` cuando aplique.
- Antes del PR: `pytest` verde + `ruff check` limpio.
- PR describe: qué, por qué, cómo se probó, Issue que cierra.

## FastAPI/agentes

- Async por defecto; los I/O (Meta, Ollama, DB) nunca bloquean el event loop.
- Tools `@tool` con schemas Pydantic estrictos; validar entradas y salidas.
- Cada nodo del grafo: función pura con estado explícito; efectos secundarios en services.
- Tests: cada tool y cada nodo con casos válidos, inválidos y de borde.

## Java (S1–S3, exigencia SENATI)

- Java 17 + Maven; JUnit 5; commits y PR igual que en Python.
