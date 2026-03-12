# /launch-agent - Intelligent Agent Selection & Launch

**Purpose**: Analyze a task and launch the optimal agent with correct model, tools, and context
**Type**: Routing Command

---

## Usage

```bash
/launch-agent <task description>
```

**Examples**:
```bash
/launch-agent "refactor the auth module to use JWT"
/launch-agent "write tests for the payment service"
/launch-agent "document our REST API endpoints"
/launch-agent "review the PR for security issues"
```

---

## How It Works

### Step 1: Classify the Task

Read the task description and classify:

| Signal | Agent Type | Model |
|--------|-----------|-------|
| implement, build, refactor, fix, code | **engineer** | sonnet |
| test, coverage, spec, assert | **engineer** (test focus) | sonnet |
| document, guide, README, API docs | **documentation** | sonnet |
| review, audit, security, quality | **reviewer** | sonnet |
| design, architecture, schema, plan | **architect** | opus |
| simple fix, typo, rename, format | **engineer** | haiku |

**Complexity override**:
- If task mentions >5 files, multi-service, or "complex" → upgrade to `opus`
- If task is a single file, quick fix, or "simple" → downgrade to `haiku`

### Step 2: Select Agent Definition

Check for custom agent types in `.claude/agents/`:
```bash
# If .claude/agents/{type}.md exists, use it as subagent_type
# Otherwise fall back to general-purpose with persona from .claude-library/agents/
```

Load the matching agent from `.claude-library/REGISTRY.json` to get:
- Agent path and persona
- Required tools
- Relevant contexts

### Step 3: Launch

Use the Agent tool to launch with the selected configuration:

```python
Agent(
    description="<short task summary>",
    prompt="""
    <Load agent persona from selected agent file>

    ## Task
    <user's task description>

    ## Project Context
    <Load relevant contexts from REGISTRY.json>
    """,
    subagent_type="<matched type or general-purpose>",
    model="<selected model>"
)
```

### Step 4: Report

After agent completes, summarize:
- What was done
- Files created/modified
- Any issues or follow-ups needed

---

## Decision Tree

```
Task Description
├── Contains: implement/build/fix/refactor/code
│   ├── Simple (1 file, quick) → engineer + haiku
│   ├── Medium (2-5 files) → engineer + sonnet
│   └── Complex (>5 files, architecture) → engineer + opus
├── Contains: test/spec/coverage
│   └── → engineer (test focus) + sonnet
├── Contains: review/audit/security
│   └── → reviewer + sonnet
├── Contains: document/guide/README
│   └── → documentation + sonnet
├── Contains: design/architecture/plan
│   └── → architect + opus
└── Unclear
    └── → general-purpose + sonnet
```

---

## Integration

This command reads from:
- `.claude-library/REGISTRY.json` — agent definitions, tools, contexts
- `.claude/agents/` — custom subagent types (if they exist)
- `.claude-library/agents/` — full agent persona files

For projects without a REGISTRY.json, falls back to `general-purpose` agent type with sonnet model.
