# FateCat Skill Reference Index

## Quick Links

- 上手与边界：`architecture.md`
- 常用命令：`commands.md`
- 输入输出契约：`io-contract.md`
- 迁移与导出：`migration-plan.md`
- 故障排查：`troubleshooting.md`

## Reading Order

1. 先看 `architecture.md`，理解 `project/` 作为当前源码根的边界
2. 再看 `commands.md`，直接执行纯分析、健康检查与交付命令
3. 需要对接上层系统时，看 `io-contract.md`
4. 要做独立 skill 分发时，看 `migration-plan.md`
5. 遇到启动或依赖异常时，看 `troubleshooting.md`

## Scope Notes

- 这里记录的是 skill 化视角下的操作材料，不重复 FateCat 全量 README
- 外部成熟算法仓库仍以 `assets/vendor/` 为真相源，不在此处转抄
