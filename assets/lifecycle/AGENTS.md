# AGENTS.md - Lifecycle Assets

## 目录用途

`lifecycle/` 是 FateCat skill 的阶段治理层，用来记录从需求到退役的连续证据。

## 目录结构

```text
lifecycle/
├── AGENTS.md
├── README.md
├── packs/
└── templates/
```

## 职责边界

- `templates/`：标准阶段模板，脚本据此初始化生命周期包。
- `packs/`：真实任务或版本的沉淀目录。
- `README.md`：解释生命周期资产怎么用。
