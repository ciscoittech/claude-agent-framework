#!/usr/bin/env python3
"""
PostToolUse Hook: Track Agent Task Completion
Captures task completion, duration, status, and metrics
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone

# Add observability library to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_helper import (
    update_execution,
    insert_metrics,
    get_execution,
    get_current_execution_id,
    clear_current_execution_id
)


def extract_token_metrics(tool_result):
    """Extract token usage from tool result if available"""
    tokens_input = 0
    tokens_output = 0
    tokens_cached = 0
    tokens_cache_write = 0

    # Check for usage data in result
    if isinstance(tool_result, dict):
        usage = tool_result.get('usage', {})
        tokens_input = usage.get('input_tokens', 0)
        tokens_output = usage.get('output_tokens', 0)
        tokens_cached = usage.get('cache_read_input_tokens', 0)
        tokens_cache_write = usage.get('cache_creation_input_tokens', 0)

    return tokens_input, tokens_output, tokens_cached, tokens_cache_write


def main():
    # Read hook input from stdin (JSON format)
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(0)

    # Check if this is a Task tool
    # The subagent tool is named 'Agent'; 'Task' is its former name, accepted so
    # older Claude Code versions keep working. Gating on 'Task' alone silently
    # disabled every one of these hooks.
    tool_name = hook_input.get('tool', {}).get('name')
    if tool_name not in ('Agent', 'Task'):
        sys.exit(0)

    # Get current execution ID
    execution_id = get_current_execution_id()
    if not execution_id:
        # No execution tracked, nothing to update
        sys.exit(0)

    # Extract result data
    tool_result = hook_input.get('result', {})
    error = hook_input.get('error')

    # Determine status
    if error:
        status = 'failed'
        error_message = str(error)
    elif tool_result.get('timeout'):
        status = 'timeout'
        error_message = 'Task execution timed out'
    else:
        status = 'success'
        error_message = None

    # Calculate duration. Prefer the harness-supplied start time; fall back to the
    # row's own started_at, which observe_task_start.py always writes. Without the
    # fallback, duration is silently lost whenever the hook payload omits it.
    #
    # Timezones matter here: SQLite's CURRENT_TIMESTAMP is UTC, while a
    # harness-supplied timestamp is local (or carries an explicit offset).
    # Comparing a UTC start against a local now yields a negative duration.
    duration_ms = None
    started, started_is_utc = None, False

    if 'started_at' in hook_input:
        try:
            started = datetime.fromisoformat(hook_input['started_at'])
        except (ValueError, TypeError):
            started = None

    if started is None and execution_id:
        row = get_execution(execution_id)
        if row and row['started_at']:
            try:
                started = datetime.fromisoformat(row['started_at'])
                started_is_utc = True  # SQLite CURRENT_TIMESTAMP is naive UTC
            except (ValueError, TypeError):
                started = None

    if started is not None:
        if started.tzinfo is not None:
            now = datetime.now(timezone.utc)
        elif started_is_utc:
            now = datetime.now(timezone.utc).replace(tzinfo=None)
        else:
            now = datetime.now()
        duration_ms = max(0, int((now - started).total_seconds() * 1000))

    try:
        # Update execution record
        update_execution(
            execution_id=execution_id,
            status=status,
            duration_ms=duration_ms,
            error_message=error_message
        )

        # Extract and insert metrics
        tokens_input, tokens_output, tokens_cached, tokens_cache_write = extract_token_metrics(tool_result)
        if tokens_input or tokens_output or tokens_cached or tokens_cache_write:
            # cost_usd is deliberately omitted: insert_metrics prices the run from
            # the model tier recorded at task start, via pricing.py. Passing a cost
            # here would override that with a tier-blind number.
            insert_metrics(
                execution_id=execution_id,
                tokens_input=tokens_input,
                tokens_output=tokens_output,
                tokens_cached=tokens_cached,
                tokens_cache_write=tokens_cache_write
            )

            # Output metrics for logging
            print(f"✅ Completed: {status}", file=sys.stderr)
            if duration_ms:
                print(f"   Duration: {duration_ms}ms", file=sys.stderr)
            print(f"   Tokens: {tokens_input + tokens_output} in+out, {tokens_cached} cache-read, {tokens_cache_write} cache-write", file=sys.stderr)
        else:
            print(f"✅ Completed: {status}", file=sys.stderr)

        # Clear execution ID (task complete)
        clear_current_execution_id()

    except Exception as e:
        print(f"Warning: Failed to track task end: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
