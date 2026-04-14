# AGENTS.md - fate 配置目录

## 目录用途

`assets/fate/` 存放命理核心的字段与 profile 配置，是输出字段口径的配置真相源。

## 目录结构

```text
assets/fate/
├── AGENTS.md
└── profiles/
    └── pure_analysis.json
```

## 职责边界

- `profiles/`：定义某个输出 profile 允许返回哪些字段。
- 这里不放算法代码，不依赖 Telegram / FastAPI / 数据库。
- 新增字段时，先更新这里的 profile，再更新 `services/fate_core/` 的 provider / usecase。
