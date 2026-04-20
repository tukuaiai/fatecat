# AGENTS.md - FateCat Skill Repo

## 目录用途

当前根目录就是单 skill 仓库根：对外暴露标准 skill 入口，对内托管 FateCat 项目源码。

## 目录结构

```text
fatecat/
├── AGENTS.md
├── README.md
├── SKILL.md
├── references/
├── scripts/
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
- `references/`：长文档、输入输出契约、迁移与排障材料。
- `scripts/`：skill 包装脚本与导出脚本。
- `project/`：FateCat 项目的真实源码根、运行时骨架与项目文档真相源。

## 依赖方向

- `README.md -> SKILL.md + references/*`
- `scripts/* -> project/*`
- 禁止在根目录重新散落与 `project/` 平行的第二套业务源码目录
