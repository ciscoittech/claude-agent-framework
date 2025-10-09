# Agent Output Format Guide

This guide provides standard response structures for all agents to ensure consistent, user-friendly output across the framework.

## Standard Response Structures

### Task Completion Format

Use this format when you've successfully completed a task:

```markdown
✅ **Task Complete**: [One sentence summary]

**What I Did**:
1. [Action 1] - Result: [outcome]
2. [Action 2] - Result: [outcome]

**Files Changed**:
- `path/to/file.py:45` - [What changed]
- `path/to/file.py:67` - [What changed]

**Next Steps** (if applicable):
- [Suggested action 1]
- [Suggested action 2]
```

**Example**:
```markdown
✅ **Task Complete**: Added authentication middleware to API routes

**What I Did**:
1. Created JWT validation middleware - Result: Validates tokens on protected routes
2. Updated route configuration - Result: Applied middleware to /api/* endpoints
3. Added error handling - Result: Returns 401 for invalid tokens

**Files Changed**:
- `src/middleware/auth.py:15` - Added JWTAuthMiddleware class
- `src/api/routes.py:34` - Registered middleware on protected routes
- `src/api/errors.py:89` - Added UnauthorizedError handler

**Next Steps**:
- Add integration tests for protected endpoints
- Update API documentation with auth requirements
```

---

### Search/Analysis Results Format

Use this format when returning search or analysis results:

```markdown
📊 **Found N results** (showing top 10)

**Most Relevant**:
1. `file.py:23` - [Context snippet]
   Relevance: [Why this matches]

2. `file.py:45` - [Context snippet]
   Relevance: [Why this matches]

**Summary**: [Pattern or insight across results]

**To see more**: [How to expand search]
```

**Example**:
```markdown
📊 **Found 47 results** (showing top 10)

**Most Relevant**:
1. `src/auth/jwt.py:45` - `def verify_token(token: str) -> bool:`
   Relevance: Main token verification function

2. `tests/test_auth.py:123` - `assert verify_token(valid_token) == True`
   Relevance: Test coverage for token verification

3. `src/middleware/auth.py:67` - `if not verify_token(request.headers.get("Authorization")):`
   Relevance: Usage in middleware

**Summary**: Token verification is centralized in jwt.py with 8 call sites across the codebase. All usages follow the same pattern of checking headers.

**To see more**: Use `Grep("verify_token", output_mode="content", -C=5)` for full context around each usage.
```

---

### Errors/Blockers Format

Use this format when you encounter an error or blocker:

```markdown
⚠️ **Blocked**: [What couldn't be done]

**Issue**: [Clear explanation]

**Attempted**:
1. [What I tried]
2. [What I tried]

**Suggested Solutions**:
1. [Most likely fix]
2. [Alternative approach]
3. [Workaround if needed]

**Need from you**: [Specific user action required]
```

**Example**:
```markdown
⚠️ **Blocked**: Cannot run tests - pytest not installed

**Issue**: Test suite requires pytest but it's not available in the environment.

**Attempted**:
1. Checked for pytest in project dependencies - Found in requirements.txt but not installed
2. Looked for alternative test runners - None configured
3. Checked virtual environment - No venv activated

**Suggested Solutions**:
1. **Install dependencies**: Run `pip install -r requirements.txt`
2. **Activate virtual environment**: Run `source venv/bin/activate` then retry
3. **Manual verification**: I can review test files for issues, but cannot execute them

**Need from you**: Please install project dependencies or confirm which Python environment to use.
```

---

## Usage in Agent Definitions

Add this section to each agent definition:

```markdown
## Output Format

Follow the standard output format guide for all responses:
- Use structured markdown with clear sections
- Include file paths as `path:line` for easy navigation
- Provide result counts and pagination info
- Suggest next steps when applicable
- Make errors actionable with solutions

See: `.claude-library/patterns/output-format-guide.md`
```

---

## Best Practices

### File Path References

Always include line numbers with file paths for easy navigation:
- ✅ Good: `src/auth.py:45`
- ❌ Bad: `src/auth.py`

### Result Counts

Always indicate total results and what you're showing:
- ✅ Good: "Found 47 results (showing top 10)"
- ❌ Bad: "Here are some results"

### Pagination Guidance

Tell users how to see more results:
- ✅ Good: "To see all results, use `limit=100`"
- ❌ Bad: "There are more results"

### Actionable Errors

Make errors specific and actionable:
- ✅ Good: "Run `npm install` to install missing dependencies"
- ❌ Bad: "Dependencies missing"

### Next Steps

Always suggest what should happen next:
- ✅ Good: "Next Steps: Run tests, update docs"
- ❌ Bad: [No guidance provided]

---

## Response Length Guidelines

### Concise (Preferred)
- Task completion: 5-10 lines
- Search results: Top 10 items with summary
- Errors: 3 solutions maximum

### Detailed (When Needed)
- Complex analysis: Add "Deep Dive" section
- Multiple changes: Group by category
- Systematic errors: Show pattern analysis

### Always Truncate Large Output
- Default: Show first 10-20 items
- Provide: "To see more, use [command]"
- Include: Total count

---

## Visual Indicators

Use these consistently across all agents:

- ✅ Success/Completion
- ⚠️ Warning/Blocker
- 📊 Analysis/Results
- 🔍 Search/Discovery
- 💡 Suggestion/Insight
- ❌ Error/Failure
- 🔧 Fix/Solution

---

## Token Efficiency

### Efficient Output
- Show summaries, not full content
- Provide paths to detailed info
- Use pagination for large results
- Group similar items

### Example - Efficient
```markdown
📊 **Found 47 function definitions** (showing top 5)

Grouped by type:
- API handlers: 23 functions
- Database queries: 15 functions
- Utility helpers: 9 functions

To see details: `Grep("def ", glob="**/*.py", -n, -C=3)`
```

### Example - Inefficient
```markdown
Here's every function I found:
[47 full function definitions with 20 lines each = 940 lines of output]
```

---

*Part of Claude Agent Framework - Output Standardization Guide v1.0*
