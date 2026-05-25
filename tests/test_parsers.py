import json

import pytest

from mcp_test_runner.parsers import parse_test_output


def test_parse_test_output_returns_summary_counts() -> None:
    stdout = json.dumps(
        {
            "summary": {
                "passed": 2,
                "failed": 0,
                "skipped": 1,
            },
            "tests": [],
        }
    )

    result = parse_test_output(stdout, "pytest")

    assert result.passed == 2
    assert result.failed == 0
    assert result.skipped == 1
    assert result.failures == []


def test_parse_test_output_maps_pytest_failures() -> None:
    stdout = json.dumps(
        {
            "summary": {
                "passed": 1,
                "failed": 1,
                "skipped": 0,
            },
            "tests": [
                {
                    "nodeid": "test_sample.py::test_fails",
                    "outcome": "failed",
                    "file": "test_sample.py",
                    "line": 3,
                    "call": {
                        "crash": {"message": "assert False"},
                        "longrepr": "E assert False",
                    },
                },
                {
                    "nodeid": "test_sample.py::test_ok",
                    "outcome": "passed",
                },
            ],
        }
    )

    result = parse_test_output(stdout, "pytest")

    assert result.passed == 1
    assert result.failed == 1
    assert result.skipped == 0
    assert len(result.failures) == 1
    failure = result.failures[0]
    assert failure.test_id == "test_sample.py::test_fails"
    assert failure.message == "assert False"
    assert failure.file == "test_sample.py"
    assert failure.line == 3
    assert failure.traceback == "E assert False"


def test_parse_test_output_maps_jest_failures() -> None:
    stdout = json.dumps(
        {
            "numPassedTests": 1,
            "numFailedTests": 1,
            "numPendingTests": 1,
            "testResults": [
                {
                    "name": "math.test.js",
                    "assertionResults": [
                        {
                            "fullName": "adds numbers",
                            "status": "failed",
                            "failureMessages": ["Expected 3, received 4"],
                        },
                        {
                            "fullName": "subtracts numbers",
                            "status": "passed",
                            "failureMessages": [],
                        },
                    ],
                }
            ],
        }
    )

    result = parse_test_output(stdout, "jest")

    assert result.passed == 1
    assert result.failed == 1
    assert result.skipped == 1
    assert len(result.failures) == 1
    failure = result.failures[0]
    assert failure.test_id == "adds numbers"
    assert failure.message == "Expected 3, received 4"
    assert failure.file == "math.test.js"
    assert failure.traceback == "Expected 3, received 4"


def test_parse_test_output_rejects_unsupported_framework() -> None:
    with pytest.raises(ValueError, match="Unsupported framework: vitest"):
        parse_test_output("{}", "vitest")
