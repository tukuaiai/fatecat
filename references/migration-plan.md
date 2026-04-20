# FateCat Skill 单仓布局与导出计划

## 当前布局

- 根目录直接作为 skill 根
- `SKILL.md`、`references/`、`scripts/` 位于根目录
- FateCat 项目整体收口到 `project/`
- 包装脚本只依赖 `project/` 这一处源码真相源

## 导出 bundle

- 通过 `export-runtime.sh` 复制运行所需骨架到导出目录
- 导出目标结构保持当前单-skill布局
- 排除 `.git/`、`.venv/`、真实 `.db`、真实 `.env`

## 后续优化

- 评估 `full` bundle 与 `lite` bundle 两种分发模式
- 视情况增加校验脚本，确保导出后命令仍可用

## 导出边界

必须带走：

- `README.md`
- `AGENTS.md`
- `SKILL.md`
- `references/`
- `scripts/`
- `project/`

必须排除：

- `.git/`
- `.history/`
- `.venv/`
- `.pytest_cache/`
- `.ruff_cache/`
- `project/assets/config/.env`
- `project/runtime/**/*.db`

## 风险

- 包体积仍然很大，因为 `assets/vendor/` 是运行时依赖的一部分
- 若未来路径发现逻辑变化，包装脚本与导出脚本需要一起更新
