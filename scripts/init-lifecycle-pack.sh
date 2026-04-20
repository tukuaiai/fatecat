#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "${script_dir}/common.sh"

pack_name=""
output_dir=""

usage() {
  cat <<'EOF'
用法:
  bash scripts/init-lifecycle-pack.sh --name <slug> [--output <dir>]
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      [[ $# -ge 2 ]] || usage_error "--name 缺少参数"
      pack_name="$2"
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

if [[ -z "${pack_name}" ]]; then
  usage
  exit 2
fi

ensure_lifecycle_dirs
slug="$(normalize_slug "${pack_name}")"
if [[ -z "${slug}" ]]; then
  usage_error "生命周期包名称无效，请使用字母、数字、空格、点、下划线或横线"
fi

if [[ -z "${output_dir}" ]]; then
  pack_dir="${lifecycle_packs_dir}/$(date +%Y%m%d)-${slug}"
else
  pack_dir="$(mkdir -p "${output_dir}" && cd "${output_dir}" && pwd)"
fi

if [[ -e "${pack_dir}" ]] && find "${pack_dir}" -mindepth 1 -maxdepth 1 -print -quit | grep -q .; then
  usage_error "目标目录已存在且非空: ${pack_dir}"
fi

mkdir -p "${pack_dir}"
cp "${lifecycle_templates_dir}/"*.md "${pack_dir}/"

git_rev="$(git -C "${skill_root}" rev-parse --short HEAD 2>/dev/null || echo unknown)"

cat > "${pack_dir}/INDEX.md" <<EOF
# Lifecycle Pack

- 名称：${slug}
- 生成时间：$(date '+%Y-%m-%d %H:%M:%S %z')
- skill 根：${skill_root}
- project 根：${project_root}
- git 版本：${git_rev}

## 阶段顺序

1. \`00-context.md\`
2. \`01-requirements.md\`
3. \`02-prototype.md\`
4. \`03-iteration.md\`
5. \`04-mature-refactor.md\`
6. \`05-production-hardening.md\`
7. \`06-operations.md\`
8. \`07-retirement.md\`

## 使用约束

- 不把业务实现拷进这里。
- 这里只记录阶段决策、风险、验收和运维证据。
- 真正的业务改动仍然落在 \`${project_root}\`。
EOF

echo "生命周期包已初始化: ${pack_dir}"
