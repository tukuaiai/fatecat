# AGENTS.md - fate_core

## 目录用途

`modules/fate_core/` 是命理胶水层内核：负责字段契约、profile、adapter、pipeline 与 usecase，不承载 Telegram / FastAPI 交付逻辑。

## 目录结构

```text
modules/fate_core/
├── AGENTS.md
└── src/fate_core/
    ├── adapters/
    ├── contracts/
    ├── kernel/
    ├── providers/
    ├── support/
    └── usecases/
```

## 职责边界

- `contracts/`：字段契约与 profile 加载；禁止依赖 Telegram / FastAPI。
- `adapters/`：唯一允许接触外部成熟 repo 或遗留 calculator 的地方。
- `providers/`：按字段组装配纯命理输出；允许调用 adapter 提供的运行时与遗留 helper。
- `kernel/`：结果投影与管线拼装；不实现底层算法。
- `usecases/`：对外暴露 `pure_analysis` / `full_report` 等应用入口。

## 依赖方向

- `usecases -> providers/kernel/contracts/adapters`
- `providers -> contracts/adapters`
- `kernel -> contracts`
- `adapters -> 外部库 / 遗留模块`
- 禁止 `contracts` 反向依赖 `usecases` 或 `telegram/api`
