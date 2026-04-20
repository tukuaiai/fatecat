# FateCat Skill 故障排查

## `配置文件不存在`

- 原因：`assets/config/.env` 缺失
- 处理：先复制 `assets/config/.env.example` 或 `assets/config/agent.env.example`

## `未设置 FATE_BOT_TOKEN`

- 原因：你在执行 `delivery` 检查或启动 Bot，但没有配置 token
- 处理：补齐 `assets/config/.env` 后再执行 `health --mode delivery`

## `缺少必需依赖`

- 原因：`assets/vendor/` 下的运行依赖不完整
- 处理：先在仓库根目录完成完整 checkout，不要裁剪 vendor

## `找不到 runtime root`

- 原因：你直接拷走了 `skills/fatecat/`，但没有执行导出脚本物化运行时代码
- 处理：回到源仓库执行 `export-runtime.sh --output <dir>`，再从导出目录运行

## 导出目录里仍然有敏感文件

- 原因：手工复制绕过了导出脚本
- 处理：删除导出目录，重新使用 `export-runtime.sh`
