# Índice de conversaciones sintéticas (v2)

Generado por `tools/corpus/generar_sinteticas.py` (semilla 20261014): 100 conversaciones, 629 mensajes. **No editar a mano**: se regenera.

> **Datos ficticios.** No hay chats, nombres ni teléfonos reales. Reproducen patrones agregados del Excel operativo; la tabla de abajo dice cuáles son *medidos* y cuáles *supuestos*. Sirven para probar el comportamiento del bot y armar evals, **no** para estimar conversión real (la hoja 07 lo descarta). El split `natural` sigue las frecuencias medidas; el `cobertura` fuerza caminos poco frecuentes (cita, cancelar, reprogramar, duda clínica, otra ciudad, n8n que repite).

## Composición

| split | escenario | conversaciones |
|---|---|---|
| cobertura | agenda | 3 |
| cobertura | gestion_cita | 6 |
| cobertura | servicios | 11 |
| natural | agenda | 13 |
| natural | gestion_cita | 13 |
| natural | ruido | 7 |
| natural | servicios | 32 |
| natural | ubicacion | 15 |

Canal: {'manychat': 82, 'n8n': 18}

Desenlaces: abandono 11, cancelar 7, cita 11, ciudad_otra 12, handoff 4, handoff_clinico 5, n8n_repite 6, n8n_sin_precio 8, n8n_ubicacion_vaga 4, reprogramar 12, ruido_auto_reply 2, ruido_proveedor 2, ruido_prueba 3, seguimiento 3, ubicacion_ok 10

## Parámetros y su fuente

| parámetro | valor | tipo | fuente |
|---|---|---|---|
| `escenarios` | `{"servicios": 15, "ubicacion": 7, "agenda": 6, "gestion_cita": 6, "ruido": 3}` | medido (menos «ruido») | 03_EVENTOS.automation_flow: HM_WA_20_SERVICIOS=15, HM_WA_10_UBICACION=7, HM_WA_30_AGENDA=6, HM_WA_40_GESTION_CITA=6. «ruido»=3 es supuesto: 07 dice que aparecen proveedores, auto-reply y pruebas, sin conteo. |
| `servicio` | `{"vitaminas_hierro": 24, "moldeamiento": 7, "verrugas_lunares": 5, "glow": 3}` | medido | 07_APRENDIZAJES_INBOX «Servicios»: 39 vistas con servicio identificable. |
| `canal_manychat` | `0.7` | supuesto | Proporción de sinteticas_v1 (7 ManyChat / 3 n8n); el Excel no la mide. |
| `p_horario_elegido` | `0.0606` | medido | 07 «Agendamiento»: 33 invitaciones a agendar, 2 horarios elegidos. |
| `p_seguimiento` | `0.2424` | medido | 07 «Agendamiento»: 8 seguimientos sobre 33 invitaciones. |
| `gestion_cita` | `{"reprogramar": 6, "cancelar": 6}` | medido | 03_EVENTOS.event_type: RESCHEDULED=6, CANCELLED=6. |
| `p_ciudad_otra` | `0.25` | supuesto | 07 «Ubicación»: hay fricción por descubrir tarde que la atención es en Chimbote; la frecuencia no está medida. |
| `p_nota_voz` | `0.2` | supuesto | Las notas de voz aparecen en la muestra; la frecuencia no está medida. |
| `p_duda_clinica` | `0.15` | supuesto | 07 «Seguridad clínica»: preguntas que requieren criterio humano; sin frecuencia. |
| `p_pide_persona` | `0.2` | supuesto | 03_EVENTOS: HANDOFF_REQUESTED=19 de 47 eventos; no separa causas. |
| `p_agenda_confirma` | `0.5` | supuesto | Sin dato: cuántos clientes que piden agendar completan la coordinación. |
