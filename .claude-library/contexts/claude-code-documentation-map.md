# Claude Code Documentation Map

**Source**: https://docs.claude.com/en/docs/claude-code/claude_code_docs_map.md
**Purpose**: Complete map of all Claude Code documentation
**Auto-update**: Fetch latest from docs.claude.com

---

## Documentation Structure

### Getting Started
- [overview](https://docs.claude.com/en/docs/claude-code/overview.md)
- [quickstart](https://docs.claude.com/en/docs/claude-code/quickstart.md)
- [common-workflows](https://docs.claude.com/en/docs/claude-code/common-workflows.md)

### Build with Claude Code
- [sub-agents](https://docs.claude.com/en/docs/claude-code/sub-agents.md)
- [output-styles](https://docs.claude.com/en/docs/claude-code/output-styles.md)
- [hooks-guide](https://docs.claude.com/en/docs/claude-code/hooks-guide.md)
- [github-actions](https://docs.claude.com/en/docs/claude-code/github-actions.md)
- [gitlab-ci-cd](https://docs.claude.com/en/docs/claude-code/gitlab-ci-cd.md)
- [mcp](https://docs.claude.com/en/docs/claude-code/mcp.md)
- [troubleshooting](https://docs.claude.com/en/docs/claude-code/troubleshooting.md)

### Claude Code SDK > Guides
- [streaming-vs-single-mode](https://docs.claude.com/en/docs/claude-code/sdk/streaming-vs-single-mode.md)
- [sdk-permissions](https://docs.claude.com/en/docs/claude-code/sdk/sdk-permissions.md)
- [sdk-sessions](https://docs.claude.com/en/docs/claude-code/sdk/sdk-sessions.md)
- [modifying-system-prompts](https://docs.claude.com/en/docs/claude-code/sdk/modifying-system-prompts.md)
- [sdk-mcp](https://docs.claude.com/en/docs/claude-code/sdk/sdk-mcp.md)
- [custom-tools](https://docs.claude.com/en/docs/claude-code/sdk/custom-tools.md)

### Configuration
- [settings](https://docs.claude.com/en/docs/claude-code/settings.md)
- [ide-integrations](https://docs.claude.com/en/docs/claude-code/ide-integrations.md)
- [terminal-config](https://docs.claude.com/en/docs/claude-code/terminal-config.md)
- [model-configuration](https://docs.claude.com/en/docs/claude-code/model-configuration.md)

### Reference
- [cli-reference](https://docs.claude.com/en/docs/claude-code/cli-reference.md)
- [slash-commands](https://docs.claude.com/en/docs/claude-code/slash-commands.md)
- [interactive-mode](https://docs.claude.com/en/docs/claude-code/interactive-mode.md)
- [checkpointing](https://docs.claude.com/en/docs/claude-code/checkpointing.md)
- [hooks-reference](https://docs.claude.com/en/docs/claude-code/hooks-reference.md)

---

## Key Documentation by Use Case

### For Framework Development

**Core Concepts**:
1. [sub-agents](https://docs.claude.com/en/docs/claude-code/sub-agents.md) - Task tool and parallel execution
2. [hooks-guide](https://docs.claude.com/en/docs/claude-code/hooks-guide.md) - Event-driven automation
3. [mcp](https://docs.claude.com/en/docs/claude-code/mcp.md) - Extending capabilities
4. [output-styles](https://docs.claude.com/en/docs/claude-code/output-styles.md) - Customizing responses

**Advanced Topics**:
1. [sdk-sessions](https://docs.claude.com/en/docs/claude-code/sdk/sdk-sessions.md) - Session management
2. [modifying-system-prompts](https://docs.claude.com/en/docs/claude-code/sdk/modifying-system-prompts.md) - Prompt customization
3. [custom-tools](https://docs.claude.com/en/docs/claude-code/sdk/custom-tools.md) - Tool creation

### For Agent Building

**Essential**:
1. [sub-agents](https://docs.claude.com/en/docs/claude-code/sub-agents.md) - How to launch agents
2. [common-workflows](https://docs.claude.com/en/docs/claude-code/common-workflows.md) - Proven patterns
3. [sdk-permissions](https://docs.claude.com/en/docs/claude-code/sdk/sdk-permissions.md) - Tool access control

**Optimization**:
1. [streaming-vs-single-mode](https://docs.claude.com/en/docs/claude-code/sdk/streaming-vs-single-mode.md) - Performance tuning
2. [model-configuration](https://docs.claude.com/en/docs/claude-code/model-configuration.md) - Model selection

### For CI/CD Integration

**Automation**:
1. [github-actions](https://docs.claude.com/en/docs/claude-code/github-actions.md) - GitHub integration
2. [gitlab-ci-cd](https://docs.claude.com/en/docs/claude-code/gitlab-ci-cd.md) - GitLab integration
3. [cli-reference](https://docs.claude.com/en/docs/claude-code/cli-reference.md) - Command line usage

**Workflows**:
1. [hooks-guide](https://docs.claude.com/en/docs/claude-code/hooks-guide.md) - Automated validation
2. [checkpointing](https://docs.claude.com/en/docs/claude-code/checkpointing.md) - State management

---

## Best Practices Cross-Reference

**From**: https://www.anthropic.com/engineering/claude-code-best-practices

Maps to documentation:
- **Customize Setup** → [settings](https://docs.claude.com/en/docs/claude-code/settings.md)
- **Optimize Context** → [sdk-permissions](https://docs.claude.com/en/docs/claude-code/sdk/sdk-permissions.md)
- **Workflow Strategies** → [common-workflows](https://docs.claude.com/en/docs/claude-code/common-workflows.md)
- **Advanced Techniques** → [sub-agents](https://docs.claude.com/en/docs/claude-code/sub-agents.md), [mcp](https://docs.claude.com/en/docs/claude-code/mcp.md)

---

## Framework Context Files

These framework contexts correspond to official docs:

| Framework Context | Official Doc(s) |
|------------------|-----------------|
| `claude-code-best-practices.md` | [Best Practices Article](https://www.anthropic.com/engineering/claude-code-best-practices) |
| `claude-code-subagents.md` | [sub-agents.md](https://docs.claude.com/en/docs/claude-code/sub-agents.md) |
| `claude-code-hooks.md` | [hooks-guide.md](https://docs.claude.com/en/docs/claude-code/hooks-guide.md), [hooks-reference.md](https://docs.claude.com/en/docs/claude-code/hooks-reference.md) |
| `claude-code-mcp.md` | [mcp.md](https://docs.claude.com/en/docs/claude-code/mcp.md), [sdk-mcp.md](https://docs.claude.com/en/docs/claude-code/sdk/sdk-mcp.md) |

---

## Update Strategy

### For `/update-docs` Command

The framework-research-specialist agent should:

1. **Fetch Core Docs** (priority order):
   ```
   1. claude-code-best-practices (engineering blog)
   2. sub-agents.md (Task tool)
   3. hooks-guide.md (Hooks system)
   4. mcp.md (MCP integration)
   5. common-workflows.md (Patterns)
   ```

2. **Check for Changes**:
   - Compare content hashes
   - Identify new sections
   - Detect deprecated features
   - Track version updates

3. **Update Context Files**:
   - Extract key principles
   - Update code examples
   - Add new patterns
   - Remove deprecated info

4. **Generate Change Report**:
   - List what changed
   - Suggest framework updates
   - Identify breaking changes
   - Recommend actions

### Automation

```python
# framework-research-specialist agent logic
async def update_documentation():
    docs_to_fetch = [
        ("best-practices", "https://www.anthropic.com/engineering/claude-code-best-practices"),
        ("sub-agents", "https://docs.claude.com/en/docs/claude-code/sub-agents.md"),
        ("hooks", "https://docs.claude.com/en/docs/claude-code/hooks-guide.md"),
        ("mcp", "https://docs.claude.com/en/docs/claude-code/mcp.md"),
    ]

    changes = []
    for name, url in docs_to_fetch:
        new_content = await fetch_url(url)
        old_content = read_context_file(f"claude-code-{name}.md")

        if has_changed(old_content, new_content):
            update_context_file(f"claude-code-{name}.md", new_content)
            changes.append(f"Updated: {name}")

    return changes
```

---

## Resources

**Official**:
- Docs Home: https://docs.claude.com/en/docs/claude-code/overview
- Best Practices: https://www.anthropic.com/engineering/claude-code-best-practices
- Doc Map: https://docs.claude.com/en/docs/claude-code/claude_code_docs_map.md

**Framework**:
- All context files: `.claude-library/contexts/`
- Update command: `/update-docs`
- Research agent: `framework-research-specialist`

---

**Last Updated**: October 4, 2025
**Update Method**: `/update-docs` command (auto-fetches latest)
