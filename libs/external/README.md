# 外部依赖库

> fate-service 使用的外部命理库说明

## 目录结构

```
libs/external/
├── github/          # GitHub 开源库（本地克隆）
└── web/             # 网页资源
```

## 依赖库清单

### 必需依赖

| 库名 | 目录 | 语言 | 用途 | 来源 |
|------|------|------|------|------|
| lunar-python | `lunar-python-master` | Python | 核心历法计算 | https://github.com/6tail/lunar-python |
| bazi-1 | `bazi-1-master` | Python | 八字神煞格局 | https://github.com/bazi-1/bazi |
| sxwnl | `sxwnl-master` | JavaScript | 寿星万年历 | https://github.com/sxwnl/sxwnl |
| china_coordinates.csv | `../data/` | CSV | 城市坐标数据 | 自维护 |

### 扩展依赖

| 库名 | 目录 | 语言 | 用途 | 来源 |
|------|------|------|------|------|
| fortel-ziweidoushu | `fortel-ziweidoushu-main` | TypeScript | 紫微斗数 | https://github.com/fortelzhao/fortel-ziweidoushu |
| iztro | `iztro-main` | TypeScript | 紫微斗数 | https://github.com/SylarLong/iztro |
| dantalion | `dantalion-master` | TypeScript | 现代八字分析 | https://github.com/nicktaobo/dantalion |
| mikaboshi | `mikaboshi-main` | Rust | 风水罗盘 | https://github.com/nicktaobo/mikaboshi |
| Chinese-Divination | `Chinese-Divination-master` | Python | 六爻/梅花 | https://github.com/xxx/Chinese-Divination |
| Iching | `Iching-master` | Python | 易经系统 | https://github.com/xxx/Iching |
| holiday-calendar | `holiday-and-chinese-almanac-calendar-main` | ICS | 黄历数据 | https://github.com/nicktaobo/holiday-calendar |
| chinese-calendar | `chinese-calendar-master` | Python | 农历转换 | https://github.com/LKI/chinese-calendar |
| js_astro | `js_astro-master` | JavaScript | 天文计算 | https://github.com/nicktaobo/js_astro |

### 其他库（备用/参考）

共 53 个外部库，详见 `github/` 目录。

## 使用方式

### 路径引用

所有外部库通过 `_paths.py` 统一管理：

```python
from _paths import (
    LUNAR_PYTHON_DIR,      # lunar-python 路径
    BAZI_1_DIR,            # bazi-1 路径
    SXWNL_DIR,             # sxwnl 路径
    FORTEL_ZIWEI_DIR,      # fortel-ziweidoushu 路径
    DANTALION_DIR,         # dantalion 路径
    IZTRO_DIR,             # iztro 路径
    MIKABOSHI_DIR,         # mikaboshi 路径
    CHINESE_DIVINATION_DIR,# Chinese-Divination 路径
    ICHING_DIR,            # Iching 路径
    HOLIDAY_CALENDAR_DIR,  # holiday-calendar 路径
    CHINESE_CALENDAR_DIR,  # chinese-calendar 路径
    JS_ASTRO_DIR,          # js_astro 路径
)
```

### 动态导入示例

```python
import sys
from _paths import LUNAR_PYTHON_DIR

# 添加到 sys.path
sys.path.insert(0, str(LUNAR_PYTHON_DIR))

# 导入模块
from lunar import Lunar, Solar
```

### importlib 方式

```python
import importlib.util
from _paths import SRC_DIR

spec = importlib.util.spec_from_file_location(
    "module_name",
    str(SRC_DIR / "some_integration.py")
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
```

## 维护规则

1. **只读原则** - 禁止修改外部库代码
2. **版本锁定** - 使用固定版本快照
3. **路径统一** - 所有路径通过 `_paths.py` 管理
4. **集成封装** - 通过 `*_integration.py` 封装调用

## 安装/更新

### 手动克隆

```bash
cd libs/external/github

# 克隆必需库
git clone https://github.com/6tail/lunar-python.git lunar-python-master
git clone https://github.com/bazi-1/bazi.git bazi-1-master

# 克隆扩展库
git clone https://github.com/fortelzhao/fortel-ziweidoushu.git fortel-ziweidoushu-main
```

### Node.js 依赖

部分库需要 Node.js 环境：

```bash
# sxwnl
cd sxwnl-master && npm install

# fortel-ziweidoushu
cd fortel-ziweidoushu-main && npm install

# iztro
cd iztro-main && npm install

# dantalion
cd dantalion-master && npm install
```

### Rust 依赖

```bash
# mikaboshi（风水罗盘）
cd mikaboshi-main && cargo build --release
```

## 依赖检查

启动时自动检查依赖：

```python
from _paths import check_dependencies

results = check_dependencies()
# results["ok"] = True/False
# results["errors"] = [...]
# results["warnings"] = [...]
```

或手动检查：

```bash
cd plugins/first-party/fate/services/telegram/src
python -c "from _paths import check_dependencies; print(check_dependencies())"
```
