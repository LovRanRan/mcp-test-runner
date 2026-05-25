# mcp-test-runner

MCP server for deterministic local test execution and normalized test result reporting.

`mcp-test-runner` is the verification layer for codebase onboarding agents. It will expose focused MCP tools for running pytest and Jest, parsing test output, and summarizing coverage so downstream agents can mark claims as verified, unverified, or contradicted by real execution.

## Status

This repository is in Commit 5 scaffold state. The MCP server currently exposes only `health()` while the pytest execution path is built in small slices.

The server does not use an LLM. Test results come from subprocess execution and structured parser output.

## Planned Tools

| Tool | Purpose |
| --- | --- |
| `health()` | Returns `ok` for smoke checks. |
| `run_pytest(path, filter?)` | Run pytest in a bounded working directory and return normalized results. |
| `run_jest(path, filter?)` | Run Jest and return normalized results. |
| `run_single_test(test_id)` | Run one framework-specific test target. |
| `parse_test_output(stdout, framework)` | Normalize test runner JSON output. |
| `get_coverage_summary(path, framework)` | Return coverage summary data when available. |

## Supported Scope

- Python 3.11+ package.
- FastMCP 2.x server.
- pytest-first implementation path.
- Jest support planned for v1 full acceptance.
- Subprocess sandboxing planned with timeout and POSIX `resource.setrlimit`.

## Current Limitations

- `run_pytest` is not implemented yet.
- `run_jest` is not implemented yet.
- Coverage parsing is not implemented yet.
- v1 will not use Docker; it will use subprocess boundaries and resource limits.

## Local Development

Install dependencies:

```bash
uv sync --extra dev
```

Run the MCP server:

```bash
uv run mcp-test-runner
```

Run verification:

```bash
uv run ruff check .
uv run mypy
uv run pytest
```

## License

MIT
