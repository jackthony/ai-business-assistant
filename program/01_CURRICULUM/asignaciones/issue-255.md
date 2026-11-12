# #255 · Citas en las respuestas informativas de DeepSeek

## Comportamiento

Después de cerrar el bloque de la pregunta, el prompt de información exige la marca numérica del fragmento que respalda cada dato y pide abstenerse cuando falte evidencia. El validador sigue descartando respuestas sin cita, con citas inválidas o con cifras fuera de la evidencia permitida.

## Archivos

- `src/agents/info.py`

## Pruebas

- `tests/test_agent_info.py`
- `pytest -q tests/test_agent_info.py` verifica el prompt que recibe el modelo y el rechazo de respuestas sin cita o sin sustento.
- `python -m evals.run --live` verifica los 12 escenarios en la M5 con DeepSeek, BGE-M3 y umbral 0.6.
