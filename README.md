# FateCat

当前仓库已经收口为 skill-only 结构。

真实项目源码位于：

`skills/fatecat/scripts/fatecat_runtime/`

根目录现在只承担 3 件事：

- 作为 Git 仓库根
- 作为 skill 入口导航层
- 作为后续导出与分发的最小容器

## 快速入口

- skill 说明：`skills/fatecat/SKILL.md`
- skill 架构：`skills/fatecat/AGENTS.md`
- 项目源码根：`skills/fatecat/scripts/fatecat_runtime/AGENTS.md`

## 常用命令

```bash
bash skills/fatecat/scripts/bootstrap.sh
bash skills/fatecat/scripts/health.sh --mode pure --json
bash skills/fatecat/scripts/pure-analysis.sh \
  --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市"}' \
  --pretty
```

## 说明

- 不要再把源码散回根目录。
- 需要改业务代码时，直接进入 `skills/fatecat/scripts/fatecat_runtime/`。
- 需要导出独立 skill bundle 时，使用 `bash skills/fatecat/scripts/export-runtime.sh --output <dir>`。
