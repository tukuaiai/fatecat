#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

remove_venv="0"
dry_run="0"

usage() {
  cat <<'EOF'
用法:
  bash scripts/clean-runtime.sh [--venv] [--dry-run]

说明:
  - 清理根 skill 输出目录与 project 内的本地缓存
  - 默认不删除 project/.venv；如需彻底重建环境，再加 --venv
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --venv)
      remove_venv="1"
      shift
      ;;
    --dry-run)
      dry_run="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage_error "未知参数: $1"
      ;;
  esac
done

targets=(
  "${skill_root}/output"
  "${project_root}/.pytest_cache"
  "${project_root}/.ruff_cache"
  "${project_root}/.mypy_cache"
  "${project_root}/modules/telegram/output"
)

if [[ "${remove_venv}" == "1" ]]; then
  targets+=("${project_root}/.venv")
fi

for target in "${targets[@]}"; do
  if [[ ! -e "${target}" ]]; then
    continue
  fi

  if [[ "${dry_run}" == "1" ]]; then
    echo "[clean-runtime] would remove ${target}"
    continue
  fi

  rm -rf "${target}"
  echo "[clean-runtime] removed ${target}"
done
