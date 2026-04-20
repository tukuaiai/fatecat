# AGENTS.md - FateCat Skill Repo

## 目录用途

当前根目录就是单 skill 仓库根：对外暴露标准 skill 入口，对内托管生命周期治理层与 FateCat 项目源码。

## 目录结构

```text
fatecat/
├── AGENTS.md
├── README.md
├── SKILL.md
├── assets/
│   ├── AGENTS.md
│   └── lifecycle/
│       ├── AGENTS.md
│       ├── README.md
│       ├── packs/
│       └── templates/
├── references/
│   └── execution-playbook.md
├── scripts/
│   └── preflight.sh
└── project/
    ├── AGENTS.md
    ├── pyproject.toml
    ├── assets/
    ├── modules/
    ├── runtime/
    ├── scripts/
    └── tests/
```

## 职责边界

- `SKILL.md`：标准 skill 入口说明。
- `assets/`：生命周期模板、治理资产与可沉淀的 agent 运维材料。
- `references/`：长文档、阶段门禁、输入输出契约、迁移与排障材料；其中 `execution-playbook.md` 是统一执行顺序真相源。
- `scripts/`：skill 包装脚本、生命周期脚手架与导出脚本；其中 `preflight.sh` 是默认预检入口。
- `project/`：FateCat 项目的真实源码根、运行时骨架与项目文档真相源。

## 依赖方向

- `README.md -> SKILL.md + assets/* + references/*`
- `assets/* -> scripts/* + references/*`
- `scripts/* -> project/*`
- `SKILL.md -> scripts/preflight.sh + references/execution-playbook.md`
- 禁止在根目录重新散落与 `project/` 平行的第二套业务源码目录
