# Composition

*Skills and subagents stack. The direction decides what the run knows.*

Prerequisites: [02 — Skills](./02-skills.md) and [03 — Subagents](./03-subagents.md).

## The two directions

| Approach | System prompt comes from | The task is | Also loaded |
|---|---|---|---|
| Skill with `context: fork` | The agent type it forks into | The `SKILL.md` content | `CLAUDE.md`, except for Explore/Plan |
| Subagent with a `skills:` field | The subagent's own body | Claude's delegation message | The preloaded skills, plus `CLAUDE.md` |

**`context: fork` exports a procedure.** You write the task in the skill and pick an
environment to run it in.

**`skills:` imports a convention.** You define an environment and send known context along
with whatever task gets delegated to it.

## Forking a skill

```markdown
---
name: deep-research
description: Research a topic thoroughly and report back with file references
allowed-tools: Read, Grep, Glob
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly. Find relevant files with Glob and Grep, read
them, and summarize your findings with specific file references.
```

The `agent:` field picks the execution environment — model, tools, permissions. Built-ins
(`Explore`, `Plan`, `general-purpose`) or any custom subagent. Omitted, it uses
`general-purpose`. `Explore` and `Plan` skip `CLAUDE.md` to stay small, so a fork using them
sees only the skill content and the agent's own system prompt.

A forked skill runs in the background by default; its result arrives when it completes. Set
`background: false` to wait for it in the invoking turn.

## The empty fork

**`context: fork` only makes sense for a skill with explicit instructions.**

Fork a skill that is only guidelines — "prefer composition over inheritance," "always
parameterize queries" — and the forked context receives a system prompt, a page of advice,
and no task. It returns nothing useful, and it does not error.

The test is mechanical: **if the skill body contains no imperative sentences, it is reference
content, and reference content is not forkable.**

## Preloading skills

```markdown
---
name: api-developer
description: Implement API endpoints following team conventions
model: sonnet
effort: high
tools: Read, Write, Edit, Grep, Glob
skills:
  - api-conventions
  - error-handling-patterns
---

Implement the endpoint described in the delegation. Follow the preloaded conventions.
```

The full content of each listed skill is injected at startup — not just the description. This
controls what is *preloaded*, not what is *accessible*: without the field the subagent can
still discover and invoke skills through the Skill tool.

You cannot preload a skill that sets `disable-model-invocation: true`.

## Choosing

- The work is a **procedure** you want run in isolation → fork the skill.
- The work is **delegated judgment** that needs house conventions → preload skills into a
  subagent.
- The skill is **pure reference** → neither. Let it load inline where it applies.

---

*Next: [05 — Hooks and memory](./05-hooks-and-memory.md) · [Back to the index](./README.md)*
