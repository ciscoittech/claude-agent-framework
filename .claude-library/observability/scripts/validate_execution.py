#!/usr/bin/env python3
"""
PostToolUse Hook: Validate Task Execution Against Expectations
Checks if agent execution matches defined task expectations
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any

# Add observability library to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_helper import (
    get_execution,
    get_execution_sub_agents,
    get_execution_artifacts,
    get_expectation_for_task,
    insert_validation,
    get_current_execution_id
)


def validate_agents(expected_agents: List[str], actual_agents: List[str]) -> Dict[str, Any]:
    """Check if expected agents were launched"""
    violations = []

    for expected in expected_agents:
        if expected not in actual_agents:
            violations.append({
                'type': 'missing_agent',
                'expected': expected,
                'actual': None
            })

    return violations


def validate_files(expected_files: List[str], actual_files: List[str]) -> Dict[str, Any]:
    """Check if expected files were created/modified"""
    import fnmatch

    violations = []

    for expected_pattern in expected_files:
        # Check if any actual file matches the pattern
        matches = [f for f in actual_files if fnmatch.fnmatch(f, expected_pattern)]
        if not matches:
            violations.append({
                'type': 'missing_file',
                'expected': expected_pattern,
                'actual': None
            })

    return violations


def validate_artifacts(required_artifacts: List[str], actual_artifacts: List[Dict]) -> Dict[str, Any]:
    """Check if required artifact types were created"""
    violations = []

    actual_types = {a['artifact_type'] for a in actual_artifacts}

    for required in required_artifacts:
        if required not in actual_types:
            violations.append({
                'type': 'missing_artifact',
                'expected': required,
                'actual': None
            })

    return violations


def validate_performance(execution: Dict[str, Any], expectation: Dict[str, Any]) -> Dict[str, Any]:
    """Check if performance meets expectations"""
    violations = []

    # Duration check
    if expectation.get('max_duration_ms') and execution.get('duration_ms'):
        if execution['duration_ms'] > expectation['max_duration_ms']:
            violations.append({
                'type': 'duration_exceeded',
                'expected': expectation['max_duration_ms'],
                'actual': execution['duration_ms']
            })

    # Token check
    if expectation.get('max_tokens') and execution.get('tokens_total'):
        if execution['tokens_total'] > expectation['max_tokens']:
            violations.append({
                'type': 'tokens_exceeded',
                'expected': expectation['max_tokens'],
                'actual': execution['tokens_total']
            })

    # Cost check
    if expectation.get('max_cost_usd') and execution.get('cost_usd'):
        if execution['cost_usd'] > expectation['max_cost_usd']:
            violations.append({
                'type': 'cost_exceeded',
                'expected': expectation['max_cost_usd'],
                'actual': execution['cost_usd']
            })

    return violations


def calculate_score(total_checks: int, violations: List[Dict]) -> float:
    """Calculate validation score (0-100)"""
    if total_checks == 0:
        return 100.0

    passed = total_checks - len(violations)
    score = (passed / total_checks) * 100
    return round(score, 2)


def main():
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(0)

    # Only validate Task tool completions
    tool_name = hook_input.get('tool', {}).get('name')
    if tool_name != 'Task':
        sys.exit(0)

    # Get execution ID
    execution_id = get_current_execution_id()
    if not execution_id:
        sys.exit(0)

    # Skip validation if task failed
    if hook_input.get('error'):
        sys.exit(0)

    try:
        # Get execution details
        execution = get_execution(execution_id)
        if not execution or not execution.get('task_description'):
            sys.exit(0)

        # Check if there's an expectation for this task
        expectation = get_expectation_for_task(execution['task_description'])
        if not expectation:
            # No expectation defined, skip validation
            sys.exit(0)

        # Gather actual data
        sub_agents = get_execution_sub_agents(execution_id)
        artifacts = get_execution_artifacts(execution_id)

        actual_agent_names = [sa['agent_name'] for sa in sub_agents]
        actual_file_paths = [
            a['artifact_path'] for a in artifacts
            if a['artifact_type'] in ('file_created', 'file_modified')
        ]

        # Run validations
        all_violations = []
        total_checks = 0

        # Validate agents
        if expectation.get('expected_agents'):
            expected_agents = json.loads(expectation['expected_agents'])
            violations = validate_agents(expected_agents, actual_agent_names)
            all_violations.extend(violations)
            total_checks += len(expected_agents)

        # Validate files
        if expectation.get('expected_files'):
            expected_files = json.loads(expectation['expected_files'])
            violations = validate_files(expected_files, actual_file_paths)
            all_violations.extend(violations)
            total_checks += len(expected_files)

        # Validate artifacts
        if expectation.get('required_artifacts'):
            required_artifacts = json.loads(expectation['required_artifacts'])
            violations = validate_artifacts(required_artifacts, artifacts)
            all_violations.extend(violations)
            total_checks += len(required_artifacts)

        # Validate performance
        perf_violations = validate_performance(execution, expectation)
        all_violations.extend(perf_violations)
        total_checks += 3  # duration, tokens, cost

        # Calculate results
        passed = len(all_violations) == 0
        score = calculate_score(total_checks, all_violations)

        # Insert validation record
        insert_validation(
            execution_id=execution_id,
            passed=passed,
            violations=all_violations,
            expectation_id=expectation['id'],
            score=score
        )

        # Output results
        if passed:
            print(f"✅ Validation PASSED (score: {score})", file=sys.stderr)
        else:
            print(f"⚠️  Validation FAILED (score: {score})", file=sys.stderr)
            print(f"   {len(all_violations)} violations found", file=sys.stderr)

    except Exception as e:
        print(f"Warning: Validation error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
