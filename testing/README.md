# Testing Observability

Session-scoped test tracking: what ran, what failed, how it trended, and what to do about it.
Opt-in — nothing here is wired by default.

## Provenance, and why it is worth reading

This layer came from a separate `claude-testing-framework` repo (v1.1, October 2025) that was
built to verify this framework did what it claimed. Its design was sound. Its plumbing was not:

- Every hook passed shell variables — `"$tool"`, `"$file_path"`, `"$output"`, `"$exit_code"` —
  that Claude Code never sets. Each script received empty strings.
- Config paths pointed at `.claude-library/hooks/scripts/testing/`; the files were at
  `.claude-library/scripts/testing/`. Relative either way, so a session started in a
  subdirectory exited 127.
- `analyze_test_results.py` parsed `Total Tests: N` — the format of that repo's own wrapper
  script, not pytest. Against real pytest output it reported zero of everything.

So the layer never ran, and a layer that never runs looks exactly like one that always passes.
That is the same failure this framework's own security hook had, and the reason
`run_checks.py` exists.

Fixed on import: payloads read from stdin as JSON, real pytest summaries parsed
(`2 failed, 10 passed in 1.42s`), paths anchored with `$CLAUDE_PROJECT_DIR`, timezone-aware
timestamps. Verified by running each script against a real payload and watching the numbers
change from `0 | 0 | 0` to `12 | 10 | 2`.

## Enable it

Copy the entries from `.claude-library/hooks/configs/testing-observability.json` into
`.claude/settings.json`. Hooks only fire from there — `REGISTRY.json` is framework metadata
the harness never reads.

## What each script does

| Script | Event | Reads | Writes |
|---|---|---|---|
| `init_test_session.sh` | `SessionStart` | — | `.claude-metrics/testing/current_session.json` |
| `pre_test_validation.sh` | `PreToolUse` | `tool_name`, `tool_input.command` | `pre_test_validation.log` |
| `analyze_test_results.py` | `PostToolUse` (Bash) | `tool_response.stdout`, `.exit_code` | `test_metrics.jsonl`, per-run JSON |
| `track_test_changes.sh` | `PostToolUse` (Write\|Edit) | `tool_input.file_path` | `test_changes.jsonl` |
| `generate_test_report.py` | `Stop` | the session + metrics files | session report |

All of them exit 0 on any failure. Observability must never block the work it observes.

## Testing a change to these

Run the script against a real payload rather than reading it — that distinction is the whole
point of this directory:

```bash
echo '{"tool_name":"Bash","tool_response":{"stdout":"2 failed, 10 passed in 1.4s","exit_code":1}}' \
  | python3 testing/analyze_test_results.py
```
