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

### Step 2: Create Minimal Agent Launcher

Create `.claude/agent-launcher.md` (Keep under 1KB):

```markdown
# [PROJECT NAME] Agent Launcher

Minimal agent launcher. Loads only essential agents.

## Available Command
- `/build "description"` - Build features (only command initially)

## Core Agents (3 only)
- `architect` - Design structure
- `engineer` - Implement code
- `reviewer` - Review quality

## Simple Loading
1. Try direct command first
2. Load agent only if needed
3. Keep context minimal

## Simplicity First
- Don't over-engineer
- Start with basics
- Add complexity only when proven necessary
```

### Step 3: Create MINIMAL Core Agents

#### Minimal Architect (`.claude-library/agents/core/architect.md`)

```markdown
# Minimal Architect

Design simple, working solutions. Avoid over-engineering.

## Do
- Design basic structure
- Define simple data models
- Create minimal API specs

## Don't
- Over-architect
- Add unused patterns
- Create complex hierarchies

## Tools
- Read, Write, Grep, Glob

Keep it simple. Add complexity only when needed.
```

#### Minimal Engineer (`.claude-library/agents/core/engineer.md`)

```markdown
# Minimal Engineer

Write simple, working code. Don't over-engineer.

## Do
- Write clean code
- Add tests if they exist
- Handle basic errors
- Follow existing patterns

## Don't
- Over-optimize prematurely
- Add unnecessary abstractions
- Create complex patterns
- Anticipate future needs

## Tools
All tools available (*)

Start simple. Ship working code.
```

#### Minimal Reviewer (`.claude-library/agents/core/reviewer.md`)

```markdown
# Minimal Reviewer

Review for basics. Don't nitpick.

## Check For
- Does it work?
- Major bugs?
- Security issues if auth/payment code?
- Follows existing patterns?

## Don't
- Request perfection
- Add unnecessary complexity
- Require 80% coverage for simple project
- Demand SOLID for 100-line script

## Tools
Read, Grep, Glob

Ship working code, not perfect code.
```

### Step 3b: Create Custom Subagent Types (Optional)

<!-- NEW in v2.0 -->

Custom subagent types let you define specialized agents that Claude Code can launch by name.

Create `.claude/agents/architect.md`:
```markdown
You are a system architect. Design simple, working solutions.

## Focus
- Basic structure and data models
- Minimal API specs
- Follow existing patterns

## Tools
Read, Write, Grep, Glob
```

Create `.claude/agents/reviewer.md`:
```markdown
You are a code reviewer. Check for correctness and security.

## Focus
- Does it work?
- Major bugs or security issues?
- Follows existing patterns?

## Tools
Read, Grep, Glob (read-only)
```

Usage in commands:
```python
Task(
    description="Design auth system",
    prompt="Design authentication for this project",
    subagent_type="architect"  # loads .claude/agents/architect.md
)
```

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
├── .claude/
│   ├── agent-launcher.md
│   ├── settings.json
│   ├── MEMORY.md              # NEW: Cross-conversation memory index
│   ├── agents/                # NEW: Custom subagent types
│   │   ├── architect.md
│   │   └── reviewer.md
│   ├── rules/                 # NEW: Path-specific rules
│   │   ├── tests.md
│   │   └── api.md
│   └── commands/
│       └── build.md
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
- **Task**: For spawning sub-agents
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

Create `.claude-library/REGISTRY.json`:

```json
{
  "version": "2.0.0",
  "project": "YOUR_PROJECT_NAME",
  "description": "Agent registry for YOUR_PROJECT",
  "agents": {
    "system-architect": {
      "name": "system-architect",
      "path": ".claude-library/agents/core/system-architect.md",
      "description": "Architecture design and specifications",
      "tools": ["Read", "Write", "Grep", "Glob"],
      "triggers": ["architecture", "design", "spec", "API", "database"],
      "category": "core",
      "priority": 1
    },
    "senior-engineer": {
      "name": "senior-engineer",
      "path": ".claude-library/agents/core/senior-engineer.md",
      "description": "Full-stack development and implementation",
      "tools": ["*"],
      "triggers": ["implement", "code", "build", "fix", "debug"],
      "category": "core",
      "priority": 1
    },
    "code-reviewer": {
      "name": "code-reviewer",
      "path": ".claude-library/agents/core/code-reviewer.md",
      "description": "Code review for quality and security",
      "tools": ["Read", "Grep", "Glob"],
      "triggers": ["review", "security", "performance", "quality"],
      "category": "core",
      "priority": 2
    },
    "workflow-orchestrator": {
      "name": "workflow-orchestrator",
      "path": ".claude-library/agents/core/workflow-orchestrator.md",
      "description": "Coordinate multi-agent workflows",
      "tools": ["Task", "Read"],
      "triggers": ["orchestrate", "coordinate", "workflow", "complex"],
      "category": "core",
      "priority": 1
    }
  },
  "skills": {
    "agent-launcher": {
      "path": ".claude-library/skills/agent-launcher-skill/",
      "description": "Intelligent agent selection and routing"
    }
  },
  "commands": {
    "build": {
      "path": ".claude/commands/build.md",
      "description": "Build features with TDD",
      "agents": ["system-architect", "senior-engineer", "code-reviewer"],
      "workflow": "parallel-sequential"
    },
    "debug": {
      "path": ".claude/commands/debug.md",
      "description": "Debug issues",
      "agents": ["senior-engineer"],
      "workflow": "single"
    },
    "review": {
      "path": ".claude/commands/review.md",
      "description": "Review code",
      "agents": ["code-reviewer"],
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

### Step 7: Create Settings

Create `.claude/settings.json`:

```json
{
  "project": {
    "name": "YOUR_PROJECT_NAME",
    "description": "YOUR_PROJECT_DESCRIPTION",
    "github_repo": "YOUR_GITHUB_REPO"
  }
}
```

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

### Test Agent Loading
- `"I need to design a REST API"` -> System architect loads with API context

### Test Command Execution
- `/build user authentication` -> Parallel execution of architect, test planner, researcher

### Test Context Loading
- `"Debug database performance"` -> Database expert loads with database patterns context

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
