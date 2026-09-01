# Simplicity Enforcement Guide
## Circuit Breakers Against Over-Engineering

### Core Principle: "Simplest Approach First, Always"

---

## 🚫 The Over-Engineering Problem

Common mistakes in agent systems:
- Creating 20 agents for a 500-line project
- Parallel execution for 2 sequential tasks
- Specialized agents for features that don't exist
- Complex workflows for simple operations
- Anticipating needs that never materialize

**This guide provides circuit breakers to prevent these mistakes.**

---

## 🎯 Simplicity Circuit Breakers

### Circuit Breaker 1: Complexity Assessment

**BEFORE creating any agent system, measure:**

```markdown
Project Size:
- < 1,000 lines → NO specialized agents
- 1,000-10,000 lines → MAX 1-2 specialists
- > 10,000 lines → Consider full system

Actual Complexity:
- Single file operations → Direct commands only
- 2-3 step process → Simple workflow
- 4-5 steps → Basic agents
- 6+ dynamic steps → Full agents

Current Patterns:
- No tests → Don't add test agent
- No database → Don't add DB specialist
- No API → Don't add API architect
- Basic CRUD → Keep it simple
```

### Circuit Breaker 2: The Three-Strike Rule

**Try in this order:**
1. **Strike 1**: Can a simple prompt solve this?
2. **Strike 2**: Can a basic workflow handle it?
3. **Strike 3**: Only now consider agents

Example:
```markdown
Task: "Format all Python files"

Strike 1: `black *.py` ✅ WORKS - STOP HERE
Strike 2: Not needed
Strike 3: Not needed

Task: "Debug production crash"

Strike 1: Check logs ❌ Too complex
Strike 2: Sequential debug workflow ❌ Need dynamic investigation
Strike 3: Debug agent ✅ Justified
```

### Circuit Breaker 3: Justify Every File

**Each generated file must pass this test:**

```markdown
File: [name]
Purpose: [one sentence - if longer, TOO COMPLEX]
Actively needed: [YES/NO based on current code]
Could existing tool do this: [YES = don't create]
Used in first session: [NO = don't create yet]
```

### Circuit Breaker 4: Progressive Disclosure

**Start with ONLY:**
```
.claude/
├── settings.json (0.5KB)     # hooks + permissions, or omit it entirely
├── agents/                   # frontmatter + a short persona each
│   ├── architect.md (1KB)
│   ├── engineer.md (1KB)
│   └── reviewer.md (1KB)
└── commands/
    └── build.md (1KB)
```

**Add ONLY when:**
- User hits actual error → Add debug.md
- Tests exist and fail → Add test.md
- Deployment configured → Add deploy.md
- Never preemptively

---

## 📋 Simplicity Enforcement Checklist

### Before Creating Agents

- [ ] Is this a single command? → NO AGENTS
- [ ] Are steps predictable? → NO AGENTS
- [ ] Under 1000 lines of code? → MINIMAL ONLY
- [ ] No actual database? → NO DB SPECIALIST
- [ ] No real API endpoints? → NO API ARCHITECT
- [ ] No authentication code? → NO AUTH SPECIALIST
- [ ] No payment processing? → NO PAYMENT SPECIALIST

### Before Adding Features

- [ ] Does this feature exist in code? → NO = DON'T ADD
- [ ] Has user requested this? → NO = DON'T ADD
- [ ] Will this be used immediately? → NO = DON'T ADD
- [ ] Can we add it later? → YES = DON'T ADD NOW

### Before Parallel Execution

- [ ] Are there 3+ independent tasks? → NO = SEQUENTIAL
- [ ] Will parallel save >30 seconds? → NO = SEQUENTIAL
- [ ] Is the complexity worth it? → NO = SEQUENTIAL

---

## 🛑 Anti-Patterns to Avoid

### ❌ Pattern: "Kitchen Sink Generation"
**Bad**: Creating every possible agent type
**Good**: Start with 3 core agents only

### ❌ Pattern: "Fortune Telling"
**Bad**: Adding features for anticipated needs
**Good**: Add only when need is proven

### ❌ Pattern: "Parallel Everything"
**Bad**: Forcing parallel execution everywhere
**Good**: Sequential by default, parallel when beneficial

### ❌ Pattern: "Specialist Inflation"
**Bad**: Creating specialists for every domain
**Good**: Core agents handle 80% of tasks

### ❌ Pattern: "Context Explosion"
**Bad**: Loading everything "just in case"
**Good**: Load minimal context on demand

---

## ✅ Simplicity Patterns to Follow

### ✅ Pattern: "Start Naked"
Begin with NO agents, add only when something fails

### ✅ Pattern: "One Command Wonder"
Start with single /build command, expand from actual use

### ✅ Pattern: "Earn Your Complexity"
Each complexity addition must be justified by failure

### ✅ Pattern: "Delete First"
Before adding, try removing something

### ✅ Pattern: "User Pull"
Let user needs pull features, don't push possibilities

---

## 📊 Complexity Scoring System

Rate your project (lower is simpler/better):

```markdown
Size Score:
- < 1K lines: 0 points
- 1K-10K lines: 1 point
- > 10K lines: 2 points

Tech Score:
- Single language: 0 points
- 2-3 technologies: 1 point
- 4+ technologies: 2 points

Integration Score:
- No external services: 0 points
- 1-2 integrations: 1 point
- 3+ integrations: 2 points

Total Score:
- 0-1: Use MINIMAL setup (7 files)
- 2-3: Use BASIC setup (10 files)
- 4-6: Consider FULL setup (15+ files)
```

---

## 🎯 When to Escalate Complexity

### Add Specialized Agents When:

**Database Specialist**:
- ✅ > 5 tables with relationships
- ✅ Complex queries (JOIN, aggregations)
- ✅ Performance issues observed
- ❌ NOT for simple CRUD

**API Specialist**:
- ✅ > 10 endpoints defined
- ✅ GraphQL/tRPC complexity
- ✅ Complex authentication flows
- ❌ NOT for basic REST

**Frontend Specialist**:
- ✅ > 20 components
- ✅ Complex state management
- ✅ Advanced animations/interactions
- ❌ NOT for simple forms

**Test Specialist**:
- ✅ > 40% test coverage exists
- ✅ Complex test scenarios
- ✅ E2E/Integration tests
- ❌ NOT for basic unit tests

---

## 🚀 Implementation Guide

### Step 1: Assess First
```bash
# Count lines of code
find . -name "*.py" | xargs wc -l

# Count test files
find . -name "*test*.py" | wc -l

# Check for database
grep -r "CREATE TABLE\|Model\|Schema" .

# Check for API
grep -r "@app.route\|@api\|endpoint" .
```

### Step 2: Start Minimal
```bash
# Generate with minimal flag
"Generate minimal agent system for simple project"

# Not: "Generate complete agent system"
```

### Step 3: Evolve Based on Use
```bash
# After first error
"Add debug command for this specific error"

# After tests found
"Add test command for existing test suite"

# Not: "Add all possible commands"
```

---

## 📏 Measuring Success

### Good Signs:
- ✅ First generation < 10 files
- ✅ Context < 5KB loaded
- ✅ Simple tasks stay simple
- ✅ User never sees unnecessary complexity
- ✅ Can explain each file's purpose

### Bad Signs:
- ❌ > 15 files for simple project
- ❌ Specialized agents never used
- ❌ Parallel execution for 2 tasks
- ❌ Features for "future needs"
- ❌ Can't explain why file exists

---

## 🎓 Remember

> "Perfection is achieved not when there is nothing more to add,
> but when there is nothing left to take away."
> — Antoine de Saint-Exupéry

**The best agent system is the simplest one that works.**

**Start minimal. Grow naturally. Complexity is earned, not assumed.**

---

*Simplicity Enforcement Guide v1.0*
*Part of Claude Agent Framework*