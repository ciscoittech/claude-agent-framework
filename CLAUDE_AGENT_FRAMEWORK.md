# The Claude Code Agent System Framework
*A Comprehensive Guide to Building Effective Multi-Agent Development Systems*

## Table of Contents
1. [Introduction](#introduction)
2. [Core Philosophy](#core-philosophy)
3. [System Architecture](#system-architecture)
4. [Agent Design Principles](#agent-design-principles)
5. [Skills (Commands)](#skills-commands)
6. [Command Workflows](#command-workflows)
6. [Context Management](#context-management)
7. [Extended Context & Tool Search](#extended-context--tool-search)
8. [Tool Configuration](#tool-configuration)
9. [Parallel Execution](#parallel-execution)
10. [Agent Teams](#agent-teams)
11. [Best Practices](#best-practices)
12. [Performance Optimization](#performance-optimization)
13. [Hooks (Optional)](#hooks-optional)

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
│   ├── settings.json            # Hooks and permissions - nothing else
│   ├── agents/                  # Subagent definitions: frontmatter + persona
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

### How routing actually works

Earlier versions of this framework put a hand-written `agent-launcher.md` in
`.claude/` and asked it to parse intent and dispatch. **Do not generate one.**
Claude Code already does this, and does it from a field you control: each
subagent's `description` in `.claude/agents/<name>.md` frontmatter. A launcher
file competes with that routing rather than driving it, and it is auto-loaded
context paid for on every session.

What this means in practice:

1. **`description` is the routing surface.** Write what the agent is for and when
   to reach for it, in the words a request would use. That string is what the
   dispatcher matches on.
2. **`REGISTRY.json` is framework metadata, not a dispatch table.** Claude Code
   never reads it. It exists so the framework's own tooling - the validator, the
   generator, the commands - has one source of truth.
3. **Commands are the explicit path.** `.claude/commands/<name>.md` is invoked as
   `/name` and orchestrates agents deliberately, for work where you do not want
   the router deciding.

## Agent Design Principles

### Agent Definition Structure

**An agent is two files.** The split is not organizational tidiness - the stub's
body becomes the subagent's system prompt and is paid on every launch, while the
playbook is read only when the agent needs it.

**`.claude/agents/<name>.md`** - the real definition. Frontmatter is mandatory;
without it the tier declarations are unenforced prose and the agent inherits
whatever the session is running. Keep the body under ~100 lines.

```markdown
---
name: architect
description: Designs system structure and interfaces. Use for design decisions, choosing patterns, and planning how a new component fits.
model: opus
effort: xhigh
tools: Read, Write, Edit, Grep, Glob
---

You are a system architect. You decide structure and interfaces; you do not
implement.

## When you are the right agent
Design questions, architectural trade-offs, planning a component's shape.
Not: writing the implementation, reviewing finished code.

## Before you start
Read `.claude-library/agents/core/architect.md` for the full playbook.
```

Required keys, exactly these: `name`, `description`, `model`, `effort`, `tools`.
`color` is optional. `tools` is a **comma-separated string**, never a YAML list.
`name` must equal the filename. `description` is the routing surface - see *How
routing actually works* above.

**`.claude-library/agents/core/<name>.md`** - the playbook. Size is not a
constraint here. This is where the responsibilities, boundaries, output format,
worked examples, and failure modes live:

```markdown
# Architect

## Core Responsibilities
1. **Primary Task**: What this agent primarily does
2. **Secondary Tasks**: Supporting activities
3. **Quality Assurance**: How it ensures quality

## What You SHOULD Do / SHOULD NOT Do
Boundaries, anti-patterns, and which work belongs to another agent.

## Output Format
The exact shape the caller expects back.

## Success Criteria
Measurable outcomes and quality gates.
```

`REGISTRY.json` declares the same `model`, `effort`, and `tools` as the stub's
frontmatter. `validate_agent_system.py` fails if the two disagree - a tier that
exists only in the registry is a tier nothing enforces.

### Tool Configuration Guidelines

Agents should only have access to tools they need:

| Agent Type | Typical Tools | Restricted Tools |
|------------|--------------|------------------|
| **Architect** | Read, Write, Grep, Glob | Bash |
| **Engineer** | Read, Write, Edit, Grep, Glob, Bash | Agent |
| **Reviewer** | Read, Grep, Glob, Bash | Write, Edit |
| **Orchestrator** | Agent, Read, Grep, Glob | Write, Edit, Bash |
| **Debugger** | Read, Edit, Grep, Glob, Bash | Write |

Never grant `*`. A wildcard is not a shortcut for "I have not decided yet" - it
is a decision to grant everything, and the validator rejects it. The subagent
tool is named **`Agent`**; `Task` is its former name and matches nothing.

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

## Skills

A **skill** is a procedure a user invokes as `/name`. Two forms exist:

- `.claude/commands/<name>.md` — what this framework uses and what the validator checks.
- `.claude/skills/<name>/SKILL.md` — the richer form, supporting bundled resources and
  path-scoped auto-activation. A `SKILL.md` takes precedence over a same-named command
  file. Reach for it when a skill needs more than one file.

Either way the skill is declared in `REGISTRY.json`'s `skills` section.

### Skill vs agent vs neither

This is the decision that matters, and most of the time the answer is "neither".

| You have | Build |
|---|---|
| A repeatable procedure with known steps that a person triggers | **Skill** |
| A role that exercises judgment across varying inputs | **Agent** |
| A one-off instruction, or something a direct tool call handles | **Neither** |

A skill is a *procedure*; an agent is a *role*. `/review-code` is a skill — the steps
are known, a human starts it. `framework-code-reviewer` is an agent — it decides what
matters in code it has not seen before. The skill can launch the agent; they are not
alternatives to each other.

Per SIMPLICITY_ENFORCEMENT, do not create either until the direct approach has actually
failed. A skill that wraps one tool call is worse than the tool call.

This table is the short version. [learn/01-four-surfaces.md](./learn/01-four-surfaces.md)
adds the two surfaces it omits — hooks and `CLAUDE.md` — and the cost model that decides
between them: a skill's body is a recurring context cost, a subagent's window is discarded,
and a hook is the only one the model cannot skip.

**On the vocabulary.** `REGISTRY.json` has a `skills{}` section and a `commands{}` section,
and the files live in `.claude/commands/`. These are not three concepts. `skills{}` is the
declaration that reaches the file — description, tool pre-approval, invocation control.
`commands{}` is orchestration wiring: which agents a command drives. The directory name is
just where this repo keeps them.

### Required frontmatter

**Frontmatter is what gives you control.** Without it a command still loads — Claude
Code falls back to the first paragraph for a description — but you get whatever that
paragraph happens to say, no tool pre-approval, and no way to opt out of model
invocation. The declared form is the one you can reason about.

```markdown
---
description: Review code changes for bugs, security issues, and quality
allowed-tools: Read, Grep, Glob, Agent, Bash(git diff:*)
---
```

- **`description`** — what the model matches on. Write what the command *does*, not what
  it is called. This is the field that makes a skill discoverable.
- **`allowed-tools`** — **pre-approves** tools; it does not sandbox them. Unlisted tools
  remain callable and fall through to your normal permission settings, so an incomplete
  list causes prompts (or denials in non-interactive runs), not hard failures. Scope
  `Bash` with permission-rule syntax: `Bash(git diff:*)` pre-approves exactly that, where
  bare `Bash` pre-approves everything. Never `*` or `Bash(*)`.
  Use `disallowed-tools` when you need to actually restrict.
  Note a rule matches each command independently — `Bash(git diff:*)` does not cover
  `git diff | head`, and it does not cover `gh pr diff`.
- **`disable-model-invocation: true`** — optional. Set it when the skill is expensive or
  far-reaching enough that firing it should be a deliberate human act. `/build-feature`
  sets it because it spawns a chain across eight agents.

### The registry and the file must agree

`REGISTRY.json` declares each skill's `description` and `allowed_tools`; the file repeats
them in frontmatter. `validate_agent_system.py` fails if they drift, if a command has no
registry entry, or if frontmatter is missing.

This mirrors how agents work, and for the same reason: a declaration the harness never
reads is decoration. `REGISTRY.json` is framework metadata — Claude Code reads
`.claude/commands/*.md` frontmatter, and nothing else.

### Adding a skill

1. Add an entry to `REGISTRY.json` -> `skills` with `path`, `description`, `allowed_tools`.
2. Create `.claude/commands/<name>.md` with matching frontmatter.
3. Write the procedure in the body — steps, not prose.
4. Run `python3 validate_agent_system.py .` — it fails on any disagreement.

---

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

Commands use the `Agent` tool to launch subagents. Name the real
`subagent_type` - the persona already lives in `.claude/agents/<name>.md`, so
pasting it into the prompt duplicates it and pays for it twice:

```javascript
// Parallel execution - all Agent calls in ONE message
Agent({
  subagent_type: "architect",
  description: "Architecture design",
  prompt: "Design the architecture for: {feature}"
})
Agent({
  subagent_type: "test-engineer",
  description: "Test specifications",
  prompt: "Write test specs for: {feature}"
})
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

### Leveraging Claude Code's Agent Tool

The `Agent` tool enables parallel subagent execution. (`Task` was its former
name; nothing answers to it now.)

```javascript
// WRONG - Sequential (slow)
await runAgent('architect');
await runAgent('test-writer');
await runAgent('researcher');

// RIGHT - Parallel (fast)
// Send all Agent calls in ONE message
[
  Agent({subagent_type: 'architect',    prompt: prompt1}),
  Agent({subagent_type: 'test-writer',  prompt: prompt2}),
  Agent({subagent_type: 'researcher',   prompt: prompt3})
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
---
name: security-reviewer
description: Reviews code for OWASP Top 10 vulnerabilities. Use for security review of auth, input handling, and anything touching user data.
model: sonnet
effort: high
tools: Read, Grep, Glob
---

You are a security-focused code reviewer specializing in OWASP Top 10 vulnerabilities.

## Responsibilities
- Review code for injection, XSS, CSRF vulnerabilities
- Check authentication and authorization logic
- Verify input validation and output encoding

## Output Format
Report findings as: severity (Critical/High/Medium/Low), location, description, fix.
```

The tool grant lives in `tools:`, not in a prose section - a "## Tools" heading
listing read-only access grants nothing. `model` and `effort` are two independent
dials: `model` is the capability floor, `effort` is how much reasoning it spends
there. See `MODEL_SELECTION.md`.

### Using Custom Agent Types

```python
# Launch with a custom type instead of general-purpose
Agent(
    description="Security review of auth module",
    prompt="Review src/auth/ for security vulnerabilities",
    subagent_type="security-reviewer"  # matches .claude/agents/security-reviewer.md
)
```

### Agent Teams in Workflows

```python
# Parallel team of specialists
[
    Agent(description="Security review", prompt="...", subagent_type="security-reviewer"),
    Agent(description="Performance review", prompt="...", subagent_type="performance-analyst"),
    Agent(description="Code quality", prompt="...", subagent_type="reviewer")
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
   - Lean agent stubs - frontmatter plus a short persona, depth in the library
   - `settings.json` for hooks and permissions only
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
  "version": "2.0.0",
  "agents": {
    "architect": {
      "path": ".claude-library/agents/core/architect.md",
      "type": "core",
      "domain": "architecture",
      "tools": ["Read", "Write", "Edit", "Grep", "Glob"],
      "model": "opus",
      "effort": "xhigh",
      "triggers": ["design", "architecture", "spec"],
      "contexts": ["project.md"],
      "priority": 1
    },
    "engineer": {
      "path": ".claude-library/agents/core/engineer.md",
      "type": "core",
      "domain": "implementation",
      "tools": ["Read", "Write", "Edit", "Grep", "Glob", "Bash"],
      "model": "sonnet",
      "effort": "high",
      "triggers": ["implement", "build", "fix"],
      "contexts": ["project.md"],
      "priority": 1
    },
    "reviewer": {
      "path": ".claude-library/agents/core/reviewer.md",
      "type": "core",
      "domain": "quality",
      "tools": ["Read", "Grep", "Glob"],
      "model": "sonnet",
      "effort": "high",
      "triggers": ["review", "quality"],
      "contexts": ["project.md"],
      "priority": 2
    }
  },
  "commands": {
    "feature": {
      "path": ".claude/commands/feature.md",
      "agents": ["architect", "engineer", "reviewer"],
      "workflow": "parallel-sequential"
    }
  },
  "contexts": {
    "project": {
      "path": ".claude-library/contexts/project.md",
      "description": "Stack, conventions, and layout"
    }
  },
  "skills": {
    "feature": {
      "path": ".claude/commands/feature.md",
      "description": "Build the feature described, using the project's agents",
      "allowed_tools": ["Agent", "Read", "Write", "Edit", "Grep", "Glob"]
    }
  }
}
```

Two path conventions, and mixing them is the most common generation error:
`path` is **repo-root-relative**, while `contexts[]` entries are **bare
filenames** resolved against `.claude-library/contexts/`. `model` and `effort`
must match the agent's frontmatter exactly. Keys are `type` and `domain` - not
`category`, not `file`.

### Workflow Optimization

1. **Batch operations**: Group similar tasks
2. **Parallel by default**: Unless dependencies exist
3. **Progressive loading**: Start with minimal context
4. **Early termination**: Stop on critical failures

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
          "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude-library/hooks/scripts/format_code.sh"
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
*Optional Hooks patterns for production workflows*