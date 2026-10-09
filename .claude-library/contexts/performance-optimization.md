# Performance Optimization

**Type**: Specialized context
**Domain**: Performance
**Audience**: Agents optimizing or validating framework performance

Performance targets, context budgets, and the cost levers that actually matter.

---

## Framework Targets

| Target | Value |
|---|---|
| Auto-loaded context (`.claude/`) | < 10KB; < 5KB for a minimal generated system |
| Parallel speedup | ~3x over sequential for independent work |
| Setup time for a new project | < 2 minutes |
| Tech stack support | Any, without framework modification |

---

## What Actually Drives Cost

In priority order. Earlier levers dominate later ones.

### 1. Effort tuning

Reasoning effort (`low` → `medium` → `high` → `xhigh` → `max`) is independent of model
choice and is usually the largest single lever. Lower effort means fewer and more
consolidated tool calls, less preamble, terser output.

Match effort to the work: `low` for mechanical and lookup tasks, `medium` for routine
implementation and docs, `high` to `xhigh` for design and review, `max` only when
correctness outweighs cost.

### 2. Prompt caching

Cached reads cost roughly a tenth of fresh input. Caching is a **prefix match** — any byte
change anywhere in the prefix invalidates everything after it.

Assemble every agent prompt stable-first:

```
persona → pinned contexts → volatile task
```

Selecting a different context set per task produces a different prefix on every run and
yields a near-zero hit rate. A fixed per-agent context bundle that caches reliably beats a
smaller bundle assembled fresh each call.

Silent invalidators to check for: timestamps or run IDs in the persona, unsorted JSON,
a tool list whose order varies between runs.

### 3. Model tier

Choose the lowest tier that clears the task's capability bar, then stop. See
`MODEL_SELECTION.md` for per-agent assignments. Escalating a coordinator is cheap;
escalating a coordinator *and* everything it spawns is not.

---

## Context Budgets

| Category | Budget | Notes |
|---|---|---|
| Subagent definition (`.claude/agents/*.md`) | < 2KB | Becomes the system prompt; paid every launch |
| Project instructions (`CLAUDE.md`) | < 5KB | Auto-loaded |
| Domain context file | 5–20KB | Loaded on demand |
| Code under analysis | Grep first, then Read | Locate before loading |
| Prior agent output | < 10KB | Summarize; never pass raw output forward |

**Relevance beats volume.** Every current model has a 1M context window,
which removes the old pressure to prune aggressively — but a focused 10KB context still
outperforms an unfocused 500KB dump. The window being large is not a reason to fill it.

Haiku 5.5 bills 5x once a request's prompt passes 100K tokens — for haiku, relevance is
also the price lever.

---

## Context Loading Strategies

| Strategy | Load time | Resident size | Cache hit rate |
|---|---|---|---|
| Full load | 5s | 250KB | n/a |
| Lazy load | 0.5s | 10KB | 0% initial |
| Cached load | 0.1s | 10KB | 85% |
| Pruned load | 0.3s | 5KB | 60% |

Scale the strategy to the project: load everything under ~50 files; lazy-load
non-essential contexts from ~50–500 files; prune and inherit above that; always use
per-domain context with lazy loading in a monorepo.

Note the tension between lazy loading and caching. Lazy loading minimizes bytes resident;
caching rewards those bytes staying identical. When an agent runs repeatedly, favor a
stable bundle. When it runs once, favor loading less.

---

## Parallel Execution

| Execution | 3 agents | 5 agents |
|---|---|---|
| Sequential | 90s | 150s |
| Parallel | 30s | 30s |

Launch parallel agents **in a single message** — split across messages they run
sequentially. Returns diminish beyond 5–7 concurrent agents; 3–5 is the sweet spot.

Parallel agents that write files need `isolation: "worktree"` or they will conflict.

---

## Per-Agent Baselines

Rough envelopes for a typical task; investigate sustained overruns.

| Agent | Token budget | Duration |
|---|---|---|
| `framework-system-architect` | 50K | 90s |
| `framework-code-reviewer` | 40K | 60s |
| `framework-validation-engineer` | 60K | 90s |

---

## Measuring

The framework has no built-in cost or duration tracking (the observability subsystem is
retired to `archive/v2-observability/`). Measure from the billing source: `/cost` in
Claude Code for the session, or the Anthropic Console for usage over time.

Compare **cost per completed task**, not per call. A model assignment that looks
expensive per call can be cheaper per completed task if it avoids retries — measure
completed work, not tokens in isolation.

## Anti-Patterns

- Loading entire codebases because the window allows it.
- Passing raw agent output forward instead of a summary.
- Varying an agent's context set per task, destroying its cache prefix.
- Parallelizing dependent work, then serializing on the fan-in anyway.
- Downgrading a model to save tokens and paying for it in retries.

---

## Related

- `framework-architecture.md` — directory split and registry schema
- `framework-development-patterns.md` — execution patterns and error handling
- `MODEL_SELECTION.md` — model and effort tier assignments
