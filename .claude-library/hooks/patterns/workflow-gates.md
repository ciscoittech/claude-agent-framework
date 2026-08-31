# Workflow Quality Gates Pattern

**Pattern Type:** Hooks Integration
**Complexity:** Low
**Use Case:** Enforce quality standards automatically

## Overview

Quality gates ensure code meets standards before proceeding to next workflow stage. Hooks provide automatic, deterministic enforcement without agent intervention.

**Two rules every example below depends on:**

1. **A hook receives its payload as JSON on stdin, never as shell variables.** A
   command written `script.sh "$file_path"` passes an empty string - `$file_path`
   is not a variable the harness defines. Read the path with
   `jq -r '.tool_input.file_path // empty'`. See README.md § Hook Input Contract.
2. **On `PreToolUse`, exit 2 blocks the tool call; exit 1 does not.** A gate that
   prints a refusal and exits 1 lets the command run anyway.

## Pattern: Auto-Format After Every Change

### Implementation

**Hook Configuration:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude-library/hooks/scripts/format_code.sh"
          }
        ]
      }
    ]
  }
}
```

**Workflow:**
```
Agent writes code → File saved → Hook triggers → Code auto-formatted → Continue
```

### Benefits
- ✅ Consistent code style across all agents
- ✅ No manual formatting needed
- ✅ Works with any formatter (black, prettier, rustfmt, etc.)
- ✅ Never blocks workflow (PostToolUse)

## Pattern: Test Before Proceeding

### Implementation

**Hook Configuration:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude-library/hooks/scripts/run_tests.sh"
          }
        ]
      }
    ]
  }
}
```

**Workflow:**
```
Agent creates file → Tests run automatically → Results logged → Continue
```

### Benefits
- ✅ Immediate feedback on code quality
- ✅ Catch regressions early
- ✅ Works with any test framework
- ✅ Logs results for review

## Pattern: Security Gate (Blocking)

### Implementation

**Hook Configuration:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$CLAUDE_PROJECT_DIR\"/.claude-library/hooks/scripts/security_check.py"
          }
        ]
      }
    ]
  }
}
```

**Workflow:**
```
Agent attempts bash command → Security check → Pass ✅ or Block 🚫
```

### Benefits
- ✅ Prevents dangerous operations
- ✅ Audit trail of all bash commands
- ✅ Blocks before execution (PreToolUse)
- ✅ Customizable security rules

## Pattern: Multi-Stage Validation

### Implementation

**Hook Configuration:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude-library/hooks/scripts/format_code.sh"
          },
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude-library/hooks/scripts/run_tests.sh"
          }
        ]
      }
    ]
  }
}
```

**Workflow:**
```
File written → Format → Lint → Test → Continue
```

### Benefits
- ✅ Comprehensive quality checks
- ✅ Runs in sequence automatically
- ✅ All results logged
- ✅ Catches multiple issue types

## Pattern: Workflow-Specific Gates

**Hooks are not declared per command.** There is no `commands.<name>.hooks` block
that Claude Code reads - every hook lives in `.claude/settings.json` and applies
to the whole session. Scope it with the `matcher` (which tool fired) and with
logic inside the script (which file, which branch, which environment), not by
attaching it to a command.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 scripts/pre_deploy_check.py"
          }
        ]
      }
    ]
  }
}
```

The gate decides for itself whether this invocation is one it cares about:

```python
# scripts/pre_deploy_check.py - runs on every Bash call, acts on deploys only
import json, sys
payload = json.load(sys.stdin)
command = payload.get("tool_input", {}).get("command", "")
if "deploy" not in command:
    sys.exit(0)
...
sys.exit(2)  # 2 blocks the tool call; 1 does not
```

## Pattern: Environment-Specific Gates

### Development vs Production

```bash
#!/bin/bash
# smart_gate.sh - PreToolUse gate, strict in production

# The payload is on stdin. $file_path is not a variable the harness sets.
file_path=$(jq -r '.tool_input.file_path // empty')
[ -n "$file_path" ] || exit 0

if [ "$ENVIRONMENT" = "production" ]; then
    # Strict checks for production. exit 2 is the only code that blocks a
    # PreToolUse call - `|| exit 1` here would print a refusal and proceed.
    python3 scripts/strict_validation.py "$file_path" || exit 2
    npm test || exit 2
    npm run build || exit 2
else
    # Lenient checks for development
    prettier --write "$file_path" 2>/dev/null || true
fi

exit 0
```

## Best Practices

### 1. Never Block on Non-Critical Checks

```bash
# ✅ Good - a formatter that is missing or unhappy changes nothing
prettier --write "$file_path" 2>/dev/null || true
exit 0

# ❌ Bad - the formatter's exit code silently becomes the hook's verdict, and a
#    stray 2 from a PreToolUse hook blocks the tool call outright
prettier --write "$file_path"
exit $?
```

### 2. Use PostToolUse for Non-Blocking Quality

```json
{
  "PostToolUse": [/* Formatting, linting, tests */]
}
```

### 3. Use PreToolUse Only for Security/Critical

```json
{
  "PreToolUse": [/* Security checks, deployment gates */]
}
```

### 4. Log All Hook Results

```bash
echo "$(date) | hook_name | result" >> .claude-metrics/hooks.log
```

### 5. Make Hooks Fast

- Keep execution under 1 second
- Cache configurations
- Run only necessary checks
- Use incremental testing

## Common Pitfalls

### ❌ Blocking on Formatting Errors

**Problem:** The hook inherits a tool's exit code. On `PreToolUse` a 2 blocks the
call; any non-zero code surfaces stderr to Claude as a hook error.
**Solution:** End non-critical checks with an explicit `exit 0`

### ❌ Running Full Test Suite Every Time

**Problem:** Hooks take 30+ seconds
**Solution:** Run only related tests (`--onlyChanged`, `--findRelatedTests`)

### ❌ No Error Handling

**Problem:** Hook crashes, unclear why
**Solution:** Redirect errors, log to file, always exit gracefully

### ❌ Not Checking Tool Availability

**Problem:** Hook fails if prettier not installed
**Solution:** Check with `command -v` before running

## Integration with Commands

A command cannot carry its own hooks, so the composition goes the other way: the
command does its work, and session-wide hooks in `.claude/settings.json` react to
the tools it uses.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{"type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude-library/hooks/scripts/format_code.sh"}]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [{"type": "command", "command": "npm test && npm run build"}]
      }
    ]
  }
}
```

`Stop` fires at the end of every turn, not at the end of one command. If a check
should only run for some work, put that condition in the script - read the
payload and return early - rather than hoping the event is narrower than it is.

## Metrics & Monitoring

### Track Hook Performance

```bash
# In each hook script.
# `date +%s%3N` is GNU-only - BSD/macOS date emits a literal "N" and the
# arithmetic below then fails. python3 is already a framework dependency.
now_ms() { python3 -c 'import time;print(int(time.time()*1000))'; }

start_time=$(now_ms)

# ... do work ...

duration=$(( $(now_ms) - start_time ))
echo "${duration}ms | $hook_name" >> .claude-metrics/hook_performance.log
```

### Success Rate Tracking

```bash
# Log success/failure
if [ $? -eq 0 ]; then
    status="success"
else
    status="failed"
fi
echo "$(date) | $hook_name | $status" >> .claude-metrics/hooks.log
```

## Summary

Quality gates via hooks provide:
- ✅ Automatic enforcement
- ✅ Consistent standards
- ✅ Fast feedback
- ✅ No agent intervention needed
- ✅ Customizable per workflow
- ✅ Environment-specific rules

Start with code formatting hooks, add security gates, then layer in testing as needed.
