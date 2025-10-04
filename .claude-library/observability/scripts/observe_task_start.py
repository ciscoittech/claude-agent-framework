#!/usr/bin/env python3
"""
PreToolUse Hook: Track Agent Task Start
Captures when Task tool is invoked and records execution start in SQLite
"""

import sys
import json
import os
from pathlib import Path

# Add observability library to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_helper import (
    insert_execution,
    set_current_execution_id,
    get_current_execution_id
)


def main():
    # Read hook input from stdin (JSON format)
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(0)  # Don't block on error

    # Check if this is a Task tool invocation
    tool_name = hook_input.get('tool', {}).get('name')
    if tool_name != 'Task':
        # Not a Task tool, nothing to track
        sys.exit(0)

    # Extract task details
    tool_params = hook_input.get('tool', {}).get('parameters', {})

    agent_name = tool_params.get('subagent_type', 'unknown')
    task_description = tool_params.get('prompt')

    # Check if this is a sub-agent (launched by another agent)
    parent_id = get_current_execution_id()  # Will be None if no parent

    try:
        # Insert execution record
        execution_id = insert_execution(
            agent_name=agent_name,
            task_description=task_description,
            parent_id=parent_id
        )

        # Store execution ID for end hook
        set_current_execution_id(execution_id)

        # Output for logging (optional)
        print(f"📊 Tracking: {agent_name}", file=sys.stderr)
        if parent_id:
            print(f"   Sub-agent of execution #{parent_id}", file=sys.stderr)

    except Exception as e:
        print(f"Warning: Failed to track task start: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block on error


if __name__ == '__main__':
    main()
