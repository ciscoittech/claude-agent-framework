# Worked Example

*One task, all four surfaces, and two things deliberately not built.*

No new concepts here. Every decision cites the lesson that produced it.

## The situation

A service stores orders in Postgres. Migrations live in `migrations/`, named
`NNNN_verb_noun.sql`. Every migration must be reversible. A migration that has merged is
never edited. Before writing one, someone should check what the schema already has.

Four people keep getting this wrong in four different ways. What should be built?

---

## 1. `CLAUDE.md` — the naming convention

```text
Migrations live in `migrations/`, named `NNNN_verb_noun.sql` (e.g. `0042_add_order_status.sql`).
Every migration needs a matching DOWN section. Run them with `make migrate`.
```

Three sentences. **Ladder step 2** — a short fact, true on every turn, that you want applied
without anyone asking.

Not a skill: a skill only applies when invoked, and a naming convention that applies 10% of
the time is worse than useless, because the other 90% produces inconsistent names that look
deliberate.

## 2. A skill — `writing-a-migration`

Reversibility patterns, the `ALTER TABLE` locking gotchas, how the team writes a `DOWN`.

```markdown
---
name: writing-a-migration
description: Patterns for writing a reversible Postgres migration, including locking gotchas and DOWN sections
allowed-tools: Read, Grep, Glob
---

When writing a migration:
- Every UP has a matching DOWN. If the DOWN is impossible, say so in a comment and explain why.
- `ALTER TABLE ... ADD COLUMN` with a default rewrites the table. Add nullable, backfill, then set the default.
- Never `DROP COLUMN` in the same migration that stops writing to it. Two deploys.
```

**Ladder step 4.** Known steps, pulled in by name.

No `disable-model-invocation` — you *want* this loading automatically when the topic comes up
([02](./02-skills.md)).

And explicitly **not** `context: fork`. Read the body: it is three guidelines and no
imperative task. Fork it and the subagent gets a system prompt, three bullet points, and
nothing to do. It returns nothing and does not error — the empty fork from
[04](./04-composition.md).

## 3. A subagent — `schema-auditor`

Before writing anything: read the current schema, the last forty migrations, and the column
definitions for the touched tables.

```markdown
---
name: schema-auditor
description: Report what the orders schema already contains before a migration is written
model: haiku
effort: low
tools: Read, Grep, Glob
---

Report on the current state of the schema for the tables named in the request.
Return a short summary: what exists, what was recently changed, and anything that
would conflict. Do not return raw DDL.
```

**Ladder step 3.** Hundreds of lines of DDL in, one paragraph out:

> `orders.status` is already indexed. The enum has six values. Migration 0039 renamed
> `placed_at` to `created_at`.

Two independent reasons, and either alone would justify it: the output is verbose and
disposable, and `tools` is a real restriction, unlike a skill's `allowed-tools`
([03](./03-subagents.md)).

### The delegation that fails

This is the failure from [01](./01-four-surfaces.md), concretely.

Six turns of conversation established that the new column must be nullable, because an older
client still writes to this table and would break on a `NOT NULL`. Then:

> ❌ "Add the migration for the new `fulfillment_channel` column."

Back comes a `NOT NULL` column with a default. The subagent was not wrong. It was not there —
it receives none of your conversation history.

> ✅ "Add a migration adding `fulfillment_channel` to `orders`. It must be **nullable** — an
> older client still writes to this table and would break on NOT NULL. Include a DOWN.
> Return the SQL only."

## 4. A hook — merged migrations are immutable

`PreToolUse` on `Edit|Write`, matching `migrations/*.sql`, blocking any file already reachable
from `origin/main`.

**Ladder step 1**, and the cleanest test of the whole ladder. Apply the question from
[05](./05-hooks-and-memory.md): *name the case where the model would be right to skip this.*

There isn't one. And a model told this rule four hundred times can still be talked out of it
by a user saying "just fix it quickly, I'll squash the commits." A rule that survives only
while the model agrees is not a rule.

Payload as JSON on stdin, `exit 2` to block. See
[the hooks README](../.claude-library/hooks/README.md).

---

## 5. Neither — the wrapped command

The team also wants "run this migration against a scratch DB and diff the schema." Tempting
to build `/verify-migration`.

It is one line:

```bash
psql -f migrations/0042_add_status.sql scratch && pg_dump --schema-only scratch | diff -u baseline.sql -
```

Wrapping it buys a file, a registry entry, a description that must stay in sync with the
command, and a permanent line of invocation-time context — to save typing something run twice
a month.

**Type the command.** Run it weekly for a month and it has earned a skill. This is the
three-strike rule in [SIMPLICITY_ENFORCEMENT.md](../SIMPLICITY_ENFORCEMENT.md).

## 6. Neither — the wrapped tool call

Someone proposes a `migration-namer` agent to pick the next `NNNN` prefix.

That is `ls migrations | tail -1`. An agent is a role that exercises judgment; there is no
judgment here.

---

## The tally

| # | Decision | Surface | Ladder step |
|---|---|---|---|
| 1 | Naming convention and location | `CLAUDE.md` | 2 |
| 2 | Reversibility patterns | Skill | 4 |
| 3 | Pre-write schema audit | Subagent | 3 |
| 4 | Merged migrations immutable | Hook | 1 |
| 5 | Verify against scratch DB | **Neither** | 5 |
| 6 | Pick the next number | **Neither** | 5 |

Four surfaces used, two proposals rejected, one command still typed by hand. That ratio is
the honest one, and it is the reason to trust the rest.

---

*[Back to the index](./README.md)*
