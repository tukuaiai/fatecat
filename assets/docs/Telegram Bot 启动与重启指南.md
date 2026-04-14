# Telegram Bot 启动与重启指南

## 环境前提
- 项目根：仓库根目录
- 依赖：已按 `modules/telegram/requirements.txt` 安装
- 环境变量优先放在 `assets/config/.env`
  - `FATE_BOT_TOKEN`（必需）
  - `FATE_ADMIN_USER_IDS`（可选，管理员 Telegram ID）

## 单实例启动（推荐）
1) 先清理旧进程，避免多实例冲突  
```bash
pgrep -f "modules/telegram/src/bot.py" | xargs -r kill
```
2) 前台启动（便于观察输出）  
```bash
cd modules/telegram
../../.venv/bin/python start.py bot
```
看到 “🤖 启动 Telegram Bot...” 即开始运行，`Ctrl+C` 结束。

## 后台守护启动
```bash
cd modules/telegram
nohup ../../.venv/bin/python start.py bot > output/logs/nohup.out 2>&1 &
pgrep -f "modules/telegram/src/bot.py"
```
记下输出的 PID，后续停止/重启使用。

## 停止 / 重启
- 停止：`pgrep -f "modules/telegram/src/bot.py" | xargs -r kill`
- 强制：`... | xargs -r kill -9`
- 重启：按“停止”→“后台守护启动”顺序。

## 日志查看
```bash
tail -f modules/telegram/output/logs/bot.log
```
若使用 nohup，可同时查看 `output/logs/nohup.out`。

## 运行模式
- 仅 Bot：`python3 start.py bot`
- 仅 API：`python3 start.py api`
- Bot+API：`python3 start.py both`（线程方式并发）

## 自恢复与健康
- Bot 内置重连与发送重试；网络抖动会指数退避。
- 若 60s 内持续失败，进程会退出，便于外部 watchdog/supervisor 重启。
- 管理员（`FATE_ADMIN_USER_IDS` 中的首个 ID）调用排盘时跳过假进度，直接返回结果，便于验证。

## 故障排查速查
- 报“未设置 FATE_BOT_TOKEN”：确认 `assets/config/.env` 已加载，或先导出同名环境变量。
- 启动报端口占用（API 模式）：释放端口或修改 `src/main.py` 端口。
- 长时间无响应：`tail -f bot.log`，必要时按“停止/重启”执行。
