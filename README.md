# Claude Agent Framework

### Transform any project into an AI-powered development powerhouse in 2 minutes

[![Framework Version](https://img.shields.io/badge/version-2.0-blue)]()
[![Setup Time](https://img.shields.io/badge/setup-2%20minutes-green)]()
[![Performance](https://img.shields.io/badge/speed-3--6x%20faster-orange)]()
[![Context Reduction](https://img.shields.io/badge/context-97%25%20smaller-red)]()

---

## What is Claude Agent Framework?

Claude Agent Framework is a battle-tested system that transforms Claude Code into a team of specialized AI agents working in parallel on your project. Whether you're building a startup MVP, enterprise system, or personal project, this framework adapts to your stack and your patterns.

**One prompt. Two minutes. Full agent team.**

---

## The 2-Minute Setup

```bash
# In your project directory
$ claude

# Paste this:
"I want to set up Claude Agent Framework for my project.
Please read the SYSTEM_GENERATOR_PROMPT.md from ./claude-agent-framework/
and create my custom agent system."

# That's it. You're done.
```

Your custom agent team is now ready with:
- Agents that understand your tech stack
- Commands tailored to your workflow
- Patterns extracted from your codebase
- Parallel execution for 3-6x speed boost

---

## From Zero to Hero

### Start Small (Minute 0-2)
Run the generator. Get instant:
- `/build` - Parallel TDD development
- `/debug` - Smart debugging
- `/test` - Comprehensive testing
- `/deploy` - One-command deployment

### Grow Naturally (Day 1-7)
Your system learns and adapts:
- Agents understand your code patterns
- Commands evolve with your workflow
- Context stays minimal (<10KB)
- Speed increases as patterns emerge

### Expand as Needed (Week 2+)
Build your dream team:
- Add specialized agents for new domains
- Create custom workflows for your process
- Integrate with your CI/CD pipeline
- Scale to any project size

---

## Why Claude Agent Framework?

### The Problem
- **Manual Claude setup** takes hours of context building
- **Sequential execution** wastes time on independent tasks
- **Context overload** (250KB+) slows every interaction
- **Repetitive prompts** for common workflows

### The Solution
- **2-minute setup** with intelligent auto-configuration
- **Parallel agents** work simultaneously (3-6x faster)
- **Minimal context** (<10KB auto-loaded)
- **Smart commands** that orchestrate complex workflows

---

## What Gets Built

```
your-project/
├── .claude/                    # Ultra-light core (<10KB)
│   ├── agent-launcher.md      # Your mission control
│   ├── settings.json          # Project metadata
│   ├── MEMORY.md              # Cross-conversation memory
│   ├── agents/                # Custom subagent types
│   ├── rules/                 # Path-specific rules
│   └── commands/              # Your power tools
│       ├── build.md          # Feature development
│       ├── debug.md          # Problem solving
│       ├── test.md           # Quality assurance
│       └── deploy.md         # Ship to production
│
└── .claude-library/           # On-demand specialists
    ├── REGISTRY.json         # Central configuration (v2.0)
    ├── agents/               # Your AI team
    ├── contexts/             # Shared knowledge
    └── skills/               # Skill definitions
```

---

## Framework Documentation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| [SIMPLICITY_ENFORCEMENT.md](./SIMPLICITY_ENFORCEMENT.md) | Circuit breakers | Read first |
| [SYSTEM_GENERATOR_PROMPT.md](./SYSTEM_GENERATOR_PROMPT.md) | Auto-generate system | Start here (2 min) |
| [CLAUDE_AGENT_FRAMEWORK.md](./CLAUDE_AGENT_FRAMEWORK.md) | Architecture guide | Learn the system |
| [AGENT_PATTERNS.md](./AGENT_PATTERNS.md) | Implementation patterns | Optimize |
| [AGENT_SYSTEM_TEMPLATE.md](./AGENT_SYSTEM_TEMPLATE.md) | Manual setup | Custom control |
| [MULTI_MODEL_ROUTING.md](./MULTI_MODEL_ROUTING.md) | Cost optimization | Save costs |

---

## Your Stack, Your Rules

Claude Agent Framework automatically adapts to:

**Frontend:** React, Vue, Angular, Svelte, Next.js, Nuxt, SvelteKit
**Backend:** Node.js, Python, Go, Rust, Java, C#, Ruby
**Databases:** PostgreSQL, MySQL, MongoDB, Redis, SQLite
**Cloud:** AWS, GCP, Azure, Vercel, Netlify, Cloudflare
**Testing:** Jest, Pytest, Playwright, Cypress, Vitest
**AI/ML:** OpenAI, Anthropic, LangChain, HuggingFace, LocalLLMs

---

## The Philosophy

> "Start simple. Ship fast. Scale infinitely."

1. **Progressive Enhancement** - Start with basics, add complexity as needed
2. **Context Minimalism** - Load only what's essential
3. **Parallel Everything** - Why wait when agents can work together?
4. **Your Patterns First** - Adapt to your code, not the other way around

---

## Performance Metrics

| Metric | Traditional | Claude Agent Framework | Improvement |
|--------|------------|------------|-------------|
| Setup Time | 2+ hours | 2 minutes | 60x faster |
| Context Size | 250KB+ | <10KB | 97% smaller |
| Execution | Sequential | Parallel | 3-6x faster |
| Learning Curve | Days | Minutes | Instant |

---

## Getting Started

### Option 1: Instant Generation (Recommended)
```bash
claude> Use Claude Agent Framework SYSTEM_GENERATOR_PROMPT.md to set up my project
```

### Option 2: Guided Setup (30 min)
```bash
claude> Follow AGENT_SYSTEM_TEMPLATE.md for manual configuration
```

### Option 3: Full Customization (Advanced)
```bash
claude> Study CLAUDE_AGENT_FRAMEWORK.md and build custom system
```

---

## What's New in v2.0

### Slim-Down
- 9 files archived, 50% fewer root docs
- REGISTRY.json slimmed 64% (1,154 -> 421 lines)
- 10+ new Claude Code features integrated

### New Capabilities
- **Agent Teams**: Custom subagent types in `.claude/agents/`
- **Path-Specific Rules**: `.claude/rules/` with glob-based targeting
- **Auto Memory**: Persistent cross-conversation knowledge via MEMORY.md
- **Extended Context**: 1M token context window
- **MCP Tool Search**: Deferred tool loading via ToolSearch
- **Effort Levels**: `model: "haiku"` for fast/cheap, `model: "opus"` for complex
- **Worktree Isolation**: `isolation: "worktree"` for safe parallel work
- **Background Agents**: `run_in_background: true` for async execution
- **Managed Settings**: Centralized permission and model configuration
- **Skills with context:fork**: Branch context for skill execution

---

## Optional Patterns

### Observability
Track agent workflows with local SQLite-based monitoring. Zero cloud dependencies.
[Learn more ->](./.claude-library/observability/README.md)

### Hooks
Add deterministic control: auto-format, block dangerous operations, validate outputs.
[Learn more ->](./.claude-library/hooks/README.md)

Both patterns disabled by default. Zero overhead when off.

---

## Contributing

Claude Agent Framework is built from real-world patterns used in production:

- **Share your patterns** - Add to AGENT_PATTERNS.md
- **Submit improvements** - Make it better for everyone
- **Report issues** - Help us fix what's broken

---

## License

MIT License - Use freely in your projects, commercial or otherwise.

---

<div align="center">

**Stop reading. Start building.**

```bash
$ claude
> "Set up Claude Agent Framework for my project"
```

*Claude Agent Framework v2.0 | Built by developers, for developers*

[Documentation](./CLAUDE_AGENT_FRAMEWORK.md) | [Examples](./AGENT_PATTERNS.md) | [Support](https://github.com/ciscoittech/claude-agent-framework/issues)

</div>
