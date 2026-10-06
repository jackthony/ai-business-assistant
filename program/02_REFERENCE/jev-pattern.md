# Patrón Jev — decisiones de 1 token con confianza calibrada

> Fuente: `jackthony/IA-local` (MIT, lab interno del monitor). Sirve para **clasificar, rutear y evaluar rápido y barato**; nunca para generar texto. Lectura previa recomendada para S9 (#16), S10 (#19) y S12 (#27).

## La idea

En vez de pedirle al LLM un texto y parsearlo, se le pide una decisión **tipada** (`Choice` con opciones, `Score` 1–n) y se lee la **distribución de probabilidad (logprobs) del primer token** de cada opción:

- `Choice(("facturacion", "tecnico"))` → el modelo emite 1 token; la confianza sale de los logprobs reales.
- Resultado: `valor` + `confianza`, en **~1–2 s en CPU** con un modelo chico (qwen3:4b-instruct).

## Por qué gana al texto libre (en decisiones)

1. **Salida siempre en el dominio:** cero errores de parseo ("el modelo respondió mal el formato").
2. **Confianza medible y calibrable** (temperature scaling): si confianza < umbral → handoff humano. Un judge de texto libre no puede decir "no estoy seguro" con precisión.
3. **Costo:** 1 token vs cientos. En el camino caliente (triage, router) es la diferencia entre <2 s y 20+ s.
4. **Lusser:** es el validador que sí conviene — bajo confianza no repara mal, deriva a humano (f≈0).

## Cuándo lo usamos

| Caso | Semana / Issue | Uso |
|---|---|---|
| Triage clínico/riesgo | S9 #16 | Choice(riesgo) + umbral → congelar bot |
| Router de intención | S10 #19 | Choice(info/citas/checkout/safety); LLM solo para ambiguos |
| Evals offline | S12 #27 | Score 1–9 por criterio (logprobs) vs judge de texto libre |

No se usa para: generar respuestas, resumir ni nada que requiera texto.

## Cómo estudiarlo (antes de S9 — para el monitor y los chicos)

1. Clonar `jackthony/IA-local`, `uv sync`, `ollama pull qwen3:4b-instruct`, correr `python jev/test_jev.py`.
2. Leer `jev/jev.py`: la clase `Jev`, los tipos `Choice`/`Score` y cómo lee logprobs del primer token.
3. Leer los labs 01 (tools), 03 (handoff) y 11 (aprobación humana).
4. Pregunta de estudio: ¿por qué 26 opciones es el tope práctico? ¿Qué pasa cuando la confianza cae bajo el umbral? ¿Cómo se calibra (temperature scaling) y con qué set?

## Criterio de sustentación

En #16, #19 y #27 los chicos deben explicar: qué decisión le piden a Jev, qué umbral usan y qué ocurre cuando la confianza está por debajo del umbral.
