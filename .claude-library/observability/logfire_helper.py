"""
Logfire integration helper for Claude Agent Framework.

IMPORTANT: Requires LOGFIRE_TOKEN environment variable or Logfire CLI authentication.
Get your free API key at: https://logfire.pydantic.dev/
"""

import os
import json
import logfire
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

# Initialize Logfire
try:
    logfire.configure()
    LOGFIRE_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Logfire initialization warning: {e}")
    print("Continuing without Logfire - observability will be disabled")
    LOGFIRE_AVAILABLE = False

CONTEXT_FILE = Path("/tmp/claude-workflow-context.json")


def get_workflow_context() -> Optional[Dict[str, Any]]:
    """Read shared workflow context created by launcher."""
    if CONTEXT_FILE.exists():
        return json.loads(CONTEXT_FILE.read_text())
    return None


def create_workflow_context(command: str, project: str) -> Dict[str, Any]:
    """
    Create workflow context file for agents to share.
    Called by agent launcher at workflow initialization.
    """
    workflow_id = f"wf-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    context = {
        "workflow_id": workflow_id,
        "command": command,
        "project": project,
        "started_at": datetime.now().isoformat(),
        "observability_enabled": True
    }

    CONTEXT_FILE.write_text(json.dumps(context, indent=2))
    return context


def clear_workflow_context():
    """Remove workflow context file after completion."""
    if CONTEXT_FILE.exists():
        CONTEXT_FILE.unlink()


@contextmanager
def log_agent_task(
    agent_type: str,
    task_description: str,
    **extra_attributes
):
    """
    Context manager for agents to log their work.

    Usage in agent:
        with log_agent_task('architect', 'Design auth system') as span:
            # do work
            span.set_attribute('files_created', ['auth.py'])
            span.set_attribute('status', 'success')
    """
    if not LOGFIRE_AVAILABLE:
        yield None
        return

    ctx = get_workflow_context()

    if not ctx:
        # Observability enabled but no context? Log warning
        print("⚠️  Observability enabled but no workflow context found")
        yield None
        return

    with logfire.span(
        f'agent: {agent_type}',
        workflow_id=ctx['workflow_id'],
        task=task_description,
        agent_type=agent_type,
        **extra_attributes
    ) as span:
        yield span


@contextmanager
def log_workflow(command: str, project: str):
    """
    Context manager for launcher to log entire workflow.

    Usage in launcher:
        with log_workflow('/build', 'myapp') as workflow:
            # spawn agents
            workflow.set_attribute('total_agents', 5)
            workflow.set_attribute('status', 'success')
    """
    if not LOGFIRE_AVAILABLE:
        print("⚠️  Logfire not available - workflow will not be logged")
        yield None
        return

    context = create_workflow_context(command, project)

    with logfire.span(
        f'workflow: {command}',
        workflow_id=context['workflow_id'],
        command=command,
        project=project
    ) as span:
        try:
            yield span
        finally:
            clear_workflow_context()


def log_parallel_group(group_name: str, agent_types: List[str]):
    """
    Log a parallel execution group.

    Usage:
        log_parallel_group('architecture', ['architect', 'test-planner', 'researcher'])
    """
    if not LOGFIRE_AVAILABLE:
        return

    ctx = get_workflow_context()
    if ctx:
        with logfire.span(
            f'parallel_group: {group_name}',
            workflow_id=ctx['workflow_id'],
            agents=agent_types,
            agent_count=len(agent_types)
        ):
            pass  # Span created to mark the parallel group in traces


def log_validation_result(
    agent_type: str,
    claimed_outputs: List[str],
    actual_outputs: List[str],
    validation_passed: bool,
    **extra_details
):
    """
    Log validation results from Observer agent.

    Usage:
        log_validation_result(
            'architect',
            claimed_outputs=['schema.md'],
            actual_outputs=['schema.md'],
            validation_passed=True
        )
    """
    if not LOGFIRE_AVAILABLE:
        return

    ctx = get_workflow_context()
    if ctx:
        logfire.info(
            'validation_result',
            workflow_id=ctx['workflow_id'],
            agent_type=agent_type,
            claimed_outputs=claimed_outputs,
            actual_outputs=actual_outputs,
            validation_passed=validation_passed,
            missing_outputs=[f for f in claimed_outputs if f not in actual_outputs],
            **extra_details
        )


def query_workflow_spans(workflow_id: str) -> List[Dict[str, Any]]:
    """
    Query Logfire for all spans in a workflow.

    Note: This is a placeholder - actual implementation would use Logfire's query API
    """
    if not LOGFIRE_AVAILABLE:
        return []

    # This would use Logfire's actual query API
    # For now, return empty list as placeholder
    print(f"🔍 Would query Logfire for workflow: {workflow_id}")
    print(f"📊 View traces at: https://logfire-us.pydantic.dev/notoriouscsv/agentframework")
    return []