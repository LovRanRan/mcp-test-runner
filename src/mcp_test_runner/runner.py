import subprocess
from pathlib import Path

from pydantic import BaseModel


class CommandResult(BaseModel):
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False


def _output_to_text(output: str | bytes | None) -> str:
    if output is None:
        return ""
    if isinstance(output, bytes):
        return output.decode("utf-8", errors="replace")
    return output


def run_command(
    command: list[str],
    cwd: str | Path,
    timeout_seconds: float = 10.0,
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
