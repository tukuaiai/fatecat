# FateCat Skill 架构说明

## 目标

把 FateCat 从“完整应用仓库”包成“可触发的 Agent skill”，同时保持现有 CLI / API / Bot 能力不漂移。

## 当前阶段设计

```text
fatecat/
├── SKILL.md                 # 触发入口
├── references/             # 长文档
├── scripts/                # 包装脚本与导出脚本
│   ├── *.sh                # 直接调用 FateCat CLI
│   └── export-runtime.sh   # 物化独立 single-skill bundle
└── project/                # FateCat 真实源码根
```

## 当前运行策略

- `project/` 已经承载 FateCat 的真实源码、运行时目录与项目元数据。
- 包装脚本只从 `project/` 解析 runtime root，不再在 `scripts/` 下嵌套源码。
- `bootstrap.sh` 负责在 `project/` 内补齐 `.venv`，导出脚本负责按同样边界生成可分发 bundle。

## 依赖边界

- 纯分析核心：`project/modules/fate_core/`
- 交付层：`project/modules/telegram/`
- 配置、profile、schema、vendor：`project/assets/`
- 运行态数据：`project/runtime/`
- skill 外壳不重写业务逻辑，只包装入口与迁移路径
