# GUÍA PRACTICANTE — cómo trabajar en este repo

> Léela entera una vez (10 min). Después, ante cualquier duda: **tu Issue es la ley** y las fuentes de tu semana están en la tabla "Materiales por semana" del plan.
>
> **Días de práctica:** Josue lun–mar–mié · Pilar y Allan mié–jue–vie. Tus Issues de la semana **aparecen solos el domingo por la noche**; D1/D2/D3 son tus 3 sesiones de la semana, no días fijos del calendario.

## 1. Tu panorama (dónde ves todo)

| Qué | Dónde |
|---|---|
| Repo (público) | https://github.com/jackthony/ai-business-assistant |
| **Tus asignaciones** | Board https://github.com/users/jackthony/projects/3 (solo lectura, campo `Alumno`) + pestaña Issues → **Assigned to me** |
| Tu Issue del día | asignado a ti (#2/#3/#4 esta semana) — los **criterios de aceptación son lo que se evalúa** |
| Tu expediente | `program/05_EVALUATION/students/<tu-nombre>.md` (lo llena el monitor) |
| Tu progreso automático | Issue "Digest semanal — …" (viernes) + "📄 Borrador de informe quincenal — …" (#11–#13, se refresca cada noche mar–vie) |

## 2. Primer día: descargar y preparar

1. Aceptar la invitación de colaborador (correo de GitHub).
2. `git clone https://github.com/jackthony/ai-business-assistant.git && cd ai-business-assistant`
3. Entorno (**Windows — tu caso**): `py -3.11 -m venv .venv` y activa con `.venv\Scripts\activate` (PowerShell: `.venv\Scripts\Activate.ps1`); luego `pip install -e ".[dev]"` (o `uv sync`); si aún no hay `pyproject.toml`, `pip install -r requirements.txt`. En macOS/Linux: `python -m venv .venv && source .venv/bin/activate`.
4. `pip install pre-commit && pre-commit install` → ruff y el formateo corren solos en **cada commit**.
5. `copy .env.example .env` (Windows) / `cp .env.example .env` (macOS) — el `.env` jamás se commitea.
6. **Tu IA de apoyo:** tu PC no corre los modelos grandes del proyecto (esos viven en la M5 del monitor). Para dudas instala Ollama con un modelo chico según tu RAM (`qwen2.5-coder:1.5b` si tienes 8 GB, `:3b` si 16 GB) o usa **DeepSeek web gratis** (chat.deepseek.com). Detalle: `program/02_REFERENCE/deepseek-local.md`.

## 3. Antes de codear (10 min, obligatorio)

1. `program/00_PROJECT/current_status.md` — dónde está el proyecto HOY.
2. Tu Issue del día y sus criterios de aceptación.
3. Tus fuentes: tabla **"Materiales por semana"** en `program/01_CURRICULUM/16_week_plan.md` + mapa `program/02_REFERENCE/source_map.md`. Lee, revisa, investiga; si contradicen algo, gana la doc oficial.
4. Si usas IA (DeepSeek web, ChatGPT o un agente): pégale **solo** `AGENTS.md` + `GUIA_AGENTE.md` + tu Issue + la guía de tu semana. Nunca el repo completo. En S4 (#2/#3/#4) la IA es para dudas y revisar tu código, no para que te haga el Issue entero: las preguntas de comprensión del Issue y del PR demuestran que lo entiendes tú.
5. **Trabajo en equipo (orden de consulta):** 1) tu Issue + docs oficiales → 2) un compañero (mira sus PRs, comenta constructivo, usa `apoyo`) → 3) el grupo → 4) el monitor. Anota en el PR a quién consultaste o ayudaste.
6. **La puerta de comprensión:** antes de subir o completar tu semana, responde las preguntas de comprensión **con tus palabras** y prepárate para explicarle al LT qué hiciste, por qué y qué probaste. Si no puedes explicarlo, no está listo: vuelve a leer.

## 4. Trabajar con TBD (correcto, sin excepciones)

1. Actualizar: `git pull origin main`.
2. Rama: `git switch -c issue-N-<slug>` (ej. `issue-2-setup-fastapi`). Patrón válido: `(tbd|issue)-N-<slug>`.
3. Commits en **convención estricta** (sección de abajo). **Sin límite de cantidad**: pushea cuantas veces necesites — cada push respalda tu trabajo y dispara el CI. El merge squash une todo en `main`.

### Commits (convención estricta — la valida `tbd-guardian`)

```
tipo(alcance): verbo en imperativo, sin punto final, ≤72 caracteres

[cuerpo opcional: por qué, decisiones, y Refs: #NN]
```

- **Tipos:** `feat` (nuevo), `fix` (arreglo), `docs`, `test`, `refactor`, `ci`, `chore`, `perf`, `style`.
- **Imperativo:** "agrega", "valida", "corrige" — nunca "agregado", "agregando".
- **1 commit = 1 cambio atómico**: si el mensaje dice "y" (dos cosas), divídelo en dos commits.
- **Alcance** (opcional): el módulo (`(api)`, `(webhook)`, `(tests)`).
- El cuerpo explica el POR QUÉ cuando no es obvio; `Refs: #N` enlaza el Issue.
- **Prohibido:** `fix`, `update`, `cambios`, `wip`, `final`, mensajes con fecha, o terminar en punto.
- Buenos: `feat(api): agrega endpoint /health` · `test: cubre 405 en POST /health` · `fix(sender): reintenta una vez ante error de red`.
- Malos: `arreglando cosas` · `update` · `feat: agrega /health y .gitignore.` (dos cambios + punto).
- Tu agente (DeepSeek/ChatGPT) también debe seguir esta convención: revísale cada mensaje antes de pushear.
4. Tests que cubran los **criterios del Issue** (casos borde incluidos). Antes de pushear corre las 4 puertas:
   `ruff check src tests && mypy src --ignore-missing-imports && pytest tests -q && bandit -r src -x tests -ll`
5. `git push -u origin issue-N-<slug>` **cuantas veces quieras** (cada push corre el CI y queda respaldado) y abre el PR con la plantilla: sección "Cómo se probó", checklist, evidencia (captura/video) y **`Closes #N` en el cuerpo**. ¿Aún no está listo? Ábrelo como **Draft** y conviértelo cuando termines.
6. Espera CI verde (4 puertas + chequeo de capas de `estandares.md`) y el review del monitor. **Ambos checks son obligatorios para mergear**: `guardian-tbd / reglas-tbd` y `CI estricto / calidad`. Si el repo tiene `DEEPSEEK_API_KEY`, DeepSeek deja un primer pase de review automático en tu PR (y la ficha del PR muestra un chequeo automático de estándares); la nota final la pone el monitor. El merge es **squash** a `main`; la rama muere y el Issue se cierra solo.

**Qué NO hacer (lo vigila `tbd-enforcer` automáticamente):**
- Push directo a `main` → **se revierte** y se te avisa.
- PR sin `Closes #N` o rama mal nombrada → el guardián **lo bloquea**.
- PR abierto **>7 días** sin actividad → **se cierra solo** (a los 4 días te llega un recordatorio; tu semana de práctica dura 3 días).
- **Cerrar un Issue sin terminar la tarea ni justificarlo → se REABRE solo** (`issue-closed`): ciérralo con su PR mergeado (`Closes #N`) o escribe el argumento en un comentario antes de cerrar.

### ¿Terminaste antes? (pull, no solo push)

Tu Issue mergeado no significa "me quedo esperando". En orden:

1. **Jala el siguiente Issue.** Los Issues de tu semana **aparecen solos el domingo por la noche** (los crea el flujo) y cualquiera del backlog `program/01_CURRICULUM/issues_backlog.md` sin dueño es justo tomarlo: créalo tú con la plantilla "Tarea de sesión" (título `[S## D#] ...`, label `week:S#`), asígnatelo, y avisa al monitor. El board se actualiza solo (o el monitor lo sincroniza en su revisión).
   - **Los Issues asignados a otro compañero NO se tocan.** Solo dos excepciones: 1) pides permiso al monitor y te lo da; 2) proactividad justificada — la tarea tiene un impacto que no se midió bien (alguien quedó bloqueado, el Issue es más grande de lo previsto) y es **necesario** — en ese caso lo comentas en el Issue/PR explicando por qué lo tomaste.
2. **Apoya a un compañero.** Mira los PRs abiertos: deja comentarios constructivos (rúbrica: `program/05_EVALUATION/rubric.md`), propón cambios si están atascados, o ofrécete con el label `apoyo`. Tu review cuenta como evidencia en tu expediente.
3. **Propón algo nuevo.** Usa la plantilla "Propuesta" + label `propuesta`: qué problema ves, qué harías, qué necesitas. El líder **@jackthony** la revisa y decide (aceptada → backlog/semana; o cerrada con motivo). No tomes decisiones de arquitectura sin pasar por un ADR.

## 5. Tu progreso e informes (se generan solos desde GitHub)

- **Diario:** registra tus horas/actividades en tu Word FPE (tu registro se llena con tus commits).
- **Viernes 17:00:** el workflow `digest-semanal` crea un Issue con **tus commits por día**, tus PRs y tus Issues abiertos.
- **Cada noche (dom–vie 21:00):** el workflow `informe-quincenal` crea/refresca tu **borrador de informe FPE** (Issues #11 Allan, #12 Pilar, #13 Josue) con tu registro semanal real (desde commits/PRs/Issues), tu tarea más significativa sugerida y el checklist (horas, ATS, diagrama). No lo edites: se regenera; completa en tu Word FPE.
- **Tú:** completas horas, seguridad (ATS), resultados y la justificación de la tarea significativa; lo pasas al Word FPE (CNIU-108) y sustentas el sábado.
- **Si no cumples la asignación:** no hay commits/PR → tu digest y tu borrador salen vacíos → no hay evidencia → los criterios del Issue se evalúan sin evidencia (afecta la nota) y tu PR se cierra solo a los 7 días.

### Notificaciones: tu coach automático (actívalas una vez)

Un coach automático te escribe **@mencionándote**, así que te llega una notificación de GitHub (web, correo y app móvil). Así sabes **qué hacer, dónde mirar y cuándo**, sin que nadie tenga que perseguirte:

| Cuándo | Qué te llega | Dónde |
|---|---|---|
| Tus días de práctica, 8:00 a. m. (Lima) | **Arranque:** tu foco del día, qué leer primero, qué jalar si terminas antes | tu hilo `📣 Coach — <tu nombre>` |
| Tus días de práctica, 2:00 p. m. | **Pulso:** solo si aún no hay actividad tuya; pregunta cómo vas y avisa al monitor | tu hilo |
| Tus días de práctica, 5:30 p. m. | **Cierre:** qué dejar hecho antes de irte (push, PR, preguntas, Word FPE) | tu hilo |
| Cuando revisan tu PR | **Tienes revisión:** qué hacer en orden (leer, responder, corregir, pedir revisión) | tu PR |
| Cuando te asignan un Issue | **Primeros pasos** del Issue y dónde mirar | el Issue |
| Cuando mergean tu PR | **¿Qué sigue?** tu informe, el siguiente Issue disponible y a quién apoyar | tu PR |

**Actívalo (2 min):** GitHub → *Settings → Notifications*: deja marcadas *Participating, @mentions and custom* por **Email** y/o **Web and Mobile**; instala **GitHub Mobile** (iOS/Android) y permite notificaciones push. En este repo pulsa *Watch → All Activity*. Si no te llega un aviso, mira primero tus *spam*.

**Tu centro de mando:** el [board](https://github.com/users/jackthony/projects/3) tiene vistas hechas para ti: **🎯 Mis tareas** (solo lo tuyo, sin terminar), **📣 Disponibles (pull)** (qué jalar al terminar) y **Tabla por Semana**. Se sincroniza solo con tus Issues, PRs y labels; si algo se ve mal, avisa en tu hilo.

## 6. Reglas duras (siempre)

- Nada clínico: el bot deriva a humano; tú tampoco opinas de salud.
- Nunca datos reales de clientes (fixtures anonimizados). Nunca secretos en código.
- No copies código sin licencia; cita la fuente. Orden de autoridad: doc oficial > código reproducible > libro/curso > paper > "lo dijo un LLM".
- Los ADRs (`program/03_ARCHITECTURE/decisions/`) no se cambian en silencio: si propones algo distinto, justifícalo contra el ADR.
