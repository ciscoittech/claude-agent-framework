# Claude Code Subagents Context

**Source**: https://docs.claude.com/en/docs/claude-code/sub-agents.md
**Purpose**: Official patterns for using the Task tool to launch subagents
**Auto-update**: Fetch latest from docs.claude.com

---

## Subagent Fundamentals

### What is a Subagent?

A **subagent** is an independent Claude instance launched via the `Task` tool to handle specialized work in parallel or sequentially.

**Key Characteristics**:
- Full Claude instance with own context
- Can use all available tools
- Runs independently of parent
- Returns results to parent when complete
- Can be parallel or sequential

### When to Use Subagents

**✅ Use Subagents For**:
- Complex, multi-step tasks
- Specialized work (research, coding, testing)
- Parallel execution for speed
- Independent context needed
- Task requires different tool permissions

**❌ Don't Use Subagents For**:
- Simple, single-step tasks
- Tasks requiring shared context
- Quick tool calls
- Already in focused context

---

## Task Tool Syntax

### Basic Usage

```python
# Launch a single subagent
Task(
    description="Clear task description",
    prompt="""
    Detailed instructions for the subagent.
    Include context, requirements, and expected output.
    """,
    subagent_type="general-purpose"  # or specialized type
)
```

### Parallel Execution

```python
# Launch multiple subagents in parallel (single message, multiple Task calls)
[
    Task(
        description="Research API patterns",
        prompt="Research REST API best practices for Python FastAPI",
        subagent_type="general-purpose"
    ),
    Task(
        description="Research database patterns",
        prompt="Research SQLAlchemy best practices for async operations",
        subagent_type="general-purpose"
    ),
    Task(
        description="Research testing patterns",
        prompt="Research pytest patterns for async API testing",
        subagent_type="general-purpose"
    )
]
```

### Sequential Execution

```python
# First subagent
result1 = Task(
    description="Design database schema",
    prompt="Create database schema for user authentication system",
    subagent_type="general-purpose"
)

# Use result1 in next subagent
result2 = Task(
    description="Implement schema",
    prompt=f"Implement this database schema:\n{result1}\n\nUse SQLAlchemy async",
    subagent_type="general-purpose"
)
```

---

## Subagent Types

### general-purpose
**Capabilities**: All tools, general problem-solving
**Use For**: Research, multi-step tasks, general development
**Example**:
```python
Task(
    description="Research authentication patterns",
    prompt="Research OAuth2 implementation patterns for FastAPI",
    subagent_type="general-purpose"
)
```

### Specialized Types (Framework-Specific)
**Note**: Custom subagent types are defined in `.claude-library/REGISTRY.json`

Example custom types:
- `framework-architect`: System design
- `framework-engineer`: Implementation
- `framework-reviewer`: Code review
- `framework-validator`: Testing

---

## Best Practices

### 1. Clear Task Descriptions

**Good**:
```python
Task(
    description="Research FastAPI async patterns",
    prompt="""
    Research and summarize best practices for:
    1. Async route handlers in FastAPI
    2. Database connection pooling
    3. Error handling patterns

    Provide code examples for each.
    """,
    subagent_type="general-purpose"
)
```

**Bad**:
```python
Task(
    description="Research stuff",
    prompt="Look into FastAPI",
    subagent_type="general-purpose"
)
```

### 2. Provide Context

**Include in prompt**:
- What problem you're solving
- Any constraints or requirements
- Expected output format
- Related files or documentation

**Example**:
```python
Task(
    description="Implement user authentication",
    prompt="""
    Implement JWT-based authentication for our FastAPI app.

    Context:
    - Using PostgreSQL with SQLAlchemy
    - Need to support refresh tokens
    - Follow patterns in existing auth.py

    Requirements:
    - /login endpoint
    - /refresh endpoint
    - Middleware for protected routes

    Output:
    - Complete implementation
    - Unit tests
    - Usage documentation
    """,
    subagent_type="general-purpose"
)
```

### 3. Manage Dependencies

**Sequential for Dependencies**:
```python
# Design first
design = Task(description="Design", prompt="...", subagent_type="general-purpose")

# Implement using design
implement = Task(
    description="Implement",
    prompt=f"Implement this design:\n{design}",
    subagent_type="general-purpose"
)

# Test implementation
test = Task(
    description="Test",
    prompt=f"Test this implementation:\n{implement}",
    subagent_type="general-purpose"
)
```

**Parallel for Independence**:
```python
# Single message with multiple independent tasks
[
    Task(description="Build frontend", prompt="...", subagent_type="general-purpose"),
    Task(description="Build backend API", prompt="...", subagent_type="general-purpose"),
    Task(description="Build database schema", prompt="...", subagent_type="general-purpose")
]
```

### 4. Performance Optimization

**Minimize Context**:
- Only include necessary information
- Reference files instead of duplicating
- Use focused prompts

**Maximize Parallelism**:
- Identify independent tasks
- Launch in single message
- Aggregate results after

**Monitor Performance**:
- Track subagent duration
- Measure parallel speedup
- Use observability for insights

---

## Framework Integration

### With Local Observability

Subagents are automatically tracked:
- `observe_task_start.py` captures launch
- `observe_task_end.py` captures completion
- `track_artifact.py` captures outputs
- `validate_execution.py` validates against expectations

### With Agent Launcher

The framework's agent launcher coordinates subagents:
```markdown
## Agent Launcher Logic

1. Parse user request
2. Identify required agents
3. Determine parallel/sequential execution
4. Launch via Task tool
5. Aggregate results
6. Validate outputs
```

### With REGISTRY.json

Define custom subagent types:
```json
{
  "agents": {
    "my-specialist": {
      "path": ".claude-library/agents/specialized/my-specialist.md",
      "type": "specialized",
      "tools": ["Read", "Write"],
      "triggers": ["special task"],
      "contexts": ["my-context.md"]
    }
  }
}
```

Launch with:
```python
Task(
    description="Special task",
    prompt="Do the special thing",
    subagent_type="my-specialist"  # Matches REGISTRY.json
)
```

---

## Common Patterns

### Research → Implement → Test

```python
# Phase 1: Research (parallel)
research_results = [
    Task(description="Research API", prompt="...", subagent_type="general-purpose"),
    Task(description="Research DB", prompt="...", subagent_type="general-purpose"),
    Task(description="Research Auth", prompt="...", subagent_type="general-purpose")
]

# Phase 2: Design (sequential)
design = Task(
    description="Design system",
    prompt=f"Design based on:\n{research_results}",
    subagent_type="framework-architect"
)

# Phase 3: Implement (parallel)
implementations = [
    Task(description="Build API", prompt=f"Implement:\n{design.api}", subagent_type="general-purpose"),
    Task(description="Build DB", prompt=f"Implement:\n{design.db}", subagent_type="general-purpose")
]

# Phase 4: Test (sequential)
tests = Task(
    description="Test all",
    prompt=f"Test:\n{implementations}",
    subagent_type="framework-validator"
)
```

### Parallel Review

```python
# Implementation done, get multiple reviews in parallel
reviews = [
    Task(description="Security review", prompt="...", subagent_type="general-purpose"),
    Task(description="Performance review", prompt="...", subagent_type="general-purpose"),
    Task(description="Code quality review", prompt="...", subagent_type="general-purpose")
]
```

### Hierarchical Decomposition

```python
# Top-level coordination
coordinator = Task(
    description="Build feature",
    prompt="""
    Build user authentication feature.

    You should launch subagents for:
    1. Database schema design
    2. API implementation
    3. Frontend integration
    4. Testing

    Coordinate their work and ensure consistency.
    """,
    subagent_type="framework-architect"
)
# The coordinator launches its own subagents
```

---

## Troubleshooting

### Subagent Not Responding
- Check subagent_type is valid
- Verify prompt is clear
- Check for circular dependencies

### Slow Execution
- Minimize context in prompts
- Use parallel where possible
- Check observability for bottlenecks

### Inconsistent Results
- Provide more context
- Use sequential for dependencies
- Validate outputs with observer

---

## Resources

**Official Docs**:
- Subagents Guide: https://docs.claude.com/en/docs/claude-code/sub-agents.md
- Task Tool Reference: https://docs.claude.com/en/docs/claude-code/tools

**Framework Docs**:
- Agent Patterns: `AGENT_PATTERNS.md`
- Performance: `performance-optimization.md`
- Observability: `.claude-library/observability/README.md`

---

**Last Updated**: October 4, 2025
**Update Method**: `/update-docs` command or WebFetch
