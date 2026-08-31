#!/usr/bin/env python3
"""
Local Observability CLI Tool
Query and analyze agent execution data from project-local SQLite database

Usage:
    obs.py recent [--limit N]              # Show recent executions
    obs.py failed [--limit N]              # Show failed executions
    obs.py execution <id>                  # Show execution details
    obs.py summary [--days N]              # Show daily summary
    obs.py agents                          # Show agent performance
    obs.py session                         # Show current session info
    obs.py expectations                    # List task expectations
    obs.py cleanup [--days N]              # Delete old data
    obs.py tools <execution_id>            # Show tools used in execution
    obs.py tool-stats [tool_name]          # Show tool usage statistics
    obs.py tool-efficiency                 # Show tool efficiency metrics
"""

import sys
import json
from pathlib import Path
from typing import Optional
import argparse

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from db_helper import (
    get_recent_executions,
    get_execution,
    get_execution_sub_agents,
    get_execution_artifacts,
    get_execution_validation,
    get_daily_summary,
    get_agent_performance,
    get_session_id,
    cleanup_old_data,
    get_db,
    get_tool_usage_by_execution,
    get_tool_usage_stats,
    get_tool_efficiency
)


def format_duration(ms: Optional[int]) -> str:
    """Format duration in human-readable format"""
    if ms is None:
        return 'N/A'
    if ms < 1000:
        return f"{ms}ms"
    elif ms < 60000:
        return f"{ms/1000:.1f}s"
    else:
        return f"{ms/60000:.1f}m"


def format_cost(usd: Optional[float]) -> str:
    """Format cost in USD"""
    if usd is None:
        return '?'        # cost unknown (unpriced model) - not the same as free
    if usd == 0:
        return '$0.0000'
    return f"${usd:.4f}"


def format_tier(row) -> str:
    """Render model/effort as 'opus/xhigh'. Executions logged before tiers were
    tracked have no model; show them as '-' rather than blank."""
    try:
        model = row['model']
        effort = row['effort']
    except (KeyError, IndexError):
        return '-'
    if not model:
        return '-'
    return f"{model}/{effort}" if effort else model


def cmd_recent(args):
    """Show recent executions"""
    executions = get_recent_executions(limit=args.limit, failed_only=False)

    if not executions:
        print("No executions found")
        return

    print(f"\n📊 Recent Executions (last {len(executions)}):\n")
    print(f"{'ID':<5} {'Agent':<20} {'Status':<10} {'Model':<14} {'Duration':<10} {'Tokens':<10} {'Cost':<12} {'Time':<20}")
    print("-" * 116)

    for e in executions:
        status_icon = '✅' if e['status'] == 'success' else '❌'
        print(
            f"{e['id']:<5} "
            f"{e['agent_name'][:19]:<20} "
            f"{status_icon} {e['status']:<8} "
            f"{format_tier(e):<14} "
            f"{format_duration(e['duration_ms']):<10} "
            f"{e['tokens_total']:<10} "
            f"{format_cost(e['cost_usd']):<12} "
            f"{e['started_at'][:19]:<20}"
        )


def cmd_failed(args):
    """Show failed executions"""
    executions = get_recent_executions(limit=args.limit, failed_only=True)

    if not executions:
        print("✅ No failed executions found")
        return

    print(f"\n❌ Failed Executions (last {len(executions)}):\n")

    for e in executions:
        print(f"ID: {e['id']}")
        print(f"Agent: {e['agent_name']}")
        print(f"Task: {e['task_description'][:80] if e['task_description'] else 'N/A'}")
        print(f"Error: {e['error_message'] if 'error_message' in e else 'Unknown'}")
        print(f"Time: {e['started_at']}")
        print("-" * 80)


def cmd_execution(args):
    """Show execution details"""
    execution = get_execution(args.id)

    if not execution:
        print(f"Execution {args.id} not found")
        return

    print(f"\n📊 Execution #{execution['id']}:\n")
    print(f"Agent: {execution['agent_name']}")
    print(f"Status: {execution['status']}")
    print(f"Task: {execution['task_description'] if execution['task_description'] else 'N/A'}")
    print(f"Started: {execution['started_at']}")
    print(f"Duration: {format_duration(execution['duration_ms'])}")
    fresh = execution.get('tokens_fresh', execution['tokens_total'])
    cached = execution['tokens_total'] - fresh
    print(f"Tokens: {execution['tokens_total']} total "
          f"({fresh} fresh + {cached} cache) "
          f"(cost: {format_cost(execution['cost_usd'])})")

    # Sub-agents
    sub_agents = get_execution_sub_agents(args.id)
    if sub_agents:
        print(f"\n🤖 Sub-Agents ({len(sub_agents)}):")
        for sa in sub_agents:
            print(f"  - {sa['agent_name']} ({sa['agent_type']}) at {sa['launched_at'][:19]}")

    # Artifacts
    artifacts = get_execution_artifacts(args.id)
    if artifacts:
        print(f"\n📁 Artifacts ({len(artifacts)}):")
        for a in artifacts:
            size = f" ({a['artifact_size_bytes']} bytes)" if a['artifact_size_bytes'] else ""
            print(f"  - {a['artifact_type']}: {a['artifact_path'][:60]}{size}")

    # Tool Usage
    tools = get_tool_usage_by_execution(args.id)
    if tools:
        print(f"\n🔧 Tools Used ({len(tools)}):")
        for t in tools:
            status = "✅" if t['success'] else "❌"
            duration = f" ({format_duration(t['duration_ms'])})" if t['duration_ms'] else ""
            tokens = f" - {t['tokens_used']} tokens" if t['tokens_used'] else ""
            print(f"  {status} {t['tool_name']}{duration}{tokens} at {t['timestamp'][:19]}")

    # Validation
    validation = get_execution_validation(args.id)
    if validation:
        status = "✅ PASSED" if validation['passed'] else "❌ FAILED"
        print(f"\n🔍 Validation: {status} (score: {validation['score']})")
        if validation.get('violations'):
            print(f"Violations:")
            for v in validation['violations']:
                print(f"  - {v['type']}: expected {v['expected']}, got {v.get('actual', 'None')}")


def cmd_summary(args):
    """Show daily summary"""
    summary = get_daily_summary(days=args.days)

    if not summary:
        print("No data available")
        return

    print(f"\n📅 Daily Summary (last {args.days} days):\n")
    print(f"{'Date':<12} {'Total':<8} {'Success':<8} {'Failed':<8} {'Avg Time':<12} {'Tokens':<10} {'Cost':<12}")
    print("-" * 80)

    for s in summary:
        success_rate = f"{s['successful']/s['total_executions']*100:.0f}%" if s['total_executions'] > 0 else 'N/A'
        print(
            f"{s['date']:<12} "
            f"{s['total_executions']:<8} "
            f"{s['successful']:<8} "
            f"{s['failed']:<8} "
            f"{format_duration(s['avg_duration_ms']):<12} "
            f"{s['total_tokens']:<10} "
            f"{format_cost(s['total_cost_usd']):<12}"
        )


def cmd_agents(args):
    """Show agent performance"""
    agents = get_agent_performance()

    if not agents:
        print("No agent data available")
        return

    print(f"\n🤖 Agent Performance:\n")
    print(f"{'Agent':<25} {'Model':<14} {'Executions':<12} {'Success Rate':<15} {'Avg Time':<12} {'Avg Tokens':<12} {'Total Cost':<12}")
    print("-" * 116)

    for a in agents:
        success_rate = f"{a['successful']/a['total_executions']*100:.0f}%" if a['total_executions'] > 0 else 'N/A'
        print(
            f"{a['agent_name'][:24]:<25} "
            f"{format_tier(a):<14} "
            f"{a['total_executions']:<12} "
            f"{success_rate:<15} "
            f"{format_duration(a['avg_duration_ms']):<12} "
            f"{int(a['avg_tokens']) if a['avg_tokens'] else 0:<12} "
            f"{format_cost(a['total_cost_usd']):<12}"
        )


def cmd_cost_by_model(args):
    """Show cost aggregated by model tier"""
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM v_cost_by_model").fetchall()

    if not rows:
        print("No completed executions to report on")
        return

    print(f"\n💰 Cost by Model Tier:\n")
    print(f"{'Model':<18} {'Effort':<9} {'Runs':<7} {'OK':<6} {'Avg Time':<11} {'In':<10} {'Out':<10} {'CacheRd':<10} {'CacheWr':<10} {'Total':<12} {'Per Success':<12}")
    print("-" * 128)

    for r in rows:
        print(
            f"{r['model'][:17]:<18} "
            f"{r['effort']:<9} "
            f"{r['executions']:<7} "
            f"{r['successful']:<6} "
            f"{format_duration(r['avg_duration_ms']):<11} "
            f"{r['tokens_input']:<10} "
            f"{r['tokens_output']:<10} "
            f"{r['tokens_cached']:<10} "
            f"{r['tokens_cache_write']:<10} "
            f"{format_cost(r['total_cost_usd']):<12} "
            f"{format_cost(r['cost_per_success']):<12}"
        )

    warnings = []

    unrecorded = sum(r['executions'] for r in rows if r['model'] == 'unrecorded')
    if unrecorded:
        warnings.append(f"{unrecorded} execution(s) have no recorded model — cost could not be computed.")

    # A model string that IS recorded but has no rate entry prices as NULL. Without
    # this it renders as an ordinary row costing $0.00 and reads as a free tier.
    unpriced = sum(r['unpriced'] or 0 for r in rows)
    if unpriced:
        priced_models = ', '.join(sorted({r['model'] for r in rows if r['unpriced']}))
        warnings.append(
            f"{unpriced} execution(s) ran on a model with no rate in pricing.py "
            f"({priced_models}) — their cost is UNKNOWN, not zero."
        )

    # v_cost_by_model only covers completed executions. Anything that crashed or was
    # killed is excluded along with its cost - and those are disproportionately the
    # long, expensive runs. Report what is missing rather than under-total silently.
    with get_db() as conn:
        excl = conn.execute("""
            SELECT COUNT(*) AS n, COALESCE(SUM(m.cost_usd), 0.0) AS cost
            FROM executions e
            LEFT JOIN execution_metrics m ON m.execution_id = e.id
            WHERE e.completed_at IS NULL
        """).fetchone()
    if excl and excl['n']:
        warnings.append(
            f"{excl['n']} incomplete execution(s) excluded (never completed), "
            f"carrying {format_cost(excl['cost'])} in recorded cost."
        )

    for w in warnings:
        print(f"\n  ⚠  {w}")

    print("\n  Cost per success is the number to compare across tiers, not total cost:")
    print("  a cheaper tier that retries is not cheaper.")


def cmd_session(args):
    """Show current session info"""
    session_id = get_session_id()

    with get_db() as conn:
        cursor = conn.execute("""
            SELECT * FROM sessions WHERE session_id = ?
        """, (session_id,))
        session = cursor.fetchone()

        if not session:
            print("No session found")
            return

        print(f"\n🔄 Current Session:\n")
        print(f"ID: {session['session_id']}")
        print(f"Started: {session['started_at']}")
        print(f"Project: {session['project_path']}")
        if session['git_branch']:
            print(f"Git: {session['git_branch']} ({session['git_commit']})")
        print(f"Executions: {session['total_executions']}")
        print(f"Tokens: {session['total_tokens']}")
        print(f"Cost: {format_cost(session['total_cost_usd'])}")


def cmd_expectations(args):
    """List task expectations"""
    with get_db() as conn:
        cursor = conn.execute("""
            SELECT * FROM task_expectations
            WHERE enabled = 1
            ORDER BY id
        """)
        expectations = cursor.fetchall()

        if not expectations:
            print("No expectations defined")
            return

        print(f"\n📋 Task Expectations:\n")

        for exp in expectations:
            print(f"ID {exp['id']}: {exp['description']}")
            print(f"  Pattern: {exp['task_pattern']}")
            if exp['expected_agents']:
                print(f"  Expected Agents: {exp['expected_agents']}")
            if exp['max_duration_ms']:
                print(f"  Max Duration: {format_duration(exp['max_duration_ms'])}")
            if exp['max_tokens']:
                print(f"  Max Tokens: {exp['max_tokens']}")
            if exp['max_cost_usd']:
                print(f"  Max Cost: {format_cost(exp['max_cost_usd'])}")
            print()


def cmd_cleanup(args):
    """Delete old data"""
    print(f"Deleting executions older than {args.days} days...")
    cleanup_old_data(days=args.days)
    print("✅ Cleanup complete")


def cmd_tools(args):
    """Show tools used in an execution"""
    tools = get_tool_usage_by_execution(args.execution_id)

    if not tools:
        print(f"No tool usage found for execution {args.execution_id}")
        return

    print(f"\n🔧 Tools Used in Execution #{args.execution_id} ({len(tools)}):\n")
    print(f"{'#':<4} {'Tool':<20} {'Status':<10} {'Duration':<12} {'Tokens':<10} {'Output Size':<12} {'Time':<20}")
    print("-" * 100)

    for i, t in enumerate(tools, 1):
        status = "✅ Success" if t['success'] else "❌ Failed"
        duration = format_duration(t['duration_ms']) if t['duration_ms'] else 'N/A'
        tokens = str(t['tokens_used']) if t['tokens_used'] else 'N/A'
        output_size = f"{t['output_size_bytes']} B" if t['output_size_bytes'] else 'N/A'
        print(
            f"{i:<4} "
            f"{t['tool_name'][:19]:<20} "
            f"{status:<10} "
            f"{duration:<12} "
            f"{tokens:<10} "
            f"{output_size:<12} "
            f"{t['timestamp'][:19]:<20}"
        )


def cmd_tool_stats(args):
    """Show statistics for a specific tool or all tools"""
    stats = get_tool_usage_stats(tool_name=args.tool_name if args.tool_name else None)

    if not stats:
        print("No tool usage data available")
        return

    if args.tool_name:
        print(f"\n🔧 Tool Statistics: {args.tool_name}\n")
    else:
        print(f"\n🔧 Tool Usage Statistics (all tools):\n")

    print(f"{'Tool':<25} {'Total':<8} {'Success':<9} {'Failed':<8} {'Rate':<8} {'Avg Time':<12} {'Total Tokens':<14} {'Avg Tokens':<12}")
    print("-" * 110)

    for s in stats:
        print(
            f"{s['tool_name'][:24]:<25} "
            f"{s['total_calls']:<8} "
            f"{s['successful_calls']:<9} "
            f"{s['failed_calls']:<8} "
            f"{s['success_rate']:.1f}%{'':<4} "
            f"{format_duration(s['avg_duration_ms']):<12} "
            f"{s['total_tokens']:<14} "
            f"{int(s['avg_tokens']) if s['avg_tokens'] else 0:<12}"
        )


def cmd_tool_efficiency(args):
    """Show tool efficiency metrics (tokens per success)"""
    efficiency = get_tool_efficiency()

    if not efficiency:
        print("No tool efficiency data available")
        return

    print(f"\n🎯 Tool Efficiency (Tokens per Successful Call):\n")
    print(f"{'Tool':<25} {'Total Calls':<12} {'Successful':<12} {'Total Tokens':<14} {'Tokens/Success':<16} {'Avg Duration':<12}")
    print("-" * 100)

    for e in efficiency:
        print(
            f"{e['tool_name'][:24]:<25} "
            f"{e['total_calls']:<12} "
            f"{e['successful_calls']:<12} "
            f"{e['total_tokens']:<14} "
            f"{int(e['tokens_per_success']) if e['tokens_per_success'] else 0:<16} "
            f"{format_duration(e['avg_duration_ms']):<12}"
        )


def main():
    parser = argparse.ArgumentParser(description='Local Observability CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Recent executions
    p_recent = subparsers.add_parser('recent', help='Show recent executions')
    p_recent.add_argument('--limit', type=int, default=20, help='Number of executions to show')
    p_recent.set_defaults(func=cmd_recent)

    # Failed executions
    p_failed = subparsers.add_parser('failed', help='Show failed executions')
    p_failed.add_argument('--limit', type=int, default=10, help='Number to show')
    p_failed.set_defaults(func=cmd_failed)

    # Execution details
    p_exec = subparsers.add_parser('execution', help='Show execution details')
    p_exec.add_argument('id', type=int, help='Execution ID')
    p_exec.set_defaults(func=cmd_execution)

    # Daily summary
    p_summary = subparsers.add_parser('summary', help='Show daily summary')
    p_summary.add_argument('--days', type=int, default=7, help='Number of days')
    p_summary.set_defaults(func=cmd_summary)

    # Agent performance
    p_agents = subparsers.add_parser('agents', help='Show agent performance')
    p_agents.set_defaults(func=cmd_agents)

    # Session info
    p_cost = subparsers.add_parser('cost-by-model', help='Show cost aggregated by model tier')
    p_cost.set_defaults(func=cmd_cost_by_model)

    p_session = subparsers.add_parser('session', help='Show current session')
    p_session.set_defaults(func=cmd_session)

    # Expectations
    p_expect = subparsers.add_parser('expectations', help='List task expectations')
    p_expect.set_defaults(func=cmd_expectations)

    # Cleanup
    p_cleanup = subparsers.add_parser('cleanup', help='Delete old data')
    p_cleanup.add_argument('--days', type=int, default=30, help='Keep data newer than N days')
    p_cleanup.set_defaults(func=cmd_cleanup)

    # Tools used in execution
    p_tools = subparsers.add_parser('tools', help='Show tools used in an execution')
    p_tools.add_argument('execution_id', type=int, help='Execution ID')
    p_tools.set_defaults(func=cmd_tools)

    # Tool statistics
    p_tool_stats = subparsers.add_parser('tool-stats', help='Show tool usage statistics')
    p_tool_stats.add_argument('tool_name', nargs='?', help='Filter by specific tool (optional)')
    p_tool_stats.set_defaults(func=cmd_tool_stats)

    # Tool efficiency
    p_tool_eff = subparsers.add_parser('tool-efficiency', help='Show tool efficiency metrics')
    p_tool_eff.set_defaults(func=cmd_tool_efficiency)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    args.func(args)


if __name__ == '__main__':
    main()
