# FateCat

当前仓库已经重构为单-skill 仓库布局，并补齐了面向 agent 的全生命周期 skill 外壳。

真实项目源码位于：

`project/`

根目录现在承担 4 件事：

- 作为标准 skill 根目录
- 作为 FateCat 的生命周期治理层
- 作为 FateCat 的包装入口与文档层
- 作为可导出的单-skill bundle 源

## 快速入口

- skill 说明：`SKILL.md`
- skill 架构：`AGENTS.md`
- 生命周期模板：`assets/lifecycle/`
- 项目源码根：`project/AGENTS.md`

## 常用命令

```bash
bash scripts/init-lifecycle-pack.sh --name first-delivery
bash scripts/lifecycle-status.sh
bash scripts/preflight.sh --mode pure --bootstrap --pretty
bash scripts/acceptance.sh
bash scripts/delivery-smoke.sh --target api
bash scripts/pure-analysis.sh \
  --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市"}' \
  --output-file output/bazi-result.json \
  --pretty
bash scripts/clean-runtime.sh --dry-run
bash scripts/collect-ops-bundle.sh --output /tmp/fatecat-ops-bundle
bash scripts/export-runtime.sh --output-parent /tmp/export-lite --mode lite
```

## 说明

- 不要再把业务源码塞回 `scripts/` 或 `references/`。
- 根级 `assets/` 用来放生命周期模板和治理资产，不放第二套业务代码。
- 需要改业务代码时，直接进入 `project/`。
- 日常执行默认先走 `bash scripts/preflight.sh --mode pure --bootstrap --pretty`，再进入真实任务。
- 要做完整发布门禁，直接执行 `bash scripts/acceptance.sh`。
- 要验证交付层不是“文档可用”，而是“入口可起”，执行 `bash scripts/delivery-smoke.sh --target api`；如果仓库里没有真实 `.env`，脚本会自动生成临时 smoke 配置并在退出后删除。
- 需要清理本地缓存而不误删源码时，执行 `bash scripts/clean-runtime.sh`；只有确实要重建环境时再加 `--venv`。
- 需要导出独立 skill bundle 时，优先用 `bash scripts/export-runtime.sh --output-parent /tmp/export-lite --mode lite`，只在确实需要带历史 lifecycle packs 时再用 `full`。
