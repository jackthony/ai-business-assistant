# Datos del negocio — Hola Mujer (normalizados)

Datos del negocio que viven en el Excel operativo, pasados a JSON validado para trabajarlos en el repo sin depender del Excel. **Son datos del negocio, no de personas**: no hay contactos, citas, eventos ni conversaciones reales (ver «Qué no entra»).

| Archivo | Qué es | Fuente |
|---|---|---|
| `servicios.json` | 47 servicios con precio, reserva, duración, sesiones y marcas de cuidado | hoja `05_SERVICIOS` |
| `promociones.json` | 3 promociones, **todas inactivas** y con fechas por confirmar | hoja `06_PROMOCIONES` |
| `negocio.json` | 17 datos del negocio (dirección, horario, plantillas, protocolo…) con su estado | hoja `04_CONFIG` + confirmaciones del monitor |
| `vocabularios.json` | Listas permitidas del dominio (etapas, eventos, estados de cita, CTA) | validaciones de lista del Excel |

Cada archivo trae `meta` (fuente, captura y notas) e `items`. Los valores salen del Excel tal cual; lo que no se pudo confirmar queda marcado, no se rellena.

## Cómo se regenera

```bash
pip install -e ".[etl]"
python tools/datos/normalizar_hola_mujer.py RUTA_AL_EXCEL.xlsx
```

El esquema (Pydantic v2) valida: IDs únicos con formato `HM-LINEA-NNN`, precio > 0, reserva ≤ precio, sesiones coherentes y que una promoción inactiva o con fechas ambiguas no pueda marcarse como usable. `tests/test_datos_hola_mujer.py` revisa los JSON publicados. **No se editan a mano**: se cambia el Excel (o `CONFIRMADOS` en el script, para lo que confirma el monitor) y se regenera.

## Campos que conviene entender

- `duracion_verificada: false` — las 47 duraciones son 60 min, parece un valor por defecto. No citarlas al cliente como dato aprobado hasta que Jioysi las confirme (`DEFAULT_APPOINTMENT_MINUTES` sigue pendiente).
- `sensible_clinico: true` — 21 servicios de 5 categorías (obstetricia, planificación familiar, prevención y tamizaje, prevención y salud femenina, salud íntima). Es una **heurística por categoría** para el guardrail «nada clínico, deriva a humano»; Jioysi debe confirmar la lista.
- `espacio_entre_sesiones` — unidad sin confirmar (probable días; solo 8 servicios lo traen).
- `requiere_evaluacion: false` — solo los 2 talleres de la Academy.
- `usable_en_rag: false` en las 3 promociones — se activan solo cuando el negocio confirme vigencia y precio.

## Auditoría del Excel (revisión a fondo, 2026-10-14)

**Sólido:** `05_SERVICIOS` (47 filas, sin vacíos relevantes, IDs únicos, reserva siempre menor al precio, todo activo) y los vocabularios de las validaciones de lista, que son el lenguaje del dominio.

**Hallazgos a resolver con el negocio:**

1. **Promociones (`06`)**: solo 3 reales (`LUNARES`, `MOLDEA`, `GLUTEOS`), las 3 con `activo=NO`. El Excel convirtió fechas `dd/mm` a fecha `mm/dd` en algunas (p. ej. `2026-11-09` con fin `13/09`, casi seguro 11-sep), así que se conservan como texto sin interpretar. `LUNARES` (49.99) y `MOLDEA` (59.99) cuestan lo mismo que su servicio base: no se ve descuento. `GLUTEOS` (179.99, paquete de 4 sesiones) **no existe en el catálogo** y aparece como `service_id` en una cita. Debajo de la fila 200 hay tres bloques repetidos de un catálogo viejo (IDs `OBS-001`, `EST-005`…, que ya no existen): se ignoran.
2. **Datos del negocio (`04`)**: 11 de 17 seguían pendientes. Dirección, mapa y horario quedaron confirmados por el monitor el 2026-10-14. Siguen pendientes `CALENDAR_ID`, plantillas de WhatsApp, `PRIVACY_NOTICE_URL`, `EMERGENCY_PROTOCOL`, `DEFAULT_APPOINTMENT_MINUTES` y los dos campos de ManyChat de Jioysi.
3. **Operación real (hojas `01`–`03`)**: la muestra es mínima: 6 contactos, 9 citas y 47 eventos entre el 27-ago y el 30-sep. Las 9 citas tienen recordatorios, sincronización e ID de calendario **vacíos**: la integración con calendario nunca corrió (coincide con los pasos 10–12 del plan en `TODO`). El flujo `HM_WA_35_RESULTADO_CALCOM` sugiere que se usó Cal.com para agendar (inferido del nombre; confirmar).
4. **Integridad entre hojas**: 2 eventos apuntan a un `contact_id` que no existe en contactos, 8 a un `cita_id` que no existe y 3 citas a un contacto inexistente. Hay valores fuera de lista (`CANCELADO` en vez de `CANCELLED`, `Whatsapp` en vez de `WHATSAPP`, el evento `CANCELLED_MISMATCH` que la lista no incluye), teléfonos con formatos mezclados y fechas de cita como texto (`07/09 09:30`). Todo esto debe validarse en el esquema del agente, no asumirse.
5. **Datos operativos: sí están en el repo, pseudonimizados** (`operativo/`; ver sección siguiente). Solo quedan fuera `00_EMPEZAR` y la hoja oculta, que no tienen valor de dominio: `00_EMPEZAR` (trae nombres y apellidos de personas con estado «Cliente» y enlaces a documentos de Google) y la hoja oculta `MANYCHAT_SERVICE_SHEET` (borrador de 930 fórmulas `QUERY` rotas con algunos nombres y teléfonos). Conviene limpiarlas en el Excel.

## Qué no entra y por qué

`01_CONTACTOS`, `02_CITAS`, `03_EVENTOS`, `09_MUESTRA_INBOX_11D`, `00_EMPEZAR` y `MANYCHAT_SERVICE_SHEET`: contienen o pueden contener datos de personas (Ley 29733 sin validar; el repo es público). Sus **patrones agregados** ya alimentan el corpus sintético (`data/conversaciones/INDICE_v2.md`).

## Datos operativos pseudonimizados (`operativo/`)

El repo es **público**, así que las hojas con personas entran **sin** nombres, teléfonos, ids de plataforma ni enlaces, y con todo lo demás intacto (fechas, etapas, flujos, estados, notas, vacíos y defectos), para que se trabaje con la forma real de los datos.

| Archivo | Hoja origen | Filas | Qué cambia |
|---|---|---|---|
| `contactos.json` | 01_CONTACTOS | 5 | `contact_id` → `C001…`; sin `nombre`/`telefono` (solo `tiene_nombre`, `tiene_telefono`) |
| `citas.json` | 02_CITAS | 9 | `contact_id` → alias; fechas serial de Excel pasadas a ISO |
| `eventos.json` | 03_EVENTOS | 46 | `contact_id`, `event_id`, `cita_id` → alias (mismo alias para el mismo contacto) |
| `muestra_inbox.json` | 09_MUESTRA_INBOX_11D | 220 | nada: ya eran clasificaciones sin texto (82 con vista previa útil) |

Defectos reales conservados a propósito (los alumnos deben tratarlos, no esconderlos): citas sin `contact_id`, estado `CANCELADO` fuera del vocabulario, `inicio` como texto `"07/09 09:30"`, eventos duplicados con el mismo `event_id`, `canal` con distinta capitalización, contactos sin teléfono.

Regenerar: `python tools/datos/pseudonimizar_operativo.py RUTA.xlsx`. El Excel original sigue fuera del repo. Si el dueño decide hacer el repo privado, se puede volver a subir el dato crudo en otro PR; en un repo público no se debe, porque el historial de git es permanente.
