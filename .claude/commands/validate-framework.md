# /validate-framework Command

**Purpose**: Validate framework improvements from applied best practices through comprehensive testing

**Usage**: `/validate-framework <best-practice-name>`

**Example**: `/validate-framework tool-writing`

---

## Workflow Overview

This command runs comprehensive tests to validate that a best practice improvement:
1. Delivers measurable benefits
2. Maintains simplicity principle
3. Passes all test scenarios (Easy, Medium, Hard)
4. Is ready for integration into the framework

```
Stage 1: Run Test Suite
    ↓
Stage 2: Compare Metrics
    ↓
Stage 3: Check Simplicity Compliance
    ↓
Stage 4: Generate Integration Recommendation
```

---

## Command Execution

When user invokes `/validate-framework <best-practice-name>`:

### Stage 1: Execute Test Suite

Run the best practice test file:

```bash
pytest test_best_practice_{best-practice-name}.py -v --tb=short
```

The test suite will:
- Run baseline tests (current framework)
- Run improved tests (with best practice applied)
- Measure metrics for comparison
- Track test pass/fail status

### Stage 2: Analyze Results

Extract key findings from test output:

```markdown
- **Pass Rate**: X% (Y/Z tests passed)
- **Average Improvement**: +X.X%
- **Key Metrics**:
  - [Metric name]: Baseline → Improved (+X%)
  - [Metric name]: Baseline → Improved (+X%)

- **Test Failures**: [None or list specific failures]
```

### Stage 3: Simplicity Assessment

Check that improvements don't violate simplicity constraints:

```markdown
**File Count Impact**:
- Before: N files
- After: M files
- Change: +/-X files [✅ Acceptable / ⚠️ Review]

**Context Size Impact**:
- Before: X KB auto-loaded
- After: Y KB auto-loaded
- Change: +/-Z KB [✅ Acceptable / ⚠️ Review]

**Complexity Score**:
- Before: X/10
- After: Y/10
- [✅ Maintained simplicity / ⚠️ Added complexity]
```

### Stage 4: Generate Recommendation

Produce clear integration verdict:

```markdown
# Validation Report: {Best Practice Name}

## Executive Summary

**Verdict**: ✅ APPROVED / ⚠️ REVIEW / ❌ REJECTED

**Reasoning**:
- Test pass rate: X%
- Average improvement: +X%
- Simplicity maintained: YES/NO
- Ready for integration: YES/NO

## Detailed Findings

### Test Results
[Breakdown of all test scenarios]

### Performance Gains
[Specific improvements with percentages]

### Simplicity Impact
[Assessment of complexity changes]

## Recommendation

[If APPROVED]
✅ **RECOMMENDED FOR INTEGRATION**

This best practice delivers significant improvements while maintaining framework simplicity.

**Next Steps**:
1. Merge experimental changes to main framework files
2. Update CHANGELOG.md with improvements
3. Archive experiment in experiments/archive/
4. Run full framework test suite to verify compatibility

**Files to Update**:
- [List specific files]

**Expected Impact**:
- [Specific improvement metric]
- [Specific improvement metric]

---

[If REVIEW]
⚠️ **NEEDS REVIEW**

This best practice shows promise but requires attention to:
- [Issue 1]
- [Issue 2]

**Recommendations**:
1. [Specific action to address issue]
2. [Specific action to address issue]

Re-run validation after addressing concerns.

---

[If REJECTED]
❌ **NOT RECOMMENDED**

This best practice does not meet integration criteria:
- [Reason 1]
- [Reason 2]

**Alternatives**:
- [Suggestion 1]
- [Suggestion 2]
```

---

## Implementation Notes

### Test File Location

The command expects test files to follow naming convention:
```
test_best_practice_{best-practice-name}.py
```

Examples:
- `test_best_practice_tool_writing.py`
- `test_best_practice_context_protocol.py`
- `test_best_practice_error_handling.py`

### Integration Criteria

A best practice is **APPROVED** when:
- ✅ Pass rate ≥ 90%
- ✅ Average improvement ≥ 10%
- ✅ Simplicity maintained (no file explosion, context under control)
- ✅ No critical test failures

A best practice requires **REVIEW** when:
- ⚠️ Pass rate 70-89%
- ⚠️ Improvement 5-9%
- ⚠️ Minor simplicity concerns
- ⚠️ Some test failures but not critical

A best practice is **REJECTED** when:
- ❌ Pass rate < 70%
- ❌ Improvement < 5%
- ❌ Violates simplicity principle
- ❌ Critical test failures

### Error Handling

**If test file doesn't exist**:
```
❌ Test file not found: test_best_practice_{name}.py

Did you mean:
- test_best_practice_tool_writing.py
- test_best_practice_template.py

To create a new test:
1. Copy test_best_practice_template.py
2. Rename to test_best_practice_{name}.py
3. Customize test scenarios
4. Run: /validate-framework {name}
```

**If tests fail to run**:
```
❌ Test execution failed

Error: [error message]

Troubleshooting:
1. Check pytest is installed: pip install pytest
2. Verify test file syntax is valid
3. Check experiment directory exists: .claude-library/experiments/{name}/
4. Review test output for specific errors
```

---

## Output Locations

Validation results are saved to:
```
.claude-library/experiments/{best-practice-name}/
├── gap-analysis.md                  # From /ingest-best-practice
├── test-results/
│   └── report-{timestamp}.json     # Generated by test suite
└── validation-report.md             # Generated by this command
```

---

## Example Output

```
🧪 Running validation tests for: tool-writing

📊 Test Execution
==================

Running: pytest test_best_practice_tool_writing.py -v

test_tool_namespacing ... ✅ PASSED
test_token_efficiency_guidance ... ✅ PASSED
test_context_quality ... ✅ PASSED
test_prompt_clarity ... ✅ PASSED
test_tool_consolidation ... ✅ PASSED

Test Results: 5/5 passed (100%)

📈 Performance Analysis
========================

Metrics Comparison:
- tool_namespacing_ratio: 15.0% → 60.0% (+300% ✅)
- efficiency_guidance_per_agent: 1.5 → 4.0 (+167% ✅)
- context_quality_score: 30 → 80 (+167% ✅)
- tool_description_clarity: 25 → 100 (+300% ✅)
- tool_count: 12 → 3 (-75% ✅ Consolidation)

Overall Improvement: +171.8%

🎯 Simplicity Check
====================

File Count: 0 new files (✅ No bloat)
Context Size: No change (✅ Maintained)
Complexity: Improved (✅ Better organized)

✅ VERDICT: APPROVED FOR INTEGRATION

This best practice delivers exceptional improvements:
- 171.8% average metric improvement
- 100% test pass rate
- Zero complexity increase
- Clear implementation path

Next Steps:
1. Update REGISTRY.json with tool namespacing guide
2. Rewrite agent tool descriptions using template
3. Add token efficiency patterns to all agents
4. Run: pytest (full suite) to verify compatibility

📄 Full report: .claude-library/experiments/tool-writing/validation-report.md
```

---

## Related Commands

- `/ingest-best-practice <url>` - Import new best practice before validation
- `/feature` - Implement approved improvements

---

## Maintenance

When updating this command:
- Keep integration criteria consistent
- Ensure all output paths are correct
- Update example output if report format changes
- Maintain clear success/failure messaging

---

*Command Version 1.0*
*Part of Claude Agent Framework - Best Practices Integration System*
