# Tool Usage Guide: Architect Agent

## Tool Philosophy

Architects research deeply to understand existing patterns, then design concisely to guide implementation. The goal is specification, not implementation—use tools to discover what exists, analyze patterns, and document clear architectural decisions that engineers can execute independently.

---

## Recommended Tool Patterns

### Pattern 1: Discovery Workflow
**When to Use**: Starting architectural analysis for a new feature or module
**Workflow**:
1. `Glob` to find relevant file types (e.g., `**/*.py`, `**/models/*.ts`)
2. `Grep` with `files_with_matches` to identify files containing key patterns
3. `Grep` with `content` mode to extract specific architectural patterns
4. `Read` only the most relevant files for deep analysis

**Example**:
```
1. Glob "**/*.py" → finds 47 Python files
2. Grep "class.*Model" files_with_matches → identifies 12 model files
3. Grep "class.*Model" content -A 5 → extracts model definitions
4. Read only the 3 core models for inheritance patterns
```
**Token Cost**: ~8K (Glob: 1K, Grep: 3K, Read: 4K)

### Pattern 2: Architecture Analysis
**When to Use**: Understanding existing architectural patterns before designing new ones
**Workflow**:
1. `Read` existing architecture docs or main entry points
2. `Grep` for architectural patterns (factories, builders, strategies)
3. `Grep` for integration points (imports, dependencies)
4. Analyze in memory without additional reads

**Example**:
```
1. Read "docs/architecture.md" → understand intended design
2. Grep "Factory|Builder|Strategy" → find 8 pattern implementations
3. Grep "from.*import" type:py → map dependency graph
4. Synthesize findings into architectural assessment
```
**Token Cost**: ~12K (Read: 5K, Grep: 4K, Analysis: 3K)

### Pattern 3: Specification Creation
**When to Use**: Documenting architectural decisions and component designs
**Workflow**:
1. Research phase (Glob + Grep patterns above)
2. `Write` concise specification files (not implementation)
3. Focus on interfaces, contracts, and integration points
4. Keep specs under 200 lines

**Example**:
```
1. Research existing auth patterns (8K tokens)
2. Write ".claude-library/specs/auth-architecture.md":
   - Authentication flow (20 lines)
   - Interface definitions (30 lines)
   - Integration requirements (15 lines)
   - Security considerations (25 lines)
```
**Token Cost**: ~10K (Research: 8K, Write: 2K)

### Pattern 4: Pattern Research
**When to Use**: Before creating new architectural patterns
**Workflow**:
1. `Grep` for existing similar patterns across codebase
2. `Read` pattern implementations to understand rationale
3. Identify gaps or inconsistencies
4. Document pattern decision (use existing vs. create new)

**Example**:
```
1. Grep "singleton|borg" → finds 3 singleton implementations
2. Read the most recent one → see thread-safe pattern
3. Grep "thread.*safe" → validate threading approach
4. Specify: "Use existing SingletonMeta from utils.patterns"
```
**Token Cost**: ~7K (Grep: 3K, Read: 3K, Specification: 1K)

### Pattern 5: Design Validation
**When to Use**: Validating architectural decisions against existing code
**Workflow**:
1. `Read` current implementation or specification
2. `Grep` for conflicting patterns or inconsistencies
3. Compare proposed design against findings
4. Refine specification to align with codebase conventions

**Example**:
```
1. Read proposed API design (3K tokens)
2. Grep "class.*API|def.*endpoint" → find 15 existing APIs
3. Compare naming conventions, error handling, auth patterns
4. Refine spec to match established patterns
```
**Token Cost**: ~8K (Read: 3K, Grep: 3K, Refinement: 2K)

---

## Anti-Patterns to Avoid

1. ❌ **Using Bash to explore code structure**: Running `find` or `ls -R` wastes tokens and provides unstructured output → ✅ **Instead**: Use `Glob` with patterns like `**/*.py` for structured file discovery

2. ❌ **Writing implementation code**: Architects who write actual code blur responsibilities and waste architectural capacity → ✅ **Instead**: Write interface definitions, contracts, and integration specs that engineers implement

3. ❌ **Editing files directly**: Architects modifying implementation files creates confusion about ownership → ✅ **Instead**: Create specification documents that engineers use to make proper edits

4. ❌ **Reading sequentially without Grep first**: Reading files one-by-one to find patterns wastes massive tokens → ✅ **Instead**: `Grep` to identify relevant files, then `Read` only the 2-3 most important ones

5. ❌ **Designing without researching existing patterns**: Creating new patterns that conflict with established conventions → ✅ **Instead**: Always `Grep` for similar patterns first, reuse and extend rather than reinvent

---

## Token Budget Allocation

**Typical Budget**: 50K tokens

**Allocation**:
- Research Phase: 60% (~30K tokens) - Discovery, pattern analysis, validation
- Design Phase: 30% (~15K tokens) - Specification creation, documentation
- Iteration Phase: 10% (~5K tokens) - Refinements based on engineer feedback

**Budget Management**:
- Use `Grep` with `files_with_matches` before `content` mode (saves 50-70%)
- Read only critical files after filtering with Grep
- Write concise specs (100-200 lines) instead of comprehensive guides
- Avoid reading implementation details unless architecturally significant

---

## Efficiency Tips

1. **Parallel Discovery**: When researching multiple aspects (models, APIs, configs), run multiple `Grep` searches in parallel to save round trips. Example: Search for models, services, and tests simultaneously rather than sequentially.

2. **Grep-First Strategy**: Always start with `Grep files_with_matches` to get file counts, then decide if `content` mode is needed. This saves 50-70% on tokens compared to reading content immediately.

3. **Pattern Libraries**: Maintain `.claude-library/patterns/` directory with reusable architectural patterns. Reference existing patterns rather than researching from scratch each time.

4. **Interface-Focused Specs**: Document what components do (interfaces, contracts) rather than how they do it (algorithms, implementation). A 50-line interface spec is worth more than a 500-line implementation guide.

5. **Validation Loops**: After creating specs, use targeted `Grep` queries to validate assumptions. Example: After specifying async patterns, `Grep "async def|await"` to confirm codebase already uses async/await consistently.

---

*Tool Usage Guide v1.0 - Architect Agent*
*Part of Claude Agent Framework - Best Practices Integration*
