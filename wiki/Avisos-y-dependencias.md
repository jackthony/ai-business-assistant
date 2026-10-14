# Avisos y dependencias

## ¿Todo el equipo se entera cuando alguien sube algo?
**Por defecto, no del todo:** GitHub avisa por correo solo cuando te **asignan**, te **mencionan** (@usuario), te piden una **revisión** o participas en la conversación. Ver todo lo demás depende de que cada persona tenga el repo en *Watch*.

Por eso hay **dos capas**:

### Capa 1 · Automática (robots)
| Cuándo | Qué pasa | Quién se entera |
|---|---|---|
| Un alumno sube su rama `issue-N-*` | El robot abre un **PR en borrador** y comenta mencionando al equipo | el resto de alumnos y el monitor |
| Un alumno marca *Ready for review* | Comentario: «listo para revisión, ayuden con la rúbrica» | el resto del equipo |
| Se mergea un PR de un alumno | Comentario: «mergeado, hagan `git pull origin main`» | el resto del equipo |
| Se mergea un Issue del que otros dependían | Comentario **🔓 «ya puedes empezar»** en el Issue dependiente y se quita la etiqueta `bloqueado` | quien tiene asignado el Issue desbloqueado |
| Cada push | Comentario «🧭 Revisión guiada» actualizado | autor del PR |
| Cada domingo por la noche | Aparece la **Lectura guiada** en Discussions, mencionando a todo el equipo | todos (por la mención) |
| Alguien abre una discusión | El robot comenta mencionando al resto del equipo | el resto de alumnos y el monitor |
| Alguien comenta en una discusión | GitHub te avisa **si ya participaste** en ella (comentar te suscribe) o te mencionan | quienes participan en esa discusión |

Mencionar con @ es lo que garantiza el correo/notificación: no depende de tu configuración de *Watch*. **Lo que no se automatiza:** los comentarios nuevos en discusiones donde no participas. Para verlos todos, pon el repo en *Watch → Custom → Discussions* (Capa 2). El monitor conviene que use **All Activity**.

### Capa 2 · Configura tus notificaciones
1. Abre el repo → **Watch → Custom** y marca **Issues**, **Pull requests** y **Discussions**. (O **All Activity** si quieres todo.)
2. En [github.com/settings/notifications](https://github.com/settings/notifications) deja marcado **Email** y confirma que el correo de tu perfil es uno que lees. Revisa la carpeta de spam.
3. Acepta la invitación de colaborador si aún está pendiente.

## Dependencias entre Issues
Una asignación que depende de otra **no se empieza** hasta que la anterior esté en `main`. Las dependencias salen de la columna «Depende de» de la [tabla Issue → contrato](https://github.com/jackthony/ai-business-assistant/blob/main/program/01_CURRICULUM/asignaciones/README.md); el Issue bloqueado lleva la etiqueta `bloqueado`.

| Issue | Depende de | Estado |
|---|---|---|
| [#53](https://github.com/jackthony/ai-business-assistant/issues/53) (Pilar) | [#52](https://github.com/jackthony/ai-business-assistant/issues/52) (Josue) | ⛔ bloqueado hasta que #52 esté en `main` |
| [#54](https://github.com/jackthony/ai-business-assistant/issues/54) (Allan) | [#52](https://github.com/jackthony/ai-business-assistant/issues/52) (Josue) | ⛔ bloqueado hasta que #52 esté en `main` |

**Mientras esperan:** lecturas de la semana, estudios guiados (cola «Pull») y apoyar el PR de Josue con la rúbrica. **Josue:** tu PR destraba a todo el equipo; súbelo temprano y en borrador para que te ayuden.
