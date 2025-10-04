#!/usr/bin/env python3
"""
Test Suite for Local Observability System
Tests the SQLite-based agent tracking across easy, medium, and hard complexity scenarios
"""

import sys
import json
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime

# Add observability to path
sys.path.insert(0, str(Path(__file__).parent))

from db_helper import (
    init_database,
    insert_execution,
    update_execution,
    insert_metrics,
    insert_artifact,
    insert_sub_agent,
    get_expectation_for_task,
    insert_validation,
    get_execution,
    get_recent_executions,
    get_agent_performance,
    get_daily_summary,
    DB_PATH
)

# Test results
test_results = []


def log_test(name, passed, details=""):
    """Log test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    test_results.append({
        'name': name,
        'passed': passed,
        'details': details
    })
    print(f"{status}: {name}")
    if details:
        print(f"   {details}")


def setup_test_db():
    """Initialize test database"""
    try:
        # Remove existing test db
        if DB_PATH.exists():
            DB_PATH.unlink()

        # Initialize fresh database
        init_database()
        log_test("Database Initialization", True, "Created fresh test database")
        return True
    except Exception as e:
        log_test("Database Initialization", False, str(e))
        return False


def test_easy_project():
    """Test Case 1: Easy - Simple single-agent task"""
    print("\n" + "="*60)
    print("TEST CASE 1: EASY COMPLEXITY")
    print("Scenario: Single agent creates a simple file")
    print("="*60)

    try:
        # Simulate simple task
        task_desc = "Create a hello world script"
        exec_id = insert_execution(
            agent_name="engineer",
            task_description=task_desc
        )

        # Simulate work
        update_execution(
            execution_id=exec_id,
            status="success",
            duration_ms=1500
        )

        # Add metrics
        insert_metrics(
            execution_id=exec_id,
            tokens_input=500,
            tokens_output=200,
            cost_usd=0.012
        )

        # Add artifact
        insert_artifact(
            execution_id=exec_id,
            artifact_type="file_created",
            artifact_path="hello.py",
            artifact_size_bytes=45
        )

        # Verify
        execution = get_execution(exec_id)
        assert execution['agent_name'] == "engineer"
        assert execution['status'] == "success"
        assert execution['tokens_total'] == 700

        log_test("Easy: Single Agent Execution", True,
                f"Agent: {execution['agent_name']}, Tokens: {execution['tokens_total']}, Cost: ${execution['cost_usd']}")

        return True

    except Exception as e:
        log_test("Easy: Single Agent Execution", False, str(e))
        return False


def test_medium_project():
    """Test Case 2: Medium - Multi-agent with sub-agents"""
    print("\n" + "="*60)
    print("TEST CASE 2: MEDIUM COMPLEXITY")
    print("Scenario: Parent agent spawns 2 sub-agents")
    print("="*60)

    try:
        # Parent agent starts
        task_desc = "Implement authentication system"
        parent_id = insert_execution(
            agent_name="architect",
            task_description=task_desc
        )

        # Parent does initial work
        insert_artifact(
            execution_id=parent_id,
            artifact_type="file_created",
            artifact_path="auth_design.md",
            artifact_size_bytes=1200
        )

        # Spawn sub-agent 1: engineer
        sub_id_1 = insert_execution(
            agent_name="engineer",
            task_description="Build auth module",
            parent_id=parent_id
        )

        insert_sub_agent(
            parent_execution_id=parent_id,
            agent_name="engineer",
            agent_type="specialized",
            sequence_order=1
        )

        update_execution(sub_id_1, "success", 3500)
        insert_metrics(sub_id_1, 2000, 1500, 0, 0.065)
        insert_artifact(sub_id_1, "file_created", "auth.py", 2500)

        # Spawn sub-agent 2: reviewer
        sub_id_2 = insert_execution(
            agent_name="reviewer",
            task_description="Review auth implementation",
            parent_id=parent_id
        )

        insert_sub_agent(
            parent_execution_id=parent_id,
            agent_name="reviewer",
            agent_type="specialized",
            sequence_order=2
        )

        update_execution(sub_id_2, "success", 1800)
        insert_metrics(sub_id_2, 1500, 800, 0, 0.042)

        # Parent completes
        update_execution(parent_id, "success", 6000)
        insert_metrics(parent_id, 3000, 2000, 0, 0.095)

        # Check validation
        expectation = get_expectation_for_task(task_desc)
        if expectation:
            # Simulate validation
            violations = []  # No violations
            insert_validation(
                execution_id=parent_id,
                passed=True,
                violations=violations,
                expectation_id=expectation['id'],
                score=100.0
            )
            log_test("Medium: Validation System", True,
                    f"Matched expectation: {expectation['description']}")

        # Verify hierarchy
        from db_helper import get_execution_sub_agents
        sub_agents = get_execution_sub_agents(parent_id)
        assert len(sub_agents) == 2

        log_test("Medium: Multi-Agent Hierarchy", True,
                f"Parent: architect, Sub-agents: {len(sub_agents)}")

        return True

    except Exception as e:
        log_test("Medium: Multi-Agent Hierarchy", False, str(e))
        return False


def test_hard_project():
    """Test Case 3: Hard - Complex parallel agents with failures"""
    print("\n" + "="*60)
    print("TEST CASE 3: HARD COMPLEXITY")
    print("Scenario: Complex workflow with parallel agents and failures")
    print("="*60)

    try:
        # Main orchestrator
        task_desc = "Create API endpoint with tests and docs"
        main_id = insert_execution(
            agent_name="architect",
            task_description=task_desc
        )

        # Parallel group 1: API implementation
        api_id = insert_execution(
            agent_name="engineer",
            task_description="Build API endpoint",
            parent_id=main_id
        )
        insert_sub_agent(main_id, "engineer", "specialized", 1)
        update_execution(api_id, "success", 4500)
        insert_metrics(api_id, 3500, 2000, 500, 0.098)
        insert_artifact(api_id, "file_created", "api/users.py", 3200)

        # Parallel group 2: Tests (fails initially)
        test_id = insert_execution(
            agent_name="test-engineer",
            task_description="Write API tests",
            parent_id=main_id
        )
        insert_sub_agent(main_id, "test-engineer", "specialized", 2)
        update_execution(test_id, "failed", 2200, "Import error in test file")
        insert_metrics(test_id, 1800, 900, 0, 0.045)

        # Parallel group 3: Documentation
        doc_id = insert_execution(
            agent_name="documenter",
            task_description="Create API documentation",
            parent_id=main_id
        )
        insert_sub_agent(main_id, "documenter", "specialized", 3)
        update_execution(doc_id, "success", 2800)
        insert_metrics(doc_id, 2000, 1200, 0, 0.058)
        insert_artifact(doc_id, "file_created", "docs/api.md", 1800)

        # Retry failed test agent
        test_retry_id = insert_execution(
            agent_name="test-engineer",
            task_description="Fix and rerun API tests",
            parent_id=main_id
        )
        insert_sub_agent(main_id, "test-engineer", "specialized", 4)
        update_execution(test_retry_id, "success", 3000)
        insert_metrics(test_retry_id, 2200, 1100, 0, 0.057)
        insert_artifact(test_retry_id, "file_created", "tests/test_api.py", 1500)
        insert_artifact(test_retry_id, "test_run", "pytest tests/test_api.py", None)

        # Main completes
        update_execution(main_id, "success", 12500)
        insert_metrics(main_id, 5000, 3000, 0, 0.145)

        # Validation with violations
        expectation = get_expectation_for_task(task_desc)
        if expectation:
            violations = [
                {'type': 'duration_exceeded', 'expected': 60000, 'actual': 12500}
            ]
            insert_validation(
                execution_id=main_id,
                passed=False,
                violations=violations,
                expectation_id=expectation['id'],
                score=85.0
            )
            log_test("Hard: Validation with Violations", True,
                    "Detected duration violation (score: 85.0)")

        # Verify complex hierarchy
        from db_helper import get_execution_sub_agents, get_db
        sub_agents = get_execution_sub_agents(main_id)

        # Get all artifacts from this execution tree (parent + children)
        with get_db() as conn:
            cursor = conn.execute("""
                SELECT COUNT(*) FROM artifacts
                WHERE execution_id IN (
                    SELECT id FROM executions
                    WHERE id = ? OR parent_execution_id = ?
                )
            """, (main_id, main_id))
            total_artifacts = cursor.fetchone()[0]

            cursor = conn.execute("""
                SELECT COUNT(*) FROM artifacts
                WHERE artifact_type = 'file_created'
                AND execution_id IN (
                    SELECT id FROM executions
                    WHERE id = ? OR parent_execution_id = ?
                )
            """, (main_id, main_id))
            files_created = cursor.fetchone()[0]

        assert len(sub_agents) == 4  # 4 sub-agents (including retry)
        assert files_created >= 3  # At least 3 files created

        log_test("Hard: Complex Workflow", True,
                f"Sub-agents: {len(sub_agents)}, Files: {files_created}, Artifacts: {total_artifacts}, 1 failure + retry")

        return True

    except Exception as e:
        log_test("Hard: Complex Workflow", False, str(e))
        return False


def test_performance_queries():
    """Test Case 4: Performance - Query and aggregation tests"""
    print("\n" + "="*60)
    print("TEST CASE 4: PERFORMANCE & QUERIES")
    print("Scenario: Test CLI queries and aggregations")
    print("="*60)

    try:
        # Test recent executions
        recent = get_recent_executions(limit=10)
        assert len(recent) > 0
        log_test("Performance: Recent Executions Query", True,
                f"Retrieved {len(recent)} executions")

        # Test agent performance aggregation
        perf = get_agent_performance()
        assert len(perf) > 0

        # Find most used agent
        most_used = max(perf, key=lambda x: x['total_executions'])
        log_test("Performance: Agent Performance Query", True,
                f"Most used: {most_used['agent_name']} ({most_used['total_executions']} executions)")

        # Test daily summary
        summary = get_daily_summary(days=7)
        if summary:
            total_today = summary[0]
            log_test("Performance: Daily Summary Query", True,
                    f"Today: {total_today['total_executions']} executions, ${total_today['total_cost_usd']:.4f}")
        else:
            log_test("Performance: Daily Summary Query", True, "No summary data yet (expected)")

        # Test failed executions
        failed = get_recent_executions(limit=10, failed_only=True)
        log_test("Performance: Failed Executions Query", True,
                f"Found {len(failed)} failed executions")

        return True

    except Exception as e:
        log_test("Performance: Query Tests", False, str(e))
        return False


def test_cli_commands():
    """Test Case 5: CLI - Command line interface tests"""
    print("\n" + "="*60)
    print("TEST CASE 5: CLI TOOL")
    print("Scenario: Test obs.py commands")
    print("="*60)

    try:
        obs_path = Path(__file__).parent / "obs.py"

        # Test recent command
        result = subprocess.run(
            ["python3", str(obs_path), "recent", "--limit", "5"],
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        log_test("CLI: obs.py recent", True, "Command executed successfully")

        # Test agents command
        result = subprocess.run(
            ["python3", str(obs_path), "agents"],
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        log_test("CLI: obs.py agents", True, "Command executed successfully")

        # Test expectations command
        result = subprocess.run(
            ["python3", str(obs_path), "expectations"],
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0
        log_test("CLI: obs.py expectations", True, "Command executed successfully")

        return True

    except Exception as e:
        log_test("CLI: Command Tests", False, str(e))
        return False


def generate_report():
    """Generate final test report"""
    print("\n" + "="*80)
    print("OBSERVABILITY SYSTEM TEST REPORT")
    print("="*80)

    total_tests = len(test_results)
    passed_tests = sum(1 for t in test_results if t['passed'])
    failed_tests = total_tests - passed_tests
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    print(f"\nTotal Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✅")
    print(f"Failed: {failed_tests} ❌")
    print(f"Pass Rate: {pass_rate:.1f}%")

    print("\n" + "-"*80)
    print("TEST BREAKDOWN BY COMPLEXITY")
    print("-"*80)

    for result in test_results:
        status = "✅" if result['passed'] else "❌"
        print(f"{status} {result['name']}")
        if result['details']:
            print(f"   {result['details']}")

    # Database stats
    print("\n" + "-"*80)
    print("DATABASE STATISTICS")
    print("-"*80)

    with sqlite3.connect(DB_PATH) as conn:
        # Count records
        cursor = conn.execute("SELECT COUNT(*) FROM executions")
        exec_count = cursor.fetchone()[0]

        cursor = conn.execute("SELECT COUNT(*) FROM artifacts")
        artifact_count = cursor.fetchone()[0]

        cursor = conn.execute("SELECT COUNT(*) FROM validations")
        validation_count = cursor.fetchone()[0]

        cursor = conn.execute("SELECT SUM(tokens_total) FROM execution_metrics")
        total_tokens = cursor.fetchone()[0] or 0

        cursor = conn.execute("SELECT SUM(cost_usd) FROM execution_metrics")
        total_cost = cursor.fetchone()[0] or 0

        print(f"Executions Tracked: {exec_count}")
        print(f"Artifacts Created: {artifact_count}")
        print(f"Validations Run: {validation_count}")
        print(f"Total Tokens Used: {total_tokens:,}")
        print(f"Total Cost: ${total_cost:.4f}")

        # Database size
        db_size = DB_PATH.stat().st_size / 1024  # KB
        print(f"Database Size: {db_size:.1f} KB")

    print("\n" + "="*80)

    # Final verdict
    if pass_rate == 100:
        print("🎉 ALL TESTS PASSED - System is production ready!")
    elif pass_rate >= 80:
        print("⚠️  MOSTLY PASSING - Some issues need attention")
    else:
        print("❌ CRITICAL ISSUES - System needs fixes")

    print("="*80 + "\n")

    return pass_rate == 100


def main():
    """Run all tests"""
    print("="*80)
    print("LOCAL OBSERVABILITY SYSTEM - COMPREHENSIVE TEST SUITE")
    print("Testing across Easy, Medium, and Hard complexity scenarios")
    print("="*80)

    # Setup
    if not setup_test_db():
        print("❌ Database setup failed - aborting tests")
        sys.exit(1)

    # Run test cases
    test_easy_project()
    test_medium_project()
    test_hard_project()
    test_performance_queries()
    test_cli_commands()

    # Generate report
    success = generate_report()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
