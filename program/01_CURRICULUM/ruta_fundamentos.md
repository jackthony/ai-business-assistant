# Ruta de fundamentos — NLP, LLMs, Transformers, ML y Deep Learning

> **Regla de oro:** solo fuentes **top**: oficiales (la doc del propio proyecto), o de **autores reconocidos** (Karpathy, Jurafsky, Huyen, Ng, Raschka, 3Blue1Brown…). Nada de blogs random, resúmenes de Medium ni videos de "trucos". Si tu IA te sugiere una fuente que no está aquí: busca primero el equivalente en esta ruta; si de verdad es top, avisa al monitor para agregarla.
>
> **No es tarea extra:** es tu recurso para el *porqué* cuando el Issue lo pida. Profundidad sin límite permitido: NLP, LLMs, transformers, ML, DL — todo lo que quieras y necesites **se puede aquí**. Todo es gratis.

## Nivel 0 — Intuición visual (horas, cuando quieres *ver* la idea)

| Recurso | Quién | Para qué | Cuándo |
|---|---|---|---|
| 3Blue1Brown — serie «Neural Networks» (YouTube) | Grant Sanderson (el mejor divulgador visual) | ver qué es una red y backprop sin matemática | antes de S5 |
| Jay Alammar — «The Illustrated Transformer» (jalammar.github.io) | referencia universal del tema | ver la atención con dibujos | S5 / S10 |
| Karpathy — «Intro to Large Language Models» (charla) | ex-OpenAI/Tesla | mapa mental completo de un LLM | S4–S5 |

## Nivel 1 — Construir desde cero (el que de verdad enseña)

| Recurso | Quién | Para qué | Cuándo |
|---|---|---|---|
| Karpathy — «Neural Networks: Zero to Hero» (YouTube) + `karpathy/nanoGPT` y `minGPT` (MIT) | Andrej Karpathy | construir backprop y un GPT desde cero, línea por línea | S5 (estado/prompt) · S10 · S12 |
| «Dive into Deep Learning» — d2l.ai (libro interactivo, código Apache-2.0) | Zhang, Lipton, Li, Smola (universitario) | DL con runnable code: vectores, embeddings, atención | S6 (embeddings) · S12 |
| «Practical Deep Learning for Coders» — course.fast.ai | Jeremy Howard (fast.ai) | enfoque práctico top-down | S6 · S11 (visión) |
| Raschka — «Build a Large Language Model (From Scratch)» + `rasbt/LLMs-from-scratch` (MIT) | Sebastian Raschka (autor reconocido) | implementar un transformer completo y entender cada pieza | S10–S12 |

## Nivel 2 — NLP y Transformers formales

| Recurso | Quién | Para qué | Cuándo |
|---|---|---|---|
| Jurafsky & Martin — «Speech and Language Processing», 3.ª ed. (borrador libre: `web.stanford.edu/~jurafsky/slp3`) | el libro canónico de NLP (Stanford) | el fondo de NLP: embeddings, clasificación, diálogo | S6–S7 |
| Hugging Face — NLP/LLM Course (`huggingface.co/learn`, oficial y gratis) | HF (la empresa del ecosistema) | tokenizers, transformers, fine-tuning, agents — con código | S6 (embeddings) · S7 (tools) |
| «Natural Language Processing with Transformers» (O'Reilly) | Tunstall, von Werra, Wolf (autores de HF) | transformer aplicado con la librería que usamos | S6–S7 |
| Stanford CS224n — materiales oficiales (`web.stanford.edu/class/cs224n`) | Stanford | NLP con deep learning a nivel curso top | profundidad S7+ |
| Paper «Attention Is All You Need» (`arxiv.org/abs/1706.03762`) | Vaswani et al. (Google) | el paper original de la arquitectura | S10 (opcional antes) |

## Nivel 3 — LLMs a fondo

| Recurso | Quién | Para qué | Cuándo |
|---|---|---|---|
| Stanford CS336 — «Language Modeling from Scratch» (`github.com/stanford-cs336`) | Stanford (materiales oficiales 2024) | construir un LLM completo: datos, tokenizer, atención, entrenamiento | S12+ (quien quiera el fondo real) |
| Karpathy — «Let's build GPT: from scratch» (video) | Karpathy | versión guiada y corta del anterior | S10–S12 |

## Nivel 4 — Ingeniería de productos con LLM (lo más cercano a nuestro trabajo)

| Recurso | Quién | Para qué | Cuándo |
|---|---|---|---|
| Chip Huyen — «AI Engineering» (2025) y «Designing Machine Learning Systems» | referente de la ingeniería de IA en producción | evaluación, RAG, costos, operación de sistemas con LLM | S6 (RAG) · S8 (métricas) · S12 (evals) · S15 (FinOps) |
| «LLM Engineer's Handbook» (Packt; repo oficial `PacktPublishing/LLM-Engineers-Handbook`) | Iusztin & Labonne | LLMops práctico: pipelines, serving, observabilidad | S8 · S14 |
| Guías **oficiales** de prompt engineering (docs de Anthropic y OpenAI) | los propios laboratorios | escribir prompts por componentes, structured outputs, tool-use | S5 (prompt) · S7 (tools) |
| Anthropic — «Building Effective Agents» + «12-Factor Agents» (ya en `source_map.md` N1) | Anthropic · Dex Horthy | patrones de agentes y flujo correcto | S5+ · S10 |

## Nivel 5 — ML / DL clásico (la base, cuando quieras la base)

| Recurso | Quién | Para qué | Cuándo |
|---|---|---|---|
| Andrew Ng — Machine Learning + Deep Learning Specializations (Coursera, audit gratis) | el estándar para empezar ML | fundamentos guiados paso a paso | S8+ (opcional) |
| Goodfellow, Bengio & Courville — «Deep Learning» (`deeplearningbook.org`, libre) | los autores de referencia | consulta teórica puntual (capítulo que necesites) | consulta |
| MIT 6.S191 «Introduction to Deep Learning» (`introtodeeplearning.com`) | MIT (materiales oficiales) | intro rigurosa y corta | consulta |
| Stanford CS229 (`cs229.stanford.edu`) | Stanford | ML riguroso (matemática) | consulta profunda |

## Cómo estudiar con esta ruta (sin quemar tiempo ni tokens)

1. **Empieza por el nivel más bajo** que responda tu duda (Nivel 0/1 antes de saltar a papers).
2. Cuando un Issue pida algo concreto (RAG, tools, evals): **Nivel 4 aplicado + Nivel 2 para el porqué**.
3. **Un recurso por duda**: ve al capítulo/sección exacta, no al curso completo (la IA puede resumirte *una* sección si le das el enlace y la pregunta — pero tú lees y explicas).
4. Lo aprendido se anota en tu informe FPE: *qué leí, qué entendí, cómo lo apliqué al proyecto*.
5. Prohibido copiar código de cursos/libros sin licencia (regla de `source_map.md`); se lee, se entiende, se reimplementa.

## Mapa semana → tema (si te trabas, ve a…)

| Semana | Tema que puede requerir fondo | Fuente recomendada |
|---|---|---|
| S4 | HTTP/webhooks | docs FastAPI (N1) — sin fondo profundo aún |
| S5 | estado del grafo, prompt, atención básica | N0 (3B1B + Alammar + charla Karpathy) · N4 prompt oficial |
| S6 | RAG, embeddings, similitud vectorial | N4 Huyen (cap. RAG) · N2 HF course (embeddings) · N1 d2l (vectores) |
| S7 | tools, structured outputs | N4 Anthropic tool-use + 12-Factor · N2 HF (agents) |
| S8 | telemetría, trazas, métricas | N4 LLM Engineer's Handbook (observabilidad) + Langfuse (source_map) |
| S9 | safety, HITL | N4 Huyen (seguridad) · OWASP GenAI/ASI (source_map N1) |
| S10 | supervisor, routing, visión | N4 Anthropic patterns · N3 CS336 (opcional) · N1 fast.ai (visión) |
| S11 | NeuraCode, multimodal | N1 fast.ai · docs Qwen-VL/Ollama (source_map) |
| S12 | evals, inyección, jueces | N4 Huyen (evals) · OWASP ASI · Langfuse evals |
| S13–S16 | FinOps, operación, venta | N4 Huyen (costos) · LLM Engineer's (deploy) |

**Nota de ambición:** esto no se acaba en S16. Si un tema te atrapa (transformers, visión, evals), esta ruta te lleva hasta los materiales de Stanford — el mismo camino con el que se forman los que construyen esto. Se puede.
