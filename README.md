# ai-business-assistant — Programa SENATI 2026 + Producto

Repositorio único: **programa de prácticas** (currículo, evaluación, gestión) **+ producto** (`src/` desde S4) — HealthTech Software & AI · SENATI 2026 · ciclo 3 (Allan, Pilar y Josue).

## Regla de oro

| Artefacto | Rol |
|---|---|
| **Este repo** (`ai-business-assistant`) | Fuente canónica: programa (currículo, ADRs, evaluación) + producto (`src/` desde S4) |
| **Excel EVALUABLE** | Notas numéricas y seguimiento quincenal (Drive; binario) |
| **Google Drive** | Distribución: Excel, PDFs e informes SENATI |

Nada del plan se duplica fuera de este repo: si un artefacto contradice a otro, gana este repo.

## Las tres bases de conocimiento (no confundir)

| Base | Qué es | Dónde vive | Quién la usa |
|---|---|---|---|
| **1. KB-P · Proyecto** | Currículo, arquitectura, ADRs, rúbrica, expedientes. Curada a mano. Fuente canónica. | **Este repo** | Monitor + practicantes + DeepSeek (2–3 archivos por tarea) |
| **2. KB-A · Agentes** | Datos de negocio para RAG: 47 servicios, promociones, cursos. Un namespace por tenant. | Repo de código: `data/` + ChromaDB (`configs/hola_mujer`, `configs/neuracode`) | El bot en runtime — **nunca** se usa para gestionar el programa |
| **3. KB-T · Transitoria** | 2–3 archivos por tarea (current_status + Issue + módulo/documento). | Se arma al momento en DeepSeek/IDE | El monitor y los practicantes al programar o evaluar |

Reglas: **KB-A nunca contiene docs del programa**; **KB-P nunca contiene precios/listas reales de clientes** (eso va al Excel operativo o a KB-A); **KB-T nunca incluye el repo completo**. Mezclarlas rompe seguridad, calidad del RAG y la memoria de DeepSeek.

## Estructura

| Carpeta | Contenido |
|---|---|
| `00_PROJECT/` | Visión, alcance, roadmap y **`current_status.md`** (leer siempre primero) |
| `01_CURRICULUM/` | Syllabus, plan de 16 semanas y backlog de Issues #01–#39 |
| `02_REFERENCE/` | **`source_map.md`** (jerarquía de fuentes + kit de rescate) y guías por tema |
| `03_ARCHITECTURE/` | Arquitectura objetivo + ADRs en `decisions/` |
| `04_DOMAIN/` | Dominio de negocio: Hola Mujer y NeuraCode |
| `05_EVALUATION/` | Rúbrica y expedientes individuales de alumnos |
| `AGENTS.md` (raíz) | Instrucciones para cualquier agente de IA (protocolo, coding, review, evaluación) |

## Cómo usarlo con DeepSeek local

1. Leer `00_PROJECT/current_status.md` **siempre**.
2. Cargar solo 2–3 archivos de la tarea en curso (nunca el repo completo).
3. El protocolo completo está en `AGENTS.md` (raíz del repo).
