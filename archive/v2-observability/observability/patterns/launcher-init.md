# Agent Launcher Observability Integration

This snippet shows how to add observability to your agent launcher.

## Integration Template

Add this to your `.claude/agent-launcher.md`:

```markdown
## Workflow Observability (Optional)

**Step 1: Check if observability is enabled**

```python
import json
from pathlib import Path

registry = json.loads(Path('.claude-library/REGISTRY.json').read_text())
observability_enabled = registry['settings'].get('observability', {}).get('enabled', False)
```

**Step 2: Initialize workflow context (if enabled)**

```python
if observability_enabled:
    from observability.logfire_helper import log_workflow

    with log_workflow(command="{COMMAND}", project="{PROJECT}") as workflow:
        print(f"🔍 Observability enabled - tracking workflow")

        # Log parallel groups before spawning
        from observability.logfire_helper import log_parallel_group
        log_parallel_group('architecture', ['architect', 'test-planner', 'researcher'])

        # ... spawn your agents here ...

        # After completion, log workflow metadata
        workflow.set_attribute('total_agents_spawned', 3)
        workflow.set_attribute('parallel_groups', 1)
        workflow.set_attribute('status', 'success')
else:
    # Normal operation without observability overhead
    print("🚀 Running without observability")
    # ... spawn your agents here ...
```
```

## Example: /build Command with Observability

```markdown
# /build Command

## Purpose
Build a new feature using TDD workflow

## Workflow with Observability

```python
import json
from pathlib import Path

# Check observability setting
registry = json.loads(Path('.claude-library/REGISTRY.json').read_text())
observability_enabled = registry['settings'].get('observability', {}).get('enabled', False)

if observability_enabled:
    from observability.logfire_helper import log_workflow, log_parallel_group

    with log_workflow('/build', 'myproject') as workflow:
        ### Stage 1: Architecture Phase (Parallel)
        log_parallel_group('architecture', ['architect', 'test-planner', 'researcher'])

        # Spawn 3 agents in parallel
        <Task>...</Task>
        <Task>...</Task>
        <Task>...</Task>

        ### Stage 2: Implementation Phase (Sequential)
        # Spawn engineer agent
        <Task>...</Task>

        ### Stage 3: Validation
        # Spawn reviewer agent
        <Task>...</Task>

        # Log completion
        workflow.set_attribute('total_agents_spawned', 5)
        workflow.set_attribute('stages_completed', 3)
        workflow.set_attribute('status', 'success')

        # Optionally spawn Observer to validate
        if registry['settings']['observability']['config']['auto_spawn_observer']:
            <Task>
              [Load Observer agent]
              Validate this workflow's outputs
            </Task>
else:
    # Same workflow without observability overhead
    # Spawn agents directly...
```
```

## Parallel Group Tracking

When spawning agents in parallel, log the group:

```python
if observability_enabled:
    from observability.logfire_helper import log_parallel_group

    # Before spawning parallel agents
    log_parallel_group('architecture', ['architect', 'test-planner', 'researcher'])

    # Now spawn agents (they will nest under this parallel group in traces)
    <Task>...</Task>  # architect
    <Task>...</Task>  # test-planner
    <Task>...</Task>  # researcher
```

This creates a visual grouping in Logfire traces showing which agents ran in parallel.

## Workflow Attributes Reference

### Standard Workflow Attributes

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `command` | string | Command executed | `'/build'` |
| `project` | string | Project name | `'myproject'` |
| `total_agents_spawned` | int | Number of agents used | `5` |
| `parallel_groups` | int | Number of parallel groups | `2` |
| `stages_completed` | int | Workflow stages finished | `3` |
| `status` | string | Final status | `'success'`, `'failed'` |
| `duration_seconds` | float | Total time | `45.2` |

### Optional Workflow Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `feature_description` | string | What was built |
| `files_total_created` | int | Total files created |
| `tests_passed` | bool | Did tests pass? |
| `build_succeeded` | bool | Did build succeed? |

## Error Handling in Launcher

When workflow fails:

```python
if observability_enabled:
    with log_workflow('/build', 'myproject') as workflow:
        try:
            # Spawn agents...
            workflow.set_attribute('status', 'success')
        except Exception as e:
            workflow.set_attribute('status', 'failed')
            workflow.set_attribute('error_type', type(e).__name__)
            workflow.set_attribute('error_message', str(e))
            raise
```

## Observer Agent Integration

Automatically spawn Observer to validate outputs:

```python
if observability_enabled:
    with log_workflow('/build', 'myproject') as workflow:
        # ... normal workflow ...

        # After completion, validate if configured
        auto_validate = registry['settings']['observability']['config'].get('auto_spawn_observer', False)

        if auto_validate:
            <Task>
              <subagent_type>general-purpose</subagent_type>
              <description>Validate workflow outputs</description>
              <prompt>
                [Load Observer agent from .claude-library/agents/observability/observer.md]

                Validate the outputs of workflow: {workflow_id}

                Check that:
                1. All claimed files exist
                2. Tests pass (if applicable)
                3. Build succeeds (if applicable)

                Report validation results.
              </prompt>
            </Task>
```

## Manual Observer Invocation

User can also manually request validation:

```markdown
## /validate Command

```python
import json
from pathlib import Path
from observability.logfire_helper import get_workflow_context

# Get current workflow
ctx = get_workflow_context()

if not ctx:
    print("❌ No active workflow to validate")
else:
    # Spawn Observer agent
    <Task>
      [Load Observer agent]
      Validate workflow: {ctx['workflow_id']}
    </Task>
```
```

## Complete Example: Multi-Stage Workflow

```python
import json
from pathlib import Path

registry = json.loads(Path('.claude-library/REGISTRY.json').read_text())
observability_enabled = registry['settings'].get('observability', {}).get('enabled', False)

if observability_enabled:
    from observability.logfire_helper import log_workflow, log_parallel_group

    with log_workflow('/feature-loop', 'web-app') as workflow:
        print("🔍 Starting observed workflow")

        ## Stage 1: Parallel Architecture (30 seconds)
        log_parallel_group('architecture', ['architect', 'test-planner', 'researcher'])
        print("Stage 1/3: Architecture design (parallel)")

        # Spawn 3 agents in parallel
        <Task subagent_type="general-purpose" description="Architecture design">
          [Load architect agent]
          Design: {feature}
        </Task>
        <Task subagent_type="general-purpose" description="Test planning">
          [Load test-planner agent]
          Plan tests for: {feature}
        </Task>
        <Task subagent_type="general-purpose" description="Research patterns">
          [Load researcher agent]
          Find patterns for: {feature}
        </Task>

        ## Stage 2: Implementation (45 seconds)
        print("Stage 2/3: Implementation")

        <Task subagent_type="general-purpose" description="Implement feature">
          [Load engineer agent]
          Implement: {feature}
        </Task>

        ## Stage 3: Review & Validation (20 seconds)
        log_parallel_group('validation', ['reviewer', 'observer'])
        print("Stage 3/3: Review and validation")

        <Task subagent_type="general-purpose" description="Code review">
          [Load reviewer agent]
          Review implementation
        </Task>

        <Task subagent_type="general-purpose" description="Output validation">
          [Load observer agent]
          Validate workflow outputs
        </Task>

        ## Log workflow completion
        workflow.set_attribute('total_agents_spawned', 5)
        workflow.set_attribute('parallel_groups', 2)
        workflow.set_attribute('stages_completed', 3)
        workflow.set_attribute('feature', feature)
        workflow.set_attribute('status', 'success')

        print("✅ Workflow complete - view traces at Logfire dashboard")

else:
    # Same workflow without observability
    print("🚀 Starting lean workflow")

    ## Stage 1: Architecture
    <Task>...</Task>
    <Task>...</Task>
    <Task>...</Task>

    ## Stage 2: Implementation
    <Task>...</Task>

    ## Stage 3: Review
    <Task>...</Task>

    print("✅ Workflow complete")
```

## Best Practices

### 1. Initialize Once Per Workflow

Don't create multiple workflow contexts:

```python
# Good - one context for entire workflow
with log_workflow('/build', 'myproject') as workflow:
    # all agent spawning here

# Bad - multiple contexts
with log_workflow('/build', 'myproject'):
    # some agents
with log_workflow('/build', 'myproject'):  # Creates duplicate!
    # more agents
```

### 2. Use Context Manager

Always use `with log_workflow()` to ensure cleanup:

```python
# Good - automatic cleanup
with log_workflow(...) as workflow:
    # work

# Bad - manual cleanup needed
context = create_workflow_context(...)
# work
clear_workflow_context()  # Easy to forget!
```

### 3. Log Parallel Groups

Help visualize concurrent execution:

```python
# Log before spawning parallel agents
log_parallel_group('phase_name', ['agent1', 'agent2', 'agent3'])

# Then spawn agents
<Task>...</Task>
<Task>...</Task>
<Task>...</Task>
```

### 4. Provide User Feedback

Tell users when observability is active:

```python
if observability_enabled:
    print("🔍 Observability enabled - workflow will be tracked")
    with log_workflow(...):
        # work
else:
    print("🚀 Running in lean mode")
    # work
```

## Testing Launcher Integration

### Test 1: Disabled Observability

1. Set `"enabled": false` in REGISTRY.json
2. Run command: `/build "test feature"`
3. Verify: No Logfire calls, no errors
4. Workflow completes normally

### Test 2: Enabled Observability

1. Set `"enabled": true` in REGISTRY.json
2. Set LOGFIRE_TOKEN environment variable
3. Run command: `/build "test feature"`
4. Verify:
   - Workflow context created at `/tmp/claude-workflow-context.json`
   - Logfire shows workflow trace
   - Agents nested under workflow
   - Context cleaned up after completion

### Test 3: Parallel Group Visualization

1. Enable observability
2. Run workflow with parallel agents
3. Check Logfire dashboard
4. Verify: Parallel group span shows agents running concurrently

## Troubleshooting

### "No workflow context found" in Agents

**Cause:** Launcher didn't initialize context before spawning agents

**Fix:** Ensure launcher calls `log_workflow()` BEFORE spawning agents

### Context File Not Cleaned Up

**Cause:** Workflow crashed or launcher didn't use context manager

**Fix:** Use `with log_workflow()` to ensure automatic cleanup

### Duplicate Workflow IDs

**Cause:** Multiple contexts created in same workflow

**Fix:** Create only ONE workflow context per command execution

### Performance Degradation

**Cause:** Too many parallel group logs or workflow attributes

**Fix:** Log only essential attributes, one parallel group per stage