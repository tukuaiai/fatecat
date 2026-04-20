#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

output_dir=""
bundle_mode="full"
expected_skill_dir_name="fatecat"

usage() {
  cat <<'EOF'
用法:
  bash scripts/export-runtime.sh --output <dir> [--mode full|lite]

说明:
  - full: 导出完整单-skill 仓库骨架，保留 lifecycle templates 与 packs
  - lite: 导出运行与交付必需骨架，排除根级 assets/lifecycle/packs 历史沉淀
  - 若后续要通过 strict skill 校验，导出目录 basename 应为 fatecat
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output)
      [[ $# -ge 2 ]] || usage_error "--output 缺少参数"
      output_dir="$2"
      shift 2
      ;;
    --mode)
      [[ $# -ge 2 ]] || usage_error "--mode 缺少参数"
      bundle_mode="$2"
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

if [[ -z "${output_dir}" ]]; then
  usage >&2
  exit 2
fi

case "${bundle_mode}" in
  full|lite)
    ;;
  *)
    usage_error "--mode 只支持 full 或 lite"
    ;;
esac

dest_root="$(mkdir -p "${output_dir}" && cd "${output_dir}" && pwd)"
case "${dest_root}" in
  "${skill_root}"|"${skill_root}/"* )
    usage_error "导出目录不能位于当前 skill 仓库内部，否则会形成递归复制"
    ;;
esac

dest_name="$(basename -- "${dest_root}")"

rsync_args=(
  -a
  --exclude '.git/'
  --exclude '.history/'
  --exclude 'project/.venv/'
  --exclude 'project/.pytest_cache/'
  --exclude 'project/.ruff_cache/'
  --exclude 'project/.mypy_cache/'
  --exclude 'project/assets/config/.env'
  --exclude 'project/runtime/**/*.db'
)

if [[ "${bundle_mode}" == "lite" ]]; then
  rsync_args+=(--exclude 'assets/lifecycle/packs/')
fi

rsync "${rsync_args[@]}" "${skill_root}/" "${dest_root}/"

mkdir -p "${dest_root}/project/runtime/database/bazi"
touch "${dest_root}/project/runtime/database/bazi/.gitkeep"

if [[ -f "${dest_root}/project/runtime/database/bazi/bazi.db" ]]; then
  rm -f "${dest_root}/project/runtime/database/bazi/bazi.db"
fi

echo "导出完成: ${dest_root} (mode=${bundle_mode})"

if [[ "${dest_name}" != "${expected_skill_dir_name}" ]]; then
  echo "提示：当前导出目录名为 ${dest_name}；若要通过 strict skill 校验，目录 basename 应为 ${expected_skill_dir_name}。" >&2
fi
