from pathlib import Path

import pytest

from mcp_test_runner.jest_runner import build_jest_command, run_jest
from mcp_test_runner.runner import CommandResult, ResourceLimits


def test_build_jest_command_includes_json_report_flags() -> None:
    command = build_jest_command()

    assert command == [
        "npx",
        "jest",
        "--json",
        "--outputFile=.jest-report.json",
    ]


def test_build_jest_command_adds_filter() -> None:
    command = build_jest_command("adds numbers")

    assert command == [
        "npx",
        "jest",
        "--json",
        "--outputFile=.jest-report.json",
        "--testNamePattern",
        "adds numbers",
    ]


def test_run_jest_delegates_to_command_runner(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    calls: list[tuple[list[str], Path, float, ResourceLimits | None]] = []

    def fake_run_command(
        command: list[str],
        cwd: str | Path,
        timeout_seconds: float = 10.0,
        resource_limits: ResourceLimits | None = None,
    ) -> CommandResult:
        calls.append((command, Path(cwd), timeout_seconds, resource_limits))
        return CommandResult(exit_code=0, stdout="{}", stderr="")

    monkeypatch.setattr("mcp_test_runner.jest_runner.run_command", fake_run_command)

    limits = ResourceLimits(cpu_seconds=2, memory_mb=256)
    result = run_jest(
        tmp_path,
        test_filter="adds numbers",
        timeout_seconds=3.0,
        resource_limits=limits,
    )

    assert result.exit_code == 0
    assert calls == [
        (
            [
                "npx",
                "jest",
                "--json",
                "--outputFile=.jest-report.json",
                "--testNamePattern",
                "adds numbers",
            ],
            tmp_path,
            3.0,
            limits,
        )
    ]
