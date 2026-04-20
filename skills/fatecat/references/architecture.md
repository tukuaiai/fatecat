# FateCat Skill 架构说明

## 目标

把 FateCat 从“完整应用仓库”包成“可触发的 Agent skill”，同时保持现有 CLI / API / Bot 能力不漂移。

## 当前阶段设计

```text
skills/fatecat/
├── SKILL.md                 # 触发入口
├── references/             # 长文档
└── scripts/                # 包装脚本与导出脚本
     ├── *.sh               # 直接调用 FateCat CLI
     ├── fatecat_runtime/   # FateCat 真实源码根
     └── export-runtime.sh  # 物化独立 runtime
```

## 当前运行策略

- `skills/fatecat/scripts/fatecat_runtime/` 已经承载 FateCat 的真实源码、运行时目录与项目元数据。
- 包装脚本只从这一个位置解析 runtime root，不再回退到 skill 外层根目录。
- `bootstrap.sh` 负责在这个 runtime 内补齐 `.venv`，导出脚本负责按同样边界生成可分发 bundle。

## 依赖边界

- 纯分析核心：`modules/fate_core/`
- 交付层：`modules/telegram/`
- 配置、profile、schema、vendor：`assets/`
- 运行态数据：`runtime/`
- skill 外壳不重写业务逻辑，只包装入口与迁移路径
