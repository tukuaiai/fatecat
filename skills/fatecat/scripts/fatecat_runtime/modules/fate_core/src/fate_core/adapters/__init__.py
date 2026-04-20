"""外部成熟 repo 与遗留实现适配层。"""

from .legacy_bazi import LegacyBaziInput, PURE_ANALYSIS_HIDE, calculate_legacy_bazi, calculate_pure_analysis_raw

__all__ = [
    "LegacyBaziInput",
    "PURE_ANALYSIS_HIDE",
    "calculate_legacy_bazi",
    "calculate_pure_analysis_raw",
]
