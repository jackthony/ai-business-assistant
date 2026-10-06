# ADR-004: ChromaDB como vector store inicial (RAG)

- **Fecha:** 2026-10-06
- **Estado:** aceptada

## Contexto

El agente debe responder sobre 47 servicios (Hola Mujer) y cursos (NeuraCode) sin alucinar, con datos que viven en Excel.

## Problema

¿Qué base vectorial usar para el RAG local?

## Opciones

1. ChromaDB (embeddings locales, persistencia simple).
2. FAISS (librería, sin metadata cómodo).
3. pgvector (requiere Postgres desde el inicio).

## Decisión

ChromaDB con embeddings locales (nomic-embed-text/bge-m3 vía Ollama). Los datasets se derivan de los Excel a JSON versionado.

## Consecuencias

- RAG 100% local, sin costos por embedding.
- Ingesta reproducible por script (Issue #08 y #21).
- Si el volumen crece, se evalúa pgvector al migrar a Postgres (ADR-005) sin cambiar la interfaz.
