# mcp-test-runner

<!-- mcp-name: io.github.LovRanRan/mcp-test-runner -->

MCP server for deterministic local test execution and normalized test result reporting.

`mcp-test-runner` is the verification layer for codebase onboarding agents. It exposes focused MCP tools for running pytest and Jest, parsing test output, and summarizing coverage so downstream agents can mark claims as verified, unverified, or contradicted by real execution.

## Codebase Onboarding Stack

`mcp-test-runner` is the verification layer in a three-server MCP tool stack for Project 6 `wayfinder`, a codebase onboarding agent.

- [`mcp-repo-mapper`](https://github.com/LovRanRan/mcp-repo-mapper) maps repository structure, languages, entry points, framework evidence, and Python dependency edges.
- [`mcp-ast-explorer`](https://github.com/LovRanRan/mcp-ast-explorer) provides symbol-grounded Python definition, signature, reference, call-chain, and class-hierarchy lookups.
- [`mcp-test-runner`](https://github.com/LovRanRan/mcp-test-runner) runs local pytest/Jest checks and coverage summaries so agent claims can be verified against execution.

In `wayfinder`, this server turns high-risk code understanding claims into `verified`, `unverified`, or `contradicted` evidence from real test execution.

## Status

This repository is a Python-first v1 MCP test runner. It supports bounded pytest execution, Jest command execution, single-test targeting, pytest coverage summaries, and normalized pytest/Jest JSON parsing.

The server does not use an LLM. Test results come from subprocess execution and structured parser output.

## Tools

| Tool | Purpose |
| --- | --- |
| `health()` | Returns `ok` for smoke checks. |
| `run_pytest(path, test_filter?, timeout_seconds?, cpu_seconds?, memory_mb?)` | Run pytest in a bounded working directory and return raw command output. |
| `run_jest(path, test_filter?, timeout_seconds?, cpu_seconds?, memory_mb?)` | Run Jest through `npx jest` and return raw command output. |
| `run_single_test(path, test_id, framework?, timeout_seconds?, cpu_seconds?, memory_mb?)` | Run one pytest node id or one Jest test-name pattern. |
| `parse_test_output(stdout, framework)` | Normalize test runner JSON output. |
| `get_coverage_summary(path, framework?, timeout_seconds?, cpu_seconds?, memory_mb?)` | Return pytest-cov JSON coverage totals. |

## Supported Scope

- Python 3.11+ package.
- FastMCP 2.x server.
- pytest execution with JSON report output via `pytest-json-report`.
- Jest command execution via `npx jest --json --outputFile`.
- pytest and Jest JSON normalization into one `TestRunResult` schema.
- Single pytest node id execution and Jest test-name targeting.
- pytest-cov coverage summary from `.coverage.json`.
- Subprocess timeout plus POSIX `resource.setrlimit` CPU / memory caps.

## Current Limitations

- v1 does not use Docker. It uses cwd validation, subprocess timeouts, and POSIX resource limits.
- Resource limits require a POSIX platform that supports `resource.setrlimit`.
- Jest execution expects Node.js plus project-local or `npx`-resolvable Jest.
- Jest single-test targeting uses `--testNamePattern`; it does not parse Jest file-specific node ids.
- Coverage summary is pytest-only in v1.
- Tools return raw command output for execution; call `parse_test_output` to normalize framework JSON.

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
