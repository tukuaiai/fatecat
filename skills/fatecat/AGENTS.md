# AGENTS.md - skills/fatecat

## 目录用途

`skills/fatecat/` 是 FateCat 的 skill 封装包：对上暴露 Agent 友好的使用入口，对下复用仓库现有 CLI / API / Bot / 资产体系。

## 目录结构

```text
skills/fatecat/
├── AGENTS.md
├── SKILL.md
├── references/
│   ├── index.md
│   ├── architecture.md
│   ├── commands.md
│   ├── io-contract.md
│   ├── migration-plan.md
│   └── troubleshooting.md
└── scripts/
    ├── common.sh
    ├── bootstrap.sh
    ├── health.sh
    ├── pure-analysis.sh
    ├── serve-api.sh
    ├── serve-bot.sh
    ├── export-runtime.sh
    └── fatecat_runtime/
```

## 职责边界

- `SKILL.md`：只给操作手册，不承载大段背景资料。
- `references/`：解释架构、命令、迁移与排障；引用仓库真相源，不复制 vendor 文档。
- `scripts/`：包装 FateCat CLI，并负责把当前 skill 导出成独立 bundle。
- `scripts/fatecat_runtime/`：当前 FateCat 项目的真实源码与运行时骨架；所有包装脚本都从这里起跳。

## 依赖方向

- `SKILL.md -> references/* + scripts/*`
- `scripts/* -> embedded/exported scripts/fatecat_runtime`
- 禁止把真实 `assets/config/.env`、真实 `.db`、`.venv/` 打进导出产物
