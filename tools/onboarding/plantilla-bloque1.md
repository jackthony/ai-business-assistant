# Bloque 1 — Conversaciones: qué haría una persona atenta (plantilla de entrega)

> Copia este archivo a `notas-estudio/bloque1-conversaciones.md` y complétalo con tus palabras. Tiempo: 10 min.

## Cómo ver las conversaciones

```
py -3.11 tools\onboarding\ver_conversacion.py conv_0001
py -3.11 tools\onboarding\ver_conversacion.py conv_0002
py -3.11 tools\onboarding\ver_conversacion.py conv_0003
```

(Antes haz `git pull` en `main`. Son conversaciones **sintéticas** inspiradas en patrones reales de Hola Mujer; no hay datos de clientas.)

## Lista cerrada de conductas (elige 3 distintas)

- **C1** Recordar el hilo (no repreguntar lo ya dicho)
- **C2** Hablar corto (≤ 3 líneas)
- **C3** Una sola pregunta por turno
- **C4** Ofrecer 2–3 horarios u opciones concretas como siguiente paso
- **C5** Detectar un tema de salud y derivar a una persona (Jioysi) sin opinar
- **C6** Resolver la fricción (ubicación, precio, duda) con empatía en vez de repetir el menú

## Tu entrega (una fila por conducta, 3 filas)

| Conducta | conversacion_id | Turno | Frase exacta del bot | Qué habría hecho una persona atenta |
|---|---|---|---|---|
| C_ | conv_000_ | _ | "…" | … |
| C_ | conv_000_ | _ | "…" | … |
| C_ | conv_000_ | _ | "…" | … |

## Pregunta de control (2–3 líneas, en tus palabras)

¿Por qué un bot con menús rígidos pierde clientas aunque «funcione» técnicamente?

**Tu respuesta debe mencionar:** (1) que el menú no entiende lo que la clienta realmente dijo; (2) que repite opciones en vez de avanzar al siguiente paso; (3) que no recuerda el hilo ni distingue una duda de salud; (4) el efecto en el negocio (la clienta se va; el embudo 33 → 2 lo muestra).

## Cómo se revisa

El monitor abre el turno que citaste (`ver_conversacion.py conv_000X`) y comprueba que la frase existe y que la conducta corresponde. Una fila sin turno y frase exacta no cuenta.
