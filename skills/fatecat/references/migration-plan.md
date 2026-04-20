# FateCat Skill 迁移与导出计划

## Phase 1: 仓库内可运行的 skill 外壳

- 创建 `skills/fatecat/`
- 提供 `SKILL.md`、参考文档、包装脚本
- 所有脚本优先复用仓库根目录的 FateCat runtime

## Phase 2: 导出独立 bundle

- 通过 `export-runtime.sh` 复制运行所需骨架到导出目录
- 导出目标结构包含 `skills/fatecat/scripts/fatecat_runtime/`
- 排除 `.git/`、`.venv/`、真实 `.db`、真实 `.env`

## Phase 3: 后续优化

- 评估 `full` bundle 与 `lite` bundle 两种分发模式
- 视情况增加校验脚本，确保导出后命令仍可用

## 导出边界

必须带走：

- `pyproject.toml`
- `Makefile`
- `modules/`
- `assets/`
- `tests/`
- `README.md`
- `AGENTS.md`

必须排除：

- `.git/`
- `.venv/`
- `.pytest_cache/`
- `.ruff_cache/`
- `assets/config/.env`
- `runtime/**/*.db`

## 风险

- 导出包体积仍会很大，因为 `assets/vendor/` 是运行时依赖的一部分
- 若未来路径发现逻辑变化，包装脚本与导出脚本需要一起更新
