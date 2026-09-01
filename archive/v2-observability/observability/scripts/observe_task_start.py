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
    get_current_execution_id,
    resolve_agent_tier
)


def main():
    # Read hook input from stdin (JSON format)
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(0)  # Don't block on error

    # Check if this is a Task tool invocation
    # The subagent tool is named 'Agent'; 'Task' is its former name, accepted so
    # older Claude Code versions keep working. Gating on 'Task' alone silently
    # disabled every one of these hooks.
    tool_name = hook_input.get('tool', {}).get('name')
    if tool_name not in ('Agent', 'Task'):
        # Not a subagent launch, nothing to track
        sys.exit(0)

    # Extract task details
    tool_params = hook_input.get('tool', {}).get('parameters', {})

    agent_name = tool_params.get('subagent_type', 'unknown')
    task_description = tool_params.get('prompt')

    # Model tier: an explicit `model` on the launch wins; otherwise fall back to
    # the agent's declared tier in REGISTRY.json. Effort is not a launch
    # parameter, so it always comes from the registry.
    registry_model, effort = resolve_agent_tier(agent_name)
    model = tool_params.get('model') or registry_model

    # Check if this is a sub-agent (launched by another agent)
    parent_id = get_current_execution_id()  # Will be None if no parent

    try:
        # Insert execution record
        execution_id = insert_execution(
            agent_name=agent_name,
            task_description=task_description,
            parent_id=parent_id,
            model=model,
            effort=effort
        )

        # Store execution ID for end hook
        set_current_execution_id(execution_id)

        # Output for logging (optional)
        tier = f"{model}/{effort}" if model else "untiered"
        print(f"📊 Tracking: {agent_name} ({tier})", file=sys.stderr)
        if parent_id:
            print(f"   Sub-agent of execution #{parent_id}", file=sys.stderr)

    except Exception as e:
        print(f"Warning: Failed to track task start: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block on error


if __name__ == '__main__':
    main()
