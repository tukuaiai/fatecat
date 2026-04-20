# FateCat Skill 命令参考

## 仓库内运行

### 标准预检（推荐默认入口）

```bash
bash scripts/preflight.sh --mode pure --bootstrap --pretty
```

### 标准预检并生成烟雾样例

```bash
bash scripts/preflight.sh \
  --mode pure \
  --bootstrap \
  --smoke \
  --output-file output/preflight-sample.json \
  --pretty
```

### 初始化生命周期包

```bash
bash scripts/init-lifecycle-pack.sh --name first-delivery
```

### 查看生命周期包状态

```bash
bash scripts/lifecycle-status.sh
```

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
  --output-file output/bazi-result.json \
  --pretty
```

### 启动 API

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/serve-api.sh
```

### 启动 Bot

```bash
bash scripts/preflight.sh --mode delivery --bootstrap --pretty
bash scripts/serve-bot.sh
```

### 采集 agent 运维包

```bash
bash scripts/collect-ops-bundle.sh --output /tmp/fatecat-ops-bundle
```

## 导出独立 bundle

```bash
bash scripts/export-runtime.sh --output /tmp/export-full/fatecat --mode full
```

## 导出轻量 bundle

```bash
bash scripts/export-runtime.sh --output /tmp/export-lite/fatecat --mode lite
```

导出后的目录再执行：

```bash
bash scripts/bootstrap.sh
bash scripts/preflight.sh --mode pure --bootstrap --pretty
/home/lenovo/.codex/skills/auto-skill/scripts/validate-skill.sh /tmp/export-lite/fatecat --strict
```
