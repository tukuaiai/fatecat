#!/usr/bin/env python3
"""测试统一品牌配置加载与拼装。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "modules" / "fate_core" / "src"))

from fate_core.support import (
    append_branding_text,
    build_branding_text,
    get_branding_payload,
    get_disclaimer_payload,
)


def test_get_branding_payload_contains_required_fields():
    branding = get_branding_payload()

    assert branding["name"] == "交易猫 TradeCat"
    assert branding["tradecatRepo"] == "https://github.com/tukuaiai/tradecat"
    assert branding["fatecatRepo"] == "https://github.com/tukuaiai/fatecat"
    assert branding["ca"] == "0x8a99b8d53eff6bc331af529af74ad267f3167777"


def test_get_disclaimer_payload_matches_required_text():
    disclaimer = get_disclaimer_payload()

    assert "本项目及AI分析结果仅供传统文化研究、算法测试与娱乐参考。" in disclaimer
    assert "命理学非精密科学，命运掌握在自己手中。" in disclaimer
    assert "本开源项目及开发者概不负责。" in disclaimer


def test_append_branding_text_appends_sponsor_block():
    text = append_branding_text("测试正文", compact=True)

    assert text.startswith("⚠️ 免责声明")
    assert "测试正文" in text
    assert "交易猫 TradeCat" in text
    assert "TradeCat Repo: https://github.com/tukuaiai/tradecat" in text


def test_build_branding_text_puts_disclaimer_before_branding():
    text = build_branding_text(compact=False)

    assert text.startswith("⚠️ 免责声明")
    assert "交易猫 TradeCat｜世界最强的专业命理排盘与 AI 命理分析基础设施" in text
