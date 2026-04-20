from __future__ import annotations

from functools import lru_cache
from typing import Any
import json

from fate_core.support.paths import FATE_PROFILE_DIR


@lru_cache(maxsize=None)
def load_profile(profile_name: str) -> dict[str, Any]:
    """从配置目录加载字段 profile。"""
    path = FATE_PROFILE_DIR / f"{profile_name}.json"
    if not path.exists():
        raise ValueError(f"未知 profile: {profile_name}")
    with path.open("r", encoding="utf-8") as fh:
        profile = json.load(fh)
    if not isinstance(profile.get("fields"), list) or not profile["fields"]:
        raise ValueError(f"profile 缺少 fields 配置: {profile_name}")
    return profile
