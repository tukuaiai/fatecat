"""
fate-service 路径管理模块
统一管理所有路径，避免硬编码绝对路径
"""
from pathlib import Path
import os

# 服务根目录: services/telegram
SERVICE_ROOT = Path(__file__).resolve().parent.parent

# fate-service 仓库根目录
FATE_SERVICE_ROOT = SERVICE_ROOT.parent.parent

# 新核心模块路径
FATE_CORE_ROOT = FATE_SERVICE_ROOT / "services" / "fate_core"
FATE_CORE_SRC_DIR = FATE_CORE_ROOT / "src"

# tradecat 项目根目录
PROJECT_ROOT = FATE_SERVICE_ROOT.parent.parent

# 配置文件路径 (统一使用 tradecat/assets/config/.env)
CONFIG_DIR = PROJECT_ROOT / "assets" / "config"
ENV_FILE = CONFIG_DIR / ".env"

# fate-service 内部路径
LIBS_DIR = FATE_SERVICE_ROOT / "libs"
EXTERNAL_LIBS_DIR = LIBS_DIR / "external" / "github"
DATA_DIR = LIBS_DIR / "data"
DATABASE_DIR = LIBS_DIR / "database"

# 外部库路径
LUNAR_PYTHON_DIR = EXTERNAL_LIBS_DIR / "lunar-python-master"
BAZI_1_DIR = EXTERNAL_LIBS_DIR / "bazi-1-master"
SXWNL_DIR = EXTERNAL_LIBS_DIR / "sxwnl-master"
IZTRO_DIR = EXTERNAL_LIBS_DIR / "iztro-main"
FORTEL_ZIWEI_DIR = EXTERNAL_LIBS_DIR / "fortel-ziweidoushu-main"
MIKABOSHI_DIR = EXTERNAL_LIBS_DIR / "mikaboshi-main"
CHINESE_DIVINATION_DIR = EXTERNAL_LIBS_DIR / "Chinese-Divination-master"
ICHING_DIR = EXTERNAL_LIBS_DIR / "Iching-master"
HOLIDAY_CALENDAR_DIR = EXTERNAL_LIBS_DIR / "holiday-and-chinese-almanac-calendar-main"
CHINESE_CALENDAR_DIR = EXTERNAL_LIBS_DIR / "chinese-calendar-master"
JS_ASTRO_DIR = EXTERNAL_LIBS_DIR / "js_astro-master"
DANTALION_DIR = EXTERNAL_LIBS_DIR / "dantalion-master"

# 服务内部路径
SRC_DIR = SERVICE_ROOT / "src"
SCRIPTS_DIR = SERVICE_ROOT / "scripts"
OUTPUT_DIR = SERVICE_ROOT / "output"
LOGS_DIR = OUTPUT_DIR / "logs"
TXT_DIR = OUTPUT_DIR / "txt"
QUEUE_DIR = OUTPUT_DIR / "queue"

# 数据库路径
BAZI_DB_DIR = DATABASE_DIR / "bazi"
BAZI_DB_PATH = BAZI_DB_DIR / "bazi.db"

# 数据文件
CHINA_COORDS_CSV = DATA_DIR / "china_coordinates.csv"

# 脚本路径
TRUE_SOLAR_TIME_JS = SCRIPTS_DIR / "true_solar_time.js"
SXWNL_INTERFACE_JS = SXWNL_DIR / "sxwnl_interface.js"
DANTALION_BRIDGE_JS = SCRIPTS_DIR / "dantalion_bridge.js"

# prompts 目录
PROMPTS_DIR = SRC_DIR / "prompts"


def ensure_dirs():
    """确保必要目录存在"""
    for d in [LOGS_DIR, TXT_DIR, QUEUE_DIR, BAZI_DB_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def get_env_file() -> Path:
    """获取环境变量文件路径，统一使用 tradecat/assets/config/.env"""
    if not ENV_FILE.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {ENV_FILE}\n请复制 assets/config/.env.example 为 assets/config/.env 并填写配置"
        )
    return ENV_FILE


def check_dependencies() -> dict:
    """检查所有依赖是否就绪，返回检查结果"""
    results = {"ok": True, "errors": [], "warnings": []}
    
    # 必须存在的目录/文件
    required = [
        (ENV_FILE, "配置文件"),
        (LUNAR_PYTHON_DIR, "lunar-python 库"),
        (BAZI_1_DIR, "bazi-1 库"),
        (SXWNL_DIR, "sxwnl 库"),
        (CHINA_COORDS_CSV, "城市坐标数据"),
    ]
    
    # 可选的外部库
    optional = [
        (FORTEL_ZIWEI_DIR, "fortel-ziweidoushu 库（紫微斗数）"),
        (DANTALION_DIR, "dantalion 库（现代八字）"),
        (IZTRO_DIR, "iztro 库（紫微斗数）"),
        (MIKABOSHI_DIR, "mikaboshi 库（风水罗盘）"),
        (CHINESE_DIVINATION_DIR, "Chinese-Divination 库（六爻梅花）"),
        (ICHING_DIR, "Iching 库（易经）"),
        (HOLIDAY_CALENDAR_DIR, "holiday-calendar（黄历）"),
        (CHINESE_CALENDAR_DIR, "chinese-calendar（农历）"),
        (JS_ASTRO_DIR, "js_astro 库（天文）"),
    ]
    
    for path, name in required:
        if not path.exists():
            results["ok"] = False
            results["errors"].append(f"缺少必需依赖: {name} ({path})")
    
    for path, name in optional:
        if not path.exists():
            results["warnings"].append(f"缺少可选依赖: {name} ({path})")
    
    # 检查环境变量
    if ENV_FILE.exists():
        from dotenv import dotenv_values
        config = dotenv_values(ENV_FILE)
        if not config.get("FATE_BOT_TOKEN"):
            results["ok"] = False
            results["errors"].append("未配置 FATE_BOT_TOKEN")
    
    return results


def startup_check():
    """启动时执行完整检查"""
    print("[fate-service] 启动检查...")
    
    # 1. 确保目录存在
    ensure_dirs()
    print("  ✅ 目录结构已就绪")
    
    # 2. 检查依赖
    results = check_dependencies()
    
    for warn in results["warnings"]:
        print(f"  ⚠️  {warn}")
    
    if not results["ok"]:
        print("  ❌ 启动检查失败:")
        for err in results["errors"]:
            print(f"     - {err}")
        raise RuntimeError("依赖检查失败，请修复后重试")
    
    print("  ✅ 依赖检查通过")
    return True
