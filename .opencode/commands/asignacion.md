---
description: Carga mi asignación del día y dime por dónde empiezo
---
Eres el asistente de un practicante de 2.º año. Sigue el «Protocolo de asignación» de AGENTS.md.

Rama actual: !`git branch --show-current`
Issue indicado por el practicante (opcional): $ARGUMENTS

1. Deduce el número de Issue: de la rama `issue-N-slug`, del argumento (número o nombre) o, si estoy en `main` sin argumento, pregúntame solo mi nombre y búscalo en la columna *Alumno* de la tabla (paso 2). Mi asignación en GitHub ya está hecha y tú no puedes verla: no me pidas «aceptarla», no me mandes a pedir al monitor que me asigne el Issue y no me pidas pruebas de ello.
2. Lee `program/01_CURRICULUM/asignaciones/README.md` y localiza su contrato `S##_D#.md` y su paso a paso `S##_D#_paso_a_paso.md`. Lee solo esos dos archivos.
3. Dime en máximo 8 líneas: el objetivo (sección 1 del contrato), cuánto dura la sesión, y en qué paso del paso a paso debo empezar según lo que ya existe en mi repo (comprueba con `git status` y mirando si existen los archivos de la sección 4).
4. No escribas código de la solución. Termina preguntándome si ya hice el Paso 0.
