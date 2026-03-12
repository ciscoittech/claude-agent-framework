# Agent Reference Patterns
*Comprehensive guide combining Anthropic's "Building Effective Agents" principles with Claude Agent Framework patterns*

## Table of Contents
1. [Anthropic Agent Principles](#anthropic-agent-principles)
2. [Workflows vs Agents Distinction](#workflows-vs-agents-distinction)
3. [The 5 Core Workflow Types](#the-5-core-workflow-types)
4. [Tool Design Principles](#tool-design-principles)
5. [Implementation Strategies](#implementation-strategies)
6. [Decision Trees](#decision-trees)
7. [Template Snippets](#template-snippets)
8. [Common Pitfalls](#common-pitfalls)
9. [Performance Optimization](#performance-optimization)
10. [Real-World Examples](#real-world-examples)

## Anthropic Agent Principles

### Core Philosophy from "Building Effective Agents"

Anthropic's research emphasizes that **effective agents are built on sound workflows**, not complex reasoning loops. The key insight: **start with workflows, add agency only when needed**.

#### The Hierarchy of Solutions
```
1. Prompt Engineering (simplest)
   ↓
2. Structured Workflows (most effective)
   ↓
3. Agentic Systems (most complex)
```

### When to Choose Each Approach

| Problem Type | Solution | Example |
|-------------|----------|---------|
| **Single-step task** | Prompt Engineering | "Summarize this document" |
| **Multi-step process** | Workflow | "Analyze → Plan → Implement → Review" |
| **Dynamic decisions** | Agent | "Research unknown topic, adapt strategy based on findings" |

### The Agent vs Workflow Test

Ask yourself:
- ✅ **Workflow**: Can I define the steps in advance?
- ✅ **Agent**: Do the steps depend on dynamic intermediate results?

## Workflows vs Agents Distinction

### Workflows: Predictable Multi-Step Processes

**Characteristics:**
- Steps are known in advance
- Dependencies are clear
- Outputs are predictable
- Failures can be anticipated

**Best for:**
- Software development processes
- Code review workflows
- Testing pipelines
- Documentation generation

### Agents: Dynamic Decision-Making Systems

**Characteristics:**
- Steps emerge based on context
- Decisions depend on intermediate results
- Outputs vary significantly
- Requires adaptive strategies

**Best for:**
- Research and analysis
- Complex debugging
- Creative problem solving
- User interaction systems

## The 5 Core Workflow Types

### 1. Prompt Chaining (Sequential)

**Definition**: Each step's output becomes the next step's input.

**When to use**: Dependencies between steps, progressive refinement needed.

#### Claude Code Implementation
```javascript
// Sequential execution with context passing
async function promptChaining(initialInput) {
  // Step 1: Architecture
  const architecture = await runTask({
    type: 'general-purpose',
    description: 'Design system architecture',
    prompt: `Design architecture for: ${initialInput}`
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

#### Template Pattern
```markdown
# Prompt Chaining Workflow

## Stage {N}: {Stage Name}
**Input**: {Previous stage output or initial input}
**Agent**: {Specialized agent name}
**Output**: {Structured output format}

### Prompt Template
```
You are a {role} specializing in {domain}.

Input from previous stage:
{previous_output}

Your task:
{specific_task_description}

Output format:
{structured_format}
```

## Dependencies
- Requires: {Previous stage completion}
- Provides: {Input for next stage}
- Critical path: {Yes/No}
```

### 2. Routing (Conditional Branching)

**Definition**: Direct different inputs to specialized handlers based on classification.

**When to use**: Different input types need different processing approaches.

#### Claude Code Implementation
```javascript
// Router agent with specialized handlers
async function routingWorkflow(input) {
  // Classification step
  const classification = await runTask({
    type: 'general-purpose',
    description: 'Classify input type',
    prompt: `Classify this request and return JSON:
    "${input}"

    Categories: [bug_report, feature_request, question, documentation]

    Return: {"type": "category", "confidence": 0.9, "reasoning": "why"}`
  });

  const { type } = JSON.parse(classification.result);

  // Route to appropriate specialist
  const handlers = {
    bug_report: () => runTask({
      type: 'general-purpose',
      description: 'Debug issue',
      prompt: `[Load debugging agent]
      Analyze and fix this bug: ${input}`
    }),

    feature_request: () => runTask({
      type: 'general-purpose',
      description: 'Implement feature',
      prompt: `[Load feature agent]
      Design and implement: ${input}`
    }),

    question: () => runTask({
      type: 'general-purpose',
      description: 'Answer question',
      prompt: `[Load support agent]
      Answer this question: ${input}`
    }),

    documentation: () => runTask({
      type: 'general-purpose',
      description: 'Create documentation',
      prompt: `[Load documentation agent]
      Document this: ${input}`
    })
  };

  return handlers[type]?.() || handleUnknown(input);
}
```

#### Template Pattern
```markdown
# Routing Workflow

## Classification Stage
**Agent**: classifier
**Purpose**: Determine input type and route appropriately

### Classification Prompt
```
Analyze this input and classify it:
"{input}"

Available routes:
- Route A: {description and criteria}
- Route B: {description and criteria}
- Route C: {description and criteria}

Return JSON: {"route": "route_name", "confidence": 0.95, "data": {}}
```

## Route Handlers

### Route A: {Name}
**Trigger**: {Classification criteria}
**Agent**: {Specialized agent}
**Process**: {Specific workflow}

### Route B: {Name}
**Trigger**: {Classification criteria}
**Agent**: {Specialized agent}
**Process**: {Specific workflow}

## Error Handling
- Unknown input: {Fallback strategy}
- Low confidence: {Human escalation}
- Multiple matches: {Disambiguation process}
```

### 3. Parallelization (Concurrent Execution)

**Definition**: Multiple independent tasks execute simultaneously.

**When to use**: Tasks are independent, speed is important.

#### Claude Code Implementation
```javascript
// Parallel execution using Task tool
async function parallelWorkflow(input) {
  // ALL TASKS SENT IN SINGLE MESSAGE - KEY FOR PARALLELIZATION
  const results = await Promise.allSettled([
    runTask({
      type: 'general-purpose',
      description: 'Security analysis',
      prompt: `[Load security specialist]
      Analyze security implications of: ${input}`
    }),

    runTask({
      type: 'general-purpose',
      description: 'Performance analysis',
      prompt: `[Load performance specialist]
      Analyze performance impact of: ${input}`
    }),

    runTask({
      type: 'general-purpose',
      description: 'UX analysis',
      prompt: `[Load UX specialist]
      Analyze user experience of: ${input}`
    }),

    runTask({
      type: 'general-purpose',
      description: 'Technical feasibility',
      prompt: `[Load technical architect]
      Assess implementation feasibility of: ${input}`
    })
  ]);

  // Process results
  const successful = results
    .filter(r => r.status === 'fulfilled')
    .map(r => r.value);

  const failed = results
    .filter(r => r.status === 'rejected')
    .map(r => r.reason);

  return { successful, failed, summary: synthesizeResults(successful) };
}
```

#### Performance Optimization
```javascript
// CRITICAL: Send all Tasks in ONE message for true parallelization
// ✅ CORRECT - Parallel execution
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Security analysis</description>
  <prompt>Analyze security...</prompt>
</Task>
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>Performance analysis</description>
  <prompt>Analyze performance...</prompt>
</Task>
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>UX analysis</description>
  <prompt>Analyze UX...</prompt>
</Task>

// ❌ WRONG - Sequential execution (3x slower)
// First task, wait for completion, then second task, etc.
```

#### Template Pattern
```markdown
# Parallelization Workflow

## Parallel Execution Block
**Execution**: All tasks start simultaneously
**Duration**: ~{estimated time}
**Dependencies**: None between parallel tasks

### Task A: {Name}
**Agent**: {Specialist name}
**Focus**: {Specific analysis area}
**Output**: {Expected format}

### Task B: {Name}
**Agent**: {Specialist name}
**Focus**: {Specific analysis area}
**Output**: {Expected format}

### Task C: {Name}
**Agent**: {Specialist name}
**Focus**: {Specific analysis area}
**Output**: {Expected format}

## Synthesis Stage
**Input**: All parallel results
**Process**: {How to combine results}
**Output**: {Final deliverable}

## Error Handling
- Partial failure: {Continue with available results}
- Complete failure: {Fallback strategy}
- Timeout: {Graceful degradation}
```

### 4. Orchestrator-Workers (Hierarchical)

**Definition**: Parent agent coordinates multiple child agents with different roles.

**When to use**: Complex problems requiring coordination and specialization.

#### Claude Code Implementation
```javascript
// Orchestrator pattern with specialized workers
async function orchestratorWorkflow(complexProblem) {
  // Orchestrator analyzes and plans
  const plan = await runTask({
    type: 'general-purpose',
    description: 'Problem analysis and planning',
    prompt: `You are the orchestrator for complex problem solving.

    Problem: ${complexProblem}

    Analyze and create:
    1. Problem breakdown
    2. Required specialist types
    3. Coordination strategy
    4. Success criteria

    Return structured plan.`
  });

  // Spawn specialists based on plan
  const workers = await spawnWorkers(plan);

  // Coordinate worker execution
  const coordination = await coordinateWorkers(workers, plan);

  // Synthesize final result
  return synthesizeResults(coordination);
}

async function spawnWorkers(plan) {
  // Dynamic worker spawning based on plan
  const workerTasks = plan.specialists.map(specialist =>
    runTask({
      type: 'general-purpose',
      description: `${specialist.role} specialist`,
      prompt: `You are a ${specialist.role} specialist.

      Your assignment: ${specialist.task}
      Context: ${specialist.context}
      Deliverables: ${specialist.deliverables}

      Work independently but be ready to coordinate with other specialists.`
    })
  );

  return Promise.allSettled(workerTasks);
}
```

#### Template Pattern
```markdown
# Orchestrator-Workers Workflow

## Orchestrator Agent
**Role**: Project coordination and planning
**Responsibilities**:
- Problem analysis and decomposition
- Specialist selection and spawning
- Progress monitoring and coordination
- Result synthesis and quality assurance

### Orchestrator Prompt Template
```
You are the orchestrator for {domain} problems.

Problem: {complex_problem}

Your tasks:
1. Analyze problem complexity and requirements
2. Identify required specialist types
3. Create coordination plan
4. Define success criteria
5. Monitor progress and adjust strategy

Available specialists: {specialist_list}

Return: Structured execution plan
```

## Worker Specialists

### Worker Type A: {Specialist Name}
**Domain**: {Area of expertise}
**Spawned when**: {Conditions}
**Responsibilities**: {Specific tasks}
**Reports to**: Orchestrator
**Coordinates with**: {Other workers}

### Worker Type B: {Specialist Name}
**Domain**: {Area of expertise}
**Spawned when**: {Conditions}
**Responsibilities**: {Specific tasks}
**Reports to**: Orchestrator
**Coordinates with**: {Other workers}

## Coordination Protocol
1. **Planning**: Orchestrator creates master plan
2. **Spawning**: Workers created with specific roles
3. **Execution**: Workers execute with coordination checkpoints
4. **Synthesis**: Orchestrator combines worker outputs
5. **Validation**: Quality gates and success criteria
```

### 5. Evaluator-Optimizer (Iterative Improvement)

**Definition**: Generate solutions, evaluate quality, and iteratively improve.

**When to use**: Quality is critical, multiple iterations can improve results.

#### Claude Code Implementation
```javascript
// Iterative improvement with evaluation feedback
async function evaluatorOptimizer(task, maxIterations = 3) {
  let currentSolution = null;
  let bestSolution = null;
  let bestScore = 0;

  for (let iteration = 0; iteration < maxIterations; iteration++) {
    // Generate solution
    const solution = await runTask({
      type: 'general-purpose',
      description: `Solution generation - iteration ${iteration + 1}`,
      prompt: `Generate solution for: ${task}

      ${currentSolution ? `Previous solution: ${currentSolution}` : ''}
      ${currentSolution ? `Previous feedback: ${currentSolution.feedback}` : ''}

      Improve based on feedback or create initial solution.`
    });

    // Evaluate solution
    const evaluation = await runTask({
      type: 'general-purpose',
      description: `Solution evaluation - iteration ${iteration + 1}`,
      prompt: `Evaluate this solution:
      ${solution.result}

      Criteria:
      - Technical correctness (1-10)
      - Performance efficiency (1-10)
      - Security compliance (1-10)
      - Maintainability (1-10)
      - User experience (1-10)

      Return: {"score": 85, "feedback": "detailed feedback", "improvements": ["list"]}`
    });

    const { score, feedback, improvements } = JSON.parse(evaluation.result);

    // Track best solution
    if (score > bestScore) {
      bestScore = score;
      bestSolution = { ...solution, score, feedback, improvements };
    }

    // Early termination if excellent
    if (score >= 95) {
      break;
    }

    currentSolution = { ...solution, feedback, improvements };
  }

  return bestSolution;
}
```

#### Template Pattern
```markdown
# Evaluator-Optimizer Workflow

## Generator Agent
**Role**: Solution creation and improvement
**Approach**: Iterative enhancement based on feedback

### Generator Prompt Template
```
You are a solution generator for {domain}.

Task: {specific_task}

Iteration: {N} of {max_iterations}
Previous solution: {previous_solution}
Evaluation feedback: {evaluation_feedback}
Improvement areas: {improvement_list}

Generate an improved solution that addresses the feedback.
```

## Evaluator Agent
**Role**: Solution assessment and feedback
**Criteria**: {Specific evaluation metrics}

### Evaluator Prompt Template
```
You are a solution evaluator for {domain}.

Solution to evaluate:
{solution_text}

Evaluation criteria:
- Criterion 1: {description} (weight: {X}%)
- Criterion 2: {description} (weight: {Y}%)
- Criterion 3: {description} (weight: {Z}%)

Return JSON:
{
  "overall_score": 85,
  "criterion_scores": {"criterion1": 90, "criterion2": 80},
  "strengths": ["list of strengths"],
  "weaknesses": ["list of weaknesses"],
  "improvements": ["specific improvement suggestions"],
  "priority": "high|medium|low"
}
```

## Optimization Loop
1. **Generate**: Create solution (or improve previous)
2. **Evaluate**: Score against criteria
3. **Decide**: Continue iterating or accept solution
4. **Optimize**: Apply feedback for next iteration

## Termination Conditions
- Maximum iterations reached
- Score threshold achieved (e.g., 95%)
- No improvement for N iterations
- Resource/time limits
```

## Tool Design Principles

### Anthropic's Tool Design Guidelines

#### 1. Granular Tools Over Multi-Purpose Tools

**❌ Avoid:**
```javascript
// Too broad, unclear purpose
function fileManager(action, path, content, options) {
  if (action === 'read') return readFile(path);
  if (action === 'write') return writeFile(path, content);
  if (action === 'delete') return deleteFile(path);
  // ... many more actions
}
```

**✅ Prefer:**
```javascript
// Clear, single-purpose tools
function readFile(path) { /* focused implementation */ }
function writeFile(path, content) { /* focused implementation */ }
function deleteFile(path) { /* focused implementation */ }
```

#### 2. Tools Should Be Deterministic

**❌ Avoid:**
```javascript
// Unpredictable behavior
function smartAnalyze(code) {
  // Sometimes returns metrics, sometimes suggestions, sometimes both
  return Math.random() > 0.5 ? getMetrics(code) : getSuggestions(code);
}
```

**✅ Prefer:**
```javascript
// Predictable, consistent outputs
function analyzeCodeMetrics(code) { /* always returns metrics */ }
function generateCodeSuggestions(code) { /* always returns suggestions */ }
```

#### 3. Clear Error Handling and Feedback

**❌ Avoid:**
```javascript
// Silent failures or unclear errors
function processFile(path) {
  try {
    return doProcessing(path);
  } catch (e) {
    return null; // Lost error information
  }
}
```

**✅ Prefer:**
```javascript
// Clear error reporting
function processFile(path) {
  try {
    return { success: true, data: doProcessing(path) };
  } catch (error) {
    return {
      success: false,
      error: error.message,
      path: path,
      timestamp: new Date().toISOString()
    };
  }
}
```

### Claude Code Tool Optimization

#### Efficient Tool Usage Patterns

```javascript
// ✅ Batch operations when possible
const files = ['file1.js', 'file2.js', 'file3.js'];
const contents = await Promise.all(
  files.map(file => Read({ file_path: file }))
);

// ✅ Use appropriate tools for tasks
// Don't use Bash for file reading - use Read tool
const content = await Read({ file_path: '/path/to/file.js' });

// ✅ Leverage parallel capabilities
const analysis = await Promise.all([
  Grep({ pattern: 'security', glob: '**/*.js' }),
  Grep({ pattern: 'performance', glob: '**/*.js' }),
  Grep({ pattern: 'error', glob: '**/*.js' })
]);
```

#### Tool Selection Guidelines

| Task Type | Recommended Tool | Avoid |
|-----------|-----------------|--------|
| **File Reading** | `Read` | `Bash("cat file")` |
| **File Search** | `Grep` | `Bash("grep pattern")` |
| **File Patterns** | `Glob` | `Bash("find . -name")` |
| **Code Analysis** | `Read` + `Grep` | `Bash("awk/sed")` |
| **Agent Spawning** | `Task` | Multiple sequential requests |

## Implementation Strategies

### Strategy 1: Start Simple, Scale Progressively

#### Phase 1: Single Agent Workflows
```markdown
# Basic Implementation Agent
You are a software engineer implementing features.
- Read requirements
- Write code following TDD
- Ensure tests pass
- Document changes
```

#### Phase 2: Specialized Agents
```markdown
# Frontend Specialist
You are a React specialist focusing on:
- Component architecture
- State management
- Performance optimization
- Accessibility compliance

# Backend Specialist
You are a Node.js API specialist focusing on:
- RESTful design
- Database optimization
- Security best practices
- Error handling
```

#### Phase 3: Orchestrated Workflows
```markdown
# Feature Development Orchestrator
You coordinate a team of specialists:
1. Architect: Design system structure
2. Frontend: Implement user interface
3. Backend: Create API endpoints
4. QA: Test integration and quality
5. DevOps: Prepare deployment
```

### Strategy 2: Domain-Driven Agent Design

#### Organize by Business Domain
```
agents/
├── user-management/
│   ├── auth-specialist.md
│   ├── profile-specialist.md
│   └── permissions-specialist.md
├── payment-processing/
│   ├── stripe-specialist.md
│   ├── billing-specialist.md
│   └── fraud-detection-specialist.md
└── content-management/
    ├── cms-specialist.md
    ├── search-specialist.md
    └── media-specialist.md
```

#### Domain Specialist Template
```markdown
# {Domain} Specialist Agent

## Domain Expertise
You are an expert in {specific_domain} with deep knowledge of:
- {Core concept 1}
- {Core concept 2}
- {Core concept 3}

## Responsibilities
- {Primary responsibility}
- {Secondary responsibility}
- {Quality assurance role}

## Domain Knowledge
### Key Patterns
{Domain-specific patterns and best practices}

### Common Pitfalls
{Known issues and how to avoid them}

### Integration Points
{How this domain connects with others}

## Tools and Frameworks
- {Primary tools}
- {Secondary tools}
- {Monitoring/debugging tools}
```

### Strategy 3: Quality-First Implementation

#### Quality Gates Integration
```javascript
// Progressive quality gates
const qualityGates = [
  { name: 'Syntax', critical: true, fast: true },
  { name: 'Tests', critical: true, fast: false },
  { name: 'Security', critical: true, fast: false },
  { name: 'Performance', critical: false, fast: false },
  { name: 'Documentation', critical: false, fast: true }
];

async function executeWithQuality(task) {
  const result = await executeTask(task);

  // Run critical gates first and fast gates in parallel
  const criticalResults = await runCriticalGates(result);
  if (!criticalResults.passed) {
    throw new QualityGateError(criticalResults.failures);
  }

  // Run remaining gates
  const allResults = await runRemainingGates(result);

  return {
    result,
    quality: allResults,
    passed: allResults.every(gate => gate.passed || !gate.critical)
  };
}
```

## Decision Trees

### Workflow Type Selection

```
Is this a single, simple task?
├─ YES → Use Prompt Engineering
└─ NO → Are the steps known in advance?
    ├─ YES → Use Workflow
    │   └─ Are steps dependent on each other?
    │       ├─ YES → Prompt Chaining
    │       └─ NO → Parallelization
    └─ NO → Use Agent
        └─ Is there a clear input classification?
            ├─ YES → Routing
            └─ NO → Is quality critical with iteration needed?
                ├─ YES → Evaluator-Optimizer
                └─ NO → Orchestrator-Workers
```

### Agent Complexity Selection

```
What's the task complexity?
├─ Simple (1-2 steps)
│   └─ Use: Single specialized agent
├─ Medium (3-5 steps)
│   └─ Use: Sequential workflow with 2-3 agents
└─ Complex (6+ steps or unknown)
    └─ Use: Orchestrator pattern with worker agents
```

### Parallelization Decision

```
Can tasks run independently?
├─ YES → Are tasks similar in duration?
│   ├─ YES → Full parallelization
│   └─ NO → Staggered parallel execution
└─ NO → Sequential execution with batching
```

## Template Snippets

### Agent Definition Template

```markdown
# {Agent Name}

## Identity & Role
You are a {specific_role} specializing in {domain_area}. Your expertise includes {list_key_skills}.

## Core Responsibilities
1. **Primary**: {main_responsibility}
2. **Secondary**: {supporting_tasks}
3. **Quality**: {quality_assurance_role}

## What You SHOULD Do
- {Positive action 1}
- {Positive action 2}
- {Positive action 3}

## What You SHOULD NOT Do
- {Boundary 1}
- {Boundary 2}
- {Boundary 3}

## Available Tools
You have access to these Claude Code tools:
- **Read**: Reading files and analyzing code
- **Write**: Creating new files (use sparingly)
- **Edit**: Modifying existing files (preferred over Write)
- **Grep**: Searching for patterns in codebase
- **Glob**: Finding files by pattern
- **Bash**: Running commands (use carefully)
- **Task**: Spawning sub-agents (if orchestrator)

## Tool Restrictions
- NEVER use `find`, `grep`, `cat` commands via Bash
- ALWAYS prefer Read tool over Bash for file operations
- NEVER create files unless absolutely necessary
- NEVER commit code without explicit user approval

## Output Format
{Specify expected output structure}

## Success Criteria
- {Measurable outcome 1}
- {Measurable outcome 2}
- {Quality gate 3}

## Error Handling
When you encounter issues:
1. Identify the error type clearly
2. Attempt safe automatic recovery if possible
3. Escalate to user with clear explanation
4. Suggest alternative approaches

## Progress Reporting
Use this format for progress updates:
```
🚀 Starting: {task_name}
⏳ Progress: {current_step} ({percentage}% complete)
✅ Completed: {task_name}
❌ Failed: {task_name} - {reason}
```
```

### Command Workflow Template

```markdown
# /{command-name} Command

## Purpose
{Brief description of what this command accomplishes}

## Usage
```bash
/{command-name} "description of task"
```

## Workflow Overview
```
Stage 1: {Name} ({Duration})
├─ Agent A: {Role}
├─ Agent B: {Role}
└─ Agent C: {Role}
    ↓
Stage 2: {Name} ({Duration})
├─ Agent D: {Role}
└─ Agent E: {Role}
    ↓
Stage 3: {Name} ({Duration})
└─ Agent F: {Role}
```

## Implementation

### Stage 1: {Name} (Parallel Execution)
```javascript
// All tasks execute simultaneously
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>{Agent A task}</description>
  <prompt>
    [Load Agent A from .claude-library/agents/agent-a.md]

    Task: {specific_task_for_agent_a}
    Context: {relevant_context}
  </prompt>
</Task>
<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>{Agent B task}</description>
  <prompt>
    [Load Agent B from .claude-library/agents/agent-b.md]

    Task: {specific_task_for_agent_b}
    Context: {relevant_context}
  </prompt>
</Task>
```

### Stage 2: {Name} (Sequential/Dependent)
```javascript
// Uses results from Stage 1
const stage1Results = {stage1_summary};

<Task>
  <subagent_type>general-purpose</subagent_type>
  <description>{Agent D task}</description>
  <prompt>
    [Load Agent D from .claude-library/agents/agent-d.md]

    Previous stage results:
    {stage1Results}

    Your task: {build_upon_previous_results}
  </prompt>
</Task>
```

## Quality Gates
- [ ] {Quality check 1}
- [ ] {Quality check 2}
- [ ] {Quality check 3}

## Error Handling
- **Stage 1 failure**: {recovery_strategy}
- **Partial results**: {continuation_strategy}
- **Complete failure**: {fallback_approach}

## Expected Outputs
- {Deliverable 1}: {description}
- {Deliverable 2}: {description}
- {Summary report}: {description}
```

### Context Definition Template

```markdown
# {Context Name}

## Overview
This context provides {description_of_knowledge_area} for agents working on {domain_tasks}.

## Key Information

### {Category 1}
{Relevant data, patterns, or configurations}

### {Category 2}
{Relevant data, patterns, or configurations}

## Code Patterns

### Pattern 1: {Name}
```{language}
// Example implementation
{code_example}
```

### Pattern 2: {Name}
```{language}
// Example implementation
{code_example}
```

## Configuration Values
```{format}
{configuration_examples}
```

## Important Notes
- ⚠️ {Security consideration}
- 🚀 {Performance tip}
- 🔧 {Maintenance note}

## Related Contexts
- {Related context 1}: {relationship}
- {Related context 2}: {relationship}

## Usage Guidelines
This context should be loaded when:
- {Condition 1}
- {Condition 2}
- {Condition 3}
```

## Common Pitfalls

### Pitfall 1: Over-Engineering Simple Tasks

**❌ Wrong Approach:**
```javascript
// Using orchestrator for simple file creation
const orchestrator = new ComplexOrchestrator();
orchestrator.addAgent('analyst');
orchestrator.addAgent('planner');
orchestrator.addAgent('implementer');
orchestrator.addAgent('reviewer');
await orchestrator.execute('create hello world file');
```

**✅ Right Approach:**
```javascript
// Simple prompt for simple task
await runTask({
  type: 'general-purpose',
  description: 'Create hello world file',
  prompt: 'Create a simple hello world application file.'
});
```

### Pitfall 2: Sequential Execution of Independent Tasks

**❌ Wrong Approach:**
```javascript
// Sequential when parallel is possible (3x slower)
const security = await analyzeSecurityRisks(code);
const performance = await analyzePerformance(code);
const quality = await analyzeQuality(code);
```

**✅ Right Approach:**
```javascript
// Parallel execution for independent analyses
const [security, performance, quality] = await Promise.all([
  analyzeSecurityRisks(code),
  analyzePerformance(code),
  analyzeQuality(code)
]);
```

### Pitfall 3: Overloaded Agent Responsibilities

**❌ Wrong Approach:**
```markdown
# Super Agent (trying to do everything)
You are responsible for:
- Architecture design
- Implementation
- Testing
- Security review
- Performance optimization
- Documentation
- Deployment
```

**✅ Right Approach:**
```markdown
# Specialized Agent (clear boundaries)
You are a security specialist responsible for:
- Identifying vulnerabilities
- Recommending security fixes
- Validating authentication flows
- Reviewing access controls
```

### Pitfall 4: Context Overload

**❌ Wrong Approach:**
```javascript
// Loading everything upfront
const context = await loadAllContexts(); // 250KB loaded
```

**✅ Right Approach:**
```javascript
// Lazy loading based on task
const context = await loadContextForTask(taskType); // 10KB loaded
```

### Pitfall 5: Ignoring Error Recovery

**❌ Wrong Approach:**
```javascript
// No error handling
const result = await runAgent('complex-task');
return result; // What if it fails?
```

**✅ Right Approach:**
```javascript
// Graceful error handling with fallbacks
try {
  return await runAgent('complex-task');
} catch (error) {
  console.log(`Primary approach failed: ${error.message}`);
  return await runAgent('fallback-task');
}
```

## Performance Optimization

### Optimization Strategy 1: Minimize Context Loading

#### Before: Traditional Approach
```
Auto-loaded at startup: 250KB
├─ All agent definitions: 150KB
├─ All contexts: 80KB
├─ All commands: 20KB
└─ Result: Slow startup, memory waste
```

#### After: Optimized Approach
```
Auto-loaded at startup: 8KB
├─ Agent launcher only: 5KB
├─ Basic settings: 2KB
├─ Command shortcuts: 1KB
└─ Dynamic loading: On-demand from .claude-library/
```

### Optimization Strategy 2: Parallel Execution Patterns

#### Performance Comparison
| Task Count | Sequential Time | Parallel Time | Speedup |
|------------|----------------|---------------|---------|
| 3 agents | 90 seconds | 30 seconds | 3.0x |
| 5 agents | 150 seconds | 35 seconds | 4.3x |
| 10 agents | 300 seconds | 45 seconds | 6.7x |

#### Implementation Pattern
```javascript
// ✅ CORRECT: All tasks in single message
const parallelResults = [
  runTask({ /* Task 1 */ }),
  runTask({ /* Task 2 */ }),
  runTask({ /* Task 3 */ })
]; // All execute simultaneously

// ❌ WRONG: Sequential task spawning
await runTask({ /* Task 1 */ }); // Wait for completion
await runTask({ /* Task 2 */ }); // Then start task 2
await runTask({ /* Task 3 */ }); // Then start task 3
```

### Optimization Strategy 3: Smart Caching

#### Context Caching Implementation
```javascript
class ContextCache {
  constructor() {
    this.cache = new Map();
    this.accessCount = new Map();
    this.maxSize = 50; // Limit cache size
  }

  async get(contextName) {
    // Return cached if available
    if (this.cache.has(contextName)) {
      this.incrementAccess(contextName);
      return this.cache.get(contextName);
    }

    // Load and cache
    const context = await this.loadContext(contextName);
    this.set(contextName, context);
    return context;
  }

  set(name, context) {
    // Evict least used if cache full
    if (this.cache.size >= this.maxSize) {
      this.evictLeastUsed();
    }

    this.cache.set(name, context);
    this.accessCount.set(name, 1);
  }

  evictLeastUsed() {
    const leastUsed = Array.from(this.accessCount.entries())
      .sort((a, b) => a[1] - b[1])[0][0];

    this.cache.delete(leastUsed);
    this.accessCount.delete(leastUsed);
  }
}
```

### Optimization Strategy 4: Progressive Quality Gates

#### Optimized Quality Pipeline
```javascript
// Run fast, critical checks first
const fastGates = ['syntax', 'linting'];
const slowGates = ['security-scan', 'performance-test'];

// Parallel fast gates
const fastResults = await Promise.all(
  fastGates.map(gate => runQualityGate(gate, code))
);

// Early termination on critical failures
if (fastResults.some(r => r.critical && !r.passed)) {
  throw new QualityGateError('Critical fast gate failed');
}

// Only run slow gates if fast gates pass
const slowResults = await Promise.all(
  slowGates.map(gate => runQualityGate(gate, code))
);
```

## Real-World Examples

### Example 1: E-commerce Feature Development

**Scenario**: Build shopping cart functionality with payment integration.

#### Workflow Design
```javascript
// Stage 1: Parallel Analysis (30 seconds)
const analysis = await Promise.all([
  runTask({
    type: 'general-purpose',
    description: 'E-commerce architecture analysis',
    prompt: `[Load e-commerce architect agent]

    Design shopping cart system with:
    - State management (Redux/Zustand)
    - Payment integration (Stripe)
    - Inventory tracking
    - Price calculations
    - Tax handling`
  }),

  runTask({
    type: 'general-purpose',
    description: 'Security requirements analysis',
    prompt: `[Load security specialist agent]

    Analyze security requirements for:
    - Payment data handling (PCI compliance)
    - User authentication
    - Session management
    - Data encryption
    - Input validation`
  }),

  runTask({
    type: 'general-purpose',
    description: 'UX/UI requirements analysis',
    prompt: `[Load UX specialist agent]

    Design user experience for:
    - Cart interactions
    - Checkout flow
    - Payment forms
    - Error states
    - Mobile responsiveness`
  })
]);

// Stage 2: Parallel Implementation (45 seconds)
const implementation = await Promise.all([
  runTask({
    type: 'general-purpose',
    description: 'Frontend cart implementation',
    prompt: `[Load frontend engineer agent]

    Implement based on:
    ${analysis[0].result} // Architecture
    ${analysis[2].result} // UX requirements

    Create React components with:
    - Cart state management
    - Payment form integration
    - Real-time price updates
    - Responsive design`
  }),

  runTask({
    type: 'general-purpose',
    description: 'Backend API implementation',
    prompt: `[Load backend engineer agent]

    Implement based on:
    ${analysis[0].result} // Architecture
    ${analysis[1].result} // Security requirements

    Create API endpoints for:
    - Cart CRUD operations
    - Payment processing
    - Inventory updates
    - Order management`
  }),

  runTask({
    type: 'general-purpose',
    description: 'Security implementation',
    prompt: `[Load security engineer agent]

    Implement security measures:
    ${analysis[1].result} // Security requirements

    Focus on:
    - Input validation
    - Authentication middleware
    - Payment data encryption
    - Rate limiting`
  })
]);

// Stage 3: Integration & Testing (20 seconds)
const integration = await runTask({
  type: 'general-purpose',
  description: 'Integration and testing',
  prompt: `[Load integration specialist agent]

  Integration results:
  Frontend: ${implementation[0].result}
  Backend: ${implementation[1].result}
  Security: ${implementation[2].result}

  Tasks:
  - Integrate all components
  - Create end-to-end tests
  - Validate payment flow
  - Performance testing`
});
```

### Example 2: Production Bug Investigation

**Scenario**: API response times degraded from 200ms to 5 seconds.

#### Hierarchical Debugging Workflow
```javascript
// Orchestrator analyzes symptoms and coordinates specialists
const debugPlan = await runTask({
  type: 'general-purpose',
  description: 'Debug coordination and planning',
  prompt: `[Load debug orchestrator agent]

  Issue Analysis:
  - Symptom: API response time 200ms → 5s
  - Timeline: Started 3 hours ago
  - Scope: All endpoints affected
  - Environment: Production
  - Recent changes: None reported

  Create investigation plan and coordinate specialists.`
});

// Spawn parallel specialists based on orchestrator's plan
const specialists = await Promise.all([
  runTask({
    type: 'general-purpose',
    description: 'Database investigation',
    prompt: `[Load database specialist agent]

    Investigate database performance:
    - Query execution times
    - Lock contention
    - Connection pool status
    - Index effectiveness
    - Recent query patterns`
  }),

  runTask({
    type: 'general-purpose',
    description: 'Cache system investigation',
    prompt: `[Load cache specialist agent]

    Investigate caching layer:
    - Redis connection status
    - Cache hit/miss ratios
    - Memory usage patterns
    - Eviction rates
    - Network latency to cache`
  }),

  runTask({
    type: 'general-purpose',
    description: 'Application server investigation',
    prompt: `[Load application specialist agent]

    Investigate application layer:
    - CPU and memory usage
    - Thread pool status
    - GC performance
    - Request queue depth
    - Error rates and patterns`
  }),

  runTask({
    type: 'general-purpose',
    description: 'Network infrastructure investigation',
    prompt: `[Load network specialist agent]

    Investigate network performance:
    - DNS resolution times
    - Load balancer health
    - CDN status
    - Network latency
    - Bandwidth utilization`
  })
]);

// Synthesis and solution planning
const solution = await runTask({
  type: 'general-purpose',
  description: 'Root cause analysis and solution',
  prompt: `[Load solution architect agent]

  Investigation Results:
  Database: ${specialists[0].result}
  Cache: ${specialists[1].result}
  Application: ${specialists[2].result}
  Network: ${specialists[3].result}

  Provide:
  1. Root cause identification
  2. Immediate mitigation steps
  3. Long-term solution plan
  4. Prevention measures
  5. Monitoring improvements`
});
```

### Example 3: Legacy System Migration

**Scenario**: Migrate from monolithic PHP application to microservices architecture.

#### Multi-Phase Migration Workflow
```javascript
// Phase 1: Assessment and Planning
const assessment = await Promise.all([
  runTask({
    type: 'general-purpose',
    description: 'Legacy system analysis',
    prompt: `[Load legacy system analyst agent]

    Analyze existing PHP monolith:
    - Code structure and dependencies
    - Database schema complexity
    - Business logic identification
    - Performance bottlenecks
    - Technical debt assessment`
  }),

  runTask({
    type: 'general-purpose',
    description: 'Microservices architecture design',
    prompt: `[Load microservices architect agent]

    Design target architecture:
    - Service boundaries definition
    - Data consistency strategies
    - Communication patterns
    - Deployment strategies
    - Monitoring and observability`
  }),

  runTask({
    type: 'general-purpose',
    description: 'Risk assessment and mitigation',
    prompt: `[Load risk analyst agent]

    Assess migration risks:
    - Business continuity risks
    - Data integrity risks
    - Performance impact
    - Security considerations
    - Rollback strategies`
  })
]);

// Phase 2: Migration Strategy
const strategy = await runTask({
  type: 'general-purpose',
  description: 'Migration strategy planning',
  prompt: `[Load migration strategist agent]

  Based on assessment:
  Legacy Analysis: ${assessment[0].result}
  Target Architecture: ${assessment[1].result}
  Risk Assessment: ${assessment[2].result}

  Create detailed migration plan:
  - Service extraction order
  - Data migration strategies
  - Deployment sequence
  - Testing approaches
  - Success metrics`
});

// Phase 3: Parallel Implementation Streams
const implementation = await Promise.all([
  runTask({
    type: 'general-purpose',
    description: 'User service implementation',
    prompt: `[Load microservice engineer agent]

    Extract user management service:
    - Authentication service
    - User profile management
    - Session handling
    - API gateway integration`
  }),

  runTask({
    type: 'general-purpose',
    description: 'Product catalog service implementation',
    prompt: `[Load microservice engineer agent]

    Extract product catalog service:
    - Product data management
    - Search functionality
    - Inventory tracking
    - Category management`
  }),

  runTask({
    type: 'general-purpose',
    description: 'Order processing service implementation',
    prompt: `[Load microservice engineer agent]

    Extract order processing service:
    - Order lifecycle management
    - Payment integration
    - Shipping coordination
    - Order history`
  }),

  runTask({
    type: 'general-purpose',
    description: 'Data migration tooling',
    prompt: `[Load data engineer agent]

    Create migration tooling:
    - Data validation scripts
    - Migration verification
    - Rollback procedures
    - Sync mechanisms`
  })
]);
```

## Conclusion

This reference guide combines Anthropic's research-backed principles with practical Claude Agent Framework patterns. Key takeaways:

### Start With Workflows, Not Agents
- Most problems are solved better with structured workflows
- Only add agency when dynamic decision-making is truly needed
- Progressive complexity: prompt → workflow → agent

### Leverage Parallelization
- Claude Code's Task tool enables true parallel execution
- 3-6x speedup for independent tasks
- Critical: Send all parallel tasks in single message

### Design for Quality
- Implement progressive quality gates
- Build error recovery into workflows
- Plan for graceful degradation

### Optimize Performance
- Minimize auto-loaded context (< 10KB)
- Use lazy loading and smart caching
- Prefer specialized tools over general-purpose tools

### Focus on Maintainability
- Clear agent boundaries and responsibilities
- Comprehensive error handling
- Progressive complexity scaling

Remember: **Effective agents are built on effective workflows**. Master the workflow patterns first, then add sophistication as needed.

---

*Based on Anthropic's "Building Effective Agents" research and production patterns from the Claude Agent Framework*