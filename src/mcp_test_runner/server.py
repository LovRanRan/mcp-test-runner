from fastmcp import FastMCP

from mcp_test_runner.parsers import parse_test_output as parse_pytest_output
from mcp_test_runner.pytest_runner import run_pytest as run_pytest_command
from mcp_test_runner.runner import CommandResult
from mcp_test_runner.schemas import TestRunResult

mcp = FastMCP("mcp-test-runner")


@mcp.tool
def health() -> str:
    return "ok"


@mcp.tool
def run_pytest(
    path: str,
    test_filter: str | None = None,
    timeout_seconds: float = 10.0,
) -> CommandResult:
    return run_pytest_command(
        path=path,
        test_filter=test_filter,
        timeout_seconds=timeout_seconds,
    )


@mcp.tool
def parse_test_output(stdout: str, framework: str = "pytest") -> TestRunResult:
    return parse_pytest_output(stdout, framework)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
