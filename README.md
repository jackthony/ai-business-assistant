# senati-ai-agents-context

Repositorio de **contexto, currículo y gestión** del programa de prácticas **HealthTech Software & AI — SENATI 2026** (ciclo 3 · practicantes: Allan, Pilar y Josue).

## Regla de oro

| Artefacto | Rol |
|---|---|
| **Este repo** | Fuente canónica de currículo, arquitectura, decisiones (ADRs) y evaluación |
| **Excel** `Plan Maestro — HealthTech Software & AI — SENATI 2026 (EVALUABLE).xlsx` | Registro de notas y seguimiento quincenal (lo llena el monitor) |
| **Repo de código** `ai-business-assistant` (pendiente) | El software real que desarrollan los practicantes |

Nada del plan se duplica fuera de este repo: si un artefacto contradice a otro, gana este repo.

## Estructura

| Carpeta | Contenido |
|---|---|
| `00_PROJECT/` | Visión, alcance, roadmap y **`current_status.md`** (leer siempre primero) |
| `01_CURRICULUM/` | Syllabus, plan de 16 semanas y backlog de Issues #01–#39 |
| `02_REFERENCE/` | Fuentes curadas: libro guía, LangGraph, Meta WhatsApp API, DeepSeek local |
| `03_ARCHITECTURE/` | Arquitectura objetivo + ADRs en `decisions/` |
| `04_DOMAIN/` | Dominio de negocio: Hola Mujer y NeuraCode |
| `05_EVALUATION/` | Rúbrica y expedientes individuales de alumnos |
| `09_AI_INSTRUCTIONS/` | Instrucciones para DeepSeek local (sistema, coding, review, evaluación) |

## Cómo usarlo con DeepSeek local

1. Leer `00_PROJECT/current_status.md` **siempre**.
2. Cargar solo 2–3 archivos de la tarea en curso (nunca el repo completo).
3. El protocolo completo está en `09_AI_INSTRUCTIONS/deepseek_system.md`.
