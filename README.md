# Fate Service

> 专业级八字排盘服务 | TradeCat 微服务之一

## 项目简介

Fate Service 是 TradeCat 项目的命理服务模块，提供专业的八字排盘、紫微斗数、择日等功能。

## 快速开始

### 1. 环境要求

- Python 3.12+
- Node.js 18+ (寿星万年历支持)

### 2. 安装依赖

```bash
cd plugins/fate

# 创建虚拟环境并安装依赖
make install

# 或手动安装
python3 -m venv .venv
.venv/bin/pip install -r services/telegram/requirements.txt
```

### 3. 配置

fate-service 使用 TradeCat 统一配置文件 `assets/config/.env`：

```bash
# 复制配置模板（如果还没有）
cp assets/config/.env.example assets/config/.env

# 编辑配置，填入 fate-service 专用配置
vim assets/config/.env
```

需要配置的变量：

```env
# fate-service 配置（独立 Bot）
FATE_BOT_TOKEN=your_bot_token_here      # 从 @BotFather 获取
FATE_ADMIN_USER_IDS=123456789           # 管理员 Telegram ID
```

### 4. 启动服务

```bash
# 方式一：使用 Makefile（推荐）
make start          # 后台启动
make stop           # 停止服务
make status         # 查看状态
make run            # 前台运行（调试用）

# 方式二：使用启动脚本
./services/telegram/scripts/start.sh start

# 方式三：直接运行
cd services/telegram
.venv/bin/python start.py bot     # 启动 Telegram Bot
.venv/bin/python start.py api     # 启动 FastAPI 服务
.venv/bin/python start.py both    # 同时启动
```

### 5. 验证运行

```bash
# 查看状态
make status

# 查看日志
tail -f services/telegram/output/logs/bot.log
```

## 自动化特性

服务启动时会自动执行以下检查：

1. **目录检查** - 自动创建 logs、output、database 目录
2. **依赖检查** - 验证外部库和配置文件是否存在
3. **数据库初始化** - 自动创建数据库表（如不存在）
4. **配置验证** - 检查 FATE_BOT_TOKEN 是否配置

如果检查失败，服务会输出详细错误信息并拒绝启动。

## 项目结构

```
fate-service/
├── Makefile                    # 常用命令
├── .venv/                      # Python 虚拟环境
├── services/
│   └── telegram/       # Telegram Bot 服务
│       ├── src/
│       │   ├── bot.py          # Bot 主程序
│       │   ├── _paths.py       # 统一路径管理
│       │   ├── bazi_calculator.py  # 八字计算核心
│       │   ├── liuyao_factors/ # 六爻量化因子模块
│       │   └── ...
│       ├── output/
│       │   ├── logs/           # 日志目录
│       │   └── txt/            # 报告输出
│       ├── scripts/
│       │   └── start.sh        # 启动脚本
│       └── start.py            # 启动入口
├── libs/
│   ├── data/                   # 数据文件（城市坐标等）
│   ├── database/bazi/          # SQLite 数据库
│   └── external/               # 外部依赖（来自 GitHub 开源项目）
│       ├── github/             # GitHub 克隆的命理库
│       └── web/                # 网页资源
└── docs/                       # 文档
```

## 外部依赖库

本项目依赖多个 GitHub 开源命理库，已克隆到 `libs/external/github/` 目录：

### 必需依赖

| 库名 | GitHub 来源 | 用途 |
|------|-------------|------|
| lunar-python | [6tail/lunar-python](https://github.com/6tail/lunar-python) | 核心历法计算 |
| bazi-1 | [bazi-1/bazi](https://github.com/nicktaobo/bazi-1) | 八字神煞格局 |
| sxwnl | [sxwnl/sxwnl](https://github.com/nicktaobo/sxwnl) | 寿星万年历 |

### 可选依赖

| 库名 | GitHub 来源 | 用途 |
|------|-------------|------|
| fortel-ziweidoushu | [fortelzhao/fortel-ziweidoushu](https://github.com/nicktaobo/fortel-ziweidoushu) | 紫微斗数 |
| iztro | [SylarLong/iztro](https://github.com/SylarLong/iztro) | 紫微斗数 |
| dantalion | [nicktaobo/dantalion](https://github.com/nicktaobo/dantalion) | 现代八字分析 |
| mikaboshi | [nicktaobo/mikaboshi](https://github.com/nicktaobo/mikaboshi) | 风水罗盘 |
| Chinese-Divination | GitHub | 六爻/梅花易数 |
| Iching | GitHub | 易经系统 |

> 详细说明见 `libs/external/README.md`

## 常用命令

```bash
make help       # 查看所有命令
make install    # 安装依赖
make start      # 后台启动
make stop       # 停止服务
make status     # 查看状态
make restart    # 重启服务
make run        # 前台运行
make lint       # 代码检查
make test       # 运行测试
make clean      # 清理缓存
make reset      # 重建虚拟环境
```

## 功能特性

### 核心功能
- 八字排盘（四柱、藏干、十神、神煞、格局）
- 大运流年分析
- 真太阳时计算
- 地点模糊匹配（3199+ 城市）

### 扩展功能
- 紫微斗数
- 择日算法
- 合婚分析
- 姓名学

## 配置说明

所有配置集中在 `tradecat/assets/config/.env`：

| 变量 | 必填 | 说明 |
|------|------|------|
| `FATE_BOT_TOKEN` | ✅ | fate-service 专用 Bot Token |
| `FATE_ADMIN_USER_IDS` | ❌ | 管理员 ID（逗号分隔） |
| `FATE_SERVICE_HOST` | ❌ | API 服务地址（默认 0.0.0.0） |
| `FATE_SERVICE_PORT` | ❌ | API 服务端口（默认 8001） |

## 故障排查

### Bot 无响应

1. 检查配置：`grep FATE_BOT_TOKEN assets/config/.env`
2. 检查网络/代理
3. 确认只有一个 Bot 实例运行

### 排盘失败

1. 检查日志：`tail -f services/telegram/output/logs/bot.log`
2. 验证数据库：`sqlite3 libs/database/bazi/bazi.db ".tables"`

### 依赖缺失

```bash
# 重新安装依赖
make reset
make install
```

## 许可证

MIT License
