# Asignaciones deterministas

Cada Issue de producción tiene aquí su **contrato de asignación** (`S05_D1.md`, `S05_D2.md`, …), escrito con la estructura de [`_PLANTILLA.md`](_PLANTILLA.md).

**Por qué existen.** Para que nadie se desvíe y todos aprendan lo mismo: entradas, archivos, pruebas, comandos y criterio de «hecho» están fijados de antemano, de modo que dos alumnos distintos entregan algo comparable y el monitor revisa contra una lista, no contra una opinión.

**Qué fijan y qué no.**
- Fijan el **QUÉ**: contrato público, tabla de pruebas, archivos a tocar, orden de pasos, preguntas de comprensión con su rúbrica.
- No escriben el **CÓMO**: la implementación y las decisiones de diseño son del alumno. Si un contrato te dice la implementación línea por línea, está mal escrito: repórtalo en el Issue.

**Cómo se usan.** (El *paso a paso* es la guía para trabajar sin perderte: mini-conceptos, un paso por prueba, escalera de pistas. No reemplaza al contrato.)
1. El Issue del día enlaza su archivo `S##_D#.md`; ese archivo manda sobre cualquier resumen del Issue.
2. Se lee en orden (secciones 1–12). Las pruebas (sección 6) se escriben primero.
3. En el PR se responden las preguntas de la sección 11. El monitor revisa que cada respuesta cubra los puntos de «tu respuesta debe mencionar».
4. Si una instrucción no se puede ejecutar tal cual (ruta inexistente, comando que falla en Windows), se reporta en el Issue con el error pegado; el monitor corrige el contrato.

## Issue → contrato

| Issue | Contrato | Paso a paso | Tema | Alumno (GitHub) | Depende de |
|---|---|---|---|---|---|
| #52 | [`S05_D1.md`](S05_D1.md) | [`S05_D1_paso_a_paso.md`](S05_D1_paso_a_paso.md) | Grafo mínimo con estado explícito (`AgentState`, nodo eco, CLI) | Josue (`adbon-dm1`) | — |
| #53 | [`S05_D2.md`](S05_D2.md) | [`S05_D2_paso_a_paso.md`](S05_D2_paso_a_paso.md) | Prompt de Hola Mujer **por componentes** (`prompt_v1.md`: 5 piezas + cargador) y verificación de estilo de las respuestas (`check_reply_style`) | Pilar (`estefanyP-hub`) | — |
| #54 | [`S05_D3.md`](S05_D3.md) | [`S05_D3_paso_a_paso.md`](S05_D3_paso_a_paso.md) | Memoria persistente por teléfono sobre el agente real (`SqliteSaver`, `thread_id`; el bot derivado sigue callado tras un reinicio) | Allan (`WhoAllan`) | — |
| #156 | [`S06_D1.md`](S06_D1.md) | [`S06_D1_paso_a_paso.md`](S06_D1_paso_a_paso.md) | Ejemplos (few-shot) para objeciones, `prompt_v2` sin activar y comparación de estilo v1/v2 (`compare_prompts`) | Josue (`adbon-dm1`) | **#177** (base del monitor): `prompt_v1.md` y `check_reply_style` |
| #157 | [`S06_D2.md`](S06_D2.md) | [`S06_D2_paso_a_paso.md`](S06_D2_paso_a_paso.md) | Ingesta reproducible del RAG (huella del corpus y CLI) y evaluación de la recuperación (preguntas de oro, calibración de `RAG_MAX_DISTANCE`) | Josue (`adbon-dm1`) | — |
| #158 | [`S06_D3.md`](S06_D3.md) | [`S06_D3_paso_a_paso.md`](S06_D3_paso_a_paso.md) | Contrato de canal (`InboundEvent`/`OutboundReply`, ADR-011), despachador y canales web y Telegram sobre el mismo agente | Josue (`adbon-dm1`) | — |
| #184 | [`S07_D2.md`](S07_D2.md) | [`S07_D2_paso_a_paso.md`](S07_D2_paso_a_paso.md) | Herramienta `consultar_servicio` (LangChain `StructuredTool`, N1) sobre el catálogo real, con errores tipados y sin citar duraciones no verificadas | Allan (`WhoAllan`) | — |
| #185 | [`S07_D3.md`](S07_D3.md) | [`S07_D3_paso_a_paso.md`](S07_D3_paso_a_paso.md) | Oferta proactiva de 2–3 horarios libres cuando falta fecha u hora y pruebas de colisión | Josue (`adbon-dm1`) | — |
| #3 | [`S04_D2.md`](S04_D2.md) | [`S04_D2_paso_a_paso.md`](S04_D2_paso_a_paso.md) | Webhook de WhatsApp con fixtures: verificación GET, firma HMAC del cuerpo crudo, conversión a `InboundEvent` y respuesta en segundo plano | Pilar (`estefanyP-hub`) | — |

Los contratos S06 (#156–#158) se verificaron con pruebas y una solución de referencia. El #53 se cerró cuando la base del prompt entró por #178. La práctica vigente de Pilar es #3 y parte de la etiqueta `tdd-issue-3`.

## Issues pendientes de contrato

Antes de iniciar un cambio de producto, el Issue debe enlazar un contrato con comportamiento observable, archivos previstos y comandos que ejecuten sus pruebas. Para entregar, conserva el commit de pruebas previo al código, la salida en rojo y las mismas pruebas en verde. Usa datos sintéticos.

Si el Issue ya está en la tabla, usa el contrato allí enlazado. Para un Issue nuevo, guarda `issue-N.md` en esta carpeta con tres secciones:

- **Comportamiento** describe qué resultado se debe observar.
- **Archivos** enumera entre acentos graves las rutas de producto que se pueden cambiar.
- **Pruebas** incluye las rutas de pruebas entre acentos graves y el comando para ejecutarlas, por ejemplo `pytest tests/test_ejemplo.py -q`.

El primer commit puede incluir el contrato nuevo y la prueba. La puerta `calidad` comprueba el Issue vinculado, el alcance y que una prueba indicada en el contrato cambie en un commit separado, anterior al código. Después corre la suite sobre el resultado final. Pega en el PR el fallo inicial y la salida final para que el revisor pueda comprobar el ciclo completo.

| Issues abiertos | Qué falta concretar para escribir sus pruebas |
|---|---|
| #183 | Separar ubicación y CTA de la respuesta comercial que depende de Jioysi. |
| #210, #211 | Acordar datos mínimos y estado del lead ficticio. Definir qué se verifica en una escritura simulada y en su reintento. |
| #212 | Definir el flujo sintético y las métricas locales antes de instrumentar en la M5. |
| #224 | Acordar el resultado esperado para consultas ambiguas y fijar la matriz de casos. |
| #225, #226 | Definir la reanudación con avisos simulados y los escenarios de cierre del HITO 2 que pueden ejecutarse localmente. |

**La asignación ya está hecha:** la columna *Alumno* es la fuente. Tu asistente no puede ver GitHub, así que no te pide «demostrarla»: si dices tu nombre o tu Issue, confía en ti y sigue con tu contrato. Nunca debe mandarte a pedir al monitor que te asigne el Issue; si de verdad no encuentras tu Issue en la tabla, repórtalo en el Issue o en el grupo.

Una asignación que depende de otra **no se empieza** hasta que la anterior esté mergeada en `main` (`git pull` y comprueba que existen sus archivos). Si ves a un compañero bloqueado por eso, ofrécele ayuda con `apoyo`.

## Revisión automática del avance

Subir el trabajo a medias es parte del método. Al hacer `git push` de tu rama `issue-N-*`, el robot `pr-borrador` abre un PR en borrador con `Closes #N` (solo para alumnos del roster, `.github/coach.json`). En cada push, `revision-guiada` compara tu diff con tu contrato y **actualiza un único comentario**: archivos de la sección 4 trabajados/faltantes y fuera de contrato (cálculo exacto, sin IA) y, si hay clave de DeepSeek, un tutor que dice qué va bien, qué corregir citando la sección, cuál es el siguiente paso y hace preguntas de comprensión. No escribe la solución y no pone nota: la nota la decide el monitor.

## Con OpenCode

El repo encamina a tu asistente: `AGENTS.md` (se carga solo) trae el «Protocolo de asignación» y `.opencode/commands/` trae cinco comandos: `/asignacion` (carga tu contrato y por dónde empezar), `/paso N`, `/pista`, `/revisar` (tu `git diff` contra el contrato) y `/comprension` (ensayo de las preguntas del PR). Si OpenCode se cuelga: [guía de solución](../../02_REFERENCE/opencode-solucion-problemas.md).

## Para el monitor

- Cada contrato `S##_D#.md` sigue [`_PLANTILLA.md`](_PLANTILLA.md); cada paso a paso `S##_D#_paso_a_paso.md` sigue [`_PASO_A_PASO_PLANTILLA.md`](_PASO_A_PASO_PLANTILLA.md).
- Verificadores (solo librería estándar): `python tools/asignaciones/check_paths.py . <archivo.md>` lista las rutas citadas que no existen; `python tools/asignaciones/check_walkthrough.py <contrato.md> <paso_a_paso.md>` comprueba que cada prueba del contrato tenga su paso y que no se regale la solución.

**Fuente canónica.** Estos archivos son la fuente; `issues_backlog.md` mantiene el resumen que genera el Issue dominical.
