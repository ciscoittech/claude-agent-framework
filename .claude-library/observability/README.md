# Local Agent Observability

**Project-local SQLite observability for Claude Agent Framework**

Track agent executions, validate task outputs, and analyze performance metrics—all stored locally in your project with zero cloud dependencies.

---

## 🎯 Features

- **Agent Execution Tracking**: Capture when agents launch, which sub-agents they spawn, duration, and token usage
- **Validation Layer**: Automatically verify task outputs match expectations
- **Performance Metrics**: Track tokens, costs, and execution times
- **Artifact Tracking**: Monitor files created/modified and commands executed
- **Project-Local Database**: Each project gets its own `.claude-metrics/observability.db`
- **Powerful CLI**: Query and analyze data with simple commands
- **Zero Cloud Dependencies**: 100% offline, SQLite-based

---

## 🚀 Quick Start

### 1. Enable in REGISTRY.json

Edit `.claude-library/REGISTRY.json`:

```json
{
  "settings": {
    "hooks": {
      "enabled": true,
      "scope": "project",
      "configs": [
        ".claude-library/observability/configs/local-observability.json"
      ],
      "allow_blocking": false,
      "timeout_ms": 5000
    }
  }
}
```

### 2. Database Auto-Initializes

The observability database is automatically created on the next Claude Code session start:

```
✅ Initializing observability database: .claude-metrics/observability.db
   Schema applied successfully
   Session ID: a3f8c2b1...
```

### 3. Query Execution Data

```bash
# Show recent agent executions
python3 .claude-library/observability/obs.py recent

# Show failed executions
python3 .claude-library/observability/obs.py failed

# Show execution details
python3 .claude-library/observability/obs.py execution 1

# Show daily summary
python3 .claude-library/observability/obs.py summary --days 7

# Show agent performance
python3 .claude-library/observability/obs.py agents
```

---

## 📊 What Gets Tracked

### Automatic Tracking (via Hooks)

- **Task Launches**: Captures every `Task` tool invocation
  - Agent name and type
  - Task description
  - Parent-child relationships (sub-agents)

- **Task Completion**: Records results
  - Success/failure status
  - Duration in milliseconds
  - Error messages (if failed)

- **Token Metrics**: Tracks usage
  - Input tokens
  - Output tokens
  - Cached tokens
  - Estimated cost (USD)

- **Artifacts**: Monitors changes
  - Files created/modified/deleted
  - Commands executed
  - Test runs

- **Validation**: Checks expectations
  - Expected agents launched
  - Expected files created
  - Performance limits (duration, tokens, cost)

---

## 🔍 Validation System

### How It Works

Define task expectations with regex patterns. When a task description matches a pattern, the system validates the execution against expectations.

### Example: Authentication Task

```sql
INSERT INTO task_expectations (
  task_pattern,
  description,
  expected_agents,
  expected_files,
  max_duration_ms,
  max_tokens
) VALUES (
  '(?i)implement.*(auth|authentication)',
  'Implementing authentication systems',
  '["architect", "engineer", "reviewer"]',
  '["auth.py", "tests/test_auth.py"]',
  120000,
  50000
);
```

**What Gets Validated:**
- ✅ Were expected agents launched? (architect, engineer, reviewer)
- ✅ Were expected files created? (auth.py, tests/test_auth.py)
- ✅ Did duration stay under 120 seconds?
- ✅ Did token usage stay under 50,000?

### Validation Results

```bash
python3 .claude-library/observability/obs.py execution 1

# Output:
🔍 Validation: ✅ PASSED (score: 100.0)

# Or if failed:
🔍 Validation: ❌ FAILED (score: 75.0)
Violations:
  - missing_agent: expected reviewer, got None
  - duration_exceeded: expected 120000, got 145000
```

---

## 🛠️ Database Schema

### Core Tables

**executions** - Main execution records
- `id`, `session_id`, `agent_name`, `task_description`
- `parent_execution_id` (for sub-agents)
- `started_at`, `completed_at`, `duration_ms`
- `status` (running, success, failed, timeout, cancelled)

**execution_metrics** - Performance data
- `tokens_input`, `tokens_output`, `tokens_cached`, `tokens_total`
- `cost_usd`

**artifacts** - Created/modified resources
- `artifact_type` (file_created, file_modified, command_run, test_run)
- `artifact_path`, `artifact_size_bytes`, `artifact_hash`

**task_expectations** - Validation rules
- `task_pattern` (regex)
- `expected_agents`, `expected_files`, `required_artifacts` (JSON)
- `max_duration_ms`, `max_tokens`, `max_cost_usd`

**validations** - Validation results
- `execution_id`, `expectation_id`
- `passed`, `violations` (JSON), `score`

**sub_agents** - Agent hierarchy
- `parent_execution_id`, `agent_name`, `agent_type`

**sessions** - Claude Code sessions
- `session_id`, `project_path`, `git_branch`, `git_commit`
- `total_executions`, `total_tokens`, `total_cost_usd`

---

## 📈 CLI Commands

### Recent Executions

```bash
python3 .claude-library/observability/obs.py recent --limit 10
```

Output:
```
📊 Recent Executions (last 10):

ID    Agent                Status      Duration    Tokens      Cost          Time
---------------------------------------------------------------------------------------------------
5     architect            ✅ success  2.3s        12500       $0.0450       2025-10-04 14:23:15
4     engineer             ✅ success  5.1s        28000       $0.1200       2025-10-04 14:20:10
```

### Failed Executions

```bash
python3 .claude-library/observability/obs.py failed
```

### Execution Details

```bash
python3 .claude-library/observability/obs.py execution 5
```

Output:
```
📊 Execution #5:

Agent: architect
Status: success
Task: Design authentication system for user login
Started: 2025-10-04 14:23:15
Duration: 2.3s
Tokens: 12500 (cost: $0.0450)

🤖 Sub-Agents (2):
  - engineer (specialized) at 2025-10-04 14:23:18
  - reviewer (specialized) at 2025-10-04 14:25:20

📁 Artifacts (3):
  - file_created: auth/login.py (1250 bytes)
  - file_created: tests/test_login.py (890 bytes)
  - test_run: pytest tests/test_login.py

🔍 Validation: ✅ PASSED (score: 100.0)
```

### Daily Summary

```bash
python3 .claude-library/observability/obs.py summary --days 7
```

### Agent Performance

```bash
python3 .claude-library/observability/obs.py agents
```

Output:
```
🤖 Agent Performance:

Agent                     Executions   Success Rate    Avg Time     Avg Tokens   Total Cost
---------------------------------------------------------------------------------------------------
architect                 12           100%            2.5s         15000        $0.5400
engineer                  25           96%             4.2s         22000        $1.8500
reviewer                  18           100%            1.8s         8000         $0.4800
```

### Current Session

```bash
python3 .claude-library/observability/obs.py session
```

### Task Expectations

```bash
python3 .claude-library/observability/obs.py expectations
```

### Cleanup Old Data

```bash
python3 .claude-library/observability/obs.py cleanup --days 30
```

---

## 🎯 Use Cases

### 1. Track Agent Hierarchy

See which agents launch sub-agents and when:

```sql
-- Query directly with SQLite
sqlite3 .claude-metrics/observability.db

SELECT
  e1.id,
  e1.agent_name as parent_agent,
  e2.agent_name as sub_agent,
  e2.started_at
FROM executions e1
JOIN executions e2 ON e2.parent_execution_id = e1.id
ORDER BY e1.started_at DESC;
```

### 2. Cost Analysis

Track spending per agent type:

```bash
python3 .claude-library/observability/obs.py agents
```

### 3. Performance Regression Detection

Monitor if execution times are increasing:

```bash
python3 .claude-library/observability/obs.py summary --days 30
```

### 4. Validation for Quality Assurance

Ensure tasks follow expected patterns:

1. Define expectations for common tasks
2. Let validation run automatically
3. Review violations with `obs.py execution <id>`

### 5. Debugging Failed Executions

Quickly find and analyze failures:

```bash
python3 .claude-library/observability/obs.py failed
```

---

## 🔧 Advanced Usage

### Custom SQL Queries

Direct database access for complex analysis:

```bash
sqlite3 .claude-metrics/observability.db

-- Most expensive executions
SELECT agent_name, task_description, cost_usd
FROM v_recent_executions
ORDER BY cost_usd DESC
LIMIT 10;

-- Agent success rates
SELECT
  agent_name,
  COUNT(*) as total,
  SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful,
  ROUND(100.0 * SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) / COUNT(*), 1) as success_rate
FROM executions
WHERE completed_at IS NOT NULL
GROUP BY agent_name;
```

### Adding Custom Expectations

```bash
sqlite3 .claude-metrics/observability.db

INSERT INTO task_expectations (
  task_pattern,
  description,
  expected_agents,
  max_duration_ms,
  max_tokens
) VALUES (
  '(?i)create.*api.*endpoint',
  'API endpoint creation',
  '["architect", "engineer"]',
  60000,
  30000
);
```

### Export Data

```bash
# Export to JSON
sqlite3 .claude-metrics/observability.db <<EOF
.mode json
.once executions.json
SELECT * FROM v_recent_executions LIMIT 100;
EOF

# Export to CSV
sqlite3 .claude-metrics/observability.db <<EOF
.mode csv
.headers on
.once summary.csv
SELECT * FROM v_daily_summary;
EOF
```

---

## 📁 Files Structure

```
.claude-library/observability/
├── README.md                              # This file
├── schema.sql                             # Database schema
├── db_helper.py                           # Database access library
├── obs.py                                 # CLI tool
│
├── configs/
│   └── local-observability.json          # Hook configuration
│
└── scripts/
    ├── init_observability_db.sh          # SessionStart: Initialize DB
    ├── observe_task_start.py             # PreToolUse: Track task start
    ├── observe_task_end.py               # PostToolUse: Track completion
    ├── track_artifact.py                 # PostToolUse: Track files/commands
    └── validate_execution.py             # PostToolUse: Validate output

.claude-metrics/
├── observability.db                       # SQLite database
├── .session_id                           # Current session ID
└── .current_execution_id                 # Current execution ID
```

---

## 🔒 Privacy & Data

- **100% Local**: All data stored in project's `.claude-metrics/` directory
- **No Cloud Sync**: Zero external dependencies
- **Git-Ignored**: Add `.claude-metrics/` to `.gitignore`
- **Per-Project**: Each project has isolated database
- **Auto-Cleanup**: Configure retention with `obs.py cleanup`

---

## 🚨 Troubleshooting

### Database Not Initializing

Check that SessionStart hook is enabled:

```bash
# Verify hook config
cat .claude-library/REGISTRY.json | jq '.settings.hooks'

# Manually initialize
bash .claude-library/observability/scripts/init_observability_db.sh
```

### No Data Being Tracked

1. Verify hooks are enabled in REGISTRY.json
2. Check that `.claude-library/observability/configs/local-observability.json` is in configs array
3. Ensure scripts are executable:

```bash
chmod +x .claude-library/observability/scripts/*.py
chmod +x .claude-library/observability/scripts/*.sh
```

### Import Errors in Python Scripts

Scripts automatically add parent directory to path. If issues persist:

```bash
# Check Python version (requires 3.8+)
python3 --version

# Verify db_helper.py exists
ls -la .claude-library/observability/db_helper.py
```

---

## 🎯 Performance

- **Hook Overhead**: ~200-500ms per execution (negligible)
- **Database Size**: ~1-5MB per 1000 executions
- **Query Speed**: Instant (<100ms) for most queries
- **Storage**: SQLite auto-vacuums on cleanup

---

## 📚 Integration with Framework

### Used by System Generator

When generating agent systems, the generator can:
1. Reference execution history for context
2. Validate agent patterns match expectations
3. Optimize based on performance metrics

### Used by Quality Assurance

Track if generated systems meet quality targets:
- Agent hierarchy depth
- Token efficiency
- Success rates
- Cost per task

---

## 🔄 Next Steps

1. **Enable in your project**: Update REGISTRY.json
2. **Run some agents**: Let data accumulate
3. **Analyze performance**: Use CLI to explore
4. **Define expectations**: Add validation rules
5. **Optimize**: Use insights to improve agent patterns

---

**Version**: 1.0.0
**Author**: Claude Agent Framework
**License**: MIT
