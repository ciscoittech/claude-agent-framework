# /build-feature - Self-Building Feature Development

**Purpose**: Use Claude Agent Framework to build framework features using framework's own agents
**Agent**: framework-feature-builder (coordinator)
**Type**: Meta-Building Command
**Frequency**: On-demand when adding features

---

## Command Usage

```bash
/build-feature <feature_name> [--description "Feature description"]
```

**Arguments**:
- `feature_name` (required): Name of the feature to build
- `--description` (optional): Detailed feature description

**Examples**:
```bash
/build-feature task-validation
/build-feature performance-optimizer --description "Optimize agent execution speed"
/build-feature context-caching --description "Add context caching for faster loading"
```

---

## What This Command Does

This is **the most important command** in the framework - it proves the framework works by using itself to build itself.

**The Meta-Building Process**:
1. **Research Phase**: framework-research-specialist fetches relevant Claude Code patterns
2. **Design Phase**: framework-architect designs feature following best practices
3. **Implementation Phase**: framework-senior-engineer implements (parallel with review prep)
4. **Validation Phase**: framework-validation-engineer tests + framework-best-practice-auditor audits
5. **Documentation Phase**: documentation-specialist creates usage docs
6. **Integration**: Validate all quality gates, report results

**Key Innovation**: Uses Task tool to coordinate agents who build the feature. If this works, it proves the framework can build anything.

---

## Workflow

### Execution Pattern

**Mixed** - Parallel where possible, sequential when dependencies exist

### Phase 1: Research (30s)

**Agent**: framework-research-specialist
**Execution**: Single agent

```markdown
Task:
  description: "Research Claude Code patterns for [feature_name]"
  prompt: |
    Research official Claude Code documentation for: {feature_name}

    Fetch from relevant sources:
    - Best practices article
    - Sub-agents guide
    - Hooks guide
    - MCP guide
    - Documentation map

    Extract:
    - Key patterns relevant to {feature_name}
    - Implementation examples
    - Best practices to follow
    - Performance considerations
    - Integration points

    Output: Research summary with:
    - Relevant patterns found
    - Code examples from official docs
    - Recommended approach
    - Performance targets
  subagent_type: "framework-research-specialist"
```

### Phase 2: Design (30s)

**Agent**: framework-architect
**Execution**: Sequential (needs research results)

```markdown
Task:
  description: "Design [feature_name] following best practices"
  prompt: |
    Design feature: {feature_name}
    Description: {user_description}

    Research findings:
    {research_results}

    Design Requirements:
    - Follow SIMPLICITY_ENFORCEMENT.md principles
    - Reference claude-code-best-practices.md patterns
    - Start minimal, add complexity only if needed
    - Include integration points with existing framework
    - Define success criteria
    - Set performance targets

    Output complete design document with:
    - Architecture overview
    - File structure (which files to create/modify)
    - Agent definitions (if new agents needed)
    - Integration plan (how it fits in framework)
    - Success criteria (how to validate it works)
    - Performance targets (speed, token usage)
  subagent_type: "framework-architect"
```

### Phase 3: Implementation (60s)

**Agents**: framework-senior-engineer + framework-code-reviewer
**Execution**: Parallel

```markdown
Task (Parallel - 2 agents):

1. Implementation:
  description: "Implement [feature_name]"
  prompt: |
    Implement feature: {feature_name}

    Design:
    {design_document}

    Requirements:
    - Follow framework coding standards
    - Write clean, well-documented code
    - Include inline examples where helpful
    - Meet performance targets from design
    - Integrate with existing framework patterns

    Files to create/modify:
    {file_list_from_design}

    Output:
    - All implementation files created/modified
    - Code follows framework patterns
    - Performance targets considered
  subagent_type: "framework-senior-engineer"

2. Review Preparation:
  description: "Prepare review criteria for [feature_name]"
  prompt: |
    Create review checklist for: {feature_name}

    Design: {design_document}

    Prepare:
    - Compliance checklist (best practices to verify)
    - Test scenarios (what to test)
    - Performance criteria (targets to meet)
    - Integration points (what to check)

    Output: Complete review checklist for validation phase
  subagent_type: "framework-code-reviewer"
```

### Phase 4: Validation (30s)

**Agents**: framework-validation-engineer + framework-best-practice-auditor
**Execution**: Sequential (needs implementation)

```markdown
Task (Sequential after implementation):

1. Testing:
  description: "Test [feature_name] implementation"
  prompt: |
    Test feature: {feature_name}

    Implementation:
    {implementation_files}

    Review criteria:
    {review_checklist}

    Run these tests:
    - Unit tests for new functionality
    - Integration tests with existing framework
    - Performance tests against targets
    - Edge case validation

    Output:
    - Test results (pass/fail for each test)
    - Coverage report
    - Performance metrics
    - Issues found (if any)
  subagent_type: "framework-validation-engineer"

2. Compliance Audit:
  description: "Audit [feature_name] compliance"
  prompt: |
    Audit feature: {feature_name}

    Implementation: {implementation_files}
    Test results: {test_results}

    Check against:
    - claude-code-best-practices.md
    - claude-code-subagents.md (if agents involved)
    - framework-architecture.md
    - SIMPLICITY_ENFORCEMENT.md

    Audit categories:
    - Tool usage patterns
    - Workflow structure
    - Context optimization
    - Documentation quality
    - Performance compliance

    Output:
    - Compliance score (0-100%)
    - Gaps identified
    - Recommendations
    - GO/NO-GO decision
  subagent_type: "framework-best-practice-auditor"
```

### Phase 5: Documentation (20s)

**Agent**: documentation-specialist
**Execution**: Parallel with validation (if tests passing)

```markdown
Task:
  description: "Document [feature_name]"
  prompt: |
    Document feature: {feature_name}

    Design: {design_document}
    Implementation: {implementation_files}

    Create comprehensive documentation:
    - Usage guide (how to use the feature)
    - API documentation (if applicable)
    - Integration examples (code samples)
    - Performance notes (targets and tips)
    - Troubleshooting (common issues)

    Follow framework documentation style.

    Output:
    - Complete documentation file(s)
    - Usage examples
    - Integration guide
  subagent_type: "documentation-specialist"
```

### Phase 6: Integration & Report

**Coordinator**: framework-feature-builder
**Execution**: Synthesize all results

```markdown
Final validation:
- All phases completed
- Tests passing (>90%)
- Compliance acceptable (>85%)
- Documentation complete
- Performance targets met

Quality Gates:
✅ Research completed
✅ Design approved
✅ Implementation clean
✅ Tests passing: [X]%
✅ Compliance: [X]%
✅ Documentation complete
✅ Performance: Meets targets

Decision: READY FOR MERGE / NEEDS WORK
```

---

## Expected Output

### Successful Build

```markdown
🔨 Building feature: task-validation

Phase 1: Research ✅ (12.3s, 3,421 tokens, $0.02)
├─ Fetched Claude Code validation patterns
├─ Identified 3 relevant best practices
└─ Found 2 SDK examples

Phase 2: Design ✅ (18.7s, 5,234 tokens, $0.03)
├─ Architecture: Validation hooks + DB expectations
├─ Integration: PostToolUse hook, task_expectations table
├─ Files: 2 new (validate_task.py, schema update)
└─ Complexity: MINIMAL (follows simplicity first)

Phase 3: Implementation ✅ (35.2s, 11,876 tokens, $0.06)
├─ Engineer: Created validate_task.py hook
├─ Engineer: Updated schema.sql with expectations
├─ Reviewer: Prepared compliance checklist
└─ Files: 2 created, 1 modified

Phase 4: Validation ✅ (22.1s, 6,543 tokens, $0.04)
├─ Tests: 13/13 passing ✅
├─ Performance: <200ms overhead ✅
├─ Compliance: 95% (Excellent) ✅
└─ Decision: GO for merge

Phase 5: Documentation ✅ (15.4s, 4,123 tokens, $0.02)
├─ Usage guide created
├─ 3 integration examples
└─ Troubleshooting section

─────────────────────────────────────────────────
Build Complete! ✅

Summary:
├─ Total time: 103.7s (1.7 min)
├─ Total tokens: 31,197
├─ Total cost: $0.17
├─ Quality: 95% compliance
└─ Status: READY FOR MERGE

Files Created/Modified:
├─ .claude-library/observability/scripts/validate_task.py (new)
├─ .claude-library/observability/schema.sql (modified)
└─ .claude-library/observability/VALIDATION.md (new)

Observability Tracking:
├─ Execution ID: 42
├─ Sub-agents launched: 6
├─ All tracked in .claude-metrics/observability.db
└─ Query: python3 .claude-library/observability/obs.py execution 42

Quality Gates: ✅ ALL PASSED
├─ Tests: 13/13 (100%)
├─ Compliance: 95% (A grade)
├─ Performance: Meets targets
└─ Documentation: Complete

Next Steps:
1. Review implementation in listed files
2. Run /audit-practices for full framework check
3. Merge if approved
4. Update REGISTRY.json if needed

Ready for merge? [Y/N]
```

### Build with Issues

```markdown
🔨 Building feature: complex-optimizer

Phase 1: Research ✅ (15s)
Phase 2: Design ✅ (22s)
Phase 3: Implementation ⚠️ (45s)
├─ Implementation complete
└─ Reviewer flagged 2 concerns

Phase 4: Validation ❌ (28s)
├─ Tests: 8/12 passing (66%) ❌
├─ Performance: Exceeds 500ms target ❌
├─ Compliance: 72% (Acceptable, below 85% target) ⚠️
└─ Decision: NO-GO

─────────────────────────────────────────────────
Build Incomplete ⚠️

Issues Found:
1. [CRITICAL] 4 tests failing in validation
   - Location: test_optimizer.py
   - Impact: Core functionality broken
   - Fix: Debug test failures

2. [HIGH] Performance exceeds target (650ms vs 500ms)
   - Location: optimize_context.py
   - Impact: Slows framework
   - Fix: Add caching or optimize algorithm

3. [MEDIUM] Compliance below threshold (72% vs 85%)
   - Issues: Missing error handling, no examples
   - Fix: Add error handling, include usage examples

Recommendations:
1. Fix failing tests first
2. Profile and optimize performance
3. Add error handling and examples
4. Re-run /build-feature after fixes

Status: BLOCKED - Cannot merge
Action: Fix issues and retry build
```

---

## Performance Targets

Per phase:
- **Research Phase**: <30s
- **Design Phase**: <30s
- **Implementation Phase**: <60s
- **Validation Phase**: <30s
- **Documentation Phase**: <20s

**Total Feature Build**: <3 minutes (170s)

---

## Quality Criteria

Build succeeds when:
- ✅ All 5 phases complete
- ✅ Tests passing >90%
- ✅ Compliance score >85%
- ✅ Performance targets met
- ✅ Documentation complete
- ✅ Quality gates all green

Build is blocked when:
- ❌ Tests <90% passing
- ❌ Compliance <85%
- ❌ Performance exceeds targets significantly
- ❌ Critical issues found

---

## Integration with Observability

**Every build is fully tracked**:

```sql
-- View the feature build
SELECT * FROM v_recent_executions
WHERE agent_name = 'framework-feature-builder'
ORDER BY started_at DESC
LIMIT 1;

-- See all sub-agents launched
SELECT * FROM v_agent_hierarchy
WHERE root_agent = 'framework-feature-builder';

-- Check validation results
SELECT * FROM validations
WHERE execution_id = (
    SELECT id FROM executions
    WHERE agent_name = 'framework-feature-builder'
    ORDER BY started_at DESC LIMIT 1
);
```

**CLI queries**:
```bash
# View recent builds
python3 .claude-library/observability/obs.py recent

# Deep dive into specific build
python3 .claude-library/observability/obs.py execution <id>

# See all framework-feature-builder performance
python3 .claude-library/observability/obs.py agents
```

---

## Integration with Other Commands

### Before Building
```bash
# Ensure latest best practices
/update-docs

# Check current compliance
/audit-practices
```

### After Building
```bash
# Verify framework still compliant
/audit-practices

# If issues found, improve
/self-improve
```

### Complete Workflow
```bash
# 1. Get latest patterns
/update-docs

# 2. Build new feature
/build-feature my-feature

# 3. Validate compliance
/audit-practices

# 4. Commit if green
git add .
git commit -m "feat: add my-feature via self-building"
```

---

## Why This Command Matters

**This is the proof that the framework works.**

If the Claude Agent Framework can:
1. Use its own agents (via Task tool)
2. Follow its own patterns (via context files)
3. Validate its own quality (via auditor)
4. Track its own progress (via observability)
5. Build new features for itself

Then it proves the framework can build **anything**.

**The Ultimate Test**: Can the framework improve itself? If yes, users can trust it to improve their projects.

---

## Example: Building task-validation Feature

**Input**: `/build-feature task-validation --description "Add validation layer for task execution"`

**What Happens**:
1. framework-feature-builder reads the request
2. Launches framework-research-specialist to research validation patterns
3. Launches framework-architect to design the validation system
4. Launches framework-senior-engineer + framework-code-reviewer in parallel
5. Engineer creates validate_task.py hook and updates schema
6. Launches framework-validation-engineer to test it
7. Launches framework-best-practice-auditor to check compliance
8. Launches documentation-specialist to document usage
9. Validates all quality gates
10. Reports: READY FOR MERGE

**Result**: New feature built entirely by framework's own agents, following its own best practices, tracked by its own observability system.

**Proof**: Framework can build itself = Framework can build anything.

---

## Error Handling

### If Agent Launch Fails
```markdown
❌ Phase 2 Failed: Could not launch framework-architect

Error: Agent not found in REGISTRY.json

Resolution:
1. Check REGISTRY.json has framework-architect entry
2. Verify agent file exists at path
3. Re-run /build-feature after fix
```

### If Quality Gates Fail
```markdown
⚠️ Quality Gate Failure

Gate: Compliance Score
├─ Required: >85%
├─ Actual: 72%
└─ Status: BLOCKED

Violations:
1. Missing error handling in 3 functions
2. No usage examples in documentation
3. Performance target exceeded by 30%

Action: Fix violations and re-run build
```

### If Build Times Out
```markdown
⏱️ Build Timeout

Phase: Implementation
├─ Started: 10:15:30
├─ Timeout: 10:16:30 (60s limit)
└─ Status: CANCELLED

Possible causes:
1. Feature too complex for single build
2. Agent stuck on difficult decision
3. Network issues fetching docs

Recommendations:
1. Break feature into smaller parts
2. Provide more detailed description
3. Check agent performance logs
```

---

## Tips for Success

### Feature Naming
- **Good**: `task-validation`, `context-caching`, `performance-optimizer`
- **Bad**: `feature1`, `new-thing`, `fix`

### Descriptions
- **Good**: "Add validation layer to verify task outputs match expected patterns"
- **Bad**: "Make it better"

### Scope
- **Good**: Single, well-defined feature
- **Bad**: "Rewrite entire framework"

### Complexity
- Start simple, let framework decide complexity
- Trust SIMPLICITY_ENFORCEMENT.md principles
- Let agents suggest if more complexity needed

---

## Observability Metrics

Tracked for every build:
- Total duration (target: <3 min)
- Tokens used (all phases)
- Cost in USD
- Number of sub-agents launched
- Quality gate pass/fail
- Compliance score
- Test pass rate
- Performance vs targets

**Query with**:
```bash
python3 .claude-library/observability/obs.py agents
# Look for: framework-feature-builder stats
```

---

**Command Version**: 1.0.0
**Agent**: framework-feature-builder
**Performance Baseline**: <3 minutes per feature
**Last Updated**: October 4, 2025

**This command is the heart of the self-building system** ❤️
