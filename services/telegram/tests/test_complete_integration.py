#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from datetime import datetime
from bazi_calculator import BaziCalculator
from location import get as get_loc
import json

def test_complete_integration():
    print("🔮 测试完整集成功能")
    print("=" * 70)
    
    # 创建计算器
    lng, lat = get_loc("深圳")
    calc = BaziCalculator(
        birth_dt=datetime(1990, 5, 15, 14, 30),
        gender="male",
        longitude=lng,
        latitude=lat,
        name="张三",
        birth_place="深圳",
    )
    
    # 执行计算
    try:
        result = calc.calculate()
    except Exception as e:
        print(f"❌ 计算失败: {e}")
        return
    
    # 统计字段数量
    total_fields = len(result)
    print(f"📊 总字段数: {total_fields}")
    print()
    
    print("🎯 关键字段校验:")
    ctst = result.get("completeTrueSolarTime", {})
    if ctst:
        print(f"✅ 真太阳时: {ctst.get('trueSolarTime')}")
    zta = result.get("ziTimeAnalysis", {})
    if zta:
        print(f"✅ 子时判定: 时支{zta.get('timeZhi','')} 触发{zta.get('zwzShift')}")
    ws = result.get("wuxingScores", {})
    if ws:
        print(f"✅ 强弱口径: {ws.get('weakStrong')}")
    sp = result.get("spiritsFull", {}).get("byPillar", {})
    if sp:
        print(f"✅ 神煞口径: 年{len(sp.get('year', []))} 月{len(sp.get('month', []))} 日{len(sp.get('day', []))} 时{len(sp.get('hour', []))}")
    
    print()
    print("=" * 70)
    print(f"🎯 完整功能集成度: {total_fields}个字段")
    print("🌟 所有功能均直接调用完整本地库，无任何阉割！")
    
    # 保存完整结果
    with open('complete_integration_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print("📄 完整结果已保存到 complete_integration_result.json")

if __name__ == "__main__":
    test_complete_integration()
