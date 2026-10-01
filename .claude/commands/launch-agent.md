---
description: Analyze a task and launch the optimal agent with the right model, effort, and tools
allowed-tools: Agent, Read, Grep, Glob
---

# /launch-agent - Intelligent Agent Selection & Launch

**Purpose**: Analyze a task and launch the optimal agent with correct model, tools, and context
**Type**: Routing Command

---

## Usage

```bash
/launch-agent <task description>
```

**Examples**:
```bash
/launch-agent "refactor the auth module to use JWT"
/launch-agent "write tests for the payment service"
/launch-agent "document our REST API endpoints"
/launch-agent "review the PR for security issues"
```

---

## How It Works

### Step 1: Classify the Task

Read the task description and classify:

| Signal | Agent Type | Model | Effort |
|--------|-----------|-------|--------|
| simple fix, typo, rename, format | **engineer** | haiku | low |
| test, coverage, spec, assert | **engineer** (test focus) | sonnet | medium |
| document, guide, README, API docs | **documentation** | sonnet | medium |
| research, fetch docs, summarize | **research** | sonnet | low |
| implement, build, refactor, fix, code | **engineer** | opus | high |
| review, audit, security, quality | **reviewer** | opus | high |
| design, architecture, schema, plan | **architect** | opus | xhigh |
| multi-subsystem rewrite, long-horizon refactor | **architect** | fable | xhigh |

**Model and effort are separate dials.** Model sets the capability floor; effort sets how
hard it thinks. Adjust them independently:

- Task spans >5 files, multiple services, or says "complex" → raise **effort** first
  (`high` → `xhigh`), and only then the model.
- Task is a single file, a quick fix, or says "simple" → lower **effort** to `low` before
  dropping the model tier.
- Correctness matters more than cost (security, data migration, payments) → `max` effort.

**Two hard constraints:**

- **Haiku is 200K context; every other model is 1M.** Never route long-context work to
  haiku regardless of how simple the task looks — a "simple rename" across a large
  codebase is a long-context task.
- **Fable is an opt-in escalation, not a tier to route to automatically.** It costs 2.5x opus
  ($10/$50 vs $4/$20), always thinks, and runs substantially longer turns. Use it only when
  opus has already failed on this task, or when the work genuinely spans multiple
  subsystems and needs one coherent plan. When in doubt, use opus at `xhigh`.

### Step 2: Select Agent Definition

Every registry agent has a real subagent definition in `.claude/agents/<name>.md`
carrying its `model`, `effort`, and `tools` in frontmatter. Pass the filename as
`subagent_type` and Claude Code applies that tier automatically:

```python
subagent_type="framework-code-reviewer"   # .claude/agents/framework-code-reviewer.md
```

`.claude-library/REGISTRY.json` remains the source of truth — the stubs are generated to
match it, and `test_v2_structure.py` fails if they drift. Read the registry entry for:
- The full playbook path (the stub only points at it)
- Declared tools and restrictions
- Contexts to load
- `model` and `effort`

Fall back to `general-purpose` only when no registry agent matches the task.

### Step 3: Launch

Use the Agent tool to launch with the selected configuration:

```python
Agent(
    description="<short task summary>",
    prompt="""
    <Load agent persona from selected agent file>

    ## Project Context
    <Load relevant contexts from REGISTRY.json>

    ## Task
    <user's task description>
    """,
    subagent_type="<matched type or general-purpose>",
    model="<selected model>"
)
```

Note the prompt order: persona and contexts are stable across runs, the task is not.
Putting the volatile part last keeps the cacheable prefix intact. Reversing this costs
cache hits on every launch.

If the matched agent has an `effort` in `REGISTRY.json`, pass it too — the registry is the
source of truth for both dials, and a coordinator must never substitute its own tier:

```python
# Each sub-agent runs at ITS OWN registry tier, never the caller's
for agent in matched_agents:
    Agent(..., model=registry[agent]["model"])
```

### Step 4: Report

After agent completes, summarize:
- What was done
- Files created/modified
- Any issues or follow-ups needed

---

## Decision Tree

```
Task Description
├── Contains: implement/build/fix/refactor/code
│   ├── Simple (1 file, quick)        → engineer + haiku/low
│   ├── Medium (2-5 files)            → engineer + opus/medium
│   └── Complex (>5 files)            → engineer + opus/xhigh
├── Contains: test/spec/coverage      → engineer (test focus) + sonnet/medium
├── Contains: review/audit/security   → reviewer + opus/high
├── Contains: document/guide/README   → documentation + sonnet/medium
├── Contains: research/fetch docs     → research + sonnet/low
├── Contains: design/architecture/plan
│   ├── Single subsystem              → architect + opus/xhigh
│   └── Multi-subsystem, long-horizon → architect + fable/xhigh  (opt-in)
└── Unclear                           → general-purpose + sonnet/medium

Long context (large file set, whole-repo sweep)? Never haiku — it is 200K.
```

---

## Integration

This command reads from:
- `.claude-library/REGISTRY.json` — agent definitions, tools, contexts
- `.claude/agents/` — custom subagent types (if they exist)
- `.claude-library/agents/` — full agent persona files

For projects without a REGISTRY.json, falls back to `general-purpose` agent type with sonnet model.
