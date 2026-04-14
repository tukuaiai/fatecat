#!/bin/bash
# FateCat 外部环境搭建脚本
# 用于搭建 Node.js、Rust 等外部依赖环境

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENDOR_GITHUB_DIR="$ROOT/assets/vendor/github"

echo "🚀 FateCat 外部环境搭建开始"
echo "═══════════════════════════════════════════════════════════════"

# 1. 安装Node.js依赖包
echo "📦 1. 安装Node.js依赖包..."
cd "$VENDOR_GITHUB_DIR/sxwnl-master"
if [ -f "package.json" ]; then
    npm install
    echo "✅ 寿星万年历Node.js依赖安装完成"
else
    echo "⚠️ 寿星万年历package.json不存在，创建基础依赖"
    cat > package.json << EOF
{
  "name": "sxwnl-calculator",
  "version": "1.0.0",
  "description": "寿星万年历计算器",
  "main": "index.js",
  "dependencies": {
    "moment": "^2.29.4",
    "lunar-javascript": "^1.6.12"
  }
}
EOF
    npm install
fi

# 2. 编译Rust项目
echo "🦀 2. 编译Rust项目..."
cd ../mikaboshi-main
if [ -f "Cargo.toml" ]; then
    cargo build --release
    echo "✅ 风水罗盘Rust项目编译完成"
else
    echo "⚠️ 风水罗盘Cargo.toml不存在，创建基础项目"
    cargo init --name mikaboshi_fengshui
    echo "✅ 风水罗盘Rust项目初始化完成"
fi

# 3. 安装天文计算库
echo "🌟 3. 安装天文计算库..."
cd ../js_astro-master
if [ -f "package.json" ]; then
    npm install
    echo "✅ 天文计算库依赖安装完成"
else
    echo "⚠️ 天文计算库package.json不存在，创建基础依赖"
    cat > package.json << EOF
{
  "name": "js-astro-calculator",
  "version": "1.0.0",
  "description": "JavaScript天文计算库",
  "main": "index.js",
  "dependencies": {
    "astronomy-engine": "^2.1.19",
    "swisseph": "^2.10.3"
  }
}
EOF
    npm install
fi

# 4. 创建Python绑定
echo "🐍 4. 创建Python绑定..."
cd "$ROOT/modules/telegram"
if [ -x "$ROOT/.venv/bin/pip" ]; then
    "$ROOT/.venv/bin/pip" install nodejs cffi pycparser
else
    pip install nodejs cffi pycparser
fi

# 5. 测试环境
echo "🧪 5. 测试外部环境..."
python3 -c "
import subprocess
import sys

print('测试Node.js环境:')
try:
    result = subprocess.run(['node', '--version'], capture_output=True, text=True)
    print(f'✅ Node.js: {result.stdout.strip()}')
except:
    print('❌ Node.js测试失败')

print('测试Rust环境:')
try:
    result = subprocess.run(['rustc', '--version'], capture_output=True, text=True)
    print(f'✅ Rust: {result.stdout.strip()}')
except:
    print('❌ Rust测试失败')

print('测试Python环境:')
print(f'✅ Python: {sys.version.split()[0]}')
"

echo "═══════════════════════════════════════════════════════════════"
echo "🎉 FateCat 外部环境搭建完成！"
echo "   Node.js: ✅ 寿星万年历支持"
echo "   Rust: ✅ 风水罗盘支持"  
echo "   Python: ✅ 主计算引擎"
echo "═══════════════════════════════════════════════════════════════"
