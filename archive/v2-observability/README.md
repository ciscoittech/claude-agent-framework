# v2 Observability (retired)

SQLite-based agent execution tracking, retired from the active framework because it was
not in use and not ready to be relied on.

Nothing in `.claude/` or `.claude-library/` references this directory. It is kept because
the code works and is tested — reviving it is cheaper than rewriting it.

## What's here

| Path | What it is |
|---|---|
| `observability/schema.sql` | Tables, indexes, and views |
| `observability/db_helper.py` | Connection handling, migrations, insert/update helpers |
| `observability/pricing.py` | Per-tier rates and cost calculation |
| `observability/obs.py` | CLI: `recent`, `agents`, `execution <id>`, `cost-by-model` |
| `observability/scripts/` | Hook scripts that capture launches, completions, artifacts |
| `observability/configs/` | Hook config wiring the scripts to events |
| `observability/test_observability.py` | 49-test suite, passing at time of archival |
| `observer.md` | The agent that validated workflow outputs against the database |

## State at archival

The test suite passed 49/49. Late fixes worth knowing about if this is revived:

- Hooks gated on the tool name `Task`; the subagent tool is now `Agent`. Both are accepted.
- Migrations must run **before** `executescript()` — `schema.sql` indexes a column that
  migrations add, so the original ordering left old databases permanently broken.
- Views use `DROP VIEW` then `CREATE VIEW`; `CREATE VIEW IF NOT EXISTS` silently kept
  stale definitions on existing databases.
- Unpriced models record `NULL` cost, not `0.0` — zero reads as "free".
- `datetime.now()` is local while SQLite `CURRENT_TIMESTAMP` is UTC; duration must
  account for that.

## Known limitations (not fixed)

- `set_current_execution_id()` is a single slot, so metrics misattribute when agents run
  concurrently or nested. This needs an execution-id stack.
- The rate values in `pricing.py` were never verified against a published price card —
  only the arithmetic was tested.

## Reviving it

1. Move `observability/` back to `.claude-library/`.
2. Move `observer.md` to `.claude-library/agents/observability/`, and recreate a
   `.claude/agents/observer.md` stub plus its `REGISTRY.json` entry.
3. Re-add the `settings.observability` block and the hook config to `REGISTRY.json`.
4. Run `python3 .claude-library/observability/test_observability.py`.
