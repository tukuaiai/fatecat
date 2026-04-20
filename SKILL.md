---
name: fatecat
description: "FateCat 命理分析交付 skill：封装 pure-analysis、health、serve api、serve bot 与独立导出流程。Use when 你要用 FateCat 做结构化命理分析、健康检查、Bot/API 交付，或把当前仓库导出为可分发 skill bundle。"
---

# fatecat Skill

用 FateCat 的单-skill仓库布局稳定执行结构化命理分析、交付层启动与 skill bundle 导出；不在 skill 层重写业务算法。

## When to Use This Skill

Trigger when any of these applies:
- 你要把出生时间、性别、经纬度等输入转换为 FateCat `pure-analysis` 结构化 JSON
- 你要先做 `health` 检查，再决定当前环境是否能跑纯分析或 Telegram / API 交付
- 你要启动 FateCat 的 FastAPI 或 Telegram Bot 入口
- 你要把当前 FateCat 仓库封装成可分发的独立 skill bundle
- 你要查询 FateCat 的输入输出契约、命令入口、迁移约束或排障手册

## Not For / Boundaries

- 这个 skill 不重写 `assets/vendor/` 下的成熟算法仓库，也不替代它们的原始文档。
- 当前仓库的 FateCat 源码真相源位于 `project/`；根目录只保留 skill 入口、文档与包装脚本。
- 这个 skill 不接受缺失核心输入的纯分析请求；最少需要 `birthDateTime`、`gender`、`longitude`、`latitude`。
- 这个 skill 不应把真实 `assets/config/.env`、真实运行态数据库或敏感凭据混入文档层或导出产物。

## Quick Reference

### 先安装当前仓库运行环境

```bash
bash scripts/bootstrap.sh
```

### 检查纯分析依赖

```bash
bash scripts/health.sh --mode pure --json
```

### 执行纯命理分析

```bash
bash scripts/pure-analysis.sh \
  --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市"}' \
  --pretty
```

### 启动 API

```bash
bash scripts/serve-api.sh
```

### 启动 Bot

```bash
bash scripts/serve-bot.sh
```

### 导出独立 skill runtime

```bash
bash scripts/export-runtime.sh --output /tmp/fatecat-skill-bundle
```

## Examples

### Example 1

- Input: 只需要给 AI / Agent 一份稳定的命理结构化 JSON
- Steps:
  1. 执行 `bash scripts/bootstrap.sh`
  2. 执行 `bash scripts/health.sh --mode pure --json`
  3. 执行 `bash scripts/pure-analysis.sh --input-json '...' --pretty`
- Expected output / acceptance:
  - 输出 JSON 顶层包含 `success`、`profile`、`data`、`branding`、`disclaimer`
  - `profile` 为 `pure_analysis`

### Example 2

- Input: 当前环境要暴露 HTTP 接口给上层工作流调用
- Steps:
  1. 准备 `project/assets/config/.env`
  2. 执行 `bash scripts/health.sh --mode delivery --json`
  3. 执行 `bash scripts/serve-api.sh`
- Expected output / acceptance:
  - FastAPI 进程启动成功
  - `/health` 可返回带 branding 的健康响应

### Example 3

- Input: 需要把当前 FateCat 仓库导出成可分发的 skill bundle
- Steps:
  1. 执行 `bash scripts/export-runtime.sh --output /tmp/fatecat-skill-bundle`
  2. 检查输出目录下是否存在 `SKILL.md`、`scripts/`、`project/`
  3. 在导出目录内继续执行 `bash scripts/bootstrap.sh`
- Expected output / acceptance:
  - 导出目录不包含 `.venv/`、`.git/`、真实 `.db`、真实 `.env`
  - 导出目录保留 `pyproject.toml`、`modules/`、`assets/`、`tests/` 等运行所需骨架

## References

- `references/index.md`: 导航索引
- `references/architecture.md`: skill 外壳与运行时边界
- `references/commands.md`: 常用命令入口
- `references/io-contract.md`: 输入输出契约
- `references/migration-plan.md`: 单-skill布局与 bundle 导出路线
- `references/troubleshooting.md`: 常见失败模式

## Maintenance

- Sources: `project/README.md`、`project/AGENTS.md`、`project/pyproject.toml`、`project/modules/fate_core/src/fate_core/cli.py`、`project/modules/telegram/src/main.py`、`project/assets/deploy/bootstrap_agent.sh`
- Verification path:
  - 命令帮助：`project/.venv/bin/fatecat --help`
  - 纯分析：`project/.venv/bin/fatecat pure-analysis --help`
  - 健康检查：`project/.venv/bin/fatecat health --help`
  - 交付层：`project/.venv/bin/fatecat serve --help`
  - skill 结构校验：`/home/lenovo/.codex/skills/auto-skill/scripts/validate-skill.sh . --strict`
- Last updated: 2026-04-20
- Known limits:
  - `project/` 现在就是 FateCat 源码真相源
  - 导出 bundle 会剥离 `.venv`、真实 `.env`、真实 `.db`，导出后仍需重新 bootstrap
  - `delivery` 模式仍然依赖完整配置与外部库
