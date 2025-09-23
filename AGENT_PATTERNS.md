# Agent Implementation Patterns
*Real-world patterns and examples from production agent systems*

## Table of Contents
1. [Parallel Execution Patterns](#parallel-execution-patterns)
2. [TDD Workflow Implementation](#tdd-workflow-implementation)
3. [Error Handling & Recovery](#error-handling--recovery)
4. [Agent Communication](#agent-communication)
5. [Context Optimization](#context-optimization)
6. [Quality Gates](#quality-gates)
7. [Real-World Examples](#real-world-examples)

## Parallel Execution Patterns

### Pattern 1: Independent Analysis

When multiple agents need to analyze different aspects of the same problem:

```javascript
// PATTERN: Parallel Independent Analysis
// Use when: Agents don't depend on each other's output

// All three agents start SIMULTANEOUSLY
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Security analysis</description>
  <prompt>
    Analyze codebase for security vulnerabilities:
    - SQL injection risks
    - XSS vulnerabilities
    - Authentication flaws
    - Data exposure risks
  </prompt>
</Task>

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Performance analysis</description>
  <prompt>
    Analyze codebase for performance issues:
    - N+1 query problems
    - Memory leaks
    - Inefficient algorithms
    - Missing indexes
  </prompt>
</Task>

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Code quality analysis</description>
  <prompt>
    Analyze codebase for quality issues:
    - Code duplication
    - Complex functions
    - Missing tests
    - Poor naming
  </prompt>
</Task>
```

### Pattern 2: Parallel Implementation with Live Review

One agent implements while another reviews in real-time:

```javascript
// PATTERN: Parallel Implementation + Review
// Use when: You want immediate feedback during development

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Implementation</description>
  <prompt>
    [Engineer Agent Persona]

    Implement user authentication with:
    1. JWT tokens
    2. Refresh token rotation
    3. Rate limiting
    4. Password hashing with bcrypt

    Follow TDD approach:
    - Write tests first
    - Implement to pass tests
    - Refactor for quality
  </prompt>
</Task>

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Real-time review</description>
  <prompt>
    [Reviewer Agent Persona]

    As the engineer implements, review for:
    - Security vulnerabilities
    - Performance issues
    - Best practices violations
    - Test coverage gaps

    Provide immediate feedback on critical issues.
  </prompt>
</Task>
```

### Pattern 3: Hierarchical Decomposition

Parent agent spawns specialized children for subtasks:

```javascript
// PATTERN: Hierarchical Task Decomposition
// Use when: Complex problem needs breakdown

// Parent Orchestrator
function orchestrateDebug(issue) {
  // Analyze issue type
  const issueType = analyzeIssue(issue);

  // Spawn appropriate specialists
  if (issueType.includes('frontend')) {
    spawnAgent('frontend-debugger', {
      focus: ['hydration', 'state', 'rendering']
    });
  }

  if (issueType.includes('backend')) {
    spawnAgent('backend-debugger', {
      focus: ['api', 'database', 'auth']
    });
  }

  if (issueType.includes('performance')) {
    spawnAgent('performance-debugger', {
      focus: ['queries', 'caching', 'bundling']
    });
  }

  // Coordinate results
  synthesizeFindings();
}
```

## TDD Workflow Implementation

### The Red-Green-Refactor Pattern

```markdown
# TDD Implementation Workflow

## Stage 1: RED (Write Failing Tests)

### Test Specification Agent
```typescript
// User Authentication Tests
describe('UserAuthentication', () => {
  describe('Registration', () => {
    it('should hash passwords with bcrypt', async () => {
      const password = 'testPassword123';
      const user = await registerUser({
        email: 'test@example.com',
        password
      });

      expect(user.password).not.toBe(password);
      expect(await bcrypt.compare(password, user.password)).toBe(true);
    });

    it('should validate email format', async () => {
      await expect(registerUser({
        email: 'invalid-email',
        password: 'valid123'
      })).rejects.toThrow('Invalid email format');
    });

    it('should enforce password requirements', async () => {
      await expect(registerUser({
        email: 'test@example.com',
        password: '123' // Too short
      })).rejects.toThrow('Password must be at least 8 characters');
    });
  });
});
```

## Stage 2: GREEN (Make Tests Pass)

### Implementation Agent
```typescript
// Minimal implementation to pass tests
export async function registerUser({ email, password }) {
  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    throw new Error('Invalid email format');
  }

  // Password validation
  if (password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }

  // Hash password
  const hashedPassword = await bcrypt.hash(password, 10);

  // Save user (simplified)
  const user = {
    email,
    password: hashedPassword
  };

  return user;
}
```

## Stage 3: REFACTOR (Improve Code Quality)

### Refactoring Agent
```typescript
// Refactored with better structure and error handling
import { z } from 'zod';

// Validation schemas
const UserRegistrationSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[0-9]/, 'Password must contain number')
});

// Service layer
export class AuthService {
  private readonly SALT_ROUNDS = 10;

  async registerUser(data: unknown) {
    // Validate input
    const validated = UserRegistrationSchema.parse(data);

    // Check for existing user
    const existing = await this.findUserByEmail(validated.email);
    if (existing) {
      throw new ConflictError('Email already registered');
    }

    // Hash password with error handling
    const hashedPassword = await this.hashPassword(validated.password);

    // Create user with transaction
    return await this.createUser({
      email: validated.email,
      password: hashedPassword
    });
  }

  private async hashPassword(password: string): Promise<string> {
    try {
      return await bcrypt.hash(password, this.SALT_ROUNDS);
    } catch (error) {
      throw new InternalError('Password hashing failed');
    }
  }
}
```
```

## Error Handling & Recovery

### Pattern 1: Graceful Degradation

```javascript
// PATTERN: Try primary approach, fallback to alternatives
async function executeWithFallback(task) {
  const strategies = [
    primaryStrategy,
    fallbackStrategy,
    manualStrategy
  ];

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

### Pattern 2: Retry with Exponential Backoff

```javascript
// PATTERN: Retry transient failures
async function retryWithBackoff(fn, maxRetries = 3) {
  let lastError;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      // Check if error is retryable
      if (!isRetryable(error)) {
        throw error;
      }

      // Exponential backoff
      const delay = Math.min(1000 * Math.pow(2, i), 10000);
      await sleep(delay);
    }
  }

  throw lastError;
}

function isRetryable(error) {
  return [
    'TIMEOUT',
    'NETWORK_ERROR',
    'RATE_LIMIT',
    'TEMPORARY_FAILURE'
  ].includes(error.code);
}
```

### Pattern 3: Circuit Breaker

```javascript
// PATTERN: Prevent cascading failures
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
      if (Date.now() < this.nextAttempt) {
        throw new Error('Circuit breaker is OPEN');
      }
      this.state = 'HALF_OPEN';
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.timeout;
    }
  }
}
```

## Agent Communication

### Pattern 1: Shared Context Passing

```javascript
// PATTERN: Pass context between sequential agents
const sharedContext = {
  architecture: null,
  tests: null,
  implementation: null,
  review: null
};

// Stage 1: Architecture
sharedContext.architecture = await runAgent('architect', {
  task: 'Design user authentication',
  output: 'architecture_spec'
});

// Stage 2: Tests (uses architecture)
sharedContext.tests = await runAgent('test-engineer', {
  task: 'Write tests based on architecture',
  input: sharedContext.architecture,
  output: 'test_specifications'
});

// Stage 3: Implementation (uses both)
sharedContext.implementation = await runAgent('engineer', {
  task: 'Implement to pass tests',
  architecture: sharedContext.architecture,
  tests: sharedContext.tests,
  output: 'implementation_code'
});
```

### Pattern 2: Event-Driven Coordination

```javascript
// PATTERN: Agents communicate via events
class AgentEventBus {
  constructor() {
    this.events = new EventEmitter();
    this.agents = new Map();
  }

  registerAgent(name, agent) {
    this.agents.set(name, agent);

    // Subscribe to relevant events
    agent.subscribedEvents.forEach(eventType => {
      this.events.on(eventType, (data) => {
        agent.handleEvent(eventType, data);
      });
    });
  }

  emit(event, data) {
    this.events.emit(event, {
      timestamp: Date.now(),
      source: data.source,
      payload: data.payload
    });
  }
}

// Agent implementation
class ReviewAgent {
  subscribedEvents = ['code.updated', 'tests.completed'];

  handleEvent(eventType, data) {
    switch(eventType) {
      case 'code.updated':
        this.reviewCode(data.payload.files);
        break;
      case 'tests.completed':
        this.validateCoverage(data.payload.coverage);
        break;
    }
  }
}
```

### Pattern 3: Result Aggregation

```javascript
// PATTERN: Combine results from parallel agents
async function aggregateResults(agents) {
  // Run all agents in parallel
  const results = await Promise.allSettled(
    agents.map(agent => runAgent(agent))
  );

  // Separate successes and failures
  const successes = results
    .filter(r => r.status === 'fulfilled')
    .map(r => r.value);

  const failures = results
    .filter(r => r.status === 'rejected')
    .map(r => ({
      agent: r.reason.agent,
      error: r.reason.message
    }));

  // Synthesize successful results
  const synthesis = {
    consensus: findConsensus(successes),
    conflicts: findConflicts(successes),
    recommendations: mergeRecommendations(successes),
    failures: failures
  };

  return synthesis;
}
```

## Context Optimization

### Pattern 1: Lazy Loading

```javascript
// PATTERN: Load context only when needed
class ContextManager {
  constructor() {
    this.loaded = new Map();
    this.cache = new Map();
  }

  async getContext(name) {
    // Return cached if available
    if (this.cache.has(name)) {
      return this.cache.get(name);
    }

    // Load on demand
    const context = await this.loadContext(name);
    this.cache.set(name, context);
    return context;
  }

  async loadContext(name) {
    const path = `.claude-library/contexts/${name}.md`;
    return await readFile(path);
  }

  // Preload contexts for known task types
  async preloadForTask(taskType) {
    const contexts = this.getRequiredContexts(taskType);
    await Promise.all(
      contexts.map(ctx => this.getContext(ctx))
    );
  }

  getRequiredContexts(taskType) {
    const contextMap = {
      'api': ['api-patterns', 'auth', 'validation'],
      'database': ['schema', 'migrations', 'optimization'],
      'frontend': ['components', 'state', 'styling'],
      'testing': ['test-patterns', 'mocks', 'coverage']
    };

    return contextMap[taskType] || ['project'];
  }
}
```

### Pattern 2: Context Pruning

```javascript
// PATTERN: Include only relevant parts of context
function pruneContext(fullContext, task) {
  const relevant = [];

  // Extract only sections that match task keywords
  const sections = fullContext.split('##');
  const keywords = extractKeywords(task);

  sections.forEach(section => {
    const sectionScore = calculateRelevance(section, keywords);
    if (sectionScore > 0.5) {
      relevant.push(section);
    }
  });

  return relevant.join('\n##');
}

function calculateRelevance(text, keywords) {
  const words = text.toLowerCase().split(/\s+/);
  let matches = 0;

  keywords.forEach(keyword => {
    if (words.includes(keyword.toLowerCase())) {
      matches++;
    }
  });

  return matches / keywords.length;
}
```

### Pattern 3: Context Inheritance

```javascript
// PATTERN: Build specialized contexts from base contexts
class ContextHierarchy {
  constructor() {
    this.contexts = {
      base: {
        content: 'Project fundamentals...',
        children: ['frontend', 'backend', 'database']
      },
      frontend: {
        parent: 'base',
        content: 'Frontend specific...',
        children: ['react', 'vue', 'angular']
      },
      react: {
        parent: 'frontend',
        content: 'React specific patterns...'
      }
    };
  }

  getFullContext(name) {
    const context = this.contexts[name];
    let fullContent = context.content;

    // Include parent context
    if (context.parent) {
      fullContent = this.getFullContext(context.parent) + '\n' + fullContent;
    }

    return fullContent;
  }
}
```

## Quality Gates

### Pattern 1: Progressive Quality Checks

```javascript
// PATTERN: Multiple quality gates with early termination
async function qualityGatePipeline(code) {
  const gates = [
    { name: 'Syntax', fn: checkSyntax, critical: true },
    { name: 'Linting', fn: runLinter, critical: true },
    { name: 'Type Check', fn: checkTypes, critical: true },
    { name: 'Unit Tests', fn: runUnitTests, critical: true },
    { name: 'Coverage', fn: checkCoverage, critical: false },
    { name: 'Security', fn: scanSecurity, critical: true },
    { name: 'Performance', fn: checkPerformance, critical: false },
    { name: 'Integration', fn: runIntegrationTests, critical: false }
  ];

  const results = {
    passed: [],
    failed: [],
    warnings: []
  };

  for (const gate of gates) {
    try {
      const result = await gate.fn(code);

      if (result.passed) {
        results.passed.push(gate.name);
      } else if (gate.critical) {
        results.failed.push({
          gate: gate.name,
          reason: result.reason
        });
        break; // Stop on critical failure
      } else {
        results.warnings.push({
          gate: gate.name,
          reason: result.reason
        });
      }
    } catch (error) {
      if (gate.critical) {
        throw new Error(`Critical gate ${gate.name} failed: ${error.message}`);
      }
      results.warnings.push({
        gate: gate.name,
        error: error.message
      });
    }
  }

  return results;
}
```

### Pattern 2: Automated Rollback

```javascript
// PATTERN: Rollback on quality gate failure
class DeploymentPipeline {
  async deploy(code) {
    const checkpoint = await this.createCheckpoint();

    try {
      // Run quality gates
      const quality = await this.runQualityGates(code);
      if (!quality.passed) {
        throw new Error('Quality gates failed');
      }

      // Deploy
      await this.performDeployment(code);

      // Smoke tests
      const smokeTests = await this.runSmokeTests();
      if (!smokeTests.passed) {
        throw new Error('Smoke tests failed');
      }

      // Success
      await this.commitDeployment();
      return { success: true };

    } catch (error) {
      // Automatic rollback
      await this.rollback(checkpoint);
      return {
        success: false,
        error: error.message,
        rolledBack: true
      };
    }
  }
}
```

## Real-World Examples

### Example 1: Building a REST API

```javascript
// Complete workflow for building REST API

// Step 1: Architecture (Parallel - 30 seconds)
const tasks = [
  {
    agent: 'api-architect',
    prompt: `Design REST API for user management:
      - CRUD operations
      - Authentication
      - Authorization
      - Rate limiting
      Requirements: RESTful, JWT auth, role-based access`
  },
  {
    agent: 'database-architect',
    prompt: `Design database schema for:
      - User profiles
      - Sessions
      - Permissions
      - Audit logs`
  },
  {
    agent: 'test-planner',
    prompt: `Create test specifications for:
      - API endpoints
      - Auth flows
      - Error cases
      - Performance`
  }
];

// Step 2: Implementation (Parallel - 45 seconds)
const implementation = [
  {
    agent: 'backend-engineer',
    prompt: `Implement based on architecture:
      ${architectureResults}
      Use TDD approach with provided tests`
  },
  {
    agent: 'security-reviewer',
    prompt: `Review implementation for:
      - SQL injection
      - JWT vulnerabilities
      - Rate limiting bypass
      - Data exposure`
  }
];

// Step 3: Integration & Documentation (15 seconds)
const finalization = {
  agent: 'integration-specialist',
  prompt: `
    - Verify all endpoints work
    - Generate API documentation
    - Create postman collection
    - Write deployment guide`
};
```

### Example 2: Debugging Production Issue

```javascript
// Hierarchical debugging workflow

// Root orchestrator analyzes symptoms
const rootAnalysis = {
  agent: 'debug-orchestrator',
  prompt: `
    Issue: API response times degraded from 200ms to 5s
    Symptoms:
    - Started 3 hours ago
    - Affects all endpoints
    - No recent deployments
    - CPU usage normal

    Determine root cause category and spawn specialists.`
};

// Spawns parallel specialists based on analysis
const specialists = [
  {
    agent: 'database-debugger',
    prompt: `Check for:
      - Slow queries
      - Lock contention
      - Connection pool exhaustion
      - Index issues`
  },
  {
    agent: 'cache-debugger',
    prompt: `Check for:
      - Cache misses
      - Redis connection issues
      - Eviction problems
      - Memory pressure`
  },
  {
    agent: 'network-debugger',
    prompt: `Check for:
      - DNS issues
      - Proxy problems
      - CDN failures
      - Rate limiting`
  }
];

// Synthesis and solution
const solution = {
  agent: 'solution-architect',
  prompt: `
    Based on findings:
    ${specialistResults}

    Provide:
    1. Root cause
    2. Immediate fix
    3. Long-term solution
    4. Prevention measures`
};
```

### Example 3: Feature Migration

```javascript
// Complex migration workflow

// Phase 1: Analysis
const analysis = {
  parallel: [
    {
      agent: 'code-analyzer',
      prompt: 'Map all dependencies and usage of old feature'
    },
    {
      agent: 'risk-assessor',
      prompt: 'Identify migration risks and rollback points'
    },
    {
      agent: 'test-analyzer',
      prompt: 'Identify all tests that need updating'
    }
  ]
};

// Phase 2: Planning
const planning = {
  agent: 'migration-planner',
  prompt: `Create migration plan based on:
    ${analysisResults}
    Include:
    - Step-by-step process
    - Parallel migration paths
    - Rollback procedures
    - Success metrics`
};

// Phase 3: Execution (Multiple parallel streams)
const execution = {
  streams: [
    {
      name: 'Database Migration',
      agents: ['db-migrator', 'db-validator']
    },
    {
      name: 'Code Migration',
      agents: ['code-migrator', 'test-updater']
    },
    {
      name: 'Configuration',
      agents: ['config-updater', 'env-validator']
    }
  ]
};

// Phase 4: Validation
const validation = {
  sequential: [
    'integration-tester',
    'performance-validator',
    'security-scanner',
    'documentation-updater'
  ]
};
```

## Performance Benchmarks

### Execution Time Comparison

| Workflow Type | Sequential | Parallel | Improvement |
|--------------|------------|----------|-------------|
| 3-Agent Analysis | 90s | 30s | 3x faster |
| 5-Agent Review | 150s | 35s | 4.3x faster |
| 10-Agent Debug | 300s | 45s | 6.7x faster |
| TDD Cycle | 180s | 75s | 2.4x faster |

### Context Loading Performance

| Strategy | Load Time | Memory | Cache Hit |
|----------|-----------|---------|-----------|
| Full Load | 5s | 250KB | N/A |
| Lazy Load | 0.5s | 10KB | 0% |
| Cached Load | 0.1s | 10KB | 85% |
| Pruned Load | 0.3s | 5KB | 60% |

## Best Practices Summary

### DO:
- ✅ Use parallel execution for independent tasks
- ✅ Implement progressive quality gates
- ✅ Cache frequently used contexts
- ✅ Define clear agent boundaries
- ✅ Handle errors gracefully with fallbacks
- ✅ Provide progress feedback
- ✅ Use appropriate workflow patterns

### DON'T:
- ❌ Load all contexts upfront
- ❌ Run dependent tasks in parallel
- ❌ Skip quality gates
- ❌ Ignore error handling
- ❌ Mix agent responsibilities
- ❌ Forget progress reporting
- ❌ Over-engineer simple tasks

## Conclusion

These patterns represent battle-tested approaches from production agent systems. Start with simple patterns and progressively adopt more sophisticated ones as your system grows. Remember: the goal is to make development faster and more reliable, not more complex.

---

*Patterns extracted from AfroLove AI Dating Platform production system*