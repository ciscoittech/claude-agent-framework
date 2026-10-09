# Claude Agent Framework

### Turn a project into a working team of Claude Code subagents

[![Framework Version](https://img.shields.io/badge/version-2.2-blue)]()
[![Setup Time](https://img.shields.io/badge/setup-2%20minutes-green)]()
[![Checks](https://img.shields.io/badge/checks-run__checks.py-orange)]()

---

## What this is

A generator and a contract. Point it at your project and it writes a `.claude/` and
`.claude-library/` pair configured for your stack: subagents with declared model and
effort tiers, commands that orchestrate them, and a registry the framework's own
validator holds to a contract.

The generator is a prompt, not a program. What makes the output trustworthy is not the
prompt — it is that the result is validated, and that the same checks run against this
repository's own documentation, so the examples cannot drift from the contract they teach.

---

## Two things people get wrong

Read these before anything else. Both fail silently, which is why they are here and not
further down.

**1. Model and effort are two independent dials.**

`model` sets the capability floor — `haiku` → `sonnet` → `opus` → `fable`.
`effort` sets reasoning depth — `low` → `medium` → `high` → `xhigh` → `max`.

An Opus agent at `low` effort and a Haiku agent are different things. Declare both, in
`.claude/agents/<name>.md` frontmatter *and* in `REGISTRY.json` — they must agree, or the
tier is prose that nothing enforces. See [MODEL_SELECTION.md](./MODEL_SELECTION.md).

**2. Hooks go in `.claude/settings.json`. Never `REGISTRY.json`.**

Claude Code does not read `REGISTRY.json` — that is framework metadata, for the validator
and the generator. A hook declared there never fires, and a hook that never fires looks
exactly like one that always passes. This framework shipped a security hook that approved
every command for precisely that reason.

A hook also receives its payload as **JSON on stdin**, never as shell variables. A command
written `script.sh "$file_path"` passes an empty string.

---

## Which surface?

Before building anything, decide where the work actually goes. Ask these in order and take
the first "yes":

1. **Must this happen every time, even if the model is convinced otherwise?** → **Hook**
2. **A short fact, true on every turn?** → **`CLAUDE.md`**
3. **Would it flood your context with output you'll never read again?** → **Subagent**
4. **A procedure with known steps, started by name?** → **Skill**
5. **None of the above?** → **Neither.** Type the command.

Step 5 is the most common correct answer. A skill that wraps one tool call is worse than the
tool call.

Full reasoning, the cost model behind it, and a worked example:
**[learn/01-four-surfaces.md](./learn/01-four-surfaces.md)**.

---

## Setup

```bash
# In your project directory
$ claude

> Read SYSTEM_GENERATOR_PROMPT.md from ./claude-agent-framework/
  and generate my agent system.
```

Generation is not the end of it. Three things follow, in this order:

**1. Validate.** The generator's last step, and yours if you are checking its work:

```bash
python3 /path/to/claude-agent-framework/validate_agent_system.py .
```

It resolves every declared path and context, checks that each agent's frontmatter agrees
with its registry entry, and rejects wildcard tool grants. A system that does not validate
does not load correctly — do not skip this because the files look right.

**2. Read `GETTING_STARTED.md`.** The generator writes it into your project root,
describing the system it actually built: which agents you got, what tier each runs at and
why, how to launch one by `subagent_type`, and how to add the next one.

**3. Add only what you need.** You start with one command. A test command when there are
tests to run, a deploy command when there is something to deploy. See
[SIMPLICITY_ENFORCEMENT.md](./SIMPLICITY_ENFORCEMENT.md) — complexity is earned.

---

## What gets built

```
your-project/
├── GETTING_STARTED.md          # What was created, and how to verify it
├── .claude/                    # Auto-loaded every session - keep it lean
│   ├── settings.json          # Hooks and permissions. The file the harness reads
│   ├── agents/                # Subagent definitions: frontmatter + short persona
│   │   ├── architect.md      # model + effort declared here, or nowhere
│   │   ├── engineer.md
│   │   └── reviewer.md
│   └── commands/              # Invoked as /name
│       └── build.md          # Start with one; earn the rest
│
└── .claude-library/           # Read on demand - size is not a constraint here
    ├── REGISTRY.json         # Source of truth for tiers and wiring
    ├── agents/               # Full playbooks - depth lives here
    ├── contexts/             # Project knowledge
    └── hooks/                # Optional deterministic control
```

**Agents live in two places on purpose.** The `.claude/agents/` stub is the real subagent
definition — its body becomes that agent's system prompt and is paid on every launch, so
it stays short. The playbook in `.claude-library/agents/` is read only when needed.

---

## Documentation

| Document | Purpose | When to read |
|---|---|---|
| [learn/](./learn/README.md) | Which surface work belongs on, and when the answer is "neither" | Before anything else |
| [SIMPLICITY_ENFORCEMENT.md](./SIMPLICITY_ENFORCEMENT.md) | Circuit breakers against over-engineering | First |
| [SYSTEM_GENERATOR_PROMPT.md](./SYSTEM_GENERATOR_PROMPT.md) | Generate a system (§4.6b is the normative contract) | Start here |
| [MODEL_SELECTION.md](./MODEL_SELECTION.md) | Model and effort tiers, rates, cost levers | Choosing a tier |
| [CLAUDE_AGENT_FRAMEWORK.md](./CLAUDE_AGENT_FRAMEWORK.md) | Architecture and principles | Understanding it |
| [AGENT_PATTERNS.md](./AGENT_PATTERNS.md) | Implementation patterns | Optimizing |
| [AGENT_SYSTEM_TEMPLATE.md](./AGENT_SYSTEM_TEMPLATE.md) | Manual setup, step by step | Building by hand |
| [hooks/README.md](./.claude-library/hooks/README.md) | Hook configuration and the input contract | Adding a hook |
| [CHANGELOG.md](./CHANGELOG.md) | What changed and why | After an upgrade |

---

## Checks

```bash
python3 run_checks.py          # everything, ~1.5 seconds
```

| Suite | What it proves |
|---|---|
| `test_v2_structure.py` | Structure, and that the docs' own examples satisfy the contract those docs state |
| `test_generated_system.py` | A system built to the contract validates; every documented deviation is caught; every registry example in the docs can actually be built |
| `test_learning_docs.py` | Every frontmatter example in the docs satisfies the validator's own predicates; the decision material stays linked |
| `test_hooks.py` | The hook scripts, executed against real payloads |

These run in CI on every push and pull request, and on edit via a `PostToolUse` hook.

**A check counts only once it has been seen to fail.** Every one here was run against a
deliberately broken version first. Two of this framework's worst bugs — a security hook
that approved everything, and its first fix, which printed a block banner and let the
command run anyway — shipped green under tests that never exercised the real path.

---

## Your stack

The generator reads your project rather than matching it against a list, so it adapts to
whatever is there — React or Rails, Postgres or SQLite, pytest or Vitest. What it produces
is shaped by your `CLAUDE.md`, your directory layout, and the patterns already in your
code.

---

## What's new

**2.2** — Rewrote the hooks context, which documented an API that does not exist and was
loaded by three agents as official documentation. Anchored every hook path with
`$CLAUDE_PROJECT_DIR`; relative paths broke whenever a session started in a subdirectory.
Fixed the framework documents that contradicted the generator contract, and added checks
so they cannot drift back. Added the generated-system and hook-execution suites, plus CI.
Verified the rate table against the price card and pinned it.

**2.1** — Model and effort separated into two independent dials. Real subagent definitions
in `.claude/agents/` with enforced frontmatter. Hooks moved to `.claude/settings.json` and
made to actually fire. Commands became real skills with frontmatter.
`validate_agent_system.py` extracted so it runs against any generated system.

Full detail in [CHANGELOG.md](./CHANGELOG.md).

---

## A note on context size

Earlier versions of this README led with "97% smaller context (250KB → 8KB)". That was the
right optimization when context was scarce and every token billed fresh. It is no longer
the metric that matters most: current models other than Haiku have a 1M window, and cached
reads bill at a tenth of fresh input or less.

Minimizing bytes and maximizing cache hits pull in opposite directions. A context set
assembled fresh per task is small but never caches; for an agent that runs repeatedly, a
larger *stable* bundle costs less than a smaller one rebuilt each call. `.claude/` stays
lean because it loads on every session. Beyond that, optimize for prefix stability.

---

## Contributing

- **Patterns** — add to `AGENT_PATTERNS.md`, with the failure mode it avoids
- **Fixes** — every change runs `python3 run_checks.py`; a new check must be shown to fail
  against the bug it catches before it counts
- **Issues** — [report what broke](https://github.com/ciscoittech/claude-agent-framework/issues)

## License

MIT.

---

*Claude Agent Framework v2.2*
