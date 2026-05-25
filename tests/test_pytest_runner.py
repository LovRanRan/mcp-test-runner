from pathlib import Path

from mcp_test_runner.parsers import parse_test_output
from mcp_test_runner.pytest_runner import build_pytest_command, run_pytest


def test_build_pytest_command_includes_json_report_flags() -> None:
    command = build_pytest_command()

    assert command == [
        "pytest",
        "--json-report",
        "--json-report-file=.pytest-report.json",
    ]


def test_build_pytest_command_adds_filter() -> None:
    command = build_pytest_command("smoke")

    assert command == [
        "pytest",
        "--json-report",
        "--json-report-file=.pytest-report.json",
        "-k",
        "smoke",
    ]


def test_run_pytest_runs_passing_tests_and_writes_json_report(tmp_path: Path) -> None:
    (tmp_path / "test_sample.py").write_text(
        "def test_ok():\n"
        "    assert True\n",
        encoding="utf-8",
    )

    result = run_pytest(tmp_path)

    assert result.exit_code == 0
    assert (tmp_path / ".pytest-report.json").exists()


def test_run_pytest_records_failing_tests_in_json_report(tmp_path: Path) -> None:
    (tmp_path / "test_sample.py").write_text(
        "def test_fails():\n"
        "    assert False\n",
        encoding="utf-8",
    )

    result = run_pytest(tmp_path)
    report = (tmp_path / ".pytest-report.json").read_text(encoding="utf-8")
    parsed = parse_test_output(report, "pytest")

    assert result.exit_code == 1
    assert parsed.failed == 1
    assert len(parsed.failures) == 1
    assert parsed.failures[0].test_id == "test_sample.py::test_fails"


def test_run_pytest_filter_with_no_matching_tests_returns_nonzero(tmp_path: Path) -> None:
    (tmp_path / "test_sample.py").write_text(
        "def test_ok():\n"
        "    assert True\n",
        encoding="utf-8",
    )

    result = run_pytest(tmp_path, test_filter="missing_test_name")

    assert result.exit_code != 0
    assert (tmp_path / ".pytest-report.json").exists()


def test_run_pytest_returns_timeout_result(tmp_path: Path) -> None:
    (tmp_path / "test_sample.py").write_text(
        "import time\n\n"
        "def test_slow():\n"
        "    time.sleep(2)\n",
        encoding="utf-8",
    )

    result = run_pytest(tmp_path, timeout_seconds=0.1)

    assert result.exit_code == -1
    assert result.timed_out is True
