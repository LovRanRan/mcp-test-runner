from pathlib import Path

import pytest

from mcp_test_runner.coverage import build_coverage_command, get_coverage_summary


def test_build_coverage_command_returns_pytest_cov_command() -> None:
    assert build_coverage_command() == [
        "pytest",
        "--cov=.",
        "--cov-report=json:.coverage.json",
    ]


def test_get_coverage_summary_returns_pytest_totals(tmp_path: Path) -> None:
    (tmp_path / "app.py").write_text(
        "def add(a, b):\n"
        "    return a + b\n",
        encoding="utf-8",
    )
    (tmp_path / "test_app.py").write_text(
        "from app import add\n\n"
        "def test_add():\n"
        "    assert add(1, 2) == 3\n",
        encoding="utf-8",
    )

    result = get_coverage_summary(tmp_path)

    assert result.framework == "pytest"
    assert result.covered_lines > 0
    assert result.total_lines > 0
    assert result.percent_covered > 0
    assert result.report_path == str(tmp_path / ".coverage.json")


def test_get_coverage_summary_rejects_unsupported_framework(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Unsupported framework: jest"):
        get_coverage_summary(tmp_path, framework="jest")
