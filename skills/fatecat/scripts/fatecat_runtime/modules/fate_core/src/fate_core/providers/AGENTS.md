# AGENTS.md - fate_core providers

## 目录用途

`modules/fate_core/src/fate_core/providers/` 负责把纯命理输出拆成可组合的字段组装器；每个文件只关心一组字段，不直接承载 HTTP / Bot 交付。

## 目录结构

```text
modules/fate_core/src/fate_core/providers/
├── AGENTS.md
├── __init__.py
├── base_chart.py
├── classical.py
├── fortune.py
└── runtime.py
```

## 职责边界

- `runtime.py`：构建共享运行时，集中复用遗留 `BaziCalculator` 与外部库入口。
- `base_chart.py`：本命盘基础字段。
- `fortune.py`：大运 / 流年 / 流月等运势字段。
- `classical.py`：格局、调候、建除、称骨等传统分析字段。

## 依赖约束

- 允许依赖 `contracts/` 与 `adapters/`。
- 禁止反向依赖 `main.py`、Telegram Bot、FastAPI schema。
- 优先复用已有成熟 repo 与遗留 helper，不在这里重写底层算法。
