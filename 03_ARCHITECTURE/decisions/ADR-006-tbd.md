# ADR-006: Trunk-Based Development y un solo repo de producto

- **Fecha:** 2026-10-06
- **Estado:** aceptada

## Contexto

3 practicantes construyen un mismo producto multitenant. SENATI requiere evidencia individual.

## Problema

¿Un repo por alumno o un repo compartido? ¿Qué estrategia de branching?

## Opciones

1. 3 repos de alumno sobre template común.
2. 1 repo producto + branches cortas por Issue + PRs.
3. GitFlow con branches largas.

## Decisión

Opción 2. TBD real: branch `issue-NN-slug` desde `main`, vida de horas/pocos días, PR con review y merge. La evidencia individual son los PRs y commits firmados por cada alumno.

## Consecuencias

- `main` siempre desplegable; integración frecuente.
- Prohibidas las branches de más de ~3 días.
- El template inicial evita 3 arquitecturas incompatibles.
