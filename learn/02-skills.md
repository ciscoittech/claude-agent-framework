# Skills

*A procedure or a convention, loaded by name.*

Prerequisite: [01 — The Four Surfaces](./01-four-surfaces.md), which covers when a skill is
the right surface at all. This lesson assumes you have decided it is.

## Two forms, one thing

Custom commands and skills are the same mechanism. A file at `.claude/commands/deploy.md` and
a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and behave the same way.

The directory form adds three things: a place for supporting files, frontmatter that controls
who may invoke it, and automatic loading when Claude judges it relevant. If a `SKILL.md` and
a same-named command file both exist, **the `SKILL.md` wins** — which makes the command file
a file that looks live and is dead. Do not keep both.

> **A note on this framework's vocabulary.** `REGISTRY.json` has a `skills{}` section and a
> `commands{}` section, and the files live in `.claude/commands/`. These are not three
> concepts. `skills{}` is the declaration that reaches the file — description, tool
> pre-approval, invocation control. `commands{}` is orchestration wiring: which agents a
> command drives. The directory name is just where this repo happens to keep them.

## Two kinds of content

**Reference content** is knowledge applied to whatever you are already doing — conventions,
patterns, domain facts. It runs inline, alongside your conversation.

**Task content** is step-by-step instructions for an action: deploy, commit, generate. These
are usually things you want to fire deliberately by name, not have the model start on your
behalf.

The distinction matters because it decides two later choices: whether to set
`disable-model-invocation`, and whether the skill can be forked at all
([04 — Composition](./04-composition.md)).

## Who can invoke it

By default both you and Claude can invoke any skill. Two keys change that:

| Frontmatter | You | Claude | When loaded |
|---|---|---|---|
| *(default)* | Yes | Yes | Description always in context; full body loads on invocation |
| `disable-model-invocation: true` | Yes | No | Description **not** in context; body loads when you invoke |
| `user-invocable: false` | No | Yes | Description always in context; body loads on invocation |

Use `disable-model-invocation: true` for anything with side effects or timing you want to
own — `/deploy`, `/commit`, anything that spawns eight agents. You do not want Claude deciding
to deploy because the code looks ready.

Use `user-invocable: false` for background knowledge that is not a meaningful action. A skill
explaining how a legacy system works should inform Claude when relevant, but
`/legacy-system-context` is not something a person "runs."

Note the middle row: `disable-model-invocation` also removes the description from context.
That is a feature — it is how you keep a rarely-used skill from costing anything until the
moment you want it.

## A correct skill

```markdown
---
name: which-surface
description: Decide whether a piece of work belongs in a skill, a subagent, a hook, CLAUDE.md, or none of them
argument-hint: [what you want to make repeatable]
allowed-tools: Read, Grep, Glob
---

Work through the ladder in learn/01-four-surfaces.md and recommend one surface.
State which question produced the answer.
```

Four things that will bite you:

1. **`allowed-tools` pre-approves; it does not restrict.** It grants tools without a prompt
   for the turn that invokes the skill. It is not a sandbox. Scope Bash to what the skill
   actually runs — `Bash(pytest:*)`, never bare `Bash`, never `*`.
2. **The spellings differ by side.** Frontmatter uses `allowed-tools` with a hyphen; this
   framework's `REGISTRY.json` uses `allowed_tools` with an underscore. They must otherwise
   match exactly, and `validate_agent_system.py` fails when they drift.
3. **Put the key use case first in the description.** The combined `description` and
   `when_to_use` text is truncated at 1,536 characters in the skill listing.
4. **Keep the body short.** It stays in context for every turn after it loads. State what to
   do rather than narrating why.

## Supporting files

The directory form lets a skill carry references it does not pay for on every render:

```text
.claude/skills/which-surface/
├── SKILL.md            # short: the procedure
└── decision-table.md   # read only when needed
```

Use `${CLAUDE_SKILL_DIR}` to reference bundled files regardless of the working directory.

## When it stops working

If a skill seems to stop influencing behavior after the first response, its content is
usually still present and the model is simply choosing other approaches. Strengthen the
`description` and the instructions. If it *must* happen, it was never a skill — see
[05 — Hooks and memory](./05-hooks-and-memory.md).

---

*Next: [03 — Subagents](./03-subagents.md) · [Back to the index](./README.md)*
