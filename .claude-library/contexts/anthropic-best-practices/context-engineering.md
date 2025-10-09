# Effective Context Engineering for AI Agents - Anthropic Best Practices

**Source**: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
**Date Ingested**: 2025-10-09
**Framework Version**: 1.1
**Relevance**: Context management, system prompts, agent design, performance optimization

---

## Core Philosophy

> "As models become more capable, the challenge isn't just crafting the perfect prompt—it's thoughtfully curating what information enters the model's limited attention budget at each step."

Context is a **precious, finite resource** with **diminishing marginal returns**. The goal is finding the **smallest possible set of high-signal tokens** that maximize the likelihood of desired outcomes.

---

## Key Principles

### 1. Context as a Finite Resource

**Best Practice**: Treat every token in context as valuable real estate

**Core Concepts**:
- Context windows have **diminishing marginal returns** - more isn't always better
- Information overload reduces agent performance
- Quality over quantity in context selection
- Attention budget is limited - spend it wisely

**Analogy**:
> Think of context like RAM in a computer - you have a fixed amount, and filling it with irrelevant data slows everything down

**Framework Application**:
- Audit current auto-loaded context size
- Measure impact of each context file on performance
- Remove low-signal context aggressively
- Implement context budgeting (token limits per component)

**Example**:
```markdown
❌ Bad: Load 50KB of docs "just in case"
✅ Good: Load 5KB of essential docs, 45KB on-demand

❌ Bad: Include entire codebase context
✅ Good: Include only files relevant to current task
```

---

### 2. System Prompt Design

**Best Practice**: Use simple, direct language at the right altitude

**Guidelines**:
- **Simple Language**: Avoid jargon, complex instructions
- **Right Altitude**: Not too abstract, not too detailed
- **Clear Structure**: Use XML or Markdown sections
- **Minimal Start**: Begin simple, add complexity only when needed

**Anti-Patterns**:
- ❌ Overly complex nested instructions
- ❌ Vague guidance like "be creative"
- ❌ Redundant or contradictory rules
- ❌ Kitchen-sink approach (everything at once)

**Good Patterns**:
- ✅ Direct imperatives: "Do X when Y"
- ✅ Organized sections: Responsibilities, Boundaries, Tools
- ✅ Concrete examples over abstract rules
- ✅ Progressive disclosure: Start minimal, expand as proven necessary

**Framework Application**:
- Review all agent definitions for simplicity
- Remove vague instructions
- Organize with clear XML/Markdown sections
- Test minimal versions before adding complexity

**Example**:
```markdown
❌ Bad Prompt:
"You should try to be helpful and consider various aspects of the
problem space while maintaining awareness of potential edge cases..."

✅ Good Prompt:
"You are a database specialist. Your role:
1. Analyze schema issues
2. Suggest optimizations
3. Explain trade-offs clearly"
```

---

### 3. Tool Selection and Design

**Best Practice**: Create minimal, self-contained, extremely clear tools

**Guidelines**:
- **Self-Contained**: Each tool does one thing completely
- **Robust to Error**: Handle edge cases gracefully
- **Extremely Clear**: No ambiguity in purpose or parameters
- **Minimal Overlap**: Avoid redundant tools
- **Descriptive Parameters**: Names reveal meaning

**Tool Curation Principle**:
> "Minimal viable set of tools" - fewest tools that enable the task

**Framework Application**:
- Audit tool lists in REGISTRY.json
- Remove overlapping tools
- Consolidate similar functionality
- Rewrite tool descriptions for absolute clarity
- Test tool understanding with edge cases

**Example**:
```markdown
❌ Bad: 10 tools for file operations
   - read_file()
   - read_file_partial()
   - read_file_with_encoding()
   - read_file_async()
   ...

✅ Good: 1 comprehensive tool
   - read_file(path, encoding="utf-8", lines=None, offset=0)
```

---

### 4. Context Retrieval Strategies

**Best Practice**: Implement just-in-time, progressive context loading

**Strategies**:

**A. Just-In-Time Loading**
- Load context only when needed for current task
- Don't preload "might need" information
- Use task triggers to determine what to load

**B. Metadata-Guided Retrieval**
- Use file system structure as signals
- Leverage naming conventions
- Check file timestamps, sizes
- Use git history for relevance

**C. Progressive Disclosure**
- Start with high-level overview
- Let agents request deeper detail
- Incremental context expansion
- "Zoom in" approach vs "dump everything"

**Framework Application**:
- Remove auto-loaded contexts where possible
- Implement on-demand context loading
- Create context hierarchies (summary → detail)
- Use agent triggers to determine context needs

**Example**:
```markdown
❌ Bad: Auto-load all contexts at startup
   - project.md (50KB)
   - database.md (30KB)
   - api.md (40KB)
   - patterns.md (25KB)
   Total: 145KB always loaded

✅ Good: Load based on task
   Task: "Fix database query"
   - Load: project.md (5KB summary section only)
   - Load: database.md (30KB - relevant)
   - Skip: api.md, patterns.md
   Total: 35KB task-specific
```

---

### 5. Long-Horizon Task Techniques

**Best Practice**: Use compaction, note-taking, and multi-agent patterns for extended tasks

**Techniques**:

**A. Context Compaction**
- Periodically summarize conversation history
- Keep only essential information
- Compress verbose exchanges into key points
- Prevents context window overflow

**B. Structured Note-Taking**
- Maintain notes outside context window
- Write to files agents can re-read
- Create persistent memory across resets
- Use standard formats (markdown, JSON)

**C. Multi-Agent Architecture**
- Decompose complex tasks across multiple agents
- Each agent has fresh context window
- Pass only essential information between agents
- Enables longer effective task duration

**D. Persistent Memory**
- Store findings in files/database
- Re-load only relevant findings when needed
- Create "memory checkpoints"
- Enable context-independent continuation

**Framework Application**:
- Add compaction patterns to long-running agents
- Implement note-taking workflows
- Use Task tool for context-fresh sub-agents
- Create memory patterns in contexts/

**Example**:
```markdown
Long Task: "Refactor entire authentication system"

❌ Bad: Single agent, context explodes
   - Load all auth code at once
   - Try to keep everything in memory
   - Context window fills up
   - Performance degrades

✅ Good: Multi-agent with note-taking
   Agent 1: Analyze current system → write analysis.md
   Agent 2: Read analysis.md → design new system → write design.md
   Agent 3: Read design.md → implement module 1 → write progress.md
   Agent 4: Read progress.md → implement module 2
   ...
   Each agent: Fresh context, focused task
```

---

## Implementation Checklist

Apply these best practices to the framework:

### Context Budget Management
- [ ] Measure current auto-loaded context size
- [ ] Set target: < 10KB auto-loaded (framework currently ~8KB ✅)
- [ ] Create context budget per agent type
- [ ] Monitor context usage in observability

### System Prompt Optimization
- [ ] Audit all agent prompts for simplicity
- [ ] Remove vague instructions ("be creative", "consider all aspects")
- [ ] Reorganize with clear XML/Markdown sections
- [ ] Test minimal versions before expanding

### Tool Minimization
- [ ] List all tools available to each agent
- [ ] Identify overlapping functionality
- [ ] Consolidate redundant tools
- [ ] Rewrite tool descriptions for clarity
- [ ] Set "minimal viable toolset" per agent

### Just-In-Time Loading
- [ ] Identify currently auto-loaded contexts
- [ ] Mark which are truly essential
- [ ] Move non-essential to on-demand loading
- [ ] Create context loading triggers based on task keywords

### Long-Horizon Patterns
- [ ] Add compaction examples to agent definitions
- [ ] Create note-taking workflow patterns
- [ ] Document multi-agent decomposition strategies
- [ ] Implement memory checkpoint pattern

---

## Metrics for Success

**Context Efficiency**:
- Auto-loaded context size: Target < 10KB (currently 8KB ✅)
- On-demand context hit rate: > 80% relevant when loaded
- Unused context ratio: < 10% loaded but not referenced

**Performance Indicators**:
- Task completion rate: > 90%
- Average tokens per task: 20% reduction target
- Agent confusion rate: < 5% (wrong tool selection, etc.)
- Multi-step task success: > 85%

**Quality Metrics**:
- Prompt clarity score: All agents > 80/100
- Tool description comprehension: > 95% correct first try
- Context relevance score: > 90% of loaded context used

---

## Framework Current State Analysis

### Strengths (Already Aligned)
✅ **Minimal Auto-Loading**: Currently 8KB in `.claude/` folder
✅ **On-Demand Library**: `.claude-library/` loaded as needed
✅ **Clear Structure**: XML/Markdown sections in agent definitions
✅ **Progressive Complexity**: Simplicity enforcement built-in

### Opportunities (Gaps to Address)
⚠️ **Context Budgeting**: No explicit token limits per component
⚠️ **Just-In-Time Triggers**: Could be more sophisticated
⚠️ **Compaction Patterns**: Not explicitly documented in agents
⚠️ **Note-Taking Workflows**: Limited examples in patterns
⚠️ **Context Metrics**: Not tracked in observability

### Quick Wins
1. **Add context budgets to REGISTRY.json** (1 hour)
   - Define max_context_kb per agent type
   - Track in observability

2. **Document compaction patterns** (2 hours)
   - Add to AGENT_PATTERNS.md
   - Include examples in long-running agents

3. **Create note-taking workflow** (2 hours)
   - Add patterns/memory-checkpoints.md
   - Show multi-agent continuation examples

---

## Advanced Techniques

### 1. Attention Budget Allocation

Distribute context strategically:
```markdown
Total Budget: 200K tokens

Allocation:
- System Prompt: 10K (5%)
- Task Context: 50K (25%)
- Retrieved Knowledge: 100K (50%)
- Conversation History: 40K (20%)

Prioritization:
1. Current task description (essential)
2. Immediately relevant code/docs (high-signal)
3. Related patterns/examples (supporting)
4. General knowledge (on-demand only)
```

### 2. Context Decay Strategy

Older context becomes less relevant:
```markdown
Age-based weighting:
- Last 5 turns: 100% retained
- 5-10 turns ago: Summarize
- 10-20 turns ago: Key points only
- 20+ turns ago: Discard unless explicitly referenced
```

### 3. Hierarchical Context Structure

Layer information by abstraction level:
```markdown
Level 1 (Always loaded): Project identity (1KB)
Level 2 (Task-triggered): Domain context (5-10KB)
Level 3 (Agent-requested): Detailed docs (20-50KB)
Level 4 (On-demand search): Full codebase (100KB+)
```

---

## Related Framework Documents

- `SIMPLICITY_ENFORCEMENT.md` - Aligns with minimal context principle
- `CLAUDE_AGENT_FRAMEWORK.md` - Context Management section (lines 266-315)
- `AGENT_PATTERNS.md` - Progressive loading patterns
- `.claude-library/REGISTRY.json` - Context definitions and priorities

---

## Comparison to "Writing Tools for Agents"

Both best practices complement each other:

| Aspect | Writing Tools | Context Engineering |
|--------|---------------|---------------------|
| **Focus** | Tool design | Information curation |
| **Goal** | Clear, efficient tools | Minimal, high-signal context |
| **Metric** | Tool usage accuracy | Tokens per task |
| **Principle** | Simplify tools | Simplify context |

**Combined Impact**: Well-designed tools + curated context = maximum agent efficiency

---

## Next Steps

1. Run gap analysis comparing these practices to current framework
2. Identify high-impact improvements (focus on context budgeting)
3. Create experimental implementations
4. Test improvements with validation suite
5. Measure before/after metrics (tokens per task, success rate)
6. Integrate successful improvements into framework

---

## Test Scenarios

When validating this best practice:

**Easy Test**: Single agent with minimal context
- Baseline: Load all available context
- Improved: Load only task-relevant context
- Metric: Token reduction, task success rate

**Medium Test**: Multi-step task with progressive context
- Baseline: Front-load all context
- Improved: Just-in-time loading at each step
- Metric: Context efficiency, completion time

**Hard Test**: Long-horizon task requiring compaction
- Baseline: Single agent, context overflow
- Improved: Multi-agent with note-taking
- Metric: Task completion, final quality

---

*Best Practice Document v1.0*
*Part of Claude Agent Framework - Best Practices Integration System*
