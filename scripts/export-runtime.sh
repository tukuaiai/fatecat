#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

output_dir=""
runtime_root="$(resolve_runtime_root)"

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
  echo "用法: bash scripts/export-runtime.sh --output <dir>" >&2
  exit 2
fi

dest_root="$(mkdir -p "${output_dir}" && cd "${output_dir}" && pwd)"
case "${dest_root}" in
  "${skill_root}"|"${skill_root}/"* )
    echo "导出目录不能位于当前 skill 仓库内部，否则会形成递归复制。" >&2
    exit 2
    ;;
esac

rsync -a \
  --exclude '.git/' \
  --exclude '.history/' \
  --exclude 'project/.venv/' \
  --exclude 'project/.pytest_cache/' \
  --exclude 'project/.ruff_cache/' \
  --exclude 'project/.mypy_cache/' \
  --exclude 'project/assets/config/.env' \
  --exclude 'project/runtime/**/*.db' \
  "${skill_root}/" \
  "${dest_root}/"

mkdir -p "${dest_root}/project/runtime/database/bazi"
touch "${dest_root}/project/runtime/database/bazi/.gitkeep"

if [[ -f "${dest_root}/project/runtime/database/bazi/bazi.db" ]]; then
  rm -f "${dest_root}/project/runtime/database/bazi/bazi.db"
fi

echo "导出完成: ${dest_root}"
