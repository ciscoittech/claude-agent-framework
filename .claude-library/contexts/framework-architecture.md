# Framework Architecture

**Type**: Core context
**Domain**: Architecture
**Audience**: All framework agents

Core architecture of the Claude Agent Framework: how the two directories divide
responsibility, how agents are defined, and how work is routed.

---

## The Two-Directory Split

The framework separates *what loads automatically* from *what loads on demand*.

```
project-root/
├── .claude/                    # Auto-loaded by Claude Code. Keep it lean.
│   ├── agents/                 # Subagent definitions (YAML frontmatter + brief persona)
│   ├── commands/               # User-facing commands, invoked as /command-name
│   ├── rules/                  # Path-specific rules with glob targeting
│   ├── settings.json           # Project metadata, permissions, hooks
│   └── MEMORY.md               # Cross-conversation memory index
│
└── .claude-library/            # Loaded on demand only. Size is not a constraint here.
    ├── REGISTRY.json           # Central configuration — the source of truth
    ├── agents/                 # Full agent playbooks (core/, specialized/)
    ├── contexts/               # Shared project knowledge (this file)
    ├── patterns/               # Tool-usage guidance per agent role
    └── hooks/                  # Optional deterministic control
```

**The rule**: anything Claude Code reads at startup lives in `.claude/`. Everything else
lives in `.claude-library/` and is read by an agent only when that agent needs it.

---

## Agent Definitions Are Split in Two

An agent exists in two places, deliberately:

1. **`.claude/agents/<name>.md`** — the real subagent definition. YAML frontmatter
   (`name`, `description`, `tools`, `model`) plus a short persona: mission, when to use,
   and a pointer to the full playbook. Keep these lean; the body becomes that subagent's
   system prompt and is paid on every launch.

2. **`.claude-library/agents/<category>/<name>.md`** — the full playbook. Output formats,
   checklists, worked examples, anti-patterns. Read on demand by the agent itself.

This split exists because a subagent's system prompt is a fixed cost paid at every launch,
while its playbook is a variable cost paid only when the detail is actually needed.

`description` is the field that matters most for routing — the Agent tool matches against
it. Write it as "Use for X, Y, Z", not as a title.

---

## REGISTRY.json Is the Source of Truth

Every agent, command, context, and skill is declared in `.claude-library/REGISTRY.json`.
Each agent entry carries:

| Field | Purpose |
|---|---|
| `path` | Location of the full playbook |
| `type` | `core` or `specialized` |
| `domain` | Area of responsibility |
| `tools` | Tools the agent may use |
| `restrictions` | Tools explicitly denied |
| `model` | Capability tier: `haiku`, `sonnet`, `opus`, `fable` |
| `effort` | Reasoning depth: `low`, `medium`, `high`, `xhigh`, `max` |
| `triggers` | Keywords that route work here |
| `contexts` | Context files to load for this agent |
| `priority` | Routing precedence (1 = highest) |

**Referential integrity is a hard requirement.** Every `path` and every entry in a
`contexts[]` array must resolve to a file that exists. An agent told to load a missing
context silently degrades. `test_v2_structure.py` enforces this.

---

## Model and Effort Are Separate Dials

These are orthogonal and must not be conflated:

- **Model** sets the capability floor: `haiku` → `sonnet` → `opus` → `fable`.
- **Effort** sets reasoning depth: `low` → `medium` → `high` → `xhigh` → `max`.

An Opus agent at `low` effort and a Haiku agent are different things. `xhigh` is the
right setting for most coding and agentic work, and is not the Claude Code default.

Two constraints worth remembering:
- Haiku is the only current model with a 200K context window; everything else is 1M.
  Never route long-context work to it.
- Fable is 2.5x Opus per token, always thinks, and runs substantially longer
  turns. It is an opt-in escalation, never a default.

See `MODEL_SELECTION.md` for tier assignments and the full rationale.

---

## Routing

1. Input beginning with `/` resolves to `.claude/commands/<name>.md`.
2. Otherwise, match the request against `triggers` in REGISTRY.json.
3. Load the matched agent, its declared contexts, and launch at its `model` / `effort`.
4. With no match, fall back to `general-purpose`.

**A coordinator never propagates its own model to the agents it launches.** Each
sub-agent runs at the tier declared for it in REGISTRY.json. A coordinator escalated to
Fable that leaked its tier into six sub-agents would multiply the cost of an entire
workflow for no benefit.

---

## Workflow Shapes

- **Sequential** — each stage consumes the previous stage's output. Use for dependent work.
- **Parallel** — independent agents launched in a single message. Use for independent work.
- **Hierarchical** — a coordinator decomposes a problem and spawns specialists.

Parallel agents that write files should use worktree isolation to avoid conflicts.
Returns diminish beyond 5–7 concurrent agents as coordination overhead grows.

---

## Design Principles

1. **Simplicity first.** Direct action, then a command, then agents — in that order.
   Complexity is earned, not assumed.
2. **Single responsibility.** One agent, one job, with explicit boundaries on what it
   should *not* do.
3. **Least tools.** Grant only the tools the role requires; declare the rest as
   `restrictions`.
4. **Stable prefixes.** Assemble prompts stable-first (persona → pinned contexts →
   volatile task) so the cacheable prefix stays byte-identical across runs.
5. **Progressive complexity.** Start at three agents and one command. Add only on
   demonstrated need.

---

## Related

- `framework-development-patterns.md` — execution patterns and error handling
- `performance-optimization.md` — performance targets and context budgets
- `claude-code-subagents.md` — official Task tool and subagent reference
- `SIMPLICITY_ENFORCEMENT.md` — circuit breakers against over-engineering
