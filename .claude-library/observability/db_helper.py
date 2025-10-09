#!/usr/bin/env python3
"""
Database Helper Library for Local Agent Observability
Provides convenient functions for tracking agent executions in SQLite
"""

import sqlite3
import json
import os
import hashlib
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime
from typing import Optional, List, Dict, Any

# Database location (project-local)
DB_PATH = Path('.claude-metrics/observability.db')
SCHEMA_PATH = Path(__file__).parent / 'schema.sql'

# Session ID (stored in temp file for current session)
SESSION_ID_FILE = Path('.claude-metrics/.session_id')


# ==============================================================================
# DATABASE CONNECTION
# ==============================================================================

@contextmanager
def get_db():
    """Get database connection with automatic commit/rollback"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_database():
    """Initialize database with schema if it doesn't exist"""
    # Create directory
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Apply schema
    if SCHEMA_PATH.exists():
        with get_db() as conn:
            schema_sql = SCHEMA_PATH.read_text()
            conn.executescript(schema_sql)
        return True
    else:
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")


# ==============================================================================
# SESSION MANAGEMENT
# ==============================================================================

def get_session_id() -> str:
    """Get or create session ID for current Claude Code session"""
    if SESSION_ID_FILE.exists():
        return SESSION_ID_FILE.read_text().strip()
    else:
        # Generate new session ID
        import uuid
        session_id = str(uuid.uuid4())
        SESSION_ID_FILE.parent.mkdir(parents=True, exist_ok=True)
        SESSION_ID_FILE.write_text(session_id)

        # Create session record
        with get_db() as conn:
            # Get git info
            try:
                import subprocess
                git_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
                git_commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], stderr=subprocess.DEVNULL).decode().strip()
            except:
                git_branch = None
                git_commit = None

            conn.execute("""
                INSERT INTO sessions (session_id, project_path, git_branch, git_commit)
                VALUES (?, ?, ?, ?)
            """, (session_id, str(Path.cwd()), git_branch, git_commit))

        return session_id


def end_session():
    """Mark session as ended"""
    if SESSION_ID_FILE.exists():
        session_id = SESSION_ID_FILE.read_text().strip()
        with get_db() as conn:
            conn.execute("""
                UPDATE sessions
                SET ended_at = CURRENT_TIMESTAMP
                WHERE session_id = ?
            """, (session_id,))
        # Don't delete the file - keep it for reference


# ==============================================================================
# EXECUTION TRACKING
# ==============================================================================

def insert_execution(
    agent_name: str,
    task_description: Optional[str] = None,
    parent_id: Optional[int] = None
) -> int:
    """
    Insert new execution record

    Args:
        agent_name: Name of the agent being executed
        task_description: Description of the task
        parent_id: ID of parent execution (for sub-agents)

    Returns:
        Execution ID
    """
    session_id = get_session_id()

    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO executions (session_id, agent_name, task_description, parent_execution_id, status)
            VALUES (?, ?, ?, ?, 'running')
        """, (session_id, agent_name, task_description, parent_id))
        return cursor.lastrowid


def update_execution(
    execution_id: int,
    status: str,
    duration_ms: Optional[int] = None,
    error_message: Optional[str] = None
):
    """
    Update execution completion

    Args:
        execution_id: ID of execution to update
        status: Final status (success, failed, timeout, cancelled)
        duration_ms: Execution duration in milliseconds
        error_message: Error message if failed
    """
    with get_db() as conn:
        conn.execute("""
            UPDATE executions
            SET completed_at = CURRENT_TIMESTAMP,
                status = ?,
                duration_ms = ?,
                error_message = ?
            WHERE id = ?
        """, (status, duration_ms, error_message, execution_id))


# ==============================================================================
# METRICS TRACKING
# ==============================================================================

def insert_metrics(
    execution_id: int,
    tokens_input: int = 0,
    tokens_output: int = 0,
    tokens_cached: int = 0,
    cost_usd: float = 0.0
):
    """Insert or update execution metrics"""
    with get_db() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO execution_metrics
            (execution_id, tokens_input, tokens_output, tokens_cached, cost_usd)
            VALUES (?, ?, ?, ?, ?)
        """, (execution_id, tokens_input, tokens_output, tokens_cached, cost_usd))


# ==============================================================================
# ARTIFACT TRACKING
# ==============================================================================

def insert_artifact(
    execution_id: int,
    artifact_type: str,
    artifact_path: str,
    artifact_size_bytes: Optional[int] = None
):
    """
    Insert artifact record

    Args:
        execution_id: ID of execution that created artifact
        artifact_type: Type (file_created, file_modified, command_run, etc.)
        artifact_path: Path to artifact
        artifact_size_bytes: Size in bytes (optional)
    """
    # Calculate hash for files
    artifact_hash = None
    if artifact_type in ('file_created', 'file_modified'):
        try:
            path = Path(artifact_path)
            if path.exists() and path.is_file():
                if artifact_size_bytes is None:
                    artifact_size_bytes = path.stat().st_size
                # Only hash small files (< 1MB)
                if artifact_size_bytes < 1024 * 1024:
                    artifact_hash = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        except:
            pass

    with get_db() as conn:
        conn.execute("""
            INSERT INTO artifacts (execution_id, artifact_type, artifact_path, artifact_size_bytes, artifact_hash)
            VALUES (?, ?, ?, ?, ?)
        """, (execution_id, artifact_type, artifact_path, artifact_size_bytes, artifact_hash))


# ==============================================================================
# SUB-AGENT TRACKING
# ==============================================================================

def insert_sub_agent(
    parent_execution_id: int,
    agent_name: str,
    agent_type: Optional[str] = None,
    sequence_order: Optional[int] = None
):
    """Record a sub-agent being launched"""
    with get_db() as conn:
        conn.execute("""
            INSERT INTO sub_agents (parent_execution_id, agent_name, agent_type, sequence_order)
            VALUES (?, ?, ?, ?)
        """, (parent_execution_id, agent_name, agent_type, sequence_order))


# ==============================================================================
# VALIDATION
# ==============================================================================

def get_expectation_for_task(task_description: str) -> Optional[Dict[str, Any]]:
    """Find matching task expectation using regex pattern"""
    with get_db() as conn:
        cursor = conn.execute("""
            SELECT * FROM task_expectations
            WHERE enabled = 1
            ORDER BY id
        """)

        import re
        for row in cursor:
            pattern = row['task_pattern']
            if re.search(pattern, task_description, re.IGNORECASE):
                return dict(row)

    return None


def insert_validation(
    execution_id: int,
    passed: bool,
    violations: List[Dict[str, Any]],
    expectation_id: Optional[int] = None,
    score: Optional[float] = None
):
    """Insert validation result"""
    violations_json = json.dumps(violations) if violations else None

    with get_db() as conn:
        conn.execute("""
            INSERT INTO validations (execution_id, expectation_id, passed, violations, score)
            VALUES (?, ?, ?, ?, ?)
        """, (execution_id, expectation_id, passed, violations_json, score))


# ==============================================================================
# QUERIES
# ==============================================================================

def get_execution(execution_id: int) -> Optional[Dict[str, Any]]:
    """Get execution by ID"""
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM v_recent_executions WHERE id = ?", (execution_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_recent_executions(limit: int = 20, failed_only: bool = False) -> List[Dict[str, Any]]:
    """Get recent executions"""
    where_clause = "WHERE status = 'failed'" if failed_only else ""

    with get_db() as conn:
        cursor = conn.execute(f"""
            SELECT * FROM v_recent_executions
            {where_clause}
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]


def get_execution_sub_agents(execution_id: int) -> List[Dict[str, Any]]:
    """Get sub-agents for an execution"""
    with get_db() as conn:
        cursor = conn.execute("""
            SELECT * FROM sub_agents
            WHERE parent_execution_id = ?
            ORDER BY sequence_order, launched_at
        """, (execution_id,))
        return [dict(row) for row in cursor.fetchall()]


def get_execution_artifacts(execution_id: int) -> List[Dict[str, Any]]:
    """Get artifacts for an execution"""
    with get_db() as conn:
        cursor = conn.execute("""
            SELECT * FROM artifacts
            WHERE execution_id = ?
            ORDER BY created_at
        """, (execution_id,))
        return [dict(row) for row in cursor.fetchall()]


def get_execution_validation(execution_id: int) -> Optional[Dict[str, Any]]:
    """Get validation result for execution"""
    with get_db() as conn:
        cursor = conn.execute("""
            SELECT * FROM validations
            WHERE execution_id = ?
            ORDER BY validated_at DESC
            LIMIT 1
        """, (execution_id,))
        row = cursor.fetchone()
        if row:
            result = dict(row)
            if result['violations']:
                result['violations'] = json.loads(result['violations'])
            return result
    return None


def get_daily_summary(days: int = 7) -> List[Dict[str, Any]]:
    """Get daily summary for last N days"""
    with get_db() as conn:
        cursor = conn.execute("""
            SELECT * FROM v_daily_summary
            LIMIT ?
        """, (days,))
        return [dict(row) for row in cursor.fetchall()]


def get_agent_performance() -> List[Dict[str, Any]]:
    """Get performance metrics per agent"""
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM v_agent_performance")
        return [dict(row) for row in cursor.fetchall()]


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def get_current_execution_id() -> Optional[int]:
    """Get current execution ID from temp file"""
    temp_file = Path('.claude-metrics/.current_execution_id')
    if temp_file.exists():
        try:
            return int(temp_file.read_text().strip())
        except:
            return None
    return None


def set_current_execution_id(execution_id: int):
    """Store current execution ID in temp file"""
    temp_file = Path('.claude-metrics/.current_execution_id')
    temp_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file.write_text(str(execution_id))


def clear_current_execution_id():
    """Clear current execution ID"""
    temp_file = Path('.claude-metrics/.current_execution_id')
    if temp_file.exists():
        temp_file.unlink()


# ==============================================================================
# TOOL USAGE TRACKING
# ==============================================================================

def insert_tool_usage(
    execution_id: int,
    tool_name: str,
    parameters_json: Optional[str],
    success: bool,
    duration_ms: Optional[int] = None,
    tokens_used: Optional[int] = None,
    output_size_bytes: Optional[int] = None
):
    """
    Insert tool usage record

    Args:
        execution_id: ID of execution using this tool
        tool_name: Name of the tool (e.g., 'Read', 'Bash', 'Edit')
        parameters_json: JSON string of tool parameters
        success: Whether the tool call succeeded
        duration_ms: Tool execution duration in milliseconds
        tokens_used: Tokens consumed by this tool call
        output_size_bytes: Size of tool output in bytes
    """
    with get_db() as conn:
        conn.execute("""
            INSERT INTO tool_usage
            (execution_id, tool_name, parameters_json, success, duration_ms, tokens_used, output_size_bytes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (execution_id, tool_name, parameters_json, success, duration_ms, tokens_used, output_size_bytes))


def get_tool_usage_by_execution(execution_id: int) -> List[Dict[str, Any]]:
    """
    Get all tool usage for an execution

    Args:
        execution_id: ID of execution

    Returns:
        List of tool usage records
    """
    with get_db() as conn:
        cursor = conn.execute("""
            SELECT * FROM tool_usage
            WHERE execution_id = ?
            ORDER BY timestamp
        """, (execution_id,))
        return [dict(row) for row in cursor.fetchall()]


def get_tool_usage_stats(
    tool_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get tool usage statistics

    Args:
        tool_name: Filter by specific tool (optional)
        start_date: Start date filter (ISO format, optional)
        end_date: End date filter (ISO format, optional)

    Returns:
        List of tool statistics
    """
    where_clauses = []
    params = []

    if tool_name:
        where_clauses.append("tool_name = ?")
        params.append(tool_name)

    if start_date:
        where_clauses.append("timestamp >= ?")
        params.append(start_date)

    if end_date:
        where_clauses.append("timestamp <= ?")
        params.append(end_date)

    where_clause = ""
    if where_clauses:
        where_clause = "WHERE " + " AND ".join(where_clauses)

    with get_db() as conn:
        # If filtering, use custom query; otherwise use view
        if where_clause:
            query = f"""
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
                {where_clause}
                GROUP BY tool_name
                ORDER BY total_calls DESC
            """
            cursor = conn.execute(query, params)
        else:
            cursor = conn.execute("SELECT * FROM v_tool_stats")

        return [dict(row) for row in cursor.fetchall()]


def get_tool_efficiency() -> List[Dict[str, Any]]:
    """
    Get tool efficiency metrics (tokens per successful call)

    Returns:
        List of tool efficiency records
    """
    with get_db() as conn:
        cursor = conn.execute("SELECT * FROM v_tool_efficiency")
        return [dict(row) for row in cursor.fetchall()]


# ==============================================================================
# MAINTENANCE
# ==============================================================================

def cleanup_old_data(days: int = 30):
    """Delete data older than N days"""
    with get_db() as conn:
        conn.execute("""
            DELETE FROM executions
            WHERE started_at < datetime('now', '-' || ? || ' days')
        """, (days,))


def vacuum_database():
    """Optimize database by reclaiming space"""
    with get_db() as conn:
        conn.execute("VACUUM")
