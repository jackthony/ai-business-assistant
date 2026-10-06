# ROI para Hola Mujer — métricas y defensa del valor

> Objetivo: demostrar valor medible al cliente desde el primer mes. Sin métricas no hay ROI: el MIT reporta que **95% de los pilots GenAI no logran retorno medible**; la diferencia está en instrumentar.

## KPIs a instrumentar (desde S4)

| KPI | Definición | Meta inicial | Dónde se mide |
|---|---|---|---|
| Conversación → cita | % de chats que terminan en cita agendada | ≥60% | logs del bot + `02_CITAS` |
| Tiempo de primera respuesta | segundos hasta el primer mensaje | <60 s | telemetría FastAPI |
| Conversaciones recuperadas | chats inactivos reactivados que terminan en cita | 10+/mes | módulo proactivo (S13) |
| Contención | % de conversaciones resueltas sin humano | ≥70% | handoffs / total |
| Costo por conversación | infra + API vs costo de atención humana | menor que 1 atención manual | cálculo del monitor |
| Horas ahorradas | carga de front-desk | 10–18 h/semana | validado con Jioysi |
| No-show | citas no asistidas | ↓ vs baseline | `02_CITAS` |
| CSAT | 1 pregunta post-cita | ≥4/5 | plantilla WhatsApp |

## Benchmarks reales (usar como rango, nunca como promesa)

- Clínica Al Habib (Tanla): **+200%** citas nuevas con chatbot de WhatsApp.
- Clínica Fomina (Chat2Desk): **69.3%** de conversión; **59.8%** citas confirmadas sin llamada.
- Cadena de salones (ZielDigital): **120+ citas recuperadas/mes**, **18 h/semana** ahorradas, **3.4x** rebooking.
- Prima AFP Perú (Meta): **−18%** costo por lead.
- Caveat: varias cifras son autoevaluadas y no repetibles; presentarlas como referencia del sector.

## Costes del canal

- WhatsApp cobra **por mensaje entregado**; los mensajes de servicio son **gratis en la ventana de 24 h** (72 h si entran por anuncio click-to-WhatsApp).
- LLM local = costo marginal ~0 por token (ventaja fuerte sobre APIs cloud); el costo real es cómputo y mantenimiento.

## Riesgos que matan el ROI (y mitigación)

- **Gartner:** >40% de proyectos agentic se cancelarán para fin-2027 (costos crecientes, valor difuso, controles débiles). **MIT:** 95% de pilots sin retorno medible.
- Mitigación: alcance fijo por fases (4–6 semanas), KPIs desde S4, RAG con fuente citada, handoff humano en salud, revisión mensual con el cliente, ADRs para todo cambio de alcance.
- **Legal:** Ley 29733 (Perú, protección de datos personales) — validar con abogado antes de tocar datos reales; el bot nunca maneja datos clínicos.

## Cómo lo enseñamos

- Cada HITO (S6, S9, S12) se demuestra con **métricas**, no solo con demo.
- S13 (analytics de conversión) produce el informe mensual que se entrega al cliente.
