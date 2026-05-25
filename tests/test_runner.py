import sys
from pathlib import Path

import pytest

from mcp_test_runner.runner import ResourceLimits, run_command


def test_run_command_returns_stdout_and_exit_code(tmp_path: Path) -> None:
    result = run_command(
        [sys.executable, "-c", "print('ok')"],
        cwd=tmp_path,
    )

    assert result.exit_code == 0
    assert result.stdout.strip() == "ok"
    assert result.stderr == ""
    assert result.timed_out is False


def test_run_command_uses_requested_cwd(tmp_path: Path) -> None:
    result = run_command(
        [sys.executable, "-c", "from pathlib import Path; print(Path.cwd())"],
        cwd=tmp_path,
    )

    assert result.stdout.strip() == str(tmp_path)


def test_run_command_returns_timeout_result(tmp_path: Path) -> None:
    result = run_command(
        [sys.executable, "-c", "import time; time.sleep(2)"],
        cwd=tmp_path,
        timeout_seconds=0.1,
    )

    assert result.exit_code == -1
    assert result.timed_out is True


def test_run_command_applies_memory_limit_to_child_process(tmp_path: Path) -> None:
    result = run_command(
        [sys.executable, "-c", "print('ok')"],
        cwd=tmp_path,
        resource_limits=ResourceLimits(memory_mb=512),
    )

    assert result.exit_code == 0
    assert result.stdout.strip() == "ok"


@pytest.mark.skipif(sys.platform == "win32", reason="resource.setrlimit is POSIX-only")
def test_run_command_applies_cpu_limit_to_child_process(tmp_path: Path) -> None:
    result = run_command(
        [sys.executable, "-c", "while True: pass"],
        cwd=tmp_path,
        timeout_seconds=5.0,
        resource_limits=ResourceLimits(cpu_seconds=1),
    )

    assert result.exit_code != 0
    assert result.timed_out is False


def test_run_command_rejects_missing_cwd(tmp_path: Path) -> None:
    missing_dir = tmp_path / "missing"

    with pytest.raises(ValueError, match="cwd must be an existing directory"):
        run_command(
            [sys.executable, "-c", "print('should not run')"],
            cwd=missing_dir,
        )
