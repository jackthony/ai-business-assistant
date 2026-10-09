# Onboarding — tu carpeta de trabajo ordenada

`empezar.sh` (macOS/Linux/Git Bash) y `empezar.ps1` (Windows PowerShell) dejan tu máquina lista **y te enseñan a trabajar como profesional**: una carpeta ordenada, el repo siempre actualizado, el mismo entorno que el CI, tu identidad de git protegida y una bitácora diaria. Corre el mismo script **todos los días de práctica**.

```
senati-2026/
├── ai-business-assistant/   ← el repo (aquí se programa; este es el único lugar)
├── bitacora/                ← un archivo por día (qué hiciste, qué aprendiste y por qué)
├── evidencias/              ← capturas, videos, logs por Issue
├── informes/                ← borradores del informe FPE
└── notas-estudio/           ← lo que lees y entiendes (con tus palabras)
```

**Windows (PowerShell):** `powershell -ExecutionPolicy Bypass -File tools\onboarding\empezar.ps1`
**macOS/Linux:** `bash tools/onboarding/empezar.sh`

Si descargaste el proyecto en *Descargas* o como ZIP, ejecuta el script igual: clona el repo en la carpeta ordenada y te avisa que trabajes solo desde ahí.
