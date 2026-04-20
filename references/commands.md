# FateCat Skill 命令参考

## 仓库内运行

### 安装

```bash
bash scripts/bootstrap.sh
```

### 纯分析健康检查

```bash
bash scripts/health.sh --mode pure --json
```

### 交付层健康检查

```bash
bash scripts/health.sh --mode delivery --json
```

### 纯分析

```bash
bash scripts/pure-analysis.sh \
  --input-json '{"birthDateTime":"1990-01-01 08:00:00","gender":"男","longitude":116.4074,"latitude":39.9042,"birthPlace":"北京市"}' \
  --pretty
```

### 启动 API

```bash
bash scripts/serve-api.sh
```

### 启动 Bot

```bash
bash scripts/serve-bot.sh
```

## 导出独立 bundle

```bash
bash scripts/export-runtime.sh --output /tmp/fatecat-skill-bundle
```

导出后的目录再执行：

```bash
bash scripts/bootstrap.sh
bash scripts/health.sh --mode pure --json
```
