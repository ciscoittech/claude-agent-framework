# /dev-docs-update Command

## Purpose
Update dev docs before compacting conversation to ensure perfect continuity. Captures current state, completed tasks, new discoveries, and next steps so you can seamlessly resume after compaction.

## Usage
```
/dev-docs-update
/dev-docs-update [task-name]
```

If no task-name provided, will auto-detect from `~/dev/active/`.

## When to Use

### Always Use Before:
- ⚠️ Context getting full (>80%)
- ⚠️ Auto-compaction triggered
- ⚠️ End of work session
- ⚠️ Major phase completion
- ⚠️ Before long break from task

### Also Use After:
- ✅ Discovering important new context
- ✅ Making key architectural decisions
- ✅ Completing several tasks
- ✅ Finding critical files/patterns

## What Gets Updated

### Context File Update
**Adds/Updates**:
- **New Files Discovered**: Files you've worked with since last update
- **Decisions Made**: Architecture/implementation choices
- **Patterns Identified**: Code patterns discovered
- **Technical Constraints**: Limitations found
- **Integration Discoveries**: How systems connect
- **Next Steps**: What to do when resuming

**Format**:
```markdown
## Recent Updates

### [Timestamp] - Session [N]

**Files Modified**:
- `src/auth/service.ts`: Added JWT token generation
- `src/middleware/auth.ts`: Created auth middleware

**Decisions Made**:
- Using bcrypt for password hashing (SALT_ROUNDS=10)
- JWT expiry: 15min access, 7day refresh
- Storing refresh tokens in database

**Patterns Discovered**:
- BaseController pattern for error handling
- Repository pattern for database access
- ServiceResponse<T> for consistent returns

**Constraints**:
- Must maintain backwards compatibility with old auth
- Need to handle migration of existing users
- Rate limiting required per user

**Next Steps**:
1. Complete Phase 2 Task 3 (Refresh token rotation)
2. Add integration tests
3. Update API documentation

**Last Updated**: [Timestamp]
```

### Tasks File Update
**Updates**:
- ✅ Mark completed tasks as checked
- 📝 Add newly discovered tasks
- 🔄 Update task descriptions with specifics
- 📍 Note current position in plan

**Example Update**:
```markdown
## Phase 1: Authentication Service ✅ COMPLETE

- [x] Create User model with Prisma
- [x] Add password hashing utility
- [x] Implement registration endpoint
- [x] Add email validation

## Phase 2: JWT Token Management 🔄 IN PROGRESS

- [x] Generate access tokens
- [x] Generate refresh tokens
- [ ] Implement token rotation (CURRENT)
- [ ] Add token blacklisting
- [ ] Store refresh tokens in DB

## Phase 3: Integration (Added during implementation)

- [ ] Create auth middleware
- [ ] Protect existing routes
- [ ] Add logout endpoint
```

### Plan File (Usually Not Modified)
The plan typically stays stable, but may note:
- Scope changes approved by user
- Major pivots in approach

## Workflow

### Step 1: Detect Active Task
```bash
# Look in ~/dev/active/ for task directories
# If multiple, ask user which one
# If single, use that automatically
```

### Step 2: Analyze Current State
**Check**:
- Git status for modified files
- Completed vs pending tasks
- Current phase/progress

**Gather**:
- Recent commits (if any)
- Files edited this session
- New files created

### Step 3: Update Context File
**Add Section** with:
- Timestamp
- Session number (if tracking)
- All updates (files, decisions, patterns, constraints, next steps)

**Format** for easy scanning and continuity.

### Step 4: Update Tasks File
**Mark Complete**:
- Tasks finished this session
- Use ✅ checkmark

**Add New**:
- Discovered subtasks
- Unexpected work items

**Note Current**:
- Which task you're on
- What's in progress

### Step 5: Validate Updates
**Check**:
- Are next steps clear?
- Is current state obvious?
- Can you resume from just reading these files?

### Step 6: Report
Show user:
- What was updated
- Current progress
- Next steps summary
- Readiness for compaction

## Example Output

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 DEV DOCS UPDATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Task: user-authentication-system

Files Updated:
  📄 user-authentication-system-context.md
  ☑️  user-authentication-system-tasks.md

Progress:
  ✅ Phase 1: Complete (4/4 tasks)
  🔄 Phase 2: In Progress (2/5 tasks)
  ⏳ Phase 3: Not Started (0/3 tasks)

This Session:
  - Completed JWT token generation
  - Discovered BaseController pattern
  - Added refresh token database schema
  - Started token rotation implementation

Next Steps Documented:
  1. Complete refresh token rotation
  2. Add token blacklisting
  3. Write integration tests

🎯 You're ready to compact! These docs will bring you
   right back to this exact point.

Last Updated: 2025-01-13 15:42:00 UTC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Smart Detection

### Auto-Detect Recent Work
Uses multiple signals:
1. **Git**: `git diff --name-only` for modified files
2. **Timestamps**: Recently touched files
3. **Edit Tracking**: Hook logs (if quality-control enabled)

### Infer Completed Tasks
Compares:
- Tasks in tasks.md
- Files that exist/were modified
- Test status
- Build success

**Example**: If task says "Create User model" and `prisma/schema.prisma` has User model → Mark complete

## Context Compaction Workflow

**The Ideal Flow**:

```
[Working on implementation]
  ↓
[Context reaches 80%]
  ↓
[Claude suggests: "Context getting full. Run /dev-docs-update?"]
  ↓
[User runs /dev-docs-update]
  ↓
[Docs updated with current state]
  ↓
[User compacts conversation]
  ↓
[New session starts]
  ↓
[User: "continue the user auth task"]
  ↓
[Claude reads dev docs]
  ↓
[Resumes EXACTLY where left off]
  ↓
[No context lost! 🎉]
```

## Best Practices

### Update Frequency
- **Minimum**: Before every compaction
- **Recommended**: After completing each phase
- **Ideal**: After every 2-3 tasks completed

### What to Capture
**DO capture**:
- ✅ File locations and what they do
- ✅ Architectural decisions and why
- ✅ Patterns discovered in codebase
- ✅ Technical constraints hit
- ✅ Next concrete steps

**DON'T capture**:
- ❌ Low-level code details (that's in the files)
- ❌ Obvious next steps from the plan
- ❌ General knowledge
- ❌ Excessive detail

### Next Steps Quality
**Bad next step**:
❌ "Continue implementation"

**Good next step**:
✅ "Implement `rotateRefreshToken()` method in `AuthService.ts`: (1) Invalidate old token in DB, (2) Generate new token, (3) Update user session, (4) Return new token pair"

## Integration with Other Systems

### With Quality Control Hooks
If enabled, can read edit tracking log to know exactly what was modified.

### With Git
Reads `git status` and `git diff --name-only` to detect changes.

### With Planning System
Maintains sync between plan and actual progress.

## Troubleshooting

### Multiple Active Tasks
If `~/dev/active/` has multiple task directories:
- Lists them
- Asks user which one to update
- Or specify in command: `/dev-docs-update task-name`

### No Active Tasks
If no dev docs found:
- Suggests running `/dev-docs` first
- Or helps create docs for current work

### Stale Docs
If docs haven't been updated in a while:
- Notes the gap in time
- Captures everything since last update
- May suggest reviewing what happened

## Success Metrics

Dev docs updates are working when:
- ✅ You can resume after compaction without re-explaining
- ✅ Next steps are immediately clear
- ✅ No "what was I doing?" moments
- ✅ Context loss is zero
- ✅ Implementation stays on track

## Related Commands

- **/dev-docs**: Create initial dev docs
- Planning mode: Create the original plan
- **strategic-plan-architect**: Deep planning

---

**The #1 cause of implementation drift**: Losing context across sessions.

**The solution**: Disciplined dev docs updates. This command makes it effortless.

**Habit to build**: Before clicking "Compact" → Run `/dev-docs-update` → Then compact with confidence.
