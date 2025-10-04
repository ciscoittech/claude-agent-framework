# The Solo SaaS Builder: Complete Business & Product Workflow

## Your Complete End-to-End Process

---

# Part 1: Core Workflow Overview

```
IDEA
  ↓
[5 min] Stage 1: Idea Intake & Clarification
  ↓
[2 min] Stage 2: Stack Compatibility Check
  ↓
  ├─ REJECT → Document why + move on
  └─ PASS ↓
  
[3 min] Stage 2.5: Stack Recommendation + HUMAN APPROVAL
  ↓
[2 min] Stage 3: Agent Validation Check
  ↓
  ├─ Skip → Go to Stage 5
  └─ Build Agent ↓
  
[1-4 hrs] Stage 4: Agent Prototype & Validation
  ↓
  ├─ FAIL → Document learnings + pivot/reject
  └─ SUCCESS ↓
  
[30-60 min] Stage 5: Product Spec Generation (AI-assisted)
  ↓
[10 min] Stage 6: GitHub Issues Creation (AI-structured)
  ↓
[Ongoing] Stage 7: AI Coding Agent Execution
  ↓
SHIP
```

**Total Time: Idea → First Commit = 4-6 hours**

---

# Part 2: Your Technical Constraints (Decision Filters)

## Stack Options (These are your ONLY choices)

### Stack A: Makerkit Next.js Supabase Turbo
**When:** Standard SaaS, need speed, auth/billing/teams out of box
**Time to MVP:** 1-2 weeks
**Pre-built:** Auth, billing, multi-tenancy, admin (40+ hours saved)
**Database:** Supabase Postgres (included)
**Deployment:** Cloudflare Workers
**License:** Unlimited (no cost concern)

### Stack B: Laravel 11 + Inertia + React
**When:** Complex business logic, background jobs, need Laravel ecosystem
**Time to MVP:** 3-4 weeks
**Database:** SQLite (dev) → Postgres on Vultr VPS (production)
**AI Support:** pgvector on Postgres
**Deployment:** Vultr VPS + Cloudflare CDN
**Management:** Laravel Forge (recommended)

### Stack C: FastAPI (AI Features Only)
**When:** Need AI/ML features alongside Stack A or B
**Purpose:** LLM integrations, embeddings, ML inference
**Deployment:** Cloudflare Workers Python OR Railway
**Integration:** API calls from main stack

### Stack D: Claude Code (Validation Only)
**When:** Testing APIs, validating workflows, cost estimation
**Purpose:** Prove feasibility before building
**Output:** Observability reports, real data, go/no-go decision

## Hard Constraints (AUTO-REJECT)
- ❌ Native mobile apps (suggest PWA or reject)
- ❌ Desktop apps
- ❌ Video/audio processing
- ❌ Blockchain/Web3
- ❌ IoT/Hardware
- ❌ Gaming
- ❌ Next.js from scratch (use Makerkit)
- ❌ Laravel API mode first (Inertia first)
- ❌ Deploy to Vercel (Cloudflare only)
- ❌ Separate vector DB (use pgvector)

---

# Part 3: Stage-by-Stage Workflow

## STAGE 1: Idea Intake (5-10 minutes)
**Role:** You (Founder/Product)
**AI Role:** Interview assistant

### Process:
1. AI asks clarifying questions:
   - What problem are you solving?
   - Who has this problem?
   - What's the core feature?
   - How do users interact with it?
   - What technical components needed?
   - Success metrics?

2. You answer naturally

3. AI synthesizes into structured summary

### Output Document: "Idea Summary"
```
Problem: [1 paragraph]
Target User: [Who]
Solution: [What we're building]
Core Feature: [The ONE thing that must work]
Technical Needs: [APIs, real-time, AI, etc.]
Success Metrics: [How we measure]
```

**Decision Point:** Does this idea excite you? 
- No → Stop here, save the time
- Yes → Continue to Stage 2

---

## STAGE 2: Stack Compatibility Check (2 minutes)
**Role:** AI Agent
**Your Role:** Await results

### Decision Logic:
```
Does idea require:
├─ Native mobile? → REJECT
├─ Desktop app? → REJECT  
├─ Technologies outside stack? → REJECT
├─ Web application? 
    ├─ YES → Which stack?
    │   ├─ Standard SaaS features? → Makerkit
    │   ├─ Complex background jobs? → Laravel
    │   ├─ Want speed? → Makerkit
    │   └─ Need Laravel ecosystem? → Laravel
    └─ NO → REJECT
```

### Output: "Stack Compatibility Report"

**If PASS:**
```
✅ STACK FIT: YES

Fits: [Makerkit OR Laravel]
Why: [3 specific reasons]
Concerns: [Any limitations to consider]

→ Proceeding to Stack Recommendation
```

**If REJECT:**
```
❌ STACK FIT: NO

Doesn't fit because: [Reason]
Would need: [Technology outside your stack]

Options:
1. Pivot to: [Modified version that fits]
2. Don't build: [Why it's not worth forcing]

My recommendation: [Agent's honest take]

→ WORKFLOW STOPPED
```

---

## STAGE 2.5: Stack Recommendation (3 minutes + Human Decision)
**Role:** AI Agent recommends, YOU decide
**Critical:** This is the ONLY human checkpoint before building

### AI Presents:

```
RECOMMENDED STACK: [Makerkit OR Laravel]

Why this stack:
1. [Business reason]
2. [Technical reason]  
3. [Time/complexity reason]

Comparison:
| Need | Makerkit | Laravel | Winner |
|------|----------|---------|--------|
| Speed to market | 1 week | 3 weeks | Makerkit |
| [Your need] | [Assessment] | [Assessment] | [Winner] |

Time estimates:
- Makerkit: [X weeks]
- Laravel: [Y weeks]

My recommendation: [Stack] because [reason]
```

### Your Decision Required:

**Questions to answer:**
1. Do you approve this stack? (Yes/No)
2. Any concerns about the choice?
3. Timeline acceptable?

**If Laravel selected:**
- Deployment: Laravel Forge or Manual?
- Confirm ecosystem tools (Queues, Cashier, Reverb, etc.)

**If Makerkit selected:**
- Any customizations you know you'll need?

### Once Approved:
```
✅ STACK APPROVED: [Your choice]

Configuration:
- [Specific setup details]
- [Tools included]
- [Timeline confirmed]

→ Proceeding to Agent Validation Check
```

**This is your LAST chance to change direction before work begins**

---

## STAGE 3: Agent Validation Check (2 minutes)
**Role:** AI Agent
**Decision:** Should we prototype first?

### Decision Logic:
```
Does the core feature involve:
├─ External API integrations? → BUILD AGENT
├─ Web scraping? → BUILD AGENT
├─ Workflow with unknown feasibility? → BUILD AGENT
├─ Third-party services to test? → BUILD AGENT
├─ Complex data processing? → BUILD AGENT
├─ Standard CRUD operations? → SKIP AGENT
└─ Features you've built before? → SKIP AGENT
```

### Output:

**If BUILD AGENT:**
```
🤖 AGENT VALIDATION RECOMMENDED

Why: [Specific risk this will mitigate]

Agent will test:
1. [Specific thing - e.g., "Twitter API rate limits"]
2. [Specific thing - e.g., "Data quality"]
3. [Specific thing - e.g., "Cost per operation"]

Time: 1-4 hours
Confidence gain: 80-90% before writing production code

→ Proceeding to Agent Prototype Build
```

**If SKIP AGENT:**
```
⏭️ SKIPPING AGENT VALIDATION

Why: [This is straightforward/proven/standard]

→ Proceeding directly to Spec Generation
```

---

## STAGE 4: Agent Prototype Build (1-4 hours)
**Role:** Claude Code builds and runs
**Your Role:** Provide API keys, review results

### Process:

**Step 1: AI generates Claude Code prompt**
```
Complete prompt with:
- Objective (what to validate)
- Tasks (specific actions)
- Success criteria
- Observability requirements
- Output format
```

**Step 2: You run prompt in Claude Code**
- Agent builds working prototype
- Agent executes against real APIs
- Agent encounters real problems
- Agent logs everything
- Agent generates report

**Step 3: Agent returns findings**

### Output: "Agent Validation Report"

```
FINDINGS SUMMARY

✅ What Worked:
- [Specific success 1]
- [Specific success 2]

❌ What Broke:
- [Specific failure 1]
- [Specific failure 2]

⚠️ Edge Cases Found:
- [Edge case 1]
- [Edge case 2]

📊 Metrics:
- Timing: [Real numbers]
- Cost: [Real costs]
- Success Rate: [Real percentage]
- API Limits: [What we hit]

RECOMMENDATION: [GO / NO-GO / PIVOT]

Reasoning: [Why this decision]
```

### Your Decision:

**If GO:**
```
✅ Validated - Building with confidence

Known challenges: [List]
Mitigation plans: [How we'll handle each]

→ Proceeding to Spec Generation with real data
```

**If NO-GO:**
```
❌ Not feasible

Deal-breakers: [What can't be solved]

Options:
1. Pivot to: [Modified approach]
2. Kill idea: [Why not worth it]

→ WORKFLOW STOPPED (saved 2-4 weeks)
```

**If PIVOT:**
```
🔄 Needs adjustment

Changes required: [What to modify]
Impact: [How this affects scope]

→ Return to Stage 2.5 with new requirements
```

---

## STAGE 5: Product Spec Generation (30-60 minutes)
**Role:** AI generates, YOU review and approve
**Output:** Complete product specification

### AI generates based on:
- Stage 1: Idea details
- Stage 2: Stack selection
- Stage 4: Agent findings (if applicable)
- Your domain knowledge

### Document Structure:

```
PRODUCT SPECIFICATION: [Product Name]

1. EXECUTIVE SUMMARY
   - One-liner
   - Problem statement
   - Solution overview
   - Target user
   - Success metrics

2. PRODUCT VISION
   - What we're building
   - Why it's different
   - Success looks like

3. FEATURES (Priority-ordered)
   MVP Features (Must Have):
   - Feature 1: [Why critical]
   - Feature 2: [Why critical]
   - Feature 3: [Why critical]
   
   Post-MVP (Should Have):
   - [List]
   
   Future (Nice to Have):
   - [List]
   
   Out of Scope:
   - [What we're NOT building]

4. USER FLOWS
   Primary Flow:
   1. User does [action]
   2. System responds [response]
   3. User sees [result]
   
   Edge Cases:
   - [How we handle errors]

5. TECHNICAL ARCHITECTURE
   Stack: [Approved stack from Stage 2]
   
   Components:
   - Frontend: [What/how]
   - Backend: [What/how]
   - Database: [Tables needed]
   - External Services: [APIs we'll use]
   - AI Services: [If applicable]
   
   Agent Findings Integration:
   - [Key learnings from Stage 4]
   - [How they influence architecture]

6. SUCCESS METRICS
   Launch Metrics (Week 1):
   - [Specific numbers]
   
   Month 1 Metrics:
   - [Specific numbers]

7. RISKS & MITIGATION
   Risk: [From agent testing or experience]
   - Impact: [High/Med/Low]
   - Mitigation: [How we handle]

8. TIMELINE
   Week 1-2: [Milestones]
   Week 3-4: [Milestones]
   Week 5-6: [Milestones]
   
   Total Time to MVP: [Estimate]
```

### Your Review:
- Does this capture the vision?
- Are priorities right?
- Timeline realistic?
- Anything missing?

**Approve to proceed to Stage 6**

---

## STAGE 6: GitHub Issues Creation (10 minutes)
**Role:** AI generates structured issues
**Output:** Ready-to-build task list

### AI creates issues in this format:

**Issue Structure (AI Agent-Friendly):**
```
ISSUE #1: [Clear, specific title]

## Context
[Why this task exists, how it fits in the product]

## Acceptance Criteria
- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]

## Technical Approach
[High-level approach - what needs to be built]

## Dependencies
- Depends on: #[issue number]
- Blocks: #[issue number]

## Stack Context
- Using: [Makerkit OR Laravel]
- Database: [Supabase OR Postgres]
- [Other relevant stack details]

## Files Likely Needed
- [Approximate file paths]
- [Component locations]

## Time Estimate
[X hours]

## Testing Requirements
- [ ] [How to verify it works]

## Notes
[Any special considerations from agent testing]
```

### Issue Organization:

**Labels:**
- `mvp` - Must have for launch
- `post-mvp` - Can wait until after launch
- `frontend` - UI work
- `backend` - Server/API work
- `database` - Schema changes
- `integration` - External services
- `ai-feature` - AI/ML work
- `blocked` - Waiting on something

**Milestones:**
- Sprint 1 (Week 1-2)
- Sprint 2 (Week 3-4)
- Sprint 3 (Week 5-6)

**Project Boards:**
```
Backlog → Ready → In Progress → Review → Done

Backlog: All issues, prioritized
Ready: Next up, no blockers
In Progress: Currently building
Review: Testing/validation
Done: Shipped
```

### Critical: Issues are sequenced correctly
```
Foundation issues first:
1. Project setup
2. Database schema
3. Auth system

Then feature issues:
4. Core feature 1
5. Core feature 2
6. Integrations

Finally polish:
7. Testing
8. Deployment
9. Documentation
```

---

## STAGE 7: AI Coding Agent Execution (Ongoing)
**Role:** AI coding agent (Cursor/Cline) builds
**Your Role:** Direct, review, validate

### Your Workflow:

**Daily Process:**

**Morning (15 min):**
1. Review yesterday's completed work
2. Move issues on project board
3. Pick today's top priority issue
4. Read issue completely

**Build Session 1 (3 hours):**
```
1. Open issue in Cursor/Cline
2. Provide context to AI agent:
   "Working on Issue #X: [title]
   
   Context:
   - Stack: [Makerkit/Laravel]
   - Database: [Supabase/Postgres]
   - This feature does: [summary]
   
   Acceptance criteria:
   [Paste from issue]
   
   Build this now."

3. AI agent generates code
4. You review each chunk:
   - Does it match requirements?
   - Does it follow conventions?
   - Any obvious bugs?
   
5. Run and test locally
6. Fix any issues (with AI help)
7. Commit when working
```

**Midday Check (15 min):**
- Is this on track to finish today?
- Any blockers?
- Update issue with progress

**Build Session 2 (3 hours):**
- Continue building OR
- Start next issue if first is done

**End of Day (15 min):**
1. Commit all work
2. Update issue status
3. Move completed issues to Review
4. Test completed work
5. Plan tomorrow's issue

### Weekly Process:

**Friday Afternoon (1 hour):**
1. Review week's progress
2. Test all completed features together
3. Update milestones
4. Plan next week's priorities
5. Deploy if sprint complete

---

# Part 4: Role Definitions (You Wear All Hats)

## Your Product Manager Hat
**When:** Stages 1, 2.5, 5
**Responsibilities:**
- Validate idea has market
- Decide on priorities
- Approve specifications
- Make go/no-go decisions
- Set success metrics

**Time:** 20% of total time

## Your Engineering Lead Hat
**When:** Stages 2, 3, 4, 7
**Responsibilities:**
- Validate technical feasibility
- Choose architecture approach
- Review AI-generated code
- Make technical decisions
- Debug issues

**Time:** 70% of total time

## Your Project Manager Hat
**When:** Stages 6, 7
**Responsibilities:**
- Break work into tasks
- Sequence tasks correctly
- Track progress
- Adjust timeline as needed
- Remove blockers

**Time:** 10% of total time

---

# Part 5: Decision Points & Checkpoints

## Go/No-Go Gates

### Gate 1: After Stage 1 (Idea Intake)
**Question:** Do I want to pursue this?
**Time invested:** 10 minutes
**Decision:**
- GO → Stack compatibility check
- NO-GO → Document and move on

### Gate 2: After Stage 2 (Stack Check)
**Question:** Does this fit my constraints?
**Time invested:** 12 minutes
**Decision:**
- FITS → Human approval required
- DOESN'T FIT → Document why, pivot or reject

### Gate 3: After Stage 2.5 (Stack Selection)
**Question:** Do I approve this stack and approach?
**Time invested:** 15 minutes
**Decision:**
- APPROVE → Continue to agent check
- REVISE → Discuss alternatives
- REJECT → Kill idea

**This is your main decision point**

### Gate 4: After Stage 4 (Agent Validation)
**Question:** Is this feasible to build?
**Time invested:** 4-6 hours
**Decision:**
- FEASIBLE → Build with confidence
- NOT FEASIBLE → Kill or pivot
- NEEDS CHANGES → Adjust scope

### Gate 5: During Stage 7 (Mid-Build)
**Question:** Is this still the right priority?
**Frequency:** Weekly
**Decision:**
- CONTINUE → Keep building
- PIVOT → Adjust features
- PAUSE → Work on something else

---

# Part 6: Communication Flow (With AI)

## How AI Helps at Each Stage

### Stage 1: Interview Partner
```
You → AI: "I have an idea"
AI → You: [Asks clarifying questions]
You → AI: [Answers naturally]
AI → You: [Structured summary]
```

### Stage 2-3: Technical Advisor
```
AI → You: [Stack recommendation with reasoning]
You → AI: [Approval or concerns]
AI → You: [Adjusted recommendation OR proceed]
```

### Stage 4: Validation Engineer
```
AI → You: [Claude Code prompt]
You → Claude Code: [Runs prompt]
Claude Code → You: [Working prototype + findings]
You → AI: [Share results]
AI → You: [Analysis and recommendation]
```

### Stage 5: Documentation Writer
```
AI → You: [Complete specification]
You → AI: [Feedback and changes]
AI → You: [Updated specification]
You → AI: [Approval]
```

### Stage 6: Task Breakdown Expert
```
AI → You: [GitHub issues + project board]
You → AI: [Any adjustments]
AI → You: [Final task list]
```

### Stage 7: Coding Partner
```
You → Cursor/Cline: [Issue context + instruction]
Cursor/Cline → You: [Code implementation]
You → Cursor/Cline: [Feedback]
Cursor/Cline → You: [Revised code]
[Repeat until done]
```

---

# Part 7: Time Budgets

## Idea to First Commit

**With Agent Validation:**
- Stage 1: 10 min
- Stage 2: 2 min
- Stage 2.5: 5 min (human decision)
- Stage 3: 2 min
- Stage 4: 3 hours (agent prototype)
- Stage 5: 45 min (spec generation)
- Stage 6: 10 min (issue creation)
**Total: ~4.5 hours**

**Without Agent Validation:**
- Stages 1-3: 20 min
- Stage 5: 45 min
- Stage 6: 10 min
**Total: ~1.5 hours**

## Idea to MVP Launch

**Makerkit Projects:**
- Planning (Stages 1-6): 4-6 hours
- Building (Stage 7): 40-60 hours
- **Total: 1-2 weeks**

**Laravel Projects:**
- Planning (Stages 1-6): 4-6 hours
- Building (Stage 7): 80-120 hours
- **Total: 3-4 weeks**

---

# Part 8: Documentation Artifacts

## What Gets Documented (Stored in Project)

1. **Idea Summary** (from Stage 1)
   - Store in: Notion/Docs
   - Reference when: Making decisions

2. **Stack Decision** (from Stage 2.5)
   - Store in: Project README
   - Reference when: Onboarding AI agents

3. **Agent Report** (from Stage 4, if applicable)
   - Store in: Project docs folder
   - Reference when: Building features

4. **Product Spec** (from Stage 5)
   - Store in: Project docs folder
   - Reference when: Building, prioritizing

5. **GitHub Issues** (from Stage 6)
   - Store in: GitHub
   - Reference when: Daily work

## What Gets Discarded

- Interview transcripts
- Alternative stack considerations
- Detailed agent logs (keep summary only)

---

# Part 9: Your Weekly Rhythm

**Monday (Planning Day):**
- Review last week's progress (30 min)
- Groom backlog with AI (30 min)
- Prioritize this week's issues (15 min)
- Set weekly goal (5 min)
**Total: 1.5 hours planning, 5.5 hours building**

**Tuesday-Thursday (Build Days):**
- Morning: Pick issue, build (3 hours)
- Afternoon: Continue or start next (3 hours)
- End of day: Review and commit (15 min)
**Total: 6+ hours building/day**

**Friday (Ship Day):**
- Morning: Complete remaining issues (3 hours)
- Afternoon: Test, deploy, plan next week (3 hours)
**Total: 6 hours**

**Weekly Total: 30-35 hours** → 1 MVP every 1-4 weeks depending on complexity

---

# Part 10: Success Metrics

## Process Metrics (How efficient are you?)

- **Idea rejection rate:** Should be 60-70% (Stack filters working)
- **Agent validation success:** Should save 1-2 weeks per project
- **Time to first commit:** Should be < 6 hours
- **Issues completed per week:** Track your velocity
- **Code review cycles:** Should be 1-2 per feature (AI quality)

## Product Metrics (Are you building the right things?)

- **Time to MVP:** Makerkit 1-2 weeks, Laravel 3-4 weeks
- **Feature completion rate:** 80%+ of planned features ship
- **Post-launch pivots:** < 30% (validation is working)
- **Customer adoption:** Track your specific KPIs

---

# Summary: Your Complete System

**You are a product company that:**
1. Validates ideas ruthlessly (60-70% rejected immediately)
2. Prototypes uncertainties with AI agents (saves weeks)
3. Generates detailed specs with AI (30-60 min vs 8+ hours)
4. Builds with AI coding agents (10x faster than manual)
5. Ships MVPs in 1-4 weeks (not 3-6 months)

**Your competitive advantage:**
- **Speed:** Others spend 3 months planning, you ship in 3 weeks
- **Validation:** Others build then discover problems, you discover then build
- **Leverage:** Others write every line, you direct AI to write it
- **Focus:** Others try everything, you only build what fits your stack

**Your constraint is your superpower:** You can only build 2-3 types of products, so you build them REALLY well and REALLY fast.

This is your workflow. Follow it religiously, and you'll ship more in a year than most founders ship in five.