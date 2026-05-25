from pathlib import Path

from mcp_test_runner.jest_runner import run_jest
from mcp_test_runner.pytest_runner import build_pytest_command
from mcp_test_runner.runner import CommandResult, ResourceLimits, run_command


def run_single_test(
    path: str | Path,
    test_id: str,
    framework: str = "pytest",
    timeout_seconds: float = 10.0,
    resource_limits: ResourceLimits | None = None,
) -> CommandResult:
    if framework == "pytest":
        return run_command(
            build_pytest_command(test_id=test_id),
            cwd=path,
            timeout_seconds=timeout_seconds,
            resource_limits=resource_limits,
        )

    if framework == "jest":
        return run_jest(
            path=path,
            test_filter=test_id,
            timeout_seconds=timeout_seconds,
            resource_limits=resource_limits,
        )

    raise ValueError(f"Unsupported framework: {framework}")
