# Claude Code Hooks Context

**Source**: https://code.claude.com/docs/en/hooks (reference), https://code.claude.com/docs/en/hooks-guide (guide)
**Purpose**: What Claude Code's hook system actually accepts and honors
**Auto-update**: `/update-docs`, or WebFetch the two URLs above

---

## Read this first

Hooks are the one place in this framework where being approximately right is
indistinguishable from being wrong. A hook with an invented config key does not
error - it never runs. A hook that reads a field the payload does not contain
gets `None` and approves whatever it was meant to stop. Every hook bug in this
repo's history had that shape, and none was visible by reading the script.

Three facts do most of the work:

1. **Hooks live in `.claude/settings.json`.** Claude Code does not read
   `REGISTRY.json` - that is framework metadata. A hook declared there is inert.
2. **A hook receives its payload as JSON on stdin.** Not argv, not environment
   variables. `script.sh "$file_path"` passes an empty string, because
   `$file_path` is not a variable anything sets.
3. **On `PreToolUse`, exit 2 blocks. Exit 1 does not.** Exit 1 is a non-blocking
   error: the transcript shows a hook-error notice and the tool call proceeds.

---

## Configuration

### Where hooks are declared

| Location | Scope | Shared |
|---|---|---|
| `.claude/settings.json` | this project | yes, committed |
| `.claude/settings.local.json` | this project | no, gitignored |
| `~/.claude/settings.json` | all your projects | no |
| Managed policy settings | organization | admin-controlled |
| Plugin `hooks/hooks.json` | while the plugin is enabled | yes |
| Skill / subagent frontmatter | while that skill or subagent is active | yes |

### Schema

Three levels of nesting: **event → matcher group → handlers.**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude-library/hooks/scripts/security_check.py",
            "timeout": 30,
            "statusMessage": "Checking command safety..."
          }
        ]
      }
    ]
  }
}
```

| Field | Meaning |
|---|---|
| `matcher` | Which tool the event applies to. Tool-name regex on tool events (`Bash`, `Edit\|Write`, `mcp__.*`). Omitted or empty = every occurrence of the event |
| `type` | `command` (shell), `prompt` (a model decides), or `agent` (a subagent verifies) |
| `command` | What runs. Shell form by default |
| `args` | Present = **exec form**: `command` is spawned directly with this argument vector, no shell. Use it to sidestep quoting entirely |
| `timeout` | Seconds |
| `statusMessage` | Shown in the UI while the hook runs |
| `if` | Permission-rule filter, e.g. `"Bash(git *)"`, `"Edit(*.ts)"`. **Tool events only** - on any other event a hook with `if` set never runs |

### Reference scripts by path, not by luck

Handlers run in the current directory, which is not necessarily the project
root - start Claude Code from a subdirectory and every relative hook path breaks
with `command not found`. Anchor them:

```json
"command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude-library/hooks/scripts/check_structure.sh"
```

`CLAUDE_PROJECT_DIR` is the project root where the session started, exported into
the hook's environment. Quote it - project paths contain spaces.

---

## Events

Claude Code fires far more events than a project normally needs. The ones this
framework uses or is likely to:

| Event | When it fires | Can block? |
|---|---|---|
| `SessionStart` | session begins or resumes | no |
| `UserPromptSubmit` | you submit a prompt, before Claude sees it | **yes** |
| `PreToolUse` | before a tool call executes | **yes** |
| `PostToolUse` | after a tool call succeeds | no |
| `PostToolUseFailure` | after a tool call fails | no |
| `PermissionRequest` | a tool call needs a permission decision | via decision object |
| `SubagentStart` / `SubagentStop` | a subagent is spawned / finishes | stop: **yes** |
| `Stop` | Claude finishes responding | **yes** |
| `PreCompact` / `PostCompact` | around context compaction | no |
| `SessionEnd` | session ends | no |

Also available: `Setup`, `UserPromptExpansion`, `PermissionDenied`,
`PostToolBatch`, `Notification`, `MessageDisplay`, `TaskCreated`,
`TaskCompleted`, `StopFailure`, `TeammateIdle`, `InstructionsLoaded`,
`ConfigChange`, `CwdChanged`, `DirectoryAdded`, `FileChanged`,
`WorktreeCreate`, `WorktreeRemove`, `PreModelSwitch`, `PostModelSwitch`,
`Elicitation`, `ElicitationResult`.

**There is no `PrePrompt` or `PostPrompt`.** An earlier version of this file
listed both. A hook registered under a name Claude Code does not recognize is
not an error - it simply never fires.

---

## Input contract

The payload arrives as one JSON object on stdin. Common fields on every event:

```json
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse"
}
```

Tool events (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`,
`PermissionRequest`, `PermissionDenied`) add:

```json
{
  "tool_name": "Bash",
  "tool_use_id": "toolu_01ABC123...",
  "tool_input": { "command": "npm test", "description": "Run test suite" },
  "tool_response": "output text here"
}
```

Note the shape: **`tool_name` and `tool_input`, flat, at the top level.** Not
`tool.name`, not `tool.parameters`, not `result.usage`. Reading a field that is
not there yields `None`, and a check against `None` passes.

Selected event-specific fields:

| Event | Adds |
|---|---|
| `SessionStart` | `session_start_reason` (`startup\|resume\|clear\|compact\|fork`), `model` |
| `UserPromptSubmit` | `user_prompt` |
| `Stop` / `SubagentStop` | `last_assistant_message` |
| `SessionEnd` | `session_end_reason` |
| `FileChanged` | `file_path` |

Inside a subagent the payload also carries `agent_id` and `agent_type`.

### Reading it

```bash
# bash
file_path=$(jq -r '.tool_input.file_path // .tool_response.filePath // empty')
[ -n "$file_path" ] || exit 0
```

```python
# python
import json, sys
payload = json.load(sys.stdin)
command = payload.get("tool_input", {}).get("command", "")
```

Never let an empty payload read as "nothing to object to". Decide explicitly
what an unreadable payload means, and make that decision visible in the code.

---

## Output contract

### Exit codes

| Code | Effect |
|---|---|
| `0` | Success. stdout goes to the debug log only - **except** on `UserPromptSubmit`, `UserPromptExpansion`, `SessionStart` and `PostModelSwitch`, where plain-text stdout is added to Claude's context |
| `2` | Blocking error. On an event that can block, exit 2 blocks whether or not you print JSON - it overrides even `"permissionDecision": "allow"`. The message shown is the reason from your JSON decision, or your stderr |
| other | **Non-blocking.** The action proceeds and the transcript shows a hook-error notice. If stdout is valid JSON, the JSON alone decides the outcome |

`PostToolUse` cannot block - the tool already ran. `WorktreeCreate` is the
exception to the table: any non-zero exit aborts it.

### JSON on stdout

Universal fields, any event:

```json
{
  "systemMessage": "Text Claude will see as context",
  "suppressOutput": false,
  "terminalSequence": "]9;4;1;desktop-notification"
}
```

**`PreToolUse` and the other permission events** use the standard decision model:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook",
    "additionalContext": "Information for Claude that does not block",
    "updatedInput": { "command": "safer command" }
  }
}
```

`permissionDecision` is `allow`, `deny`, or `review` (forces review, not
auto-approval). When several hooks answer, the most restrictive wins:
`deny` > `defer` > `ask` > `allow`. `additionalContext` from every hook is kept.

**`PostToolUse` and `Stop` use a different shape** - a top-level `decision`:

```json
{ "decision": "block", "reason": "Tests failed:\n\n..." }
```

`PermissionRequest` uses a third shape, `hookSpecificOutput.decision.behavior`.
Check the reference per event rather than assuming one form generalizes.

`additionalContext` must be nested inside `hookSpecificOutput`. Placed at the top
level it is silently ignored.

---

## Worked example: block destructive commands

`.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude-library/hooks/scripts/security_check.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

The script - see `.claude-library/hooks/scripts/security_check.py` for the
shipped version:

```python
#!/usr/bin/env python3
import json, re, sys

payload = json.load(sys.stdin)
command = payload.get("tool_input", {}).get("command", "")

if re.search(r"rm\s+-rf\s+/", command):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Destructive command blocked by hook",
        }
    }))
    sys.exit(2)          # 2 blocks. 1 would print this and run the command anyway.

sys.exit(0)              # no decision; the normal permission flow applies
```

---

## Model-backed hooks

For decisions that need judgment rather than a regex, a handler can be
`type: "prompt"` (one model call, Haiku by default, `model` overridable) or
`type: "agent"` (a subagent that can read files and run commands before
deciding). Both answer with `{"ok": bool, "reason": str}`.

On `PostToolUse`, a prompt hook's `ok: false` ends the turn with the reason as a
warning by default; `continueOnBlock: true` feeds the reason back and continues.
Agent hooks behave as if `continueOnBlock` were set.

Use a prompt hook when the payload alone is enough to decide, and an agent hook
when the decision depends on the state of the codebase.

---

## What this framework ships

| Script | Event | Behavior |
|---|---|---|
| `check_structure.sh` | PostToolUse, `Write\|Edit` | Runs `test_v2_structure.py` after edits under `.claude/` or `.claude-library/`; reports failures with `decision: block`. **Wired live** |
| `security_check.py` | PreToolUse, `Bash` | Denies destructive commands; exit 2 |
| `run_tests.sh` | PostToolUse, `Write\|Edit` | Runs the relevant suite; reports a red suite with `decision: block` |
| `format_code.sh` | PostToolUse, `Write\|Edit` | Formats the edited file; never blocks |
| `track_timing.sh` | Pre/PostToolUse, `Agent` | Millisecond timing per subagent |
| `validate_agent_output.py` | SubagentStop | Checks subagent output shape |
| `notify_team.sh` | Stop, SessionStart | Slack/Discord webhook, if configured |

The subagent tool is named **`Agent`**. `Task` is its former name; a matcher
still written as `Task` matches nothing.

Ready-made configs to copy into `.claude/settings.json` live in
`.claude-library/hooks/configs/`. They are examples, not live configuration -
only `.claude/settings.json` is read.

`test_hooks.py` at the repo root executes each of these against real payloads.
Anything added here should be added there, and the new check must be confirmed
to fail against the broken version before it counts.

---

## Troubleshooting

**The hook never runs.** Check it is in `.claude/settings.json`, not
`REGISTRY.json`. Check the event name against the table above. Check the matcher
- an event with `if` set on a non-tool event never fires. Check the path: if the
session started from a subdirectory, a relative command is not found. Run with
`claude --debug` to see hook resolution.

**The hook runs but its JSON has no effect.** Shell-form hooks are spawned with
`sh -c`, and some shell profiles print on startup. Anything printed before your
JSON means stdout no longer begins with `{`, so it is treated as plain text and
the decision is dropped silently. Guard profile output with
`if [[ $- == *i* ]]; then ... fi`, or use exec form (`"args": []`).

**The hook says it blocked but the command ran.** It exited 1. Only exit 2
blocks, and only on an event that can block.

**The hook is slow.** `timeout` is in seconds. Anything on `PreToolUse` runs
before every matching call - keep it in the tens of milliseconds.

---

**Last Updated**: August 31, 2026
**Update Method**: `/update-docs`, or WebFetch the source URLs at the top
