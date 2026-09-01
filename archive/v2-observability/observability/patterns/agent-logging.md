# Agent Logging Pattern

This snippet shows how to add observability to individual agents.

## Integration Template

Add this section to the **end** of any agent definition file:

```markdown
---

## Observability (Optional - Active when enabled in REGISTRY.json)

**After completing your task, log your work if observability is enabled:**

```python
# Check if observability is enabled
import json
from pathlib import Path

registry = json.loads(Path('.claude-library/REGISTRY.json').read_text())
observability_enabled = registry['settings'].get('observability', {}).get('enabled', False)

if observability_enabled:
    from observability.logfire_helper import log_agent_task

    with log_agent_task('{AGENT_TYPE}', '{TASK_DESCRIPTION}') as span:
        # Log outputs created
        span.set_attribute('files_created', ['file1.py', 'file2.py'])

        # Log tools used
        span.set_attribute('tools_used', ['Read', 'Write', 'Edit'])

        # Log context loaded (approximate KB)
        span.set_attribute('context_loaded_kb', 8.5)

        # Log status
        span.set_attribute('status', 'success')  # or 'failed'

        # Optional: Log specific decisions or actions
        span.set_attribute('decisions_made', 'Used Factory pattern for auth')
```

**If observability is disabled, this section is automatically skipped.**
```

## Example: System Architect Agent

```markdown
# System Architect Agent

You are a system architect specializing in...

## Core Responsibilities
[Your agent's normal responsibilities...]

## Available Tools
[Your agent's tools...]

---

## Observability (Optional - Active when enabled in REGISTRY.json)

After completing your architecture design, log your work:

```python
import json
from pathlib import Path

registry = json.loads(Path('.claude-library/REGISTRY.json').read_text())
if registry['settings'].get('observability', {}).get('enabled', False):
    from observability.logfire_helper import log_agent_task

    with log_agent_task('architect', 'Design authentication system') as span:
        span.set_attribute('files_created', ['architecture.md', 'schema.md'])
        span.set_attribute('tools_used', ['Read', 'Write', 'Grep'])
        span.set_attribute('patterns_applied', 'Factory, Strategy, Singleton')
        span.set_attribute('status', 'success')
```
```

## Example: Senior Engineer Agent

```markdown
# Senior Engineer Agent

You are a senior engineer specializing in...

---

## Observability (Optional)

After implementing features, log your work:

```python
import json
from pathlib import Path

registry = json.loads(Path('.claude-library/REGISTRY.json').read_text())
if registry['settings'].get('observability', {}).get('enabled', False):
    from observability.logfire_helper import log_agent_task

    with log_agent_task('engineer', 'Implement user authentication') as span:
        span.set_attribute('files_created', ['auth.py', 'models.py', 'tests.py'])
        span.set_attribute('files_modified', ['__init__.py', 'config.py'])
        span.set_attribute('tools_used', ['Read', 'Write', 'Edit', 'Bash'])
        span.set_attribute('tests_written', 15)
        span.set_attribute('test_coverage', '92%')
        span.set_attribute('status', 'success')
```
```

## Logging on Failure

When an agent encounters errors:

```python
if observability_enabled:
    from observability.logfire_helper import log_agent_task

    with log_agent_task('engineer', 'Implement feature') as span:
        span.set_attribute('status', 'failed')
        span.set_attribute('error_type', 'ImportError')
        span.set_attribute('error_message', 'Module not found: pydantic')
        span.set_attribute('files_attempted', ['auth.py'])
        span.set_attribute('resolution_suggested', 'Install missing dependency')
```

## Attributes Reference

### Standard Attributes (All Agents)

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `status` | string | Success or failure | `'success'`, `'failed'` |
| `files_created` | list | New files created | `['auth.py', 'tests.py']` |
| `files_modified` | list | Existing files edited | `['config.py']` |
| `tools_used` | list | Tools invoked | `['Read', 'Write', 'Bash']` |
| `context_loaded_kb` | float | Approx context size | `12.5` |

### Agent-Specific Attributes

**Architect:**
- `patterns_applied`: Design patterns used
- `components_designed`: Number of components
- `diagrams_created`: Architecture diagrams

**Engineer:**
- `lines_of_code`: Approximate LOC written
- `tests_written`: Number of test cases
- `test_coverage`: Coverage percentage

**Reviewer:**
- `files_reviewed`: Files analyzed
- `issues_found`: Number of issues
- `severity_breakdown`: Critical/major/minor counts

**Debugger:**
- `bugs_identified`: Number of bugs found
- `root_cause`: Root cause analysis
- `fixes_applied`: Fixes implemented

### Error Attributes (When status='failed')

| Attribute | Type | Description |
|-----------|------|-------------|
| `error_type` | string | Error category |
| `error_message` | string | Error details |
| `files_attempted` | list | Files agent tried to work on |
| `resolution_suggested` | string | How to fix |

## Best Practices

### 1. Keep Logging Lightweight

✅ **Do log:**
- Files created/modified
- Major decisions
- Tools used
- Final status

❌ **Don't log:**
- Every tool call
- Entire file contents
- Debugging print statements
- Intermediate steps

### 2. Log After Completion

Place logging at the **end** of agent work:

```python
# Do work first
# ... agent does its task ...

# Then log results
if observability_enabled:
    with log_agent_task(...) as span:
        # Log what was accomplished
```

### 3. Handle Observability Gracefully

Always check the flag first:

```python
# Good
if observability_enabled:
    # log stuff

# Bad - don't import if not enabled
from observability.logfire_helper import log_agent_task  # May fail if not installed
```

### 4. Use Meaningful Task Descriptions

```python
# Good
log_agent_task('architect', 'Design user authentication system')
log_agent_task('engineer', 'Implement JWT token validation')

# Bad - too vague
log_agent_task('architect', 'Do architecture')
log_agent_task('engineer', 'Write code')
```

## Testing Observability Integration

### Test Agent with Observability OFF

1. Set `"enabled": false` in REGISTRY.json
2. Run agent task
3. Verify: No logging code executes, no errors

### Test Agent with Observability ON

1. Set `"enabled": true` in REGISTRY.json
2. Set LOGFIRE_TOKEN environment variable
3. Run agent task
4. Check Logfire dashboard for trace

### Verify Zero Overhead When Disabled

```python
import time

# Test 1: Disabled
start = time.time()
# Run agent with observability OFF
time_disabled = time.time() - start

# Test 2: Enabled
start = time.time()
# Run agent with observability ON
time_enabled = time.time() - start

overhead = (time_enabled - time_disabled) / time_disabled * 100
print(f"Observability overhead: {overhead:.1f}%")
# Should be < 15%
```

## Troubleshooting

### "No module named 'observability'" Error

**Cause:** Trying to import when observability is disabled or not installed

**Fix:** Always check the flag BEFORE importing:
```python
if observability_enabled:
    from observability.logfire_helper import log_agent_task
```

### "LOGFIRE_TOKEN not set" Error

**Cause:** Observability enabled but no API key configured

**Fix:** Set your Logfire API key:
```bash
export LOGFIRE_TOKEN="your-key-here"
```

### Logs Not Appearing in Logfire

**Cause:** Workflow context not initialized by launcher

**Fix:** Ensure launcher calls `log_workflow()` or `create_workflow_context()`

### Agent Runs Slowly with Observability

**Cause:** Logging too much data or too frequently

**Fix:** Reduce logging frequency, log only essential attributes