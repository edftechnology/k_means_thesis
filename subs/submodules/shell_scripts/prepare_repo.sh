#!/usr/bin/env bash
# Se estiver no zsh, reexecuta em bash para evitar problemas
if [ -n "${ZSH_VERSION-}" ]; then
  exec bash "$0" "$@"
fi

set -euo pipefail

# ---------- utilitario ----------
run() { echo "+ $*"; "$@"; }

# ---------- definir raiz do projeto ----------
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$PROJECT_ROOT" || {
  echo "[ERROR] Could not cd into $PROJECT_ROOT"
  exit 1
}

echo "[INFO] Project root set to: $PROJECT_ROOT"

# ---------- checagem de chave SSH ----------
if ssh-add -l >/dev/null 2>&1; then
    echo "[INFO] SSH key already loaded in agent."
else
    echo "[INFO] No SSH key loaded. Starting ssh-agent..."
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_rsa || {
      echo "[ERROR] Could not add ~/.ssh/id_rsa"
      exit 1
    }
fi

# ---------- lista de submodulos ----------
SUBMODULES=(
  "subs/submodules/agents"
  "subs/submodules/git_scripts"
  "subs/submodules/python_scripts"
  "subs/submodules/shell_scripts"
  "subs/submodules/txt_scripts"
  ".github/workflows"
  ".vscode"
)

# ---------- funcao para garantir excecao no .gitignore ----------
ensure_gitignore_exception() {
  local path="$1"
  if git check-ignore -q "$path"; then
    echo "[WARN] Path $path is ignored by .gitignore"
    echo "[INFO] Adding exception for $path in .gitignore"
    echo "!$path/" >> .gitignore
  fi
}

# ---------- commit de seguranca ----------
if [[ -n $(git status --porcelain) ]]; then
  echo "[INFO] Local changes detected. Performing automatic commit..."
  run git add -A
  run git commit -m "Automatic backup before syncing submodules" || true
else
  echo "[INFO] No local changes pending."
fi

# ---------- funcao para adicionar ou atualizar submodulos ----------
OWNER="edftechnology"
add_or_update_submodule() {
  local path="$1"
  local repo_name
  repo_name="$(basename "$path")"
  local url="git@github.com:$OWNER/$repo_name.git"

  ensure_gitignore_exception "$path"

  if [ -d "$path/.git" ] || [ -f "$path/.git" ]; then
    echo "[INFO] Submodule $repo_name already exists. Updating from remote..."
    (cd "$path" && run git fetch origin && run git pull origin main) || {
      echo "[ERROR] Could not update $repo_name, skipping."
      return
    }
  else
    echo "[INFO] Adding new submodule: $repo_name at $path"
    run git submodule add "$url" "$path"
  fi
}

# ---------- funcao para atualizar ponteiro no repo pai ----------
update_submodule_pointer() {
  local path="$1"
  echo "[INFO] Updating pointer for $path in parent repo"
  run git add "$path"
  if [[ -n $(git diff --cached --name-only) ]]; then
    run git commit -m "Update pointer for $path" || true
    run git push origin main || true
  else
    echo "[INFO] No pointer update needed for $path"
  fi
}

# ---------- processar todos os submodulos ----------
for sub in "${SUBMODULES[@]}"; do
  add_or_update_submodule "$sub"
done

echo "[INFO] Syncing all submodules recursively..."
run git submodule update --init --recursive --remote

for sub in "${SUBMODULES[@]}"; do
  update_submodule_pointer "$sub"
done

# ---------- copiar scripts e AGENTS.md para raiz ----------
copy_missing_to_root() {
  local src_dir="$1"
  if [ -d "$src_dir" ]; then
    shopt -s dotglob
    for file in "$src_dir"/*; do
      local base="$(basename "$file")"
      if [ ! -e "$PROJECT_ROOT/$base" ]; then
        echo "[INFO] Copying $base from $src_dir to $PROJECT_ROOT"
        run cp -r "$file" "$PROJECT_ROOT/"
      fi
    done
    shopt -u dotglob
  fi
}

copy_missing_to_root "subs/submodules/git_scripts"
copy_missing_to_root "subs/submodules/txt_scripts"

if [ -f "subs/submodules/agents/AGENTS.md" ] && [ ! -f "$PROJECT_ROOT/AGENTS.md" ]; then
  echo "[INFO] Copying AGENTS.md from subs/submodules/agents to $PROJECT_ROOT"
  run cp "subs/submodules/agents/AGENTS.md" "$PROJECT_ROOT/"
fi

# ---------- mover duplicados do python_scripts ----------
if [ -d "subs/submodules/python_scripts" ]; then
  for file in subs/submodules/python_scripts/*; do
    base="$(basename "$file")"
    if [ -e "$PROJECT_ROOT/$base" ] && [ ! -d "$PROJECT_ROOT/$base" ]; then
      echo "[INFO] Removing duplicate $base from $PROJECT_ROOT (kept in python_scripts)"
      run rm -f "$PROJECT_ROOT/$base"
    fi
  done
fi

# ---------- criar pastas fixas ----------
FOLDERS=(
  "main"
  "docs"
  "inputs"
  "outputs"
  "tests"
  "venvs"
)

for folder in "${FOLDERS[@]}"; do
  if [ ! -d "$PROJECT_ROOT/$folder" ]; then
    echo "[INFO] Creating folder: $folder"
    run mkdir -p "$PROJECT_ROOT/$folder"
  fi
done

# ---------- criar __init__.py em todas as pastas ----------
while IFS= read -r -d '' dir; do
  if [ ! -f "$dir/__init__.py" ]; then
    echo "[INFO] Creating __init__.py in $dir"
    run touch "$dir/__init__.py"
  fi
done < <(find "$PROJECT_ROOT" -type d -print0)

echo "[INFO] Script completed."
