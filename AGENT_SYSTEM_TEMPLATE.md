# Claude Code Agent System - Quick Start Template
*Start simple, grow naturally*

## IMPORTANT: Choose Your Setup Level

### MINIMAL Setup (Recommended Start)
**For:** Projects < 1000 lines, simple workflows
**Files:** 7 total
**Time:** 2 minutes

### STANDARD Setup
**For:** Projects 1000-10000 lines, moderate complexity
**Files:** 10-12 total
**Time:** 5 minutes

### FULL Setup
**For:** Projects > 10000 lines, complex systems
**Files:** 15-20 total
**Time:** 10 minutes

---

## MINIMAL Setup (START HERE)

### Step 1: Create Minimal Structure

```bash
# Create only essential directories
mkdir -p .claude/commands
mkdir -p .claude/agents          # NEW: Custom subagent types
mkdir -p .claude-library/agents/core
```

### Step 2: Create `.claude/settings.json`

This is the file Claude Code reads for hooks and permissions. There is no
`agent-launcher.md` — the harness routes on each agent's `description`
frontmatter, so a hand-rolled launcher only duplicates it and drifts.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude-library/hooks/scripts/format_code.sh" }
        ]
      }
    ]
  }
}
```

Hooks get their payload as **JSON on stdin**, never as shell variables — a
command like `script.sh "$file_path"` receives an empty string. Parse it with
`jq -r '.tool_input.file_path // empty'`.

Skip this file entirely if you have no hooks yet.

### Step 3: Create MINIMAL Core Agents

Each agent is a **pair**: a lean definition in `.claude/agents/` that Claude Code
loads, and a fuller playbook in `.claude-library/agents/core/` read on demand.

**The frontmatter is what makes it an agent.** Without it, Claude Code ignores
tools listed as prose under a `## Tools` heading and the agent runs with default
model, default effort, and every tool available.

`model` and `effort` are independent dials: model sets the capability floor,
effort sets reasoning depth. Note that **haiku is the only 200K-context model**;
everything else is 1M.

#### `.claude/agents/architect.md`

```markdown
---
name: architect
description: Designs structure and data models. Use for design work, architectural decisions, and planning how a feature fits.
model: opus
effort: xhigh
tools: Read, Write, Edit, Grep, Glob
---

Design simple, working solutions. Avoid over-engineering.

## Do
- Design basic structure, simple data models, minimal API specs

## Don't
- Over-architect, add unused patterns, create complex hierarchies

Full playbook: `.claude-library/agents/core/architect.md`
```

#### `.claude/agents/engineer.md`

```markdown
---
name: engineer
description: Implements features from a design. Use for building, coding, refactoring, and fixing.
model: opus
effort: high
tools: Read, Write, Edit, Grep, Glob, Bash
---

Write simple, working code. Don't over-engineer.

## Do
- Clean code, tests if they exist, basic error handling, existing patterns

## Don't
- Over-optimize prematurely, add unnecessary abstractions, anticipate future needs

Full playbook: `.claude-library/agents/core/engineer.md`
```

Note `tools` lists what the role needs. **Never `*`** — an engineer that can do
anything is an engineer with no boundaries.

#### `.claude/agents/reviewer.md`

```markdown
---
name: reviewer
description: Reviews code for correctness, security, and quality. Use for code review and pre-merge checks. Read-only.
model: opus
effort: high
tools: Read, Grep, Glob
---

Review for basics. Don't nitpick.

## Check For
- Does it work? Major bugs? Security issues in auth/payment code?

## Don't
- Request perfection, demand SOLID for a 100-line script

This role reports; it does not change files. Note that if `Bash` is ever added
here it is not sandboxed — read-only would then rest on convention.

Full playbook: `.claude-library/agents/core/reviewer.md`
```

### Step 3b: Launching Your Agents

Pass the filename in `.claude/agents/` as `subagent_type`. Claude Code applies
that agent's declared model, effort, and tools automatically — you do not repeat
them at the call site.

```python
Agent(
    description="Design auth system",
    prompt="Design authentication for this project",
    subagent_type="architect"          # -> .claude/agents/architect.md
)
```

The tool is named `Agent` (`Task` was its former name).

**A coordinator never propagates its own model.** If one agent launches others,
pass each sub-agent its own registry tier explicitly rather than letting it
inherit — otherwise an escalated coordinator silently escalates everything it
spawns, multiplying cost across a whole workflow for no benefit.

### Step 3c: Path-Specific Rules (Optional)

<!-- NEW in v2.0 -->

Create `.claude/rules/` to define rules that apply only when working with specific file paths:

Create `.claude/rules/tests.md`:
```markdown
---
globs: ["tests/**", "**/*.test.*", "**/*.spec.*"]
---
- Use pytest for all test files
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external services, use real database
- Minimum 80% branch coverage for new code
```

Create `.claude/rules/api.md`:
```markdown
---
globs: ["src/api/**", "src/routes/**"]
---
- All endpoints must have input validation
- Return consistent error format: { error: { code, message } }
- Include rate limiting on public endpoints
- Document with OpenAPI annotations
```

### Step 3d: Auto Memory (Optional)

<!-- NEW in v2.0 -->

Claude Code's auto memory system persists knowledge across conversations via `MEMORY.md`.

Create `.claude/MEMORY.md`:
```markdown
# Project Memory

## Architecture Decisions
- [Link to memory file about key decision]

## User Preferences
- [Link to memory file about preferred patterns]
```

Memory files are stored in `~/.claude/projects/<project>/memory/` and indexed by MEMORY.md. The system automatically loads relevant memories in future conversations.

**When to use memory vs contexts:**
- **Memory**: User preferences, project decisions, feedback — persists across conversations
- **Contexts**: Technical patterns, API docs, code conventions — loaded per-task

### Step 4: Create Single Build Command

Create `.claude/commands/build.md` (Start with ONE command only):

```markdown
# /build Command

Simple build command. Start here.

## Usage
`/build "feature description"`

## Workflow
1. Design (architect)
2. Implement (engineer)
3. Review (reviewer)

Keep it sequential. Add parallel only if >3 independent tasks.
```

---

## STANDARD Setup (Only if Minimal Insufficient)

Add these ONLY when minimal setup proves insufficient:

### Additional Commands (add one at a time as needed):
- `/debug` - When you hit first complex bug
- `/test` - When test suite exists
- `/deploy` - When deployment configured

### Directory Structure

```
project-root/
├── .claude/                   # Auto-loaded - keep lean
│   ├── agents/                # Subagent definitions (frontmatter + brief persona)
│   │   ├── architect.md
│   │   ├── engineer.md
│   │   └── reviewer.md
│   ├── commands/
│   │   └── build.md
│   ├── settings.json          # Hooks + permissions (the file the harness reads)
│   ├── rules/                 # Optional: path-specific rules
│   └── MEMORY.md              # Optional: cross-conversation memory index
└── .claude-library/
    ├── REGISTRY.json
    ├── agents/
    │   └── core/
    └── contexts/
```

### Workflow Orchestrator (only if needed)

**When to add**: Only when you have 5+ parallel tasks regularly

#### Workflow Orchestrator (`.claude-library/agents/core/workflow-orchestrator.md`)

```markdown
# Workflow Orchestrator

You are a workflow orchestrator that coordinates multi-agent workflows for complex tasks.

## Core Responsibilities
1. **Workflow Planning**: Break down complex tasks
2. **Agent Coordination**: Launch and manage agents
3. **Progress Tracking**: Monitor execution
4. **Result Synthesis**: Combine outputs
5. **Quality Gates**: Ensure requirements are met

## Workflow Patterns

### Sequential Workflow
```
Architect → Engineer → Reviewer
```

### Parallel Workflow
```
┌─ Agent A ─┐
├─ Agent B ─┼─→ Synthesis
└─ Agent C ─┘
```

### Hierarchical Workflow
```
Orchestrator
├─ Team A (Agent 1, Agent 2)
└─ Team B (Agent 3)
```

## Available Tools
- **Agent**: For spawning sub-agents (`Task` was its former name)
- **Read**: For reading results

## Execution Process
1. Analyze task complexity and select agents
2. Determine workflow pattern (sequential/parallel/hierarchical)
3. Launch agents, monitor progress
4. Synthesize results and validate quality gates

## Progress Reporting
- Pending / In Progress / Completed / Failed / Retrying
```

### Step 4: Create Your First Command

Create `.claude/commands/build.md`:

```markdown
# /build Command

## Purpose
Build features using TDD with multiple specialized agents.

## Usage
/build "Feature description"
/build "API endpoint for user authentication"

## Workflow
1. **Architecture & Planning** (Parallel): Architect + Test Planner + Researcher
2. **Implementation & Review** (Parallel): Engineer + Reviewer
3. **Integration**: Orchestrator validates and integrates

## Implementation
1. Load agent definitions from `.claude-library/agents/`
2. Load relevant contexts from `.claude-library/contexts/`
3. Execute agents in parallel where possible
4. Synthesize results and report completion

## Success Criteria
- All tests passing
- Code review approved
- Documentation complete
```

### Step 5: Create Registry

Create `.claude-library/REGISTRY.json`. Every agent needs `model` and `effort`,
and they must match that agent's frontmatter in `.claude/agents/` exactly — if
they disagree, the tier is prose that nothing enforces.

Agent names here must match the `.claude/agents/*.md` filenames. Use current tool
names (`Agent`, not `Task`; `Edit`, not `MultiEdit`), and never `["*"]`.

**Hooks do not go in this file.** Claude Code never reads it — hooks go in
`.claude/settings.json` (Step 2).

```json
{
  "version": "2.0.0",
  "project": "YOUR_PROJECT_NAME",
  "description": "Agent registry for YOUR_PROJECT",
  "agents": {
    "architect": {
      "name": "architect",
      "path": ".claude-library/agents/core/architect.md",
      "description": "Architecture design and specifications",
      "tools": ["Read", "Write", "Edit", "Grep", "Glob"],
      "model": "opus",
      "effort": "xhigh",
      "triggers": ["architecture", "design", "spec", "API", "database"],
      "type": "core",
      "domain": "architecture",
      "contexts": ["project.md"],
      "priority": 1
    },
    "engineer": {
      "name": "engineer",
      "path": ".claude-library/agents/core/engineer.md",
      "description": "Full-stack development and implementation",
      "tools": ["Read", "Write", "Edit", "Grep", "Glob", "Bash"],
      "model": "opus",
      "effort": "high",
      "triggers": ["implement", "code", "build", "fix", "debug"],
      "type": "core",
      "domain": "implementation",
      "contexts": ["project.md"],
      "priority": 1
    },
    "reviewer": {
      "name": "reviewer",
      "path": ".claude-library/agents/core/reviewer.md",
      "description": "Code review for quality and security",
      "tools": ["Read", "Grep", "Glob"],
      "model": "opus",
      "effort": "high",
      "triggers": ["review", "security", "performance", "quality"],
      "type": "core",
      "domain": "quality",
      "contexts": ["project.md"],
      "priority": 2
    }
  },
  "commands": {
    "build": {
      "path": ".claude/commands/build.md",
      "description": "Build features with TDD",
      "agents": ["architect", "engineer", "reviewer"],
      "workflow": "parallel-sequential"
    },
    "debug": {
      "path": ".claude/commands/debug.md",
      "description": "Debug issues",
      "agents": ["engineer"],
      "workflow": "single"
    },
    "review": {
      "path": ".claude/commands/review.md",
      "description": "Review code",
      "agents": ["reviewer"],
      "workflow": "single"
    }
  },
  "contexts": {
    "project": {
      "path": ".claude-library/contexts/project.md",
      "description": "Project configuration and setup"
    },
    "patterns": {
      "path": ".claude-library/contexts/patterns.md",
      "description": "Code patterns and conventions"
    }
  },
  "settings": {
    "auto_load_agents": false,
    "max_parallel_agents": 3,
    "cache_loaded_agents": true
  }
}
```

### Step 6: Create Project Context

Create `.claude-library/contexts/project.md`:

```markdown
# Project Context

## Overview
[Your project description]

## Tech Stack
- **Language**: [e.g., TypeScript, Python, Go]
- **Framework**: [e.g., Next.js, Django, FastAPI]
- **Database**: [e.g., PostgreSQL, MongoDB]
- **Testing**: [e.g., Jest, Pytest]

## Project Structure
```
src/
├── api/         # API routes
├── components/  # UI components
├── services/    # Business logic
├── models/      # Data models
└── tests/       # Test files
```

## Development Standards
- Code style: [e.g., ESLint, Black]
- Git flow: [e.g., feature branches]
- Testing: [minimum coverage]

## Common Commands
```bash
npm install    # Install dependencies
npm run dev    # Run development
npm test       # Run tests
npm run build  # Build production
```
```

### Step 7: Settings and Hooks

`.claude/settings.json` (created in Step 2) is the only config file Claude Code
reads. Add hooks here when you want something to happen automatically:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/.claude-library/hooks/scripts/format_code.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Two rules that decide whether a hook does anything at all:

1. **Payload arrives as JSON on stdin, not as shell variables.** `script.sh
   "$file_path"` receives an empty string — parse stdin instead.
2. **Never fail open, and use the right exit code.** For `PreToolUse`, **exit 2
   blocks**; exit 1 is a *non-blocking* error and the tool runs anyway. A hook
   that prints a block banner and exits 1 announces a block that never happened.
   Decide and emit the verdict before any logging that could throw.

Verify a new hook rather than assuming it runs:

```bash
echo '{"tool_input":{"file_path":"README.md"}}' | bash your_hook.sh   # does it work?
jq -e '.hooks.PostToolUse[0].hooks[0].command' .claude/settings.json  # exit 0 = valid
```

### Step 8: Write `GETTING_STARTED.md`

Put it in the project root. This is the artifact that explains what you built — six
months from now, or to a teammate who did not build it, the two directories alone say
nothing about how they work or whether they still do.

Cover, in this order:

1. **How to verify it works** — `python3 validate_agent_system.py .` and what a pass
   looks like. First, because it is the first thing anyone needs.
2. **What you created** — the `.claude/` vs `.claude-library/` split and why.
3. **The agents** — name, model/effort, and why that tier. Include the rule that a
   coordinator never propagates its model to agents it launches.
4. **How to use it** — available commands, and launching an agent by `subagent_type`.
5. **How to extend it** — adding an agent, a skill, a hook.
6. **The two rules broken most often**: registry and frontmatter must agree; hooks go in
   `.claude/settings.json`, never `REGISTRY.json`.

Describe what you actually built. A getting-started doc that does not match the system
on disk is worse than none — it sends people looking for things that are not there.

## Customization Guide

### Adding Specialized Agents

Create `.claude-library/agents/specialized/database-expert.md`:

```markdown
# Database Expert

You are a database specialist with expertise in schema design, query optimization, and data migrations.

## Core Responsibilities
1. Design efficient database schemas
2. Optimize queries for performance
3. Create data migrations
4. Implement indexing strategies
5. Ensure data integrity

## Specialized Knowledge
- Relational databases (PostgreSQL, MySQL), NoSQL (MongoDB, Redis)
- Query optimization, indexing strategies, transaction management
```

### Adding Custom Commands

Create `.claude/commands/optimize.md`:

```markdown
# /optimize Command

## Purpose
Optimize code for performance

## Usage
/optimize "database queries"
/optimize "frontend bundle size"

## Workflow
1. Analyze current performance
2. Identify bottlenecks
3. Implement optimizations
4. Measure improvements
```

### Adding Project-Specific Context

Create `.claude-library/contexts/api-patterns.md`:

```markdown
# API Patterns

## REST Conventions
- GET /resources - List
- GET /resources/:id - Get one
- POST /resources - Create
- PUT /resources/:id - Update
- DELETE /resources/:id - Delete

## Error Handling
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  }
}
```

## Authentication
- Bearer tokens in Authorization header
- JWT with refresh tokens
- Rate limiting per API key
```

## Testing Your Setup

### 1. Validate the system loads (do this first)

```bash
python3 validate_agent_system.py .
```

This catches what silently breaks a system: registry paths that do not resolve,
agents referencing missing contexts, a `subagent_type` naming an agent that does
not exist, missing or invalid `model`/`effort`, unparseable frontmatter, and
frontmatter that disagrees with the registry.

**Exit 0 means it will load. Non-zero means agents fail at launch — fix first.**

### 2. Confirm agents are registered

Your agents should appear as launchable types. If an agent is missing, its
frontmatter did not parse — check that the file opens with `---` on line 1 and
that `name` matches the filename.

### 3. Test routing by intent

- `"I need to design a REST API"` -> architect
- `"Review this for security issues"` -> reviewer
- `/build user authentication` -> your build workflow

If the wrong agent is chosen, fix its `description` — that is what the harness
routes on, not the filename or the `triggers` array.

### 4. Confirm hooks fire

Edit a file the hook matches and check the side effect actually happened. A hook
that silently does nothing looks identical to one that works.

## Scaling Your System

### Progressive Enhancement
1. **Start Simple**: Begin with core agents
2. **Add Specialization**: Create domain-specific agents
3. **Optimize Workflows**: Identify parallel opportunities
4. **Refine Contexts**: Add patterns as you discover them
5. **Measure Performance**: Track execution times

### Performance Metrics
- Context size: < 10KB in .claude/
- Agent loading: < 2 seconds
- Parallel execution: 3x faster than sequential
- Cache hit rate: > 60%

## Troubleshooting

### Common Issues

**Agents not loading:**
- Check REGISTRY.json syntax
- Verify file paths are correct
- Ensure triggers match user input

**Slow performance:**
- Reduce context size
- Use parallel execution
- Cache frequently used agents

**Conflicts between agents:**
- Define clear boundaries
- Use explicit triggers
- Separate concerns properly

## Next Steps

1. **Customize agents** for your domain
2. **Create specialized commands** for common tasks
3. **Build context library** with patterns
4. **Test parallel workflows** for speed
5. **Document your customizations**

---

*This template provides everything you need to get started. Customize it for your specific project needs.*
