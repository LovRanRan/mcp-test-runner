from pathlib import Path

from mcp_test_runner.runner import CommandResult, ResourceLimits, run_command


def build_jest_command(test_filter: str | None = None) -> list[str]:
    command = [
        "npx",
        "jest",
        "--json",
        "--outputFile=.jest-report.json",
    ]

    if test_filter:
        command.extend(["--testNamePattern", test_filter])

    return command


def run_jest(
    path: str | Path,
    test_filter: str | None = None,
    timeout_seconds: float = 10.0,
    resource_limits: ResourceLimits | None = None,
) -> CommandResult:
    return run_command(
        build_jest_command(test_filter),
        cwd=path,
        timeout_seconds=timeout_seconds,
        resource_limits=resource_limits,
    )
