# GUÍA PRACTICANTE — cómo trabajar en este repo

> Léela entera una vez (10 min). Después, ante cualquier duda: **tu Issue es la ley** y las fuentes de tu semana están en la tabla "Materiales por semana" del plan.

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
3. Entorno: `python -m venv .venv && source .venv/bin/activate` y luego `pip install -e ".[dev]"` (o `uv sync`); si aún no hay `pyproject.toml`, `pip install -r requirements.txt`.
4. `pip install pre-commit && pre-commit install` → ruff y el formateo corren solos en **cada commit**.
5. `cp .env.example .env` (el `.env` jamás se commitea).

## 3. Antes de codear (10 min, obligatorio)

1. `program/00_PROJECT/current_status.md` — dónde está el proyecto HOY.
2. Tu Issue del día y sus criterios de aceptación.
3. Tus fuentes: tabla **"Materiales por semana"** en `program/01_CURRICULUM/16_week_plan.md` + mapa `program/02_REFERENCE/source_map.md`. Lee, revisa, investiga; si contradicen algo, gana la doc oficial.
4. Si usas IA (ChatGPT o un agente): pégale **solo** `AGENTS.md` + tu Issue + la guía de tu semana. Nunca el repo completo.

## 4. Trabajar con TBD (correcto, sin excepciones)

1. Actualizar: `git pull origin main`.
2. Rama: `git switch -c issue-N-<slug>` (ej. `issue-2-setup-fastapi`). Patrón válido: `(tbd|issue)-N-<slug>`.
3. Commits **chicos**, en imperativo, referenciando el Issue (ej. `feat: endpoint /health (#2)`). **Máximo 6 commits por PR.**
4. Tests que cubran los **criterios del Issue** (casos borde incluidos). Antes de pushear corre las 4 puertas:
   `ruff check src tests && mypy src --ignore-missing-imports && pytest tests -q && bandit -r src -x tests -ll`
5. `git push -u origin issue-N-<slug>` y abre el PR con la plantilla: sección "Cómo se probó", checklist, evidencia (captura/video) y **`Closes #N` en el cuerpo**.
6. Espera CI verde (4 puertas) y el review del monitor. El merge es **squash** a `main`; la rama muere y el Issue se cierra solo.

**Qué NO hacer (lo vigila `tbd-enforcer` automáticamente):**
- Push directo a `main` → **se revierte** y se te avisa.
- PR sin `Closes #N`, rama mal nombrada o >6 commits → el guardián **lo bloquea**.
- PR abierto **>48 h** sin actividad → **se cierra solo** (trabaja en ramas de horas, no de días).

## 5. Tu progreso e informes (se generan solos desde GitHub)

- **Diario:** registra tus horas/actividades en tu Word FPE (tu registro se llena con tus commits).
- **Viernes 17:00:** el workflow `digest-semanal` crea un Issue con **tus commits por día**, tus PRs y tus Issues abiertos.
- **Cada noche (mar–vie 21:00):** el workflow `informe-quincenal` crea/refresca tu **borrador de informe FPE** (Issues #11 Allan, #12 Pilar, #13 Josue) con tu registro semanal real (desde commits/PRs/Issues), tu tarea más significativa sugerida y el checklist (horas, ATS, diagrama). No lo edites: se regenera; completa en tu Word FPE.
- **Tú:** completas horas, seguridad (ATS), resultados y la justificación de la tarea significativa; lo pasas al Word FPE (CNIU-108) y sustentas el sábado.
- **Si no cumples la asignación:** no hay commits/PR → tu digest y tu borrador salen vacíos → no hay evidencia → los criterios del Issue se evalúan sin evidencia (afecta la nota) y tu PR se cierra a las 48 h.

## 6. Reglas duras (siempre)

- Nada clínico: el bot deriva a humano; tú tampoco opinas de salud.
- Nunca datos reales de clientes (fixtures anonimizados). Nunca secretos en código.
- No copies código sin licencia; cita la fuente. Orden de autoridad: doc oficial > código reproducible > libro/curso > paper > "lo dijo un LLM".
- Los ADRs (`program/03_ARCHITECTURE/decisions/`) no se cambian en silencio: si propones algo distinto, justifícalo contra el ADR.
