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
2. **Maximum 4 commands initially** — `/build`, plus `/launch-agent` and
   `/review-code` (both recommended for any project), plus at most ONE more
   the project demonstrably needs (e.g. `/test` when tests exist)
3. **NO specialized agents** unless explicitly detected and justified
4. **Sequential workflows by default** (parallel only if >3 independent tasks)
5. **Keep `.claude/` under 10KB** (see Step 5; `.claude-library/` is not counted)

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

**If SIMPLE -> Use MINIMAL configuration**

Expect ~11 files for the base: 3 agent definitions + 3 playbooks + registry +
`contexts/project.md` + 1 command + `settings.json` + `GETTING_STARTED.md`. Add one
per justified addition below — a simple project with tests and the recommended utility
commands lands around 14, which is correct, not bloat. The number to keep small is
`.claude/`, not the file count.
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

> **§4.6b is normative.** These documents are background: they explain *why* the
> framework is shaped the way it is. Their examples are now held to the same contract
> by `test_v2_structure.py`, so a registry entry, agent file, or path convention copied
> from any of them will validate. Where one still disagrees with §4.6b, §4.6b wins and
> the disagreement is a bug worth reporting. If you are short on time, read §4.6b and
> skip this step.

Optional background, in `claude-agent-framework/`:
1. `SIMPLICITY_ENFORCEMENT.md` - Circuit breakers against over-engineering (read first)
2. `CLAUDE_AGENT_FRAMEWORK.md` - Core principles and architecture
3. `AGENT_SYSTEM_TEMPLATE.md` - Quick start templates
4. `AGENT_PATTERNS.md` - Implementation patterns (use sparingly)

## Step 4: Generate MINIMAL Agent System

### 4.1 Start with MINIMAL Structure

**FOR SIMPLE PROJECTS (DEFAULT):**
```bash
.claude/                      # Auto-loaded by Claude Code
├── agents/                   # Subagent definitions - REAL frontmatter (see 4.3)
│   ├── architect.md
│   ├── engineer.md
│   └── reviewer.md
├── commands/
│   └── build.md              # ONLY build command initially
└── settings.json             # Hooks + permissions (the file the harness reads)

GETTING_STARTED.md            # Explains what was created (see 4.8)

.claude-library/              # Loaded on demand
├── REGISTRY.json             # Source of truth for tiers and wiring
├── agents/
│   └── core/                 # Full playbooks (depth lives here, not in .claude/)
│       ├── architect.md
│       ├── engineer.md
│       └── reviewer.md
└── contexts/
    └── project.md            # Required: agents reference this in contexts[]
```

**Agents live in two places on purpose.** `.claude/agents/<name>.md` is the real
subagent definition — its body becomes that agent's system prompt and is paid on
every launch, so keep it under ~100 lines. The full playbook (output formats,
checklists, examples) goes in `.claude-library/agents/` and is read on demand.

Do NOT generate `agent-launcher.md`. Claude Code routes on each agent's
`description` frontmatter; a hand-rolled launcher duplicates that and drifts.

**ONLY ADD MORE IF:**
- Tests detected -> Add test.md command
- Deployment config found -> Add deploy.md
- Multiple debugging issues in code -> Add debug.md
- Database with >5 tables -> Add database-specialist.md
- >10 API endpoints -> Add api-specialist.md

**DO NOT automatically create:**
- workflow-orchestrator (unless >5 parallel tasks)
- Multiple specialized agents
- Context files beyond `project.md` (that one is required — agents reference it)
- Tech-specific patterns unless dominant in codebase

### 4.2 Generate `.claude/settings.json`

This is the file Claude Code actually reads for hooks and permissions.
`REGISTRY.json` is framework metadata — the harness never loads it, so hooks
declared there do nothing.

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Write|Edit", "hooks": [
        { "type": "command", "command": "jq -r '.tool_input.file_path // empty' | { read -r f; [ -n \"$f\" ] && your-formatter \"$f\"; } 2>/dev/null || true" } ] }
    ]
  }
}
```

**Payload arrives as JSON on stdin, never as shell variables** — `script.sh
"$file_path"` gets an empty string. **On `PreToolUse`, exit 2 blocks; exit 1 does
not** (the tool runs anyway). Only generate hooks the project can actually run,
and generate any script you reference.

### 4.3 Generate SIMPLE Core Agents

**SIMPLICITY CHECK: Before adding ANYTHING to agents:**
1. Is this feature actively used in the project? If no -> DON'T ADD
2. Can existing tools handle this? If yes -> DON'T ADD
3. Is this a "nice to have"? If yes -> DON'T ADD

Each agent is generated as a **pair**: a lean definition in `.claude/agents/`
that Claude Code loads, and a full playbook in `.claude-library/agents/core/`
read on demand.

#### The `.claude/agents/<name>.md` definition — frontmatter is mandatory

Without YAML frontmatter this file is inert: Claude Code ignores tools listed as
prose under a `## Tools` heading, and the agent silently runs with default
model, default effort, and every tool available.

```markdown
---
name: architect
description: Designs system structure and data models for this project. Use for design work, architectural decisions, and planning how a new feature fits.
model: opus
effort: xhigh
color: cyan
tools: Read, Write, Edit, Grep, Glob
---

You are the architect for [PROJECT NAME].

## When you are the right agent
A change needs a design before it needs code.

## Before you start
Read your full playbook at `.claude-library/agents/core/architect.md`.
```

Frontmatter rules:
- `name` equals the filename; `model`/`effort` match `REGISTRY.json` exactly.
- `description` is what the harness routes on — write "Use for X, Y, Z", not a title.
- `tools` is a **comma-separated string**, not a YAML list. Never `*`.
- Never `model: inherit` — it lets a sub-agent adopt a coordinator's escalated tier.

#### Model and effort are two independent dials

`model` sets the capability floor; `effort` sets reasoning depth. Do not collapse
them — an opus agent at `low` effort and a haiku agent are different things.

| Role | model / effort |
|---|---|
| Mechanical (formatting, file checks) | haiku / low |
| Research, summarizing, fetching | sonnet / low |
| Docs, tests, structured output | sonnet / medium |
| Implementation, review, debugging | opus / high |
| Architecture and planning | opus / xhigh |
| Correctness outweighs cost (security, migrations) | opus / max |

- **haiku is the only 200K model; everything else is 1M.** Never send
  long-context work there — a rename across a large codebase is long-context.
- **fable is an opt-in escalation, never a generated default** (~2x opus, always
  thinks, much longer turns).
- Raise **effort** before **model**. Most "not smart enough" results are
  underspecified prompts, not undermodeled ones.

#### The `.claude-library/agents/core/<name>.md` playbook

Depth goes here: output format, checklists, anti-patterns, worked examples.
Size is not constrained — it is read only when the agent needs it.

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
- Classify the task, then select agent + **model** + **effort** (two dials, not one)
- Pass the filename in `.claude/agents/` as `subagent_type`; the harness applies
  that agent's declared tier automatically
- Read `REGISTRY.json` for the agent's tools, contexts, and tier
- Fall back to `general-purpose` only when no registry agent matches
- **A coordinator never propagates its own model to agents it launches** — pass
  each sub-agent its own registry tier explicitly

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

### 4.6b Exact Output Contract

Everything the validator enforces, stated once. Guessing any of these produces a
system that fails to load.

**Agent frontmatter — required keys, exactly these:**
`name`, `description`, `model`, `effort`, `tools`. `color` is optional.
`tools` is a comma-separated string (`Read, Write, Edit`), never a YAML list.

**`contexts[]` entries are bare filenames resolved against
`.claude-library/contexts/`.** Write `"contexts": ["project.md"]` for the file at
`.claude-library/contexts/project.md`. Not a path from the repo root, not the
registry key.

**`path` entries ARE repo-root-relative**, e.g.
`".claude-library/agents/core/architect.md"`. The two conventions differ — this
is the single most common generation error.

**Registry top level:** `version`, `agents`, `commands`, `contexts`, `skills`.
`commands` entries carry `path`, `agents` (which agents the command orchestrates), and
`workflow`; the human-facing `description` lives in `skills`, not here — one field, one
home. `contexts` entries are `{key: {path, description}}` where the key is the filename
stem.

**Registry keys per agent:** `path`, `type`, `domain`, `tools`, `model`,
`effort`, `triggers`, `contexts`, `priority`. Optional: `restrictions`.
Agent keys must equal the `.claude/agents/*.md` filenames.

**`.claude/settings.json`** holds hooks and permissions only — no project
metadata. Generate it only if you have hooks or permissions to declare; an empty
one is noise. Permissions shape:

```json
{ "permissions": { "allow": ["Bash(pytest:*)", "Read"], "deny": [] } }
```

**Command files** are invoked as `/name` and require frontmatter, plus a matching
`REGISTRY.json` -> `skills` entry. The validator fails on a command file with neither.

```markdown
---
description: Build the feature described, using the project's agents
allowed-tools: Agent, Read, Write, Edit, Grep, Glob
---
```

```json
"skills": {
  "build": {
    "path": ".claude/commands/build.md",
    "description": "Build the feature described, using the project's agents",
    "allowed_tools": ["Agent", "Read", "Write", "Edit", "Grep", "Glob"]
  }
}
```

`description` and `allowed_tools` must match the frontmatter exactly. Note the key
spellings differ by side: frontmatter uses `allowed-tools` (hyphen), the registry uses
`allowed_tools` (underscore). `allowed-tools` **pre-approves** tools rather than
restricting them, so scope `Bash` to what the command runs — `Bash(pytest:*)`, not bare
`Bash` — and never `*` or `Bash(*)`. Add `disable-model-invocation: true` (registry:
`"disable_model_invocation": true`) for a command expensive enough that firing it should
be a deliberate human act.

**If you generate a hook, generate the script it calls.** `.claude-library/hooks/scripts/`
is not in the minimal tree — create it, or reference only scripts you wrote.

**Running the validator:** `validate_agent_system.py` ships with the framework,
not with the generated project. Run it from the framework directory against the
generated root:
`python3 /path/to/claude-agent-framework/validate_agent_system.py <generated-root>`

### 4.7 Generate Registry

Create `.claude-library/REGISTRY.json`. Every agent entry carries:

```json
{
  "agents": {
    "architect": {
      "path": ".claude-library/agents/core/architect.md",
      "type": "core",
      "domain": "architecture",
      "tools": ["Read", "Write", "Edit", "Grep", "Glob"],
      "model": "opus",
      "effort": "xhigh",
      "triggers": ["design", "architecture", "schema"],
      "contexts": ["project.md"],
      "priority": 1
    }
  }
}
```

Hard requirements (key list and path conventions are in 4.6b):

1. `model`/`effort` must match the agent's frontmatter **exactly** — disagreement
   means the tier is prose again.
2. Every `path` and `contexts[]` entry must resolve; a missing context degrades
   the agent silently.
3. Every agent in a command's `agents[]` must exist in `agents`.
4. `Agent` not `Task`, `Edit` not `MultiEdit`, never `["*"]`.
5. **No hooks here** — Claude Code does not read this file (see 4.2).

### 4.8 Generate `GETTING_STARTED.md`

Write this into the **project root** (not `.claude/`). It is the only artifact that
explains what you just created — without it the user is handed two directories and no
way to tell whether they work.

**Generate it from what you actually created**, not from a template. Every agent, tier,
and command it names must exist. A getting-started doc describing a different system
than the one on disk is worse than none.

It must cover:

1. **What was created and why** — the two-directory split, keyed to this project's stack.
2. **The agents you got** — name, model/effort, and *why that tier*. State the
   non-propagation rule: a coordinator never passes its own model to agents it launches.
3. **How to use it** — the commands available, and launching an agent by
   `subagent_type` (the filename in `.claude/agents/`).
4. **How to verify it works** — the exact validator command, and what a pass looks like.
   Put this early; it is the first thing a user needs.
5. **How to extend it** — adding an agent, a skill, or a hook, each in a few steps.
6. **The two rules most often broken later**:
   - `REGISTRY.json` and `.claude/agents/` frontmatter must agree, or the tier is
     unenforced prose.
   - Hooks go in `.claude/settings.json`. Claude Code never reads `REGISTRY.json`.

Keep it under ~120 lines. It is a starting point, not a manual.

## Step 5: Optimization

Apply these optimizations:
1. Keep `.claude/` under 10KB (this is the only size budget that matters —
   it is what loads on every session; `.claude-library/` is unconstrained)
2. Use lazy loading for all agents
3. Set up parallel execution where possible
4. Include only essential contexts
5. Cache frequently used agents

## Step 6: Validation

**Run the validator. Do not eyeball it.**

```bash
python3 /path/to/claude-agent-framework/validate_agent_system.py <generated-project-root>
```

It checks exactly what silently breaks a generated system:
- every registry `path` and `contexts[]` entry resolves
- no `subagent_type` names an agent that does not exist
- every agent has a valid `model` + `effort`
- `.claude/agents/*.md` frontmatter parses and has all required keys
- frontmatter and registry agree on model, effort, and tools
- no deprecated tool names (`Task`, `MultiEdit`)

Exit code 0 means the system will load. **A non-zero exit means agents will fail
at launch time — fix before reporting the system as generated.**

Then confirm by hand what the validator cannot see:
1. Contexts contain this project's real patterns, not generic filler
2. Command workflows match how the project is actually built and tested
3. Any generated hook runs a command this project actually has

## Implementation Instructions

Execute this plan:
1. Read CLAUDE.md and project files
2. Generate all files according to the framework
3. Customize for detected technology stack
4. Report what was created and why
5. Provide usage instructions

## Expected Output

**FOR SIMPLE PROJECTS (DEFAULT):**
- ~11 base files, ~14 with tests and utility commands (NOT 20+)
- Minimal functional system
- ONLY essential customizations
- Single build command to start
- Brief documentation

**FOR MEDIUM PROJECTS:**
- ~14-18 files (more agents and commands than SIMPLE, still no speculative ones)
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

## Appendix: Framework Maintenance

This prompt generates a system for *your* project. Maintaining the framework itself
(ingesting new Anthropic guidance, validating framework changes) is a separate
workflow documented in its own commands:

- `.claude/commands/ingest-best-practice.md` — ingest guidance, extract principles, analyze gaps
- `.claude/commands/validate-framework.md` — validate framework changes against metrics

Neither is needed to generate or use a project agent system.

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
