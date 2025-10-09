# Quick Action Plan: Implement Writing Tools Best Practices

**Goal**: Improve framework tool usage from 40% aligned → 95% aligned
**Expected Gain**: +125% improvement (validated by tests)
**Total Time**: Start seeing results in 1 hour, complete in 2-3 weeks

---

## 🚀 Start Here (Next 2 Hours)

### Action 1: Tool Description Template (1 hour)

```bash
# Open AGENT_PATTERNS.md and add the tool description template
# Location: After existing patterns, before the end

# Template is in: WRITING_TOOLS_IMPROVEMENTS.md (section 1)
```

**What to add**:
- Standard tool description format
- "New team member" writing style
- Parameter documentation template
- Example usage blocks
- Common mistakes section

**Test it works**: Use template to document one tool, see if it's clearer

---

### Action 2: Add Token Efficiency to One Agent (1 hour)

Pick the most-used agent (probably `framework-senior-engineer.md`):

```bash
# Open .claude-library/agents/core/framework-senior-engineer.md
# Find the "Available Tools" section
# Add the token efficiency guidelines after it
```

**What to add** (from WRITING_TOOLS_IMPROVEMENTS.md section 2):
- Token Efficiency Guidelines section
- Default limits for tool results
- Efficiency patterns (good vs bad examples)
- Response format standards

**Test it works**: Run a task with this agent, observe if responses are more concise

---

## ⚡ Quick Wins (Next 2 Days - 4 hours)

### Day 1: Core Agent Updates (2 hours)

Add token efficiency sections to:
- [ ] `framework-system-architect.md`
- [ ] `framework-code-reviewer.md`
- [ ] `framework-validation-engineer.md`

**Batch approach**: Copy template, customize per agent role

---

### Day 2: Output Format Guide (2 hours)

1. Create `.claude-library/patterns/output-format-guide.md`
2. Add standard response structures
3. Reference it from all agent definitions

**Benefits**:
- Consistent agent outputs
- Better user experience
- Easier to parse agent responses

---

## 📈 High Impact Changes (Week 2 - 6 hours)

### Rewrite Tool Sections (6 hours total, 2 hours per agent)

**Target agents** (in priority order):
1. `framework-senior-engineer.md` - Most critical, most used
2. `framework-system-architect.md` - Sets architectural patterns
3. `framework-research-specialist.md` - Complex tool usage

**For each agent**:
- [ ] Rewrite "Available Tools" section
- [ ] Add detailed tool descriptions
- [ ] Include examples for each tool
- [ ] Document common mistakes
- [ ] Add tool selection decision tree

**Template**: See WRITING_TOOLS_IMPROVEMENTS.md "Before/After Agent Definition"

---

## 🎯 Validation (After Each Phase)

### Quick Check
```bash
# Run the test suite
pytest test_best_practice_tool_writing.py -v

# Look for improvements in:
# - tool_description_clarity: Should increase toward 100
# - efficiency_guidance_per_agent: Should be 4-5 per agent
```

### Manual Check
1. Give an agent a task
2. Observe tool selection
3. Check response format
4. Verify token usage

**Success indicators**:
- Agent picks right tool first try
- Response is clear and structured
- No unnecessary verbose output
- File references include line numbers

---

## 📊 Expected Progress

### After 2 Hours (Quick Start)
- ✅ Template created and usable
- ✅ 1 agent improved
- ✅ Visible improvement in that agent's output

### After 2 Days (Quick Wins)
- ✅ 3 core agents improved
- ✅ Output format standardized
- ✅ Test shows +30-50% improvement

### After 1 Week
- ✅ All core agents updated
- ✅ Tool descriptions clear
- ✅ Token efficiency built in
- ✅ Test shows +70-90% improvement

### After 2-3 Weeks (Complete)
- ✅ All agents updated
- ✅ REGISTRY.json reorganized
- ✅ Agent-specific guides created
- ✅ Test shows +125% improvement ✅

---

## 🎓 Learning Check

After implementing, you should see:

**Agent Behavior**:
- Agents explain which tool they're using and why
- Fewer "oops, wrong tool" moments
- More efficient searches (narrow first, expand if needed)
- Structured, scannable output

**Performance**:
- 15-20% token reduction
- Faster task completion
- Less back-and-forth clarification
- Higher first-try success rate

**Developer Experience**:
- Easier to debug agent behavior
- Clear output format makes parsing easier
- File references with line numbers
- Actionable error messages

---

## 🚨 Common Pitfalls to Avoid

### ❌ Don't: Rewrite all agents at once
**Instead**: Start with 1 agent, validate, then scale

### ❌ Don't: Copy-paste without customizing
**Instead**: Tailor tool descriptions to each agent's role

### ❌ Don't: Add complexity for its own sake
**Instead**: Follow simplicity principle - only add what helps

### ❌ Don't: Skip testing between changes
**Instead**: Test after each agent update to track progress

---

## 📝 Checklist for Each Agent Update

When updating an agent, ensure:

- [ ] Tool descriptions use "new team member" language
- [ ] Each tool has clear "When to Use" section
- [ ] Parameters are documented with examples
- [ ] Token efficiency guidance is present
- [ ] Output format references standard guide
- [ ] Common mistakes are documented
- [ ] Decision tree or workflow shows tool selection logic
- [ ] Examples show actual usage patterns

---

## 🔄 Iterative Approach

**Don't wait for perfection**. Use this cycle:

```
1. Pick 1 agent
   ↓
2. Update tools section (1-2 hours)
   ↓
3. Test with real task
   ↓
4. Observe behavior
   ↓
5. Refine based on observations
   ↓
6. Move to next agent
```

**Each cycle should take ~2-3 hours**

After 5 cycles (1 week), you'll have 5 improved agents and clear patterns for the rest.

---

## 📂 Files Quick Reference

**Templates/Guides** (use these):
- `WRITING_TOOLS_IMPROVEMENTS.md` - Complete improvement guide
- `test_best_practice_tool_writing.py` - Validation tests

**Files to Update** (in order):
1. `AGENT_PATTERNS.md` - Add template
2. `.claude-library/agents/core/framework-senior-engineer.md`
3. `.claude-library/agents/core/framework-system-architect.md`
4. `.claude-library/agents/core/framework-code-reviewer.md`
5. `.claude-library/patterns/output-format-guide.md` (NEW)
6. All other specialized agents
7. `.claude-library/REGISTRY.json` - Tool organization

---

## 🎉 Done Criteria

You'll know you're done when:

1. **Test passes at 95%+**: `pytest test_best_practice_tool_writing.py -v`
2. **Agents self-document**: They explain tool choices clearly
3. **Token usage drops**: 15-20% reduction on similar tasks
4. **You can onboard someone**: New person can understand tool usage from agent definitions

---

## 💡 Pro Tips

1. **Start with the agent you use most** - you'll see immediate benefit
2. **Keep a before/after example** - helps see progress
3. **Test with real tasks** - not just the test suite
4. **Update gradually** - don't block on perfection
5. **Document learnings** - what worked, what didn't

---

## Next Steps

```bash
# Right now (5 minutes):
1. Open AGENT_PATTERNS.md
2. Copy tool description template from WRITING_TOOLS_IMPROVEMENTS.md
3. Paste it into a new section

# Today (1 hour):
1. Pick your most-used agent
2. Add token efficiency guidelines
3. Run a test task, observe improvement

# This week (6 hours):
1. Update 3 core agents
2. Create output format guide
3. Run validation tests

# Done! Framework is now 95% aligned with best practices
```

---

*Quick Action Plan v1.0*
*Get results in 1 hour, complete in 2-3 weeks*
*Part of Claude Agent Framework - Writing Tools Integration*
