#!/usr/bin/env bash
# Se estiver no zsh, reexecuta em bash para evitar problemas
if [ -n "${ZSH_VERSION-}" ]; then
  exec bash "$0" "$@"
fi

# Sai no erro, usa variaveis nao declaradas como erro, falha em pipes
set -euo pipefail

# ---------- utilitario ----------
run() { echo "+ $*"; "$@"; }

# ---------- solicitacao de argumentos ----------
# Usuario GitHub
if [ -z "${1-}" ]; then
    read -p "Enter GitHub username: " USER
else
    USER="$1"
fi

# Organizacao GitHub
if [ -z "${2-}" ]; then
    read -p "Enter GitHub organization: " ORG
else
    ORG="$2"
fi

# ---------- desativa pager do gh ----------
export GH_PAGER=""

# ---------- lista repositorios ----------
repos=$(gh repo list "$USER" --limit 500 --json name -q '.[].name')

# ---------- loop de transferencia ----------
for repo in $repos; do
    echo "==============================="
    echo "Transferring repository: $repo"

    # Tenta transferir o repositorio
    if run gh api \
      -X POST \
      -H "Accept: application/vnd.github.v3+json" \
      /repos/"$USER"/"$repo"/transfer \
      -f new_owner="$ORG" \
      >/dev/null 2>&1
    then
        echo "Success: $repo transferred to $ORG"
    else
        echo "Error transferring $repo. Maybe already transferred or no permission."
    fi
done
