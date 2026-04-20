# AGENTS.md - fatecat root

## 目录用途

当前根目录只是 skill 容器与版本根，不再承载 FateCat 业务源码。

## 目录结构

```text
fatecat/
├── AGENTS.md
├── README.md
└── skills/
    ├── AGENTS.md
    └── fatecat/
        ├── AGENTS.md
        ├── SKILL.md
        ├── references/
        └── scripts/
            ├── *.sh
            └── fatecat_runtime/
```

## 职责边界

- 根目录：只保留仓库说明、顶层导航与 Git 元数据。
- `skills/fatecat/`：FateCat skill 外壳。
- `skills/fatecat/scripts/fatecat_runtime/`：当前 FateCat 项目的真实源码根、运行时骨架与文档真相源。

## 依赖方向

- `README.md -> skills/fatecat/SKILL.md`
- `skills/fatecat/* -> skills/fatecat/scripts/fatecat_runtime/*`
- 禁止在根目录重新散落 `modules/`、`assets/`、`runtime/`、`tests/` 等并行源码目录
