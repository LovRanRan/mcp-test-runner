import subprocess
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path

from pydantic import BaseModel


class CommandResult(BaseModel):
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False


class ResourceLimits(BaseModel):
    cpu_seconds: int | None = None
    memory_mb: int | None = None


def _output_to_text(output: str | bytes | None) -> str:
    if output is None:
        return ""
    if isinstance(output, bytes):
        return output.decode("utf-8", errors="replace")
    return output


def _apply_resource_limits(limits: ResourceLimits) -> None:
    import resource

    if limits.cpu_seconds is not None:
        resource.setrlimit(
            resource.RLIMIT_CPU,
            (limits.cpu_seconds, limits.cpu_seconds),
        )

    if limits.memory_mb is not None:
        memory_bytes = limits.memory_mb * 1024 * 1024
        # RLIMIT_AS is platform-dependent; keep CPU limits and timeouts active.
        with suppress(OSError, ValueError):
            resource.setrlimit(
                resource.RLIMIT_AS,
                (memory_bytes, memory_bytes),
            )


def _build_preexec_fn(limits: ResourceLimits | None) -> Callable[[], None] | None:
    if limits is None:
        return None

    def apply_limits() -> None:
        _apply_resource_limits(limits)

    return apply_limits


def run_command(
    command: list[str],
    cwd: str | Path,
    timeout_seconds: float = 10.0,
    resource_limits: ResourceLimits | None = None,
) -> CommandResult:
    resolved_cwd = Path(cwd).resolve()

    if not resolved_cwd.exists() or not resolved_cwd.is_dir():
        raise ValueError(f"cwd must be an existing directory: {resolved_cwd}")

    try:
        completed = subprocess.run(
            command,
            cwd=resolved_cwd,
            timeout=timeout_seconds,
            capture_output=True,
            text=True,
            check=False,
            preexec_fn=_build_preexec_fn(resource_limits),
        )
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            exit_code=-1,
            stdout=_output_to_text(exc.stdout),
            stderr=_output_to_text(exc.stderr),
            timed_out=True,
        )

    return CommandResult(
        exit_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        timed_out=False,
    )
