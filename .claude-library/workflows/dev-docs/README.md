# Dev Docs Workflow System

## Overview

The Dev Docs system prevents Claude from "losing the plot" during long implementations by creating persistent documentation that survives context compaction.

## Problem It Solves

**The Frustration**:
1. You plan a complex feature in planning mode
2. Claude creates a great plan
3. You exit planning mode
4. Implementation starts
5. Context fills up
6. You compact the conversation
7. 😱 Claude has forgotten the plan and key decisions
8. You have to re-explain everything
9. Implementation drifts from original approach

**The Solution**: Dev Docs System

## How It Works

### Three Essential Files

For each complex task, create three markdown files:

1. **plan.md**: Complete implementation roadmap
   - Executive summary
   - Phases with tasks
   - Technical approach
   - Testing strategy
   - Risks & mitigations
   - Success criteria

2. **context.md**: Critical context that must not be lost
   - Key file locations
   - Important decisions made
   - Patterns discovered
   - Technical constraints
   - Integration points
   - Next steps

3. **tasks.md**: Progress tracking checklist
   - All tasks in checkbox format
   - Grouped by phase
   - Marked complete as you go
   - Shows current position

### Storage Location

```
~/dev/active/[task-name]/
├── [task-name]-plan.md
├── [task-name]-context.md
└── [task-name]-tasks.md
```

Active tasks live in `~/dev/active/`, completed tasks move to `~/dev/archive/`.

## Commands

### /dev-docs

Creates dev docs from an accepted plan.

**Usage**:
```
/dev-docs "feature description"
/dev-docs  # Uses accepted plan from planning mode
```

**What it does**:
1. Launches strategic-plan-architect agent
2. Creates comprehensive implementation plan
3. Extracts key context into context.md
4. Converts plan to checkbox tasks in tasks.md
5. Saves all three files
6. Reports file locations to user

**When to use**:
- After exiting planning mode with accepted plan
- Before starting any multi-step feature (4+ tasks)
- When implementation will span multiple sessions
- For cross-service/repo changes

### /dev-docs-update

Updates context and tasks before compacting conversation.

**Usage**:
```
/dev-docs-update
/dev-docs-update [task-name]
```

**What it does**:
1. Detects active task (auto or specified)
2. Analyzes current state (git status, completed tasks)
3. Updates context.md with:
   - Files modified this session
   - Decisions made
   - Patterns discovered
   - Next steps
4. Updates tasks.md:
   - Marks completed tasks
   - Adds newly discovered tasks
   - Notes current position
5. Reports readiness for compaction

**When to use**:
- Before every context compaction
- After completing major phases
- End of work session
- When context >80% full

## Workflow Example

### Setup Phase
```
User: "I need to build a user authentication system"

1. Enter planning mode
2. Research and create comprehensive plan
3. User reviews plan: "Looks good!"
4. Exit planning mode
5. Immediately run: /dev-docs
6. Files created in ~/dev/active/user-authentication-system/
```

### Implementation Phase
```
7. Start Phase 1 tasks
8. Check off tasks in tasks.md as you complete them
9. Reference context.md for key decisions
10. Keep implementing...
11. Context reaches 80%
12. Run: /dev-docs-update
13. Compact conversation
```

### Continuation Phase
```
14. New session starts
15. User: "continue the auth system"
16. Load dev docs from ~/dev/active/user-authentication-system/
17. Resume EXACTLY where left off
18. Continue checking off tasks
19. Repeat update/compact cycle as needed
```

### Completion Phase
```
20. All tasks complete
21. Feature fully implemented
22. Archive: mv ~/dev/active/user-auth-system ~/dev/archive/
23. Clean active directory
```

## Templates

Located in `templates/` directory:

- `plan-template.md`: Structure for implementation plans
- `context-template.md`: Structure for context files
- `tasks-template.md`: Structure for task checklists

These templates are used by the `/dev-docs` command to create consistent documentation.

## Best Practices

### Planning
- ✅ Always plan complex tasks (4+ steps)
- ✅ Review plans thoroughly before implementation
- ✅ Create dev docs immediately after planning
- ✅ Keep plans specific and actionable

### Implementation
- ✅ Check off tasks as you complete them
- ✅ Update context.md when making key decisions
- ✅ Reference plan.md to stay on track
- ✅ Run /dev-docs-update before compacting

### Context Updates
- ✅ Capture file locations and what they do
- ✅ Document architectural decisions and why
- ✅ Note patterns discovered in codebase
- ✅ Write clear, actionable next steps
- ❌ Don't over-document low-level details

### Organization
- ✅ One task directory per feature
- ✅ Clear, descriptive task names (lowercase-with-hyphens)
- ✅ Archive completed tasks
- ✅ Keep active directory focused

## Integration with Other Systems

### With Planning Mode
1. Use planning mode to create detailed plan
2. Exit with accepted plan
3. Run /dev-docs to persist the plan
4. Implement with confidence

### With Agent System
- strategic-plan-architect agent creates comprehensive plans
- Agent launcher suggests dev docs for complex tasks
- Quality control hooks reference dev docs for context

### With Skills
- Skills provide implementation patterns
- Dev docs capture which patterns were chosen
- Context preserves rationale for pattern selection

## Success Indicators

You know dev docs are working when:
- ✅ No "What was I doing?" moments after compaction
- ✅ Implementation follows the plan consistently
- ✅ Context loss is zero across sessions
- ✅ Tasks progress systematically
- ✅ User doesn't need to re-explain goals

## Configuration

In REGISTRY.json:
```json
{
  "dev_docs": {
    "enabled": true,
    "workflow_path": ".claude-library/workflows/dev-docs/",
    "active_docs_path": "~/dev/active/",
    "archive_docs_path": "~/dev/archive/",
    "auto_suggest_complex_tasks": true,
    "complexity_threshold": 4
  }
}
```

## Real-World Impact

### Before Dev Docs
- Context loss every compaction
- Implementation drift from original plan
- Repeated re-explanations
- Wasted time on wrong approaches

### After Dev Docs
- Zero context loss
- Implementation stays on track
- Seamless continuity across sessions
- Systematic progress

**Result**: Solo developer rewrote 300k LOC across multiple sessions without losing track.

---

*This workflow system is battle-tested from 6 months of real-world usage on large codebases.*
