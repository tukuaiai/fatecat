#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROFILE="general"
WITH_DEV="0"
WRITE_ENV_IF_MISSING="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --with-dev)
      WITH_DEV="1"
      shift
      ;;
    --write-env-if-missing)
      WRITE_ENV_IF_MISSING="1"
      shift
      ;;
    *)
      echo "未知参数: $1" >&2
      exit 2
      ;;
  esac
done

if [[ "$PROFILE" != "general" && "$PROFILE" != "openclaw" && "$PROFILE" != "harness" ]]; then
  echo "不支持的 profile: $PROFILE" >&2
  exit 2
fi

cd "$ROOT"

echo "==> FateCat Agent 自举"
echo "profile: $PROFILE"

if [[ ! -d .venv ]]; then
  echo "==> 创建虚拟环境"
  python3 -m venv .venv
fi

echo "==> 升级 pip"
.venv/bin/pip install -q --upgrade pip

echo "==> 安装 FateCat"
if [[ "$WITH_DEV" == "1" ]]; then
  .venv/bin/pip install -q -e '.[dev]'
else
  .venv/bin/pip install -q -e .
fi

if [[ "$WRITE_ENV_IF_MISSING" == "1" && ! -f assets/config/.env ]]; then
  echo "==> 创建本地配置模板 assets/config/.env"
  cp assets/config/agent.env.example assets/config/.env
fi

echo "==> 纯分析依赖检查"
.venv/bin/fatecat health --mode pure --json

cat <<EOF

✅ Agent 自举完成

推荐下一步命令:
  纯分析:
    .venv/bin/fatecat pure-analysis --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市"}' --pretty

  启动 API:
    .venv/bin/fatecat serve api

  启动 Bot:
    .venv/bin/fatecat health --mode delivery --json
    .venv/bin/fatecat serve bot

当前 profile:
  $PROFILE
EOF
