# Tool Usage Guide: Researcher Agent

## Tool Philosophy

Researchers fetch specifically with targeted extraction prompts, analyze thoroughly to synthesize findings, and document clearly for agent consumption. The goal is actionable knowledge, not raw data—use tools to retrieve precise information, compare with existing knowledge, and create structured documentation that agents can load efficiently.

---

## Recommended Tool Patterns

### Pattern 1: Targeted Fetching
**When to Use**: Retrieving information from web sources or documentation
**Workflow**:
1. `WebFetch` with specific extraction prompts (not vague requests)
2. Focus on what information is needed, not entire pages
3. Process and structure findings immediately
4. Avoid fetching the same URL multiple times

**Example**:
```
Task: Research FastAPI's latest async patterns

❌ Bad: WebFetch("https://fastapi.tiangolo.com/", "summarize this page")
✅ Good: WebFetch(
    "https://fastapi.tiangolo.com/async/",
    "Extract: 1) async/await usage patterns, 2) when to use async vs sync,
    3) performance considerations. Provide code examples for each."
)
```
**Token Cost**: ~5K (Specific fetch vs. 15K for vague fetch)

### Pattern 2: Documentation Discovery
**When to Use**: Understanding existing project documentation before adding new content
**Workflow**:
1. `Grep` to find existing documentation files
2. `Read` relevant docs to understand structure and coverage
3. Extract gaps or outdated information
4. Plan updates without duplicating existing content

**Example**:
```
1. Grep "authentication|auth" glob:"**/*.md" → finds 3 docs
2. Read "docs/auth-guide.md" → covers OAuth2, missing JWT refresh
3. Read "docs/api-security.md" → covers API keys, no JWT content
4. Plan: Update auth-guide.md to add JWT refresh section (not new file)
```
**Token Cost**: ~8K (Grep: 2K, Read: 5K, Planning: 1K)

### Pattern 3: Change Tracking
**When to Use**: Monitoring for updates to external dependencies or documentation
**Workflow**:
1. `Read` existing cached/documented version
2. `WebFetch` current version with comparison prompt
3. Identify what changed (new features, deprecations, breaking changes)
4. Document changes, not entire new version

**Example**:
```
1. Read ".claude-library/contexts/fastapi-patterns.md" → v0.104 patterns
2. WebFetch(
    "https://fastapi.tiangolo.com/release-notes/",
    "List changes from v0.104 to latest. Focus on: breaking changes,
    new async patterns, deprecated features."
)
3. Document: "FastAPI v0.110 updates: Added BackgroundTasks improvements..."
```
**Token Cost**: ~7K (Read: 3K, Fetch: 3K, Update: 1K)

### Pattern 4: Structured Documentation
**When to Use**: Creating new context files or updating existing ones
**Workflow**:
1. Research and gather information (Patterns 1-3)
2. Structure findings into sections: Overview, Key Concepts, Patterns, Examples
3. `Write` concise, agent-optimized documentation (<5KB per file)
4. Include source attribution and last-updated date

**Example**:
```
Structure for context file:
1. Overview (2-3 sentences)
2. Key Concepts (bulleted list, 5-7 items)
3. Patterns (3-5 patterns with examples)
4. Common Pitfalls (3-5 anti-patterns)
5. References (URLs, version, date)

Write ".claude-library/contexts/fastapi-async.md" → 4.2KB
```
**Token Cost**: ~10K (Research: 7K, Structuring: 2K, Writing: 1K)

### Pattern 5: Integration Workflow
**When to Use**: Complete research task from discovery to documentation
**Workflow**:
1. `Grep` to understand existing knowledge base
2. `WebFetch` to gather new/updated information
3. `Read` existing docs to find integration points
4. `Edit` existing docs or `Write` new ones as appropriate
5. Update relevant agent contexts

**Example**:
```
Task: Research and document Pydantic v2 changes

1. Grep "pydantic" glob:"**/*.md" → find existing Pydantic docs
2. Read ".claude-library/contexts/pydantic-patterns.md" → v1 patterns
3. WebFetch Pydantic v2 migration guide → get key changes
4. Edit existing file to add v2 section (don't replace v1 info)
5. Update ".claude-library/contexts/dependencies.md" → note v2 upgrade
```
**Token Cost**: ~15K (Discovery: 4K, Fetch: 5K, Read: 3K, Update: 3K)

---

## Anti-Patterns to Avoid

1. ❌ **Fetching entire pages with vague prompts**: `WebFetch(url, "summarize")` returns too much irrelevant data → ✅ **Instead**: Use specific extraction prompts: "Extract installation steps and configuration options only"

2. ❌ **Duplicating existing documentation**: Creating new files that overlap with existing docs fragments knowledge → ✅ **Instead**: Use `Grep` and `Read` to find existing docs, then `Edit` to enhance them

3. ❌ **Updating without reading current state**: Overwriting docs without understanding what's there loses valuable information → ✅ **Instead**: Always `Read` existing documentation before `Edit` or `Write` operations

4. ❌ **Creating unstructured documentation**: Writing stream-of-consciousness docs that agents can't efficiently parse → ✅ **Instead**: Use consistent structure: Overview, Concepts, Patterns, Examples, References

5. ❌ **Skipping source attribution**: Documenting information without noting sources or dates makes it impossible to validate or update → ✅ **Instead**: Always include source URLs, version numbers, and last-updated timestamps

---

## Token Budget Allocation

**Typical Budget**: 50K tokens

**Allocation**:
- Fetch Phase: 30% (~15K tokens) - WebFetch operations, gathering external information
- Research Phase: 40% (~20K tokens) - Reading existing docs, comparing sources, analysis
- Documentation Phase: 30% (~15K tokens) - Writing/editing structured documentation

**Budget Management**:
- Use specific WebFetch prompts to reduce fetched content by 60-70%
- Read existing docs before fetching to avoid duplicating known information
- Write concise documentation (<5KB per file) for efficient agent loading
- Cache frequently-accessed information in context files to avoid repeated fetches

---

## Efficiency Tips

1. **Prompt Engineering for WebFetch**: Craft extraction prompts that specify exactly what you need. Example: Instead of "get FastAPI info", use "Extract async/await patterns with code examples, list performance benchmarks, note Python version requirements". This reduces tokens by 60-70%.

2. **Documentation Hierarchy**: Organize contexts by specificity: `contexts/python.md` (general) → `contexts/fastapi.md` (framework) → `contexts/fastapi-async.md` (specific pattern). Agents load only what they need.

3. **Version Tracking**: Include version numbers and dates in all documentation. Example: "FastAPI Async Patterns (v0.110, Updated: 2025-03-15)". This makes it obvious when research needs updating.

4. **Grep Before Fetch**: Always search existing documentation before fetching external sources. You might already have 80% of needed information, requiring only targeted fetches for gaps.

5. **Structured Updates Over Rewrites**: When updating documentation, use `Edit` to add new sections or update specific parts rather than rewriting entire files. This preserves existing valuable information and reduces token usage.

---

*Tool Usage Guide v1.0 - Researcher Agent*
*Part of Claude Agent Framework - Best Practices Integration*
