# Reglas de review (PRs de practicantes)

Evalúa cada PR en este orden y entrega feedback con severidad `[BLOCKER] / [MAJOR] / [MINOR] / [NIT]`.

## Checklist

1. **Comprensión:** ¿el PR resuelve el Issue y sus criterios de aceptación exactos?
2. **Arquitectura:** ¿respeta `architecture.md` y los ADRs? ¿responsabilidades separadas?
3. **Python/Java:** type hints, nombres, sin duplicación evidente, manejo de errores.
4. **Testing:** ¿hay tests?, ¿cubren casos borde?, ¿se pueden correr?
5. **Seguridad:** sin secretos, sin datos reales, validación de entradas (prompt injection en tools).
6. **Calidad de agente:** prompts versionados, sin alucinación estructural, latencia razonable.
7. **Comprensión del alumno:** pídele que explique 2–3 decisiones del PR en el review.

## Formato de salida (por PR)

```
## Resumen
(1-3 líneas)

## Hallazgos
- [BLOCKER] ...
- [MAJOR] ...
- [MINOR] ...

## Preguntas de comprensión
1. ...

## Recomendación
Aprobar / Cambios menores / Rehacer
```

- Sé directo con el código, respetuoso con la persona.
- No reescribas el PR completo: guía con pistas y deja que el alumno lo corrija.
- Registra patrones de error para el expediente (`05_EVALUATION/students/`).
