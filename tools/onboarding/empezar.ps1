# Empieza (o retoma) tu dia de practica con orden profesional. Windows PowerShell.
#   powershell -ExecutionPolicy Bypass -File tools\onboarding\empezar.ps1
#   $env:EMPEZAR_RAIZ="D:\mis-practicas"; powershell -ExecutionPolicy Bypass -File tools\onboarding\empezar.ps1
# Es idempotente: puedes correrlo todos los dias de practica. Que hace, y por que:
#   1. Tu trabajo vive en UNA carpeta ordenada (no en Descargas): ahi encuentras todo y llevas tu avance.
#   2. Clona o actualiza el repo (git pull): empezar con el codigo viejo es la causa n.1 de conflictos.
#   3. Prepara el entorno (Python 3.11, dependencias, pre-commit): lo que corre en tu PC = lo que corre el CI.
#   4. Revisa tu identidad de git: tu correo personal no debe quedar en un historial publico.
#   5. Crea la bitacora de HOY: lo que no se escribe no se aprende (y alimenta tu informe FPE).
$ErrorActionPreference = "Continue"   # los comandos nativos escriben en stderr aunque no fallen

$RepoUrl = if ($env:EMPEZAR_REPO) { $env:EMPEZAR_REPO } else { "https://github.com/jackthony/ai-business-assistant.git" }
$Raiz = if ($env:EMPEZAR_RAIZ) { $env:EMPEZAR_RAIZ } else { Join-Path $HOME "senati-2026" }
$RepoDir = Join-Path $Raiz "ai-business-assistant"
$SinInstalar = $env:EMPEZAR_SIN_INSTALAR -eq "1"
$Aqui = Split-Path -Parent $MyInvocation.MyCommand.Path

function Paso($t)  { Write-Host ""; Write-Host ">> $t" -ForegroundColor Cyan }
function Ok($t)    { Write-Host "   [OK] $t" -ForegroundColor Green }
function Aviso($t) { Write-Host "   [!]  $t" -ForegroundColor Yellow }
function Falta($t) { Write-Host "   [X]  $t" -ForegroundColor Red; exit 1 }

Paso "1/5  Tu carpeta de trabajo: $Raiz"
foreach ($d in @("bitacora", "evidencias", "informes", "notas-estudio")) {
    New-Item -ItemType Directory -Force -Path (Join-Path $Raiz $d) | Out-Null
}
Ok "bitacora (diario) - evidencias (capturas y videos por Issue) - informes (borradores FPE) - notas-estudio (lo que lees y entiendes)"

Paso "2/5  El repositorio (siempre actualizado)"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Falta "Instala git: https://git-scm.com/downloads" }
if (Test-Path (Join-Path $RepoDir ".git")) {
    git -C $RepoDir pull --ff-only
    if ($LASTEXITCODE -ne 0) { Falta "No pude actualizar el repo. Si tienes cambios sin guardar, haz commit o stash y vuelve a correr el script." }
    Ok "repo actualizado en $RepoDir"
} else {
    git clone $RepoUrl $RepoDir
    if ($LASTEXITCODE -ne 0) { Falta "No pude clonar el repo. Revisa tu internet y que la invitacion de GitHub este aceptada." }
    Ok "repo clonado en $RepoDir"
}
$QueCorre = (Resolve-Path (Join-Path $Aqui "..\..")).Path
if ($QueCorre -ne (Resolve-Path $RepoDir).Path) {
    Aviso "Estas usando una copia en $QueCorre. Trabaja SOLO desde: $RepoDir (borra la otra copia cuando quieras)."
}

Paso "3/5  Entorno de Python 3.11"
if ($SinInstalar) {
    Aviso "EMPEZAR_SIN_INSTALAR=1: se omite el entorno (solo para pruebas)"
} else {
    $PyExe = $null; $PyArgs = @()
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3.11 -c "import sys" 2>$null
        if ($LASTEXITCODE -eq 0) { $PyExe = "py"; $PyArgs = @("-3.11") }
    }
    if (-not $PyExe -and (Get-Command python -ErrorAction SilentlyContinue)) {
        python -c "import sys; sys.exit(0 if sys.version_info[:2]==(3,11) else 1)" 2>$null
        if ($LASTEXITCODE -eq 0) { $PyExe = "python" }
    }
    if (-not $PyExe) { Falta "No encontre Python 3.11 (el CI usa 3.11; no uses 3.12/3.13). Instalalo: https://www.python.org/downloads/release/python-3119/ (marca 'Add python.exe to PATH')." }
    $VenvPy = Join-Path $RepoDir ".venv\Scripts\python.exe"
    if (-not (Test-Path $VenvPy)) { & $PyExe @PyArgs -m venv (Join-Path $RepoDir ".venv") }
    Push-Location $RepoDir
    & $VenvPy -m pip install -q -U pip
    & $VenvPy -m pip install -q -e ".[dev]"
    if ($LASTEXITCODE -ne 0) { Pop-Location; Falta "Fallo la instalacion de dependencias. Copia el error y pregunta en el grupo." }
    & (Join-Path $RepoDir ".venv\Scripts\pre-commit.exe") install
    Pop-Location
    Ok "entorno listo (.venv) y pre-commit instalado: ruff corre solo en cada commit"
    $EnvFile = Join-Path $RepoDir ".env"
    if (-not (Test-Path $EnvFile)) {
        Copy-Item (Join-Path $RepoDir ".env.example") $EnvFile
        Ok ".env creado desde .env.example (NUNCA se sube al repo; pon aqui tus claves de prueba)"
    }
}

Paso "4/5  Tu identidad de git (el historial es publico)"
$Correo = (git -C $RepoDir config user.email) 2>$null
if ($Correo -like "*noreply.github.com") {
    Ok "usas el correo privado de GitHub ($Correo)"
} elseif (-not $Correo) {
    Aviso "No tienes correo configurado. GitHub > Settings > Emails > 'Keep my email addresses private' y copia tu correo ...@users.noreply.github.com; luego: git config --global user.email ""ese-correo"" y git config --global user.name ""Tu Nombre"""
} else {
    Aviso "Tu correo ($Correo) quedaria publico en tus commits. Cambialo al noreply: GitHub > Settings > Emails > 'Keep my email addresses private' + 'Block command line pushes that expose my email'; luego: git config --global user.email ""tu-id+usuario@users.noreply.github.com"""
}

Paso "5/5  Tu bitacora de hoy"
$Hoy = Get-Date -Format "yyyy-MM-dd"
$Nota = Join-Path $Raiz "bitacora\$Hoy.md"
if (-not (Test-Path $Nota)) {
    (Get-Content (Join-Path $Aqui "plantilla-bitacora.md") -Raw -Encoding UTF8) -replace "AAAA-MM-DD", $Hoy | Set-Content $Nota -Encoding UTF8
    Ok "creada $Nota"
} else {
    Ok "ya existe $Nota"
}

Write-Host ""
Write-Host "----------------------------------------------------------"
Write-Host "Listo. Tu rutina de hoy (cada paso tiene su porque en GUIA_PRACTICANTE.md):"
Write-Host "  1. cd `"$RepoDir`"   (activa el entorno: .venv\Scripts\Activate.ps1)"
Write-Host "  2. Lee tu Issue y el bloque de tu semana en program\01_CURRICULUM\pack_contexto.md"
Write-Host "  3. Trabaja en una rama issue-N-<slug>, commits chicos, y abre el PR con 'Closes #N'"
Write-Host "  4. Al terminar, completa tu bitacora: $Nota"
Write-Host "Donde mirar: https://github.com/users/jackthony/projects/3 (vista 'Mis tareas')"
Write-Host "----------------------------------------------------------"
