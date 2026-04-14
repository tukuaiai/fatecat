# FateCat

> 命理胶水层仓库：外部成熟命理库 + 纯分析内核 + Telegram / API 交付层

## 赞助商

- `交易猫 TradeCat`
  - 本项目由交易猫赞助与支持。
  - CA：`0x8a99b8d53eff6bc331af529af74ad267f3167777`

## 项目定位

FateCat 不再沿用旧的 `libs/ + docs/ + deploy/` 平铺结构。

当前仓库按职责拆成三层：

- `assets/`：静态资产与配置真相源
- `runtime/`：运行期状态与数据库文件
- `services/`：纯分析内核与交付服务代码

核心设计原则：

1. 外部成熟仓库只做只读依赖，不在本仓库重写底层算法。
2. 纯命理分析优先沉淀到 `services/fate_core/`。
3. Telegram / FastAPI 只负责交付、编排和适配。
4. 配置、数据、schema、文档统一归入 `assets/`。
5. SQLite 实库、日志、队列等运行态内容统一归入 `runtime/` 或服务输出目录。

## 当前目录结构

```text
fatecat/
├── Makefile
├── pyproject.toml
├── assets/
│   ├── config/          # 环境变量模板与配置文件
│   ├── data/            # 静态数据，如城市坐标
│   ├── database/        # 数据库 schema 等静态定义
│   ├── deploy/          # 打包与部署脚本
│   ├── docs/            # 项目文档与历史记录
│   ├── fate/            # 命理字段 profile 与配置真相源
│   └── vendor/          # 外部成熟仓库与网页资源，只读
├── runtime/
│   └── database/        # SQLite 实库与其他运行态数据
├── services/
│   ├── fate_core/       # 纯命理分析内核
│   └── telegram/        # Telegram Bot / FastAPI 交付层
├── scripts/             # 仓库级脚本
└── tests/               # 测试
```

目录重构说明见 `assets/docs/当前目录结构.md`。

## 快速开始

### 1. 环境要求

- Python 3.12+
- Node.js 18+

### 2. 安装依赖

```bash
python3 -m venv .venv
.venv/bin/pip install -r services/telegram/requirements.txt
```

或直接：

```bash
make install
```

### 3. 初始化配置

```bash
cp assets/config/.env.example assets/config/.env
vim assets/config/.env
```

最少需要：

```env
FATE_BOT_TOKEN=your_bot_token_here
FATE_ADMIN_USER_IDS=123456789
```

### 4. 启动服务

```bash
make start
make status
```

或直接：

```bash
cd services/telegram
../../.venv/bin/python start.py bot
```

## 关键目录说明

### `assets/`

- `assets/config/`：统一配置入口，只允许放模板与配置文件
- `assets/data/`：静态业务数据
- `assets/database/`：数据库 schema，不放运行态 `.db`
- `assets/deploy/`：部署与打包脚本
- `assets/docs/`：说明文档、记录、结构图
- `assets/fate/`：输出字段 profile，例如 `pure_analysis.json`
- `assets/vendor/`：外部仓库快照与网页资源，默认只读

### `runtime/`

- `runtime/database/`：SQLite 实库
- 只放运行态产物，不放 schema、文档、脚本

### `services/`

- `services/fate_core/`：纯命理分析用例、contracts、providers、adapters
- `services/telegram/`：Telegram Bot、FastAPI、报告生成、兼容旧能力

## 外部依赖

外部成熟仓库存放在 `assets/vendor/github/`。

必需依赖：

| 库名 | 目录 | 用途 |
|------|------|------|
| lunar-python | `assets/vendor/github/lunar-python-master` | 核心历法计算 |
| bazi-1 | `assets/vendor/github/bazi-1-master` | 八字神煞格局 |
| sxwnl | `assets/vendor/github/sxwnl-master` | 寿星万年历 |

可选依赖：

| 库名 | 目录 | 用途 |
|------|------|------|
| fortel-ziweidoushu | `assets/vendor/github/fortel-ziweidoushu-main` | 紫微斗数 |
| iztro | `assets/vendor/github/iztro-main` | 紫微斗数 |
| dantalion | `assets/vendor/github/dantalion-master` | 现代八字分析 |
| mikaboshi | `assets/vendor/github/mikaboshi-main` | 风水罗盘 |
| paipan | `assets/vendor/github/paipan-master` | 真太阳时 |

详细说明见 `assets/vendor/README.md`。

## 常用命令

```bash
make help
make install
make lint
make test
make start
make stop
make status
make restart
```

## 故障排查

### 配置缺失

```bash
grep FATE_BOT_TOKEN assets/config/.env
```

### 数据库检查

```bash
sqlite3 runtime/database/bazi/bazi.db ".tables"
```

### 查看日志

```bash
tail -f services/telegram/output/logs/bot.log
```

## 开发约束

- 不在仓库根目录或服务目录新增 `.env`
- 不修改 `assets/vendor/` 下外部仓库源码
- 不把运行态数据库重新放回 `assets/`
- 新增输出字段时，先改 `assets/fate/` 的 profile，再改 `services/fate_core/`

## 许可证

MIT
