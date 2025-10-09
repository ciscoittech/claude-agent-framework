-- Claude Agent Framework - Local Observability Database Schema
-- SQLite database for tracking agent executions, validation, and metrics
-- Project-local: Each project gets its own .claude-metrics/observability.db

-- ==============================================================================
-- AGENT EXECUTION TRACKING
-- ==============================================================================

CREATE TABLE IF NOT EXISTS executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    task_description TEXT,
    parent_execution_id INTEGER,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    duration_ms INTEGER,
    status TEXT CHECK(status IN ('running', 'success', 'failed', 'timeout', 'cancelled')) DEFAULT 'running',
    error_message TEXT,
    FOREIGN KEY (parent_execution_id) REFERENCES executions(id) ON DELETE CASCADE
);

-- ==============================================================================
-- METRICS TRACKING (Tokens, Costs, Performance)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS execution_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    execution_id INTEGER NOT NULL UNIQUE,
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    tokens_cached INTEGER DEFAULT 0,
    tokens_total INTEGER GENERATED ALWAYS AS (tokens_input + tokens_output) STORED,
    cost_usd DECIMAL(10,6) DEFAULT 0.0,
    FOREIGN KEY (execution_id) REFERENCES executions(id) ON DELETE CASCADE
);

-- ==============================================================================
-- ARTIFACTS (Files, Commands, Tests)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS artifacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    execution_id INTEGER NOT NULL,
    artifact_type TEXT CHECK(artifact_type IN ('file_created', 'file_modified', 'file_deleted', 'command_run', 'test_run', 'output')) NOT NULL,
    artifact_path TEXT NOT NULL,
    artifact_size_bytes INTEGER,
    artifact_hash TEXT,  -- Optional: SHA256 hash for verification
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (execution_id) REFERENCES executions(id) ON DELETE CASCADE
);

-- ==============================================================================
-- TASK EXPECTATIONS (Validation Rules)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS task_expectations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_pattern TEXT NOT NULL UNIQUE,
    description TEXT,
    expected_agents TEXT,  -- JSON array: ["architect", "engineer", "reviewer"]
    expected_files TEXT,   -- JSON array: ["*.py", "tests/*"]
    required_artifacts TEXT, -- JSON array: ["file_created", "test_run"]
    max_duration_ms INTEGER,
    max_tokens INTEGER,
    max_cost_usd DECIMAL(10,6),
    enabled BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- VALIDATION RESULTS
-- ==============================================================================

CREATE TABLE IF NOT EXISTS validations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    execution_id INTEGER NOT NULL,
    expectation_id INTEGER,
    validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    passed BOOLEAN NOT NULL,
    violations TEXT,  -- JSON array: [{type: "missing_agent", expected: "reviewer", actual: null}]
    score DECIMAL(5,2),  -- 0-100 score for partial validation
    FOREIGN KEY (execution_id) REFERENCES executions(id) ON DELETE CASCADE,
    FOREIGN KEY (expectation_id) REFERENCES task_expectations(id) ON DELETE SET NULL
);

-- ==============================================================================
-- SUB-AGENTS (Hierarchy Tracking)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS sub_agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_execution_id INTEGER NOT NULL,
    agent_name TEXT NOT NULL,
    agent_type TEXT,  -- core, specialized, custom
    sequence_order INTEGER,
    launched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_execution_id) REFERENCES executions(id) ON DELETE CASCADE
);

-- ==============================================================================
-- SESSIONS (Track Claude Code sessions)
-- ==============================================================================

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL UNIQUE,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    project_path TEXT,
    git_branch TEXT,
    git_commit TEXT,
    total_executions INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    total_cost_usd DECIMAL(10,6) DEFAULT 0.0
);

-- ==============================================================================
-- PERFORMANCE INDEXES
-- ==============================================================================

CREATE INDEX IF NOT EXISTS idx_executions_session ON executions(session_id);
CREATE INDEX IF NOT EXISTS idx_executions_agent ON executions(agent_name);
CREATE INDEX IF NOT EXISTS idx_executions_status ON executions(status);
CREATE INDEX IF NOT EXISTS idx_executions_started ON executions(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_executions_parent ON executions(parent_execution_id);

CREATE INDEX IF NOT EXISTS idx_artifacts_execution ON artifacts(execution_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_type ON artifacts(artifact_type);
CREATE INDEX IF NOT EXISTS idx_artifacts_path ON artifacts(artifact_path);

CREATE INDEX IF NOT EXISTS idx_validations_execution ON validations(execution_id);
CREATE INDEX IF NOT EXISTS idx_validations_passed ON validations(passed);

CREATE INDEX IF NOT EXISTS idx_sub_agents_parent ON sub_agents(parent_execution_id);
CREATE INDEX IF NOT EXISTS idx_sub_agents_name ON sub_agents(agent_name);

CREATE INDEX IF NOT EXISTS idx_sessions_id ON sessions(session_id);

-- ==============================================================================
-- VIEWS (Convenient queries)
-- ==============================================================================

-- View: Recent executions with metrics
CREATE VIEW IF NOT EXISTS v_recent_executions AS
SELECT
    e.id,
    e.session_id,
    e.agent_name,
    e.task_description,
    e.started_at,
    e.completed_at,
    e.duration_ms,
    e.status,
    COALESCE(m.tokens_total, 0) as tokens_total,
    COALESCE(m.cost_usd, 0.0) as cost_usd,
    (SELECT COUNT(*) FROM sub_agents WHERE parent_execution_id = e.id) as sub_agents_count,
    (SELECT COUNT(*) FROM artifacts WHERE execution_id = e.id) as artifacts_count,
    (SELECT passed FROM validations WHERE execution_id = e.id LIMIT 1) as validation_passed
FROM executions e
LEFT JOIN execution_metrics m ON m.execution_id = e.id
ORDER BY e.started_at DESC;

-- View: Failed executions
CREATE VIEW IF NOT EXISTS v_failed_executions AS
SELECT
    e.id,
    e.agent_name,
    e.task_description,
    e.started_at,
    e.error_message,
    e.duration_ms,
    (SELECT COUNT(*) FROM sub_agents WHERE parent_execution_id = e.id) as sub_agents_launched
FROM executions e
WHERE e.status = 'failed'
ORDER BY e.started_at DESC;

-- View: Daily summary
CREATE VIEW IF NOT EXISTS v_daily_summary AS
SELECT
    DATE(e.started_at) as date,
    COUNT(*) as total_executions,
    SUM(CASE WHEN e.status = 'success' THEN 1 ELSE 0 END) as successful,
    SUM(CASE WHEN e.status = 'failed' THEN 1 ELSE 0 END) as failed,
    ROUND(AVG(e.duration_ms), 0) as avg_duration_ms,
    SUM(COALESCE(m.tokens_total, 0)) as total_tokens,
    ROUND(SUM(COALESCE(m.cost_usd, 0.0)), 4) as total_cost_usd,
    COUNT(DISTINCT e.agent_name) as unique_agents
FROM executions e
LEFT JOIN execution_metrics m ON m.execution_id = e.id
WHERE e.completed_at IS NOT NULL
GROUP BY DATE(e.started_at)
ORDER BY date DESC;

-- View: Agent performance
CREATE VIEW IF NOT EXISTS v_agent_performance AS
SELECT
    e.agent_name,
    COUNT(*) as total_executions,
    SUM(CASE WHEN e.status = 'success' THEN 1 ELSE 0 END) as successful,
    SUM(CASE WHEN e.status = 'failed' THEN 1 ELSE 0 END) as failed,
    ROUND(AVG(e.duration_ms), 0) as avg_duration_ms,
    ROUND(AVG(COALESCE(m.tokens_total, 0)), 0) as avg_tokens,
    ROUND(SUM(COALESCE(m.cost_usd, 0.0)), 4) as total_cost_usd
FROM executions e
LEFT JOIN execution_metrics m ON m.execution_id = e.id
WHERE e.completed_at IS NOT NULL
GROUP BY e.agent_name
ORDER BY total_executions DESC;

-- ==============================================================================
-- TRIGGERS (Auto-update session totals)
-- ==============================================================================

CREATE TRIGGER IF NOT EXISTS update_session_totals_on_completion
AFTER UPDATE OF completed_at ON executions
WHEN NEW.completed_at IS NOT NULL
BEGIN
    UPDATE sessions
    SET total_executions = total_executions + 1,
        total_tokens = total_tokens + COALESCE((SELECT tokens_total FROM execution_metrics WHERE execution_id = NEW.id), 0),
        total_cost_usd = total_cost_usd + COALESCE((SELECT cost_usd FROM execution_metrics WHERE execution_id = NEW.id), 0.0)
    WHERE session_id = NEW.session_id;
END;

-- ==============================================================================
-- INITIAL DATA (Example expectations)
-- ==============================================================================

-- Example: Authentication implementation
INSERT OR IGNORE INTO task_expectations (task_pattern, description, expected_agents, expected_files, max_duration_ms, max_tokens)
VALUES (
    '(?i)implement.*(auth|authentication)',
    'Implementing authentication systems',
    '["architect", "engineer", "reviewer"]',
    '["auth.py", "tests/test_auth.py"]',
    120000,
    50000
);

-- Example: API endpoint creation
INSERT OR IGNORE INTO task_expectations (task_pattern, description, expected_agents, expected_files, max_duration_ms, max_tokens)
VALUES (
    '(?i)create.*(api|endpoint)',
    'Creating API endpoints',
    '["architect", "engineer"]',
    '["*.py", "tests/*"]',
    60000,
    30000
);

-- ==============================================================================
-- TOOL USAGE TRACKING
-- ==============================================================================

-- Tool usage tracking
CREATE TABLE IF NOT EXISTS tool_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    execution_id INTEGER NOT NULL,
    tool_name TEXT NOT NULL,
    parameters_json TEXT,
    success BOOLEAN NOT NULL,
    duration_ms INTEGER,
    tokens_used INTEGER,
    output_size_bytes INTEGER,
    timestamp TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (execution_id) REFERENCES executions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_tool_usage_execution ON tool_usage(execution_id);
CREATE INDEX IF NOT EXISTS idx_tool_usage_tool ON tool_usage(tool_name);
CREATE INDEX IF NOT EXISTS idx_tool_usage_timestamp ON tool_usage(timestamp);

-- View: Tool usage statistics
CREATE VIEW IF NOT EXISTS v_tool_stats AS
SELECT
    tool_name,
    COUNT(*) as total_calls,
    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_calls,
    SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed_calls,
    ROUND(100.0 * SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) as success_rate,
    ROUND(AVG(duration_ms), 0) as avg_duration_ms,
    SUM(COALESCE(tokens_used, 0)) as total_tokens,
    ROUND(AVG(COALESCE(tokens_used, 0)), 0) as avg_tokens,
    ROUND(AVG(COALESCE(output_size_bytes, 0)), 0) as avg_output_size
FROM tool_usage
GROUP BY tool_name
ORDER BY total_calls DESC;

-- View: Tool efficiency (tokens per success)
CREATE VIEW IF NOT EXISTS v_tool_efficiency AS
SELECT
    tool_name,
    COUNT(*) as total_calls,
    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_calls,
    SUM(COALESCE(tokens_used, 0)) as total_tokens,
    CASE
        WHEN SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) > 0
        THEN ROUND(CAST(SUM(COALESCE(tokens_used, 0)) AS REAL) / SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END), 0)
        ELSE 0
    END as tokens_per_success,
    ROUND(AVG(duration_ms), 0) as avg_duration_ms
FROM tool_usage
GROUP BY tool_name
ORDER BY tokens_per_success ASC;

-- ==============================================================================
-- SCHEMA VERSION
-- ==============================================================================

CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT OR REPLACE INTO schema_version (version, description) VALUES (2, 'Added tool usage tracking with statistics views');
