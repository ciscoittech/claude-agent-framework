# Claude Code Best Practices Context

**Source**: https://www.anthropic.com/engineering/claude-code-best-practices
**Purpose**: Official best practices for using Claude Code effectively
**Auto-update**: Use WebFetch to get latest version

---

## Core Principles

### 1. Customize Your Setup with CLAUDE.md

**What to Document**:
- Bash commands and scripts
- Code style guidelines
- Testing instructions
- Repository etiquette
- Developer environment setup

**Example CLAUDE.md Structure**:
```markdown
# Project Setup
- Run: `npm install && npm test`
- Style: ESLint + Prettier
- Tests: Jest, 80% coverage required
- Git: Conventional commits only

# Development
- Branch naming: `feature/`, `fix/`, `docs/`
- PR requires 1 approval
- CI must pass before merge
```

### 2. Optimize Context and Permissions

**Context Management**:
- Tune CLAUDE.md files iteratively
- Start minimal, add as needed
- Use `/clear` to reset focused context
- Curate allowed tools carefully

**Permission Strategy**:
- Use `/permissions` to manage tool access
- Restrict dangerous tools (Write, Edit) until needed
- Install GitHub CLI for enhanced interactions
- Review tool usage regularly

### 3. Workflow Strategies

#### A. Explore → Plan → Code → Commit
1. **Explore**: Read relevant files first
2. **Plan**: Use "think" modes for deeper analysis
3. **Code**: Create implementation plan
4. **Commit**: Verify solution, commit with clear messages

#### B. Test-Driven Development
1. Write tests first
2. Confirm tests initially fail
3. Implement code to pass tests
4. Use subagents to verify implementation

#### C. Visual Iteration
1. Provide screenshots or design mocks
2. Iterate on visual implementations
3. Take multiple screenshots to improve results

### 4. Advanced Techniques

**Subagents (Task Tool)**:
- Launch specialized agents for complex tasks
- Run agents in parallel for speed
- Use for: research, implementation, testing, documentation

**MCP Servers**:
- Extend capabilities with Model Context Protocol
- Add custom tools and data sources
- Integrate with external services

**Multiple Instances**:
- Use git worktrees for parallel work
- Run multiple Claude instances simultaneously
- Coordinate with clear communication

**Headless Mode**:
- Automate workflows with CLI
- CI/CD integration
- Batch processing

### 5. General Principles

**Be Specific**:
- Provide clear, detailed instructions
- Include examples when possible
- Specify desired output format

**Course-Correct Early**:
- Review outputs immediately
- Fix issues before they compound
- Use `/undo` to revert mistakes

**Maintain Focus**:
- Use `/clear` for focused context
- Limit scope of requests
- Break large tasks into smaller steps

**Provide References**:
- Visual references (screenshots, diagrams)
- Textual references (code samples, docs)
- Examples of desired output

**Experiment**:
- Try different approaches
- Find what works for your workflow
- Adapt patterns to your needs

---

## Framework-Specific Applications

### For Agent System Development

**When Building Agents**:
- Document agent capabilities in CLAUDE.md
- Define clear triggers and tools
- Specify contexts each agent needs
- Set performance targets

**When Creating Commands**:
- Follow Explore → Plan → Code workflow
- Use TDD for command validation
- Document expected workflow
- Set clear success criteria

**When Optimizing Performance**:
- Use `/clear` between agent tasks
- Minimize context per agent (<10KB)
- Leverage parallel execution
- Monitor with observability

### For Self-Building System

**Documentation First**:
- Update CLAUDE.md before building
- Document expected behavior
- Define validation criteria
- Set quality gates

**Iterative Enhancement**:
- Start with MVP implementation
- Test thoroughly at each step
- Use observability to track
- Refine based on metrics

**Quality Assurance**:
- Write tests before features
- Use subagents for validation
- Automate compliance checks
- Track with observability

---

## Checklist for Framework Compliance

- [ ] CLAUDE.md is comprehensive and current
- [ ] Tool permissions are curated and minimal
- [ ] Workflow follows Explore → Plan → Code → Commit
- [ ] Tests exist and pass before implementation
- [ ] Context is optimized (<10KB per agent)
- [ ] Subagents used for complex tasks
- [ ] Observability tracks all executions
- [ ] Documentation is complete and clear
- [ ] Performance targets are met
- [ ] Quality gates are enforced

---

## Resources

**Official Docs**:
- Best Practices: https://www.anthropic.com/engineering/claude-code-best-practices
- Documentation: https://docs.claude.com/en/docs/claude-code/overview
- Subagents Guide: https://docs.claude.com/en/docs/claude-code/sub-agents.md
- Hooks Reference: https://docs.claude.com/en/docs/claude-code/hooks-guide.md

**Framework Docs**:
- See `framework-architecture.md` for architecture principles
- See `framework-development-patterns.md` for implementation patterns
- See `performance-optimization.md` for performance strategies

---

**Last Updated**: October 4, 2025
**Update Method**: `python3 .claude-library/observability/obs.py` or `/update-docs` command
