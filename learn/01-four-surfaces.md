# The Four Surfaces

*Where work goes, and what each place costs.*

Claude Code gives you four places to put a decision. They are not interchangeable, and
choosing wrong is the most expensive mistake in this framework — because every one of them
fails quietly. A skill that should have been a subagent still works; it just drags three
thousand lines of grep output through every turn that follows. A rule that should have been
a hook still works, right up until the session where the model is talked out of it.

The four:

- **`CLAUDE.md`** — facts that are true on every turn.
- **Skills** — procedures and conventions, pulled in by name when relevant.
- **Subagents** — work done in a separate context window that returns a summary.
- **Hooks** — code that runs whether or not the model agrees.

---

## The economics, which is the actual difference

Everything you write ends up in a context window. The surfaces differ in *when* it arrives,
*how long it stays*, *whose window it lands in*, and whether it can be skipped.

| Surface | Enters context | Stays for | Whose window | Can the model skip it? |
|---|---|---|---|---|
| `CLAUDE.md` | Session start, always | The whole session | Main, and any subagent, which reloads it | Yes — it is instructions |
| Skill | On invocation. Its `description` is in context from the start so it can be matched | Every turn after, until compaction | Whoever invoked it | Yes, unless `disable-model-invocation: true` — and then only you can fire it |
| Subagent | Never enters yours | Its own window, discarded on return | Its own. You get only its final message | Yes — delegating is a choice |
| Hook | Never enters any window | Not applicable. It is a program | **No** |

The last column decides most cases. Three of these four are *requests*. A hook is not. If the
requirement is "this must happen even when the model has been given an excellent reason to
skip it," there is exactly one surface, and the other three are wishful thinking.

The docs say this plainly about `CLAUDE.md`, and it applies to skills too: *"Claude treats
them as context, not enforced configuration. To block an action regardless of what Claude
decides, use a PreToolUse hook instead."*

### Skill content is a recurring cost

The property people miss until it bites: **a skill's content stays**.

When a skill is invoked, its rendered `SKILL.md` enters the conversation as a single message
and remains there for the rest of the conversation. Claude Code does not re-read the file on
later turns. So every line you write in a skill is not a one-time cost — it is paid again on
every turn after invocation, including turns about something else entirely.

A 400-line skill is not thorough. It is a 400-line tax on the rest of the session.

---

## The ten-second decision

<!-- canonical: surface-decision-table -->

Ask these in order. Take the first "yes."

1. **Must this happen every time, even if the model is convinced otherwise?**
   → **Hook.** `.claude/settings.json`. Deterministic, not negotiable.
2. **Is it a short fact, true on every turn, that you want applied without anyone asking?**
   → **`CLAUDE.md`.** Naming conventions, where things live, what the test command is.
3. **Would doing this flood your conversation with output you will never read again?**
   → **Subagent.** Search results, logs, forty files skimmed to produce one paragraph.
4. **Is it a procedure with known steps, that you or the model will start by name?**
   → **Skill.** `/deploy`, `/review-code`, "how we write migrations."
5. **None of the above?**
   → **Neither.** Type the command. Say the sentence. Come back when you have done it
   three times.

Step 5 is not a consolation prize. It is the most common correct answer, and
[SIMPLICITY_ENFORCEMENT.md](../SIMPLICITY_ENFORCEMENT.md) exists because it is the one people
skip. A skill that wraps a single tool call is worse than the tool call: it is a file, a
registry entry, a description that must stay in sync, and a permanent line of invocation-time
context — all to save typing something you run twice a month.

### Picking wrong is cheap to do and expensive to keep

| You built | Because | What it actually costs |
|---|---|---|
| A skill, for a rule | It felt like documentation | It only applies when invoked. Silent the other 90% of the time |
| A skill, for a search task | It's a "procedure" | Every line of its output lives in your main window until compaction |
| `CLAUDE.md`, for a hard rule | You wrote it in bold and in caps | Bold is not enforcement. It is still a request |
| A subagent, for a two-line edit | It felt tidy | A whole extra context window and a cold start, to save you nothing |
| A hook, for a preference | Determinism felt safe | It fires on work where it makes no sense, so someone disables it entirely |

---

## Context isolation

A subagent is not "an agent with different instructions." It is a **separate context window**.

It does not receive your conversation history. It does not receive the skills you have
invoked, the files you have already read, your output style, or your auto memory. When it
finishes, its entire window is discarded and you get back exactly one thing: whatever it
wrote in its final message.

That single sentence holds both the benefit and the cost.

**The benefit.** A task that reads forty files and prints four thousand lines of grep output
costs your main conversation one paragraph. The four thousand lines were real — read,
reasoned over, thrown away. You keep the conclusion and pay nothing for the evidence. This is
the only mechanism in Claude Code that lets a session do a large amount of reading without
the reading accumulating.

**The cost.** Everything it needs, you must say. The most common subagent failure is not a
bad agent; it is a good agent that was never told what the last twenty minutes established.
You spend six turns deciding that a new column must be nullable for backward compatibility,
then delegate "add the migration," and get back a `NOT NULL`. The agent was not wrong. It was
not there.

The practical rule: **write the delegation message as if to a competent colleague who just
walked in.** State the goal, the constraints already settled, and the exact shape you want
back. If that message is getting long, that is a signal — either the task is genuinely
self-contained, and you should delegate it, or it is entangled with the conversation, and you
should do it inline.

**Stay in the main conversation when** you expect frequent back-and-forth; later phases need
what earlier phases learned; the change is small and targeted; or latency matters.

**Delegate when** the output is verbose and disposable; you want tool restrictions actually
enforced; or the work is self-contained and returns a summary.

---

## Skills and subagents compose, in two directions

These are not alternatives. They stack, and the direction you pick determines what the
resulting run knows.

| Approach | System prompt comes from | The task is | Also loaded |
|---|---|---|---|
| Skill with `context: fork` | The agent type it forks into | The `SKILL.md` content | `CLAUDE.md`, except for Explore/Plan |
| Subagent with a `skills:` field | The subagent's own markdown body | Claude's delegation message | The preloaded skills, plus `CLAUDE.md` |

Read it as: **`context: fork` sends a procedure out to be executed in isolation. A `skills:`
field sends knowledge along with a delegated task.** One exports a procedure; the other
imports a convention.

```markdown
---
name: deep-research
description: Research a topic thoroughly and report back with file references
allowed-tools: Read, Grep, Glob
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly. Find the relevant files, read them, and
summarize your findings with specific file references.
```

The trap, and it is a quiet one: **`context: fork` only makes sense for a skill containing
explicit instructions.** Fork a skill that is purely guidelines — "prefer composition over
inheritance," "always parameterize queries" — and the forked context receives no actionable
prompt. It has a system prompt, a page of advice, and nothing to do. It returns nothing
useful, and it does so without erroring. If your skill contains no imperative sentences, it
is reference content, and reference content is not forkable.

---

## Where this framework sits

This repo's `.claude/agents/<name>.md` stubs are short on purpose, and the reason is now
stateable: that body **is** the subagent's system prompt, paid fresh on every launch into a
window that starts empty. Depth belongs in `.claude-library/agents/`, read on demand from
inside that window.

Same principle as skill length. Cost that recurs must be small; cost paid once may be large.

---

*Next: [02 — Skills](./02-skills.md) · [03 — Subagents](./03-subagents.md) ·
[Back to the index](./README.md)*
