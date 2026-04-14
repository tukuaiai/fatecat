from __future__ import annotations

from typing import Any, Mapping

from fate_core.contracts import project_result


def project_by_profile(result: Mapping[str, Any], profile_name: str) -> dict[str, Any]:
    """将完整结果按 profile 裁剪为目标输出。"""
    return project_result(result, profile_name)
