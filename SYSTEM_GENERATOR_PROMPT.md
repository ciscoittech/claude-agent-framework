# Claude Agent System Generator Prompt

## Master Prompt for Automatic Agent System Generation

Copy and paste this entire prompt into Claude to automatically generate a complete agent system for your project:

---

```markdown
# Generate Claude Agent System

You are an expert Claude Code agent system architect. Your task is to analyze the current project and generate a MINIMAL agent system that follows the "simplest approach first" principle.

## CRITICAL: Simplicity Circuit Breakers

Before generating ANYTHING, follow these rules:
1. **Start with 3 core agents ONLY** (architect, engineer, reviewer)
2. **Maximum 4 commands initially** (build only, unless project shows need for others)
3. **NO specialized agents** unless explicitly detected and justified
4. **Sequential workflows by default** (parallel only if >3 independent tasks)
5. **Target <5KB total generation** for simple projects

## Your Mission

1. **Assess Complexity** - Determine if project even needs agents
2. **Start Minimal** - Begin with simplest possible setup
3. **Justify Additions** - Only add complexity when proven necessary
4. **Follow Simplicity** - Try simple approaches before complex ones

## Phase 0: Deep Project Analysis (For Medium/Complex Projects)

Before assessing complexity, perform a thorough analysis of the project.
Skip this phase for obviously simple projects (<500 lines, single file, etc.).

### 0.1 Read Core Documentation

Priority files to analyze (in order):
1. `CLAUDE.md` or `.claude/CLAUDE.md` - Project-specific Claude instructions
2. `README.md` - Project overview and setup instructions
3. `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml` - Dependencies and scripts
4. `.env.example` or config files - Configuration patterns and environment variables
5. Directory structure - Architecture patterns and organization

Read each file that exists and extract:
- Project name, purpose, and current status
- Development workflow and conventions
- Known pain points or areas of complexity
- Team preferences and constraints

### 0.2 Detect Technology Stack

Identify each layer of the stack:
- **Primary Language**: JavaScript/TypeScript/Python/Go/Rust/Java/etc.
- **Frameworks**: Next.js/Django/FastAPI/Express/Rails/Spring/etc.
- **Database**: PostgreSQL/MongoDB/MySQL/SQLite/Redis/etc.
- **Testing**: Jest/Pytest/Vitest/Mocha/Go test/etc.
- **Build Tools**: Webpack/Vite/ESBuild/Turbopack/Make/etc.
- **Deployment**: Vercel/AWS/Docker/Kubernetes/Fly.io/etc.

Record the primary technology for each layer. Ignore minor utilities and dev-only tools
unless they significantly affect the development workflow.

### 0.3 Extract Project Patterns

Scan the codebase for established conventions:
- **File naming**: kebab-case, PascalCase, snake_case, or mixed
- **Directory organization**: feature-based, layer-based, domain-driven, or flat
- **Code style**: functional, OOP, mixed, or framework-idiomatic
- **State management**: Redux, Zustand, Context, Pinia, signals, etc.
- **API patterns**: REST, GraphQL, tRPC, gRPC, WebSocket
- **Authentication**: JWT, session-based, OAuth, API keys
- **Error handling**: try/catch patterns, Result types, error boundaries

Only record patterns that are actually present in the code. Do not assume
patterns based on the framework alone.

### 0.4 Identify Key Domains

Detect business domains present in the codebase:
- **User management**: user models, profiles, preferences
- **Authentication/Authorization**: login, roles, permissions
- **Payment processing**: Stripe, PayPal, billing logic
- **Content management**: CMS, editors, media handling
- **Real-time features**: WebSockets, SSE, polling
- **Data processing**: ETL, pipelines, batch jobs
- **Third-party integrations**: external APIs, webhooks, SDKs

Each detected domain may justify a specialized agent (but only if
the domain is substantial enough -- see complexity thresholds in Step 1).

### 0.5 Smart Agent Matching

Use these auto-detection rules to map project structure to potential agents:

**Frontend Detection:**
- `components/` or `src/components/` -> UI component agents
- `pages/` or `app/` -> Routing specialists
- `styles/` or CSS-in-JS patterns -> Styling agents
- State management files -> State specialists

**Backend Detection:**
- `api/` or `routes/` -> API architects
- `models/` or `schemas/` -> Data modeling agents
- `middleware/` -> Middleware specialists
- `services/` -> Service layer agents

**Database Detection:**
- `migrations/` -> Migration specialists
- `seeds/` or `fixtures/` -> Data seeding agents
- ORM config files -> ORM specialists
- `.sql` files -> SQL experts

**Testing Detection:**
- `tests/` or `__tests__/` -> Test engineers
- `.spec.` or `.test.` files -> TDD workflow
- `e2e/` or `cypress/` or `playwright/` -> E2E test specialists
- Coverage config files -> Coverage agents

**Important**: Detection alone does not justify creating a specialist.
The directory must contain enough substance to warrant one (see thresholds in Step 1).

## Step 1: Complexity Assessment (DO THIS FIRST!)

### Determine Project Complexity Level

**SIMPLE (Use minimal setup):**
- < 1000 lines of code
- Single language/framework
- No database or simple SQLite
- Basic CRUD operations
- No complex integrations

**MEDIUM (Add some specialization):**
- 1000-10,000 lines of code
- 2-3 integrated technologies
- Database with <10 tables
- Some API endpoints
- Standard testing setup

**COMPLEX (Full agent system justified):**
- > 10,000 lines of code
- Multiple services/microservices
- Complex database relationships
- Many API endpoints
- CI/CD pipelines

**If SIMPLE -> Use MINIMAL configuration (7-9 files total)**
**If MEDIUM -> Add 1-2 specialized agents MAX**
**If COMPLEX -> Full system may be appropriate**

## Step 2: Project Analysis

After complexity assessment, analyze:
- `CLAUDE.md` (if exists) - Project documentation
- `README.md` - Project overview
- `package.json` or equivalent - Tech stack identification
- Directory structure - Architecture patterns

Extract ONLY what's essential:
- Project name and description
- Core technology (ignore minor dependencies)
- Actual patterns in use (not potential patterns)
- Features that exist (not planned features)

## Step 3: Reference Framework Documentation

Read the framework documentation located in `claude-agent-framework/`:
1. `SIMPLICITY_ENFORCEMENT.md` - Circuit breakers against over-engineering (read first)
2. `CLAUDE_AGENT_FRAMEWORK.md` - Core principles and architecture
3. `AGENT_SYSTEM_TEMPLATE.md` - Quick start templates
4. `AGENT_PATTERNS.md` - Implementation patterns (use sparingly)

## Step 4: Generate MINIMAL Agent System

### 4.1 Start with MINIMAL Structure

**FOR SIMPLE PROJECTS (DEFAULT):**
```bash
.claude/
├── agent-launcher.md     # Minimal launcher (1KB max)
├── settings.json         # Basic metadata (0.5KB max)
└── commands/
    └── build.md         # ONLY build command initially

.claude-library/
├── REGISTRY.json        # Minimal registry (2KB max)
└── agents/
    └── core/           # ONLY 3 core agents
        ├── architect.md    # Simple architect
        ├── engineer.md     # Simple engineer
        └── reviewer.md     # Simple reviewer
```

**ONLY ADD MORE IF:**
- Tests detected -> Add test.md command
- Deployment config found -> Add deploy.md
- Multiple debugging issues in code -> Add debug.md
- Database with >5 tables -> Add database-specialist.md
- >10 API endpoints -> Add api-specialist.md

**DO NOT automatically create:**
- workflow-orchestrator (unless >5 parallel tasks)
- Multiple specialized agents
- Context files unless essential
- Tech-specific patterns unless dominant in codebase

### 4.2 Generate Agent Launcher

Create `.claude/agent-launcher.md` with:
- Project name from CLAUDE.md
- Detected tech stack
- Available commands based on project type
- Loading strategy for agents

### 4.3 Generate SIMPLE Core Agents

**SIMPLICITY CHECK: Before adding ANYTHING to agents:**
1. Is this feature actively used in the project? If no -> DON'T ADD
2. Can existing tools handle this? If yes -> DON'T ADD
3. Is this a "nice to have"? If yes -> DON'T ADD

**Minimal Architect Agent:**
- ONLY include the primary framework detected
- ONLY add database patterns if database exists
- Keep under 2KB total

**Minimal Engineer Agent:**
- ONLY include the main language patterns
- ONLY add test patterns if tests exist
- Keep under 2KB total

**Minimal Reviewer Agent:**
- Basic code quality checks only
- Security only if auth/payment code exists
- Keep under 2KB total

**DO NOT add "just in case" features**
**DO NOT anticipate future needs**
**DO NOT include patterns not seen in actual code**

### 4.4 Generate Specialized Agents (ONLY IF JUSTIFIED)

**CIRCUIT BREAKER: Specialized agents need STRONG justification**

Only create specialized agents if:
- Database: >5 tables OR complex queries observed
- API: >10 endpoints OR GraphQL/tRPC detected
- Frontend: >20 components OR complex state management
- AI/ML: Actual model training/inference code present
- Testing: >40% test coverage OR >20 test files

**If criteria NOT met -> DO NOT CREATE**
**Start without them - add later if needed**

### 4.5 Generate Commands

Commands are `.claude/commands/*.md` files invoked via `/command-name` or the Skill tool.
They are Claude Code's native skill mechanism — no custom runtime needed.

#### Workflow Commands (project-specific)

**For `/build` command:**
- Use TDD if tests detected
- Include parallel architecture + implementation
- Add review stage
- Include tech-specific build steps

**For `/debug` command:**
- Include stack-specific debugging
- Add error patterns from project
- Include logging analysis

**For `/test` command:**
- Include detected test frameworks
- Add coverage requirements
- Include test patterns

#### Utility Commands (recommended for all projects)

**For `/launch-agent` command:**
- Classify task → select agent type + model
- Simple tasks → haiku, medium → sonnet, complex → opus
- Route to custom subagent types in `.claude/agents/` if they exist
- Fallback to general-purpose agent

**For `/review-code` command:**
- Review uncommitted, staged, or PR changes
- Check correctness, security (OWASP), quality, performance
- Report with severity levels: Critical / Warning / Suggestion
- Offer to fix issues after review

**For `/generate-docs` command (medium+ projects):**
- Types: api, readme, architecture, guide, changelog
- Analyze code to generate accurate documentation
- Follow project's existing doc style

### 4.6 Generate Contexts

Create context files with:
- Extracted project structure
- Detected patterns and conventions
- Environment variables found
- Common commands from package.json
- Database schemas if found

### 4.7 Generate Registry

Create `REGISTRY.json` with:
- All generated agents
- Appropriate triggers based on tech stack
- Tool configurations
- Command mappings
- Project-specific settings

## Step 5: Optimization

Apply these optimizations:
1. Keep `.claude/` folder under 10KB
2. Use lazy loading for all agents
3. Set up parallel execution where possible
4. Include only essential contexts
5. Cache frequently used agents

## Step 6: Validation

After generation:
1. Verify all file paths are correct
2. Check agent tool permissions
3. Validate command workflows
4. Test registry triggers
5. Ensure contexts are project-specific

## Implementation Instructions

Execute this plan:
1. Read CLAUDE.md and project files
2. Generate all files according to the framework
3. Customize for detected technology stack
4. Report what was created and why
5. Provide usage instructions

## Expected Output

**FOR SIMPLE PROJECTS (DEFAULT):**
- 7-9 files total (NOT 15-20!)
- Minimal functional system
- ONLY essential customizations
- Single build command to start
- Brief documentation

**FOR MEDIUM PROJECTS:**
- 10-12 files maximum
- Core + 1-2 specialists
- 2-3 commands
- Targeted customizations

**FOR COMPLEX PROJECTS:**
- 15-20 files (only if justified)
- Full agent system
- Multiple commands
- Comprehensive documentation

**Remember: It's easier to add later than to remove**

Start by reading CLAUDE.md and analyzing the project structure.
```

---

## Appendix: Best Practice Integration

This section describes how to continuously improve the framework by ingesting
and validating best practices from Anthropic documentation and other sources.

### Integration Workflow

The integration process follows four stages:

1. **Ingest**: Fetch and extract principles from Anthropic docs or other best practice sources
2. **Analyze**: Compare extracted principles against the current framework to identify gaps
3. **Test**: Validate proposed improvements with concrete, measurable metrics
4. **Integrate**: Merge approved changes into the framework after passing all checks

### Integration Criteria

Each proposed change is evaluated against three thresholds:

**APPROVED:**
- Pass rate >= 90%
- Average improvement >= 10%
- Simplicity maintained (no unnecessary bloat added)
- Action: Merge to main framework

**REVIEW:**
- Pass rate 70-89%
- Improvement 5-9%
- Minor simplicity concerns that need discussion
- Action: Refine the approach and re-test

**REJECTED:**
- Pass rate < 70%
- Improvement < 5%
- Violates the simplicity-first principle
- Action: Archive with documentation explaining why

### Available Commands

**`/ingest-best-practice <URL>`**
Fetches and analyzes a new best practice document. Outputs:
- Context document with extracted principles
- Gap analysis comparing principles to current framework
- Summary report with prioritized action items

Example:
```bash
/ingest-best-practice https://www.anthropic.com/engineering/writing-tools-for-agents
```

**`/validate-framework <name>`**
Runs validation tests for a specific best practice integration. Outputs:
- Test results with pass rate and per-metric scores
- Before/after comparison showing concrete improvements
- Simplicity compliance check
- Final verdict: APPROVED / REVIEW / REJECTED

Example:
```bash
/validate-framework tool-writing
```

### Integration File Structure

After running the integration workflow, files are organized as:
```
.claude-library/
├── contexts/anthropic-best-practices/
│   └── <best-practice-name>.md          # Extracted principles
├── experiments/
│   └── <best-practice-name>/
│       ├── gap-analysis.md              # Detailed comparison
│       ├── baseline/                    # Original files
│       ├── improved/                    # Enhanced files
│       └── test-results/               # Validation reports
└── agents/specialized/
    ├── best-practice-analyzer.md        # Ingestion agent
    └── framework-gap-analyzer.md        # Analysis agent

.claude/commands/
├── ingest-best-practice.md              # Ingestion workflow
└── validate-framework.md               # Validation workflow
```

### Tips for Best Practice Integration

- Start with quick wins: high impact, low effort changes
- Run tests frequently to catch regressions early
- Keep simplicity as the top priority at all times
- Document why each change was made or rejected
- Archive experiment data after integration is complete

---

## How to Use This Prompt

1. **Ensure the framework documentation exists** in `claude-agent-framework/` folder
2. **Copy the entire prompt** above (everything between the triple backticks)
3. **Paste into Claude Code** in your project directory
4. **Claude will automatically**:
   - Analyze your project
   - Read existing CLAUDE.md
   - Generate a complete agent system
   - Customize it for your tech stack
   - Create all necessary files

## What Gets Generated

The system will create:

### Core Structure
- `.claude/` folder with minimal auto-loaded config
- `.claude-library/` with all agents and contexts
- Project-specific agents based on your stack
- Commands tailored to your workflow

### Customized Agents
- Architects that understand your frameworks
- Engineers that follow your conventions
- Reviewers that check your specific requirements
- Specialists for your domains (API, database, UI, etc.)

### Smart Commands
- `/build` - Adapted to your development workflow
- `/debug` - Stack-specific debugging
- `/test` - Using your test frameworks
- `/deploy` - For your deployment targets

### Project Contexts
- Extracted patterns from your codebase
- Your file structure and conventions
- Your environment variables
- Your common commands

## Example Usage

```bash
# In your project directory
$ claude

Claude: I'll analyze your project and generate a complete agent system.

*Reads CLAUDE.md*
*Analyzes package.json*
*Detects Next.js, PostgreSQL, Jest*
*Generates 18 files*

Claude: Agent system generated successfully!

Created:
- 4 core agents (customized for Next.js)
- 3 specialized agents (API, Database, UI)
- 4 commands (/build, /debug, /test, /deploy)
- 3 contexts with your patterns
- Complete registry and launcher

You can now use:
- `/build "user authentication"` - Full TDD development
- `/debug "hydration error"` - Next.js debugging
- `/test` - Run your Jest tests
- `/deploy --vercel` - Deploy to Vercel

The system is optimized for your stack with parallel execution enabled.
```

## Tips for Best Results

1. **Have a CLAUDE.md file** with project details
2. **Include README.md** with project overview
3. **Have package.json** or equivalent for tech stack detection
4. **Keep consistent** file structure
5. **Document** any special patterns or conventions

## Customization After Generation

After the system is generated, you can:
- Add more specialized agents
- Create custom commands
- Extend contexts with patterns
- Adjust registry triggers
- Fine-tune agent responsibilities

The generated system is a starting point - customize it as your project evolves!
