# FateCat Skill 架构说明

## 目标

把 FateCat 从“完整应用仓库”包成“可触发的 Agent skill”，同时保持现有 CLI / API / Bot 能力不漂移。

## 当前阶段设计

```text
skills/fatecat/
├── SKILL.md                 # 触发入口
├── references/             # 长文档
├── assets/                 # 示例与模板
└── scripts/                # 包装脚本与导出脚本
     ├── *.sh               # 直接调用 FateCat CLI
     ├── fatecat_runtime/   # 嵌入式运行时镜像
     └── export-runtime.sh  # 物化独立 runtime
```

## 当前运行策略

- `skills/fatecat/scripts/fatecat_runtime/` 已包含一份 FateCat 运行时镜像。
- 为了避免刚复制出来时没有 `.venv` 导致脚本不可用，包装脚本会在“镜像未 bootstrap”时回退到源仓库。
- 当嵌入式 runtime 完成 bootstrap 后，包装脚本会优先使用它。

## 为什么仍然要保留同步脚本

- 根仓库仍然是真相源，嵌入式 runtime 只是 skill 封装所需镜像。
- 手工复制不可持续，必须有 `sync-runtime.sh` 统一刷新。
- 导出独立 bundle 时，也需要基于同样的排除规则控制 `.env`、`.db`、`.venv` 与 `.git`。

## 依赖边界

- 纯分析核心：`modules/fate_core/`
- 交付层：`modules/telegram/`
- 配置、profile、schema、vendor：`assets/`
- 运行态数据：`runtime/`
- skill 外壳不重写业务逻辑，只包装入口、镜像同步与迁移路径
