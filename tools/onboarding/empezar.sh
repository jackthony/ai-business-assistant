#!/usr/bin/env bash
# Empieza (o retoma) tu día de práctica con orden profesional. macOS / Linux / Git Bash.
#   bash tools/onboarding/empezar.sh            # primera vez y cada día de práctica
#   EMPEZAR_RAIZ=~/otra-carpeta bash tools/onboarding/empezar.sh
# Es idempotente: puedes correrlo todos los días. Qué hace, y por qué:
#   1. Tu trabajo vive en UNA carpeta ordenada (no en Descargas): ahí encuentras todo y llevas tu avance.
#   2. Clona o actualiza el repo (git pull): empezar con el código viejo es la causa nº1 de conflictos.
#   3. Prepara el entorno (Python 3.11, dependencias, pre-commit): lo que corre en tu PC = lo que corre el CI.
#   4. Revisa tu identidad de git: tu correo personal no debe quedar en un historial público.
#   5. Crea la bitácora de HOY: lo que no se escribe no se aprende (y alimenta tu informe FPE).
set -euo pipefail

REPO_URL="${EMPEZAR_REPO:-https://github.com/jackthony/ai-business-assistant.git}"
RAIZ="${EMPEZAR_RAIZ:-$HOME/senati-2026}"
REPO_DIR="$RAIZ/ai-business-assistant"
SIN_INSTALAR="${EMPEZAR_SIN_INSTALAR:-0}"
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

paso() { printf '\n\033[1m▶ %s\033[0m\n' "$1"; }
ok()   { printf '  ✅ %s\n' "$1"; }
aviso(){ printf '  ⚠️  %s\n' "$1"; }
falta(){ printf '  ❌ %s\n' "$1"; exit 1; }

paso "1/5  Tu carpeta de trabajo: $RAIZ"
mkdir -p "$RAIZ"/{bitacora,evidencias,informes,notas-estudio}
ok "bitacora/ (diario) · evidencias/ (capturas y videos por Issue) · informes/ (borradores FPE) · notas-estudio/ (lo que lees y entiendes)"

paso "2/5  El repositorio (siempre actualizado)"
command -v git >/dev/null || falta "Instala git: https://git-scm.com/downloads"
if [ -d "$REPO_DIR/.git" ]; then
  git -C "$REPO_DIR" pull --ff-only && ok "repo actualizado en $REPO_DIR"
else
  git clone "$REPO_URL" "$REPO_DIR" && ok "repo clonado en $REPO_DIR"
fi
QUE_CORRE="$(cd "$AQUI/../.." 2>/dev/null && pwd || true)"
if [ -n "$QUE_CORRE" ] && [ "$QUE_CORRE" != "$REPO_DIR" ] && [ "$QUE_CORRE" != "$(cd "$REPO_DIR" && pwd)" ]; then
  aviso "Estás usando una copia en $QUE_CORRE. Trabaja SOLO desde: $REPO_DIR (borra la otra copia cuando quieras)."
fi

paso "3/5  Entorno de Python 3.11"
PY="${EMPEZAR_PYTHON:-}"
if [ -z "$PY" ]; then
  for candidato in python3.11 python3 python; do
    if command -v "$candidato" >/dev/null && "$candidato" -c 'import sys; sys.exit(0 if sys.version_info[:2]==(3,11) else 1)' 2>/dev/null; then PY="$candidato"; break; fi
  done
fi
if [ "$SIN_INSTALAR" = "1" ]; then
  aviso "EMPEZAR_SIN_INSTALAR=1: se omite el entorno (solo para pruebas)"
elif [ -z "$PY" ]; then
  falta "No encontré Python 3.11 (el CI usa 3.11; no uses 3.12/3.13). Instálalo: https://www.python.org/downloads/release/python-3119/"
else
  [ -d "$REPO_DIR/.venv" ] || "$PY" -m venv "$REPO_DIR/.venv"
  # shellcheck disable=SC1091
  if [ -f "$REPO_DIR/.venv/bin/activate" ]; then . "$REPO_DIR/.venv/bin/activate"; else . "$REPO_DIR/.venv/Scripts/activate"; fi
  (cd "$REPO_DIR" && python -m pip install -q -U pip && pip install -q -e ".[dev]" && pre-commit install)
  ok "entorno listo (.venv) y pre-commit instalado: ruff corre solo en cada commit"
  [ -f "$REPO_DIR/.env" ] || { cp "$REPO_DIR/.env.example" "$REPO_DIR/.env"; ok ".env creado desde .env.example (NUNCA se sube al repo; pon aquí tus claves de prueba)"; }
fi

paso "4/5  Tu identidad de git (el historial es público)"
CORREO="$(git -C "$REPO_DIR" config user.email || true)"
case "$CORREO" in
  *noreply.github.com) ok "usas el correo privado de GitHub ($CORREO)" ;;
  "") aviso "No tienes correo configurado. GitHub → Settings → Emails → «Keep my email addresses private» y copia tu correo ...@users.noreply.github.com; luego: git config --global user.email \"ese-correo\" y git config --global user.name \"Tu Nombre\"" ;;
  *) aviso "Tu correo ($CORREO) quedaría público en tus commits. Cámbialo al noreply: GitHub → Settings → Emails → «Keep my email addresses private» + «Block command line pushes that expose my email»; luego: git config --global user.email \"tu-id+usuario@users.noreply.github.com\"" ;;
esac

paso "5/5  Tu bitácora de hoy"
HOY="$(date +%Y-%m-%d)"
NOTA="$RAIZ/bitacora/$HOY.md"
if [ ! -f "$NOTA" ]; then
  sed "s/AAAA-MM-DD/$HOY/" "$AQUI/plantilla-bitacora.md" > "$NOTA" && ok "creada $NOTA"
else
  ok "ya existe $NOTA"
fi

cat <<FIN

──────────────────────────────────────────────────────────
Listo. Tu rutina de hoy (cada paso tiene su porqué en GUIA_PRACTICANTE.md):
  1. cd "$REPO_DIR"   (activa el entorno: source .venv/bin/activate  ·  Windows: .venv\\Scripts\\Activate.ps1)
  2. Lee tu Issue y el bloque de tu semana en program/01_CURRICULUM/pack_contexto.md
  3. Trabaja en una rama issue-N-<slug>, commits chicos, y abre el PR con "Closes #N"
  4. Al terminar, completa tu bitácora: $NOTA
Dónde mirar: https://github.com/users/jackthony/projects/3 (vista «🎯 Mis tareas»)
──────────────────────────────────────────────────────────
FIN
