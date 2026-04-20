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

if [[ ! -x .venv/bin/python ]]; then
  rm -rf .venv
  python3 -m venv .venv
fi

.venv/bin/python -m pip install -q --upgrade pip
if [[ "${with_dev}" == "1" ]]; then
  .venv/bin/python -m pip install -q -e '.[dev]'
else
  .venv/bin/python -m pip install -q -e .
fi

echo "FateCat runtime 已准备完成: ${runtime_root}"
