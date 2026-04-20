#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

output_dir=""
runtime_root="$(resolve_runtime_root)"
repo_root="$(cd "${runtime_root}" && pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output)
      output_dir="$2"
      shift 2
      ;;
    *)
      echo "未知参数: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "${output_dir}" ]]; then
  echo "用法: bash skills/fatecat/scripts/export-runtime.sh --output <dir>" >&2
  exit 2
fi

dest_root="$(mkdir -p "${output_dir}" && cd "${output_dir}" && pwd)"
case "${dest_root}" in
  "${repo_root}"|"${repo_root}/"* )
    echo "导出目录不能位于当前 FateCat 源仓库内部，否则会形成递归复制。" >&2
    exit 2
    ;;
esac

dest_skill="${dest_root}/skills/fatecat"
dest_runtime="${dest_skill}/scripts/fatecat_runtime"
mkdir -p "${dest_runtime}"

rsync -a \
  --exclude 'scripts/fatecat_runtime/' \
  "${skill_root}/" \
  "${dest_skill}/"

rsync -a \
  --exclude '.git/' \
  --exclude '.venv/' \
  --exclude '.pytest_cache/' \
  --exclude '.ruff_cache/' \
  --exclude '.mypy_cache/' \
  --exclude 'assets/config/.env' \
  --exclude 'runtime/**/*.db' \
  "${repo_root}/AGENTS.md" \
  "${repo_root}/README.md" \
  "${repo_root}/Makefile" \
  "${repo_root}/pyproject.toml" \
  "${repo_root}/assets" \
  "${repo_root}/modules" \
  "${repo_root}/scripts" \
  "${repo_root}/tests" \
  "${repo_root}/runtime" \
  "${dest_runtime}/"

mkdir -p "${dest_runtime}/runtime/database/bazi"
touch "${dest_runtime}/runtime/database/bazi/.gitkeep"

if [[ -f "${dest_runtime}/runtime/database/bazi/bazi.db" ]]; then
  rm -f "${dest_runtime}/runtime/database/bazi/bazi.db"
fi

echo "导出完成: ${dest_skill}"
