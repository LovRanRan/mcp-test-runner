from pathlib import Path

from mcp_test_runner.runner import CommandResult, run_command


def build_pytest_command(test_filter: str | None = None) -> list[str]:
    command = [
        "pytest",
        "--json-report",
        "--json-report-file=.pytest-report.json",
    ]

    if test_filter:
        command.extend(["-k", test_filter])

    return command


def run_pytest(
    path: str | Path,
    test_filter: str | None = None,
    timeout_seconds: float = 10.0,
) -> CommandResult:
    return run_command(
        build_pytest_command(test_filter),
        cwd=path,
        timeout_seconds=timeout_seconds,
    )