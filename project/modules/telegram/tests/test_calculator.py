#!/usr/bin/env python3
"""测试八字计算器"""
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from bazi_calculator import BaziCalculator
from location import get as get_loc

def test():
    print("🔮 测试八字计算器\n" + "=" * 50)
    
    dt = datetime(1990, 5, 15, 14, 30)
    lng, lat = get_loc("深圳")
    calc = BaziCalculator(dt, "male", longitude=lng, latitude=lat, name="张三", birth_place="深圳")
    try:
        r = calc.calculate()
    except Exception as e:
        print(f"❌ 计算失败: {e}")
        return
    
    fp = r["fourPillars"]
    print(f"四柱: {fp['year']['fullName']} {fp['month']['fullName']} {fp['day']['fullName']} {fp['hour']['fullName']}")
    print(f"纳音: {fp['year']['nayin']} {fp['month']['nayin']} {fp['day']['nayin']} {fp['hour']['nayin']}")
    
    tg = r["tenGods"]
    print(f"十神: 年{tg['year']['stem']} 月{tg['month']['stem']} 时{tg['hour']['stem']}")
    
    tw = r.get("twelveGrowth", {})
    print(f"长生: {tw.get('year','')} {tw.get('month','')} {tw.get('day','')} {tw.get('hour','')}")
    
    fe = r["fiveElements"]
    print(f"五行: 木{fe['wood']['count']} 火{fe['fire']['count']} 土{fe['earth']['count']} 金{fe['metal']['count']} 水{fe['water']['count']}")
    
    dm = r["dayMaster"]
    print(f"日主: {dm['stem']}({dm['element']}) {dm['yinYang']} {dm.get('strength','')}")
    
    sp = r.get("specialPalaces", {})
    print(f"宫位: 胎元{sp.get('taiYuan',{}).get('pillar','')} 命宫{sp.get('mingGong',{}).get('pillar','')} 身宫{sp.get('shenGong',{}).get('pillar','')}")
    
    mf = r["majorFortune"]
    print(f"大运: {mf['direction']} {mf['startAge']}岁起")
    print("  " + " ".join([f"{p['age']}岁{p['fullName']}" for p in mf["pillars"]]))
    
    print("=" * 50 + "\n✅ 测试完成")

if __name__ == "__main__":
    test()
