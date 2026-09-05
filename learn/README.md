# Learn

How to decide where work goes in a Claude Code project — and when the answer is "nowhere new."

Most guidance about agent frameworks explains *how* to build an agent. The harder question,
and the one that costs the most when you get it wrong, is *whether you should*. These lessons
answer that first.

## Order

| # | Lesson | You will be able to |
|---|---|---|
| 01 | [The Four Surfaces](./01-four-surfaces.md) | Name the four places work can go, state what each costs, and pick one in ten seconds. **Start here.** |
| 02 | [Skills](./02-skills.md) | Write a correct skill in either form, and know which key controls who can invoke it |
| 03 | [Subagents](./03-subagents.md) | Predict what a subagent will and will not see before you delegate to it |
| 04 | [Composition](./04-composition.md) | Choose between forking a skill and preloading skills into a subagent |
| 05 | [Hooks and memory](./05-hooks-and-memory.md) | Separate "must always happen" from "should usually happen" |
| 06 | [Worked example](./06-worked-example.md) | Watch all four surfaces chosen on one real task, including two "neither" outcomes |

Reference: [frontmatter keys](./reference/frontmatter-keys.md) — the pinned, dated list of
every key that actually exists.

## If you only read one thing

A **hook** is the only surface the model cannot skip. A **skill's** content stays in context
for every turn after it loads, so length is a recurring cost. A **subagent** gets its own
context window and returns only a summary — which is why it is cheap for verbose work and
why it knows nothing about your conversation.

And most of the time, the right answer is none of them. See
[SIMPLICITY_ENFORCEMENT.md](../SIMPLICITY_ENFORCEMENT.md).
