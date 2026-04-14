"""Pytest configuration for fatecat tests.

Note: Main test files are in services/telegram/tests/
This conftest.py provides shared fixtures for all tests.
"""

import sys
from pathlib import Path

import pytest

# Add service paths to sys.path for imports
REPO_ROOT = Path(__file__).parent.parent
TELEGRAM_SERVICE_ROOT = REPO_ROOT / "services" / "telegram"
FATE_CORE_SRC = REPO_ROOT / "services" / "fate_core" / "src"

if str(TELEGRAM_SERVICE_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(TELEGRAM_SERVICE_ROOT / "src"))

if str(FATE_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(FATE_CORE_SRC))


@pytest.fixture
def sample_birth_data():
    """Sample birth data for bazi calculation tests."""
    return {
        "year": 1990,
        "month": 6,
        "day": 15,
        "hour": 12,
        "gender": "male",
    }


@pytest.fixture
def sample_name():
    """Sample name for xingming analysis tests."""
    return {
        "surname": "张",
        "given_name": "三",
    }
