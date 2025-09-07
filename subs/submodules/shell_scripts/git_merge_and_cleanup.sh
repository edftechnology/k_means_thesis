#!/usr/bin/env bash
# Se estiver no zsh, reexecuta em bash para evitar problemas de arrays/prompt
if [ -n "${ZSH_VERSION-}" ]; then
  exec bash "$0" "$@"
fi

set -euo pipefail

# ---------- util ----------
run() { echo "+ $*"; "$@"; }

# ---------- fetch ----------
echo "[INFO] Fetching all branches from remote..."
run git fetch --all

# ---------- montar lista (separar locais e remotas) ----------
echo "[INFO] Building branch list (local + remote)..."
LOCAL_BRANCHES=()
REMOTE_BRANCHES=()
BRANCHES=()

# Locais (ordenados)
while read -r b; do
  [ -z "$b" ] && continue
  LOCAL_BRANCHES+=("$b")
done < <(git branch --format='%(refname:short)' | sort -u)

# Remotas reais: refs/remotes/origin/*, ignorando origin/HEAD e duplicadas
while read -r rb; do
  name="${rb#origin/}"
  [ "$name" = "HEAD" ] && continue
  if ! printf '%s\n' "${LOCAL_BRANCHES[@]}" | grep -qx "$name"; then
    REMOTE_BRANCHES+=("$name")
  fi
done < <(git for-each-ref --format='%(refname:short)' refs/remotes/origin | sort -u)

# Se continuar vazio, força "main"
if [ ${#LOCAL_BRANCHES[@]} -eq 0 ] && [ ${#REMOTE_BRANCHES[@]} -eq 0 ]; then
  LOCAL_BRANCHES=("main")
fi

# Mostrar numeradas (primeiro locais, depois remotas)
echo "[INFO] Available branches:"
idx=1
for b in "${LOCAL_BRANCHES[@]}"; do
  printf "  [%d] %s (local)\n" "$idx" "$b"
  BRANCHES+=("$b")
  idx=$((idx+1))
done
for b in "${REMOTE_BRANCHES[@]}"; do
  printf "  [%d] %s (remote)\n" "$idx" "$b"
  BRANCHES+=("$b")
  idx=$((idx+1))
done

# ---------- default SOURCE ----------
LAST_REMOTE_BRANCH="$(git for-each-ref --sort=-committerdate --format='%(refname:short)' refs/remotes/origin \
  | grep -v '^origin/HEAD$' | sed 's|^origin/||' | head -n 1 || true)"

DEFAULT_SRC_INDEX=1
if [ -n "${LAST_REMOTE_BRANCH:-}" ]; then
  for i in "${!BRANCHES[@]}"; do
    if [ "${BRANCHES[$i]}" = "$LAST_REMOTE_BRANCH" ]; then
      DEFAULT_SRC_INDEX=$((i+1))
      break
    fi
  done
fi

# Escolher SOURCE
echo -n "Enter the number of the SOURCE branch to merge FROM [default: ${DEFAULT_SRC_INDEX}]: "
read -r SRC_NUM
SRC_NUM=${SRC_NUM:-$DEFAULT_SRC_INDEX}
if ! [[ "$SRC_NUM" =~ ^[0-9]+$ ]] || [ "$SRC_NUM" -lt 1 ] || [ "$SRC_NUM" -gt "${#BRANCHES[@]}" ]; then
  echo "[ERROR] Invalid selection for SOURCE."
  exit 1
fi
SRC_BRANCH="${BRANCHES[$((SRC_NUM-1))]}"
echo "[INFO] SOURCE branch: $SRC_BRANCH"

# ---------- default TARGET ----------
current_branch="$(git rev-parse --abbrev-ref HEAD)"
DEFAULT_TGT_INDEX=1
for i in "${!BRANCHES[@]}"; do
  if [ "${BRANCHES[$i]}" = "$current_branch" ]; then
    DEFAULT_TGT_INDEX=$((i+1))
    break
  fi
done
if [ "$DEFAULT_TGT_INDEX" -eq 1 ] && [ "$current_branch" != "main" ]; then
  for i in "${!BRANCHES[@]}"; do
    if [ "${BRANCHES[$i]}" = "main" ]; then
      DEFAULT_TGT_INDEX=$((i+1))
      break
    fi
  done
fi

# Escolher TARGET
echo -n "Enter the number of the TARGET branch to merge INTO [default: ${DEFAULT_TGT_INDEX}]: "
read -r TGT_NUM
TGT_NUM=${TGT_NUM:-$DEFAULT_TGT_INDEX}
if ! [[ "$TGT_NUM" =~ ^[0-9]+$ ]] || [ "$TGT_NUM" -lt 1 ] || [ "$TGT_NUM" -gt "${#BRANCHES[@]}" ]; then
  echo "[ERROR] Invalid selection for TARGET."
  exit 1
fi
TGT_BRANCH="${BRANCHES[$((TGT_NUM-1))]}"
echo "[INFO] TARGET branch: $TGT_BRANCH"

# --- SSH key check ---
if ssh-add -l >/dev/null 2>&1; then
    echo "[INFO] SSH key already loaded in agent."
else
    echo "[INFO] No SSH key loaded. Starting ssh-agent..."
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_rsa
fi

# ---------- atualizar e commitar submódulos antes do commit de segurança ----------
COMMIT_MSG="Update submodules before merge"
echo "[INFO] Checking submodules for pending changes before merge..."
SUBMODULES=$(git config --file .gitmodules --get-regexp path | awk '{print $2}')

for SUBMODULE_PATH in $SUBMODULES; do
  echo "[INFO] Entering submodule: $SUBMODULE_PATH"
  pushd "$SUBMODULE_PATH" >/dev/null

  if [[ -n $(git status --porcelain) ]]; then
    run git add -A
    run git commit -m "$COMMIT_MSG ($SUBMODULE_PATH)" || true
    run git push origin main || true
  else
    echo "[INFO] No changes in submodule."
  fi

  popd >/dev/null

  echo "[INFO] Updating submodule pointer in parent repository"
  run git add "$SUBMODULE_PATH"
  if ! git diff --cached --quiet "$SUBMODULE_PATH"; then
    run git commit -m "$COMMIT_MSG ($SUBMODULE_PATH)" || true
    run git push origin main || true
  else
    echo "[INFO] No pointer update needed for $SUBMODULE_PATH"
  fi
done

# ---------- commit de segurança ----------
if [[ -n $(git status --porcelain) ]]; then
  echo "[INFO] Local changes detected. Performing automatic commit..."
  run git add -A
  run git commit -m "Automatic backup before merge"
else
  echo "[INFO] No local changes pending."
fi

# ---------- preparar TARGET ----------
echo "[INFO] Switching to TARGET: $TGT_BRANCH"
if git show-ref --verify --quiet "refs/heads/$TGT_BRANCH"; then
  run git switch "$TGT_BRANCH"
else
  if git show-ref --verify --quiet "refs/remotes/origin/$TGT_BRANCH"; then
    run git switch -c "$TGT_BRANCH" --track "origin/$TGT_BRANCH"
  else
    run git switch -c "$TGT_BRANCH"
  fi
fi
run git pull --ff-only origin "$TGT_BRANCH" || true
run git push -u origin "$TGT_BRANCH" || true

# ---------- garantir SOURCE local ----------
if git show-ref --verify --quiet "refs/heads/$SRC_BRANCH"; then
  echo "[INFO] SOURCE exists locally."
else
  if git show-ref --verify --quiet "refs/remotes/origin/$SRC_BRANCH"; then
    echo "[INFO] Creating local SOURCE from origin/$SRC_BRANCH"
    run git fetch origin "$SRC_BRANCH"
    run git branch "$SRC_BRANCH" "origin/$SRC_BRANCH"
  else
    echo "[ERROR] SOURCE branch not found locally or on origin: $SRC_BRANCH"
    exit 1
  fi
fi

# ---------- merge ----------
echo "[INFO] Merging '$SRC_BRANCH' into '$TGT_BRANCH'"
set +e
git merge "$SRC_BRANCH" --no-edit
merge_status=$?
set -e

if [ "$merge_status" -ne 0 ]; then
  echo "[ERROR] Merge has conflicts. Resolve them, then run:"
  echo "  git diff --name-only --diff-filter=U"
  echo "  edit files, then: git add -A && git commit --no-edit && git push"
  exit 1
fi

run git status --short
run git push

# ---------- atualizar e commitar submódulos depois do merge ----------
COMMIT_MSG="Update submodules after merge"
echo "[INFO] Updating all submodules to latest remote commits"
run git submodule update --init --recursive --remote

for SUBMODULE_PATH in $SUBMODULES; do
  echo "[INFO] Entering submodule: $SUBMODULE_PATH"
  pushd "$SUBMODULE_PATH" >/dev/null

  if [[ -n $(git status --porcelain) ]]; then
    run git add -A
    run git commit -m "$COMMIT_MSG ($SUBMODULE_PATH)" || true
    run git push origin main || true
  else
    echo "[INFO] No changes in submodule."
  fi

  popd >/dev/null

  echo "[INFO] Updating submodule pointer in parent repository"
  run git add "$SUBMODULE_PATH"
  if ! git diff --cached --quiet "$SUBMODULE_PATH"; then
    run git commit -m "$COMMIT_MSG ($SUBMODULE_PATH)" || true
    run git push origin "$TGT_BRANCH" || true
  else
    echo "[INFO] No submodule pointer changes detected in parent repository."
  fi
done

# ---------- remover duplicados ----------
echo "[INFO] Checking for duplicate files in project root..."
for f in *; do
  [ -f "$f" ] || continue
  case "$f" in
    README*|LICENSE*|MANIFEST.in|setup.py|*.md|*.txt)
      continue ;; # manter arquivos importantes de metadados
  esac
  for sub in $(git config --file .gitmodules --get-regexp path | awk '{print $2}'); do
    if [ -f "$sub/$f" ]; then
      echo "[WARN] Duplicate found: $f also in $sub/"
      rm -f "$f"
      echo "[INFO] Removed duplicate $f from project root"
      break
    fi
  done
done

# ---------- commit de limpeza ----------
if [[ -n $(git status --porcelain) ]]; then
  echo "[INFO] Committing cleanup of duplicates..."
  run git add -A
  run git commit -m "Cleanup: remove duplicate files from project root"
  run git push
fi

# ---------- limpeza local (codex/*) ----------
echo "[INFO] Cleaning up local 'codex/*' branches..."
git for-each-ref --format='%(refname:short)' refs/heads/codex/* 2>/dev/null \
  | while read -r delb; do
      [ -z "$delb" ] && continue
      echo "[INFO] Deleting local branch: $delb"
      git branch -D "$delb" || true
    done

# ---------- limpeza remota (codex/*) ----------
echo "[INFO] Cleaning up remote 'codex/*' branches..."
git for-each-ref --format='%(refname:short)' refs/remotes/origin/codex/* 2>/dev/null \
  | sed 's|^origin/||' \
  | while read -r rdelb; do
      [ -z "$rdelb" ] && continue
      echo "[INFO] Deleting remote branch: $rdelb"
      git push origin --delete "$rdelb" || true
    done

echo "[INFO] Done."
echo "[INFO] Local branches:"
run git branch --format='%(refname:short)' | cat
echo "[INFO] Remote branches:"
run git branch -r | cat

run git status

# OPENAI.
# Depurar código Shell.
# Disponível em <https://chatgpt.com/g/g-p-6761f07a2b1c81918aa789debc65d68c/c/67c06bee-d0b8-8002-aa30-d2d0d57f1cfe>.
# Acessado em: 26/08/2025 15:08.
