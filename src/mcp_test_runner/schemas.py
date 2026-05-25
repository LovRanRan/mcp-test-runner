from pydantic import BaseModel, Field


class TestFailure(BaseModel):
    test_id: str
    message: str
    file: str | None = None
    line: int | None = None
    traceback: str | None = None


def empty_failures() -> list[TestFailure]:
    return []


class TestRunResult(BaseModel):
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    failures: list[TestFailure] = Field(default_factory=empty_failures)


class CoverageSummary(BaseModel):
    framework: str
    covered_lines: int
    total_lines: int
    percent_covered: float
    report_path: str | None = None
