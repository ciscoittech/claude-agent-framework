# Claude Code Hooks Context

**Source**: https://docs.claude.com/en/docs/claude-code/hooks-guide.md
**Purpose**: Official guide to Claude Code's Hooks system
**Auto-update**: Fetch latest from docs.claude.com

---

## Hooks Overview

### What are Hooks?

**Hooks** are scripts that run automatically at specific points in Claude Code's execution lifecycle. They enable:
- Custom validation logic
- Automated workflows
- Security enforcement
- Observability tracking
- Quality gates

### Hook Events

Claude Code supports these hook events:

1. **SessionStart** - When Claude Code session begins
2. **SessionEnd** - When Claude Code session ends
3. **PreToolUse** - Before any tool is executed
4. **PostToolUse** - After any tool completes
5. **PrePrompt** - Before user prompt is processed
6. **PostPrompt** - After response is generated

---

## Hook Configuration

### Enable Hooks in REGISTRY.json

```json
{
  "settings": {
    "hooks": {
      "enabled": true,
      "scope": "project",
      "configs": [
        ".claude-library/hooks/configs/my-hooks.json"
      ],
      "allow_blocking": false,
      "timeout_ms": 5000,
      "log_hook_output": true
    }
  }
}
```

### Hook Config File Structure

```json
{
  "name": "my-hook-set",
  "version": "1.0.0",
  "description": "Custom hooks for my project",
  "hooks": [
    {
      "event": "PreToolUse",
      "script": ".claude-library/hooks/scripts/validate_tool.py",
      "description": "Validate tool usage before execution",
      "blocking": false,
      "timeout_ms": 1000,
      "filters": {
        "tools": ["Write", "Edit", "Bash"]
      }
    }
  ]
}
```

---

## Hook Events in Detail

### SessionStart

**When**: Once when Claude Code starts
**Use For**:
- Initialize databases
- Load configuration
- Set up environment
- Create session tracking

**Example** (from observability system):
```bash
#!/bin/bash
# init_observability_db.sh

METRICS_DIR=".claude-metrics"
DB_FILE="${METRICS_DIR}/observability.db"

mkdir -p "${METRICS_DIR}"

if [[ ! -f "${DB_FILE}" ]]; then
    echo "✅ Initializing observability database"
    sqlite3 "${DB_FILE}" < schema.sql
fi

python3 << 'PYTHON'
from db_helper import get_session_id
session_id = get_session_id()
print(f"Session ID: {session_id[:8]}...")
PYTHON
```

### SessionEnd

**When**: Once when Claude Code ends
**Use For**:
- Cleanup resources
- Generate reports
- Archive data
- Close connections

**Example**:
```python
#!/usr/bin/env python3
import sys
from db_helper import end_session

try:
    end_session()
    print("✅ Session ended successfully")
except Exception as e:
    print(f"⚠️ Error ending session: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block on error
```

### PreToolUse

**When**: Before each tool execution
**Use For**:
- Validate inputs
- Check permissions
- Block dangerous operations
- Track tool usage

**Hook Input** (via stdin):
```json
{
  "tool": {
    "name": "Write",
    "parameters": {
      "file_path": "/path/to/file.py",
      "content": "..."
    }
  },
  "context": {
    "session_id": "abc123",
    "timestamp": "2025-10-04T10:00:00Z"
  }
}
```

**Example**:
```python
#!/usr/bin/env python3
import sys
import json

hook_input = json.loads(sys.stdin.read())
tool_name = hook_input['tool']['name']

# Block writes to sensitive files
if tool_name == 'Write':
    file_path = hook_input['tool']['parameters']['file_path']
    if '.env' in file_path or 'secret' in file_path:
        print(f"❌ Blocked: Cannot write to {file_path}", file=sys.stderr)
        sys.exit(1)  # Non-zero exit blocks execution

# Allow
sys.exit(0)
```

### PostToolUse

**When**: After each tool completes
**Use For**:
- Track results
- Validate outputs
- Log metrics
- Trigger workflows

**Hook Input**:
```json
{
  "tool": {...},
  "result": {
    "success": true,
    "output": "...",
    "usage": {
      "input_tokens": 500,
      "output_tokens": 200
    }
  },
  "error": null,
  "duration_ms": 1500
}
```

**Example** (from observability):
```python
#!/usr/bin/env python3
import sys
import json
from db_helper import update_execution, insert_metrics

hook_input = json.loads(sys.stdin.read())

if hook_input['tool']['name'] == 'Task':
    execution_id = get_current_execution_id()
    result = hook_input['result']

    # Update execution
    update_execution(
        execution_id=execution_id,
        status='success' if result['success'] else 'failed',
        duration_ms=hook_input['duration_ms']
    )

    # Track metrics
    usage = result.get('usage', {})
    insert_metrics(
        execution_id=execution_id,
        tokens_input=usage.get('input_tokens', 0),
        tokens_output=usage.get('output_tokens', 0)
    )
```

### PrePrompt

**When**: Before processing user prompt
**Use For**:
- Modify prompts
- Add context
- Validate requests
- Inject instructions

**Example**:
```python
#!/usr/bin/env python3
import sys
import json

hook_input = json.loads(sys.stdin.read())
user_prompt = hook_input['prompt']

# Add project context
enhanced_prompt = f"""
{user_prompt}

Project Context:
- Tech Stack: Python, FastAPI, PostgreSQL
- Follow PEP 8 style guide
- Write tests for all new code
"""

# Output modified prompt
print(json.dumps({"prompt": enhanced_prompt}))
```

### PostPrompt

**When**: After generating response
**Use For**:
- Validate responses
- Log outputs
- Trigger post-processing
- Update metrics

---

## Hook Filters

### Tool Filters

Only run hook for specific tools:
```json
{
  "event": "PostToolUse",
  "script": "./track_writes.py",
  "filters": {
    "tools": ["Write", "Edit", "NotebookEdit"]
  }
}
```

### Custom Filters

Add logic in script:
```python
# Only track Task tool for specific agents
tool_name = hook_input['tool']['name']
if tool_name == 'Task':
    agent_type = hook_input['tool']['parameters'].get('subagent_type')
    if agent_type in ['framework-architect', 'framework-engineer']:
        # Track this
        pass
    else:
        # Skip
        sys.exit(0)
```

---

## Best Practices

### 1. Non-Blocking by Default

```json
{
  "blocking": false,  // Don't block on errors
  "timeout_ms": 1000  // Fast timeout
}
```

Use `blocking: true` only for critical validation.

### 2. Fast Execution

**Targets**:
- SessionStart: <500ms
- PreToolUse: <100ms
- PostToolUse: <200ms
- SessionEnd: <500ms

**Optimization**:
- Minimize I/O
- Use efficient data structures
- Cache when possible
- Async where applicable

### 3. Error Handling

```python
try:
    # Hook logic
    process_hook(hook_input)
except Exception as e:
    print(f"⚠️ Hook error: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block on error (unless critical)
```

### 4. Logging

```python
import sys

# Log to stderr (appears in Claude Code output)
print(f"📊 Tracking: {tool_name}", file=sys.stderr)

# Log to file for persistence
with open('.claude-metrics/hooks.log', 'a') as f:
    f.write(f"{timestamp} - {tool_name} - {status}\n")
```

### 5. Security

```python
# Validate input
assert isinstance(hook_input, dict)
assert 'tool' in hook_input

# Sanitize file paths
file_path = hook_input['tool']['parameters']['file_path']
if '..' in file_path or file_path.startswith('/etc'):
    sys.exit(1)  # Block

# Check permissions
if tool_name in ['Bash', 'Write'] and not has_permission():
    sys.exit(1)
```

---

## Framework Integration

### With Local Observability

The observability system uses 5 hooks:
1. **SessionStart**: `init_observability_db.sh` - Initialize database
2. **PreToolUse**: `observe_task_start.py` - Track agent launch
3. **PostToolUse**: `observe_task_end.py` - Track completion
4. **PostToolUse**: `track_artifact.py` - Track files/commands
5. **PostToolUse**: `validate_execution.py` - Validate against expectations

### With Quality Gates

```json
{
  "event": "PostToolUse",
  "script": ".claude-library/hooks/scripts/quality_gate.py",
  "blocking": true,
  "filters": {
    "tools": ["Bash"]
  }
}
```

```python
# quality_gate.py
# Block if tests fail
if 'pytest' in hook_input['tool']['parameters']['command']:
    result = hook_input['result']
    if result['exit_code'] != 0:
        print("❌ Tests failed - blocking", file=sys.stderr)
        sys.exit(1)
```

### With CI/CD

```json
{
  "event": "SessionEnd",
  "script": ".claude-library/hooks/scripts/ci_report.py"
}
```

```python
# ci_report.py
# Generate CI report
from db_helper import get_daily_summary

summary = get_daily_summary(days=1)
report = generate_ci_report(summary)

# Upload to CI system
upload_to_ci(report)
```

---

## Common Patterns

### Pattern 1: Security Enforcement

```python
# Block dangerous operations
BLOCKED_PATTERNS = ['.env', 'secret', 'password', 'token']

for pattern in BLOCKED_PATTERNS:
    if pattern in file_path.lower():
        sys.exit(1)
```

### Pattern 2: Auto-Documentation

```python
# Auto-update docs when code changes
if tool_name in ['Write', 'Edit']:
    file_path = hook_input['tool']['parameters']['file_path']
    if file_path.endswith('.py'):
        # Extract docstrings
        update_api_docs(file_path)
```

### Pattern 3: Performance Monitoring

```python
# Track slow operations
duration_ms = hook_input['duration_ms']
if duration_ms > 5000:
    log_slow_operation(tool_name, duration_ms)
    send_alert(f"Slow operation: {tool_name} took {duration_ms}ms")
```

### Pattern 4: Cost Tracking

```python
# Track token usage and costs
usage = hook_input['result']['usage']
tokens = usage['input_tokens'] + usage['output_tokens']
cost = calculate_cost(tokens)

update_budget(cost)
if get_budget() < 0:
    send_alert("Budget exceeded!")
```

---

## Troubleshooting

### Hook Not Running
- Check `enabled: true` in REGISTRY.json
- Verify config file path
- Check script has execute permissions: `chmod +x script.py`

### Hook Blocking Execution
- Check `blocking: false` unless critical
- Verify script exits with 0 on success
- Check timeout is sufficient

### Hook Too Slow
- Profile script execution
- Minimize I/O operations
- Use caching
- Consider async execution

---

## Resources

**Official Docs**:
- Hooks Guide: https://docs.claude.com/en/docs/claude-code/hooks-guide.md
- Configuration: https://docs.claude.com/en/docs/claude-code/configuration

**Framework Examples**:
- Observability Hooks: `.claude-library/observability/scripts/`
- Hook Configs: `.claude-library/observability/configs/`
- Pattern Docs: `.claude-library/observability/patterns/`

---

**Last Updated**: October 4, 2025
**Update Method**: `/update-docs` command or WebFetch
