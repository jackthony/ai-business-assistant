# #257 · Fecha de mañana en la agenda

## Comportamiento

En una petición directa de cita para mañana, calcula el día siguiente con el reloj de Lima antes de consultar el calendario, aunque el modelo devuelva otra fecha o la omita. Aplica a la petición actual y a una respuesta directa dentro de la agenda. Expresiones distintas como «pasado mañana», una negación o «por la mañana» conservan el flujo de extracción existente.

Repetir la petición para el mismo día y hora conserva una sola cita. Un horario ocupado ofrece alternativas. La confirmación sigue requiriendo aprobación.

## Archivos

- `src/agents/booking.py`

## Pruebas

- `tests/test_booking_flow.py`
- `pytest -q tests/test_booking_flow.py` con un calendario simulado y respuestas del modelo que cambian de fecha.
- `python -m evals.run --live` con DeepSeek y BGE-M3 en la M5.
