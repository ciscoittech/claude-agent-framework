# /generate-docs - Documentation Generation

**Purpose**: Analyze code and generate professional documentation
**Type**: Documentation Command

---

## Usage

```bash
/generate-docs <type> [target]
```

**Types**: `api`, `readme`, `architecture`, `guide`, `changelog`

**Examples**:
```bash
/generate-docs api                    # Generate API docs from code
/generate-docs readme                 # Generate/update README.md
/generate-docs architecture           # System architecture overview
/generate-docs guide src/auth/        # User guide for auth module
/generate-docs changelog              # Generate changelog from git history
```

---

## Workflow

### Step 1: Analyze Target

Read the codebase to understand:
- Project structure and tech stack (from package.json, CLAUDE.md, etc.)
- Existing documentation (don't duplicate)
- Code patterns and conventions

### Step 2: Generate by Type

#### `api` — API Reference
1. Find all route/endpoint definitions (Express routes, FastAPI endpoints, etc.)
2. Extract: method, path, parameters, request/response schemas, auth requirements
3. Generate markdown with:
   - Endpoint table (method | path | description)
   - Per-endpoint details with request/response examples
   - Authentication section
   - Error codes table
   - Code examples in the project's primary language + cURL

#### `readme` — Project README
1. Read CLAUDE.md, package.json, existing README
2. Generate sections:
   - Project description (from package.json or CLAUDE.md)
   - Quick start / installation
   - Usage examples
   - Configuration
   - Contributing guidelines
   - License
3. Preserve any existing sections the user has customized

#### `architecture` — Architecture Overview
1. Analyze directory structure and imports
2. Generate:
   - System overview (what it does, how it's organized)
   - Component diagram (ASCII or mermaid)
   - Data flow description
   - Technology stack table
   - Key design decisions

#### `guide` — Module/Feature Guide
1. Analyze the specified target directory
2. Generate:
   - Overview of what the module does
   - Key files and their roles
   - Usage examples
   - Configuration options
   - Common patterns

#### `changelog` — Changelog from Git
1. Read git log since last tag/release
2. Group commits by type (feat, fix, refactor, docs)
3. Generate Keep a Changelog format entry

### Step 3: Write Output

- Write to conventional locations (README.md, docs/, etc.)
- Use the project's existing doc style if present
- Don't overwrite user-customized sections

---

## Quality Standards

Generated docs must:
- Be accurate to the actual code (no hallucinated endpoints)
- Include working code examples
- Follow the project's existing naming conventions
- Be concise — no filler prose
