import sys
from pathlib import Path

from mcp_test_runner.runner import CommandResult, ResourceLimits, run_command


def build_pytest_command(
    test_filter: str | None = None,
    test_id: str | None = None,
) -> list[str]:
    # Invoke via the running interpreter (`python -m pytest`) instead of a bare
    # `pytest` console script, which is not reliably on the subprocess PATH.
    command = [
        sys.executable,
        "-m",
        "pytest",
        "--json-report",
        "--json-report-file=.pytest-report.json",
    ]

    if test_id:
        command.append(test_id)

    if test_filter:
        command.extend(["-k", test_filter])

    return command


def run_pytest(
    path: str | Path,
    test_filter: str | None = None,
    timeout_seconds: float = 10.0,
    resource_limits: ResourceLimits | None = None,
) -> CommandResult:
    return run_command(
        build_pytest_command(test_filter),
        cwd=path,
        timeout_seconds=timeout_seconds,
        resource_limits=resource_limits,
    )
