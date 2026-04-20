# AGENTS.md - Skill Assets

## 目录用途

根级 `assets/` 只承载 skill 治理资产，不承载 FateCat 业务源码。

## 目录结构

```text
assets/
└── lifecycle/
    ├── AGENTS.md
    ├── README.md
    ├── packs/
    └── templates/
```

## 职责边界

- `lifecycle/templates/`：全生命周期阶段模板。
- `lifecycle/packs/`：按任务、版本或发布周期沉淀的生命周期包。
- 禁止把 `project/` 下的业务代码复制到这里形成第二真相源。
