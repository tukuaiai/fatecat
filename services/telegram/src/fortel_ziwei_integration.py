#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专业紫微斗数集成器 - 强制使用原生库，失败即报错

外部库依赖注入 (相对路径从项目根目录):
├── libs/external/github/fortel-ziweidoushu-main/  # 专业紫微斗数
└── libs/external/github/iztro-main/lib/index.js   # iztro核心算法

运行环境: Node.js 18+
纯净性声明: 强制调用原生TypeScript算法，失败即抛异常终止
"""

import subprocess
import json
import os
from datetime import datetime
from typing import Dict, Any

from _paths import IZTRO_DIR
IZTRO_PATH = str(IZTRO_DIR)

# 英文到中文映射
EN_TO_CN = {
    'origin': '本命',
    'decadal': '大限',
    'yearly': '流年',
    'monthly': '流月',
    'daily': '流日',
    'hourly': '流时',
    'major': '主星',
    'minor': '辅星',
    'soft': '吉星',
    'tough': '煞星',
    'adjective': '杂曜',
    'flower': '桃花',
    'lucun': '禄存',
    'tianma': '天马',
    'success': '成功',
}

def translate_value(obj):
    """递归翻译英文值为中文"""
    if isinstance(obj, dict):
        return {k: translate_value(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [translate_value(v) for v in obj]
    elif isinstance(obj, str) and obj in EN_TO_CN:
        return EN_TO_CN[obj]
    return obj

class FortelZiweiCalculator:
    """专业紫微斗数集成器 - 强制使用原生库，失败即报错"""
    
    def __init__(self, birth_dt: datetime, gender: str, longitude: float):
        self.birth_dt = birth_dt
        self.gender = gender
        self.longitude = longitude
        
    def _hour_to_shichen(self, hour: int) -> int:
        """小时转时辰索引(0-11)"""
        return ((hour + 1) // 2) % 12
        
    def calculate_ziwei_chart(self) -> Dict[str, Any]:
        """紫微斗数计算 - 强制使用原生算法"""
        return self._call_native_iztro()
    
    def calculate_professional_ziwei(self, as_of: datetime | None = None) -> Dict[str, Any]:
        """专业紫微计算"""
        result = self._call_native_iztro(as_of=as_of)
        return {
            'professionalZiwei': result,
            'stars': result.get('stars', {}),
            'palaces': result.get('palaces', {}),
            'influence': result.get('fiveElementsClass', {}),
            'horoscope': result.get('horoscope', {}),
        }
    
    def calculate_complete_ziwei_system(self, as_of: datetime | None = None) -> Dict[str, Any]:
        """完整紫微系统"""
        return self.calculate_professional_ziwei(as_of=as_of)
    
    def _call_native_iztro(self, as_of: datetime | None = None) -> Dict:
        """强制调用iztro原生算法"""
        shichen = self._hour_to_shichen(self.birth_dt.hour)
        gender_en = 'male' if self.gender in ['male', '男', 'm'] else 'female'
        as_of = as_of or datetime.now()
        as_of_shichen = self._hour_to_shichen(as_of.hour)
        
        js_script = f"""
        const {{ astro }} = require('{IZTRO_PATH}/lib/index.js');
        try {{
            const result = astro.bySolar(
                '{self.birth_dt.year}-{self.birth_dt.month:02d}-{self.birth_dt.day:02d}',
                {shichen},
                '{gender_en}',
                true,
                'zh-CN'
            );
            const asOf = new Date({as_of.year}, {as_of.month - 1}, {as_of.day}, {as_of.hour}, {as_of.minute}, {as_of.second});
            const hz = result.horoscope(asOf, {as_of_shichen});
            const hzOut = {{
                solarDate: hz.solarDate,
                lunarDate: hz.lunarDate,
                age: hz.age,
                decadal: hz.decadal,
                yearly: hz.yearly,
                monthly: hz.monthly,
                daily: hz.daily,
                hourly: hz.hourly,
            }};
            console.log(JSON.stringify({{
                source: "iztro原生算法",
                algorithm: "紫微斗数",
                solarDate: result.solarDate,
                lunarDate: result.lunarDate,
                fiveElementsClass: result.fiveElementsClass,
                soul: result.soul,
                body: result.body,
                palaces: result.palaces ? result.palaces.map(p => ({{name: p.name, heavenlyStem: p.heavenlyStem, earthlyBranch: p.earthlyBranch, majorStars: p.majorStars, minorStars: p.minorStars, adjectiveStars: p.adjectiveStars}})) : [],
                horoscope: hzOut,
                status: "success"
            }}));
        }} catch (e) {{
            console.log(JSON.stringify({{error: e.message}}));
            process.exit(1);
        }}
        """
        
        temp_file = '/tmp/native_iztro.js'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(js_script)
        
        env = dict(os.environ)
        env["TZ"] = "Asia/Shanghai"
        result = subprocess.run(['node', temp_file], capture_output=True, text=True, timeout=30, env=env)
        
        if result.returncode != 0:
            raise RuntimeError(f"iztro原生算法执行失败: {result.stderr}")
        
        try:
            data = json.loads(result.stdout)
            # 翻译英文为中文
            return translate_value(data)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"iztro输出解析失败: {e}")
