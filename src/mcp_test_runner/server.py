from fastmcp import FastMCP

from mcp_test_runner.coverage import get_coverage_summary as get_coverage_summary_impl
from mcp_test_runner.jest_runner import run_jest as run_jest_command
from mcp_test_runner.parsers import parse_test_output as parse_pytest_output
from mcp_test_runner.pytest_runner import run_pytest as run_pytest_command
from mcp_test_runner.runner import CommandResult, ResourceLimits
from mcp_test_runner.schemas import CoverageSummary, TestRunResult
from mcp_test_runner.single_test import run_single_test as run_single_test_impl

mcp = FastMCP("mcp-test-runner")


@mcp.tool
def health() -> str:
    return "ok"


@mcp.tool
def run_pytest(
    path: str,
    test_filter: str | None = None,
    timeout_seconds: float = 10.0,
    cpu_seconds: int | None = None,
    memory_mb: int | None = None,
) -> CommandResult:
    return run_pytest_command(
        path=path,
        test_filter=test_filter,
        timeout_seconds=timeout_seconds,
        resource_limits=ResourceLimits(cpu_seconds=cpu_seconds, memory_mb=memory_mb),
    )


@mcp.tool
def run_jest(
    path: str,
    test_filter: str | None = None,
    timeout_seconds: float = 10.0,
    cpu_seconds: int | None = None,
    memory_mb: int | None = None,
) -> CommandResult:
    return run_jest_command(
        path=path,
        test_filter=test_filter,
        timeout_seconds=timeout_seconds,
        resource_limits=ResourceLimits(cpu_seconds=cpu_seconds, memory_mb=memory_mb),
    )


@mcp.tool
def run_single_test(
    path: str,
    test_id: str,
    framework: str = "pytest",
    timeout_seconds: float = 10.0,
    cpu_seconds: int | None = None,
    memory_mb: int | None = None,
) -> CommandResult:
    return run_single_test_impl(
        path=path,
        test_id=test_id,
        framework=framework,
        timeout_seconds=timeout_seconds,
        resource_limits=ResourceLimits(cpu_seconds=cpu_seconds, memory_mb=memory_mb),
    )


@mcp.tool
def parse_test_output(stdout: str, framework: str = "pytest") -> TestRunResult:
    return parse_pytest_output(stdout, framework)


@mcp.tool
def get_coverage_summary(
    path: str,
    framework: str = "pytest",
    timeout_seconds: float = 10.0,
    cpu_seconds: int | None = None,
    memory_mb: int | None = None,
) -> CoverageSummary:
    return get_coverage_summary_impl(
        path=path,
        framework=framework,
        timeout_seconds=timeout_seconds,
        resource_limits=ResourceLimits(cpu_seconds=cpu_seconds, memory_mb=memory_mb),
    )


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
