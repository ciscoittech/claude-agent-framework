# Claude Agent System Generator Prompt

## Master Prompt for Automatic Agent System Generation

Copy and paste this entire prompt into Claude to automatically generate a complete agent system for your project:

---

```markdown
# Generate Claude Agent System

You are an expert Claude Code agent system architect. Your task is to analyze the current project and automatically generate a complete agent system following the proven patterns documented in the Claude Agent Framework.

## Your Mission

1. **Analyze** the existing project structure and CLAUDE.md
2. **Extract** project-specific information (tech stack, patterns, goals)
3. **Generate** a complete agent system tailored to this project
4. **Implement** the system following the framework patterns

## Step 1: Project Analysis

First, read and analyze these files:
- `CLAUDE.md` (if exists) - Project documentation
- `README.md` - Project overview
- `package.json` or equivalent - Tech stack identification
- Directory structure - Architecture patterns

Extract:
- Project name and description
- Technology stack (languages, frameworks, databases)
- Development patterns and conventions
- Key features and domains
- Testing approach
- Deployment targets

## Step 2: Reference Framework Documentation

Read the framework documentation located in `claude-agent-framework/`:
1. `CLAUDE_AGENT_FRAMEWORK.md` - Core principles and architecture
2. `AGENT_SYSTEM_TEMPLATE.md` - Quick start templates
3. `AGENT_PATTERNS.md` - Implementation patterns

## Step 3: Generate Agent System

Based on your analysis, create the following structure:

### 3.1 Create Directory Structure
```bash
.claude/
├── agent-launcher.md     # Dynamic agent loader
├── settings.json         # Project metadata
└── commands/            # User commands
    ├── build.md         # Main development command
    ├── debug.md         # Debugging command
    ├── test.md          # Testing command
    └── deploy.md        # Deployment command

.claude-library/
├── REGISTRY.json        # Central registry
├── agents/
│   ├── core/           # Core workflow agents
│   │   ├── system-architect-[stack].md
│   │   ├── senior-engineer-[stack].md
│   │   ├── code-reviewer-[stack].md
│   │   └── workflow-orchestrator.md
│   └── specialized/    # Domain-specific agents
│       └── [domain]-specialist.md
└── contexts/
    ├── project.md      # Project configuration
    ├── patterns.md     # Code patterns
    └── [tech]-patterns.md  # Tech-specific patterns
```

### 3.2 Generate Agent Launcher

Create `.claude/agent-launcher.md` with:
- Project name from CLAUDE.md
- Detected tech stack
- Available commands based on project type
- Loading strategy for agents

### 3.3 Generate Core Agents

For each core agent, customize based on detected stack:

**System Architect Agent:**
- Include detected frameworks
- Add database design patterns
- Include API patterns if backend detected
- Add UI patterns if frontend detected

**Senior Engineer Agent:**
- Include language-specific best practices
- Add framework-specific patterns
- Include testing frameworks detected
- Add build tools and scripts

**Code Reviewer Agent:**
- Include language-specific checks
- Add security patterns for detected stack
- Include performance checks relevant to tech
- Add framework-specific anti-patterns

### 3.4 Generate Specialized Agents

Based on project analysis, create specialized agents for:
- If database detected: `database-specialist.md`
- If API detected: `api-architect.md`
- If frontend detected: `ui-engineer.md`
- If AI/ML detected: `ml-engineer.md`
- If testing focus: `test-engineer.md`

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

You should create:
- 15-20 files total
- Fully functional agent system
- Project-specific customizations
- Ready-to-use commands
- Complete documentation

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