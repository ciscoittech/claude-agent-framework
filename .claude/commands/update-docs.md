---
description: Fetch the latest Claude Code documentation and refresh framework context files
allowed-tools: WebFetch, Read, Write, Edit, Agent
---

# /update-docs - Update Claude Code Documentation

**Purpose**: Fetch latest Claude Code documentation and update framework context files
**Agent**: framework-research-specialist
**Type**: Maintenance Command
**Frequency**: Weekly or when Claude Code releases updates

---

## Command Usage

```bash
/update-docs
```

**No arguments needed** - updates all documentation automatically.

---

## What This Command Does

1. **Fetches Latest Docs** from official sources:
   - https://www.anthropic.com/engineering/claude-code-best-practices
   - https://docs.claude.com/en/docs/claude-code/sub-agents.md
   - https://docs.claude.com/en/docs/claude-code/hooks-guide.md
   - https://docs.claude.com/en/docs/claude-code/mcp.md
   - https://docs.claude.com/en/docs/claude-code/common-workflows.md

2. **Analyzes Changes**:
   - Compares with current context files
   - Identifies new patterns and practices
   - Detects deprecated features
   - Extracts code examples

3. **Updates Context Files**:
   - `.claude-library/contexts/claude-code-best-practices.md`
   - `.claude-library/contexts/claude-code-subagents.md`
   - `.claude-library/contexts/claude-code-hooks.md`
   - `.claude-library/contexts/claude-code-mcp.md`
   - `.claude-library/contexts/claude-code-documentation-map.md`

4. **Generates Report**:
   - Lists all changes detected
   - Identifies framework impact
   - Recommends updates to agents/commands
   - Prioritizes actions

---

## Workflow

### Execution Pattern

**Sequential** - Research specialist works alone

### Steps

1. **Initialize**
   - Load current context files
   - Prepare documentation sources

2. **Fetch & Analyze** (framework-research-specialist)
   - Fetch each documentation source
   - Compare with current content
   - Extract changes and new patterns
   - Identify framework impacts

3. **Update Contexts**
   - Write updated content to context files
   - Update timestamps
   - Preserve framework-specific notes

4. **Report Results**
   - Summarize changes
   - List affected components
   - Provide recommendations

---

## Expected Output

```markdown
# Documentation Update Report

**Date**: October 4, 2025
**Duration**: 1.5 minutes
**Sources Checked**: 5

## Changes Detected

### claude-code-best-practices.md
**Status**: Updated
**Changes**:
- Added: New visual iteration workflow pattern
- Updated: Context optimization recommendations
- Removed: Deprecated workflow example

**Framework Impact**: MEDIUM
- New pattern applicable to UI-focused agents
- Context optimization already implemented

### claude-code-subagents.md
**Status**: Updated
**Changes**:
- Updated: Task tool parallel execution syntax
- Added: New example for hierarchical decomposition
- Clarified: Performance optimization guidance

**Framework Impact**: HIGH
- All commands should use updated parallel syntax
- Agent launcher can optimize coordination

### claude-code-hooks.md
**Status**: No changes
**Last checked**: October 4, 2025

### claude-code-mcp.md
**Status**: Updated
**Changes**:
- Added: Python SDK async patterns
- Added: 3 new server examples
- Updated: Security best practices

**Framework Impact**: LOW
- Examples enhance documentation
- No breaking changes

### claude-code-documentation-map.md
**Status**: Updated
**Changes**:
- Added: 2 new documentation pages
- Updated: Links to SDK guides

**Framework Impact**: LOW
- Reference update only

## Summary

**Total Updates**: 4/5 files
**Breaking Changes**: None
**New Patterns**: 2
**Deprecated**: 1

## Framework Recommendations

### HIGH Priority
1. Update agent-launcher.md with new parallel Task syntax
   - Location: `.claude/agent-launcher.md`
   - Pattern: Launch multiple agents in single message
   - Benefit: 20-30% faster coordination

### MEDIUM Priority
2. Add visual iteration workflow to AGENT_PATTERNS.md
   - Pattern: Screenshot → Iterate → Improve
   - Use case: Future UI-focused agents
   - Benefit: Better visual output quality

### LOW Priority
3. Enhance MCP documentation with new Python examples
   - Location: `claude-code-mcp.md`
   - Impact: Better developer experience
   - Benefit: Easier MCP integration

## Next Steps

1. Review HIGH priority recommendations
2. Implement updates if approved
3. Re-audit framework compliance
4. Schedule next update: November 1, 2025

---

**Documentation is now current** ✅
**Framework aligned with Claude Code best practices** ✅
```

---

## When to Run

### Recommended Schedule
- **Weekly**: Check for updates every Monday
- **Before Major Features**: Ensure latest patterns before building
- **After Claude Code Releases**: Update immediately after new versions

### Triggers
- New Claude Code version announced
- Best practices article updated
- Framework compliance score drops
- Before creating new agent patterns

---

## Integration with Other Commands

### With `/audit-practices`
After updating docs, run audit to check compliance:
```bash
/update-docs
/audit-practices
```

### With `/build-feature`
Update docs before building features to use latest patterns:
```bash
/update-docs
/build-feature my-new-feature
```

---

## Performance Targets

- **Total Duration**: < 2 minutes
- **Doc Fetch**: < 10s per source
- **Analysis**: < 30s total
- **Update**: < 20s per file
- **Report**: < 15s

---

## Quality Criteria

Command succeeds when:
- ✅ All 5 documentation sources checked
- ✅ Changes accurately detected
- ✅ Context files updated correctly
- ✅ Report is comprehensive
- ✅ Recommendations are actionable
- ✅ Performance targets met

---

## Error Handling

### If Documentation Unavailable
```markdown
⚠️ Unable to fetch: https://docs.claude.com/en/docs/claude-code/sub-agents.md

Error: Connection timeout

Fallback:
- Using cached version from September 15, 2025
- Marked for retry on next update
- Other sources updated successfully

Recommendation: Verify network connection and retry
```

### If Significant Breaking Changes
```markdown
🚨 BREAKING CHANGES DETECTED

Source: claude-code-subagents.md
Changes:
- Task tool API changed (subagent_type → agent_type)
- Parallel execution requires new syntax

Impact: HIGH
- All commands need updates
- Agent launcher must change
- Estimated effort: 2-3 hours

CRITICAL: Review changes before proceeding
Recommend: Schedule dedicated update session
```

---

## Example Execution

**User Input**: `/update-docs`

**System Response**:
```markdown
Starting documentation update...

Fetching Claude Code documentation:
✅ Best practices (2.1s)
✅ Sub-agents guide (1.8s)
✅ Hooks guide (1.5s)
✅ MCP guide (2.3s)
✅ Documentation map (1.2s)

Analyzing changes:
📝 Best practices: 2 new patterns detected
📝 Sub-agents: Syntax updated
⏭️  Hooks: No changes
📝 MCP: 3 new examples
📝 Doc map: Links updated

Updating context files:
✅ claude-code-best-practices.md
✅ claude-code-subagents.md
✅ claude-code-mcp.md
✅ claude-code-documentation-map.md

Generating report...

[Full report shown above]

Update complete! ✅
Completed in 1.8 minutes

Next: Review HIGH priority recommendations
```

---

## Tips

### Maximize Effectiveness
1. **Run regularly** - Weekly schedule prevents drift
2. **Review reports** - Don't just update, implement recommendations
3. **Track trends** - Monitor how often docs change
4. **Automate** - Consider cron job for weekly runs
5. **Combine with audit** - Update → Audit → Improve cycle

### Troubleshooting
- **Slow fetches**: Check internet connection
- **No changes detected**: Docs may be stable (good!)
- **High framework impact**: Plan implementation time
- **Breaking changes**: Coordinate with team before updating

---

**Command Version**: 1.0.0
**Agent**: framework-research-specialist
**Performance Baseline**: 1.5-2 minutes
**Last Updated**: October 4, 2025
