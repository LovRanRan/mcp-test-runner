import asyncio
import json
from pathlib import Path

from fastmcp import Client

from mcp_test_runner.schemas import TestRunResult as ResultSchema
from mcp_test_runner.server import health, mcp, parse_test_output, run_pytest


def test_health_returns_ok() -> None:
    assert health() == "ok"


def test_run_pytest_tool_returns_command_result(tmp_path: Path) -> None:
    (tmp_path / "test_sample.py").write_text(
        "def test_ok():\n"
        "    assert True\n",
        encoding="utf-8",
    )

    result = run_pytest(str(tmp_path))

    assert result.exit_code == 0
    assert result.timed_out is False
    assert (tmp_path / ".pytest-report.json").exists()


def test_parse_test_output_tool_returns_normalized_result() -> None:
    result = parse_test_output(
        json.dumps({"summary": {"passed": 1, "failed": 0, "skipped": 0}, "tests": []}),
        "pytest",
    )

    assert result.passed == 1
    assert result.failed == 0
    assert result.skipped == 0


def test_mcp_client_can_call_health_pytest_and_parse_output(tmp_path: Path) -> None:
    (tmp_path / "test_sample.py").write_text(
        "def test_ok():\n"
        "    assert True\n",
        encoding="utf-8",
    )

    async def run_client() -> None:
        async with Client(mcp) as client:
            tools = await client.list_tools()
            tool_names = {tool.name for tool in tools}

            assert "health" in tool_names
            assert "parse_test_output" in tool_names
            assert "run_pytest" in tool_names

            health_result = await client.call_tool("health", {})
            assert health_result.data == "ok"

            pytest_result = await client.call_tool("run_pytest", {"path": str(tmp_path)})
            assert pytest_result.structured_content is not None
            assert pytest_result.structured_content["exit_code"] == 0
            assert pytest_result.structured_content["timed_out"] is False

            parse_result = await client.call_tool(
                "parse_test_output",
                {
                    "stdout": json.dumps(
                        {"summary": {"passed": 1, "failed": 0, "skipped": 0}, "tests": []}
                    ),
                    "framework": "pytest",
                },
            )
            assert parse_result.structured_content is not None
            assert parse_result.structured_content["passed"] == 1

    asyncio.run(run_client())


def test_default_test_run_result_has_empty_counts() -> None:
    result = ResultSchema()

    assert result.passed == 0
    assert result.failed == 0
    assert result.skipped == 0
    assert result.failures == []
