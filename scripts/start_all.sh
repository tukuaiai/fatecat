#!/usr/bin/env bash
# 一键启动 Fate-Engine Telegram 全量服务（含清理旧进程）
# - 杀掉遗留 bot/api 进程
# - 预加载外部 .env
# - 后台启动 bot（含 API，如需单 bot 请改为 start.py bot）

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$ROOT/assets/config/.env}"
SERVICE_DIR="$ROOT/modules/telegram"
LOG_DIR="$SERVICE_DIR/output/logs"

echo "==> 切换到项目根目录: $ROOT"
cd "$ROOT"

if [[ -f "$ENV_FILE" ]]; then
  echo "==> 载入外部环境变量: $ENV_FILE"
  set -a
  # shellcheck source=/dev/null
  source "$ENV_FILE"
  set +a
else
  echo "⚠️  未找到 $ENV_FILE，确保 FATE_BOT_TOKEN 已在环境中"
fi

echo "==> 清理遗留进程..."
PIDS=$({
  pgrep -f "$SERVICE_DIR/src/bot.py" || true
  pgrep -f "$SERVICE_DIR/src/main.py" || true
  # start.py 是调度父进程（start.py both），需一并清理避免多实例并存
  pgrep -f "start.py both" || true
} | sort -u | tr '\n' ' ')
if [[ -n "$PIDS" ]]; then
  echo "$PIDS" | xargs -r kill
  sleep 1
  # 如有顽固进程，再强杀
  REMAIN=$({
    pgrep -f "$SERVICE_DIR/src/bot.py" || true
    pgrep -f "$SERVICE_DIR/src/main.py" || true
    pgrep -f "start.py both" || true
  } | sort -u | tr '\n' ' ')
  if [[ -n "$REMAIN" ]]; then
    echo "$REMAIN" | xargs -r kill -9
  fi
else
  echo "无遗留进程。"
fi

echo "==> 准备日志目录: $LOG_DIR"
mkdir -p "$LOG_DIR"

PY_BIN="$ROOT/.venv/bin/python"
if [[ ! -x "$PY_BIN" ]]; then
  PY_BIN="$(command -v python3)"
fi

echo "==> 后台启动 Bot + API（start.py both）..."
cd "$SERVICE_DIR"
nohup "$PY_BIN" start.py both > "$LOG_DIR/nohup.out" 2>&1 &
BOT_PID=$!
echo "$BOT_PID" > "$LOG_DIR/bot.pid"

echo "✅ 启动完成，PID: $BOT_PID"
echo "日志: tail -f $LOG_DIR/bot.log"
echo "nohup: tail -f $LOG_DIR/nohup.out"
