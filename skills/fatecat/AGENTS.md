# AGENTS.md - skills/fatecat

## 目录用途

`skills/fatecat/` 是 FateCat 的 skill 封装包：对上暴露 Agent 友好的使用入口，对下复用仓库现有 CLI / API / Bot / 资产体系。

## 目录结构

```text
skills/fatecat/
├── AGENTS.md
├── SKILL.md
├── assets/
│   ├── env/
│   └── request-examples/
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
    ├── sync-runtime.sh
    └── export-runtime.sh
```

## 职责边界

- `SKILL.md`：只给操作手册，不承载大段背景资料。
- `assets/`：只放 skill 自己的模板与示例；不放真实敏感配置。
- `references/`：解释架构、命令、迁移与排障；引用仓库真相源，不复制 vendor 文档。
- `scripts/`：包装 FateCat CLI，并维护嵌入式 `fatecat_runtime/` 镜像；导出脚本负责生成独立 bundle。
- `scripts/fatecat_runtime/`：当前仓库的运行时镜像，用于让 skill 本身可以脱离仓库根结构独立收口。

## 依赖方向

- `SKILL.md -> references/* + scripts/*`
- `scripts/* -> repo root or embedded/exported scripts/fatecat_runtime`
- 禁止把 `assets/config/.env`、真实 `.db`、`.venv/` 打进 skill 资产
