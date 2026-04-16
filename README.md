# FateCat

<div align="center">

**专业命理排盘胶水层：外部成熟算法 × 纯命理分析内核 × Telegram / API / Agent 交付层**

<p>
  <a href="https://github.com/tukuaiai/fatecat"><img src="https://img.shields.io/github/stars/tukuaiai/fatecat?style=for-the-badge&label=Stars" alt="GitHub Stars"></a>
  <a href="https://github.com/tukuaiai/fatecat"><img src="https://img.shields.io/github/languages/top/tukuaiai/fatecat?style=for-the-badge&label=Top%20Language" alt="Top Language"></a>
  <a href="https://github.com/tukuaiai/fatecat"><img src="https://img.shields.io/github/languages/code-size/tukuaiai/fatecat?style=for-the-badge&label=Code%20Size" alt="Code Size"></a>
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/Delivery-Telegram%20%2F%20FastAPI-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram and FastAPI">
  <img src="https://img.shields.io/badge/Agent-OpenClaw%20%2F%20Harness-6C47FF?style=for-the-badge" alt="OpenClaw and Harness">
</p>

<p>
  <a href="#overview">项目概览</a> ·
  <a href="#capabilities">核心能力</a> ·
  <a href="#quick-start">快速开始</a> ·
  <a href="#cli">CLI 调用</a> ·
  <a href="#delivery">Telegram / API</a> ·
  <a href="#agent">Agent 一键部署</a> ·
  <a href="#layout">目录结构</a> ·
  <a href="#disclaimer">免责声明</a>
</p>

<p><strong>Star History</strong></p>

<p>
  <a href="https://star-history.com/#tukuaiai/fatecat&Date">
    <img src="https://api.star-history.com/svg?repos=tukuaiai/fatecat&type=Date" alt="FateCat Star History Chart">
  </a>
</p>

</div>

> [!WARNING]
> 本项目及AI分析结果仅供传统文化研究、算法测试与娱乐参考。命理学非精密科学，命运掌握在自己手中。使用者因轻信或误读本程序结果而产生的任何心理、财务及生活决策后果，本开源项目及开发者概不负责。

> `交易猫 TradeCat` 赞助与支持本项目。推荐工作流：先用交易猫完成专业排盘，再把结构化命盘交给 AI 深度分析，尽量减少模型乱编。
>
> - TradeCat Repo：`https://github.com/tukuaiai/tradecat`
> - FateCat Repo：`https://github.com/tukuaiai/fatecat`
> - CA：`0x8a99b8d53eff6bc331af529af74ad267f3167777`

<a id="overview"></a>

## 项目概览

FateCat 的目标不是重写所有命理底层算法，而是把已经成熟的外部仓库、统一字段配置、纯分析内核与交付层稳定地胶合在一起，让结构化排盘、命理分析、Telegram 交付、API 调用和 Agent 自动化部署都走一套一致入口。

它主要解决三类问题：

- 直接让 AI 排盘容易出现胡编乱造、字段漂移、上下文不稳定。
- 外部命理仓库分散，调用方式、依赖结构和输出格式各不一致。
- Telegram / API / Agent 场景需要一个可部署、可检查、可自动化的统一入口。

FateCat 当前明确采用“胶水层”定位：

- 外部成熟仓库放在 `assets/vendor/`，默认只读，不在本仓库里重写底层算法。
- 纯命理分析能力优先沉淀到 `modules/fate_core/`。
- Telegram / FastAPI 只负责交付、编排、适配与对外接口。
- 配置、数据、schema、文档、古籍语料统一收敛到 `assets/`。
- 数据库、队列、日志等运行态内容统一放到 `runtime/` 或模块输出目录。

<a id="capabilities"></a>

## 核心能力

### 1. 纯命理分析内核

- 通过 `modules/fate_core/` 提供稳定的纯分析入口。
- 输出字段由 `assets/fate/` 真相源控制，避免不同调用方式结果漂移。
- CLI 输出支持稳定 JSON，适合继续喂给 AI、脚本或上层服务。

### 2. 统一命令行入口

- 安装后统一使用 `.venv/bin/fatecat`。
- 支持 `pure-analysis`、`health`、`serve api`、`serve bot`。
- 适合本地命令行、脚本编排、批量处理和 Agent 调用。

### 3. Telegram / API 交付层

- `modules/telegram/` 负责 Telegram Bot、FastAPI、报告生成和兼容旧能力。
- 支持通过 `.env` 统一配置 Bot Token、代理、监听地址和端口。
- 支持结构化排盘结果继续交给 AI 做后续分析。

### 4. Agent 一键自举

- 提供 `general`、`openclaw`、`harness` 三种非交互自举入口。
- 自动创建 `.venv`、安装项目、生成本地配置模板、执行健康检查。
- 面向 OpenClaw / Harness / 其他非交互 Agent 做适配，便于自动部署。

### 5. 静态知识与古籍语料

- `assets/data/classics/` 已收敛命理古籍与基础知识语料，可用于后续检索、切片、RAG 或提示词构建。
- `assets/data/` 同时承载城市坐标等静态数据，不与运行态数据混放。

<a id="quick-start"></a>

## 快速开始

### 环境要求

- Python `3.12+`
- Node.js `18+`

### 推荐安装：一键自举

通用模式：

```bash
make bootstrap-agent
```

OpenClaw / Harness：

```bash
make bootstrap-openclaw
make bootstrap-harness
```

这套入口会调用 `assets/deploy/bootstrap_agent.sh`，自动完成：

- 创建虚拟环境
- 安装 FateCat
- 可选写入本地 `.env` 模板
- 执行纯分析健康检查

### 手动安装

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
```

或：

```bash
make install
```

安装完成后，统一入口为：

```bash
.venv/bin/fatecat
```

### 初始化配置

```bash
cp assets/config/.env.example assets/config/.env
vim assets/config/.env
```

如果只跑纯命理 CLI，不强制要求 `FATE_BOT_TOKEN`。
如果需要启动 Telegram Bot / 交付层，最少填写：

```env
FATE_BOT_TOKEN=your_bot_token_here
FATE_ADMIN_USER_IDS=123456789
FATE_BOT_PROXY_URL=http://127.0.0.1:7890
FATE_SERVICE_HOST=0.0.0.0
FATE_SERVICE_PORT=8001
```

### 代理配置

Telegram 出站代理统一使用：

```env
FATE_BOT_PROXY_URL=http://127.0.0.1:7890
```

支持：

- `http://`
- `https://`
- `socks5://`

常见本地代理写法：

- Clash / Mihomo HTTP：`http://127.0.0.1:7890`
- Clash / Mihomo SOCKS：`socks5://127.0.0.1:7891`

### 启动交付层

后台方式：

```bash
make start
make status
```

前台方式：

```bash
.venv/bin/fatecat serve api
.venv/bin/fatecat serve bot
```

<a id="cli"></a>

## CLI 调用

### 查看帮助

```bash
.venv/bin/fatecat --help
```

### 纯命理分析

```bash
.venv/bin/fatecat pure-analysis --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市"}' --pretty
```

也支持从 `stdin` 传入：

```bash
cat request.json | .venv/bin/fatecat pure-analysis --pretty
```

### 健康检查

```bash
.venv/bin/fatecat health --mode pure --json
.venv/bin/fatecat health --mode delivery --json
```

### 启动 API / Bot

```bash
.venv/bin/fatecat serve api
.venv/bin/fatecat serve bot
```

推荐姿势仍然不变：

- 先完成结构化排盘
- 再把稳定 JSON 结果交给 AI 分析
- 尽量避免让 AI 直接从自然语言“脑补排盘”

<a id="delivery"></a>

## Telegram / API

### Telegram Bot

- 配置入口：`assets/config/.env`
- 必需项：`FATE_BOT_TOKEN`
- 可选项：`FATE_ADMIN_USER_IDS`、`FATE_BOT_PROXY_URL`
- 日志目录：`modules/telegram/output/logs/`

常见命令：

```bash
.venv/bin/fatecat serve bot
tail -f modules/telegram/output/logs/bot.log
```

### FastAPI

- 地址配置：`FATE_SERVICE_HOST`、`FATE_SERVICE_PORT`
- 启动命令：

```bash
.venv/bin/fatecat serve api
```

### 统一配置原则

- 配置文件统一放在 `assets/config/`
- 不在仓库根目录或模块目录放 `.env`
- 不硬编码绝对路径
- 所有模块路径统一通过仓库内路径真相源管理

<a id="agent"></a>

## Agent 一键部署

FateCat 已提供面向 OpenClaw / Harness / 其他自动化系统的非交互自举入口：

```bash
make bootstrap-agent
make bootstrap-openclaw
make bootstrap-harness
```

底层脚本：

```bash
bash assets/deploy/bootstrap_agent.sh --profile general --write-env-if-missing
bash assets/deploy/bootstrap_agent.sh --profile openclaw --write-env-if-missing
bash assets/deploy/bootstrap_agent.sh --profile harness --write-env-if-missing
```

相关文件：

- 机器可读清单：`assets/deploy/agent_manifest.json`
- 部署说明：`assets/docs/Agent 一键部署.md`

Agent 场景推荐流程：

1. 先运行 `fatecat health --mode pure --json`
2. 再执行 `fatecat pure-analysis`
3. 最后把结构化结果交给上层 AI / Agent 做解释与扩展

<a id="layout"></a>

## 目录结构

```text
fatecat/
├── Makefile
├── pyproject.toml
├── assets/
│   ├── config/                 # 环境变量模板、运行配置、品牌真相源
│   ├── data/
│   │   ├── china_coordinates.csv
│   │   └── classics/           # 命理古籍与基础知识语料
│   ├── database/               # schema 等静态数据库定义
│   ├── deploy/                 # 打包、Agent 自举、部署清单
│   ├── docs/                   # 文档、结构说明、故障记录
│   ├── fate/                   # 命理字段 profile 真相源
│   └── vendor/                 # 外部成熟仓库与网页资源，只读
├── runtime/
│   └── database/               # SQLite 实库与其他运行态数据
├── modules/
│   ├── fate_core/              # 纯命理分析内核
│   └── telegram/               # Telegram Bot / FastAPI 交付层
├── scripts/                    # 仓库级脚本
└── tests/                      # 测试
```

目录重构与结构说明可继续查看：

- `assets/docs/当前目录结构.md`
- `AGENTS.md`

<details>
<summary><strong>查看外部依赖清单</strong></summary>

### 必需依赖

| 库名 | 目录 | 用途 |
|------|------|------|
| lunar-python | `assets/vendor/github/lunar-python-master` | 核心历法计算 |
| bazi-1 | `assets/vendor/github/bazi-1-master` | 八字神煞格局 |
| sxwnl | `assets/vendor/github/sxwnl-master` | 寿星万年历 |

### 可选依赖

| 库名 | 目录 | 用途 |
|------|------|------|
| fortel-ziweidoushu | `assets/vendor/github/fortel-ziweidoushu-main` | 紫微斗数 |
| iztro | `assets/vendor/github/iztro-main` | 紫微斗数 |
| dantalion | `assets/vendor/github/dantalion-master` | 现代八字分析 |
| mikaboshi | `assets/vendor/github/mikaboshi-main` | 风水罗盘 |
| paipan | `assets/vendor/github/paipan-master` | 真太阳时 |

详细说明见 `assets/vendor/README.md`。

</details>

## 常用命令

```bash
make help
make install
make install-dev
make lint
make test
make start
make stop
make status
make restart
make bootstrap-agent
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
tail -f modules/telegram/output/logs/bot.log
```

### 健康检查

```bash
.venv/bin/fatecat health --mode pure --json
.venv/bin/fatecat health --mode delivery --json
```

<a id="disclaimer"></a>

## 免责声明

- **核心免责声明**：本项目及AI分析结果仅供传统文化研究、算法测试与娱乐参考。命理学非精密科学，命运掌握在自己手中。使用者因轻信或误读本程序结果而产生的任何心理、财务及生活决策后果，本开源项目及开发者概不负责。
- 本项目用于传统命理资料整理、结构化排盘、AI 辅助分析与工程研究，不构成医疗、法律、金融、投资、心理咨询等专业建议。
- 命理本身带有解释性与非确定性，AI 分析也可能出现理解偏差、信息缺失与生成错误，输出结果不应被视为绝对事实或唯一决策依据。
- `assets/vendor/` 中的外部仓库、`assets/data/classics/` 中的古籍语料与 OCR 文本都可能存在错漏、版本差异、编码噪声与时代局限，请使用者自行校验。
- 请勿将本项目用于诈骗、诱导、精神操控、歧视、违法合规风险场景，或任何损害他人权益的用途。
- 因使用、误用或依赖本项目输出而造成的任何直接或间接后果，由使用者自行承担。

## 开发约束

- 不在仓库根目录或模块目录新增 `.env`
- 不修改 `assets/vendor/` 下外部仓库源码
- 不把运行态数据库重新放回 `assets/`
- 新增输出字段时，先改 `assets/fate/` 的 profile，再改 `modules/fate_core/`

## 交易猫生态

- `交易猫 TradeCat`：世界最强的专业命理排盘与 AI 命理分析基础设施
- `TradeCat Repo`：`https://github.com/tukuaiai/tradecat`
- `FateCat Repo`：`https://github.com/tukuaiai/fatecat`
- `CA`：`0x8a99b8d53eff6bc331af529af74ad267f3167777`

## 许可证

项目元数据当前声明为 `MIT`，见 `pyproject.toml`。
