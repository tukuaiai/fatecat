# FateCat Skill 输入输出契约

## 纯分析最小输入

```json
{
  "birthDateTime": "1990-01-01 08:00:00",
  "gender": "男",
  "longitude": 116.4074,
  "latitude": 39.9042,
  "birthPlace": "北京市"
}
```

## 可接受别名

- `birth_datetime`
- `birth_dt`
- `datetime`
- `sex`
- `lng`
- `lat`
- `birth_place`

这些别名由 `modules/fate_core/src/fate_core/cli.py` 中的输入归一化逻辑处理。

## 纯分析输出顶层

```json
{
  "disclaimer": "...",
  "success": true,
  "profile": "pure_analysis",
  "data": {},
  "branding": {}
}
```

## 交付层入口

- CLI：`.venv/bin/fatecat pure-analysis`
- Health：`.venv/bin/fatecat health --mode pure|delivery`
- API：`POST /api/v1/bazi/pure-analysis`
- Bot：`.venv/bin/fatecat serve bot`
