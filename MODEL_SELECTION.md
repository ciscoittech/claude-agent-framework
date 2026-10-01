# Model Selection
*Choosing model and effort for Claude Agent Framework agents*

## The Two Dials

Model and reasoning effort are **independent**. Conflating them is the most common
mistake, and it was baked into earlier versions of this framework.

- **Model** sets the capability floor: `haiku` → `sonnet` → `opus` → `fable`
- **Effort** sets reasoning depth: `low` → `medium` → `high` → `xhigh` → `max`

An Opus agent at `low` effort and a Haiku agent are different things. Picking a model does
not pick an effort; set both deliberately.

`xhigh` is the Claude Code default and the right setting for most coding and agentic work.

---

## Current Models

| Model | Tier name | Context | Input $/1M | Output $/1M | Cache read $/1M |
|---|---|---|---|---|---|
| Claude Haiku 4.5 | `haiku` | **200K** | $1.00 | $5.00 | ~$0.10 |
| Claude Sonnet 5.5 | `sonnet` | 1M | $2.00 | $10.00 | $0.20 |
| Claude Opus 5.5 | `opus` | 1M | $4.00 | $20.00 | $0.20 |
| Claude Fable 5.1 | `fable` | 1M | $10.00 | $50.00 | $0.25 |

The tier names are Claude Code aliases and resolve to the newest model in each tier, so an
agent declaring `model: opus` moved to Opus 5.5 on release with no edit. Verified
2026-09-30 on Claude Code 2.1.285: `opus` → `claude-opus-5-5`, `sonnet` →
`claude-sonnet-5-5`, `haiku` → `claude-haiku-4-5-20251001`. Only a full model ID pins a
version, which is why agents here never use one.

**Last verified: 2026-09-30** against the Anthropic price card (`/claude-api`, and
https://claude.com/pricing). Every rate above was checked, not just the arithmetic built on
it — a wrong rate makes every comparison in this file wrong in the same direction, and
nothing here updates itself. Re-verify before relying on it for a tier decision, and move
the date when you do.

Rates are Anthropic first-party API prices. Claude on Microsoft Foundry bills at the same
rates; Bedrock and Vertex are partner-operated and bill separately.

**Haiku is the only current model at 200K.** Everything else is 1M. This is the single
most consequential asymmetry in the table — a task that looks trivial ("rename this symbol
everywhere") can still be a long-context task, and haiku will truncate on it.

**Effort is not a dial on every model.** The levels available depend on the model:
`low` through `max` on Opus 5.5, Sonnet 5.5 and Fable 5.1, but the API rejects the effort
parameter outright on Haiku 4.5. Treat a haiku agent's effort declaration as unenforced —
if the reasoning depth matters, that is the signal to move up a model tier, which is why
the validator warns on haiku above `medium`.

**Opus 5.5 defaults to `medium` effort**, one level below its predecessor's `high`. An opus agent
with no declared effort therefore got shallower on the 5.5 release without any file
changing. This is the concrete reason every agent here declares `effort` explicitly.

**Fast mode** (`/fast`, Opus only) is the same model at up to 2.5x output speed, priced
at $8/$40 on Opus 5.5 — 2x standard Opus. It buys latency, not capability.

---

## Agent Tier Assignments

Declared in `.claude-library/REGISTRY.json` and mirrored into each subagent definition in
`.claude/agents/`. The registry is the source of truth; `test_v2_structure.py` fails if
the two drift.

| Agent | Model | Effort | Why |
|---|---|---|---|
| `framework-feature-builder` | opus | xhigh | Coordinates a multi-stage build; `fable` is opt-in |
| `framework-system-architect` | opus | xhigh | Design decisions with long-lived consequences |
| `framework-gap-analyzer` | opus | xhigh | Comparative judgment against a standard |
| `framework-senior-engineer` | opus | high | Implementation against a settled design |
| `framework-code-reviewer` | opus | high | Adversarial reading; missing a bug is the failure mode |
| `documentation-specialist` | sonnet | medium | Writing from material that already exists |
| `framework-validation-engineer` | sonnet | medium | Runs suites and reports; little open judgment |
| `best-practice-analyzer` | sonnet | medium | Extraction and structuring |
| `framework-best-practice-auditor` | sonnet | medium | Scoring against an explicit checklist |
| `framework-research-specialist` | sonnet | low | Fetch and summarize |

---

## Choosing a Tier

**Start from the work, not the budget.**

| The task is... | Model | Effort |
|---|---|---|
| Mechanical — file checks, formatting, renames in a small scope | haiku | low |
| Fetching, summarizing, extracting from a known source | sonnet | low–medium |
| Writing docs, running suites, structured output from settled input | sonnet | medium |
| Implementing against a clear design | opus | high |
| Reviewing, auditing, debugging — where being wrong is expensive | opus | high |
| Designing, deciding architecture, planning a change | opus | xhigh |
| Correctness outweighs cost — security, migrations, payments | opus | max |
| Multi-subsystem, long-horizon, already failed on opus | fable | xhigh |

**Adjust effort before model.** If work is coming out shallow, raise effort first; it is
usually the cheaper fix and often the actual problem. Only move up a model tier when a
higher effort on the current tier has genuinely failed.

**Do not downgrade to save tokens.** A cheaper tier that retries is not cheaper. Compare
cost *per completed task*, not cost per call.

---

## The Fable Escalation

Fable 5.1 is Anthropic's most capable widely released model, and it is an **opt-in
escalation, never a routing default**.

What escalating costs you:
- 2.5x Opus on both input and output ($10/$50 vs $4/$20)
- Thinking is always on and cannot be disabled
- Turns run substantially longer, so the real multiple on a full build exceeds 2.5x

When it is justified:
- Opus at `xhigh` has already failed on this specific task, or
- The work spans multiple subsystems and needs one coherent long-horizon plan

Before escalating, try in order:
1. **Tighten the request.** Most design failures are underspecified, not undermodeled.
2. **Narrow the scope** and do it in two passes.
3. *Then* escalate.

Invoke it explicitly:

```bash
/build-feature registry-v3 --model fable
```

### Escalation never propagates

**A coordinator's model applies to the coordinator alone.** Every sub-agent it launches
runs at that sub-agent's own registry tier, passed explicitly at launch.

This is the rule with real money behind it. A Fable coordinator is 2.5x on one agent. A Fable
coordinator that leaks its tier into six sub-agents is 2.5x on an entire workflow — and buys
nothing, because those sub-agents are doing bounded, well-specified work that opus and
sonnet already handle.

Claude Code supports `model: inherit` in agent frontmatter. **This framework deliberately
does not use it.** Every agent declares its own tier.

---

## Cost Levers, In Order

Earlier levers dominate later ones. Reach for them in this order.

### 1. Effort tuning

The largest single lever, and independent of model. Lower effort produces fewer and more
consolidated tool calls, less preamble, terser output. Most agents do not need `xhigh`.

### 2. Prompt caching

Cached reads bill at a tenth of fresh input or less (Opus 5.5: a twentieth); **cache writes bill at about 1.25x**.
That asymmetry is the whole game. A prefix that caches and is read many times is close to
free after the first call; a prefix that is written every run and never hit costs 25% more
than not caching at all. Measure `cache_read_input_tokens` rather than assuming.

Caching is a **prefix match** — any byte change anywhere in the prefix invalidates
everything after it.

Assemble every agent prompt stable-first:

```
persona → pinned contexts → volatile task
```

Selecting a different context set per task produces a different prefix on every run and a
near-zero hit rate. **A larger stable context that caches beats a smaller one rebuilt each
call.** This is a real tension with lazy loading: lazy loading minimizes bytes resident,
caching rewards those bytes staying identical. For an agent that runs repeatedly, favor a
fixed bundle.

Silent invalidators worth auditing for: timestamps or run IDs in the persona, unsorted
JSON, a tool list whose order varies between runs.

### 3. Model tier

Choose the lowest tier that clears the capability bar, then stop.

### Not a lever here: the Batch API

Batch processing runs asynchronously at 50% of standard rates, which makes it the largest
discount on this page — and it does not apply to anything in this framework. Agents run
interactively through Claude Code, which is a synchronous surface. It is worth knowing
about for offline work you build *with* the API, not for tiering the agents in it.

---

## Measuring

There is no built-in cost tracking in the framework — the observability subsystem was
retired to `archive/v2-observability/`. Measure from the source that bills you:

- **Claude Code** — `/cost` for the current session.
- **Anthropic Console** — usage by model over time, which is the authoritative record.

When comparing two tier assignments, compare **cost per completed task**, not cost per
call. A cheaper tier that needs a second attempt is not cheaper, and per-call cost hides
that entirely. If you want this automated, the archived subsystem did exactly this —
see `archive/v2-observability/`.

## Related

- `.claude-library/contexts/performance-optimization.md` — budgets and targets
- `.claude-library/contexts/framework-architecture.md` — where tiers are declared
- `.claude/commands/launch-agent.md` — the routing table that applies these tiers

---

*Model Selection v2.1 | Claude Agent Framework*
