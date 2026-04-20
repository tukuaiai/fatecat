#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_bootstrap_root)"
with_dev="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-dev)
      with_dev="1"
      shift
      ;;
    *)
      usage_error "未知参数: $1"
      ;;
  esac
done

ensure_command python3

cd "${runtime_root}"

rebuild_reason=""
if ! python_entrypoint_healthy "${runtime_root}"; then
  rebuild_reason="python 入口缺失或已失效"
elif venv_has_stale_entrypoints "${runtime_root}"; then
  rebuild_reason=".venv/bin 内存在指向旧路径的入口脚本"
fi

if [[ -n "${rebuild_reason}" ]]; then
  echo "[bootstrap] 重建虚拟环境: ${rebuild_reason}"
  rm -rf .venv
  python3 -m venv .venv
fi

.venv/bin/python -m pip install -q --upgrade pip
if [[ "${with_dev}" == "1" ]]; then
  .venv/bin/python -m pip install -q -e '.[dev]'
else
  .venv/bin/python -m pip install -q -e .
fi

python_entrypoint_healthy "${runtime_root}" || die "bootstrap 后 python 入口仍不可用"
fatecat_entrypoint_healthy "${runtime_root}" || die "bootstrap 后 fatecat 入口仍不可用"
if venv_has_stale_entrypoints "${runtime_root}"; then
  die "bootstrap 后仍检测到旧路径入口脚本，请检查 .venv/bin"
fi

if [[ "${with_dev}" == "1" && ! -x .venv/bin/pytest ]]; then
  die "已请求 --with-dev，但未生成 .venv/bin/pytest"
fi

echo "FateCat runtime 已准备完成: ${runtime_root}"
