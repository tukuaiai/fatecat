#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

pack_dir=""
list_only="0"

usage() {
  cat <<'EOF'
用法:
  bash scripts/lifecycle-status.sh [--pack <dir>] [--list]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pack)
      [[ $# -ge 2 ]] || usage_error "--pack 缺少参数"
      pack_dir="$2"
      shift 2
      ;;
    --list)
      list_only="1"
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

if [[ "${list_only}" == "1" ]]; then
  if [[ ! -d "${lifecycle_packs_dir}" ]]; then
    echo "未发现生命周期包目录: ${lifecycle_packs_dir}"
    exit 0
  fi

  find "${lifecycle_packs_dir}" -mindepth 1 -maxdepth 1 -type d | sort
  exit 0
fi

if [[ -z "${pack_dir}" ]]; then
  pack_dir="$(latest_lifecycle_pack || true)"
fi

if [[ -z "${pack_dir}" ]]; then
  echo "未发现生命周期包，请先执行 bash scripts/init-lifecycle-pack.sh --name <slug>"
  exit 0
fi

stage_files=(
  "00-context.md"
  "01-requirements.md"
  "02-prototype.md"
  "03-iteration.md"
  "04-mature-refactor.md"
  "05-production-hardening.md"
  "06-operations.md"
  "07-retirement.md"
)

ready_count=0

echo "pack: ${pack_dir}"
printf '%-28s %s\n' "阶段文件" "状态"
printf '%-28s %s\n' "----------------------------" "--------"

for stage_file in "${stage_files[@]}"; do
  stage_path="${pack_dir}/${stage_file}"
  status="missing"

  if [[ -f "${stage_path}" ]]; then
    if grep -Eq '\[待补充\]|TODO|待补充' "${stage_path}"; then
      status="draft"
    else
      status="ready"
      ready_count=$((ready_count + 1))
    fi
  fi

  printf '%-28s %s\n' "${stage_file}" "${status}"
done

echo "summary: ${ready_count}/${#stage_files[@]} ready"
