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

# ---------- montar lista (local + remota) ----------
echo "[INFO] Building branch list (local + remote)..."
BRANCHES=()

# Locais (curto, ordenado)
while read -r b; do
  [ -z "$b" ] && continue
  BRANCHES+=("$b")
done < <(git branch --format='%(refname:short)' | sort -u)

# Remotas reais: refs/remotes/origin/*, ignorando origin/HEAD
while read -r rb; do
  name="${rb#origin/}"
  if [[ "$name" = "HEAD" ]] || [[ "$name" = "origin" ]] || [[ " ${BRANCHES[*]} " =~ " $name " ]]; then
    continue
  fi
  BRANCHES+=("$name")
done < <(git for-each-ref --format='%(refname:short)' refs/remotes/origin | sort -u)

# Mostrar numeradas
echo "[INFO] Available branches:"
idx=1
for b in "${BRANCHES[@]}"; do
  if git show-ref --verify --quiet "refs/heads/$b"; then
    suffix="(local)"
  else
    suffix="(remote)"
  fi
  printf "  [%d] %s %s\n" "$idx" "$b" "$suffix"
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

# ---------- commit de segurança ----------
if [[ -n $(git status --porcelain) ]]; then
  echo "[INFO] Local changes detected. Performing automatic commit..."
  run git add .
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

# ---------- limpeza local ----------
echo "[INFO] Optional cleanup of non-protected local branches..."
current_branch="$(git rev-parse --abbrev-ref HEAD)"
git branch --format='%(refname:short)' \
  | awk -v cur="$current_branch" -v a="$TGT_BRANCH" -v b="$SRC_BRANCH" '
      $0!=cur && $0!=a && $0!=b &&
      index($0,"main")==0 && index($0,"edf")==0 && index($0,"iae")==0 &&
      index($0,"ita")==0  && index($0,"ufabc")==0
    ' \
  | while read -r delb; do
      [ -z "$delb" ] && continue
      echo "[INFO] Deleting local branch: $delb"
      git branch -D "$delb" || true
    done

# ---------- limpeza remota ----------
echo "[INFO] Optional cleanup of non-protected remote branches..."
git for-each-ref --format='%(refname:short)' refs/remotes/origin \
  | grep -v '^origin/HEAD$' \
  | sed 's|^origin/||' \
  | grep -v '^origin$' \
  | awk -v a="$TGT_BRANCH" -v b="$SRC_BRANCH" '
      NF && $0!=a && $0!=b &&
      index($0,"main")==0 && index($0,"edf")==0 && index($0,"iae")==0 &&
      index($0,"ita")==0  && index($0,"ufabc")==0
    ' \
  | while read -r rdelb; do
      [ -z "$rdelb" ] && continue
      echo "[INFO] Deleting remote branch: $rdelb"
      git push origin --delete "$rdelb" || true
    done

echo "[INFO] Done."
git branch -r | cat
git status
