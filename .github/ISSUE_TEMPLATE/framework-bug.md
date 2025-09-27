---
name: Framework Bug Report
about: Report a bug or issue with the Claude Agent Framework
title: '[BUG] Brief description of the bug'
labels: 'type: bug, priority: high'
---

## Bug Description
Clear and concise description of the bug in the Claude Agent Framework

## Framework Component Affected
Which part of the framework is experiencing the issue?
- [ ] Agent Design Patterns
- [ ] Workflow Orchestration
- [ ] Context Management
- [ ] Tool Configuration
- [ ] Parallel Execution
- [ ] Performance Optimization
- [ ] Documentation/Examples

## Steps to Reproduce
1. Framework setup used
2. Specific configuration
3. Commands or actions taken
4. Expected vs actual behavior

## Environment Details
- **Framework Version**: v1.0
- **Claude Code Version**: [version]
- **Project Type**: [Laravel/React/Python/etc.]
- **Operating System**: [macOS/Windows/Linux]

## Expected Behavior
What should happen according to the framework documentation?

## Actual Behavior
What actually happens?

## Framework Configuration
Please provide relevant framework configuration:

### .claude/ Structure
```
.claude/
├── agent-launcher.md
├── settings.json
└── commands/
    └── [relevant-command].md
```

### .claude-library/ Structure
```
.claude-library/
├── REGISTRY.json
├── agents/
└── contexts/
```

### Agent Configuration
If the issue involves specific agents, please share the agent configuration:
```markdown
# Relevant agent configuration
```

### Command Configuration
If the issue involves commands, please share the command configuration:
```markdown
# Relevant command configuration
```

## Error Messages
If applicable, include any error messages:
```
Error message here
```

## Performance Impact
Is this affecting framework performance?
- [ ] No performance impact
- [ ] Minor performance degradation
- [ ] Significant performance issues
- [ ] Framework unusable

## Agent Execution Issues
If related to agent execution:
- [ ] Agents not loading properly
- [ ] Parallel execution failing
- [ ] Tool access issues
- [ ] Context loading problems
- [ ] Workflow orchestration issues

## Context Loading Issues
If related to context management:
- [ ] Contexts not loading
- [ ] Dynamic loading failures
- [ ] Context caching issues
- [ ] Memory usage problems

## Tool Configuration Issues
If related to tool configuration:
- [ ] Tool access restrictions not working
- [ ] Tool permissions issues
- [ ] MCP tool integration problems

## Workflow Issues
If related to workflow orchestration:
- [ ] Sequential workflow problems
- [ ] Parallel execution failures
- [ ] Hierarchical workflow issues
- [ ] Command routing problems

## Documentation Issues
If this is a documentation bug:
- [ ] Incorrect information
- [ ] Missing examples
- [ ] Outdated patterns
- [ ] Broken links or references

## Reproducibility
How consistently can this bug be reproduced?
- [ ] Always (100%)
- [ ] Often (75%+)
- [ ] Sometimes (25-75%)
- [ ] Rarely (<25%)
- [ ] Unable to reproduce

## Impact Assessment
What is the impact of this bug?
- [ ] Blocks framework usage completely
- [ ] Prevents specific features from working
- [ ] Causes performance degradation
- [ ] Minor inconvenience
- [ ] Documentation clarity issue

## Workaround
Is there a temporary workaround?
- [ ] No workaround available
- [ ] Workaround available (describe below)

**Workaround Description**:
[If available, describe the workaround]

## Additional Context
- Screenshots or logs if applicable
- Related issues or discussions
- Framework modifications made
- Other relevant information

## Framework Health Check
Please run this basic framework health check:

```bash
# Check core files exist
ls -la CLAUDE_AGENT_FRAMEWORK.md
ls -la AGENT_PATTERNS.md
ls -la SIMPLICITY_ENFORCEMENT.md

# Check .claude/ structure
ls -la .claude/
ls -la .claude-library/

# Validate REGISTRY.json if exists
cat .claude-library/REGISTRY.json
```

**Health Check Results**:
```
[Paste results here]
```

## Suggested Fix
If you have ideas for how to fix this issue:
- Technical approach
- Framework changes needed
- Documentation updates required

## Priority Justification
Why should this bug be prioritized?
- User impact
- Framework stability
- Development blocker
- Security implications