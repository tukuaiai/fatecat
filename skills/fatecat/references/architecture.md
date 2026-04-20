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
     └── export-runtime.sh  # 物化独立 runtime
```

## 为什么不在源仓库里直接复制 `fatecat_runtime/`

- 源仓库体量很大，`assets/vendor/` 含大量第三方代码，直接复制会造成仓库膨胀。
- 在仓库内部自复制整份源码会形成维护双写，后续任何修复都要同步两份。
- 复制到 `skills/fatecat/scripts/fatecat_runtime/` 还会制造递归打包风险。

## 运行时策略

- 仓库内使用：包装脚本直接调用仓库根目录的 FateCat 代码。
- 独立分发时：通过 `export-runtime.sh` 把运行所需骨架物化到导出目录的 `scripts/fatecat_runtime/`。

## 依赖边界

- 纯分析核心：`modules/fate_core/`
- 交付层：`modules/telegram/`
- 配置、profile、schema、vendor：`assets/`
- 运行态数据：`runtime/`
- skill 外壳不重写业务逻辑，只包装入口与迁移路径
