#!/usr/bin/env python3
"""
PostToolUse Hook: Track Agent Task Completion
Captures task completion, duration, status, and metrics
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add observability library to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_helper import (
    update_execution,
    insert_metrics,
    get_current_execution_id,
    clear_current_execution_id
)


def extract_token_metrics(tool_result):
    """Extract token usage from tool result if available"""
    tokens_input = 0
    tokens_output = 0
    tokens_cached = 0

    # Check for usage data in result
    if isinstance(tool_result, dict):
        usage = tool_result.get('usage', {})
        tokens_input = usage.get('input_tokens', 0)
        tokens_output = usage.get('output_tokens', 0)
        tokens_cached = usage.get('cache_read_input_tokens', 0)

    return tokens_input, tokens_output, tokens_cached


def calculate_cost(tokens_input, tokens_output, tokens_cached):
    """Calculate approximate USD cost based on Claude Sonnet 4.5 pricing"""
    # Sonnet 4.5 pricing (approximate)
    COST_PER_M_INPUT = 3.00    # $3 per million input tokens
    COST_PER_M_OUTPUT = 15.00   # $15 per million output tokens
    COST_PER_M_CACHED = 0.30    # $0.30 per million cached tokens

    cost = (
        (tokens_input / 1_000_000 * COST_PER_M_INPUT) +
        (tokens_output / 1_000_000 * COST_PER_M_OUTPUT) +
        (tokens_cached / 1_000_000 * COST_PER_M_CACHED)
    )

    return round(cost, 6)


def main():
    # Read hook input from stdin (JSON format)
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(0)

    # Check if this is a Task tool
    tool_name = hook_input.get('tool', {}).get('name')
    if tool_name != 'Task':
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

    # Calculate duration (if start time available)
    duration_ms = None
    if 'started_at' in hook_input:
        started = datetime.fromisoformat(hook_input['started_at'])
        ended = datetime.now()
        duration_ms = int((ended - started).total_seconds() * 1000)

    try:
        # Update execution record
        update_execution(
            execution_id=execution_id,
            status=status,
            duration_ms=duration_ms,
            error_message=error_message
        )

        # Extract and insert metrics
        tokens_input, tokens_output, tokens_cached = extract_token_metrics(tool_result)
        if tokens_input or tokens_output or tokens_cached:
            cost_usd = calculate_cost(tokens_input, tokens_output, tokens_cached)

            insert_metrics(
                execution_id=execution_id,
                tokens_input=tokens_input,
                tokens_output=tokens_output,
                tokens_cached=tokens_cached,
                cost_usd=cost_usd
            )

            # Output metrics for logging
            print(f"✅ Completed: {status}", file=sys.stderr)
            if duration_ms:
                print(f"   Duration: {duration_ms}ms", file=sys.stderr)
            print(f"   Tokens: {tokens_input + tokens_output} (${cost_usd:.4f})", file=sys.stderr)
        else:
            print(f"✅ Completed: {status}", file=sys.stderr)

        # Clear execution ID (task complete)
        clear_current_execution_id()

    except Exception as e:
        print(f"Warning: Failed to track task end: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
