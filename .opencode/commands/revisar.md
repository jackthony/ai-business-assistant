---
description: Revisa mi avance contra el contrato antes de subir el PR
---
Sigue el «Protocolo de asignación» de AGENTS.md. Rama actual: !`git branch --show-current`

Archivos que cambié respecto a main:
!`git diff --name-only main`

1. Compara esa lista con la sección 4 del contrato de mi asignación (`program/01_CURRICULUM/asignaciones/S##_D#.md`): dime qué archivos sobran y cuáles faltan.
2. Recorre la sección 8 («Hecho cuando») y dime, punto por punto, qué ya está verificado y qué falta, sin asumir nada que no veas en el repo.
3. Recuérdame correr las 4 puertas (`ruff`, `mypy`, `pytest`, `bandit`) y que el PR lleve `Closes #N`.
4. No arregles mi código: señálalo y explícame por qué, para que lo corrija yo.
