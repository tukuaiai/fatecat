#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级历法集成器（胶水层）

目标：
- 禁止“简化判断/占位数据/自写日历算法”
- 只做依赖库与数据仓库的编排与适配（glue）
- 失败即抛异常，禁止降级与回退

外部依赖（本仓库内直连源码）：
- holiday-and-chinese-almanac-calendar-main：提供 iCalendar(.ics) 的“节假日 + 黄历宜忌（全年每日条目）”
- chinese-calendar-master：提供工作日/节假日/法定节日判断（含调休）
- lunar-python-master：提供公历/农历转换、节日/节气信息
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


from _paths import (
    HOLIDAY_CALENDAR_DIR, CHINESE_CALENDAR_DIR, LUNAR_PYTHON_DIR
)

_HOLIDAY_ICS_DIR = HOLIDAY_CALENDAR_DIR
_CHINESE_CALENDAR_DIR = CHINESE_CALENDAR_DIR
_LUNAR_PY_DIR = LUNAR_PYTHON_DIR

# 强依赖复用：运行期直连外部库源码（禁止复制进本项目）
sys.path.insert(0, str(_CHINESE_CALENDAR_DIR))
sys.path.insert(0, str(_LUNAR_PY_DIR))


@dataclass(frozen=True)
class _IcsEvent:
    dtstart: str
    summary: str
    description: str


def _strip_ics_text(v: str) -> str:
    v = (v or "").strip()
    # 反转义
    v = v.replace("\\n", "\n")
    v = v.replace("\\,", ",").replace("\\;", ";").replace("\\:", ":")
    return v.strip()


def _unfold_ics_lines(raw_lines: Iterable[str]) -> List[str]:
    """
    iCalendar 行折叠：以空格/Tab 开头视为上一行的延续。
    这里只做最小实现用于读取 SUMMARY/DESCRIPTION/DTSTART 等字段。
    """
    out: List[str] = []
    for line in raw_lines:
        s = line.rstrip("\n")
        if not s:
            continue
        if s.startswith(" ") or s.startswith("\t"):
            if not out:
                raise RuntimeError("ICS 折行格式错误：首行即 continuation")
            out[-1] += s.lstrip()
        else:
            out.append(s)
    return out


def _parse_ics_events(ics_path: Path) -> List[_IcsEvent]:
    if not ics_path.exists():
        raise FileNotFoundError(f"ICS 文件不存在: {ics_path}")
    raw = ics_path.read_text(encoding="utf-8", errors="strict").splitlines(True)
    lines = _unfold_ics_lines(raw)

    events: List[_IcsEvent] = []
    in_evt = False
    cur: Dict[str, str] = {}
    for line in lines:
        if line == "BEGIN:VEVENT":
            in_evt = True
            cur = {}
            continue
        if line == "END:VEVENT":
            if not in_evt:
                continue
            dtstart = cur.get("DTSTART", "")
            summary = cur.get("SUMMARY", "")
            description = cur.get("DESCRIPTION", "")
            if not dtstart or not summary:
                raise RuntimeError(f"ICS VEVENT 缺字段: DTSTART={dtstart!r} SUMMARY={summary!r}")
            events.append(_IcsEvent(dtstart=dtstart, summary=_strip_ics_text(summary), description=_strip_ics_text(description)))
            in_evt = False
            cur = {}
            continue
        if not in_evt:
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        # key 可能带参数：DTSTART;VALUE=DATE
        base_key = key.split(";", 1)[0].strip()
        cur[base_key] = val.strip()
    if in_evt:
        raise RuntimeError("ICS 解析失败：文件结束时仍处于 VEVENT 内")
    return events


def _ics_dtstart_to_date(dtstart: str) -> date:
    # 常见格式：
    # - YYYYMMDD
    # - YYYYMMDDTHHMMSS
    # - YYYYMMDDTHHMMSSZ
    s = (dtstart or "").strip()
    if not s:
        raise RuntimeError("ICS DTSTART 为空")
    m = re.match(r"^(\d{4})(\d{2})(\d{2})", s)
    if not m:
        raise RuntimeError(f"无法解析 ICS DTSTART: {dtstart!r}")
    return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))


def _extract_huangli_from_description(desc: str) -> Dict[str, Any]:
    """
    将 ICS 的 DESCRIPTION 解析成结构化宜忌。
    说明：这是数据适配（文本解析），不是“命理算法重写”。
    """
    text = (desc or "").strip()
    out: Dict[str, Any] = {"raw": text, "yi": [], "ji": []}
    if not text:
        return out

    # 形如：🈲️忌：搬家.搬新房\n\n✅宜：破屋.治病.馀事勿取.坏垣
    m_ji = re.search(r"忌：([^\\n]+)", text)
    m_yi = re.search(r"宜：([^\\n]+)", text)
    if m_ji:
        out["ji"] = [x for x in re.split(r"[\\.。\\s]+", m_ji.group(1).strip()) if x]
    if m_yi:
        out["yi"] = [x for x in re.split(r"[\\.。\\s]+", m_yi.group(1).strip()) if x]
    return out


class AdvancedCalendarCalculator:
    """高级历法集成器（胶水层）"""

    def __init__(self, dt: datetime):
        self.dt = dt

    def calculate_advanced_calendar(self) -> Dict[str, Any]:
        result = self._call_advanced_calendar()
        return {
            "advancedCalendar": {
                "source": "外部库直连（ICS + chinese_calendar + lunar-python）",
                "features": ["节假日", "黄历宜忌", "工作日/调休", "公历/农历/节气"],
                **result,
            }
        }

    def _call_advanced_calendar(self) -> Dict[str, Any]:
        if not _HOLIDAY_ICS_DIR.exists():
            raise FileNotFoundError(f"节假日/黄历 ICS 仓库不存在: {_HOLIDAY_ICS_DIR}")
        if not _CHINESE_CALENDAR_DIR.exists():
            raise FileNotFoundError(f"chinese-calendar 仓库不存在: {_CHINESE_CALENDAR_DIR}")
        if not _LUNAR_PY_DIR.exists():
            raise FileNotFoundError(f"lunar-python 仓库不存在: {_LUNAR_PY_DIR}")

        holiday_calendar = self._process_holiday_calendar()
        chinese_calendar = self._process_chinese_calendar()
        multi_calendar = self._process_multi_calendar()

        return {
            "holidayCalendar": holiday_calendar,
            "chineseCalendar": chinese_calendar,
            "multiCalendar": multi_calendar,
        }

    def _process_holiday_calendar(self) -> Dict[str, Any]:
        """
        解析 holiday-and-chinese-almanac-calendar-main 的 .ics 数据。
        约束：该仓库按年度生成（目前观测为 2025），若当前年份无数据则直接报错（禁止伪造/兜底）。
        """
        ics_files = sorted([p.name for p in _HOLIDAY_ICS_DIR.glob("*.ics")])
        if not ics_files:
            raise RuntimeError(f"ICS 仓库内无 .ics 文件: {_HOLIDAY_ICS_DIR}")

        # 年度全量：优先使用 holidays_calendar_year.ics
        year_ics = _HOLIDAY_ICS_DIR / "holidays_calendar_year.ics"
        if not year_ics.exists():
            raise RuntimeError("ICS 缺失 holidays_calendar_year.ics（无法提供全年条目）")

        events = _parse_ics_events(year_ics)
        if not events:
            raise RuntimeError("ICS 解析后无 VEVENT 记录")

        # 验证年份一致性：DTSTART 的 year 必须覆盖当前年份
        years = {(_ics_dtstart_to_date(e.dtstart).year) for e in events}
        if self.dt.year not in years:
            # 日历数据不覆盖当前年份时，返回空结果而非报错
            return {}

        today = self.dt.date()
        today_evt: Optional[_IcsEvent] = None
        year_count = 0
        for e in events:
            d = _ics_dtstart_to_date(e.dtstart)
            if d.year != self.dt.year:
                continue
            year_count += 1
            hl = _extract_huangli_from_description(e.description)
            if d == today:
                today_evt = e

        if year_count <= 0:
            raise RuntimeError(f"ICS 当年无条目: year={self.dt.year}")
        if today_evt is None:
            raise RuntimeError(f"ICS 未找到当天条目: date={today.isoformat()}")

        return {
            "available": True,
            "source": "holiday-and-chinese-almanac-calendar-main",
            "timezone": "Asia/Shanghai",
            "icsFiles": ics_files,
            "icsYearFile": year_ics.name,
            "year": self.dt.year,
            "yearEventsCount": year_count,
            "today": {
                "date": today.isoformat(),
                "summary": today_evt.summary,
                "description": today_evt.description,
                "huangli": _extract_huangli_from_description(today_evt.description),
            },
        }

    def _process_chinese_calendar(self) -> Dict[str, Any]:
        """
        使用 chinese_calendar-master 提供的权威判断：
        - is_workday / is_holiday
        - get_holiday_detail（若是法定节日）
        """
        try:
            from chinese_calendar import get_holiday_detail, is_holiday, is_workday
        except Exception as e:
            raise RuntimeError(f"导入 chinese_calendar 失败: {e}") from e

        d = self.dt.date()
        is_wd = bool(is_workday(d))
        is_hd = bool(is_holiday(d))
        try:
            hd, name = get_holiday_detail(d)
        except Exception as e:
            raise RuntimeError(f"chinese_calendar.get_holiday_detail 失败: {e}") from e

        return {
            "available": True,
            "source": "chinese-calendar-master",
            "date": d.isoformat(),
            "isWorkday": is_wd,
            "isHoliday": is_hd,
            "holidayDetail": {"isHoliday": bool(hd), "name": name},
        }

    def _process_multi_calendar(self) -> Dict[str, Any]:
        """使用 lunar-python-master 提供公历/农历/节气信息。"""
        try:
            from lunar_python import Solar
        except Exception as e:
            raise RuntimeError(f"导入 lunar_python 失败: {e}") from e

        dt = self.dt
        solar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        lunar = solar.getLunar()

        # lunar-python 返回的节日/节气字段比较分散，这里只做结构化聚合，不做任何推导。
        lunar_festivals = lunar.getFestivals() or []
        solar_festivals = solar.getFestivals() or []
        # 节气信息在 Lunar 对象上
        jieqi = lunar.getJieQi() or ""
        prev_jq = lunar.getPrevJieQi() or ""
        next_jq = lunar.getNextJieQi() or ""

        return {
            "timezone": "UTC+8",
            "gregorian": {
                "date": dt.strftime("%Y-%m-%d"),
                "time": dt.strftime("%H:%M:%S"),
                "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
            },
            "lunar": {
                "ymd": lunar.toString(),
                "yearInChinese": lunar.getYearInChinese(),
                "monthInChinese": lunar.getMonthInChinese(),
                "dayInChinese": lunar.getDayInChinese(),
                "timeZhi": lunar.getTimeZhi(),
                "festivals": lunar_festivals,
            },
            "solar": {
                "ymd": solar.toYmd(),
                "festivals": solar_festivals,
            },
            "jieqi": {
                "current": jieqi,
                "prev": prev_jq,
                "next": next_jq,
            },
        }
