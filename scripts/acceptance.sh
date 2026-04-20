#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

with_dev="0"
skip_strict="0"
skip_delivery="0"
delivery_target="api"
output_dir="/tmp/fatecat-acceptance"
strict_validator="${HOME}/.codex/skills/auto-skill/scripts/validate-skill.sh"

usage() {
  cat <<'EOF'
用法:
  bash scripts/acceptance.sh [--with-dev] [--skip-strict] [--skip-delivery]
                             [--delivery-target api|bot] [--output <dir>]

说明:
  - 统一执行单-skill 仓库的验收链：shell 语法 -> strict skill 校验 -> pure preflight -> pytest -> delivery smoke
  - 默认输出目录为 /tmp/fatecat-acceptance
  - 若缺少 project/assets/config/.env，则默认跳过 delivery smoke
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-dev)
      with_dev="1"
      shift
      ;;
    --skip-strict)
      skip_strict="1"
      shift
      ;;
    --skip-delivery)
      skip_delivery="1"
      shift
      ;;
    --delivery-target)
      [[ $# -ge 2 ]] || usage_error "--delivery-target 缺少参数"
      delivery_target="$2"
      shift 2
      ;;
    --output)
      [[ $# -ge 2 ]] || usage_error "--output 缺少参数"
      output_dir="$2"
      shift 2
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

case "${delivery_target}" in
  api|bot)
    ;;
  *)
    usage_error "--delivery-target 只支持 api 或 bot"
    ;;
esac

runtime_root="$(resolve_runtime_root)"
mkdir -p "${output_dir}"

bootstrap_args=()
if [[ "${with_dev}" == "1" ]]; then
  bootstrap_args+=(--with-dev)
fi

echo "[acceptance] bootstrap"
bash "${script_dir}/bootstrap.sh" "${bootstrap_args[@]}"

echo "[acceptance] shell syntax"
bash -n "${script_dir}"/*.sh

if [[ "${skip_strict}" != "1" ]]; then
  if [[ -x "${strict_validator}" ]]; then
    echo "[acceptance] strict skill validate"
    "${strict_validator}" "${skill_root}" --strict
  else
    echo "[acceptance] skip strict: 未找到 ${strict_validator}"
  fi
fi

echo "[acceptance] pure preflight smoke"
bash "${script_dir}/preflight.sh" \
  --mode pure \
  --bootstrap \
  --smoke \
  --output-file "${output_dir}/preflight-pure.json" \
  --pretty

echo "[acceptance] pytest"
"${runtime_root}/.venv/bin/python" -m pytest -q \
  "${runtime_root}/tests/test_strength_mapping.py" \
  "${runtime_root}/tests/test_fate_core_cli.py"

if [[ "${skip_delivery}" == "1" ]]; then
  echo "[acceptance] skip delivery: 用户显式要求跳过"
else
  echo "[acceptance] delivery smoke (${delivery_target})"
  bash "${script_dir}/delivery-smoke.sh" \
    --target "${delivery_target}" \
    --response-file "${output_dir}/delivery-${delivery_target}.json"
fi

echo "[acceptance] done: ${output_dir}"
