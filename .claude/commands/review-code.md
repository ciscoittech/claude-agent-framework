# /review-code - Code Review

**Purpose**: Review code changes for bugs, security issues, and quality
**Type**: Quality Assurance Command

---

## Usage

```bash
/review-code [target]
```

**Examples**:
```bash
/review-code                          # Review all uncommitted changes
/review-code src/auth/                # Review specific directory
/review-code --staged                 # Review staged changes only
/review-code --pr 42                  # Review a pull request
```

---

## Workflow

### Step 1: Determine Scope

- No target → `git diff` (all uncommitted changes)
- `--staged` → `git diff --staged`
- `--pr <number>` → `gh pr diff <number>`
- Path target → read all files in that path

### Step 2: Analyze Changes

Launch a reviewer agent (read-only tools: Read, Grep, Glob) to check:

#### Correctness
- Logic errors, off-by-one, null/undefined handling
- Missing error handling for failure cases
- Race conditions in async code
- Incorrect API usage or contract violations

#### Security (OWASP Top 10)
- Injection: SQL, command, XSS
- Authentication/authorization gaps
- Sensitive data exposure (hardcoded secrets, logging PII)
- Missing input validation at system boundaries

#### Quality
- Dead code or unused imports
- Functions doing too many things
- Inconsistent naming or style vs rest of codebase
- Missing or misleading comments

#### Performance (only if obvious)
- N+1 queries
- Unbounded loops or memory allocation
- Missing indexes on queried fields
- Synchronous I/O in async context

### Step 3: Report Findings

Format as:

```markdown
## Code Review Summary

**Files reviewed**: N
**Issues found**: N critical, N warnings, N suggestions

### Critical
- `file:line` — Description of issue and why it matters
  **Fix**: What to do

### Warnings
- `file:line` — Description
  **Fix**: What to do

### Suggestions
- `file:line` — Description

### Looks Good
- Brief note on what's well done (if applicable)
```

### Step 4: Offer to Fix

After presenting findings, ask:
> "Want me to fix any of these issues?"

If yes, launch an engineer agent to apply fixes for the agreed items.

---

## Severity Levels

| Level | Meaning | Examples |
|-------|---------|---------|
| **Critical** | Must fix before merge | Security vulnerability, data loss risk, crash |
| **Warning** | Should fix | Missing error handling, potential bug, bad practice |
| **Suggestion** | Consider fixing | Style, naming, minor optimization |

---

## What This Does NOT Do

- Nitpick formatting (that's what linters are for)
- Demand test coverage percentages
- Require documentation for every function
- Block on style preferences
