# Agent Launcher Skill - Reference Documentation

## Technical Architecture

### Agent Registry Structure

The Agent Launcher reads from `.claude-library/REGISTRY.json`:

```json
{
  "agents": {
    "code-specialist": {
      "id": "code-specialist",
      "name": "Code Specialist",
      "description": "Complex code generation and refactoring",
      "complexity": "high",
      "min_tokens": 8000,
      "recommended_tokens": 12000,
      "model": "claude-3-5-sonnet-20241022",
      "capabilities": ["coding", "architecture", "optimization"],
      "tools": ["code_execution", "file_system", "git"],
      "contexts": ["codebase", "requirements"]
    },
    "documentation-expert": {
      "id": "documentation-expert",
      "name": "Documentation Expert",
      "description": "User guides and API documentation",
      "complexity": "medium",
      "min_tokens": 6000,
      "recommended_tokens": 10000,
      "model": "claude-3-5-sonnet-20241022",
      "capabilities": ["documentation", "examples", "formatting"],
      "tools": ["file_generation", "markdown_processing"],
      "contexts": ["api_spec", "code_examples"]
    },
    "test-generator": {
      "id": "test-generator",
      "name": "Test Generator",
      "description": "Comprehensive test suites and strategies",
      "complexity": "medium",
      "min_tokens": 6000,
      "recommended_tokens": 9000,
      "model": "claude-3-5-sonnet-20241022",
      "capabilities": ["testing", "coverage", "mocking"],
      "tools": ["test_framework", "code_execution"],
      "contexts": ["code", "requirements"]
    },
    "project-analyzer": {
      "id": "project-analyzer",
      "name": "Project Analyzer",
      "description": "Codebase analysis and architecture review",
      "complexity": "high",
      "min_tokens": 10000,
      "recommended_tokens": 14000,
      "model": "claude-3-5-sonnet-20241022",
      "capabilities": ["analysis", "patterns", "architecture"],
      "tools": ["codebase_search", "file_system"],
      "contexts": ["codebase", "architecture_docs"]
    },
    "generalist": {
      "id": "generalist",
      "name": "Generalist Agent",
      "description": "Simple tasks and quick implementations",
      "complexity": "low",
      "min_tokens": 2000,
      "recommended_tokens": 4000,
      "model": "claude-3-5-haiku-20241022",
      "capabilities": ["general", "quick_tasks", "debugging"],
      "tools": ["basic_file_ops", "simple_execution"],
      "contexts": ["general"]
    }
  }
}
```

### Agent Selection Algorithm

```python
def select_agent(task_description: str) -> Agent:
    """
    Analyzes task and returns most appropriate agent

    Algorithm:
    1. Extract complexity indicators from description
       - Lines of code: <100 = simple, 100-500 = medium, >500 = hard
       - Keywords: "complex", "refactor", "optimize" = higher complexity
       - Estimated duration

    2. Identify task type
       - Code keywords: implement, fix, refactor, optimize → Code Specialist
       - Doc keywords: document, guide, tutorial, explain → Documentation Expert
       - Test keywords: test, coverage, mock, fixture → Test Generator
       - Analysis keywords: analyze, review, pattern, structure → Project Analyzer
       - Default: Generalist

    3. Match against agent capabilities
       - Verify agent has required tools
       - Check token budget against task complexity
       - Confirm agent complexity matches task

    4. Return selected agent with optimized config
    """
    pass
```

### Configuration Parameters

#### Model Selection
```
complexity: simple → claude-3-5-haiku-20241022
complexity: medium → claude-3-5-sonnet-20241022
complexity: hard → claude-3-5-opus-20250514
```

#### Token Allocation
```
Base tokens: Agent's min_tokens
+ Task overhead: 1000-2000
+ Context: 2000-8000 (depending on files needed)
+ Buffer: 20% headroom

Example:
  Code Specialist + Medium task = 12000 recommended
  + 1500 overhead + 4000 context + 20% = ~21K total budget
```

#### Tool Permissions
```yaml
code_execution:
  - python_version: "3.10+"
  - packages: "pre-installed only"
  - sandbox: "filesystem isolated"

file_system:
  - read: "all project files"
  - write: "generated files only"
  - delete: "disabled"

git:
  - status: "enabled"
  - diff: "enabled"
  - commit: "requires confirmation"
```

## Agent-Specific Configurations

### Code Specialist Configuration

```json
{
  "agent_id": "code-specialist",
  "system_prompt": "You are an expert code specialist...",
  "temperature": 0.2,
  "tools": {
    "code_execution": {"timeout": 30, "memory": "2GB"},
    "file_system": {"patterns": ["*.py", "*.ts", "*.js"]},
    "git": {"allowed": ["status", "diff", "log"]}
  },
  "context_files": [
    "package.json",
    ".claude/settings.json",
    "README.md"
  ]
}
```

### Documentation Expert Configuration

```json
{
  "agent_id": "documentation-expert",
  "system_prompt": "You are an expert documentation specialist...",
  "temperature": 0.5,
  "tools": {
    "markdown_processor": {"flavor": "github"},
    "file_generation": {"formats": ["md", "pdf", "html"]}
  },
  "context_files": [
    "README.md",
    "docs/",
    "src/"
  ]
}
```

### Test Generator Configuration

```json
{
  "agent_id": "test-generator",
  "system_prompt": "You are an expert test automation specialist...",
  "temperature": 0.3,
  "tools": {
    "test_framework": {"frameworks": ["pytest", "jest", "unittest"]},
    "code_execution": {"timeout": 45}
  },
  "context_files": [
    "src/",
    "tests/",
    "package.json"
  ]
}
```

## Complexity Analysis

### Complexity Scoring

```python
def calculate_complexity_score(task: Task) -> int:
    """
    Returns 0-100 complexity score

    Factors:
    - LOC to modify: <100 = +10, 100-500 = +25, >500 = +40
    - File count: <5 = +0, 5-20 = +15, >20 = +30
    - Dependencies: local = +0, external = +20, network = +40
    - Estimated time: <1h = +0, 1-4h = +20, >4h = +40
    - Required expertise: basic = +0, intermediate = +15, advanced = +30
    """
    pass

# Complexity ranges:
# 0-30: Simple (Generalist, Haiku)
# 31-70: Medium (Code/Doc/Test Specialist, Sonnet)
# 71-100: Hard (Project Analyzer, Opus)
```

## Task Routing Examples

### Example 1: Code Implementation
```
Input: "Add OAuth2 authentication to our REST API"

Analysis:
  - Keywords: OAuth2, authentication, REST API (code-related)
  - Estimated LOC: 200-400
  - Complexity score: 45 (medium)
  - Required expertise: intermediate
  - Token estimate: 10000-12000

Routing Decision:
  Agent: Code Specialist
  Model: Sonnet
  Tokens: 12000
  Tools: code_execution, file_system, git
```

### Example 2: Bug Fix
```
Input: "Fix the race condition in the payment processor"

Analysis:
  - Keywords: race condition, bug fix
  - Complexity score: 35 (medium)
  - Estimated LOC: 50-100
  - Required expertise: intermediate

Routing Decision:
  Agent: Code Specialist (or Generalist if simple)
  Model: Sonnet
  Tokens: 8000
```

### Example 3: Simple Task
```
Input: "Update the version number to 2.0.0"

Analysis:
  - Keywords: update, simple
  - Complexity score: 5 (simple)
  - Estimated LOC: 5
  - Execution time: 1 minute

Routing Decision:
  Agent: Generalist
  Model: Haiku
  Tokens: 2000
```

## Performance Optimization

### Context Efficiency
- Uses progressive disclosure: load only needed files
- Caches common analysis results
- Reuses agent configs across similar tasks

### Token Optimization
```
Overhead: ~500 tokens (selection + config)
Context: Varies by task (2K-8K)
Execution: Varies by complexity

Total: Min 2.5K (simple) → 25K+ (complex)
```

### Caching Strategy
```
Cache these for reuse:
- Agent configs (never changes unless updated)
- Project structure analysis (refreshed daily)
- Language/framework detection (per project)

Don't cache (changes per execution):
- Task context
- User requirements
- Execution results
```

## Error Handling

### Invalid Task Description
```
Condition: Task description too vague
Resolution: Request clarification with specific questions
Fallback: Route to Generalist with lower confidence
```

### Insufficient Resources
```
Condition: Token budget insufficient for task
Resolution: Break task into smaller steps
Fallback: Recommend reducing scope or using staged execution
```

### Agent Unavailable
```
Condition: Selected agent not configured
Resolution: Fall back to next best agent
Fallback: Return error with available agents
```

## Metrics & Monitoring

### Track Per Execution
- Agent selected
- Token usage (actual vs estimated)
- Execution duration
- Success/failure status
- Cost estimate

### Aggregate Metrics
```
Sample output:
{
  "execution_id": "exec_12345",
  "agent": "code-specialist",
  "task": "Implement OAuth2",
  "status": "completed",
  "duration_seconds": 450,
  "tokens_used": 9876,
  "tokens_estimated": 10000,
  "cost_estimate": "$0.15",
  "quality_score": 0.92
}
```

## Integration Points

### With Framework Systems

#### SYSTEM_GENERATOR_PROMPT
- Uses generated agent configs
- Respects complexity limits
- Follows framework conventions

#### Simplicity Enforcement
- Respects circuit breaker settings
- Won't escalate complexity unnecessarily
- Routes simple tasks to Generalist first

#### Agent Patterns
- Follows established patterns
- Uses pattern-specific configs
- Returns results in pattern-compatible format

## Troubleshooting Guide

### Agent Selection Wrong
**Check**:
1. Task description clarity
2. Keywords in description
3. Agent capabilities match

**Fix**:
- Rephrase task with explicit agent type
- Add specific technical context
- Specify preferred agent directly

### Tokens Exhausted
**Check**:
1. Token estimate accuracy
2. Task scope creep
3. Context size

**Fix**:
- Break into smaller tasks
- Reduce context files
- Use staged execution

### Performance Issues
**Check**:
1. File system access speed
2. Git operations overhead
3. Code execution time

**Fix**:
- Cache project analysis
- Optimize context loading
- Use parallel execution

---

For implementation details and code examples, see the skills repository examples.
