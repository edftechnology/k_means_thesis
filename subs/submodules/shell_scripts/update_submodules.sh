#!/usr/bin/env bash
# Script para automatizar commits/push em submódulos + repo pai

set -euo pipefail

# ---------- util ----------
run() { echo "+ $*"; "$@"; }

# ---------- parâmetros ----------
COMMIT_MSG="${1:-Update submodules}"

# ---------- atualizar todos os submódulos para o último commit remoto ----------
echo "[INFO] Updating all submodules to latest remote commits"
run git submodule update --init --recursive --remote

# ---------- obter caminhos dos submódulos ----------
SUBMODULES=$(git config --file .gitmodules --get-regexp path | awk '{print $2}')

for SUBMODULE_PATH in $SUBMODULES; do
  echo "[INFO] Entering submodule: $SUBMODULE_PATH"
  pushd "$SUBMODULE_PATH" >/dev/null

  if [[ -n $(git status --porcelain) ]]; then
    run git add -A
    run git commit -m "$COMMIT_MSG ($SUBMODULE_PATH)"
    run git push origin main
  else
    echo "[INFO] No changes in submodule."
  fi

  popd >/dev/null

  echo "[INFO] Updating submodule pointer in parent repository"
  run git add "$SUBMODULE_PATH"
  if ! git diff --cached --quiet "$SUBMODULE_PATH"; then
    run git commit -m "$COMMIT_MSG ($SUBMODULE_PATH)"
    run git push origin main
  else
    echo "[INFO] No submodule pointer changes detected in parent repository."
  fi
done

echo "[INFO] Script finished successfully"

# OPENAI.
# Depurar código Shell.
# Disponível em <https://chatgpt.com/g/g-p-6761f07a2b1c81918aa789debc65d68c/c/67c06bee-d0b8-8002-aa30-d2d0d57f1cfe>.
# Acessado em: 26/08/2025 15:08.
