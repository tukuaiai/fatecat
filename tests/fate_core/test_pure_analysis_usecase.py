import sys
from datetime import datetime
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "services" / "fate_core" / "src"))

from fate_core.usecases import PureAnalysisInput, calculate_pure_analysis

pure_analysis_module = importlib.import_module("fate_core.usecases.calculate_pure_analysis")


def test_calculate_pure_analysis_projects_profile(monkeypatch):
    def fake_calculate_raw(_payload):
        return {
            "input": {"name": "测试"},
            "meta": {"calculateTime": "2026-04-14 00:00:00"},
            "fourPillars": {"day": {"fullName": "甲子"}},
            "majorFortune": {"pillars": []},
            "yongShen": {"note": "测试"},
            "ziweiChart": {"should": "drop"},
            "liuyaoHexagram": {"should": "drop"},
        }

    monkeypatch.setattr(pure_analysis_module, "calculate_pure_analysis_raw", fake_calculate_raw)

    result = calculate_pure_analysis(
        PureAnalysisInput(
            birth_dt=datetime(1990, 5, 15, 14, 30, 0),
            gender="male",
            longitude=113.93,
            latitude=22.54,
            name="测试",
            birth_place="深圳南山",
        )
    )

    assert result["input"]["name"] == "测试"
    assert "fourPillars" in result
    assert "majorFortune" in result
    assert "yongShen" in result
    assert "ziweiChart" not in result
    assert "liuyaoHexagram" not in result
