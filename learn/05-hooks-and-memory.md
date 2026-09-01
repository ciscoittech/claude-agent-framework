# Hooks and Memory

*The difference between "should usually" and "must always."*

Prerequisite: [01 — The Four Surfaces](./01-four-surfaces.md).

This lesson is about *whether* to reach for a hook. For how to write one — the input
contract, the exit codes, the config shape — see
[the hooks README](../.claude-library/hooks/README.md).

## The only surface that is not a request

`CLAUDE.md`, skills, and delegation messages are all instructions. The model reads them and
tries to follow them. Bold text does not change that. Capital letters do not change that.
"NEVER" does not change that.

A hook is a program. It runs at a fixed lifecycle event regardless of what the model decided,
and it can refuse the tool call outright.

So the question is never "how strongly do I feel about this rule." It is: **name the case
where the model would be right to skip it.** If you cannot, and the cost of skipping is real,
it is a hook. If you can, it is instructions, and a hook will eventually fire on work where
it makes no sense and get disabled.

## What this framework learned the hard way

Two bugs from this repo's own history, both in `CHANGELOG.md`:

**The security hook approved everything.** Its config passed `"$command"` — a shell variable
the harness never sets — so the checker received an empty string and exited 0. Including on
`rm -rf /`. Payloads arrive as **JSON on stdin**, never as shell variables.

**Then the fix did not fix it.** `exit 1` does not block a `PreToolUse` hook; **`exit 2`
does.** The script printed a convincing block banner and the command ran anyway. The test
asserted "must be non-zero," which was simply the wrong criterion.

The lesson that generalizes past hooks: **a hook that never runs looks exactly like one that
always passes.** You cannot tell by reading it. Run it against a real payload and watch the
verdict change.

## `CLAUDE.md` versus a rule versus a skill

| You have | Put it in |
|---|---|
| A fact true on every turn, needed everywhere | `CLAUDE.md` |
| A convention that only applies to some files | `.claude/rules/` with a `paths:` field |
| A procedure with steps, started by name | A skill |
| A requirement that must hold regardless | A hook |

Path-scoped rules are the middle ground people miss. A rule file with a `paths:` field loads
only when Claude works with matching files, which keeps `CLAUDE.md` short without giving up
the instruction.

The field is **`paths`**. A rule with no `paths` field loads unconditionally and applies to
every file — so writing the wrong key does not error, it silently turns a scoped rule into a
global one. (This framework's own template had `globs:` here for a year.)

Target under 200 lines for `CLAUDE.md`. Longer files consume more context and reduce
adherence.

## Auto memory

Claude also keeps its own notes across sessions — your preferences, corrections you have
given, project context it cannot derive from the code. You do not write these; Claude does.

Two things worth knowing when reasoning about what a run can see: auto memory is
machine-local, and **the main conversation's auto memory is not loaded into subagents**. A
subagent knows the `CLAUDE.md` hierarchy but not what Claude learned about you.

---

*Next: [06 — Worked example](./06-worked-example.md) · [Back to the index](./README.md)*
