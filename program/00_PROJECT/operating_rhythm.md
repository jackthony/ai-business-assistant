# Ritmo operativo del líder (primera vez liderando)

## Ciclo diario (3 días/semana)

- Arranque (10 min): cada practicante dice qué hará hoy, qué espera y qué le bloquea.
- El día se ejecuta contra **un Issue** (`issues_backlog.md`), no contra "avanzar".
- Cierre: commit/PR con evidencia y actualización del Issue.

## Ciclo semanal

- **Día 3 (viernes):**
  1. Llenar las 3 filas semanales en el Excel `EVALUACION` (30 min, criterios 1–5).
  2. Revisar PRs (DeepSeek como reviewer según `AGENTS.md` §Review).
  3. Anotar patrones de error en `program/05_EVALUATION/students/`.
  4. Actualizar `program/00_PROJECT/current_status.md`.

## Ciclo quincenal

- El **alumno** sustenta la tarea más significativa y presenta su **informe quincenal SENATI** en formato FPE (CNIU-108): por qué eligió la tarea, proceso, equipos/herramientas, seguridad/ATS y diagrama; el monitor escucha, da rumbo, firma y marca "Revisado por monitor".
- Revisar `SEGUIMIENTO_QUINCENAL` del Excel y ajustar el plan si un tema no quedó sólido.
- **Automatizado:** el workflow `informe-quincenal` (jueves por la noche o manual) crea/refresca 1 Issue-borrador por alumno con su registro semanal armado desde commits/PRs/Issues reales de GitHub (ya creados: #11 Allan, #12 Pilar, #13 Josue). El alumno solo completa horas, ATS, resultados y la justificación, y lo pasa al Word FPE. Su expediente en `program/05_EVALUATION/students/` es el respaldo (la misma estructura les sirve a los 3).

## Reglas del líder

1. No resolver el bloqueo por el practicante: dar pistas, exigir evidencia, dejar que cierre.
2. No cambiar el plan ni el stack a mitad de semana; toda decisión va a un ADR.
3. La evaluación se llena con evidencia (commits/PRs/demos), no con percepción.
4. Si el monitor no sabe algo: decirlo. Modelar la regla de evidencia (fuente primaria > opinión).

## Trampas de primera vez

- Prometer más alcance del que 3 practicantes pueden sostener.
- Adoptar cada framework nuevo que suena mejor (ver ADR-010).
- Hacer el trabajo "porque es más rápido" — a los 2 meses no saben nada.
- Confundir el conocimiento del negocio (KB-A) con el del programa (KB-P).
