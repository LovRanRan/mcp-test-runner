import json
from collections.abc import Mapping
from typing import cast

from mcp_test_runner.schemas import TestFailure, TestRunResult


def _as_mapping(value: object) -> dict[str, object]:
    if isinstance(value, Mapping):
        mapping = cast(Mapping[object, object], value)
        return {str(key): item for key, item in mapping.items()}
    return {}


def _as_list(value: object) -> list[object]:
    if isinstance(value, list):
        return cast(list[object], value)
    return []


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def _optional_int(value: object) -> int | None:
    if isinstance(value, int):
        return value
    return None


def _int_count(value: object) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(value)
    return 0


def parse_test_output(stdout: str, framework: str) -> TestRunResult:
    if framework != "pytest":
        raise ValueError(f"Unsupported framework: {framework}")

    payload = _as_mapping(json.loads(stdout))
    summary = _as_mapping(payload.get("summary"))
    tests = _as_list(payload.get("tests"))

    failures: list[TestFailure] = []
    for test in tests:
        test_payload = _as_mapping(test)
        if test_payload.get("outcome") != "failed":
            continue
        call = _as_mapping(test_payload.get("call"))
        crash = _as_mapping(call.get("crash"))

        failures.append(
            TestFailure(
                test_id=str(test_payload.get("nodeid", "")),
                message=str(crash.get("message", "")),
                file=_optional_str(test_payload.get("file")),
                line=_optional_int(test_payload.get("line")),
                traceback=_optional_str(call.get("longrepr")),
            )
        )

    return TestRunResult(
        passed=_int_count(summary.get("passed")),
        failed=_int_count(summary.get("failed")),
        skipped=_int_count(summary.get("skipped")),
        failures=failures,
    )
