# Agent Implementation Patterns
*Consolidated guide: Anthropic principles + workflow patterns + production team patterns*

## Table of Contents

1. [Core Principles](#1-core-principles)
2. [Decision Trees](#2-decision-trees)
3. [Workflow Patterns](#3-workflow-patterns)
4. [Parallel Execution](#4-parallel-execution)
5. [Error Handling & Recovery](#5-error-handling--recovery)
6. [Context Optimization](#6-context-optimization)
7. [Production Team Patterns](#7-production-team-patterns)
8. [Template Snippets](#8-template-snippets)
9. [Best Practices Summary](#best-practices-summary)

---

## 1. Core Principles

### The Hierarchy of Solutions

From Anthropic's "Building Effective Agents": effective agents are built on sound workflows, not complex reasoning loops. **Start with workflows, add agency only when needed.**

```
Level 1: Prompt Engineering (simplest)
   ↓ Only escalate when this fails
Level 2: Structured Workflows (most effective)
   ↓ Only escalate when this fails
Level 3: Agentic Systems (most complex)
```

### When to Choose Each Approach

| Problem Type | Solution | Example | Cost |
|-------------|----------|---------|------|
| **Single-step task** | Prompt Engineering | "Summarize this document" | Lowest |
| **Multi-step, predictable** | Workflow | "Analyze → Plan → Implement → Review" | Medium |
| **Dynamic decisions** | Agent | "Research unknown topic, adapt strategy based on findings" | Highest |

### The Agent vs Workflow Test

Two questions determine your approach:

- **Workflow**: Can I define the steps in advance? Steps are known, dependencies are clear, outputs are predictable.
- **Agent**: Do the steps depend on dynamic intermediate results? Steps emerge based on context, decisions depend on runtime state.

> **Key insight**: Most development tasks are workflows, not agents. A feature implementation with known stages (design → code → test → review) is a workflow even if the code itself varies. Reserve true agents for genuinely open-ended problems like complex debugging or research.

### Workflows: Predictable Multi-Step Processes

**Characteristics:**
- Steps are known in advance
- Dependencies are clear
- Outputs are predictable
- Failures can be anticipated

**Best for:** Software development processes, code reviews, testing pipelines, documentation generation

### Agents: Dynamic Decision-Making Systems

**Characteristics:**
- Steps emerge based on context
- Decisions depend on intermediate results
- Outputs vary significantly
- Requires adaptive strategies

**Best for:** Research and analysis, complex debugging, creative problem solving

### Tool Design Principles

From Anthropic's tool design guidelines:

#### 1. Granular Tools Over Multi-Purpose Tools

```javascript
// BAD: Too broad, unclear purpose
function fileManager(action, path, content, options) {
  if (action === 'read') return readFile(path);
  if (action === 'write') return writeFile(path, content);
  if (action === 'delete') return deleteFile(path);
}

// GOOD: Clear, single-purpose tools
function readFile(path) { /* focused implementation */ }
function writeFile(path, content) { /* focused implementation */ }
function deleteFile(path) { /* focused implementation */ }
```

#### 2. Tools Should Be Deterministic

```javascript
// BAD: Unpredictable behavior
function smartAnalyze(code) {
  return Math.random() > 0.5 ? getMetrics(code) : getSuggestions(code);
}

// GOOD: Predictable, consistent outputs
function analyzeCodeMetrics(code) { /* always returns metrics */ }
function generateCodeSuggestions(code) { /* always returns suggestions */ }
```

#### 3. Clear Error Handling and Feedback

```javascript
// BAD: Silent failures
function processFile(path) {
  try { return doProcessing(path); }
  catch (e) { return null; }
}

// GOOD: Clear error reporting
function processFile(path) {
  try {
    return { success: true, data: doProcessing(path) };
  } catch (error) {
    return { success: false, error: error.message, path, timestamp: new Date().toISOString() };
  }
}
```

#### 4. Give Tools Clear Names, Document Parameters, Include Examples

```markdown
### Tool: analyzeCodeSecurity

**Purpose**: Scan source files for common security vulnerabilities
**Parameters**:
- `file_path` (string, required): Absolute path to the file
- `severity` (string, optional): Minimum severity to report ("low" | "medium" | "high")
**Returns**: JSON array of findings with line numbers, severity, and remediation

**Example**:
analyzeCodeSecurity(file_path="/src/auth.ts", severity="medium")
// Returns: [{"line": 42, "severity": "high", "issue": "SQL injection", "fix": "Use parameterized query"}]
```

### Tool Selection Guidelines

| Task Type | Recommended Tool | Avoid |
|-----------|-----------------|--------|
| **File Reading** | `Read` | `Bash("cat file")` |
| **File Search** | `Grep` | `Bash("grep pattern")` |
| **File Patterns** | `Glob` | `Bash("find . -name")` |
| **Code Analysis** | `Read` + `Grep` | `Bash("awk/sed")` |
| **Agent Spawning** | `Task` | Multiple sequential requests |

---

## 2. Decision Trees

### Workflow Type Selection

```
Is this a single, simple task?
├─ YES → Use Prompt Engineering (direct command)
└─ NO → Are the steps known in advance?
    ├─ YES → Use Workflow
    │   └─ Are steps dependent on each other?
    │       ├─ YES → Sequential Workflow (prompt chaining)
    │       └─ NO → Parallel Workflow (fan-out/fan-in)
    └─ NO → Use Agent
        └─ Is there a clear input classification?
            ├─ YES → Routing Workflow
            └─ NO → Is quality critical with iteration needed?
                ├─ YES → Evaluator-Optimizer
                └─ NO → Orchestrator-Workers (hierarchical)
```

### Complexity Assessment

```
What's the project complexity?
├─ Simple (1-2 files, single concern)
│   └─ Use: Single agent, direct commands
│       Files: 7 total, 3 agents max
│       Setup: 2 minutes
│
├─ Medium (3-10 files, multiple concerns)
│   └─ Use: Sequential workflow with 2-3 specialized agents
│       Files: 10-12 total, 5 agents max
│       Setup: 15 minutes
│
└─ Complex (10+ files, cross-cutting concerns)
    └─ Use: Orchestrator pattern with worker agents
        Files: 15-20 total, 7+ agents
        Setup: 30-60 minutes
```

### Agent Selection Criteria

```
What does this task need?
├─ Code implementation only?
│   └─ Engineer Agent (+ optional Reviewer)
├─ Architecture decisions?
│   └─ Architect Agent → Engineer Agent(s)
├─ Bug investigation?
│   └─ Debugger Agent (may spawn specialists)
├─ Security review?
│   └─ Security Specialist Agent
├─ Multiple concerns?
│   └─ Orchestrator → Team of Specialists
└─ Unknown scope?
    └─ Analyst Agent first → then route appropriately
```

### When to Add Specialization

```
Is one general agent struggling?
├─ NO → Keep using general agent (don't add complexity)
└─ YES → What's the failure mode?
    ├─ Context overload → Split into domain specialists
    ├─ Poor quality in one area → Add focused specialist
    ├─ Too slow → Add parallel agents
    └─ Inconsistent results → Add evaluator-optimizer loop
```

### Parallelization Decision

```
Can tasks run independently?
├─ YES → Are tasks similar in duration?
│   ├─ YES → Full parallelization (all at once)
│   └─ NO → Staggered parallel (start long tasks first)
└─ NO → Are there independent subgroups?
    ├─ YES → Parallel groups, sequential within groups
    └─ NO → Pure sequential execution
```

### Model Selection Decision

```
What model should this agent use?
├─ Is it a simple, mechanical task? (formatting, file moves, renaming)
│   └─ Use haiku (fastest, cheapest)
├─ Is it standard development work? (implementation, testing, reviews)
│   └─ Use sonnet (balanced speed/quality)
└─ Does it require deep reasoning? (architecture, security audit, complex debugging)
    └─ Use opus (highest quality)
```

### Workflow Composition Decision

```
How should I combine patterns?
├─ All tasks independent, same priority
│   └─ Pure Parallel (fan-out/fan-in)
├─ Tasks have clear phases
│   └─ Sequential phases, parallel within each phase
├─ One coordinator, many workers
│   └─ Hierarchical (orchestrator-workers)
├─ Need iterative quality improvement
│   └─ Evaluator-Optimizer loop
└─ Different input types need different handling
    └─ Router → specialized handlers
```

### Real-World Scenario Mapping

| Scenario | Recommended Pattern | Why |
|----------|-------------------|-----|
| Add a REST endpoint | Sequential (design → implement → test) | Clear dependency chain |
| Security audit | Parallel (3-5 specialists) | Independent analysis areas |
| Debug production issue | Hierarchical (triage → specialists) | Unknown scope needs decomposition |
| Refactor large module | Feature-Loop (TDD cycle) | Need safety of test-first approach |
| Migrate database schema | Sequential with checkpoints | Risk requires careful staging |
| Build new UI page | Parallel (component → style → test) | Mostly independent concerns |
| Code review | Parallel (security + quality + perf) | Independent review dimensions |
| Monorepo change | Hierarchical + worktree isolation | Cross-package coordination |

---

## 3. Workflow Patterns

### Sequential Workflow (Prompt Chaining)

Each step's output becomes the next step's input. Use when dependencies between steps require progressive refinement.

```
Architect → Engineer → Reviewer → Deploy
   ↓           ↓          ↓         ↓
  spec       code      feedback   release
```

```javascript
// Sequential execution with context passing
async function sequentialWorkflow(requirements) {
  // Step 1: Architecture
  const architecture = await runTask({
    type: 'general-purpose',
    description: 'Design system architecture',
    prompt: `Design architecture for: ${requirements}`
  });

  // Step 2: Implementation (depends on architecture)
  const implementation = await runTask({
    type: 'general-purpose',
    description: 'Implement based on architecture',
    prompt: `Implement this architecture:
    ${architecture.result}
    Create production-ready code following TDD principles.`
  });

  // Step 3: Review (depends on implementation)
  const review = await runTask({
    type: 'general-purpose',
    description: 'Review implementation',
    prompt: `Review this implementation:
    ${implementation.result}
    Check for security, performance, and quality issues.`
  });

  return { architecture, implementation, review };
}
```

### Parallel Workflow (Fan-Out/Fan-In)

Multiple independent tasks execute simultaneously, then results are synthesized.

```
         ┌─ Security Analysis  ─┐
Input ───┼─ Performance Analysis ┼──→ Synthesis
         └─ Quality Analysis    ─┘
```

```javascript
// ALL tasks sent in SINGLE message for true parallelization
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Security analysis</description>
  <prompt>Analyze codebase for security vulnerabilities:
    - SQL injection, XSS, auth flaws, data exposure</prompt>
</Task>

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Performance analysis</description>
  <prompt>Analyze codebase for performance issues:
    - N+1 queries, memory leaks, missing indexes</prompt>
</Task>

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Code quality analysis</description>
  <prompt>Analyze codebase for quality issues:
    - Duplication, complexity, missing tests</prompt>
</Task>
```

> **Critical**: Send all Tasks in ONE message for true parallelization. Sending them sequentially makes execution 3x slower.

### Hierarchical Workflow (Orchestrator-Workers)

Parent agent coordinates specialized child agents. Use for complex problems requiring decomposition and coordination.

```
              Orchestrator
            /      |       \
     Frontend   Backend   Database
      Agent      Agent     Agent
       |          |          |
    Components  API Routes  Schema
```

```javascript
async function orchestratorWorkflow(complexProblem) {
  // Orchestrator analyzes and plans
  const plan = await runTask({
    type: 'general-purpose',
    description: 'Problem analysis and planning',
    prompt: `You are the orchestrator. Problem: ${complexProblem}
    Create: 1) Problem breakdown 2) Required specialists
    3) Coordination strategy 4) Success criteria`
  });

  // Spawn specialists based on plan (parallel)
  const workers = plan.specialists.map(specialist =>
    runTask({
      type: 'general-purpose',
      description: `${specialist.role} specialist`,
      prompt: `You are a ${specialist.role} specialist.
      Assignment: ${specialist.task}
      Context: ${specialist.context}
      Deliverables: ${specialist.deliverables}`
    })
  );

  const results = await Promise.allSettled(workers);
  return synthesizeResults(results);
}
```

### Feature-Loop Pattern (TDD)

Parallel analysis feeds into parallel implementation + review, then integration.

```
Phase 1 (Parallel):     Phase 2 (Parallel):     Phase 3:
┌─ Analyze requirements  ┌─ Implement code        Integration
├─ Design architecture   ├─ Write tests           & validation
└─ Plan test strategy    └─ Live review
```

```typescript
// Phase 1: RED - Write failing tests
describe('UserAuthentication', () => {
  it('should hash passwords with bcrypt', async () => {
    const user = await registerUser({ email: 'test@example.com', password: 'testPassword123' });
    expect(user.password).not.toBe('testPassword123');
    expect(await bcrypt.compare('testPassword123', user.password)).toBe(true);
  });

  it('should validate email format', async () => {
    await expect(registerUser({ email: 'invalid', password: 'valid12345' }))
      .rejects.toThrow('Invalid email format');
  });
});

// Phase 2: GREEN - Minimal implementation to pass
export async function registerUser({ email, password }) {
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    throw new Error('Invalid email format');
  }
  if (password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  return { email, password: await bcrypt.hash(password, 10) };
}

// Phase 3: REFACTOR - Improve with validation library
import { z } from 'zod';
const UserRegistrationSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters')
});
```

### Agent Teams Pattern <!-- NEW in v2.0 -->

Claude Code now supports custom `subagent_type` definitions via `.claude/agents/` files. Instead of always using `general-purpose`, define reusable agent personas.

```
.claude/agents/
├── security-reviewer.md    # Security specialist persona
├── frontend-engineer.md    # React/Vue specialist
└── api-designer.md         # REST/GraphQL specialist
```

**Agent file format** (`.claude/agents/security-reviewer.md`):
```markdown
---
name: Security Reviewer
description: Reviews code for security vulnerabilities
tools:
  - Read
  - Grep
  - Glob
  - Bash
---

You are a security specialist. Review code for:
- Injection attacks (SQL, XSS, command injection)
- Authentication and authorization flaws
- Data exposure and privacy violations
- Dependency vulnerabilities

Output a structured report with severity ratings.
```

**Usage in workflows**:
```javascript
// Reference custom agent types instead of general-purpose
<Task>
  <subagent_type>security-reviewer</subagent_type>
  <description>Security review of auth module</description>
  <prompt>Review src/auth/ for vulnerabilities. Focus on JWT handling.</prompt>
</Task>

<Task>
  <subagent_type>frontend-engineer</subagent_type>
  <description>Implement login component</description>
  <prompt>Create React login form with proper input validation.</prompt>
</Task>
```

### Routing Workflow (Conditional Branching)

Classify input and route to specialized handlers.

```javascript
async function routingWorkflow(input) {
  const classification = await runTask({
    type: 'general-purpose',
    description: 'Classify input type',
    prompt: `Classify this request: "${input}"
    Categories: [bug_report, feature_request, question, documentation]
    Return: {"type": "category", "confidence": 0.9}`
  });

  const { type } = JSON.parse(classification.result);

  const handlers = {
    bug_report:       () => runTask({ type: 'general-purpose', prompt: `Debug: ${input}` }),
    feature_request:  () => runTask({ type: 'general-purpose', prompt: `Implement: ${input}` }),
    question:         () => runTask({ type: 'general-purpose', prompt: `Answer: ${input}` }),
    documentation:    () => runTask({ type: 'general-purpose', prompt: `Document: ${input}` })
  };

  return handlers[type]?.() || handleUnknown(input);
}
```

### Evaluator-Optimizer (Iterative Improvement)

Generate solutions, evaluate quality, and iteratively improve. Use when quality is critical.

```javascript
async function evaluatorOptimizer(task, maxIterations = 3) {
  let currentSolution = null;
  let bestScore = 0;

  for (let i = 0; i < maxIterations; i++) {
    const solution = await runTask({
      type: 'general-purpose',
      description: `Solution generation - iteration ${i + 1}`,
      prompt: `Generate solution for: ${task}
      ${currentSolution ? `Previous feedback: ${currentSolution.feedback}` : ''}`
    });

    const evaluation = await runTask({
      type: 'general-purpose',
      description: `Evaluation - iteration ${i + 1}`,
      prompt: `Evaluate: ${solution.result}
      Score on: correctness, performance, security, maintainability (1-10 each)
      Return: {"score": 85, "feedback": "...", "improvements": [...]}`
    });

    const { score, feedback, improvements } = JSON.parse(evaluation.result);
    if (score > bestScore) bestScore = score;
    if (score >= 95) break; // Early termination

    currentSolution = { ...solution, feedback, improvements };
  }

  return currentSolution;
}
```

---

## 4. Parallel Execution

### Pattern 1: Independent Analysis

Launch multiple agents simultaneously when they don't depend on each other's output.

```javascript
// All three agents start SIMULTANEOUSLY
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Security analysis</description>
  <prompt>Analyze for: SQL injection, XSS, auth flaws, data exposure</prompt>
</Task>

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Performance analysis</description>
  <prompt>Analyze for: N+1 queries, memory leaks, inefficient algorithms</prompt>
</Task>

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Code quality analysis</description>
  <prompt>Analyze for: duplication, complexity, missing tests, naming</prompt>
</Task>
```

### Pattern 2: Parallel Implementation with Live Review

One agent implements while another reviews in real-time.

```javascript
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Implementation</description>
  <prompt>[Engineer] Implement user authentication with JWT, refresh tokens,
  rate limiting, bcrypt. Follow TDD: tests first, implement, refactor.</prompt>
</Task>

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Real-time review</description>
  <prompt>[Reviewer] As the engineer implements, review for security
  vulnerabilities, performance issues, best practices violations.</prompt>
</Task>
```

### Pattern 3: Hierarchical Decomposition

Parent agent spawns specialized children based on analysis.

```javascript
function orchestrateDebug(issue) {
  const issueType = analyzeIssue(issue);

  if (issueType.includes('frontend')) {
    spawnAgent('frontend-debugger', { focus: ['hydration', 'state', 'rendering'] });
  }
  if (issueType.includes('backend')) {
    spawnAgent('backend-debugger', { focus: ['api', 'database', 'auth'] });
  }
  if (issueType.includes('performance')) {
    spawnAgent('performance-debugger', { focus: ['queries', 'caching', 'bundling'] });
  }

  synthesizeFindings();
}
```

### Result Aggregation Pattern

Combine results from parallel agents, handling partial failures gracefully.

```javascript
async function aggregateResults(agents) {
  const results = await Promise.allSettled(agents.map(agent => runAgent(agent)));

  const successes = results.filter(r => r.status === 'fulfilled').map(r => r.value);
  const failures = results.filter(r => r.status === 'rejected').map(r => ({
    agent: r.reason.agent, error: r.reason.message
  }));

  return {
    consensus: findConsensus(successes),
    conflicts: findConflicts(successes),
    recommendations: mergeRecommendations(successes),
    failures
  };
}
```

### Real-World Example: Building a REST API (Parallel)

```javascript
// Step 1: Architecture phase (parallel - ~30 seconds)
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>API architecture design</description>
  <prompt>Design REST API for user management:
    CRUD operations, JWT auth, role-based access, rate limiting</prompt>
</Task>

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Database schema design</description>
  <prompt>Design database schema for:
    User profiles, sessions, permissions, audit logs</prompt>
</Task>

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Test plan creation</description>
  <prompt>Create test specifications for:
    API endpoints, auth flows, error cases, performance</prompt>
</Task>

// Step 2: Implementation (parallel - ~45 seconds, uses Step 1 results)
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Backend implementation</description>
  <prompt>Implement based on architecture: ${architectureResults}
    Use TDD approach with provided tests</prompt>
</Task>

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Security review</description>
  <prompt>Review implementation for SQL injection, JWT vulnerabilities,
    rate limiting bypass, data exposure</prompt>
</Task>

// Step 3: Integration (sequential - ~15 seconds)
// Verify all endpoints, generate docs, create deployment guide
```

### Performance Benchmarks

| Workflow Type | Sequential | Parallel | Improvement |
|--------------|------------|----------|-------------|
| 3-Agent Analysis | 90s | 30s | **3x faster** |
| 5-Agent Review | 150s | 35s | **4.3x faster** |
| 10-Agent Debug | 300s | 45s | **6.7x faster** |
| TDD Cycle | 180s | 75s | **2.4x faster** |

> **Diminishing returns**: Beyond 5-7 parallel agents, coordination overhead reduces gains. The sweet spot is 3-5 parallel agents for most tasks.

### Effort Levels <!-- NEW in v2.0 -->

Use the `model` parameter to match agent cost/speed to task complexity:

| Model | Use For | Speed | Cost |
|-------|---------|-------|------|
| `model: "haiku"` | Simple tasks: linting, formatting, file moves | Fastest | Lowest |
| `model: "sonnet"` | Standard tasks: implementation, testing, review | Fast | Medium |
| `model: "opus"` | Complex reasoning: architecture, debugging, security | Slower | Highest |

```javascript
// Fast/cheap: use haiku for simple file operations
<Task>
  <subagent_type>general-purpose</subagent_type>
  <model>haiku</model>
  <description>Format and lint check</description>
  <prompt>Run linter and fix formatting issues in src/</prompt>
</Task>

// Complex: use opus for architecture decisions
<Task>
  <subagent_type>general-purpose</subagent_type>
  <model>opus</model>
  <description>System architecture review</description>
  <prompt>Review system architecture for scalability and security concerns</prompt>
</Task>
```

---

## 5. Error Handling & Recovery

### Graceful Degradation

Try primary approach, fallback to alternatives.

```javascript
async function executeWithFallback(task) {
  const strategies = [primaryStrategy, fallbackStrategy, manualStrategy];

  for (const strategy of strategies) {
    try {
      return await strategy(task);
    } catch (error) {
      console.log(`Strategy ${strategy.name} failed: ${error.message}`);
      continue;
    }
  }
  throw new Error('All strategies failed');
}
```

### Retry with Exponential Backoff

```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  let lastError;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      if (!isRetryable(error)) throw error;
      const delay = Math.min(1000 * Math.pow(2, i), 10000);
      await sleep(delay);
    }
  }
  throw lastError;
}

function isRetryable(error) {
  return ['TIMEOUT', 'NETWORK_ERROR', 'RATE_LIMIT', 'TEMPORARY_FAILURE'].includes(error.code);
}
```

### Circuit Breaker Pattern

Prevent cascading failures by stopping calls to a failing service.

```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.failureCount = 0;
    this.threshold = threshold;
    this.timeout = timeout;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.nextAttempt = Date.now();
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) throw new Error('Circuit breaker is OPEN');
      this.state = 'HALF_OPEN';
    }

    try {
      const result = await fn();
      this.failureCount = 0;
      this.state = 'CLOSED';
      return result;
    } catch (error) {
      this.failureCount++;
      if (this.failureCount >= this.threshold) {
        this.state = 'OPEN';
        this.nextAttempt = Date.now() + this.timeout;
      }
      throw error;
    }
  }
}
```

### Progressive Quality Gates

Multiple gates with early termination on critical failures.

```javascript
async function qualityGatePipeline(code) {
  const gates = [
    { name: 'Syntax',      fn: checkSyntax,          critical: true },
    { name: 'Linting',     fn: runLinter,             critical: true },
    { name: 'Type Check',  fn: checkTypes,            critical: true },
    { name: 'Unit Tests',  fn: runUnitTests,          critical: true },
    { name: 'Coverage',    fn: checkCoverage,          critical: false },
    { name: 'Security',    fn: scanSecurity,           critical: true },
    { name: 'Performance', fn: checkPerformance,       critical: false },
  ];

  for (const gate of gates) {
    const result = await gate.fn(code);
    if (!result.passed && gate.critical) {
      return { passed: false, failedAt: gate.name, reason: result.reason };
    }
  }
  return { passed: true };
}
```

---

## 6. Context Optimization

### Lazy Loading Pattern

Load context only when needed, cache for reuse.

```javascript
class ContextManager {
  constructor() { this.cache = new Map(); }

  async getContext(name) {
    if (this.cache.has(name)) return this.cache.get(name);
    const context = await readFile(`.claude-library/contexts/${name}.md`);
    this.cache.set(name, context);
    return context;
  }

  async preloadForTask(taskType) {
    const contextMap = {
      'api':      ['api-patterns', 'auth', 'validation'],
      'database': ['schema', 'migrations', 'optimization'],
      'frontend': ['components', 'state', 'styling'],
      'testing':  ['test-patterns', 'mocks', 'coverage']
    };
    const contexts = contextMap[taskType] || ['project'];
    await Promise.all(contexts.map(ctx => this.getContext(ctx)));
  }
}
```

### Context Pruning

Include only relevant parts of context to save tokens.

```javascript
function pruneContext(fullContext, task) {
  const sections = fullContext.split('##');
  const keywords = extractKeywords(task);

  return sections
    .filter(section => {
      const words = section.toLowerCase().split(/\s+/);
      const matches = keywords.filter(kw => words.includes(kw.toLowerCase()));
      return matches.length / keywords.length > 0.5;
    })
    .join('\n##');
}
```

### Context Inheritance Hierarchy

Build specialized contexts from base contexts.

```javascript
class ContextHierarchy {
  constructor() {
    this.contexts = {
      base:     { content: 'Project fundamentals...', children: ['frontend', 'backend'] },
      frontend: { parent: 'base', content: 'Frontend patterns...', children: ['react', 'vue'] },
      react:    { parent: 'frontend', content: 'React-specific patterns...' }
    };
  }

  getFullContext(name) {
    const ctx = this.contexts[name];
    const parentContent = ctx.parent ? this.getFullContext(ctx.parent) + '\n' : '';
    return parentContent + ctx.content;
  }
}
```

### Context Loading Performance

| Strategy | Load Time | Memory | Cache Hit Rate |
|----------|-----------|---------|----------------|
| Full Load | 5s | 250KB | N/A |
| Lazy Load | 0.5s | 10KB | 0% initial |
| Cached Load | 0.1s | 10KB | 85% |
| Pruned Load | 0.3s | 5KB | 60% |

### Extended Context <!-- NEW in v2.0 -->

Claude Code now supports up to 1M token context windows. This changes context strategy:

- **Small projects (<50 files)**: Load everything, skip lazy loading complexity
- **Medium projects (50-500 files)**: Use lazy loading for non-essential contexts
- **Large projects (500+ files)**: Context pruning and inheritance remain critical
- **Monorepos**: Always use per-domain context with lazy loading

**Context budget guidelines:**

| Context Category | Recommended Budget | Notes |
|-----------------|-------------------|-------|
| Agent persona/instructions | <2KB | Keep personas focused |
| Project context (CLAUDE.md) | <5KB | Auto-loaded, keep lean |
| Domain contexts | 5-20KB each | Loaded on demand |
| Code being analyzed | Up to 100KB | Use Grep to find relevant sections first |
| Previous agent output | <10KB | Summarize, don't pass raw output |

**Anti-pattern**: Loading entire codebases into context. Even with 1M tokens, relevance matters more than volume. A focused 10KB context outperforms an unfocused 500KB dump.

---

## 7. Production Team Patterns

Condensed from real-world usage patterns at production scale.

### Checkpoint-Heavy Workflow ("Slot Machine" Approach)

Commit current work, run Claude Code for a focused session, then decide to accept or restart.

```bash
# Save current state
git add . && git commit -m "checkpoint: before claude session"

# Run focused session
# (work with Claude Code on specific feature)

# Decision point: accept or reset
git diff --stat  # Review what changed
# Accept: git add . && git commit -m "feat: completed feature X"
# Reject: git reset --hard HEAD  # Reset to checkpoint
```

**Why it works:**
- Prevents endless iteration cycles
- Creates natural decision points
- Maintains code quality through explicit accept/reject gates

### Auto-Accept vs Synchronous Decision Matrix

| Task Type | Mode | Reasoning |
|-----------|------|-----------|
| Core Business Logic | **Synchronous** | Requires human oversight |
| Authentication/Security | **Synchronous** | Critical security implications |
| Payment Processing | **Synchronous** | Financial risk |
| Configuration Files | **Synchronous** | System stability |
| API Integrations | **Synchronous** | External dependency risks |
| UI/UX Styling | **Auto-Accept** | Low risk, high iteration benefit |
| Documentation | **Auto-Accept** | Easy to review and fix |
| Unit Tests | **Auto-Accept** | Test failures will catch issues |

### Custom CLAUDE.md Instructions for Anti-Pattern Prevention

Encode team knowledge to prevent repeated mistakes:

```markdown
# .claude/CLAUDE.md

## Common Mistakes to Avoid
- NEVER use `any` type in TypeScript
- ALWAYS add error handling to API calls
- NEVER commit console.log statements
- ALWAYS update tests when changing interfaces
- NEVER hardcode API endpoints

## Project-Specific Rules
- Use Tailwind CSS classes, not custom CSS
- All API calls must include timeout configuration
- Database queries must include proper indexing hints
- All forms must include validation and error states
```

### Visual-First Development Pattern

Screenshots drive UI/UX decisions:

1. **Capture**: Screenshot current state
2. **Describe**: Natural language description of desired outcome
3. **Implement**: Claude Code makes modifications
4. **Verify**: Screenshot after changes for comparison
5. **Iterate**: Repeat until pixel-perfect

### MCP Server Integration (Condensed)

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx" }
    },
    "database": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres"],
      "env": { "DATABASE_URL": "postgresql://localhost:5432/myapp" }
    }
  }
}
```

**Security guidelines**: Use environment variables for secrets. Implement least-privilege access. Rotate API tokens regularly. Audit all MCP server interactions.

### Multi-Instance Parallel Strategy

Run multiple Claude Code instances for different components of the same project:

```bash
# Terminal 1: Database layer
claude --project my-app --focus database

# Terminal 2: API layer
claude --project my-app --focus api

# Terminal 3: Frontend
claude --project my-app --focus frontend
```

**Key benefits:**
- Prevents context switching between unrelated domains
- Each instance maintains focused context
- Natural parallelism without orchestration overhead

**When to use:**
- Large features spanning multiple layers
- Independent subsystem development
- Exploratory work on different approaches simultaneously

### Team Performance Metrics

Actual time savings observed in production usage:

| Task Category | Time Savings | Success Rate |
|--------------|-------------|-------------|
| Feature Development | 40-60% faster | 88% |
| Bug Fixes | 70% faster | 90% |
| Code Reviews | 50% faster | 93% |
| Documentation | 80% faster | 98% |
| UI/Styling (auto-accept) | 60% faster | 95% |
| Security Audits | 80% faster | 93% |

### Subagent Enhancements <!-- NEW in v2.0 -->

#### Worktree Isolation

Subagents can work in isolated git worktrees to prevent file conflicts:

```javascript
<Task>
  <subagent_type>general-purpose</subagent_type>
  <isolation>worktree</isolation>
  <description>Refactor auth module</description>
  <prompt>Refactor src/auth/ to use new token format.
  Working in isolated worktree - no conflicts with other agents.</prompt>
</Task>
```

**When to use worktree isolation:**
- Multiple agents editing overlapping files
- Risky refactoring that might need rollback
- Long-running tasks that shouldn't block other work

#### Background Agents

Run agents in the background for long-running tasks:

```javascript
<Task>
  <subagent_type>general-purpose</subagent_type>
  <run_in_background>true</run_in_background>
  <description>Full test suite</description>
  <prompt>Run complete test suite and report failures.</prompt>
</Task>
// Continue with other work while tests run
```

#### Agent Memory Persistence

Agents can persist findings across sessions:

```javascript
// Agent writes findings to a known location
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Codebase analysis</description>
  <prompt>Analyze codebase architecture. Write findings to
  .claude-library/contexts/architecture-analysis.md for future agents.</prompt>
</Task>

// Later agents read previous findings
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Implementation based on analysis</description>
  <prompt>Read .claude-library/contexts/architecture-analysis.md
  and implement the recommended changes.</prompt>
</Task>
```

### Skills with Context: Fork <!-- NEW in v2.0 -->

Skills can use `context: fork` to branch the conversation context, allowing exploration without polluting the main thread:

```markdown
---
name: explore-alternatives
description: Explore implementation alternatives without affecting main context
context: fork
---

Explore 3 different approaches to implement this feature.
Compare trade-offs. Report back the recommended approach only.
```

**When to use `context: fork`:**
- Exploratory research that generates lots of noise
- Comparing multiple implementation approaches
- Running speculative analysis that may not be needed

---

## 8. Template Snippets

### Agent Definition Template

```markdown
# {Agent Name}

## Identity
You are a {specific_role} specializing in {domain_area}.

## Responsibilities
1. **Primary**: {main_responsibility}
2. **Secondary**: {supporting_tasks}
3. **Quality**: {quality_assurance_role}

## What You SHOULD Do
- {Positive behavior 1}
- {Positive behavior 2}

## What You SHOULD NOT Do
- {Boundary 1 - prevents scope creep}
- {Boundary 2 - prevents anti-patterns}

## Available Tools
- **Read**: Analyze existing code (preferred for file content)
- **Edit**: Modify existing files (preferred over Write)
- **Grep**: Search for patterns in codebase
- **Glob**: Find files by name pattern
- **Bash**: Run commands (use carefully)
- **Task**: Spawn sub-agents (if orchestrator role)

## Success Criteria
- {Measurable outcome 1}
- {Measurable outcome 2}

## Error Handling
1. Identify the error type clearly
2. Attempt safe automatic recovery if possible
3. Escalate to user with clear explanation
4. Suggest alternative approaches
```

### Tool Description Template

```markdown
### Tool: {Tool Name}

**Purpose**: {One clear sentence - what this tool does}

**When to Use**:
- {Specific scenario 1}
- {Specific scenario 2}

**Parameters**:
- `param_name` (type, required/optional): Description
  - Example: `"example_value"`
  - Default: `value` (if optional)

**Returns**: {What the agent receives back}

**Example**:
{ToolName}(param_name="value", other_param=123)

**Common Mistakes**:
- Do not {common mistake 1}
- Do not {common mistake 2}
- Instead {correct approach}

**Success Indicators**:
- {How to know it worked}
```

**When to use full vs simplified descriptions:**
- **Full template**: Core tools used frequently, tools with complex parameters, tools where mistakes are common
- **Simplified template**: Secondary tools, obvious usage, well-known standard tools

#### Concrete Example: Read Tool Description

```markdown
### Read - File Content Retrieval

**Purpose**: Read and analyze file contents with line numbers

**When to Use**:
- Understanding existing code before modifications
- Reviewing configuration files
- Analyzing log files for debugging

**Parameters**:
- `file_path` (string, required): Absolute path from project root
  - Example: `"/Users/dev/project/src/auth.py"`
- `limit` (int, optional): Max lines to read (default: 2000)
- `offset` (int, optional): Starting line (default: 1)

**Returns**: File contents with line numbers (1-indexed)

**Example**:
Read(file_path="/path/to/file.py", limit=50)
# Returns first 50 lines with line numbers

**Token Efficiency**:
- For large files (>1000 lines): Use `limit` and `offset` to paginate
- To find specific code: Use Grep first, then Read the relevant sections

**Common Mistakes**:
- Do not read entire 5000-line files when only one function is needed
- Do not use Read to search - use Grep instead
- Do use Read for specific sections after Grep finds locations
```

### Command Workflow Template

```markdown
# /{command-name} Command

## Purpose
{Brief description of what this command accomplishes}

## Usage
/{command-name} "description of task"

## Workflow
Stage 1: {Name} (Parallel)
├─ Agent A: {Role}
├─ Agent B: {Role}
└─ Agent C: {Role}
    ↓
Stage 2: {Name} (Sequential)
├─ Agent D: {Role} (uses Stage 1 results)
└─ Agent E: {Role}
    ↓
Stage 3: {Name}
└─ Agent F: {Role} (final synthesis)

## Implementation

### Stage 1 (Parallel)
[Task blocks for agents A, B, C]

### Stage 2 (Sequential, depends on Stage 1)
[Task blocks using Stage 1 results]

## Quality Gates
- [ ] {Check 1}
- [ ] {Check 2}

## Error Handling
- Stage 1 failure: {recovery}
- Partial results: {continuation}
- Complete failure: {fallback}
```

### Registry Agent Entry Template

```json
{
  "agents": {
    "agent-name": {
      "file": "agents/agent-name.md",
      "description": "One-line description of agent purpose",
      "triggers": ["keyword1", "keyword2"],
      "contexts": ["context-file-1", "context-file-2"],
      "tools": ["Read", "Edit", "Grep", "Glob", "Bash"],
      "model": "sonnet",
      "thinking_patterns": ["tool-selection", "problem-decomposition"]
    }
  }
}
```

---

## Best Practices Summary

### DO

- Start with the simplest approach (prompt engineering) before escalating
- Use parallel execution for independent tasks
- Send all parallel Tasks in a single message
- Define clear agent boundaries and responsibilities
- Implement progressive quality gates with early termination
- Cache frequently used contexts
- Use checkpoints before risky operations
- Match model cost to task complexity (haiku for simple, opus for complex)
- Handle errors gracefully with fallback strategies
- Use custom agent types (`.claude/agents/`) for reusable personas
- Use worktree isolation when agents edit overlapping files
- Prune context to include only what's relevant
- Document tool parameters with examples and common mistakes

### DON'T

- Over-engineer simple tasks with complex orchestration
- Load all contexts upfront (use lazy loading)
- Run dependent tasks in parallel (use sequential chaining)
- Skip quality gates to save time
- Mix agent responsibilities (one agent, one concern)
- Use `Bash("cat file")` when `Read` tool exists
- Ignore error handling in agent workflows
- Use agents when a workflow suffices
- Use opus model for simple linting tasks
- Create files when editing existing ones works
- Forget to synthesize results from parallel agents
- Commit without explicit user approval

### Quick Reference: Pattern Selection

| I need to... | Use this pattern | Section |
|--------------|-----------------|---------|
| Run a simple task | Direct prompt engineering | [1. Core Principles](#1-core-principles) |
| Process steps in order | Sequential Workflow | [3. Workflow Patterns](#3-workflow-patterns) |
| Analyze multiple things at once | Parallel Workflow | [3. Workflow Patterns](#3-workflow-patterns) |
| Coordinate a complex project | Hierarchical Workflow | [3. Workflow Patterns](#3-workflow-patterns) |
| Route to different handlers | Routing Workflow | [3. Workflow Patterns](#3-workflow-patterns) |
| Iteratively improve quality | Evaluator-Optimizer | [3. Workflow Patterns](#3-workflow-patterns) |
| Speed up with parallelism | Parallel Execution patterns | [4. Parallel Execution](#4-parallel-execution) |
| Handle failures gracefully | Error Handling patterns | [5. Error Handling](#5-error-handling--recovery) |
| Reduce token usage | Context Optimization | [6. Context Optimization](#6-context-optimization) |
| Set up team workflows | Production Team Patterns | [7. Production Team Patterns](#7-production-team-patterns) |
| Define new agents | Template Snippets | [8. Template Snippets](#8-template-snippets) |

---

*Patterns consolidated from: Anthropic "Building Effective Agents", Claude Agent Framework v1 patterns, and production team usage. See archived sources in `archive/v1-patterns/` for original documents.*
