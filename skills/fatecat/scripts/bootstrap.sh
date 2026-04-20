#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

runtime_root="$(resolve_runtime_root)"
with_dev="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-dev)
      with_dev="1"
      shift
      ;;
    *)
      echo "未知参数: $1" >&2
      exit 2
      ;;
  esac
done

cd "${runtime_root}"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

.venv/bin/pip install -q --upgrade pip
if [[ "${with_dev}" == "1" ]]; then
  .venv/bin/pip install -q -e '.[dev]'
else
  .venv/bin/pip install -q -e .
fi

echo "FateCat runtime 已准备完成: ${runtime_root}"
