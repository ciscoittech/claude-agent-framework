# Frontmatter Keys

Every key that actually exists, and nothing else. If a key is not on these lists, the harness
does not read it — and a key the harness does not read fails silently, which is the most
expensive kind of mistake in this framework.

**Last verified: 2026-09-01** against `code.claude.com/docs/en/skills` and
`code.claude.com/docs/en/sub-agents`. `test_learning_docs.py` pins these lists and fails if
this document drifts from them. Re-verify before relying on it, and move the date when you do.

## Skills — `.claude/skills/<name>/SKILL.md` or `.claude/commands/<name>.md`

| Key | What it does |
|---|---|
| `name` | Display name. Defaults to the directory name |
| `description` | What it does and when to use it. Claude matches on this |
| `when_to_use` | Extra trigger context, appended to `description` |
| `argument-hint` | Autocomplete hint, e.g. `[issue-number]` |
| `arguments` | Named positional arguments for `$name` substitution |
| `disable-model-invocation` | `true` = only you can invoke; description leaves context |
| `user-invocable` | `false` = only Claude can invoke |
| `allowed-tools` | Tools pre-approved for the invoking turn. **Pre-approves, does not restrict** |
| `disallowed-tools` | Tools removed while the skill is active |
| `model` | Model while the skill is active |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max` |
| `context` | `fork` to run in a forked subagent |
| `agent` | Which subagent type to fork into |
| `background` | With `context: fork`, `false` waits for the result |
| `hooks` | Hooks registered when the skill is invoked |
| `paths` | Globs limiting when the skill auto-activates |
| `shell` | `bash` (default) or `powershell` |
| `metadata` | Free-form map for your own tooling |
| `license`, `compatibility` | Agent Skills spec fields; accepted, not acted on |

## Subagents — `.claude/agents/<name>.md`

| Key | What it does |
|---|---|
| `name` | Required. Lowercase and hyphens; no `:` |
| `description` | Required. When Claude should delegate here |
| `tools` | Tools it may use. **A real restriction.** Omitted = inherits all |
| `disallowedTools` | Tools denied |
| `model` | `sonnet`, `opus`, `haiku`, `fable`, a full ID, or `inherit` |
| `permissionMode` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`, `manual` |
| `maxTurns` | Turn cap before it stops and returns partial output |
| `skills` | Skills preloaded in full at startup |
| `mcpServers` | MCP servers available to it |
| `hooks` | Lifecycle hooks scoped to this subagent |
| `memory` | `user`, `project`, or `local` — persistent memory scope |
| `background` | `true` keeps it in the background |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max` |
| `isolation` | `worktree` runs it in a temporary git worktree |
| `color` | `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| `initialPrompt` | Auto-submitted first turn when run as the main session agent |
| `experimental` | Map of experimental options |

## Two spellings that are not interchangeable

- Skill frontmatter: **`allowed-tools`** (hyphen). This framework's `REGISTRY.json`:
  **`allowed_tools`** (underscore). Same values, different key, and they must match.
- Path scoping in `.claude/rules/`: **`paths`**, never `globs`. `globs` is Cursor's spelling.

## Effort is not available on every model

`low` through `max` on Opus 5.5, Sonnet 5.5, and Fable 5.1. The API rejects the effort parameter on
Haiku 4.5 — treat a haiku agent's effort declaration as unenforced.
