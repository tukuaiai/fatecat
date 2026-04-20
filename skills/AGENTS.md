# AGENTS.md - skills

## 目录用途

`skills/` 是 FateCat 的 Agent 能力封装层：把仓库已有能力整理成可触发、可导航、可导出的 skill 包，而不是重写一份业务逻辑。

## 目录结构

```text
skills/
├── AGENTS.md
└── fatecat/
    ├── AGENTS.md
    ├── SKILL.md
    ├── references/
    └── scripts/
```

## 职责边界

- `skills/fatecat/SKILL.md`：skill 入口，只写触发条件、边界、Quick Reference、Examples。
- `skills/fatecat/references/`：承载长文档、迁移方案、输入输出契约、排障说明。
- `skills/fatecat/scripts/`：承载包装脚本与导出脚本；默认只调用同目录下的 `fatecat_runtime/`。
- `skills/fatecat/scripts/fatecat_runtime/`：当前 FateCat 项目的真实源码根。

## 依赖方向

- `skills/fatecat -> skills/fatecat/scripts/fatecat_runtime/*`
- `skills/fatecat/scripts/export-runtime.sh -> embedded runtime -> 独立 bundle`
- 禁止 `modules/*` 反向依赖 `skills/`
