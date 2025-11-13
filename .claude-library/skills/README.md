# Skills System with Auto-Activation

## Overview

Skills provide Claude with domain-specific best practices, patterns, and guidelines. The auto-activation system ensures skills are actually used by analyzing prompts and file context to suggest relevant skills automatically.

## The Problem

**Skills sit unused** unless manually referenced. This defeats their purpose.

## The Solution

**Auto-activation hooks** that:
1. Analyze user prompts for keywords and intent patterns
2. Check modified files against skill triggers
3. Inject activation reminders before Claude sees the prompt
4. Track activations for continuous improvement

## How It Works

### Trigger Configuration

`skill-rules.json` defines activation rules for each skill:

```json
{
  "skills": {
    "frontend-dev-guidelines": {
      "promptTriggers": {
        "keywords": ["react", "component", "UI", "styling"],
        "intentPatterns": [
          "(create|add).*?(component|page)",
          "(style|design).*?UI"
        ]
      },
      "fileTriggers": {
        "pathPatterns": ["**/src/components/**/*.{ts,tsx}"],
        "contentPatterns": ["import.*react", "useState"]
      },
      "activationMessage": "🎯 Consider using frontend-dev-guidelines skill"
    }
  }
}
```

### Activation Flow

```
User types prompt
    ↓
UserPromptSubmit hook triggers
    ↓
skill_activator.py analyzes:
  - Prompt keywords
  - Intent patterns
  - Modified files
  - File content
    ↓
Matching skills identified
    ↓
Activation message injected
    ↓
Claude sees prompt + skill suggestion
    ↓
Claude loads relevant skill
```

### Example

```
User: "Create a React component for user profiles"

[Hook analyzes]
✓ Keyword match: "React", "component"
✓ Intent pattern: "(create|add).*?component"
✓ High confidence: 0.85

[Injects message]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SKILL ACTIVATION CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Consider using frontend-dev-guidelines skill
Reason: Prompt keywords matched
Location: .claude-library/skills/frontend-dev-guidelines/

💡 Skills provide context-specific best practices.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Claude sees both and loads the skill]
```

## Skill Structure (Anthropic Best Practice)

### Progressive Disclosure

**Main SKILL.md**: <500 lines
- Overview
- Core principles
- Quick patterns
- Common anti-patterns
- Links to resources

**resources/ directory**: Detailed guides
- In-depth pattern explanations
- Advanced techniques
- Edge cases
- Performance optimization

**Why?**
- Faster initial loading
- Better token efficiency
- Load details only when needed
- Easier to maintain

### Example Structure

```
frontend-dev-guidelines/
├── SKILL.md                    # <500 lines overview
├── resources/
│   ├── react-patterns.md      # Advanced React patterns
│   ├── state-management.md    # State strategies
│   ├── performance.md         # Performance optimization
│   ├── testing.md            # Testing guide
│   └── styling.md            # Styling approaches
└── examples/
    ├── component-example.tsx  # Real examples
    └── hook-example.ts
```

## Creating Your First Skill

### 1. Create Directory Structure

```bash
mkdir -p .claude-library/skills/my-skill/{resources,examples}
```

### 2. Write SKILL.md

Keep under 500 lines:

```markdown
# My Skill Name

## Overview
Brief description of what this skill covers.

**When to use**: Specific scenarios

## Core Principles
1. Principle 1
2. Principle 2
3. Principle 3

## Quick Patterns

### Pattern 1
\`\`\`typescript
// Example code
\`\`\`

### Pattern 2
\`\`\`typescript
// Example code
\`\`\`

## Common Anti-Patterns

### ❌ DON'T
\`\`\`typescript
// Bad example
\`\`\`

### ✅ DO
\`\`\`typescript
// Good example
\`\`\`

## Resources

For detailed guides:
- `resources/deep-dive.md`
- `resources/advanced.md`

## Quick Reference

Key points for quick lookup
```

### 3. Add to skill-rules.json

```json
{
  "skills": {
    "my-skill": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "high",
      "promptTriggers": {
        "keywords": [
          "keyword1", "keyword2", "keyword3"
        ],
        "intentPatterns": [
          "regex pattern 1",
          "regex pattern 2"
        ]
      },
      "fileTriggers": {
        "pathPatterns": [
          "**/path/pattern/**/*.ext"
        ],
        "contentPatterns": [
          "import pattern",
          "code pattern"
        ]
      },
      "activationMessage": "🎯 Consider using my-skill"
    }
  }
}
```

### 4. Test Activation

```
# Try a prompt with your keywords
"I need to [keyword1] for [keyword2]"

# Check if activation message appears
# Adjust keywords/patterns if needed
```

## Existing Skills

### frontend-dev-guidelines
**Covers**: React, components, hooks, state management, styling, performance

**Triggers**:
- Keywords: react, component, UI, hooks, state
- Files: `**/components/**/*.{tsx,jsx}`

### backend-dev-guidelines
**Covers**: APIs, routes, controllers, services, repositories, error handling

**Triggers**:
- Keywords: backend, API, endpoint, service, database
- Files: `**/api/**/*.{ts,js}`

### workflow-developer
**Covers**: Workflow automation, state machines, pipelines

**Triggers**:
- Keywords: workflow, automation, pipeline, orchestration

### database-specialist
**Covers**: Schema design, queries, migrations, optimization

**Triggers**:
- Keywords: database, SQL, query, migration, schema
- Files: `**/migrations/**/*.sql`, `prisma/schema.prisma`

### testing-specialist
**Covers**: Unit tests, integration tests, mocking, coverage

**Triggers**:
- Keywords: test, testing, spec, mock, coverage
- Files: `**/*.test.{ts,js}`, `**/__tests__/**`

## Configuration

In REGISTRY.json:

```json
{
  "settings": {
    "skills": {
      "enabled": false,              // DEFAULT: OFF
      "auto_activation": true,
      "config_path": ".claude-library/skills/skill-rules.json",
      "progressive_disclosure": true,
      "max_simultaneous": 3
    },
    "hooks": {
      "enabled": false,              // DEFAULT: OFF
      "configs": [
        ".claude-library/hooks/configs/skill-activation.json"
      ]
    }
  }
}
```

**Enable both** for auto-activation to work.

## Best Practices

### Skill Writing
- ✅ Keep main file <500 lines
- ✅ Use progressive disclosure (link to resources)
- ✅ Provide code examples
- ✅ Show both good and bad patterns
- ✅ Include quick reference section
- ❌ Don't dump everything in one file
- ❌ Don't be too generic

### Trigger Configuration
- ✅ Use specific, relevant keywords
- ✅ Test intent patterns with real prompts
- ✅ Match file paths users actually work with
- ✅ Update based on activation logs
- ❌ Don't use overly broad keywords
- ❌ Don't over-trigger (balance precision/recall)

### Organization
- ✅ One skill per major domain
- ✅ Group related resources
- ✅ Provide real examples
- ✅ Keep skills focused
- ❌ Don't create skills for everything
- ❌ Don't duplicate content across skills

## Metrics & Optimization

### Activation Logs

Located at: `.claude-metrics/skill-activations.log`

Format:
```
2025-01-13T10:30:00Z | Skills: [frontend-dev-guidelines] | Prompt: Create React component...
2025-01-13T10:45:00Z | Skills: [backend-dev-guidelines, database-specialist] | Prompt: Add user...
```

### Optimization Process

1. **Monitor logs**: Which skills activate most?
2. **Check false positives**: Skills activating unnecessarily?
3. **Check false negatives**: Skills not activating when should?
4. **Adjust triggers**: Refine keywords and patterns
5. **Repeat**: Continuous improvement

### Success Metrics

- **Activation rate**: >80% when relevant skills exist
- **False positive rate**: <10%
- **User feedback**: "Skills are actually being used"
- **Code consistency**: Patterns followed consistently

## Integration with Other Systems

### With Dev Docs
- Skills provide implementation patterns
- Dev docs capture which patterns chosen
- Context preserves rationale

### With Quality Control
- Skills define what "quality" means for domain
- Hooks check adherence
- Reminders reference skill guidelines

### With Planning
- Planning uses skills for technical approach
- Skills inform architectural decisions
- Consistency from plan to implementation

## Real-World Impact

### Before Auto-Activation
- Skills rarely used
- Inconsistent code patterns
- Had to manually reference guidelines
- Wasted skill creation effort

### After Auto-Activation
- Skills activate >80% of the time
- Consistent patterns everywhere
- Automatic best practice enforcement
- Skills actually deliver value

**Result**: 1,500+ lines of guidelines actually being followed consistently.

---

*Skills system based on 6 months of refinement in a 300k LOC production codebase.*
