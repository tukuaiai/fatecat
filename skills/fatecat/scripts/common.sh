#!/usr/bin/env bash
set -euo pipefail

skill_scripts_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
skill_root="$(cd -- "${skill_scripts_dir}/.." && pwd)"
embedded_runtime_root="${skill_root}/scripts/fatecat_runtime"

resolve_repo_runtime_root() {
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

embedded_runtime_ready() {
  [[ -f "${embedded_runtime_root}/pyproject.toml" && -x "${embedded_runtime_root}/.venv/bin/fatecat" ]]
}

embedded_runtime_exists() {
  [[ -f "${embedded_runtime_root}/pyproject.toml" ]]
}

resolve_runtime_root() {
  if embedded_runtime_ready; then
    printf '%s\n' "${embedded_runtime_root}"
    return 0
  fi

  if resolve_repo_runtime_root >/dev/null 2>&1; then
    resolve_repo_runtime_root
    return 0
  fi

  if embedded_runtime_exists; then
    printf '%s\n' "${embedded_runtime_root}"
    return 0
  fi

  echo "无法定位 FateCat runtime 根目录。" >&2
  return 1
}

resolve_bootstrap_root() {
  if embedded_runtime_exists; then
    printf '%s\n' "${embedded_runtime_root}"
    return 0
  fi
  resolve_repo_runtime_root
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
