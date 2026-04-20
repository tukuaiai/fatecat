#!/usr/bin/env bash
set -euo pipefail

skill_scripts_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
skill_root="$(cd -- "${skill_scripts_dir}/.." && pwd)"

resolve_runtime_root() {
  local embedded_runtime="${skill_root}/scripts/fatecat_runtime"
  if [[ -f "${embedded_runtime}/pyproject.toml" ]]; then
    printf '%s\n' "${embedded_runtime}"
    return 0
  fi

  local current="${skill_root}"
  while [[ "${current}" != "/" ]]; do
    if [[ -f "${current}/pyproject.toml" && -d "${current}/modules/fate_core" && -d "${current}/assets" ]]; then
      printf '%s\n' "${current}"
      return 0
    fi
    current="$(dirname -- "${current}")"
  done

  echo "无法定位 FateCat runtime 根目录。若要独立运行，请先执行 export-runtime.sh 生成 scripts/fatecat_runtime/。" >&2
  return 1
}

resolve_fatecat_bin() {
  local runtime_root="$1"
  if [[ -x "${runtime_root}/.venv/bin/fatecat" ]]; then
    printf '%s\n' "${runtime_root}/.venv/bin/fatecat"
    return 0
  fi
  echo "未找到 ${runtime_root}/.venv/bin/fatecat，请先执行 bootstrap.sh。" >&2
  return 1
}
