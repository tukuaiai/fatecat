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
    ├── assets/
    ├── references/
    └── scripts/
```

## 职责边界

- `skills/fatecat/SKILL.md`：skill 入口，只写触发条件、边界、Quick Reference、Examples。
- `skills/fatecat/references/`：承载长文档、迁移方案、输入输出契约、排障说明。
- `skills/fatecat/scripts/`：承载包装脚本与导出脚本；允许调用仓库根目录下现有 FateCat 代码。
- 禁止在 `skills/` 内复制一份会持续漂移的并行源码实现，除非是导出产物目录。

## 依赖方向

- `skills/fatecat -> modules/fate_core + modules/telegram + assets/*`
- `skills/fatecat/scripts/export-runtime.sh -> 仓库根目录源码 -> 独立 bundle`
- 禁止 `modules/*` 反向依赖 `skills/`
