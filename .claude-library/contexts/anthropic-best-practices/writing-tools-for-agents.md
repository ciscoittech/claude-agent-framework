# Writing Tools for AI Agents - Anthropic Best Practices

**Source**: https://www.anthropic.com/engineering/writing-tools-for-agents
**Date Ingested**: 2025-10-09
**Framework Version**: 1.1
**Relevance**: Agent design, tool configuration, context management

---

## Core Philosophy

> Design tools that help agents solve tasks intuitively, mirroring how a human would approach the problem.

Tools should be built around agents' unique "affordances" - what they can naturally do well versus what humans excel at.

---

## Key Principles

### 1. Choose Tools Strategically

**Best Practice**: Build a few thoughtful tools targeting high-impact workflows

**Guidelines**:
- Consolidate functionality into single tools when possible
- Avoid creating tools that merely wrap existing API endpoints
- Focus on tools that match agents' unique capabilities
- Quality over quantity

**Example**:
- ❌ Bad: `create_issue()`, `update_issue()`, `close_issue()`, `reopen_issue()`
- ✅ Good: `manage_issue(action, issue_id, data)` - Single tool with clear actions

**Framework Application**:
- Review agent tool lists in REGISTRY.json
- Consolidate overlapping tool definitions
- Ensure each tool serves a distinct, high-value purpose

---

### 2. Design Tool Namespacing

**Best Practice**: Group related tools under common prefixes using clear namespacing

**Guidelines**:
- Use service-based prefixes (e.g., `asana_search`, `github_create_pr`)
- Create clear boundaries between tool domains
- Reduce agent confusion through organization
- Use consistent naming patterns

**Example**:
```
Database Tools:
- database_query()
- database_schema()
- database_optimize()

API Tools:
- api_get()
- api_post()
- api_analyze()
```

**Framework Application**:
- Audit existing agent tool configurations
- Apply consistent naming to tool access in agent definitions
- Group tools by domain in REGISTRY.json

---

### 3. Return Meaningful Context

**Best Practice**: Prioritize high-signal information in tool responses

**Guidelines**:
- Use natural language identifiers over cryptic technical codes
- Provide flexible response formats (e.g., "concise" vs "detailed")
- Avoid returning irrelevant or overwhelming information
- Make error messages actionable

**Example**:
- ❌ Bad: `{"status": 404, "code": "ERR_NOT_FOUND"}`
- ✅ Good: `"The user profile 'john_doe' was not found. Available actions: 1) Check username spelling, 2) Create new profile, 3) Search all profiles"`

**Framework Application**:
- Update agent "Output Format" sections
- Add guidance on context quality in responses
- Teach agents to prioritize signal over noise

---

### 4. Optimize Token Efficiency

**Best Practice**: Implement pagination, filtering, and sensible truncation

**Guidelines**:
- Use default limits on result sets
- Provide filtering parameters
- Truncate responses with clear indicators
- Guide agents toward targeted, small searches
- Make error messages concise but actionable

**Example**:
```markdown
## Search Guidelines
- Default: Return top 10 results
- Use filters to narrow searches before expanding
- If >100 results, paginate and ask user to refine
- Show result count: "Found 247 items, showing top 10"
```

**Framework Application**:
- Add token efficiency guidance to all agents
- Include pagination patterns in agent instructions
- Teach agents to start narrow, then expand if needed

---

### 5. Prompt Engineering for Tools

**Best Practice**: Write tool descriptions as if explaining to a new team member

**Guidelines**:
- Be explicit about expected inputs and outputs
- Create clear, unambiguous parameter names
- Provide examples of correct usage
- Test and iterate based on agent performance
- Avoid jargon unless domain-specific

**Example**:
```markdown
## Tool: Read File

**Purpose**: Read contents of a file from the project directory

**Parameters**:
- file_path (string, required): Absolute path to file (e.g., "/Users/dev/project/src/main.py")
- limit (int, optional): Max lines to read (default: 2000)
- offset (int, optional): Starting line number (default: 1)

**Returns**: File contents with line numbers

**Example**:
Read("file_path": "/app/config.json") → Returns full JSON file with line numbers
```

**Framework Application**:
- Audit all agent tool descriptions
- Rewrite using "new team member" standard
- Add concrete examples to each tool usage section

---

## Implementation Checklist

Apply these best practices to the framework:

### Tool Strategy
- [ ] Consolidate overlapping tools in agent definitions
- [ ] Remove wrapper-only tools
- [ ] Focus on high-impact workflow tools

### Namespacing
- [ ] Apply consistent naming to all tool references
- [ ] Group tools by domain (database_, api_, file_, etc.)
- [ ] Update REGISTRY.json with organized tool lists

### Context Quality
- [ ] Audit agent "Output Format" sections
- [ ] Add guidance on returning meaningful context
- [ ] Teach agents to avoid information overload

### Token Efficiency
- [ ] Add pagination guidance to all agents
- [ ] Include filtering strategies
- [ ] Set default result limits

### Prompt Engineering
- [ ] Rewrite all tool descriptions for clarity
- [ ] Add concrete examples to each tool
- [ ] Test agent understanding of tool usage

---

## Metrics for Success

**Before/After Comparison**:
- Tool usage errors (target: 30% reduction)
- Average tokens per agent response (target: 20% reduction)
- Agent task success rate (target: 15% improvement)
- Time to complete workflows (target: 10% faster)

**Quality Indicators**:
- Agents choose correct tool on first try
- Responses contain high-signal information
- Token usage stays within optimal ranges
- User satisfaction with agent outputs

---

## Related Framework Documents

- `CLAUDE_AGENT_FRAMEWORK.md` - Agent design principles (Section: Tool Configuration)
- `AGENT_PATTERNS.md` - Implementation patterns
- `SIMPLICITY_ENFORCEMENT.md` - Complexity constraints

---

## Next Steps

1. Run gap analysis comparing these practices to current framework
2. Identify high-impact improvements
3. Create experimental implementations
4. Test improvements with validation suite
5. Measure before/after metrics
6. Integrate successful improvements into framework

---

*Best Practice Document v1.0*
*Part of Claude Agent Framework - Best Practices Integration System*
