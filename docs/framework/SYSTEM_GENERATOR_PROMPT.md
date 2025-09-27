# Claude Agent System Generator Prompt

## Master Prompt for Automatic Agent System Generation

Copy and paste this entire prompt into Claude to automatically generate a complete agent system for your project:

---

```markdown
# Generate Claude Agent System

You are an expert Claude Code agent system architect. Your task is to analyze the current project and generate a MINIMAL agent system that follows the "simplest approach first" principle.

## ⚠️ CRITICAL: Simplicity Circuit Breakers

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

## Step 1: Complexity Assessment (NEW - DO THIS FIRST!)

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

**If SIMPLE → Use MINIMAL configuration (7-9 files total)**
**If MEDIUM → Add 1-2 specialized agents MAX**
**If COMPLEX → Full system may be appropriate**

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

## Step 2: Reference Framework Documentation

Read the framework documentation located in `claude-agent-framework/`:
1. `CLAUDE_AGENT_FRAMEWORK.md` - Core principles and architecture
2. `AGENT_SYSTEM_TEMPLATE.md` - Quick start templates
3. `AGENT_PATTERNS.md` - Implementation patterns

## Step 3: Generate MINIMAL Agent System

### 3.1 Start with MINIMAL Structure

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
- Tests detected → Add test.md command
- Deployment config found → Add deploy.md
- Multiple debugging issues in code → Add debug.md
- Database with >5 tables → Add database-specialist.md
- >10 API endpoints → Add api-specialist.md

**DO NOT automatically create:**
- workflow-orchestrator (unless >5 parallel tasks)
- Multiple specialized agents
- Context files unless essential
- Tech-specific patterns unless dominant in codebase

### 3.2 Generate Agent Launcher

Create `.claude/agent-launcher.md` with:
- Project name from CLAUDE.md
- Detected tech stack
- Available commands based on project type
- Loading strategy for agents

### 3.3 Generate SIMPLE Core Agents

**SIMPLICITY CHECK: Before adding ANYTHING to agents:**
1. Is this feature actively used in the project? If no → DON'T ADD
2. Can existing tools handle this? If yes → DON'T ADD
3. Is this a "nice to have"? If yes → DON'T ADD

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

### 3.4 Generate Specialized Agents (ONLY IF JUSTIFIED)

**⚠️ CIRCUIT BREAKER: Specialized agents need STRONG justification**

Only create specialized agents if:
- Database: >5 tables OR complex queries observed
- API: >10 endpoints OR GraphQL/tRPC detected
- Frontend: >20 components OR complex state management
- AI/ML: Actual model training/inference code present
- Testing: >40% test coverage OR >20 test files

**If criteria NOT met → DO NOT CREATE**
**Start without them - add later if needed**

### 3.5 Generate Commands

Create commands based on project workflow:

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

### 3.6 Generate Contexts

Create context files with:
- Extracted project structure
- Detected patterns and conventions
- Environment variables found
- Common commands from package.json
- Database schemas if found

### 3.7 Generate Registry

Create `REGISTRY.json` with:
- All generated agents
- Appropriate triggers based on tech stack
- Tool configurations
- Command mappings
- Project-specific settings

## Step 4: Optimization

Apply these optimizations:
1. Keep `.claude/` folder under 10KB
2. Use lazy loading for all agents
3. Set up parallel execution where possible
4. Include only essential contexts
5. Cache frequently used agents

## Step 5: Validation

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

Claude: ✅ Agent system generated successfully!

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