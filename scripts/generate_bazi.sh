#!/bin/bash
# 八字排盘输出脚本
# 用法: ./generate_bazi.sh "2004-02-21" "19:30" "male" "辽宁省大连市" 121.6 "张三"

# 参数
BIRTH_DATE="${1:-2004-02-21}"
BIRTH_TIME="${2:-19:30}"
GENDER="${3:-male}"
BIRTH_PLACE="${4:-北京}"
LONGITUDE="${5:-116.4}"
NAME="${6:-}"

# 输出文件名
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_BASE="output_${TIMESTAMP}"

# 项目路径
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_DIR="${PROJECT_DIR}/modules/telegram/src"
OUTPUT_DIR="${PROJECT_DIR}/modules/telegram/output"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 激活虚拟环境并执行
cd "$SERVICE_DIR"
source "${PROJECT_DIR}/.venv/bin/activate"

python3 << EOF
from datetime import datetime
from bazi_calculator import BaziCalculator
from output_formatter import save_both

# 解析参数
birth_dt = datetime.strptime("${BIRTH_DATE} ${BIRTH_TIME}", "%Y-%m-%d %H:%M")

calc = BaziCalculator(
    birth_dt=birth_dt,
    gender="${GENDER}",
    longitude=${LONGITUDE},
    name="${NAME}",
    birth_place="${BIRTH_PLACE}"
)

result = calc.calculate()
json_path, jsonl_path = save_both(result, "${OUTPUT_DIR}/${OUTPUT_BASE}")

print(f"JSON:  {json_path}")
print(f"JSONL: {jsonl_path}")
EOF

echo ""
echo "完成！"
