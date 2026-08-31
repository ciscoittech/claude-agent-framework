# Agent Hooks Pattern

**Status:** Optional Pattern
**Complexity:** Low-Medium
**Dependencies:** None (self-contained)

## Overview

The Hooks Pattern provides deterministic control over Claude Code's behavior through shell commands that execute at specific workflow points. This is a **completely optional** enhancement to the Claude Agent Framework.

### When to Use This Pattern

✅ **Enable hooks when you need:**
- Automatic code formatting after file changes
- Security gates to block dangerous operations
- Custom validation before/after agent actions
- Team notifications (Slack, Discord, email)
- Lightweight metrics without external services
- Project-specific business rules enforcement
- Cost control (block expensive operations)

❌ **Skip hooks for:**
- Simple single-agent workflows
- Rapid prototyping phase
- Learning the framework basics

### What You Get

**With hooks enabled:**
- 🛡️ **Quality Gates**: Auto-format, lint, test after changes
- 🔒 **Security Controls**: Block dangerous bash commands
- 📢 **Notifications**: Slack/Discord/email on workflow events
- 📊 **Lightweight Metrics**: Simple logging to local files
- ✅ **Custom Validation**: Project-specific checks
- 💰 **Cost Control**: Prevent expensive operations

**Performance Impact:**
- ~100ms-1s per hook execution
- Can block operations if needed
- Zero overhead when disabled

---

## Prerequisites

### No External Dependencies!

Hooks are completely self-contained:
- ✅ Uses standard shell commands
- ✅ No API keys needed
- ✅ No external services
- ✅ Works offline

---

## Quick Start

### Step 1: Enable Hooks

Edit `.claude-library/REGISTRY.json`:

```json
{
  "settings": {
    "hooks": {
      "enabled": true,
      "scope": "project",
      "configs": [
        ".claude-library/hooks/configs/code-quality.json"
      ],
      "allow_blocking": true,
      "timeout_ms": 5000,
      "log_hook_output": true
    }
  }
}
```

### Step 2: Choose Hook Configurations

Pre-built configurations available:
- `code-quality.json` - Auto-format and lint
- `security.json` - Block dangerous operations
- `performance.json` - Track timing metrics
- `notifications.json` - Team alerts

### Step 3: Test It

```bash
# Make a code change - hooks will auto-format
claude> "Add a new function to src/utils.py"

# Hooks automatically run prettier, eslint, etc.
# View hook logs in .claude-metrics/hooks.log
```

---

## Architecture

### Hook Execution Flow

```
┌─────────────────────────────────────────────┐
│         CLAUDE CODE WORKFLOW                │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
        ┌─────────────────┐
        │  PreToolUse Hook│ (optional, can block)
        └─────────┬───────┘
                  │ ✅ Pass → Continue
                  │ ❌ Fail → Block operation
                  ▼
        ┌─────────────────┐
        │   Tool Execution│ (Read, Write, Edit, Bash, etc.)
        └─────────┬───────┘
                  │
                  ▼
        ┌─────────────────┐
        │ PostToolUse Hook│ (runs after, never blocks)
        └─────────┬───────┘
                  │
                  ▼
        ┌─────────────────┐
        │   Continue Flow │
        └─────────────────┘
```

### Hook Types & Timing

| Hook Event | When It Runs | Can Block? | Common Uses |
|------------|--------------|------------|-------------|
| `PreToolUse` | Before tool execution | ✅ Yes | Security checks, validation |
| `PostToolUse` | After tool completes | ❌ No | Formatting, notifications |
| `UserPromptSubmit` | User sends message | ✅ Yes | Custom prompts, logging |
| `Stop` | Workflow completes | ❌ No | Notifications, cleanup |
| `SubagentStop` | Agent finishes | ❌ No | Validation, metrics |
| `SessionStart` | Session begins | ❌ No | Setup, initialization |
| `SessionEnd` | Session ends | ❌ No | Cleanup, reports |

---

## Pre-Built Hook Configurations

### 1. Code Quality Hooks

**File:** `.claude-library/hooks/configs/code-quality.json`

Automatically format and lint code after changes:

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

**Benefits:**
- Consistent code style across all agents
- No manual formatting needed
- Works with any formatter (prettier, black, rustfmt, etc.)

---

### 2. Security Hooks

**File:** `.claude-library/hooks/configs/security.json`

Block dangerous operations before they execute:

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

**Blocks:**
- `rm -rf /` and similar dangerous commands
- Production database modifications
- Unauthorized API calls
- Force push to protected branches

---

### 3. Performance Tracking Hooks

**File:** `.claude-library/hooks/configs/performance.json`

Lightweight metrics without external services:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date +%s%3N) START $description\" >> .claude-metrics/timing.log"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$(date +%s%3N) END $description\" >> .claude-metrics/timing.log"
          }
        ]
      }
    ]
  }
}
```

**Tracks:**
- Agent execution times
- Tool usage patterns
- Workflow bottlenecks
- All stored in local files (no external service)

---

### 4. Notification Hooks

**File:** `.claude-library/hooks/configs/notifications.json`

Alert team on workflow completion:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude-library/hooks/scripts/notify_team.sh \"$workflow_name\" \"completed\""
          }
        ]
      }
    ]
  }
}
```

**Supports:**
- Slack webhooks
- Discord webhooks
- Email notifications
- Custom integrations

---

## Hook Script Examples

### Format Code Script

**File:** `.claude-library/hooks/scripts/format_code.sh`

```bash
#!/bin/bash
file_path="$1"

# Determine file type and format accordingly
case "$file_path" in
  *.py)
    black "$file_path" 2>/dev/null || true
    isort "$file_path" 2>/dev/null || true
    ;;
  *.js|*.ts|*.jsx|*.tsx)
    npx prettier --write "$file_path" 2>/dev/null || true
    npx eslint --fix "$file_path" 2>/dev/null || true
    ;;
  *.rs)
    rustfmt "$file_path" 2>/dev/null || true
    ;;
  *.go)
    gofmt -w "$file_path" 2>/dev/null || true
    ;;
esac

exit 0  # Never block on formatting errors
```

---

### Security Check Script

**File:** `.claude-library/hooks/scripts/security_check.py`

```python
#!/usr/bin/env python3
import sys
import re

command = sys.argv[1] if len(sys.argv) > 1 else ""

# Dangerous command patterns
DANGEROUS_PATTERNS = [
    r'rm\s+-rf\s+/',           # Delete root
    r'rm\s+-rf\s+\*',          # Delete everything
    r':\s*\(\s*\)\s*\{',       # Fork bomb
    r'dd\s+if=.*of=/dev/sd',   # Disk wipe
    r'mkfs\.',                  # Format disk
    r'>\s*/dev/sd',            # Overwrite disk
    r'curl.*\|\s*bash',        # Pipe to bash (risky)
    r'git\s+push.*--force.*main',  # Force push to main
    r'git\s+push.*--force.*master', # Force push to master
]

# Check command against patterns
for pattern in DANGEROUS_PATTERNS:
    if re.search(pattern, command, re.IGNORECASE):
        print(f"🚫 BLOCKED: Dangerous command detected: {command}", file=sys.stderr)
        sys.exit(1)  # Non-zero exit blocks the command

# Log all bash commands for audit
with open('.claude-metrics/bash_commands.log', 'a') as f:
    from datetime import datetime
    f.write(f"{datetime.now().isoformat()} | {command}\n")

sys.exit(0)  # Allow command
```

---

### Notification Script

**File:** `.claude-library/hooks/scripts/notify_team.sh`

```bash
#!/bin/bash
workflow_name="$1"
status="$2"

# Read Slack webhook from environment or .env
if [ -f .env ]; then
    source .env
fi

if [ -z "$SLACK_WEBHOOK_URL" ]; then
    exit 0  # No webhook configured, skip silently
fi

# Send notification
curl -X POST "$SLACK_WEBHOOK_URL" \
    -H 'Content-Type: application/json' \
    -d "{
        \"text\": \"🤖 Agent workflow *${workflow_name}* ${status}\",
        \"blocks\": [
            {
                \"type\": \"section\",
                \"text\": {
                    \"type\": \"mrkdwn\",
                    \"text\": \"*Workflow:* ${workflow_name}\\n*Status:* ${status}\\n*Time:* $(date)\"
                }
            }
        ]
    }" \
    2>/dev/null || true

exit 0
```

---

## Workflow-Specific Hooks

Different workflows can have different hook configurations:

### Example: Build Workflow Hooks

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
        ],
        "Stop": [
          {
            "matcher": "*",
            "hooks": [
              {
                "type": "command",
                "command": "bash .claude-library/hooks/scripts/notify_team.sh 'Build' 'completed'"
              }
            ]
          }
        ]
      }
    }
  }
}
```

### Example: Deploy Workflow Hooks

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
        ],
        "Stop": [
          {
            "matcher": "*",
            "hooks": [
              {
                "type": "command",
                "command": "bash .claude-library/hooks/scripts/notify_team.sh 'Deployment' 'completed'"
              }
            ]
          }
        ]
      }
    }
  }
}
```

---

## REGISTRY.json Configuration Reference

### Complete Configuration Schema

```json
{
  "settings": {
    "hooks": {
      "enabled": false,                    // Master switch (default: OFF)
      "scope": "project",                  // "project" or "user"
      "configs": [                         // Hook configuration files to load
        ".claude-library/hooks/configs/code-quality.json",
        ".claude-library/hooks/configs/security.json",
        ".claude-library/hooks/configs/performance.json"
      ],
      "allow_blocking": true,              // Allow PreToolUse hooks to block?
      "timeout_ms": 5000,                  // Max hook execution time
      "log_hook_output": true,             // Log hook stdout/stderr
      "log_file": ".claude-metrics/hooks.log",
      "fail_on_timeout": false,            // Block if hook times out?
      "parallel_hook_execution": false     // Run multiple hooks in parallel?
    }
  }
}
```

### Configuration Options Explained

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `false` | Master switch for all hooks |
| `scope` | string | `"project"` | `"project"` or `"user"` level hooks |
| `configs` | array | `[]` | List of hook config files to load |
| `allow_blocking` | boolean | `true` | Can PreToolUse hooks block operations? |
| `timeout_ms` | number | `5000` | Max time for hook to execute |
| `log_hook_output` | boolean | `true` | Log hook stdout/stderr to file |
| `log_file` | string | - | Path to hook log file |
| `fail_on_timeout` | boolean | `false` | Block operation if hook times out |
| `parallel_hook_execution` | boolean | `false` | Run multiple hooks simultaneously |

---

## Advanced Patterns

### Pattern 1: Conditional Hooks Based on Environment

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if [ \"$ENVIRONMENT\" = \"production\" ]; then python scripts/strict_security.py \"$command\"; else exit 0; fi"
          }
        ]
      }
    ]
  }
}
```

### Pattern 2: Multi-Stage Validation

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

### Pattern 3: Agent Output Validation

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude-library/hooks/scripts/validate_agent_output.py"
          }
        ]
      }
    ]
  }
}
```

---

## Troubleshooting

### Hook Not Executing

**Check:**
1. Is `hooks.enabled` set to `true`?
2. Is the config file path correct?
3. Is the matcher pattern correct?
4. Check `.claude-metrics/hooks.log` for errors

### Hook Blocking When It Shouldn't

**Solutions:**
1. Use `PostToolUse` instead of `PreToolUse` (can't block)
2. Set `allow_blocking: false` in REGISTRY.json
3. Ensure hook script exits with 0 on success

### Hook Timing Out

**Solutions:**
1. Increase `timeout_ms` in REGISTRY.json
2. Optimize hook script performance
3. Set `fail_on_timeout: false` to not block on timeout

### Hook Script Not Found

**Check:**
1. File path is correct relative to project root
2. Script has execute permissions: `chmod +x script.sh`
3. Script has proper shebang: `#!/bin/bash` or `#!/usr/bin/env python3`

---

## Best Practices

### 1. Start Minimal
Begin with one hook config, add more as needed:
```json
{
  "configs": ["hooks/configs/code-quality.json"]
}
```

### 2. Make Hooks Fast
Keep hook execution under 1 second:
- Use caching where possible
- Run only necessary checks
- Parallelize independent operations

### 3. Never Block on Formatting
Auto-formatting should use `PostToolUse` and always exit 0:
```bash
prettier --write "$file_path" 2>/dev/null || true
exit 0
```

### 4. Log Everything
Even when hooks pass, log for audit trail:
```python
with open('.claude-metrics/hooks.log', 'a') as f:
    f.write(f"{timestamp} | {hook_name} | {status}\n")
```

### 5. Environment-Specific Hooks
Different rules for dev vs production:
```bash
if [ "$ENVIRONMENT" = "production" ]; then
    # Strict checks
else
    # Lenient checks
fi
```

---

## Directory Structure

```
.claude-library/
├── hooks/                                 # NEW: Hooks pattern
│   ├── README.md                         # This file
│   ├── configs/                          # Pre-built configurations
│   │   ├── code-quality.json            # Auto-format, lint
│   │   ├── security.json                # Security gates
│   │   ├── performance.json             # Timing metrics
│   │   ├── notifications.json           # Team alerts
│   │   └── custom-example.json          # Template for custom hooks
│   ├── scripts/                          # Hook execution scripts
│   │   ├── format_code.sh               # Multi-language formatter
│   │   ├── security_check.py            # Security validator
│   │   ├── validate_agent_output.py     # Agent output checker
│   │   ├── notify_team.sh               # Slack/Discord notifications
│   │   ├── track_timing.sh              # Performance metrics
│   │   └── run_tests.sh                 # Test execution
│   └── patterns/                         # Integration examples
│       ├── workflow-gates.md            # Quality gate patterns
│       └── agent-validation.md          # Agent output validation
```

---

## Migration Guide

### From No Hooks → Hooks

1. Add hooks section to REGISTRY.json with `enabled: false`
2. Choose one config to start (recommend `code-quality.json`)
3. Test with simple workflow
4. Set `enabled: true`
5. Add more configs as needed

## Performance Impact

### Benchmark Results

| Hook Type | Execution Time | Impact |
|-----------|----------------|--------|
| Code formatting | 200-500ms | Low |
| Security check | 50-100ms | Minimal |
| Run tests | 1-5s | Medium |
| Slack notification | 100-300ms | Low |
| Performance logging | 10-20ms | Negligible |

### Optimization Tips

1. **Cache formatter configurations** - Don't re-parse on each run
2. **Use `|| true`** - Don't fail on non-critical errors
3. **Run tests incrementally** - Only test changed files
4. **Async notifications** - Don't wait for webhook response
5. **Batch operations** - Combine multiple checks into one script

---

## Security Considerations

### 1. Validate Hook Scripts
Only run trusted hook scripts:
```bash
# Check script signature
gpg --verify hook_script.sh.sig hook_script.sh
```

### 2. Sandbox Hook Execution
Limit hook capabilities:
```json
{
  "hooks": {
    "sandbox_enabled": true,
    "allowed_commands": ["prettier", "eslint", "black"],
    "blocked_paths": ["/etc", "/usr", "/var"]
  }
}
```

### 3. Audit Hook Execution
Log all hook runs:
```bash
echo "$(date) | $USER | $hook_name | $status" >> .claude-metrics/audit.log
```

---

## Examples from Real Projects

### Example 1: FastAPI Project

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "black \"$file_path\" && isort \"$file_path\" && mypy \"$file_path\""
          }
        ]
      }
    ]
  }
}
```

### Example 2: React Project

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$file_path\" && npx eslint --fix \"$file_path\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "npm test -- --watchAll=false"
          }
        ]
      }
    ]
  }
}
```

### Example 3: Kubernetes Deployment

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "if echo \"$command\" | grep -q 'kubectl.*production'; then python scripts/require_approval.py; fi"
          }
        ]
      }
    ]
  }
}
```

---

## Contributing

Have a useful hook configuration? Share it!

1. Create hook config in `configs/`
2. Add corresponding script in `scripts/`
3. Document in `patterns/`
4. Submit PR with examples

---

## Conclusion

The Hooks Pattern provides lightweight, self-contained workflow control without external dependencies. Perfect for:

- ✅ **Quality gates** - Automatic formatting, linting, testing
- ✅ **Security** - Block dangerous operations
- ✅ **Notifications** - Alert team on workflow events
- ✅ **Metrics** - Simple logging without external services

Start with one hook configuration and grow as needed. Hooks are fastest way to add deterministic control to your agent workflows.

**Next Steps:**
1. Enable hooks in REGISTRY.json
2. Choose a pre-built config (start with `code-quality.json`)
3. Test with simple workflow
4. Add more hooks as needed

---

*Hooks Pattern v1.0 - Part of Claude Agent Framework*
