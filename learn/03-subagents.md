# Subagents

*A separate context window that returns a summary.*

Prerequisite: [01 — The Four Surfaces](./01-four-surfaces.md), particularly the section on
context isolation. This lesson is about predicting a subagent's behavior before you rely
on it.

## What it starts with

A subagent's initial context contains:

- its own system prompt, plus environment details — **not** the Claude Code system prompt
- the delegation message Claude wrote when handing off
- the `CLAUDE.md` hierarchy the main conversation loads
- a git status snapshot from the start of the parent session
- the full content of any skill named in its `skills:` field
- a roster of the other named agents in the session

## What it does not start with

This is the list that matters, and the one people are surprised by:

- your conversation history
- skills you have already invoked
- files Claude has already read
- your output style
- the main conversation's auto memory

Every one of those is a thing you know and it does not. The exception is a **fork**, which
inherits the parent conversation and system prompt.

**The practical consequence:** a delegation message that reads fine to you can be missing the
one constraint that makes the work correct. Six turns of conversation established that the
column must be nullable; the subagent was not in those six turns. Write the delegation as if
to a competent colleague who just walked in.

## Deciding

**Delegate when:**

- the task produces verbose output you will not reference again — logs, search results, test
  output. This is the single most effective use.
- you want tool restrictions actually enforced
- the work is self-contained and can return a summary

**Stay in the main conversation when:**

- the task needs frequent back-and-forth or iterative refinement
- multiple phases share significant context — planning, then implementing, then testing
- it is a quick, targeted change
- latency matters. A subagent that is not a fork starts cold and needs time to gather context

## Frontmatter that changes behavior

```markdown
---
name: schema-auditor
description: Read the current schema and recent migrations, and report what already exists
model: haiku
effort: low
tools: Read, Grep, Glob
---

Report on the current state of the schema. Return a short summary, not the raw DDL.
```

- **`model` and `effort` are independent dials.** `model` sets the capability floor,
  `effort` sets reasoning depth. An Opus agent at `low` effort and a Haiku agent are
  different things. See [MODEL_SELECTION.md](../MODEL_SELECTION.md).
- **`tools` is a real restriction**, unlike a skill's `allowed-tools`. This is the second
  independent reason to use a subagent: enforcement you cannot get any other way.
- **Omitting `tools` inherits everything.** Name what the role needs.
- **`skills:`** preloads full skill content at startup — see
  [04 — Composition](./04-composition.md).

In this framework, the file in `.claude/agents/` is the real definition and its body becomes
the system prompt, paid on every launch. Keep it short; the playbook goes in
`.claude-library/agents/` and is read on demand.

## Cost

A subagent is not free. It is a second context window with a cold start. For a two-line edit
it costs latency and buys nothing. The value scales with how much reading the task does and
how little of that reading you need afterward.

---

*Next: [04 — Composition](./04-composition.md) · [Back to the index](./README.md)*
