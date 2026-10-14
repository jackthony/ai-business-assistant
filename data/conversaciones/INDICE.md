# Índice de conversaciones sintéticas (v1)

Fuente: `sinteticas_v1.jsonl` · 10 conversaciones · 88 mensajes. Una fila por conversación. Canal: `manychat` (7) o `n8n` (3).

> **Datos ficticios, no clínicos:** son conversaciones inventadas a partir de patrones del negocio (no son chats reales de clientes; Ley 29733). Los temas de salud son solo contexto del servicio: el bot deriva a una persona y no da consejo clínico. Sin teléfonos, DNI ni enlaces.

| id | servicio | canal | escenario | turnos | cómo termina |
|---|---|---|---|---|---|
| conv_0001 | Terapias complementarias (hierro intravenoso) | manychat | Consulta de precio de hierro intravenoso en texto libre y con nota de voz; el cliente no elige opción del menú. | 9 | El cliente se despide sin precio ni cita. |
| conv_0002 | Estética corporal (reducción de medidas) | n8n | Consulta de precio de moldeamiento corporal; la respuesta lista varios servicios y hace varias preguntas; el cliente indica que no era lo consultado. | 7 | El cliente responde con un acuse breve. Sin cita. |
| conv_0003 | Procedimientos dermatocosméticos (eliminación de lunares) | manychat | Consulta sobre un lunar que cambió de color, enviada con imagen; el cliente indica que no busca precio y pasa a una asesora humana. | 12 | La asesora propone horario de evaluación; el cliente avisa que lo verá. Sin cita. |
| conv_0004 | Terapias complementarias (hierro intravenoso y cóctel de vitaminas) | manychat | Pide hablar con una persona; ya con la asesora relata cansancio y mareos al ponerse de pie y pregunta el precio del cóctel de vitaminas. | 11 | La asesora confirma cita de evaluación para el día siguiente a las 10:00. |
| conv_0005 | Terapias complementarias (hierro intravenoso) | n8n | Consulta de precio de hierro intravenoso; la respuesta lista servicios sin precios y pide precisar; el cliente repite la consulta. | 7 | El cliente se despide y el último mensaje es del asistente. Sin precio ni cita. |
| conv_0006 | Glow (no aparece en las demás conversaciones) | manychat | Consulta de precio de Glow por texto y nota de voz; pasa a una asesora humana, que explica que requiere evaluación previa. | 8 | La asesora hace seguimiento y no hay respuesta del cliente. Sin cita. |
| conv_0007 | Procedimientos dermatocosméticos (eliminación de verrugas) | manychat | Pregunta precio de verrugas; acepta agendar evaluación; el flujo asigna una sede y el cliente indica residir en otra ciudad. | 8 | El último mensaje es del asistente, que vuelve a mostrar el menú. Sin cita. |
| conv_0008 | Estética corporal (reducción de medidas) | n8n | Consulta de precio de moldeamiento corporal; el cliente comenta que el monto es alto; la respuesta explica el sentido de la evaluación y propone agendarla. | 6 | El cliente cierra con un acuse breve. Sin cita. |
| conv_0009 | Estética corporal (reducción de medidas) y consulta sobre lunares | manychat | Consulta de moldeamiento que pasa a asesora humana; pregunta por zonas a trabajar y si los lunares se quitan en esas zonas; pregunta precio tras la indicación de evaluación previa. | 12 | El cliente acepta el horario de evaluación del jueves a las 16:00. |
| conv_0010 | Terapias complementarias (hierro intravenoso) | manychat | Cliente con cita existente quiere moverla; el flujo muestra el menú de servicios; envía una nota de voz. | 8 | El cliente desiste de la consulta. Sin cambio de cita registrado. |
