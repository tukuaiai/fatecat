# AGENTS.md - embedded fatecat runtime

## 目录用途

`skills/fatecat/scripts/fatecat_runtime/` 是 FateCat 源仓库的嵌入式运行时镜像，服务于 skill 封装与独立分发验证。

## 目录结构

```text
fatecat_runtime/
├── AGENTS.md
├── README.md
├── Makefile
├── pyproject.toml
├── assets/
├── modules/
├── runtime/
├── scripts/
└── tests/
```

## 职责边界

- 这里是镜像，不是新的源码真相源。
- 根仓库仍然是主开发面；此目录通过 `../sync-runtime.sh` 刷新。
- 禁止直接把真实 `.env`、真实 `.db`、`.venv/` 混入该镜像。

## 依赖方向

- `fatecat_runtime/modules/* -> fatecat_runtime/assets/* + fatecat_runtime/runtime/*`
- `skills/fatecat/scripts/*.sh -> 此镜像 or 根仓库 runtime`
