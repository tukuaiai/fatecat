#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

repo_root="$(resolve_repo_runtime_root)"
dest_root="${embedded_runtime_root}"

if [[ "${repo_root}" == "${dest_root}" ]]; then
  echo "当前已经位于嵌入式 runtime，无法再从自身同步。" >&2
  exit 2
fi

mkdir -p "${dest_root}"

rsync -a --delete \
  --exclude '.git/' \
  --exclude '.venv/' \
  --exclude '.pytest_cache/' \
  --exclude '.ruff_cache/' \
  --exclude '.mypy_cache/' \
  --exclude 'skills/' \
  --exclude 'assets/config/.env' \
  --exclude 'runtime/database/**/*.db' \
  "${repo_root}/README.md" \
  "${repo_root}/Makefile" \
  "${repo_root}/pyproject.toml" \
  "${repo_root}/assets" \
  "${repo_root}/modules" \
  "${repo_root}/scripts" \
  "${repo_root}/tests" \
  "${repo_root}/runtime" \
  "${dest_root}/"

rm -f "${dest_root}/runtime/database/bazi/bazi.db"
mkdir -p "${dest_root}/runtime/database/bazi"
touch "${dest_root}/runtime/database/bazi/.gitkeep"

echo "同步完成: ${dest_root}"
