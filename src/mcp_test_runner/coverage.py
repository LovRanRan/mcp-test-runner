import json
from pathlib import Path

from mcp_test_runner.parsers import _as_mapping, _int_count
from mcp_test_runner.runner import ResourceLimits, run_command
from mcp_test_runner.schemas import CoverageSummary


def _float_count(value: object) -> float:
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        return float(value)
    return 0.0


def build_coverage_command(framework: str = "pytest") -> list[str]:
    if framework != "pytest":
        raise ValueError(f"Unsupported framework: {framework}")

    return [
        "pytest",
        "--cov=.",
        "--cov-report=json:.coverage.json",
    ]


def get_coverage_summary(
    path: str | Path,
    framework: str = "pytest",
    timeout_seconds: float = 10.0,
    resource_limits: ResourceLimits | None = None,
) -> CoverageSummary:
    root = Path(path).resolve()
    result = run_command(
        build_coverage_command(framework),
        cwd=root,
        timeout_seconds=timeout_seconds,
        resource_limits=resource_limits,
    )
    if result.timed_out:
        raise RuntimeError("Coverage command timed out")
    if result.exit_code != 0:
        raise RuntimeError(result.stderr or result.stdout or "Coverage command failed")

    report_path = root / ".coverage.json"
    payload = _as_mapping(json.loads(report_path.read_text(encoding="utf-8")))
    totals = _as_mapping(payload.get("totals"))
    return CoverageSummary(
        framework=framework,
        covered_lines=_int_count(totals.get("covered_lines")),
        total_lines=_int_count(totals.get("num_statements")),
        percent_covered=_float_count(totals.get("percent_covered")),
        report_path=str(report_path),
    )
