#!/bin/bash
# FateCat 打包脚本 - 本地执行
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROJECT_NAME="$(basename "$ROOT")"
OUT="$ROOT/.dist/${PROJECT_NAME}-deploy"
ARCHIVE="$ROOT/.dist/${PROJECT_NAME}-deploy.tar.gz"

echo "==> 清理旧包"
rm -rf "$OUT" "$ARCHIVE"
mkdir -p "$(dirname "$OUT")"
mkdir -p "$OUT"

echo "==> 复制核心目录"
cp "$ROOT/README.md" "$OUT/"
cp "$ROOT/AGENTS.md" "$OUT/"
cp "$ROOT/Makefile" "$OUT/"
cp "$ROOT/pyproject.toml" "$OUT/"
cp "$ROOT/requirements-dev.txt" "$OUT/" 2>/dev/null || true
cp -r "$ROOT/modules" "$OUT/"
cp -r "$ROOT/scripts" "$OUT/"
cp -r "$ROOT/assets" "$OUT/"
mkdir -p "$OUT/runtime/database/bazi"

echo "==> 清理运行时垃圾"
find "$OUT" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
find "$OUT" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$OUT" -name "*.pyc" -delete 2>/dev/null || true
find "$OUT" -name "*.db" -delete 2>/dev/null || true

echo "==> 生成部署脚本"
cat > "$OUT/install.sh" << 'EOF'
#!/bin/bash
set -euo pipefail

DEPLOY_DIR="$HOME/.projects/fatecat"
CONFIG_ENV="$DEPLOY_DIR/assets/config/.env"
ENV_EXAMPLE="$DEPLOY_DIR/assets/config/.env.example"
SERVICE_NAME="fatecat-telegram"

echo "==> 安装系统依赖"
sudo apt update
sudo apt install -y python3-venv python3-pip nodejs npm

echo "==> 创建部署目录"
mkdir -p "$DEPLOY_DIR"
cp -r ./* "$DEPLOY_DIR/"

echo "==> 创建 Python 虚拟环境"
cd "$DEPLOY_DIR"
python3 -m venv .venv
"$DEPLOY_DIR/.venv/bin/pip" install --upgrade pip
"$DEPLOY_DIR/.venv/bin/pip" install -r modules/telegram/requirements.txt

echo "==> 构建 Node.js 依赖"
cd "$DEPLOY_DIR/assets/vendor/github/dantalion-master/packages/dantalion-core" 2>/dev/null && npm install && npm run build || echo "dantalion 跳过"
cd "$DEPLOY_DIR/assets/vendor/github/iztro-main" 2>/dev/null && npm install || echo "iztro 跳过"

echo "==> 初始化配置文件"
mkdir -p "$DEPLOY_DIR/assets/config"
if [ ! -f "$CONFIG_ENV" ] && [ -f "$ENV_EXAMPLE" ]; then
  cp "$ENV_EXAMPLE" "$CONFIG_ENV"
fi
if [ ! -f "$CONFIG_ENV" ]; then
  echo "FATE_BOT_TOKEN=你的token" > "$CONFIG_ENV"
fi

echo "==> 安装 systemd 服务"
sudo tee "/etc/systemd/system/${SERVICE_NAME}.service" > /dev/null << SYSTEMD
[Unit]
Description=FateCat Telegram Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$DEPLOY_DIR/modules/telegram
Environment="PATH=$DEPLOY_DIR/.venv/bin:/usr/bin"
EnvironmentFile=-$CONFIG_ENV
ExecStart=$DEPLOY_DIR/.venv/bin/python start.py bot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SYSTEMD

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"

echo ""
echo "✅ 部署完成"
echo "1. 编辑配置: nano $CONFIG_ENV"
echo "2. 启动服务: sudo systemctl start $SERVICE_NAME"
echo "3. 查看状态: sudo systemctl status $SERVICE_NAME"
echo "4. 查看日志: journalctl -u $SERVICE_NAME -f"
EOF
chmod +x "$OUT/install.sh"

echo "==> 打包"
cd "$(dirname "$OUT")"
tar -czvf "$ARCHIVE" "$(basename "$OUT")"

echo ""
echo "✅ 打包完成"
ls -lh "$ARCHIVE"
echo ""
echo "上传到服务器后执行："
echo "  tar -xzvf ${PROJECT_NAME}-deploy.tar.gz"
echo "  cd ${PROJECT_NAME}-deploy && ./install.sh"
