# Implementation Step 1: Tool Description Template

**Goal**: Add the tool description template to AGENT_PATTERNS.md
**Time**: 1 hour
**Impact**: Foundation for all future agent improvements
**Priority**: CRITICAL - Do this first

---

## Why This First?

This template becomes the standard for:
- All future agent definitions
- Updating existing agents
- Onboarding new contributors
- Maintaining consistency

**Once this is done**, every other improvement becomes faster because you have a template to follow.

---

## Step-by-Step Instructions

### Step 1: Open AGENT_PATTERNS.md (2 minutes)

```bash
# From framework root directory
code AGENT_PATTERNS.md

# Or read it first to understand structure
cat AGENT_PATTERNS.md
```

**What to look for**:
- Current patterns documented
- Where to insert new section
- Existing formatting style

---

### Step 2: Find Insertion Point (3 minutes)

**Best location**: After existing patterns, before any appendices or end notes

**Look for section like**:
- "## Common Patterns"
- "## Implementation Patterns"
- "## Agent Configuration"

**Insert AFTER the last major pattern**, BEFORE:
- "## Related Documents"
- "## Changelog"
- End of file

**Example structure after insertion**:
```
## Existing Pattern 1
...

## Existing Pattern 2
...

## Tool Description Pattern  ← NEW SECTION HERE
...

## Related Documents
...
```

---

### Step 3: Copy Template (5 minutes)

**Copy this entire section** and paste at the insertion point:

```markdown
---

## Tool Description Pattern

When describing tools in agent definitions, use this template to ensure clarity and consistency. This pattern implements Anthropic's "new team member" standard from their "Writing Tools for Agents" best practice.

### Standard Template

For each tool in an agent definition, provide:

```markdown
### [Tool Name] - [Brief Category]

**Purpose**: [One clear sentence describing what this tool does]

**When to Use**:
- [Specific scenario 1 - be concrete]
- [Specific scenario 2 - be concrete]
- [Specific scenario 3 - be concrete]

**Parameters**:
- `parameter_name` (type, required/optional): Clear description
  - Example: `"example_value"`
  - Default: `value` (if optional)
  - Constraints: [any limits or requirements]

**Returns**: [What the tool returns - format and content]

**Token Efficiency**:
- [Default behavior and token cost]
- [How to minimize token usage]
- [When to use pagination/filtering]

**Example Usage**:
```
ToolName(
  parameter_name="actual_example",
  other_param=123
)
# Expected result: [what happens]
```

**Common Mistakes**:
- ❌ [Common mistake 1 with explanation]
  - Result: [What goes wrong]
- ❌ [Common mistake 2 with explanation]
  - Result: [What goes wrong]
- ✅ [Correct approach]
  - Result: [Success outcome]

**Success Indicators**:
- [How to verify the tool worked correctly]
- [What output should look like]
- [Performance expectations]
```

### Why This Pattern?

**Clarity**: New team member can understand tool without prior context
**Efficiency**: Token usage guidance prevents wasteful calls
**Safety**: Common mistakes section prevents errors
**Validation**: Success indicators help verify correct usage

### When to Use This Pattern

**Always use for**:
- Core agent definitions (architect, engineer, reviewer)
- Agents with 3+ tools
- Tools with complex parameters
- Tools with token efficiency considerations

**Can simplify for**:
- Single-tool agents
- Tools with only 1-2 parameters
- Rarely-used specialized tools

In these cases, you can use a shorter version:

```markdown
### [Tool Name]

**Purpose**: [One sentence]

**Usage**: `ToolName(param="value")`

**Returns**: [What you get back]
```

### Real Example: Read Tool

Here's how the Read tool should be documented:

```markdown
### Read - File Content Retrieval

**Purpose**: Read and analyze file contents with line numbers for debugging and code understanding

**When to Use**:
- Understanding existing code before making modifications
- Reviewing configuration files for settings
- Analyzing log files for error messages
- Reading documentation to understand patterns

**Parameters**:
- `file_path` (string, required): Absolute path to file
  - Example: `"/Users/dev/project/src/main.py"`
  - Must be complete path, not relative
- `limit` (int, optional): Maximum lines to read
  - Default: `2000`
  - Use for large files to avoid token overflow
- `offset` (int, optional): Starting line number
  - Default: `1`
  - Use with limit for pagination

**Returns**: File contents with line numbers (format: `line_number\t content`)

**Token Efficiency**:
- Default loads up to 2000 lines (~8-16KB depending on content)
- For files >1000 lines: Use Grep first to find relevant sections, then Read those specific sections with offset+limit
- For entire codebase search: Use Grep with glob filter, not Read all files

**Example Usage**:
```
# Read specific section of large file
Read(
  file_path="/Users/dev/project/src/main.py",
  offset=100,
  limit=50
)
# Returns lines 100-150 with line numbers
```

**Common Mistakes**:
- ❌ Reading 5000-line file without limit
  - Result: Token overflow, slow response, wasted context
- ❌ Using Read to search for pattern across files
  - Result: Inefficient, use Grep instead
- ❌ Relative path: `"src/main.py"`
  - Result: File not found error
- ✅ Grep to find location, then Read that section
  - Result: Fast, efficient, targeted

**Success Indicators**:
- Line numbers visible in output (e.g., `42\t def function():`)
- Content matches expected file
- No truncation warnings (unless expected)
- File path confirmed in response
```

### Implementation Checklist

When adding this pattern to AGENT_PATTERNS.md:

- [ ] Find appropriate insertion point
- [ ] Copy template section
- [ ] Adjust formatting to match existing style
- [ ] Add cross-reference from main framework docs
- [ ] Update REGISTRY.json to note pattern availability
- [ ] Test template with one agent update
- [ ] Document in CHANGELOG.md

### Validation

After adding the template, verify:

1. **Format consistency**: Matches existing AGENT_PATTERNS.md style
2. **Completeness**: All template sections present
3. **Example clarity**: Real example shows usage
4. **Findability**: Easy to locate in document (clear heading)
5. **Usability**: Another person could follow template without help

### Next Steps After This Template

Once the template is in AGENT_PATTERNS.md:

1. **Update one agent** (framework-senior-engineer.md) using the template
2. **Observe improvement** in that agent's tool selection
3. **Roll out to remaining agents** systematically
4. **Reference template** in all new agent definitions

---

## Success Criteria

You'll know this step is complete when:

✅ Template is in AGENT_PATTERNS.md
✅ Template has all sections (Purpose, When to Use, Parameters, etc.)
✅ Real example (Read tool) shows how to apply it
✅ Formatting matches existing document style
✅ You can find it quickly by scanning AGENT_PATTERNS.md

---

## Time Breakdown

- **Read AGENT_PATTERNS.md**: 5 minutes
- **Find insertion point**: 3 minutes
- **Copy and paste template**: 5 minutes
- **Adjust formatting**: 10 minutes
- **Review for completeness**: 5 minutes
- **Test by updating one tool description**: 30 minutes
- **Document in CHANGELOG**: 2 minutes

**Total**: ~60 minutes

---

## Potential Issues

### Issue: Not sure where to insert

**Solution**: Put it at the end, before "Related Documents" or "Changelog" if they exist. If no clear structure, add as new section after last pattern.

### Issue: Formatting doesn't match

**Solution**: Compare:
- Header levels (use same # style)
- Code block style (```markdown vs ```)
- List formatting (- vs *)
- Spacing between sections

### Issue: Template seems too detailed

**Solution**: That's intentional! The template shows maximum detail. The pattern doc explains when to simplify (see "When to Use This Pattern" section).

---

## Actual Code to Copy-Paste

Here's the exact text to copy into AGENT_PATTERNS.md:

```markdown
---

## Tool Description Pattern

When describing tools in agent definitions, use this template to ensure clarity and consistency. This pattern implements Anthropic's "new team member" standard from their "Writing Tools for Agents" best practice.

### Standard Template

```markdown
### [Tool Name] - [Brief Category]

**Purpose**: [One clear sentence describing what this tool does]

**When to Use**:
- [Specific scenario 1]
- [Specific scenario 2]

**Parameters**:
- `parameter_name` (type, required/optional): Description
  - Example: `"value"`
  - Default: `value` (if optional)

**Returns**: [What you get back]

**Token Efficiency**:
- [Guidance on token usage]

**Example Usage**:
```
ToolName(param="value")
```

**Common Mistakes**:
- ❌ [Mistake]: Result: [What happens]
- ✅ [Correct]: Result: [Success]

**Success Indicators**:
- [How to verify it worked]
```

### When to Use

- Core agents with 3+ tools: Use full template
- Simple agents with 1-2 tools: Use simplified version
- Specialized agents: Adapt template to domain

### Example: Read Tool

```markdown
### Read - File Content Retrieval

**Purpose**: Read and analyze file contents with line numbers

**When to Use**:
- Understanding code before modifications
- Reviewing configuration
- Analyzing logs

**Parameters**:
- `file_path` (string, required): Absolute path
  - Example: `"/path/to/file.py"`
- `limit` (int, optional): Max lines (default: 2000)
- `offset` (int, optional): Start line (default: 1)

**Returns**: File contents with line numbers

**Token Efficiency**:
- Default: 2000 lines (~8-16KB)
- For large files: Use Grep first, then Read specific sections

**Example Usage**:
```
Read(file_path="/path/file.py", offset=100, limit=50)
```

**Common Mistakes**:
- ❌ Read 5000-line file: Result: Token overflow
- ✅ Grep then Read section: Result: Efficient

**Success Indicators**:
- Line numbers visible
- Content matches expected file
```

**Source**: Anthropic "Writing Tools for Agents" best practice
**Added**: 2025-10-09
**See Also**: `.claude-library/contexts/anthropic-best-practices/writing-tools-for-agents.md`

---
```

---

## After This Step

**Immediate next action**: Update framework-senior-engineer.md to use this template

**Timeline**:
- Today: Add template to AGENT_PATTERNS.md (this step)
- Today: Update 1 agent to validate template
- This week: Update 3 core agents
- Next week: Roll out to all agents

**Validation**: Run `pytest test_best_practice_tool_writing.py` to measure improvement

---

*Implementation Step 1 Guide v1.0*
*Part of Writing Tools for Agents - Quick Action Plan*
*Claude Agent Framework - Best Practices Integration System*
