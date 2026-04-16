#!/usr/bin/env python3
"""FateCat Telegram 模块启动脚本"""
import sys
import subprocess
from pathlib import Path


def main():
    src_dir = Path(__file__).parent / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    from branding import build_branding_text

    print(build_branding_text(compact=False))
    print("")

    if len(sys.argv) < 2:
        print("用法:")
        print("  python start.py bot     # 启动 Telegram Bot")
        print("  python start.py api     # 启动 FastAPI 接口")
        print("  python start.py both    # 同时启动 Bot 和 API")
        return

    mode = sys.argv[1]

    if mode == "bot":
        print("🤖 启动 Telegram Bot...")
        subprocess.run([sys.executable, str(src_dir / "bot.py")])

    elif mode == "api":
        print("🚀 启动 FastAPI 接口...")
        subprocess.run([sys.executable, str(src_dir / "main.py")])

    elif mode == "both":
        print("🚀 同时启动 Bot 和 API...")
        import threading

        def run_bot():
            subprocess.run([sys.executable, str(src_dir / "bot.py")])

        def run_api():
            subprocess.run([sys.executable, str(src_dir / "main.py")])

        bot_thread = threading.Thread(target=run_bot)
        api_thread = threading.Thread(target=run_api)

        bot_thread.start()
        api_thread.start()

        bot_thread.join()
        api_thread.join()

    else:
        print(f"❌ 未知模式: {mode}")

if __name__ == "__main__":
    main()
