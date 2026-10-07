## Qué y por qué

<!-- 1-3 líneas. Cierra el Issue con: Closes #NN -->

## Cómo se probó

- [ ] `ruff check src tests` limpio
- [ ] `mypy src` sin errores
- [ ] `pytest tests -q` verde (mocks; sin llamadas reales a modelos)
- [ ] `bandit -r src -x tests -ll` sin hallazgos de alta/media
- [ ] Casos borde considerados (válido / inválido / límite)

## Checklist

- [ ] Sin secretos ni tokens en el diff
- [ ] Sin datos reales de clientes (fixtures anonimizados)
- [ ] Estándares (`estandares.md`): núcleo sin canales/servicios/HTTP · inglés en código, español peruano al usuario · simplicidad primero
- [ ] Branch `issue-NN-slug` corta (TBD) — sin merges largos
- [ ] Docs/README actualizados si aplica
- [ ] Evidencia adjunta (captura, video o log)

## Preguntas de comprensión (para el review)

1.
