# Orquestador: ciclo con subagentes

> Para el monitor y para la sesión de Claude Code que orquesta. Lo ejecuta `/loop` sin intervalo (ritmo propio). Origen: #203.

## Idea

La sesión principal **solo orquesta**: lee informes cortos, decide, publica y comprueba. El trabajo lo hacen subagentes baratos (Haiku y Sonnet) con un harness estricto:

- **Lo determinista va en scripts** (`tools/orquestador/estado.py`, `tools/orquestador/contexto_pr.py`, `contrato_check`, las 4 puertas). El modelo solo juzga lo que un script no puede.
- **Punteros, no contenido**: cada subagente recibe un número de PR, una rama o una carpeta, y lee solo lo que dice su harness.
- **Salida con formato fijo y corto**, presupuesto de llamadas y **cero efectos hacia afuera**: los subagentes no comentan, no pushean y no mergean.

## Roles y modelos

| Rol | Harness | Modelo | Hace | Nunca |
|---|---|---|---|---|
| Orquestador | este archivo | sesión principal | planifica, decide, lanza subagentes, publica (comentarios, push, merge, estado de Issues) y comprueba | explorar el repo o leer diffs completos él mismo |
| Escáner | `.claude/agents/escaner.md` | Haiku | corre `estado.py`, resume y prioriza alertas | opinar de código, publicar |
| Revisor | `.claude/agents/revisor.md` | Sonnet | revisa un PR contra su contrato con `contexto_pr.py --gates` y sondas, y redacta la revisión | publicar, pushear, editar el repo |
| Arreglador | `.claude/agents/arreglador.md` | Sonnet | aplica un cambio ya aprobado en una rama local, con prueba antes/después y las puertas | pushear, reescribir historia, salirse de los archivos permitidos |
| Verificador | `.claude/agents/verificador.md` | Haiku | comprueba post-condiciones (CI, comentario, merge, Issue) | arreglar, publicar |

Si la sesión no lista estos tipos de agente, lanza `general-purpose` con `model` igual al del harness y la instrucción «Lee `.claude/agents/<rol>.md` completo y síguelo».

## Ciclo (una vuelta del loop)

1. **Revisar.** Lanza el escáner con `DESDE` igual al inicio del ciclo anterior (la primera vez, hace 72 h).
2. **Planificar.** Elige como máximo 3 acciones, en este orden de prioridad:
   1. CI rojo o bloqueo de un alumno (alerta A1, o un comentario de tipo «bloqueo») → revisor.
   2. Push de un alumno sin revisión (A2) → revisor.
   3. Pregunta de un alumno sin respuesta (A3) → la responde el orquestador; si es técnica, primero el revisor.
   4. Rama con commits sin PR (A4) o identidad de git mal configurada (A5) → aviso al alumno.
   5. Hueco o ambigüedad en un contrato → arreglador sobre el contrato, con Issue y PR propios.
   6. Asignación sin contrato o sin siguiente paso (A6), o alumno inactivo (A7) → propuesta al monitor. No reasignes sin él.
   7. `current_status.md` desactualizado (como mucho una vez al día) → arreglador.

   Si no hay nada, no lances nada más: programa el siguiente ciclo.
3. **Accionar.** Lanza los subagentes, en paralelo si son independientes y con `isolation: worktree` si editan. Lee su salida, decide y **publica tú** según las reglas de abajo.
4. **Comprobar.** Lanza el verificador con una post-condición por cada acción publicada.
5. **Registrar.** Escribe una línea por acción en la respuesta del ciclo: qué, a quién y la evidencia (#número o SHA).

## Reglas de publicación (las aplica solo el orquestador)

- **Comentarios a alumnos.** En español, por su nombre, con un siguiente paso concreto y el pie de Claude Code. Como mucho uno por alumno y por día, salvo que respondas una pregunta suya. Nunca repitas lo que ya dijo un comentario anterior.
- **Revisiones.** Formato de `AGENTS.md`: Resumen · Hallazgos [BLOCKER]/[MAJOR]/[MINOR] · Preguntas de comprensión · Recomendación. Pistas, no la solución del contrato.
- **Arreglos en el PR de un alumno.** Solo para hallazgos BLOCKER o MAJOR con una sonda que falla antes y pasa después. Van en un commit aparte en su rama, sin reescribir historia, y la revisión explica qué se cambió y por qué.
- **Merge de un PR de alumno.** Exige las cinco condiciones:
  - (a) check determinista ✅;
  - (b) `reglas-tbd` y `calidad` en verde en el head;
  - (c) veredicto APROBAR del revisor sobre ese mismo head;
  - (d) preguntas de comprensión respondidas por el alumno en el PR;
  - (e) sin conflictos.

  Usa squash. Usa rebase solo si el PR lo abrió el monitor y hay que conservar la autoría del alumno.
- **Contratos y documentos.** Issue propio, rama `issue-N-slug`, `Closes #N` en el PR, y validación con `tools/asignaciones/check_paths.py` y `tools/asignaciones/check_walkthrough.py`.
- **Nunca**:
  - force-push, ni rebase o amend de commits ya subidos;
  - aprobar el environment `revision-ia` (lo decide el monitor);
  - tocar secretos o datos reales de clientas;
  - tocar el Issue de otro alumno sin una justificación escrita;
  - reasignar trabajo sin el monitor.

## Criterios de salida («hasta mejorar»)

El loop termina cuando estas cinco condiciones se cumplen en **dos ciclos seguidos sin actividad nueva**, o cuando el monitor dice basta:

1. Cada alumno tiene un Issue activo con contrato vigente y un siguiente paso publicado.
2. Ningún PR de alumno tiene un push sin revisión de más de 24 h.
3. Ningún PR de alumno tiene CI rojo sin un comentario que explique qué falla.
4. Todo hueco de contrato detectado tiene su PR de corrección.
5. `current_status.md` está al día.

## Cadencia y presupuesto

- **En horario de práctica** (`.github/coach.json`: Josue lun–mié, Pilar y Allan mié–vie, de 08:00 a 17:30 Lima): un ciclo cada 20–30 min.
- **Fuera de ese horario**: un ciclo cada 60 min que solo corre el escáner; si no hay cambios, no lanza nada más.
- **Por ciclo**: como máximo 1 escáner, 2 revisores o arregladores y 1 verificador. El orquestador no lee diffs ni contratos completos: lee los informes.

## Plantillas para lanzar subagentes

- **Escáner**: `Sigue .claude/agents/escaner.md. DESDE=<ISO 8601>. FOCO=<opcional>.`
- **Revisor**: `Sigue .claude/agents/revisor.md. PR=<n>. WORKDIR=<carpeta temporal>. FOCO=<opcional>.`
- **Arreglador**: `Sigue .claude/agents/arreglador.md. RAMA_BASE=<origin/...>. RAMA_LOCAL=<...>. CAMBIOS=<F1..Fn aprobados>. ARCHIVOS_PERMITIDOS=<lista>. MENSAJE_COMMIT=<≤72>. TRAILERS=<líneas>. WORKDIR=<carpeta temporal>.`
- **Verificador**: `Sigue .claude/agents/verificador.md. POSTCONDICIONES: 1) ... 2) ...`
