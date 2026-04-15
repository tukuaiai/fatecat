#!/usr/bin/env python3
"""测试统一品牌配置加载与拼装。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "modules" / "fate_core" / "src"))

from fate_core.support import append_branding_text, get_branding_payload


def test_get_branding_payload_contains_required_fields():
    branding = get_branding_payload()

    assert branding["name"] == "交易猫 TradeCat"
    assert branding["tradecatRepo"] == "https://github.com/tukuaiai/tradecat"
    assert branding["fatecatRepo"] == "https://github.com/tukuaiai/fatecat"
    assert branding["ca"] == "0x8a99b8d53eff6bc331af529af74ad267f3167777"


def test_append_branding_text_appends_sponsor_block():
    text = append_branding_text("测试正文", compact=True)

    assert "测试正文" in text
    assert "交易猫 TradeCat" in text
    assert "TradeCat Repo: https://github.com/tukuaiai/tradecat" in text
