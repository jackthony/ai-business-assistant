# Asignaciones deterministas

Cada Issue de producción tiene aquí su **contrato de asignación** (`S05_D1.md`, `S05_D2.md`, …), escrito con la estructura de [`_PLANTILLA.md`](_PLANTILLA.md).

**Por qué existen.** Para que nadie se desvíe y todos aprendan lo mismo: entradas, archivos, pruebas, comandos y criterio de «hecho» están fijados de antemano, de modo que dos alumnos distintos entregan algo comparable y el monitor revisa contra una lista, no contra una opinión.

**Qué fijan y qué no.**
- Fijan el **QUÉ**: contrato público, tabla de pruebas, archivos a tocar, orden de pasos, preguntas de comprensión con su rúbrica.
- No escriben el **CÓMO**: la implementación y las decisiones de diseño son del alumno. Si un contrato te dice la implementación línea por línea, está mal escrito: repórtalo en el Issue.

**Cómo se usan.**
1. El Issue del día enlaza su archivo `S##_D#.md`; ese archivo manda sobre cualquier resumen del Issue.
2. Se lee en orden (secciones 1–12). Las pruebas (sección 6) se escriben primero.
3. En el PR se responden las preguntas de la sección 11. El monitor revisa que cada respuesta cubra los puntos de «tu respuesta debe mencionar».
4. Si una instrucción no se puede ejecutar tal cual (ruta inexistente, comando que falla en Windows), se reporta en el Issue con el error pegado; el monitor corrige el contrato.

## Issue → contrato

| Issue | Contrato | Tema | Depende de |
|---|---|---|---|
| #52 | [`S05_D1.md`](S05_D1.md) | Grafo mínimo con estado explícito (`AgentState`, nodo eco, CLI) | — |
| #53 | [`S05_D2.md`](S05_D2.md) | Prompt por componentes + LLM detrás de un puerto + verificación de respuesta + grafo de conversación (`START → respond → END`, archivo nuevo) | #52 en `main` (usa `src/agents/state.py`; no toca los archivos de #52) |
| #54 | [`S05_D3.md`](S05_D3.md) | Memoria persistente por teléfono (`SqliteSaver`, `thread_id`) | #52 en `main` |

Una asignación que depende de otra **no se empieza** hasta que la anterior esté mergeada en `main` (`git pull` y comprueba que existen sus archivos). Si ves a un compañero bloqueado por eso, ofrécele ayuda con `apoyo`.

## Con OpenCode

El repo encamina a tu asistente: `AGENTS.md` (se carga solo) trae el «Protocolo de asignación» y `.opencode/commands/` trae cinco comandos: `/asignacion` (carga tu contrato y por dónde empezar), `/paso N`, `/pista`, `/revisar` (tu `git diff` contra el contrato) y `/comprension` (ensayo de las preguntas del PR). Si OpenCode se cuelga: [guía de solución](../../02_REFERENCE/opencode-solucion-problemas.md).

## Para el monitor

- Cada contrato `S##_D#.md` sigue [`_PLANTILLA.md`](_PLANTILLA.md); cada paso a paso `S##_D#_paso_a_paso.md` sigue [`_PASO_A_PASO_PLANTILLA.md`](_PASO_A_PASO_PLANTILLA.md).
- Verificadores (solo librería estándar): `python tools/asignaciones/check_paths.py . <archivo.md>` lista las rutas citadas que no existen; `python tools/asignaciones/check_walkthrough.py <contrato.md> <paso_a_paso.md>` comprueba que cada prueba del contrato tenga su paso y que no se regale la solución.

**Fuente canónica.** Estos archivos son la fuente; `issues_backlog.md` mantiene el resumen que genera el Issue dominical.
