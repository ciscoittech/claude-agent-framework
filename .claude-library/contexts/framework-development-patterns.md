# Framework Development Patterns

**Type**: Specialized context
**Domain**: Development
**Audience**: Agents building or modifying framework components

Execution patterns, isolation rules, and error handling for framework work.
Condensed from `AGENT_PATTERNS.md` — read that file for worked examples.

---

## The Hierarchy of Solutions

Effective agents are built on sound workflows, not complex reasoning loops. Escalate only
when the simpler level demonstrably fails.

```
Level 1: Prompt engineering      (simplest — try first)
   ↓
Level 2: Structured workflows    (most effective — where most work belongs)
   ↓
Level 3: Agentic systems         (most complex — reserve for open-ended problems)
```

| Problem type | Solution | Cost |
|---|---|---|
| Single-step task | Prompt engineering | Lowest |
| Multi-step, predictable | Workflow | Medium |
| Dynamic decisions from runtime state | Agent | Highest |

**The test**: can you define the steps in advance? If yes it is a workflow, even if the
content of each step varies. Most development tasks are workflows. A feature with known
stages (design → code → test → review) is a workflow. Reserve true agents for genuinely
open-ended problems like complex debugging or research.

---

## Execution Patterns

### Sequential

Each stage consumes the previous stage's output. Use when work is genuinely dependent:
progressive refinement, validation chains, design → implementation.

### Parallel

Independent agents launched **in a single message**. Splitting them across messages makes
them run sequentially and forfeits the speedup.

Good candidates: independent analysis, multiple searches, separate components, distinct
test types. Poor candidates: anything where one agent's output feeds another's input.

Returns diminish beyond 5–7 concurrent agents as coordination overhead grows; 3–5 is the
usual sweet spot.

### Hierarchical

A coordinator decomposes a problem and spawns specialists. The coordinator synthesizes;
it should not implement directly.

**The coordinator never propagates its own model to the agents it launches.** Every
sub-agent runs at the tier declared for it in `REGISTRY.json`. Pass that tier explicitly
on each launch rather than letting it inherit.

---

## Worktree Isolation

Parallel agents that write files need isolation or they will conflict.

```
isolation: "worktree"
```

Each agent gets its own copy of the repository. The worktree is removed automatically if
nothing changed, and returns a branch name if changes were made.

**Use it when**: multiple agents edit overlapping files, or an agent's changes should be
reviewable before merging.

**Skip it when**: agents are read-only, or they write to provably disjoint paths. Setup
costs time and disk per agent — it is not free.

---

## Background Execution

```
run_in_background: true
```

Returns immediately and notifies on completion. Appropriate for long-running work that
nothing downstream is waiting on. Do not poll for the result — completion re-invokes you.

---

## Error Handling

### Graceful degradation

Try the primary approach, then documented fallbacks, before failing. Report which
strategy succeeded so the failure path stays visible.

### Retry with backoff

Retry only on genuinely retryable conditions — timeouts, network errors, rate limits.
Never retry a validation failure or a bad request; the second attempt fails identically.
Cap total attempts and use exponential delay.

### Progressive quality gates

Run gates in order and terminate early on a critical failure rather than continuing to
accumulate errors.

| Gate | Critical |
|---|---|
| Syntax | yes |
| Linting | yes |
| Type check | yes |
| Unit tests | yes |
| Coverage | no |
| Security scan | yes |
| Performance | no |

A non-critical failure is reported but does not block; a critical failure stops the
pipeline and returns the failing gate.

### Circuit breaking

When a dependency fails repeatedly, stop calling it rather than retrying into a cascading
failure. Resume with a single trial call after a cooling-off period.

---

## Context Loading

Load contexts declared in the agent's `contexts[]` array, not everything available.

**Order matters for caching.** Assemble prompts stable-first:

```
persona → pinned contexts → volatile task
```

A context set that varies per task produces a different prefix on every run and defeats
prompt caching entirely. Prefer a fixed per-agent context bundle over per-task selection —
a large stable context that caches beats a small one rebuilt each call.

**Anti-pattern**: loading entire codebases. Even with a 1M window, relevance beats volume.
A focused 10KB context outperforms an unfocused 500KB dump. Use Grep to locate the
relevant sections first, then Read them.

---

## Framework Change Conventions

- **Simplicity first.** Check `SIMPLICITY_ENFORCEMENT.md` before adding a component.
  Complexity must be justified by a demonstrated failure of the simpler approach.
- **Referential integrity.** Adding an agent, command, or context means adding it to
  `REGISTRY.json` — and every `path` and `contexts[]` entry must resolve to a real file.
- **Test what you change.** `python3 test_v2_structure.py` validates structure,
  referential integrity, and agent tiers. Tests are self-contained scripts that exit
  non-zero on failure. No pytest.
- **Keep `.claude/` lean.** It is auto-loaded. Depth belongs in `.claude-library/`.

---

## Related

- `framework-architecture.md` — directory split, registry schema, routing
- `performance-optimization.md` — targets and context budgets
- `AGENT_PATTERNS.md` — full pattern catalogue with code examples
