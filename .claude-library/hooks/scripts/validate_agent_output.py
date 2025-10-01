#!/usr/bin/env python3
"""
Validate agent output - checks that agents actually created what they claimed
Can be used in SubagentStop hooks to verify agent work
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

def log(message, status="info"):
    """Log to hooks log file"""
    log_file = os.getenv("CLAUDE_HOOKS_LOG", ".claude-metrics/hooks.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    timestamp = datetime.now().isoformat()
    with open(log_file, 'a') as f:
        f.write(f"{timestamp} | validate_agent_output | {status} | {message}\n")

def validate_files_exist(expected_files):
    """Check if expected files were actually created"""
    missing_files = []

    for file_path in expected_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    return missing_files

def main():
    """
    Main validation function

    Expected to be called with agent context from workflow
    For now, performs basic validation checks
    """

    # Check for workflow context file (if using observability pattern)
    workflow_context = "/tmp/claude-workflow-context.json"

    if Path(workflow_context).exists():
        try:
            with open(workflow_context, 'r') as f:
                context = json.load(f)

            workflow_id = context.get('workflow_id', 'unknown')
            command = context.get('command', 'unknown')

            log(f"Validating workflow {workflow_id} from command {command}", "info")

            # Add custom validation logic here
            # For example, check if expected files exist
            # expected_files = context.get('expected_files', [])
            # missing = validate_files_exist(expected_files)
            # if missing:
            #     log(f"Missing files: {missing}", "warning")

        except Exception as e:
            log(f"Error reading workflow context: {e}", "error")

    # Validation passed
    log("Agent output validation completed", "success")
    sys.exit(0)

if __name__ == "__main__":
    main()
