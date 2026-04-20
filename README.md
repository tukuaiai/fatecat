# FateCat

当前仓库已经重构为单-skill仓库布局。

真实项目源码位于：

`project/`

根目录现在只承担 3 件事：

- 作为标准 skill 根目录
- 作为 FateCat 的包装入口与文档层
- 作为可导出的单-skill bundle 源

## 快速入口

- skill 说明：`SKILL.md`
- skill 架构：`AGENTS.md`
- 项目源码根：`project/AGENTS.md`

## 常用命令

```bash
bash scripts/bootstrap.sh
bash scripts/health.sh --mode pure --json
bash scripts/pure-analysis.sh \
  --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市"}' \
  --pretty
```

## 说明

- 不要再把业务源码塞回 `scripts/` 或 `references/`。
- 需要改业务代码时，直接进入 `project/`。
- 需要导出独立 skill bundle 时，使用 `bash scripts/export-runtime.sh --output <dir>`。
