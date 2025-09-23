# Claude Agent Framework Launcher

Agent launcher for framework meta-development. Routes requests to specialized framework agents.

## Project
- **Framework**: Claude Agent Framework
- **Mode**: Meta-implementation (framework develops itself)
- **Agents**: Loaded from `.claude-library/`

## Commands
- `/pattern "desc"` - Create/improve agent patterns
- `/validate` - Test framework components
- `/example "stack"` - Generate examples
- `/test-framework` - Self-test framework

## Agent Selection
- **Pattern work**: architect + engineer + reviewer
- **Validation**: validation-engineer + reviewer
- **Examples**: example-generator + docs + validator
- **Documentation**: docs-specialist + reviewer

## Context Loading
Base: `framework-architecture.md`
+ Pattern: `framework-development-patterns.md`
+ Performance: `performance-optimization.md`

## Routing
Keywords → Agents via REGISTRY.json → Load contexts → Execute workflow

Ready for framework development coordination.