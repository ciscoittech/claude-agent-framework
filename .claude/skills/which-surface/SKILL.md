---
name: which-surface
description: Decide whether a piece of work belongs in a skill, a subagent, a hook, CLAUDE.md, or none of them
argument-hint: [what you want to make repeatable]
allowed-tools: Read, Grep, Glob
---

Decide where a piece of work belongs. Most of the time the answer is "nowhere new."

Deliberately model-invocable: the moment this is useful is when someone asks
"should I make an agent for this?", which means the description has to be in
context to be matched. Contrast `/build-feature`, which sets
`disable-model-invocation: true` because firing it spawns agents.

## Ask in order. Take the first yes.

1. **Must this happen every time, even if the model is convinced otherwise?**
   → **Hook**, in `.claude/settings.json`.
2. **A short fact, true on every turn, wanted without anyone asking?**
   → **`CLAUDE.md`**. If it only applies to some files, a `.claude/rules/`
   file with a `paths:` field.
3. **Would doing this flood the conversation with output nobody rereads?**
   → **Subagent**.
4. **A procedure with known steps, started by name?**
   → **Skill**.
5. **None of the above?** → **Neither.**

## Then confirm the answer

Do not skip this. Each surface has one question that catches the common mistake:

- **Hook** — name the case where the model would be *right* to skip it. If you
  can, it is instructions, not a hook, and a hook here will fire on work where
  it makes no sense until someone disables it.
- **`CLAUDE.md`** — is it under three lines? If not, it is a rule or a skill.
- **Subagent** — write the delegation message now. It receives none of this
  conversation. If the message is getting long, the work is entangled: do it
  inline instead.
- **Skill** — will the body stay under ~150 lines? It sits in context for every
  turn after it loads. And if it is pure guidelines, do not add `context: fork`;
  a forked skill with no imperative task returns nothing and does not error.
- **Neither** — have you actually done this three times? Twice is a coincidence.

## Report

State: the surface, the ladder step that produced it, the exact file path to
create, and the one confirm-check it had to survive. If the answer is "neither",
say what to type instead.

Full reasoning: `learn/01-four-surfaces.md`. Cost model, the two-direction
composition table, and a worked example with two "neither" outcomes.
Details on any single key: `learn/reference/frontmatter-keys.md`.
