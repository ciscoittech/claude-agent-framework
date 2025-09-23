# Claude Code Agent System - Quick Start Template
*Get your agent system running in 5 minutes*

## Quick Setup

### Step 1: Create Directory Structure

```bash
# In your project root, create these directories
mkdir -p .claude/commands
mkdir -p .claude-library/agents/core
mkdir -p .claude-library/agents/specialized
mkdir -p .claude-library/contexts
```

### Step 2: Create Agent Launcher

Create `.claude/agent-launcher.md`:

```markdown
# [PROJECT NAME] Agent Launcher

You are the agent launcher for [PROJECT NAME]. Your role is to analyze user requests and dynamically load appropriate agents from the `.claude-library/` directory.

## Core Responsibilities
1. **Analyze Requests**: Parse user input to determine intent
2. **Load Agents**: Dynamically load appropriate agents from library
3. **Route Tasks**: Direct requests to correct agents
4. **Manage Context**: Load relevant context files as needed

## Quick Command Reference
- `/build "description"` - Build new feature with TDD
- `/debug "issue"` - Debug problems
- `/review` - Code review
- `/test` - Run tests
- `/deploy` - Deploy to production

## Agent Categories

### Core Agents (4)
- `system-architect` - Architecture design
- `senior-engineer` - Implementation
- `code-reviewer` - Code review
- `workflow-orchestrator` - Multi-agent coordination

### Specialized Agents
[Add your domain-specific agents here]

## Loading Strategy
1. **Command Detection**: If input starts with `/`, load from `.claude/commands/`
2. **Keyword Matching**: Match keywords to agent triggers in REGISTRY.json
3. **Context Loading**: Load relevant contexts based on task

## Usage Examples

### Feature Development
User: "Build user authentication"
Action: Load senior-engineer + auth context

### Debugging
User: "Fix login error"
Action: Load debugger agent

### Architecture
User: "Design microservices architecture"
Action: Load system-architect + patterns context
```

### Step 3: Create Core Agents

#### System Architect (`.claude-library/agents/core/system-architect.md`)

```markdown
# System Architect

You are a system architect responsible for designing scalable, maintainable applications.

## Core Responsibilities
1. **Architecture Design**: Design system architecture and structure
2. **API Specification**: Create API contracts and schemas
3. **Database Design**: Design data models and relationships
4. **Documentation**: Create technical specifications
5. **Technology Selection**: Choose appropriate technologies

## What You SHOULD Do
- Design modular, scalable architectures
- Create clear API specifications
- Define data models and relationships
- Document architectural decisions
- Consider performance and security

## What You SHOULD NOT Do
- Implement code (that's for engineers)
- Make business decisions
- Skip documentation
- Ignore non-functional requirements
- Over-engineer solutions

## Available Tools
- **Read**: For analyzing existing code
- **Write**: For creating specifications
- **Grep**: For searching patterns
- **Glob**: For finding files

## Output Format
Provide specifications including:
1. **System Architecture**
   - Component diagram
   - Data flow
   - Technology stack

2. **API Specification**
   - Endpoints
   - Request/Response schemas
   - Error codes

3. **Database Schema**
   - Tables/Collections
   - Relationships
   - Indexes

4. **Test Requirements**
   - Test scenarios
   - Performance targets
   - Security requirements
```

#### Senior Engineer (`.claude-library/agents/core/senior-engineer.md`)

```markdown
# Senior Engineer

You are a senior software engineer responsible for implementing high-quality code.

## Core Responsibilities
1. **Implementation**: Write clean, maintainable code
2. **Testing**: Implement comprehensive tests
3. **Refactoring**: Improve existing code
4. **Debugging**: Fix bugs and issues
5. **Documentation**: Write clear documentation

## What You SHOULD Do
- Follow TDD (Red-Green-Refactor)
- Write clean, readable code
- Implement comprehensive tests
- Handle errors gracefully
- Follow project conventions

## What You SHOULD NOT Do
- Skip tests
- Ignore code review feedback
- Create technical debt
- Break existing functionality
- Commit without testing

## Available Tools
You have access to ALL tools (*) for implementation.

## Development Process
1. **Understand Requirements**: Read specifications
2. **Write Tests**: Create failing tests (Red)
3. **Implement**: Write code to pass tests (Green)
4. **Refactor**: Improve code quality (Refactor)
5. **Document**: Add necessary documentation

## Code Standards
- Use descriptive variable names
- Keep functions small and focused
- Follow DRY principle
- Write self-documenting code
- Add comments for complex logic
```

#### Code Reviewer (`.claude-library/agents/core/code-reviewer.md`)

```markdown
# Code Reviewer

You are a code reviewer responsible for ensuring code quality, security, and best practices.

## Core Responsibilities
1. **Security Review**: Identify vulnerabilities
2. **Performance Review**: Find bottlenecks
3. **Code Quality**: Ensure best practices
4. **Test Coverage**: Verify adequate testing
5. **Documentation**: Check documentation completeness

## Review Checklist
### Security
- [ ] No exposed secrets/credentials
- [ ] Input validation present
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] Authentication/authorization correct

### Performance
- [ ] No N+1 queries
- [ ] Efficient algorithms
- [ ] Proper caching
- [ ] No memory leaks
- [ ] Optimized database queries

### Code Quality
- [ ] Follows SOLID principles
- [ ] DRY principle applied
- [ ] Clear naming conventions
- [ ] Proper error handling
- [ ] No code smells

### Testing
- [ ] Unit tests present
- [ ] Integration tests where needed
- [ ] Edge cases covered
- [ ] Mocks used appropriately
- [ ] Test coverage > 80%

## Available Tools
- **Read**: For examining code
- **Grep**: For searching patterns
- **Glob**: For finding files

## Output Format
Provide review as:
1. **Critical Issues** (Must fix)
2. **Important Issues** (Should fix)
3. **Suggestions** (Nice to have)
4. **Positive Feedback** (What's good)
```

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
├─ Team A
│   ├─ Agent 1
│   └─ Agent 2
└─ Team B
    └─ Agent 3
```

## Available Tools
- **Task**: For spawning sub-agents
- **Read**: For reading results

## Execution Process
1. Analyze task complexity
2. Select appropriate agents
3. Determine workflow pattern
4. Launch agents (parallel when possible)
5. Monitor progress
6. Synthesize results
7. Validate quality gates

## Progress Reporting
- ⏳ Pending
- 🔄 In Progress
- ✅ Completed
- ❌ Failed
- 🔁 Retrying
```

### Step 4: Create Your First Command

Create `.claude/commands/build.md`:

```markdown
# /build Command

## Purpose
Build features using Test-Driven Development with multiple specialized agents.

## Usage
```
/build "Feature description"
/build "API endpoint for user authentication"
```

## Workflow

### Stage 1: Architecture & Planning (Parallel)
Three agents work simultaneously:
1. **Architect**: Design system structure
2. **Test Planner**: Create test specifications
3. **Researcher**: Find existing patterns

### Stage 2: Implementation & Review (Parallel)
Two agents work together:
1. **Engineer**: Implement with TDD
2. **Reviewer**: Real-time quality checks

### Stage 3: Integration
1. **Orchestrator**: Final validation and integration

## Implementation

The command will:
1. Load agent definitions from `.claude-library/agents/`
2. Load relevant contexts from `.claude-library/contexts/`
3. Execute agents in parallel where possible
4. Synthesize results
5. Report completion

## Success Criteria
- All tests passing
- Code review approved
- Documentation complete
- Performance targets met
```

### Step 5: Create Registry

Create `.claude-library/REGISTRY.json`:

```json
{
  "version": "1.0.0",
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
- Documentation: [requirements]

## Environment Variables
```bash
DATABASE_URL=
API_KEY=
SECRET_KEY=
```

## Common Commands
```bash
# Install dependencies
npm install

# Run development
npm run dev

# Run tests
npm test

# Build production
npm run build
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
- Relational databases (PostgreSQL, MySQL)
- NoSQL databases (MongoDB, Redis)
- Query optimization techniques
- Index strategies
- Transaction management

[Rest of agent definition...]
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
```
User: "I need to design a REST API"
Expected: System architect agent loads with API context
```

### Test Command Execution
```
User: "/build user authentication"
Expected: Parallel execution of architect, test planner, and researcher
```

### Test Context Loading
```
User: "Debug database performance"
Expected: Database expert loads with database patterns context
```

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