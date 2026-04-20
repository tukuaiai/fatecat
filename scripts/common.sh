#!/usr/bin/env bash
set -euo pipefail

skill_scripts_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
skill_root="$(cd -- "${skill_scripts_dir}/.." && pwd)"
project_root="${skill_root}/project"

project_ready() {
  [[ -f "${project_root}/pyproject.toml" && -x "${project_root}/.venv/bin/fatecat" ]]
}

project_exists() {
  [[ -f "${project_root}/pyproject.toml" ]]
}

resolve_runtime_root() {
  if project_ready; then
    printf '%s\n' "${project_root}"
    return 0
  fi

  if project_exists; then
    printf '%s\n' "${project_root}"
    return 0
  fi

  echo "无法定位 FateCat 项目根目录：缺少 ${project_root}。" >&2
  return 1
}

resolve_bootstrap_root() {
  resolve_runtime_root
}

fatecat_entrypoint_healthy() {
  local runtime_root="$1"
  local bin_path="${runtime_root}/.venv/bin/fatecat"

  if [[ ! -x "${bin_path}" ]]; then
    return 1
  fi

  local shebang
  shebang="$(head -n 1 "${bin_path}" 2>/dev/null || true)"
  if [[ "${shebang}" == '#!'/* ]]; then
    [[ -x "${shebang#\#!}" ]]
    return $?
  fi

  return 0
}

resolve_fatecat_bin() {
  local runtime_root="$1"
  if fatecat_entrypoint_healthy "${runtime_root}"; then
    printf '%s\n' "${runtime_root}/.venv/bin/fatecat"
    return 0
  fi

  if [[ -x "${runtime_root}/.venv/bin/fatecat" ]]; then
    echo "检测到 ${runtime_root}/.venv/bin/fatecat 指向旧路径，请先执行 bootstrap.sh 修复虚拟环境入口。" >&2
    return 1
  fi

  echo "未找到 ${runtime_root}/.venv/bin/fatecat，请先执行 bootstrap.sh。" >&2
  return 1
}
