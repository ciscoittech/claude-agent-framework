# Writing Tools for Agents - Practical Improvements

**Status**: Ready to implement
**Expected Impact**: +125% improvement (from test results)
**Effort**: 12-15 hours total

---

## Quick Wins (2-4 hours) - Implement These First

### 1. Add Tool Description Template to AGENT_PATTERNS.md

**Time**: 1 hour
**Impact**: Immediate clarity improvement

Add this section to `AGENT_PATTERNS.md`:

```markdown
## Tool Description Pattern

When describing tools in agent definitions, use this template:

### Tool: [Tool Name]

**Purpose**: [One clear sentence - what this tool does]

**When to Use**:
- [Specific scenario 1]
- [Specific scenario 2]

**Parameters**:
- `parameter_name` (type, required/optional): Clear description
  - Example value: `"example"`
  - Default: `value` (if optional)

**Returns**: [What the agent will receive back]

**Example Usage**:
```
[Tool Name](
  parameter_name="example_value",
  other_param=123
)
```

**Common Mistakes to Avoid**:
- ❌ [Common mistake 1]
- ❌ [Common mistake 2]

**Success Indicators**:
- [How to know it worked]
```

---

### 2. Add Token Efficiency Section to All Core Agents

**Time**: 2 hours
**Impact**: 20% token reduction

Add to **every** agent definition after "Available Tools":

```markdown
## Token Efficiency Guidelines

**Always Prefer**:
- ✅ Specific searches over broad queries
- ✅ Reading single files over globbing entire directories
- ✅ Targeted greps with context (-C 3) over full file searches
- ✅ Pagination: Start with limit=10, expand if needed

**Default Limits**:
- Grep results: Show first 10 matches, offer to continue
- File listings: Show first 20 files with summary
- Search results: Top 10 relevant items
- Log output: Most recent 50 lines

**Efficiency Patterns**:
```markdown
❌ Bad: Read all files, then filter
Glob("**/*.py") → Read each file → Search in memory

✅ Good: Filter first, then read
Grep("pattern", glob="**/*.py", -n) → Read only matches
```

**Response Format**:
- Include result counts: "Found 47 items, showing top 10"
- Offer next steps: "To see more, I can [action]"
- Signal truncation clearly: "... (truncated, 37 more items)"
```

---

### 3. Create Output Format Template

**Time**: 1 hour
**Impact**: Better user experience

Create `.claude-library/patterns/output-format-guide.md`:

```markdown
# Agent Output Format Guide

## Standard Response Structure

### For Task Completion
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

### For Search/Analysis Results
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

### For Errors/Blockers
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

## Usage in Agent Definitions

Add to each agent:

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
```

---

## Medium Priority (4-6 hours) - High Impact

### 4. Tool Consolidation in REGISTRY.json

**Time**: 3 hours
**Impact**: 30% reduction in tool confusion

**Current State Analysis**:
```json
{
  "agents": {
    "engineer": {
      "tools": ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
    },
    "architect": {
      "tools": ["Read", "Write", "Grep", "Glob", "Edit"]
    },
    "reviewer": {
      "tools": ["Read", "Grep", "Glob", "Bash"]
    }
  }
}
```

**Improvement**: Add tool categories and usage guidance

```json
{
  "agents": {
    "engineer": {
      "tools": {
        "file_operations": ["Read", "Write", "Edit"],
        "code_search": ["Grep", "Glob"],
        "execution": ["Bash"],
        "coordination": ["Task"]
      },
      "tool_guidelines": {
        "prefer_order": ["Read", "Grep", "Edit", "Write"],
        "avoid_patterns": [
          "Don't use Bash for file operations",
          "Prefer Grep over Read for searching"
        ],
        "token_limits": {
          "read_default": "2000 lines",
          "grep_default": "10 matches"
        }
      }
    }
  }
}
```

**Action Items**:
1. Categorize all tools by purpose
2. Add usage guidelines per agent type
3. Document anti-patterns
4. Set default limits

---

### 5. Rewrite Core Agent Tool Sections

**Time**: 3 hours
**Impact**: +300% tool description clarity (from test)

**Target**: Rewrite tool descriptions in these core agents:
- `framework-system-architect.md`
- `framework-senior-engineer.md`
- `framework-code-reviewer.md`

**Before/After Example**:

**❌ Current (typical)**:
```markdown
## Available Tools
- Read: For reading files
- Write: For creating files
- Grep: For searching
```

**✅ Improved**:
```markdown
## Available Tools

### Read - File Content Retrieval

**Purpose**: Read and analyze file contents with line numbers

**When to Use**:
- Understanding existing code before modifications
- Reviewing configuration files
- Analyzing log files for debugging

**Parameters**:
- `file_path` (string, required): Absolute path from project root
  - Example: `"/Users/dev/project/src/auth.py"`
- `limit` (int, optional): Max lines to read (default: 2000)
- `offset` (int, optional): Starting line (default: 1)

**Returns**: File contents with line numbers (1-indexed)

**Example Usage**:
```python
Read(file_path="/path/to/file.py", limit=50)
# Returns first 50 lines with line numbers
```

**Token Efficiency**:
- For large files (>1000 lines): Use `limit` and `offset` to paginate
- To find specific code: Use Grep first, then Read the relevant sections
- Default behavior loads up to 2000 lines

**Common Mistakes**:
- ❌ Reading entire 5000-line file when only need one function
- ❌ Using Read to search - use Grep instead
- ✅ Read specific sections after Grep finds locations

**Success Indicators**:
- Line numbers visible in output
- Content is readable and formatted
- File path confirmed in response
```

---

## Advanced Improvements (6-8 hours) - Maximum Impact

### 6. Create Agent-Specific Tool Guides

**Time**: 4 hours
**Impact**: Specialized optimization per agent type

Create tool usage guides per agent category:

**File**: `.claude-library/patterns/tool-usage-architect.md`
```markdown
# Tool Usage Guide: Architect Agents

## Your Tool Philosophy
You design systems, so your tools should support:
- Reading for understanding current architecture
- Writing for specifications and designs
- Searching for existing patterns

## Recommended Tool Patterns

### Pattern: Understand Before Design
```
1. Grep("class.*Auth", glob="**/*.py") → Find existing auth patterns
2. Read(relevant_files) → Understand implementation
3. Write("design.md") → Create specification
```

### Pattern: Research Existing Solutions
```
1. Grep("pattern_name", glob="**/*.md") → Find documentation
2. Read("docs/patterns.md") → Study approach
3. Write("proposal.md") → Propose architecture
```

## Anti-Patterns for Architects

❌ **Don't**: Use Bash to explore code
   **Instead**: Use Grep and Glob to map structure

❌ **Don't**: Edit files directly
   **Instead**: Write specifications for engineers

❌ **Don't**: Read every file in directory
   **Instead**: Grep to find relevant files first

## Token Budget

**Typical Architecture Task Budget**: 50K tokens

**Allocation**:
- Research (Grep/Read): 30K tokens (60%)
- Design output (Write): 15K tokens (30%)
- Iteration: 5K tokens (10%)

**Efficiency Tips**:
- Use Grep with `-n` to get line numbers
- Read file sections (limit=100) not entire files
- Write concise specs, not implementations
```

**Create similar guides for**:
- `tool-usage-engineer.md` (implementation-focused)
- `tool-usage-reviewer.md` (quality-focused)
- `tool-usage-debugger.md` (investigation-focused)

---

### 7. Add Tool Usage Metrics to Observability

**Time**: 2 hours
**Impact**: Data-driven optimization

Update `.claude-library/observability/db_helper.py`:

```python
def insert_tool_usage(execution_id, tool_name, parameters, success, duration_ms, tokens_used):
    """Track individual tool usage within agent execution"""
    with get_db() as conn:
        conn.execute("""
            INSERT INTO tool_usage (
                execution_id, tool_name, parameters_json,
                success, duration_ms, tokens_used, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            execution_id, tool_name, json.dumps(parameters),
            success, duration_ms, tokens_used, datetime.now().isoformat()
        ))
```

Add schema:
```sql
CREATE TABLE tool_usage (
    id INTEGER PRIMARY KEY,
    execution_id INTEGER,
    tool_name TEXT,
    parameters_json TEXT,
    success BOOLEAN,
    duration_ms INTEGER,
    tokens_used INTEGER,
    timestamp TEXT,
    FOREIGN KEY (execution_id) REFERENCES executions(id)
);
```

**Benefits**:
- Track which tools agents use most
- Identify inefficient tool usage patterns
- Measure token cost per tool
- Optimize based on real data

---

## Implementation Roadmap

### Week 1: Quick Wins (Foundation)
- [ ] Day 1-2: Add tool description template to AGENT_PATTERNS.md
- [ ] Day 3-4: Add token efficiency sections to all core agents
- [ ] Day 5: Create output format guide

**Deliverable**: Improved core agent definitions
**Test**: Run `test_best_practice_tool_writing.py` - expect +50% improvement

---

### Week 2: Medium Priority (Refinement)
- [ ] Day 1-2: Tool consolidation in REGISTRY.json
- [ ] Day 3-5: Rewrite core agent tool sections (3 agents)

**Deliverable**: Polished tool descriptions across framework
**Test**: Agents select correct tools 95%+ on first try

---

### Week 3: Advanced (Specialization)
- [ ] Day 1-3: Create agent-specific tool guides (4 types)
- [ ] Day 4-5: Add tool usage metrics to observability

**Deliverable**: Specialized guidance and data tracking
**Test**: Token usage reduces 20%, success rate +15%

---

## Validation Checklist

After implementing improvements, verify:

- [ ] All agent definitions have clear tool descriptions
- [ ] Tool sections follow "new team member" standard
- [ ] Token efficiency guidance present in all agents
- [ ] Output format guide referenced
- [ ] REGISTRY.json has tool categories
- [ ] Usage guidelines documented per agent type
- [ ] Test suite shows improvement: `pytest test_best_practice_tool_writing.py -v`
- [ ] Manual verification: Create task, observe tool selection accuracy

**Target Metrics** (from test):
- Tool namespacing: +50% → +60% (current: 1.7% → 2.5%)
- Token efficiency: +200% → +250% (current: 1.3 → 4.0 refs/agent)
- Description clarity: +300% (current: 25 → 100/100)
- Tool consolidation: -75% tool count

---

## Example: Before/After Agent Definition

### Before (Framework Research Specialist)
```markdown
## Available Tools
- Read: For reading files
- WebFetch: For fetching documentation
- Write: For creating files
- Edit: For modifying files
- Grep: For searching
- Glob: For finding files
```

### After (With Best Practices)
```markdown
## Available Tools

### Primary Tools (Use These First)

#### WebFetch - Documentation Retrieval
**Purpose**: Fetch and analyze official documentation from URLs

**When to Use**:
- Getting latest Claude Code documentation
- Retrieving Anthropic engineering blog posts
- Fetching API references

**Parameters**:
- `url` (string, required): Full URL to fetch
  - Example: `"https://docs.claude.com/en/docs/claude-code/sub-agents.md"`
- `prompt` (string, required): What to extract
  - Example: `"Extract all best practices about agent design"`

**Returns**: Extracted content based on prompt

**Token Efficiency**:
- Use specific prompts to extract only needed info
- Default: Fetches full page (~10-50KB)
- Tip: Request summaries for large docs

**Example**:
```
WebFetch(
  url="https://www.anthropic.com/engineering/writing-tools-for-agents",
  prompt="List the 5 main principles for tool design"
)
```

**Success Indicators**:
- Content returned matches URL
- Extracted info answers your prompt
- No network errors

---

#### Grep - Codebase Search
**Purpose**: Find patterns across project files

**When to Use**:
- Finding where a function is defined
- Locating all usages of a pattern
- Identifying files that need updates

**Parameters**:
- `pattern` (string, required): Regex pattern to search
  - Example: `"def process_.*\("`
- `glob` (string, optional): File filter
  - Example: `"**/*.py"` (Python files only)
- `-n` (flag): Show line numbers
- `-C N` (int): Show N lines of context

**Returns**: Matching lines with file paths

**Token Efficiency**:
- Use glob to narrow file scope
- Start with `output_mode: "files_with_matches"` to see which files
- Then use `output_mode: "content"` with `-n -C 3` for details
- Default: Returns first 10 matches

**Example**:
```
Grep(
  pattern="class.*Agent",
  glob="**/*.md",
  output_mode="content",
  -n=True,
  -C=2
)
```

**Common Mistakes**:
- ❌ Searching without glob filter (too broad)
- ❌ Not using -n flag (no line numbers)
- ✅ Filter first, get details second

### Secondary Tools (Use When Needed)

#### Read, Write, Edit
*[Similar detailed descriptions]*

## Tool Selection Decision Tree

```
Need to fetch external docs? → WebFetch
  ↓ No
Need to find something in code? → Grep (with glob filter)
  ↓ No
Need to understand specific file? → Read (with limit)
  ↓ No
Need to save findings? → Write
  ↓ No
Need to update existing file? → Edit
```

## Token Efficiency Guidelines

**Research Task Budget**: 30K tokens typical

**Allocation Strategy**:
1. **Discovery** (40%): Grep to find relevant files
2. **Analysis** (40%): Read selected files
3. **Documentation** (20%): Write findings

**Efficiency Tips**:
- Use Grep output_mode="files_with_matches" first (low tokens)
- Read only files that matched (targeted)
- Write concise summaries, not full docs
```

---

## Files to Update

**High Priority** (implement first):
1. `AGENT_PATTERNS.md` - Add tool description template
2. `.claude-library/agents/core/framework-system-architect.md` - Full rewrite of tools section
3. `.claude-library/agents/core/framework-senior-engineer.md` - Full rewrite of tools section
4. `.claude-library/agents/core/framework-code-reviewer.md` - Full rewrite of tools section

**Medium Priority**:
5. `.claude-library/REGISTRY.json` - Add tool categories and guidelines
6. `.claude-library/patterns/output-format-guide.md` - NEW file
7. All specialized agents - Add token efficiency sections

**Advanced**:
8. `.claude-library/patterns/tool-usage-*.md` - NEW files (4 agent types)
9. `.claude-library/observability/db_helper.py` - Add tool usage tracking
10. `.claude-library/observability/schema.sql` - Add tool_usage table

---

## Expected Results

**Immediate** (after quick wins):
- Agents understand tools better
- Token usage reduces 15-20%
- Fewer wrong tool selections

**Short-term** (after medium priority):
- Tool selection accuracy >95%
- Token efficiency +200%
- User-facing output quality improves

**Long-term** (after advanced):
- Data-driven tool optimization
- Agent-specific best practices established
- Framework becomes reference implementation of Anthropic best practices

---

*Implementation Guide v1.0*
*Part of Claude Agent Framework - Writing Tools for Agents Integration*
