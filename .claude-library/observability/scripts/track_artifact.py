#!/usr/bin/env python3
"""
PostToolUse Hook: Track File and Command Artifacts
Captures files created/modified and commands executed during agent tasks
"""

import sys
import json
from pathlib import Path

# Add observability library to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_helper import (
    insert_artifact,
    get_current_execution_id
)


def track_file_operations(tool_name, tool_params, execution_id):
    """Track file creation, modification, deletion"""
    artifact_type = None
    artifact_path = None
    artifact_size = None

    if tool_name == 'Write':
        artifact_type = 'file_created'
        artifact_path = tool_params.get('file_path')
        content = tool_params.get('content', '')
        artifact_size = len(content.encode('utf-8'))

    elif tool_name == 'Edit':
        artifact_type = 'file_modified'
        artifact_path = tool_params.get('file_path')

    elif tool_name == 'NotebookEdit':
        artifact_type = 'file_modified'
        artifact_path = tool_params.get('notebook_path')

    if artifact_type and artifact_path:
        insert_artifact(
            execution_id=execution_id,
            artifact_type=artifact_type,
            artifact_path=artifact_path,
            artifact_size_bytes=artifact_size
        )
        return True

    return False


def track_command_execution(tool_name, tool_params, execution_id):
    """Track bash commands and test executions"""
    if tool_name == 'Bash':
        command = tool_params.get('command', '')

        # Determine artifact type based on command
        if 'pytest' in command or 'test' in command:
            artifact_type = 'test_run'
        else:
            artifact_type = 'command_run'

        insert_artifact(
            execution_id=execution_id,
            artifact_type=artifact_type,
            artifact_path=command[:500],  # Truncate long commands
            artifact_size_bytes=None
        )
        return True

    return False


def main():
    # Read hook input from stdin (JSON format)
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(0)

    # Get current execution ID
    execution_id = get_current_execution_id()
    if not execution_id:
        # No execution being tracked
        sys.exit(0)

    # Extract tool info
    tool_name = hook_input.get('tool', {}).get('name')
    tool_params = hook_input.get('tool', {}).get('parameters', {})

    # Skip if tool call failed
    if hook_input.get('error'):
        sys.exit(0)

    try:
        # Track different types of artifacts
        tracked = False

        # File operations
        if tool_name in ('Write', 'Edit', 'NotebookEdit'):
            tracked = track_file_operations(tool_name, tool_params, execution_id)

        # Command executions
        elif tool_name == 'Bash':
            tracked = track_command_execution(tool_name, tool_params, execution_id)

        if tracked:
            print(f"📁 Artifact: {tool_name}", file=sys.stderr)

    except Exception as e:
        print(f"Warning: Failed to track artifact: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
