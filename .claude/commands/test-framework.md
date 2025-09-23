# /test-framework Command

Comprehensive self-testing of the Claude Agent Framework.

## Usage
`/test-framework` or `/test-framework --quick`

## Workflow
1. **Planning** (10s): Load test coordinator
2. **Testing** (90s): Load multiple testers in parallel
3. **Analysis** (15s): Load results analyst

## Test Areas
- Core functionality
- Performance benchmarks
- Pattern validation
- Meta-framework testing
- Integration testing

## Agents
- framework-validation-engineer
- framework-code-reviewer

## Contexts
- framework-architecture.md
- performance-optimization.md
- framework-development-patterns.md

Target: 115s total execution time.