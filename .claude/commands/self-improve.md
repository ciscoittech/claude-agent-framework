# /self-improve - Self-Optimization Using Observability Data

**Purpose**: Analyze observability data to identify and implement framework improvements
**Agent**: framework-feature-builder (coordinator)
**Type**: Meta-Improvement Command
**Frequency**: Weekly or when performance degrades

---

## Command Usage

```bash
/self-improve [--days 30] [--priority high|medium|low]
```

**Arguments**:
- `--days` (optional): Days of observability data to analyze (default: 30)
- `--priority` (optional): Only implement improvements at this priority level or higher

**Examples**:
```bash
/self-improve                           # Analyze last 30 days, implement top improvement
/self-improve --days 7                  # Analyze last week only
/self-improve --priority high           # Only critical improvements
```

---

## What This Command Does

This is **the ultimate self-building feature** - the framework analyzes its own performance data and improves itself.

**The Self-Improvement Process**:
1. **Analyze Observability Data**: Query `.claude-metrics/observability.db` for performance patterns
2. **Identify Improvements**: Find agents exceeding targets, workflows with failures, bottlenecks
3. **Prioritize Opportunities**: Rank by impact (frequency × severity × cost)
4. **Implement Top Fix**: Use `/build-feature` to implement the highest-priority improvement
5. **Measure Impact**: Compare before/after metrics
6. **Iterate**: Schedule next improvement cycle

**Key Innovation**: Framework uses its own observability data to identify weaknesses, then uses its own agents to fix them.

---

## Workflow

### Execution Pattern

**Sequential** - Each step depends on previous analysis

### Step 1: Data Collection (10s)

**Queries Observability Database**:
```python
import sys
sys.path.insert(0, '.claude-library/observability')
from db_helper import (
    get_agent_performance,
    get_daily_summary,
    get_recent_failed_executions,
    get_execution_details
)

# Collect metrics
agent_perf = get_agent_performance()  # All agents with stats
summary = get_daily_summary(days=days_param)  # Trend data
failures = get_recent_failed_executions(limit=50)  # Failed executions
```

**Data Collected**:
- Agent execution counts
- Average durations
- Success rates
- Token usage
- Costs
- Failure patterns
- Sub-agent relationships
- Validation results

### Step 2: Analysis (20s)

**Identify Optimization Opportunities**:

```python
# Agents exceeding performance targets
slow_agents = [
    a for a in agent_perf
    if a['avg_duration_ms'] > a['target_duration_ms']
]

# Agents with high failure rates
unreliable_agents = [
    a for a in agent_perf
    if (a['successful_executions'] / a['total_executions']) < 0.9
]

# Expensive agents (high token/cost)
expensive_agents = [
    a for a in agent_perf
    if a['total_cost_usd'] > 1.0
]

# Workflows with repeated failures
problem_workflows = [
    w for w in failures
    if w['task_description'] in recurring_failures
]
```

**Analysis Categories**:
1. **Performance Issues**: Agents slower than targets
2. **Reliability Issues**: Agents with <90% success rate
3. **Cost Issues**: Agents with high token usage
4. **Pattern Issues**: Recurring failures in workflows
5. **Integration Issues**: Sub-agent coordination problems
6. **Validation Issues**: Frequent expectation violations

### Step 3: Prioritization (10s)

**Calculate Impact Score**:
```python
def calculate_impact(issue):
    frequency = issue['execution_count'] / days  # Daily frequency
    severity = issue['deviation_from_target']     # How far off target
    cost_impact = issue['total_cost_usd']         # Financial impact

    # Impact = frequency × severity × cost
    return frequency * severity * cost_impact

# Rank all issues by impact
prioritized = sorted(issues, key=calculate_impact, reverse=True)
```

**Priority Levels**:
- **HIGH**: Impact >100, affects >10 executions/week, >$1/week cost
- **MEDIUM**: Impact 20-100, affects 3-10 executions/week
- **LOW**: Impact <20, affects <3 executions/week

### Step 4: Implementation (2-3 minutes)

**Launch `/build-feature` for Top Improvement**:

```markdown
Highest priority issue identified:
  Agent: framework-validation-engineer
  Issue: Average duration 15.2s (target: 10s)
  Impact: 150 (frequency: 15/week, severity: 1.52x, cost: $0.45/week)

Implementing fix using /build-feature...

Task:
  description: "Optimize framework-validation-engineer performance"
  prompt: |
    Feature: optimize-validation-performance

    Problem identified by observability:
    - Agent: framework-validation-engineer
    - Current performance: 15.2s average (target: 10s)
    - Frequency: 15 executions/week
    - Cost impact: +$0.45/week vs target

    Optimization goals:
    1. Reduce execution time to <10s
    2. Maintain 100% success rate
    3. Keep token usage reasonable

    Suggested approaches:
    - Add test result caching
    - Parallelize test execution
    - Optimize database queries
    - Pre-load common contexts

    Build this optimization following normal /build-feature process:
    - Research best practices
    - Design optimization
    - Implement changes
    - Validate improvement
    - Document changes

    Expected outcome:
    - Duration: 15.2s → <10s (>33% improvement)
    - Success rate: Maintained at 100%
    - Cost: Reduced by ~30%
  subagent_type: "framework-feature-builder"
```

### Step 5: Validation (30s)

**Measure Impact**:
```python
# Get baseline metrics (before improvement)
baseline = {
    'avg_duration': 15.2,
    'success_rate': 1.0,
    'avg_tokens': 6500,
    'avg_cost': 0.03
}

# Wait for improvement to be used in practice
# (or run test execution)

# Get new metrics (after improvement)
after = get_agent_performance_since(improvement_timestamp)

# Calculate improvement
improvement = {
    'duration_reduction': (baseline['avg_duration'] - after['avg_duration']) / baseline['avg_duration'],
    'success_rate_change': after['success_rate'] - baseline['success_rate'],
    'token_reduction': (baseline['avg_tokens'] - after['avg_tokens']) / baseline['avg_tokens'],
    'cost_reduction': (baseline['avg_cost'] - after['avg_cost']) / baseline['avg_cost']
}
```

### Step 6: Report & Schedule

**Generate Impact Report**:
```markdown
Show before/after metrics
Document improvement percentage
Schedule next self-improvement cycle
Update observability with improvement tracking
```

---

## Expected Output

### Successful Self-Improvement

```markdown
🚀 Self-Improvement Analysis

Analyzing observability data (last 30 days)...
├─ Total executions: 127
├─ Unique agents: 8
├─ Total cost: $5.42
└─ Overall success rate: 94.5%

─────────────────────────────────────────────────
📊 Performance Analysis

Opportunities identified: 5

1. [HIGH PRIORITY] framework-validation-engineer - Performance Issue
   ├─ Current: 15.2s avg (target: 10s)
   ├─ Frequency: 15 executions/week
   ├─ Cost impact: +$0.45/week
   ├─ Impact score: 150
   └─ Recommendation: Add caching, parallelize tests

2. [MEDIUM] framework-senior-engineer - Token Usage
   ├─ Current: 12.5K tokens avg (target: 10K)
   ├─ Frequency: 8 executions/week
   ├─ Cost impact: +$0.20/week
   ├─ Impact score: 45
   └─ Recommendation: Optimize context loading

3. [MEDIUM] documentation-specialist - Reliability
   ├─ Current: 87% success rate (target: >90%)
   ├─ Frequency: 12 executions/week
   ├─ Cost impact: Rework costs ~$0.30/week
   ├─ Impact score: 38
   └─ Recommendation: Improve error handling

4. [LOW] framework-architect - Duration
   ├─ Current: 22s avg (target: 20s)
   ├─ Frequency: 5 executions/week
   ├─ Cost impact: +$0.05/week
   ├─ Impact score: 12
   └─ Recommendation: Minor optimization

5. [LOW] framework-research-specialist - Cost
   ├─ Current: $0.08/execution (target: $0.05)
   ├─ Frequency: 3 executions/week
   ├─ Cost impact: +$0.09/week
   ├─ Impact score: 8
   └─ Recommendation: Cache documentation fetches

─────────────────────────────────────────────────
🎯 Implementing Top Priority Improvement

Issue: framework-validation-engineer performance
Target: Reduce 15.2s → <10s (33% improvement)

Launching /build-feature optimize-validation-performance...

Phase 1: Research ✅ (11s)
├─ Found caching patterns in best practices
└─ Located parallel test execution examples

Phase 2: Design ✅ (19s)
├─ Architecture: Test result cache + parallel runner
├─ Files: 2 new, 1 modified
└─ Expected improvement: 40-50%

Phase 3: Implementation ✅ (42s)
├─ Added TestResultCache class
├─ Implemented parallel test runner
└─ Updated validation workflow

Phase 4: Validation ✅ (25s)
├─ Tests: 15/15 passing ✅
├─ Performance: 8.3s avg (45% improvement!) ✅
├─ Compliance: 93% ✅
└─ Success rate: 100% maintained ✅

Phase 5: Documentation ✅ (14s)
└─ Optimization guide created

Build complete! ✅

─────────────────────────────────────────────────
📈 Impact Measurement

Before Optimization:
├─ Duration: 15.2s avg
├─ Success rate: 100%
├─ Tokens: 6,500 avg
└─ Cost: $0.03/execution

After Optimization:
├─ Duration: 8.3s avg ✅ (45% faster!)
├─ Success rate: 100% ✅ (maintained)
├─ Tokens: 5,800 avg ✅ (11% reduction)
└─ Cost: $0.025/execution ✅ (17% cheaper)

Weekly Impact:
├─ Time saved: 103.5s/week (1.7 min)
├─ Cost saved: $0.075/week ($3.90/year)
└─ Executions affected: 15/week

Cumulative Benefit (projected):
├─ 1 month: $0.30 saved
├─ 6 months: $1.80 saved
└─ 1 year: $3.90 saved

─────────────────────────────────────────────────
✅ Self-Improvement Complete

Summary:
├─ Issue identified: framework-validation-engineer performance
├─ Fix implemented: Test caching + parallelization
├─ Improvement: 45% faster, 17% cheaper
├─ Success rate: Maintained at 100%
└─ Status: DEPLOYED

Next Steps:
1. Monitor new performance over next week
2. Verify improvement persists
3. Schedule next self-improvement: November 4, 2025

Remaining opportunities: 4
├─ 1 MEDIUM priority
├─ 1 MEDIUM priority
└─ 2 LOW priority

Run /self-improve again to address next issue.

Framework is now 45% faster at validation! 🎉
```

### No Improvements Needed

```markdown
🚀 Self-Improvement Analysis

Analyzing observability data (last 30 days)...
├─ Total executions: 89
├─ Unique agents: 7
├─ Total cost: $3.21
└─ Overall success rate: 98.9%

─────────────────────────────────────────────────
📊 Performance Analysis

✅ Excellent Performance - No Critical Issues

All agents meeting targets:
├─ ✅ framework-architect: 18.2s avg (target: 20s)
├─ ✅ framework-senior-engineer: 9.8s avg (target: 10s)
├─ ✅ framework-validation-engineer: 8.5s avg (target: 10s)
├─ ✅ framework-best-practice-auditor: 2.1min avg (target: 3min)
├─ ✅ framework-research-specialist: 1.8min avg (target: 2min)
├─ ✅ documentation-specialist: 12s avg (target: 15s)
└─ ✅ framework-feature-builder: 2.3min avg (target: 3min)

Success Rates:
├─ All agents: >95% ✅
└─ Overall: 98.9% ✅

Cost Efficiency:
├─ Total spend: $3.21/month
├─ Avg cost/execution: $0.036
└─ Within budget ✅

─────────────────────────────────────────────────
🎯 Minor Optimization Opportunities

Found 2 low-priority optimizations:
1. documentation-specialist could cache templates (saves 1-2s)
2. framework-architect could pre-load contexts (saves 0.5s)

Estimated impact: <5% improvement
Recommendation: Not worth implementing now

─────────────────────────────────────────────────
✅ Framework Operating at Peak Performance

No improvements needed at this time.

Recommendation:
- Continue monitoring performance
- Run /self-improve again in 30 days
- Or run if performance degrades

Next scheduled self-improvement: November 4, 2025

Framework is healthy! 🎉
```

### Multiple Issues to Address

```markdown
🚀 Self-Improvement Analysis

Analyzing observability data (last 30 days)...
├─ Total executions: 156
├─ Unique agents: 9
├─ Total cost: $8.92
└─ Overall success rate: 88.5% ⚠️

─────────────────────────────────────────────────
📊 Performance Analysis

⚠️ Multiple Issues Detected

Critical Issues: 2
High Priority: 1
Medium Priority: 3
Low Priority: 2

Priority Order (by impact score):
1. [CRITICAL - 245] framework-code-reviewer - Reliability
   ├─ Success rate: 82% (target: >95%)
   ├─ Frequency: 20 executions/week
   ├─ Impact: Blocks 3-4 builds/week
   └─ Fix: Improve error handling, add retries

2. [CRITICAL - 198] framework-validation-engineer - Performance
   ├─ Duration: 25.3s (target: 10s)
   ├─ Frequency: 18 executions/week
   ├─ Impact: Delays all feature builds
   └─ Fix: Add caching, parallelize tests

3. [HIGH - 112] documentation-specialist - Token Usage
   ├─ Tokens: 18.5K avg (target: 10K)
   ├─ Frequency: 15 executions/week
   ├─ Cost: +$1.20/week
   └─ Fix: Optimize prompts, use templates

... (more issues listed)

─────────────────────────────────────────────────
🎯 Implementation Plan

Implementing top 3 issues would:
├─ Improve success rate: 88.5% → 96%
├─ Reduce avg duration: 18.2s → 12.1s
├─ Save cost: $8.92/month → $6.45/month
└─ Total benefit: ~$30/year + 33% faster

Choose action:
1. [Recommended] Fix top issue only (framework-code-reviewer)
2. Fix all CRITICAL issues (2 fixes)
3. Fix all HIGH+ issues (3 fixes)
4. Defer improvements

Implementing top issue (framework-code-reviewer)...

[Build process continues...]
```

---

## Performance Targets

- **Data Collection**: <10s
- **Analysis**: <20s
- **Prioritization**: <10s
- **Implementation**: <3 minutes (via /build-feature)
- **Validation**: <30s
- **Report**: <10s

**Total Self-Improvement Cycle**: <4 minutes

---

## Quality Criteria

Self-improvement succeeds when:
- ✅ Observability data analyzed
- ✅ Issues prioritized by impact
- ✅ Top improvement implemented
- ✅ Measurable performance gain
- ✅ No regressions introduced
- ✅ Next cycle scheduled

---

## Integration with Observability

**Tracks its own improvements**:

```sql
-- View all self-improvement cycles
SELECT
    started_at,
    duration_ms,
    status,
    task_description
FROM executions
WHERE agent_name = 'framework-feature-builder'
  AND task_description LIKE '%self-improve%'
ORDER BY started_at DESC;

-- Measure improvement impact
SELECT
    e1.agent_name,
    AVG(CASE WHEN e1.started_at < ?1 THEN e1.duration_ms END) as before_avg,
    AVG(CASE WHEN e1.started_at > ?1 THEN e1.duration_ms END) as after_avg,
    (AVG(CASE WHEN e1.started_at < ?1 THEN e1.duration_ms END) -
     AVG(CASE WHEN e1.started_at > ?1 THEN e1.duration_ms END)) /
     AVG(CASE WHEN e1.started_at < ?1 THEN e1.duration_ms END) * 100 as improvement_pct
FROM executions e1
WHERE agent_name = ?2
GROUP BY agent_name;
```

---

## Integration with Other Commands

### Recommended Cycle
```bash
# Monthly maintenance cycle
/update-docs        # Get latest best practices
/audit-practices    # Check compliance
/self-improve       # Fix performance issues

# Result: Framework stays current, compliant, and optimized
```

### After Major Changes
```bash
# After merging several features
/self-improve       # Optimize any degraded performance
/audit-practices    # Verify still compliant
```

### Continuous Improvement
```bash
# Weekly automation (could be cron job)
/self-improve --days 7

# Framework continuously improves itself!
```

---

## Why This Command Matters

**This proves the framework is truly intelligent.**

The framework can:
1. ✅ Observe its own behavior (observability)
2. ✅ Identify its own weaknesses (analysis)
3. ✅ Prioritize improvements (decision making)
4. ✅ Fix its own problems (self-building)
5. ✅ Measure its own improvement (validation)
6. ✅ Repeat indefinitely (continuous improvement)

**This is AI-driven development at its finest** - the framework gets better over time without human intervention.

---

## Advanced Usage

### Focus on Specific Agent
```bash
# Only improve one agent
/self-improve --agent framework-validation-engineer
```

### Dry Run (Analysis Only)
```bash
# See what would be improved without implementing
/self-improve --dry-run
```

### Multiple Improvements
```bash
# Fix top 3 issues
/self-improve --count 3
```

### Cost-Focused
```bash
# Only implement improvements saving >$1/month
/self-improve --min-savings 1.00
```

---

## Tips for Maximum Benefit

### Run Regularly
- Weekly for active development
- Monthly for stable frameworks
- After any major changes

### Let It Run Automatically
- Set up cron job for weekly runs
- Framework improves itself while you sleep
- Wake up to faster, cheaper agents

### Trust the Data
- Observability tracks everything
- Impact scores are objective
- Top priority is usually correct choice

### Monitor Trends
```bash
# See improvement over time
python3 .claude-library/observability/obs.py summary --days 90

# Track cost trends
python3 .claude-library/observability/obs.py agents --sort-by cost
```

---

## Error Handling

### No Observability Data
```markdown
❌ Cannot run self-improvement

Error: No observability data found

Possible causes:
1. Observability not initialized
2. No agent executions yet
3. Database file missing

Resolution:
1. Run: /update-docs (triggers agent execution)
2. Or: /audit-practices (collects data)
3. Then: /self-improve (should work)
```

### All Agents Performing Well
```markdown
✅ No improvements needed

All agents meeting targets.
Framework is healthy.

Run /self-improve again in 30 days.
```

### Improvement Build Fails
```markdown
⚠️ Self-Improvement Failed

Issue identified: framework-validation-engineer performance
Attempted fix: optimize-validation-performance

Build result: FAILED
├─ Tests: 8/12 passing (66%)
├─ Issue: Breaking changes introduced
└─ Action: Reverted changes

Recommendation:
1. Review failure details
2. Manual investigation needed
3. Try simpler optimization approach

Framework performance unchanged (safe fallback).
```

---

## Observability Tracking

Every self-improvement cycle tracks:
- Issues identified
- Priority scores
- Improvement implemented
- Before/after metrics
- Cost savings
- Time savings
- Success/failure status

**View history**:
```bash
# Recent self-improvements
python3 .claude-library/observability/obs.py recent | grep self-improve

# Specific cycle details
python3 .claude-library/observability/obs.py execution <id>
```

---

## Example: Real Self-Improvement Cycle

```markdown
Day 1: Framework stable, all agents performing well
  ├─ Run: /self-improve
  └─ Result: No improvements needed ✅

Day 15: New features added, validation slowing down
  ├─ Run: /self-improve
  ├─ Identified: validation-engineer 18s (target: 10s)
  ├─ Fixed: Added test caching
  └─ Result: 18s → 9s (50% improvement) ✅

Day 30: Documentation generation using too many tokens
  ├─ Run: /self-improve
  ├─ Identified: documentation-specialist 15K tokens (target: 10K)
  ├─ Fixed: Template-based generation
  └─ Result: 15K → 8K tokens, -$0.40/week ✅

Day 45: All agents optimized
  ├─ Run: /self-improve
  └─ Result: No improvements needed ✅

Total improvement: 50% faster validation, 47% cheaper docs
Annual savings: ~$20/year
Time saved: ~2 hours/year
```

**The framework literally made itself better.**

---

**Command Version**: 1.0.0
**Agent**: framework-feature-builder (coordinator)
**Performance Baseline**: <4 minutes per cycle
**Last Updated**: October 4, 2025

**The ultimate proof of intelligence: self-improvement** 🧠
