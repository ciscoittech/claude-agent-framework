# Workflow Quality Gates Pattern

**Pattern Type:** Hooks Integration
**Complexity:** Low
**Use Case:** Enforce quality standards automatically

## Overview

Quality gates ensure code meets standards before proceeding to next workflow stage. Hooks provide automatic, deterministic enforcement without agent intervention.

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
            "command": "bash .claude-library/hooks/scripts/format_code.sh \"$file_path\""
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
            "command": "bash .claude-library/hooks/scripts/run_tests.sh \"$file_path\""
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
            "command": "python .claude-library/hooks/scripts/security_check.py \"$command\""
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
            "command": "bash .claude-library/hooks/scripts/format_code.sh \"$file_path\""
          },
          {
            "type": "command",
            "command": "bash .claude-library/hooks/scripts/lint_code.sh \"$file_path\""
          },
          {
            "type": "command",
            "command": "bash .claude-library/hooks/scripts/run_tests.sh \"$file_path\""
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

### Build Workflow

```json
{
  "commands": {
    "build": {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write",
            "hooks": [
              {
                "type": "command",
                "command": "npm test -- --onlyChanged --bail"
              }
            ]
          }
        ]
      }
    }
  }
}
```

### Deploy Workflow

```json
{
  "commands": {
    "deploy": {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "python scripts/pre_deploy_check.py"
              }
            ]
          }
        ]
      }
    }
  }
}
```

## Pattern: Environment-Specific Gates

### Development vs Production

```bash
#!/bin/bash
# smart_gate.sh

if [ "$ENVIRONMENT" = "production" ]; then
    # Strict checks for production
    python scripts/strict_validation.py "$file_path" || exit 1
    npm test || exit 1
    npm run build || exit 1
else
    # Lenient checks for development
    prettier --write "$file_path" 2>/dev/null || true
fi

exit 0
```

## Best Practices

### 1. Never Block on Non-Critical Checks

```bash
# ✅ Good - never blocks
prettier --write "$file_path" 2>/dev/null || true
exit 0

# ❌ Bad - can block workflow
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

**Problem:** Hook exits non-zero, blocks workflow
**Solution:** Always exit 0 for non-critical checks

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

### Feature Development Command

```json
{
  "commands": {
    "feature": {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write",
            "hooks": [{"command": "bash hooks/scripts/format_code.sh \"$file_path\""}]
          }
        ],
        "Stop": [
          {
            "matcher": "*",
            "hooks": [{"command": "npm test && npm run build"}]
          }
        ]
      }
    }
  }
}
```

### Debug Command

```json
{
  "commands": {
    "debug": {
      "hooks": {
        "Stop": [
          {
            "matcher": "*",
            "hooks": [{"command": "bash hooks/scripts/notify_team.sh 'Debug' 'completed'"}]
          }
        ]
      }
    }
  }
}
```

## Metrics & Monitoring

### Track Hook Performance

```bash
# In each hook script
start_time=$(date +%s%3N)

# ... do work ...

end_time=$(date +%s%3N)
duration=$((end_time - start_time))
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
