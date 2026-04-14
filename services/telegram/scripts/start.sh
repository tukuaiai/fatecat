#!/usr/bin/env bash
# fate-service/telegram 标准化启动脚本
# 用法: ./scripts/start.sh [start|stop|status|restart]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_DIR="$(dirname "$SCRIPT_DIR")"
FATE_SERVICE_ROOT="$(dirname "$(dirname "$SERVICE_DIR")")"
PROJECT_ROOT="$(dirname "$(dirname "$FATE_SERVICE_ROOT")")"

# 配置文件路径（统一使用 tradecat/assets/config/.env）
CONFIG_ENV="$PROJECT_ROOT/assets/config/.env"
LEGACY_ENV="$HOME/.projects/fate-engine-env/.env"

LOG_DIR="$SERVICE_DIR/output/logs"
PID_FILE="$LOG_DIR/bot.pid"

# 安全加载 .env（禁止 source 执行文件内容）
RUNTIME_HELPERS="$PROJECT_ROOT/scripts/alternative/runtime_helpers.sh"
if [[ -f "$RUNTIME_HELPERS" ]]; then
  # shellcheck disable=SC1091
  source "$RUNTIME_HELPERS"
else
  safe_load_env_file() {
    local file="$1"
    [[ -f "$file" ]] || return 0
    while IFS= read -r line || [[ -n "$line" ]]; do
      [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
      local key=""
      local value=""
      if [[ "$line" =~ ^[[:space:]]*export[[:space:]]+([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
        key="${BASH_REMATCH[1]}"
        value="${BASH_REMATCH[2]}"
      elif [[ "$line" =~ ^[[:space:]]*([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
        key="${BASH_REMATCH[1]}"
        value="${BASH_REMATCH[2]}"
      else
        continue
      fi
      value="${value%$'\r'}"
      if [[ "$value" =~ ^\".*\"$ ]] || [[ "$value" =~ ^\'.*\'$ ]]; then
        value="${value:1:${#value}-2}"
      fi
      export "$key=$value"
    done < "$file"
  }
fi

# 加载环境变量
load_env() {
  if [[ -f "$CONFIG_ENV" ]]; then
    echo "==> 加载配置: $CONFIG_ENV"
    safe_load_env_file "$CONFIG_ENV"
  elif [[ -f "$LEGACY_ENV" ]]; then
    echo "==> 加载旧配置: $LEGACY_ENV"
    safe_load_env_file "$LEGACY_ENV"
  else
    echo "⚠️  未找到配置文件，确保 FATE_BOT_TOKEN 已在环境中"
  fi
}

# 获取 Python 解释器
get_python() {
  if [[ -x "$SERVICE_DIR/.venv/bin/python" ]]; then
    echo "$SERVICE_DIR/.venv/bin/python"
  elif [[ -x "$FATE_SERVICE_ROOT/.venv/bin/python" ]]; then
    echo "$FATE_SERVICE_ROOT/.venv/bin/python"
  else
    command -v python3
  fi
}

start() {
  load_env
  mkdir -p "$LOG_DIR"
  
  if [[ -f "$PID_FILE" ]]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
      echo "服务已在运行 (PID: $OLD_PID)"
      return 0
    fi
  fi
  
  PY_BIN=$(get_python)
  echo "==> 启动 fate-service Bot..."
  cd "$SERVICE_DIR"
  # 使用 setsid + exec 让 Bot 脱离当前会话，避免在非交互环境中被回收
  setsid bash -c "exec \"$PY_BIN\" start.py bot" > "$LOG_DIR/nohup.out" 2>&1 < /dev/null &
  BOT_PID=$!
  echo "$BOT_PID" > "$PID_FILE"
  
  echo "✅ 启动完成 (PID: $BOT_PID)"
  echo "日志: tail -f $LOG_DIR/bot.log"
}

stop() {
  if [[ -f "$PID_FILE" ]]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
      echo "==> 停止服务 (PID: $PID)..."
      kill "$PID"
      sleep 2
      if kill -0 "$PID" 2>/dev/null; then
        kill -9 "$PID"
      fi
      rm -f "$PID_FILE"
      echo "✅ 服务已停止"
    else
      echo "服务未运行"
      rm -f "$PID_FILE"
    fi
  else
    echo "服务未运行"
  fi
}

status() {
  if [[ -f "$PID_FILE" ]]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
      echo "✅ 服务运行中 (PID: $PID)"
      return 0
    fi
  fi
  echo "❌ 服务未运行"
  return 1
}

case "${1:-status}" in
  start)   start ;;
  stop)    stop ;;
  status)  status ;;
  restart) stop; sleep 1; start ;;
  *)
    echo "用法: $0 {start|stop|status|restart}"
    exit 1
    ;;
esac
