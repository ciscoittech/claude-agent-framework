# The Claude Code Agent System Framework
*A Comprehensive Guide to Building Effective Multi-Agent Development Systems*

## Table of Contents
1. [Introduction](#introduction)
2. [Core Philosophy](#core-philosophy)
3. [System Architecture](#system-architecture)
4. [Agent Design Principles](#agent-design-principles)
5. [Command Workflows](#command-workflows)
6. [Context Management](#context-management)
7. [Extended Context & Tool Search](#extended-context--tool-search)
8. [Tool Configuration](#tool-configuration)
9. [Parallel Execution](#parallel-execution)
10. [Agent Teams](#agent-teams)
11. [Best Practices](#best-practices)
12. [Performance Optimization](#performance-optimization)
13. [Observability (Optional)](#observability-optional)
14. [Hooks (Optional)](#hooks-optional)

## Introduction

This framework enables you to build sophisticated multi-agent development systems using Claude Code's capabilities. Based on proven patterns from production systems, it emphasizes **performance through minimal context loading**, **parallel agent execution**, and **clear workflow orchestration**.

### Key Benefits
- **97% reduction** in auto-loaded context (250KB → 8KB)
- **3x faster execution** through parallel agent processing
- **Project-agnostic** - works with any tech stack
- **Progressive complexity** - start simple, scale as needed

## Core Philosophy

### 1. Minimal Auto-Loading
Only load what's essential at startup:
- `.claude/` folder contains minimal configuration (< 10KB)
- `.claude-library/` holds all agents, contexts, and commands
- Dynamic loading based on task requirements

### 2. Agent Specialization
Each agent has:
- **Single responsibility** (architecture OR implementation OR review)
- **Clear boundaries** (what it should and shouldn't do)
- **Defined tools** (only the tools it needs)
- **Explicit triggers** (keywords that activate it)

### 3. Workflow-Driven Development
Commands orchestrate agents through defined workflows:
- **Sequential**: One agent completes before the next starts
- **Parallel**: Multiple agents work simultaneously
- **Hierarchical**: Parent agents spawn child agents

## System Architecture

### Directory Structure
```
project-root/
├── .claude/                      # Minimal auto-loaded configuration
│   ├── agent-launcher.md        # Dynamic agent loader (5-10KB)
│   ├── settings.json            # Project metadata
│   ├── agents/                  # Custom subagent types (NEW)
│   │   ├── security-reviewer.md
│   │   └── performance-analyst.md
│   └── commands/                # User-facing commands
│       ├── feature-loop.md     # TDD workflow command
│       ├── debug.md            # Debugging command
│       └── deploy.md           # Deployment command
│
└── .claude-library/             # On-demand agent library
    ├── REGISTRY.json           # Central agent/command registry
    ├── agents/                 # Specialized agents
    │   ├── core/              # Core workflow agents
    │   │   ├── architect.md   # System design
    │   │   ├── engineer.md    # Implementation
    │   │   └── reviewer.md    # Code review
    │   └── specialized/       # Domain-specific agents
    │       ├── database.md    # Database specialist
    │       └── api.md         # API specialist
    └── contexts/              # Shared knowledge bases
        ├── project.md         # Project configuration
        ├── patterns.md        # Code patterns
        └── standards.md       # Coding standards
```

### The Agent Launcher

The `agent-launcher.md` is your system's brain. It:
1. **Analyzes** user requests to determine intent
2. **Loads** appropriate agents from the library
3. **Routes** tasks to the right agents
4. **Manages** context loading dynamically

```markdown
# Agent Launcher

You are the agent launcher for [PROJECT NAME]. Your role is to:
1. Parse user requests to determine intent
2. Load appropriate agents from `.claude-library/`
3. Route tasks to correct agents
4. Manage context loading as needed

## Quick Commands
- `/feature "description"` - Build new feature
- `/debug "issue"` - Debug problems
- `/review` - Review code

## Loading Strategy
1. If input starts with `/`, load from `.claude/commands/`
2. Match keywords to agents in REGISTRY.json
3. Load relevant contexts based on task
```

## Agent Design Principles

### Agent Definition Structure

Every agent should follow this template:

```markdown
# [Agent Name]

You are a [role] specializing in [domain]. Your expertise includes [specific skills].

## Core Responsibilities
1. **Primary Task**: What this agent primarily does
2. **Secondary Tasks**: Supporting activities
3. **Quality Assurance**: How it ensures quality

## What You SHOULD Do
- Specific positive actions
- Expected behaviors
- Quality standards to maintain

## What You SHOULD NOT Do
- Boundaries and limitations
- Tasks for other agents
- Anti-patterns to avoid

## Available Tools
You have access to these tools:
- **Read**: For reading files
- **Write**: For creating files
- **Edit**: For modifying files
- **Task**: For spawning sub-agents (if orchestrator)
- [Other specific tools]

## Interaction Patterns
- How to communicate with users
- Output format specifications
- Progress reporting style

## Success Criteria
- Measurable outcomes
- Quality gates
- Performance targets
```

### Tool Configuration Guidelines

Agents should only have access to tools they need:

| Agent Type | Typical Tools | Restricted Tools |
|------------|--------------|------------------|
| **Architect** | Read, Write, Grep | Bash, Edit (limited) |
| **Engineer** | All tools (*) | None (full access) |
| **Reviewer** | Read, Grep, Glob | Write, Edit, Bash |
| **Orchestrator** | Task, Read | Direct file editing |
| **Debugger** | Read, Bash, Edit | Write (new files) |

### Agent Categories

Organize agents by function:

1. **Core Agents** (Always needed)
   - System Architect: Design and specifications
   - Senior Engineer: Implementation
   - Code Reviewer: Quality assurance
   - Workflow Orchestrator: Multi-agent coordination

2. **Specialized Agents** (Domain-specific)
   - Database Specialist: Schema, queries, optimization
   - API Architect: Endpoint design, contracts
   - Security Auditor: Vulnerability scanning
   - Performance Engineer: Optimization

3. **Utility Agents** (Support functions)
   - Documentation Writer: Docs and comments
   - Test Engineer: Test creation and execution
   - Deployment Manager: CI/CD and releases

## Command Workflows

### The Feature-Loop Pattern

The `/feature-loop` command demonstrates optimal workflow design:

```markdown
# /feature-loop Command

## Purpose
Complete TDD feature development using parallel agents

## Workflow Stages

### Stage 1: Parallel Analysis (3 agents)
All agents run SIMULTANEOUSLY:
- Architecture Agent: Design system structure
- Test Spec Agent: Create test specifications
- Research Agent: Find existing patterns

### Stage 2: Implementation & Review (2 agents)
Running in parallel:
- Implementation Agent: Write code (TDD style)
- Review Agent: Real-time quality checks

### Stage 3: Integration (1 agent)
- Integration Agent: Final validation
```

### Command Implementation

Commands use the Task tool to launch agents:

```javascript
// Parallel execution - all tasks in ONE message
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Architecture design</description>
  <prompt>
    [Load agent persona from .claude-library/agents/architect.md]
    [Include relevant contexts]
    Design architecture for: {feature}
  </prompt>
</Task>
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Test specifications</description>
  <prompt>
    [Load test engineer persona]
    Create comprehensive test specs for: {feature}
  </prompt>
</Task>
```

### Workflow Patterns

1. **Sequential Workflow**
   ```
   Architect → Engineer → Reviewer → Deploy
   ```
   Use when: Tasks depend on previous outputs

2. **Parallel Workflow**
   ```
   ┌─ Architect ─┐
   ├─ Tests ─────┼─→ Synthesis
   └─ Research ──┘
   ```
   Use when: Tasks are independent

3. **Hierarchical Workflow**
   ```
   Orchestrator
   ├─ Debug Team
   │   ├─ Frontend Debugger
   │   └─ Backend Debugger
   └─ Fix Team
       └─ Engineer
   ```
   Use when: Complex problems need decomposition

## Context Management

### Context Design Principles

Contexts provide shared knowledge without agent-specific instructions:

```markdown
# [Context Name]

## Overview
Brief description of what this context provides

## Key Information
- Data models
- API structures
- Configuration values
- Project patterns

## Code Examples
\`\`\`language
// Example implementations
\`\`\`

## Important Notes
- Gotchas
- Performance considerations
- Security requirements
```

### Dynamic Context Loading

Load contexts based on task requirements:

```javascript
function selectContexts(task) {
  const contexts = [];

  // Always load core context
  contexts.push('project.md');

  // Conditionally load specialized contexts
  if (task.includes('database')) {
    contexts.push('database-patterns.md');
  }
  if (task.includes('api')) {
    contexts.push('api-standards.md');
  }

  return contexts;
}
```

## Extended Context & Tool Search

<!-- NEW in v2.0 -->

### Extended Context Window
Claude Code now supports up to 1M tokens of context. This means:
- Agents can process entire codebases in a single pass
- Less need for aggressive context pruning on small-medium projects
- Large file reads (up to 2000 lines default) are more practical

### MCP Tool Search (Deferred Loading)
Tools from MCP servers can be loaded on-demand rather than all at startup:

```python
# Search for a tool by name or keyword
ToolSearch(query="select:mcp__github__create_issue")

# Keyword search for relevant tools
ToolSearch(query="database query", max_results=5)
```

This reduces initial context load and enables access to hundreds of MCP tools without upfront cost.

## Tool Configuration

### MCP Tools Integration

When using MCP tools, follow these guidelines:

1. **Prefer MCP tools** when available (they start with `mcp__`)
2. **Document tool access** in agent definitions
3. **Restrict dangerous operations** appropriately

Example MCP tool usage:
```markdown
## Available Tools
- `mcp__playwright__browser_navigate`: Web navigation
- `mcp__playwright__browser_snapshot`: Page analysis
- `mcp__nuxt-ui-remote__get_component`: UI components
```

### Tool Restrictions

Define what agents should NOT do:

```markdown
## Tool Restrictions
- NEVER use `find` or `grep` commands (use Grep tool)
- NEVER use `cat` or `tail` (use Read tool)
- AVOID creating new files (prefer editing existing)
- NEVER commit without explicit user request
```

### Managed Settings

Claude Code supports managed settings via `~/.claude/settings.json` and project `.claude/settings.json`:
- Permission presets (auto-approve specific tools)
- MCP server configurations
- Model preferences and effort levels
- Hook configurations

These replace manual CLAUDE.md instructions for tool permissions.

## Parallel Execution

### Leveraging Claude Code's Task Tool

The Task tool enables parallel agent execution:

```javascript
// WRONG - Sequential (slow)
await runAgent('architect');
await runAgent('test-writer');
await runAgent('researcher');

// RIGHT - Parallel (fast)
// Send all Tasks in ONE message
[
  Task('architect', prompt1),
  Task('test-writer', prompt2),
  Task('researcher', prompt3)
]
```

### Parallel Execution Benefits

| Execution Type | 3 Agents Time | 5 Agents Time | Efficiency |
|---------------|---------------|---------------|------------|
| Sequential | 90 seconds | 150 seconds | Baseline |
| Parallel | 30 seconds | 30 seconds | 3-5x faster |

### When to Use Parallel Execution

**Good for Parallel:**
- Independent analysis tasks
- Multiple file searches
- Separate component development
- Different test types

**Keep Sequential:**
- Dependent tasks (output feeds next input)
- Progressive refinement
- Validation chains

## Agent Teams

<!-- NEW in v2.0 -->

Claude Code now supports **custom subagent types** defined in `.claude/agents/`. This replaces the need for `general-purpose` with persona-loaded prompts.

### Defining Custom Agent Types

Create `.claude/agents/<agent-name>.md`:

```markdown
# Security Reviewer

You are a security-focused code reviewer specializing in OWASP Top 10 vulnerabilities.

## Responsibilities
- Review code for injection, XSS, CSRF vulnerabilities
- Check authentication and authorization logic
- Verify input validation and output encoding

## Tools
- Read, Grep, Glob (read-only access)

## Output Format
Report findings as: severity (Critical/High/Medium/Low), location, description, fix.
```

### Using Custom Agent Types

```python
# Launch with custom type instead of general-purpose
Task(
    description="Security review of auth module",
    prompt="Review src/auth/ for security vulnerabilities",
    subagent_type="security-reviewer"  # matches .claude/agents/security-reviewer.md
)
```

### Agent Teams in Workflows

```python
# Parallel team of specialists
[
    Task(description="Security review", prompt="...", subagent_type="security-reviewer"),
    Task(description="Performance review", prompt="...", subagent_type="performance-analyst"),
    Task(description="Code quality", prompt="...", subagent_type="code-reviewer")
]
```

### Team Composition Patterns

| Project Type | Recommended Team | Agent Count |
|-------------|-----------------|-------------|
| Simple feature | engineer, reviewer | 2 |
| API endpoint | architect, engineer, api-specialist | 3 |
| Security-critical | engineer, security-reviewer, reviewer | 3 |
| Full feature | architect, engineer, reviewer, test-engineer | 4 |

## Best Practices

### 1. Agent Identity

Each agent needs clear identity:
```markdown
You are a [specific role] with expertise in [domain].
Your primary responsibility is [main task].
You excel at [specific skills].
```

### 2. Explicit Boundaries

Define what agents should NOT do:
```markdown
## What You Should NOT Do
- Create files unless absolutely necessary
- Make architectural decisions (that's for architect)
- Commit code without user approval
- Access production systems
```

### 3. Output Specifications

Standardize agent outputs:
```markdown
## Output Format
- Use markdown for documentation
- Include file paths as `path:line`
- Provide progress indicators
- Return structured data when possible
```

### 4. Error Handling

Define failure behaviors:
```markdown
## Error Handling
1. Identify the error type
2. Attempt automatic recovery if safe
3. Escalate to user with clear explanation
4. Suggest alternative approaches
```

### 5. Progress Reporting

Keep users informed:
```markdown
Stage 1/3: Architecture Design
[complete] Architecture complete
Stage 2/3: Implementation
[in progress] Writing code (60% complete)...
```

## Performance Optimization

### Context Reduction Strategies

1. **Minimal .claude folder** (< 10KB)
   - Only agent-launcher.md
   - Basic settings.json
   - Command shortcuts

2. **On-demand loading** from .claude-library
   - Agents loaded when needed
   - Contexts loaded based on task
   - Unload after completion

3. **Smart caching**
   - Cache frequently used agents
   - Reuse loaded contexts
   - Clear cache periodically

### Registry Optimization

Structure your REGISTRY.json for fast lookup:

```json
{
  "version": "1.0.0",
  "settings": {
    "auto_load_agents": false,
    "max_parallel_agents": 3,
    "cache_loaded_agents": true
  },
  "agents": {
    "architect": {
      "path": ".claude-library/agents/architect.md",
      "tools": ["Read", "Write", "Grep"],
      "triggers": ["design", "architecture", "spec"],
      "category": "core",
      "priority": 1
    }
  },
  "commands": {
    "feature": {
      "path": ".claude/commands/feature.md",
      "agents": ["architect", "engineer", "reviewer"],
      "workflow": "parallel-sequential"
    }
  }
}
```

### Workflow Optimization

1. **Batch operations**: Group similar tasks
2. **Parallel by default**: Unless dependencies exist
3. **Progressive loading**: Start with minimal context
4. **Early termination**: Stop on critical failures

## Observability (Optional)

Track agent workflows with real-time monitoring. Two options:

1. **Local Observability** (SQLite-based, zero dependencies): See `.claude-library/observability/README.md`
2. **Cloud Observability** (Logfire): Enable in REGISTRY.json with `"observability": { "enabled": true }`

Features: workflow traces, output validation, performance metrics, error tracking.

Enable via REGISTRY.json settings:
```json
{
  "settings": {
    "observability": {
      "enabled": true,
      "provider": "logfire"
    }
  }
}
```

See `.claude-library/observability/README.md` for full setup, configuration, and troubleshooting.

## Hooks (Optional)

Add deterministic control via shell commands at workflow points:
- **PreToolUse**: Security checks, validation (can block operations)
- **PostToolUse**: Formatting, notifications
- **Stop/SubagentStop**: Team alerts, validation

Configure in `.claude/settings.json` or project settings:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "bash .claude-library/hooks/scripts/format_code.sh \"$file_path\""
        }]
      }
    ]
  }
}
```

See Claude Code docs for the full hook event reference and `.claude-library/hooks/README.md` for pre-built configurations.

## Conclusion

This framework provides a battle-tested approach to building sophisticated agent systems with Claude Code. By following these patterns, you can create systems that are:

- **Fast**: Through parallel execution and minimal context loading
- **Maintainable**: With clear separation of concerns
- **Scalable**: From simple commands to complex workflows
- **Reliable**: With defined boundaries and error handling
- **Project-agnostic**: Adaptable to any technology stack

Remember: Start simple with core agents, then progressively add specialization as your needs grow. The framework scales with your project's complexity.

## References

- [Building Effective Agents - Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)

---

*Framework Version 2.0 - Now with Agent Teams, Extended Context, and MCP Tool Search*
*Optional Hooks and Observability patterns for production workflows*