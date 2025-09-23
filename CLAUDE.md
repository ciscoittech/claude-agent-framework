# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Claude Agent Framework is a comprehensive system for building intelligent multi-agent development systems. It provides templates, patterns, and prompts to create optimized agent systems that leverage Claude Code's parallel execution capabilities.

## Key Framework Components

### Core Documentation Files (In Order of Use)

1. **SYSTEM_GENERATOR_PROMPT.md**: Auto-generation prompt for instant agent system setup (start here for 2-minute setup)
2. **CLAUDE_AGENT_FRAMEWORK.md**: Complete framework guide with architecture, principles, and workflow patterns
3. **AGENT_PATTERNS.md**: Real-world implementation patterns for parallel execution, TDD workflows, and error handling
4. **AGENT_SYSTEM_TEMPLATE.md**: Quick-start templates for manual agent system setup (30-60 minute alternative)

### Specialized Documentation

- **PROJECT_ANALYZER_PROMPT.md**: Intelligent project analysis for complex codebases - use when the basic generator needs more sophisticated analysis
- **AGENT_REFERENCE_PATTERNS.md**: Combines Anthropic's "Building Effective Agents" principles with framework patterns - explains workflows vs agents distinction and provides decision trees
- **ANTHROPIC_TEAM_PATTERNS.md**: Real-world production patterns from Anthropic teams - includes parallel instance strategies, auto-accept modes, and team-specific workflows

## Working with the Framework

### Recommended Reading Order

The framework documentation should be read in this sequence:

1. **Start**: `SYSTEM_GENERATOR_PROMPT.md` - Get working system immediately (2 minutes)
2. **Learn**: `CLAUDE_AGENT_FRAMEWORK.md` - Understand the principles
3. **Customize**: `AGENT_PATTERNS.md` - Advanced implementation patterns
4. **Manual**: `AGENT_SYSTEM_TEMPLATE.md` - Step-by-step templates for manual setup

### Primary Use Case: Agent System Generation

When users want to create an agent system for their project:

1. Direct them to use the `SYSTEM_GENERATOR_PROMPT.md` for automatic generation
2. The generator will analyze their project's CLAUDE.md and codebase
3. It creates a complete `.claude/` and `.claude-library/` structure
4. The system will be customized for their specific tech stack

### Three Implementation Approaches

**Option 1: Instant Generation (Recommended)**
- Use `SYSTEM_GENERATOR_PROMPT.md`
- 2-minute setup
- Fully automated

**Option 2: Manual Setup**
- Follow `AGENT_SYSTEM_TEMPLATE.md`
- 30-60 minutes
- More control over configuration

**Option 3: Deep Customization**
- Study `CLAUDE_AGENT_FRAMEWORK.md`
- Use `AGENT_PATTERNS.md` for advanced patterns
- Build completely custom system

### Framework Architecture

The framework follows these principles:
- **Minimal auto-loading**: `.claude/` folder < 10KB, `.claude-library/` for on-demand loading
- **Agent specialization**: Each agent has single responsibility with clear boundaries
- **Parallel execution**: Leverages Claude Code's Task tool for 3-6x performance gains
- **Progressive complexity**: Start simple, scale as needed

### Agent System Structure

Generated systems follow this pattern:
```
.claude/                    # Minimal auto-loaded
├── agent-launcher.md      # Dynamic agent router
├── settings.json          # Project metadata
└── commands/              # User workflows

.claude-library/           # On-demand library
├── REGISTRY.json         # Central configuration
├── agents/               # Specialized agents
└── contexts/             # Project knowledge
```

## Common Development Tasks

### Adding New Patterns
When adding new patterns to `AGENT_PATTERNS.md`:
- Document with real-world examples
- Include performance metrics
- Show both sequential and parallel approaches

### Updating Generator Prompts
When modifying `SYSTEM_GENERATOR_PROMPT.md`:
- Test with multiple tech stacks
- Ensure compatibility with Claude Code's Task tool
- Maintain <10KB constraint for `.claude/` folder

### Framework Documentation Updates
When updating core documentation:
- Keep examples concrete and actionable
- Include performance comparisons
- Document failure modes and recovery strategies

## Performance Optimization Targets

The framework aims for:
- 97% reduction in auto-loaded context (250KB → 8KB)
- 3x faster execution through parallel agents
- <2 minute setup time for new projects
- Support for any tech stack without modification