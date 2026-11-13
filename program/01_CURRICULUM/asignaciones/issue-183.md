# #183 · Confirmar ubicación para la atención presencial

## Comportamiento

Extiende el nodo de información existente. Si el último mensaje declara afirmativamente una ciudad con «Vivo en …» o «Estoy en …», considera Chimbote y Nuevo Chimbote como locales, sin distinguir mayúsculas. Para este primer tramo, la declaración termina en un punto o al final del mensaje. Una pregunta o una negación no cuenta como declaración.

- **Ciudad fuera de Chimbote:** devuelve una aclaración de que la atención presencial es en Chimbote y pregunta «¿Puedes acercarte?». Usa `intent="ubicacion_por_confirmar"`, `status="active"` y citas vacías. No consultes el recuperador ni el modelo en ese turno.
- **Ciudad local o sin declaración:** conserva la respuesta y las citas del flujo de información actual.
- La regla se aplica al nodo de información. Conserva las rutas de seguridad y la aprobación de citas existentes. El CTA comercial y la búsqueda híbrida quedan para otros cambios.

## Archivos

- `src/agents/info.py`

## Pruebas

- `tests/test_info_location.py`
- Comando: `pytest -q tests/test_info_location.py`
- Usa el nodo real, un modelo de prueba y un único fragmento con un taller ficticio. Comprueba el resultado en estos cuatro casos:

| Entrada | Resultado observable |
|---|---|
| «Vivo en Lima. ¿Cuánto cuesta el taller ficticio?» | Aclara Chimbote y pregunta si puede acercarse. Sin precio, citas ni llamadas al modelo o al recuperador. |
| «Vivo en NUEVO CHIMBOTE. ¿Cuánto cuesta el taller ficticio?» | Respuesta de información con el precio y la cita del fixture. |
| «¿Cuánto cuesta el taller ficticio?» | Mismo flujo de información. |
| «No vivo en Lima. ¿Cuánto cuesta el taller ficticio?» | Mismo flujo de información. La negación no declara una ciudad. |

La etiqueta `tdd-issue-183` contiene el commit de pruebas. Desde PowerShell, con el entorno Python 3.11 activo:

```powershell
git fetch origin tag tdd-issue-183
git switch -c issue-183-confirmar-ubicacion tdd-issue-183
pytest -q tests/test_info_location.py
```

En la base, deben pasar tres casos y fallar el de Lima. Tras el cambio deben pasar los cuatro y la suite completa. Conserva ambas salidas en el PR con `Closes #183`.
