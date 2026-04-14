#!/bin/bash
# Fate-Engine 打包脚本 - 本地执行
set -e

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_NAME="$(basename "$ROOT")"
OUT="$ROOT/.dist/${PROJECT_NAME}-deploy"
ARCHIVE="$ROOT/.dist/${PROJECT_NAME}-deploy.tar.gz"

echo "==> 清理旧包"
rm -rf "$OUT" "$ARCHIVE"
mkdir -p "$(dirname "$OUT")"
mkdir -p "$OUT"

echo "==> 复制核心代码"
cp -r "$ROOT/services" "$OUT/"
cp -r "$ROOT/scripts" "$OUT/" 2>/dev/null || mkdir -p "$OUT/scripts"
mkdir -p "$OUT/libs"
cp -r "$ROOT/libs/data" "$OUT/libs/"
cp -r "$ROOT/libs/database" "$OUT/libs/"

echo "==> 复制必需外部库"
mkdir -p "$OUT/libs/external/github"
LIBS="lunar-python-master bazi-1-master paipan-master sxwnl-master iztro-main dantalion-master fortel-ziweidoushu-main Chinese-Divination-master Iching-master holiday-and-chinese-almanac-calendar-main mikaboshi-main js_astro-master bazi-name-master"
for lib in $LIBS; do
  [ -d "$ROOT/libs/external/github/$lib" ] && cp -r "$ROOT/libs/external/github/$lib" "$OUT/libs/external/github/"
done

echo "==> 清理 node_modules（服务器重装）"
find "$OUT" -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
find "$OUT" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$OUT" -name "*.pyc" -delete 2>/dev/null || true

echo "==> 生成部署脚本"
cat > "$OUT/install.sh" << 'EOF'
#!/bin/bash
# Fate-Engine 服务器一键部署
set -e

DEPLOY_DIR="$HOME/.projects/fate-engine"
ENV_DIR="$HOME/.projects/fate-engine-env"

echo "==> 安装系统依赖"
sudo apt update
sudo apt install -y python3-venv python3-pip nodejs npm

echo "==> 创建目录"
mkdir -p "$DEPLOY_DIR" "$ENV_DIR"
cp -r ./* "$DEPLOY_DIR/"

echo "==> 创建 Python 虚拟环境"
cd "$DEPLOY_DIR"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r services/telegram/requirements.txt

echo "==> 构建 Node.js 依赖"
cd "$DEPLOY_DIR/libs/external/github/dantalion-master/packages/dantalion-core" 2>/dev/null && npm install && npm run build || echo "dantalion 跳过"
cd "$DEPLOY_DIR/libs/external/github/iztro-main" 2>/dev/null && npm install || echo "iztro 跳过"

echo "==> 配置环境变量"
if [ ! -f "$ENV_DIR/.env" ]; then
  echo "FATE_BOT_TOKEN=你的token" > "$ENV_DIR/.env"
  echo "⚠️  请编辑 $ENV_DIR/.env 填入真实 FATE_BOT_TOKEN"
fi

echo "==> 安装 systemd 服务"
sudo tee /etc/systemd/system/fate-engine.service > /dev/null << SYSTEMD
[Unit]
Description=Fate-Engine Telegram Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$DEPLOY_DIR/services/telegram
Environment="PATH=$DEPLOY_DIR/.venv/bin:/usr/bin"
EnvironmentFile=$ENV_DIR/.env
ExecStart=$DEPLOY_DIR/.venv/bin/python start.py bot
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SYSTEMD

sudo systemctl daemon-reload
sudo systemctl enable fate-engine

echo ""
echo "✅ 部署完成！"
echo ""
echo "下一步："
echo "1. 编辑 Token: nano $ENV_DIR/.env"
echo "2. 启动服务: sudo systemctl start fate-engine"
echo "3. 查看状态: sudo systemctl status fate-engine"
echo "4. 查看日志: journalctl -u fate-engine -f"
EOF
chmod +x "$OUT/install.sh"

echo "==> 打包"
cd "$(dirname $OUT)"
tar -czvf "$ARCHIVE" "$(basename $OUT)"

echo ""
echo "✅ 打包完成！"
ls -lh "$ARCHIVE"
echo ""
echo "上传到服务器后执行："
echo "  tar -xzvf fate-engine-deploy.tar.gz"
echo "  cd fate-engine-deploy && ./install.sh"
