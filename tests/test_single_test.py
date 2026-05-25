from pathlib import Path

import pytest

from mcp_test_runner.parsers import parse_test_output
from mcp_test_runner.single_test import run_single_test


def test_run_single_test_runs_one_pytest_node_id(tmp_path: Path) -> None:
    (tmp_path / "test_sample.py").write_text(
        "def test_ok():\n"
        "    assert True\n"
        "\n"
        "def test_other():\n"
        "    assert True\n",
        encoding="utf-8",
    )

    result = run_single_test(tmp_path, "test_sample.py::test_ok", framework="pytest")
    report = (tmp_path / ".pytest-report.json").read_text(encoding="utf-8")
    parsed = parse_test_output(report, "pytest")

    assert result.exit_code == 0
    assert parsed.passed == 1
    assert parsed.failed == 0


def test_run_single_test_rejects_unsupported_framework(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Unsupported framework: vitest"):
        run_single_test(tmp_path, "test_ok", framework="vitest")
