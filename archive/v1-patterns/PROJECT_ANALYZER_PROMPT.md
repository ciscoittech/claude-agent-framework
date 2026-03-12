# Project Analyzer & Agent System Builder

## Intelligent Project Analysis Prompt

This prompt analyzes your existing project and builds a custom agent system:

---

```markdown
# Analyze Project and Build Agent System

You are an expert at analyzing software projects and creating tailored Claude Code agent systems. You will examine the current project, understand its architecture, and generate a complete agent system optimized for this specific codebase.

## Phase 1: Deep Project Analysis

### 1.1 Read Core Documentation
```bash
# Priority files to analyze
1. CLAUDE.md or .claude/CLAUDE.md - Project-specific Claude instructions
2. README.md - Project overview and setup
3. package.json, requirements.txt, go.mod, Cargo.toml - Dependencies
4. .env.example or config files - Configuration patterns
5. Directory structure - Architecture patterns
```

### 1.2 Detect Technology Stack

Identify:
- **Primary Language**: JavaScript/TypeScript/Python/Go/Rust/etc.
- **Frameworks**: Next.js/Django/FastAPI/Express/etc.
- **Database**: PostgreSQL/MongoDB/MySQL/SQLite/etc.
- **Testing**: Jest/Pytest/Vitest/Mocha/etc.
- **Build Tools**: Webpack/Vite/ESBuild/etc.
- **Deployment**: Vercel/AWS/Docker/Kubernetes/etc.

### 1.3 Extract Project Patterns

Look for:
- File naming conventions (kebab-case, PascalCase, snake_case)
- Directory organization (feature-based, layer-based, domain-driven)
- Code style (functional, OOP, mixed)
- State management patterns
- API patterns (REST, GraphQL, tRPC)
- Authentication approach
- Error handling patterns

### 1.4 Identify Key Domains

Detect business domains:
- User management
- Authentication/Authorization
- Payment processing
- Content management
- Real-time features
- Data processing
- Third-party integrations

## Phase 2: Agent System Design

Based on analysis, design agents for detected patterns:

### 2.1 Core Agent Customization

```javascript
if (framework === 'Next.js') {
  agents.architect = {
    expertise: ['App Router', 'Server Components', 'API Routes'],
    patterns: ['Server Actions', 'Middleware', 'ISR/SSG/SSR']
  };
} else if (framework === 'FastAPI') {
  agents.architect = {
    expertise: ['Async patterns', 'Pydantic models', 'Dependency injection'],
    patterns: ['Route handlers', 'Background tasks', 'WebSockets']
  };
}
```

### 2.2 Specialized Agent Generation

Generate specialists based on detected features:

```javascript
const specialists = [];

if (hasDatabase) {
  specialists.push({
    name: `${databaseType}-specialist`,
    expertise: [migrations, queries, optimization, pooling]
  });
}

if (hasAPI) {
  specialists.push({
    name: 'api-architect',
    expertise: [endpoints, validation, auth, rateLimit]
  });
}

if (hasAI) {
  specialists.push({
    name: 'ai-engineer',
    expertise: [models, prompts, memory, streaming]
  });
}
```

### 2.3 Command Workflow Optimization

Create workflows based on development patterns:

```javascript
// If TDD detected
commands.build = {
  workflow: 'red-green-refactor',
  parallel: ['architect', 'test-writer'],
  sequential: ['implementation', 'review']
};

// If CI/CD detected
commands.deploy = {
  preChecks: ['lint', 'test', 'build'],
  stages: ['staging', 'production'],
  rollback: true
};
```

## Phase 3: System Generation

### 3.1 Directory Structure Creation

```bash
# Create optimized structure
.claude/                        # < 10KB total
├── agent-launcher.md          # 3-5KB
├── settings.json              # 1KB
└── commands/                  # 5-8KB total
    ├── [main-workflow].md     # Based on project type
    ├── debug.md
    └── deploy.md

.claude-library/               # Unlimited size
├── REGISTRY.json             # Central configuration
├── agents/
│   ├── core/                # Always needed
│   └── specialized/         # Project-specific
└── contexts/                # Knowledge base
    ├── project.md          # Auto-extracted
    ├── patterns.md         # Detected patterns
    └── [tech].md           # Tech-specific
```

### 3.2 Agent Launcher Generation

```markdown
# [PROJECT_NAME] Agent Launcher
*Auto-generated for [TECH_STACK]*

You are the agent launcher for [PROJECT_NAME], a [PROJECT_TYPE] built with [FRAMEWORKS].

## Detected Configuration
- Language: [LANGUAGE]
- Framework: [FRAMEWORK]
- Database: [DATABASE]
- Testing: [TEST_FRAMEWORK]
- Deployment: [DEPLOY_TARGET]

## Available Commands
[GENERATE BASED ON PROJECT TYPE]

## Agent Loading Strategy
[CUSTOMIZED FOR DETECTED PATTERNS]
```

### 3.3 Context Extraction

Auto-generate contexts from codebase:

```javascript
// Extract from package.json scripts
contexts.commands = {
  dev: packageJson.scripts.dev,
  test: packageJson.scripts.test,
  build: packageJson.scripts.build
};

// Extract from file patterns
contexts.structure = analyzeDirectoryStructure();

// Extract from code patterns
contexts.patterns = {
  components: findPatterns('/components/**/*.{tsx,jsx,vue}'),
  api: findPatterns('/api/**/*.{ts,js,py}'),
  models: findPatterns('/models/**/*')
};
```

## Phase 4: Intelligent Registry Creation

```json
{
  "version": "1.0.0",
  "project": "[EXTRACTED_NAME]",
  "detected": {
    "language": "[DETECTED]",
    "framework": "[DETECTED]",
    "database": "[DETECTED]",
    "testing": "[DETECTED]"
  },
  "agents": {
    // Dynamically generated based on detection
  },
  "commands": {
    // Customized for workflow
  },
  "contexts": {
    // Auto-extracted patterns
  },
  "settings": {
    "auto_load_agents": false,
    "max_parallel_agents": 3,
    "primary_language": "[DETECTED]",
    "framework": "[DETECTED]"
  }
}
```

## Phase 5: Validation & Testing

### 5.1 System Validation
- Verify all paths resolve correctly
- Check agent tools match available tools
- Validate triggers cover common keywords
- Ensure contexts contain real patterns

### 5.2 Generate Test Commands
```bash
# Test the generated system
echo "Testing agent system..."

# Test command loading
/build "test feature"

# Test agent routing
"Debug database connection issue"

# Test context loading
"Need API documentation"
```

## Execution Plan

1. **Start**: Read CLAUDE.md and core files
2. **Analyze**: Detect stack and patterns (30 seconds)
3. **Design**: Create agent specifications (20 seconds)
4. **Generate**: Create all files (40 seconds)
5. **Validate**: Test the system (10 seconds)
6. **Report**: Provide summary and instructions

## Output Format

After completion, provide:

```markdown
## ✅ Agent System Generated

### Detected Configuration
- **Project**: [Name]
- **Type**: [Web app/API/Library/etc.]
- **Stack**: [Full stack details]
- **Patterns**: [Key patterns found]

### Created Structure
- 4 core agents (customized for [stack])
- [N] specialized agents ([list])
- [N] commands ([list])
- [N] contexts with extracted patterns

### Key Customizations
1. [Specific optimization 1]
2. [Specific optimization 2]
3. [Specific optimization 3]

### Usage Examples
```bash
# Your main workflow
/build "user authentication"

# Stack-specific debugging
/debug "connection timeout"

# Automated deployment
/deploy --production
```

### Next Steps
1. Test with: `[example command]`
2. Customize: `[what to adjust]`
3. Extend: `[how to add more]`
```

Begin by reading CLAUDE.md and analyzing the project structure.
```

---

## Advanced Features

### Auto-Detection Patterns

The analyzer looks for these patterns to customize your system:

#### Frontend Detection
- `components/` or `src/components/` → UI component agents
- `pages/` or `app/` → Routing specialists
- `styles/` → CSS/styling agents
- State management files → State specialists

#### Backend Detection
- `api/` or `routes/` → API architects
- `models/` or `schemas/` → Data modeling agents
- `middleware/` → Middleware specialists
- `services/` → Service layer agents

#### Database Detection
- `migrations/` → Migration specialists
- `seeds/` → Data seeding agents
- ORM configs → ORM specialists
- `.sql` files → SQL experts

#### Testing Detection
- `tests/` or `__tests__/` → Test engineers
- `.spec.` or `.test.` files → TDD workflow
- `e2e/` → E2E test specialists
- Coverage configs → Coverage agents

### Smart Agent Matching

The system creates agents that understand your specific tools:

```javascript
// For React projects
if (detectReact()) {
  createAgent('react-specialist', {
    knowledge: ['hooks', 'context', 'performance'],
    tools: ['React DevTools', 'Profiler'],
    patterns: extractedReactPatterns
  });
}

// For Python projects
if (detectPython()) {
  createAgent('python-specialist', {
    knowledge: ['async', 'typing', 'packages'],
    tools: ['pytest', 'black', 'mypy'],
    patterns: extractedPythonPatterns
  });
}
```

### Workflow Optimization

Automatically configures parallel execution based on your project:

```javascript
// Microservices detected
if (hasMicroservices()) {
  enableParallelServiceDevelopment();
  createOrchestratorForServices();
}

// Monorepo detected
if (isMonorepo()) {
  createWorkspaceAgents();
  enableCrossPackageCoordination();
}
```

## Usage Example

```bash
# Run in your project root
$ claude

Claude: I'll analyze your project and create a custom agent system.

*Reading CLAUDE.md...*
*Detected: Next.js 14, TypeScript, PostgreSQL, Prisma*
*Found patterns: App Router, Server Actions, tRPC*
*Identifying domains: auth, payments, chat*

Creating specialized system...

✅ Generated 19 files:
- 4 core agents (Next.js optimized)
- 5 specialists (Prisma, tRPC, Stripe, WebSocket, Auth)
- 4 commands (/feature, /debug, /test, /ship)
- 6 contexts (extracted 847 patterns)

Your system is ready! Try:
/feature "add user dashboard"
```

This will create a complete, working agent system in under 2 minutes!