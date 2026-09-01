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
import pricing

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


def test_model_pricing():
    """TEST CASE 6: Model tiers and cost calculation"""
    print("\n" + "="*60)
    print("TEST CASE 6: MODEL PRICING & TIER TRACKING")
    print("Scenario: Cost is computed from the recorded model tier")
    print("="*60)

    # --- pricing arithmetic, checked by hand ---
    # opus: 10k input @ $5/1M = $0.05, 5k output @ $25/1M = $0.125 -> $0.175
    cost = pricing.calculate_cost('opus', tokens_input=10_000, tokens_output=5_000)
    log_test("Pricing: opus arithmetic", abs(cost - 0.175) < 1e-9, f"10k in + 5k out = ${cost}")

    # haiku: 1M input @ $1/1M = $1.00 exactly
    cost = pricing.calculate_cost('haiku', tokens_input=1_000_000)
    log_test("Pricing: haiku arithmetic", abs(cost - 1.00) < 1e-9, f"1M in = ${cost}")

    # fable is 2x opus on both input and output
    o = pricing.calculate_cost('opus', tokens_input=1_000_000, tokens_output=1_000_000)
    f = pricing.calculate_cost('fable', tokens_input=1_000_000, tokens_output=1_000_000)
    log_test("Pricing: fable is 2x opus", abs(f - 2 * o) < 1e-9, f"opus ${o} vs fable ${f}")

    # cache reads bill at 0.1x the input rate
    cached = pricing.calculate_cost('opus', tokens_cached=100_000)
    fresh = pricing.calculate_cost('opus', tokens_input=100_000)
    log_test("Pricing: cache reads are 0.1x input",
             abs(cached - fresh * 0.1) < 1e-9, f"cached ${cached} vs fresh ${fresh}")

    # full model ids resolve to the same tier as short names
    log_test("Pricing: model id aliases resolve",
             pricing.calculate_cost('claude-opus-5', tokens_input=1000) ==
             pricing.calculate_cost('opus', tokens_input=1000),
             "claude-opus-5 == opus")

    # An unpriceable model returns None ("cost unknown"), never 0.0 ("free") and
    # never raises. Recording an unpriced tier as zero makes it look free, which is
    # worse than recording nothing at all.
    try:
        unknown = pricing.calculate_cost('some-future-model', tokens_input=1000)
        log_test("Pricing: unpriced model returns None, not 0.0",
                 unknown is None, f"got {unknown!r}")
    except Exception as e:
        log_test("Pricing: unpriced model returns None, not 0.0", False, f"raised {e}")

    # Dated / suffixed real model ids are also unpriced - they must not read as free
    log_test("Pricing: dated model ids are unpriced, not free",
             pricing.calculate_cost('claude-sonnet-4-5-20250929', tokens_input=500_000) is None,
             "unrecognized id -> None")

    # Cache WRITES are billed at a premium. Ignoring them made a repeatedly
    # invalidated prefix look cheaper than a correctly cached one.
    w = pricing.calculate_cost('opus', tokens_cache_write=100_000)
    fresh_in = pricing.calculate_cost('opus', tokens_input=100_000)
    log_test("Pricing: cache writes cost more than fresh input",
             abs(w - fresh_in * 1.25) < 1e-9, f"write ${w} vs input ${fresh_in}")
    r = pricing.calculate_cost('opus', tokens_cached=100_000)
    log_test("Pricing: cache write is priced above cache read",
             w > r, f"write ${w} > read ${r}")

    # haiku is the only 200K model - the most common tier mistake
    log_test("Pricing: haiku flagged as 200K",
             pricing.context_window('haiku') == 200_000 and
             pricing.context_window('opus') == 1_000_000,
             "haiku 200K, opus 1M")
    log_test("Pricing: long-context guard rejects haiku",
             not pricing.is_long_context_safe('haiku', 500_000) and
             pricing.is_long_context_safe('sonnet', 500_000),
             "500K tokens: haiku unsafe, sonnet safe")

    # --- model/effort round-trip through the database ---
    exec_id = insert_execution(
        agent_name="framework-system-architect",
        task_description="Design the tiering system",
        model="opus",
        effort="xhigh",
    )
    update_execution(exec_id, status="success", duration_ms=4200)
    insert_metrics(exec_id, tokens_input=10_000, tokens_output=5_000)

    row = get_execution(exec_id)
    log_test("Tiers: model/effort round-trip",
             row['model'] == 'opus' and row['effort'] == 'xhigh',
             f"stored {row['model']}/{row['effort']}")

    # cost was computed from the model, not supplied by the caller
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        m = conn.execute(
            "SELECT cost_usd FROM execution_metrics WHERE execution_id = ?", (exec_id,)
        ).fetchone()
    log_test("Tiers: cost auto-computed from model",
             abs(m['cost_usd'] - 0.175) < 1e-6,
             f"${m['cost_usd']} (expected $0.175, never supplied by caller)")

    # an explicit cost still wins
    exec_id2 = insert_execution(agent_name="observer", model="haiku", effort="low")
    update_execution(exec_id2, status="success", duration_ms=100)
    insert_metrics(exec_id2, tokens_input=1000, cost_usd=9.99)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        m2 = conn.execute(
            "SELECT cost_usd FROM execution_metrics WHERE execution_id = ?", (exec_id2,)
        ).fetchone()
    log_test("Tiers: explicit cost overrides calculation",
             abs(m2['cost_usd'] - 9.99) < 1e-6, f"${m2['cost_usd']}")

    # An unpriced model must store NULL cost, not 0.0
    exec_unpriced = insert_execution(agent_name="future-agent", model="claude-mystery-9")
    update_execution(exec_unpriced, status="success", duration_ms=100)
    insert_metrics(exec_unpriced, tokens_input=500_000, tokens_output=100_000)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        mu = conn.execute("SELECT cost_usd FROM execution_metrics WHERE execution_id = ?",
                          (exec_unpriced,)).fetchone()
    log_test("Tiers: unpriced model stores NULL cost, not 0.0",
             mu['cost_usd'] is None, f"cost_usd = {mu['cost_usd']!r}")

    # Cached tokens must count toward the reported total (they were excluded,
    # undercounting exactly the well-cached agents the framework optimizes for)
    exec_cached = insert_execution(agent_name="cached-agent", model="opus", effort="high")
    update_execution(exec_cached, status="success", duration_ms=100)
    insert_metrics(exec_cached, tokens_input=5_000, tokens_output=3_000,
                   tokens_cached=200_000, tokens_cache_write=10_000)
    rowc = get_execution(exec_cached)
    log_test("Tiers: reported tokens include cache reads and writes",
             rowc['tokens_total'] == 218_000,
             f"5k+3k+200k+10k = {rowc['tokens_total']} (fresh alone would be 8000)")

    # executions logged without a tier must still work (backward compatibility)
    exec_id3 = insert_execution(agent_name="legacy-agent")
    update_execution(exec_id3, status="success", duration_ms=50)
    insert_metrics(exec_id3, tokens_input=500, tokens_output=100)
    row3 = get_execution(exec_id3)
    log_test("Tiers: untiered execution still works",
             row3['model'] is None and row3['status'] == 'success',
             "no model recorded, cost 0.0, no exception")

    # --- the cost-by-model view ---
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM v_cost_by_model").fetchall()
    by_model = {r['model']: r for r in rows}
    log_test("View: v_cost_by_model aggregates tiers",
             'opus' in by_model and 'haiku' in by_model,
             f"tiers present: {sorted(by_model)}")
    log_test("View: untiered rows surface as 'unrecorded'",
             'unrecorded' in by_model,
             "executions without a model are visible, not silently dropped")


def test_schema_migration():
    """TEST CASE 7: Upgrading a database created before model/effort existed"""
    print("\n" + "="*60)
    print("TEST CASE 7: SCHEMA MIGRATION")
    print("Scenario: A real upgrade via init_database(), not _apply_migrations alone")
    print("="*60)

    import db_helper
    from db_helper import _apply_migrations

    migration_db = DB_PATH.parent / 'migration_test.db'
    if migration_db.exists():
        migration_db.unlink()

    # Reproduce the PRE-UPGRADE shape: executions without model/effort, plus a
    # view built against that old shape. This is what every existing install has.
    conn = sqlite3.connect(migration_db)
    conn.executescript("""
        CREATE TABLE executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            agent_name TEXT NOT NULL,
            task_description TEXT,
            parent_execution_id INTEGER,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            duration_ms INTEGER,
            status TEXT DEFAULT 'running',
            error_message TEXT
        );
        CREATE VIEW v_recent_executions AS
            SELECT id, agent_name, status FROM executions;
        INSERT INTO executions (session_id, agent_name) VALUES ('old', 'legacy');
    """)
    conn.commit()
    cols_before = {r[1] for r in conn.execute("PRAGMA table_info(executions)")}
    log_test("Migration: starts without model/effort",
             'model' not in cols_before, f"columns: {len(cols_before)}, no model")
    conn.close()

    # Drive the REAL upgrade path. Calling _apply_migrations directly would pass
    # even when init_database() is broken - which is exactly how an ordering bug
    # (schema.sql indexing a column migrations had not yet added) shipped green.
    original_db_path = db_helper.DB_PATH
    try:
        db_helper.DB_PATH = migration_db
        try:
            db_helper.init_database()
            init_ok, init_err = True, None
        except Exception as e:
            init_ok, init_err = False, f"{type(e).__name__}: {e}"
        log_test("Migration: init_database() succeeds on an old database",
                 init_ok, init_err or "upgraded in place")

        if init_ok:
            conn = sqlite3.connect(migration_db)
            conn.row_factory = sqlite3.Row

            cols_after = {r[1] for r in conn.execute("PRAGMA table_info(executions)")}
            log_test("Migration: adds model and effort",
                     {'model', 'effort'} <= cols_after, "columns added")

            row = conn.execute("SELECT agent_name, model FROM executions WHERE id=1").fetchone()
            log_test("Migration: existing rows preserved",
                     row['agent_name'] == 'legacy' and row['model'] is None,
                     "legacy row intact, model NULL")

            # The index that triggered the original failure must now exist
            idx = {r['name'] for r in conn.execute("PRAGMA index_list(executions)")}
            log_test("Migration: index on the migrated column created",
                     'idx_executions_model' in idx, "idx_executions_model present")

            # A stale view must be refreshed, not silently kept
            vcols = {d[0] for d in conn.execute(
                "SELECT * FROM v_recent_executions LIMIT 0").description}
            log_test("Migration: stale views are refreshed",
                     {'model', 'effort'} <= vcols,
                     "v_recent_executions rebuilt with model/effort")

            # New tables from schema.sql must also be created
            tables = {r['name'] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
            log_test("Migration: missing tables created",
                     'execution_metrics' in tables, "execution_metrics present")
            conn.close()

        # Re-running must be a clean no-op
        try:
            db_helper.init_database()
            log_test("Migration: repeated init is idempotent", True, "second run clean")
        except Exception as e:
            log_test("Migration: repeated init is idempotent", False, f"{type(e).__name__}: {e}")
    finally:
        db_helper.DB_PATH = original_db_path

    # _apply_migrations in isolation is still expected to be idempotent
    conn = sqlite3.connect(migration_db)
    log_test("Migration: _apply_migrations is a no-op when current",
             _apply_migrations(conn) == [], "nothing left to apply")
    conn.close()
    migration_db.unlink()


def test_hook_integration():
    """TEST CASE 8: Hook scripts end to end (regressions found by the smoke test)"""
    print("\n" + "="*60)
    print("TEST CASE 8: HOOK INTEGRATION")
    print("Scenario: The PreToolUse/PostToolUse scripts as Claude Code runs them")
    print("="*60)

    import time
    scripts = Path(__file__).parent / 'scripts'
    repo_root = Path(__file__).parent.parent.parent

    def run_hook(script, payload):
        """Invoke a hook the way the harness does: JSON on stdin, from repo root."""
        return subprocess.run(
            [sys.executable, str(scripts / script)],
            input=json.dumps(payload), text=True, capture_output=True,
            cwd=str(repo_root),
        )

    # The tool is named 'Agent'. Gating on 'Task' alone silently disabled every hook.
    r = run_hook('observe_task_start.py', {
        'tool': {'name': 'Agent',
                 'parameters': {'subagent_type': 'framework-system-architect', 'prompt': 'design'}}
    })
    log_test("Hooks: fire on tool name 'Agent'",
             'Tracking' in r.stderr, f"stderr: {r.stderr.strip()[:70]}")

    # Tier is resolved from REGISTRY.json when the launch does not name a model
    log_test("Hooks: resolve tier from registry",
             'opus/xhigh' in r.stderr,
             f"framework-system-architect -> {r.stderr.strip()[-20:]}")

    # 'Task' still accepted so older Claude Code versions keep working
    r_task = run_hook('observe_task_start.py', {
        'tool': {'name': 'Task', 'parameters': {'subagent_type': 'observer', 'prompt': 'verify'}}
    })
    log_test("Hooks: legacy 'Task' name still accepted",
             'Tracking' in r_task.stderr, "backward compatible")

    # A non-subagent tool must be ignored entirely
    r_other = run_hook('observe_task_start.py', {
        'tool': {'name': 'Bash', 'parameters': {'command': 'ls'}}
    })
    log_test("Hooks: ignore non-subagent tools",
             'Tracking' not in r_other.stderr, "Bash not tracked as an execution")

    # NOTE: set_current_execution_id() is a single slot, so observe_task_end.py
    # always attributes metrics to the most recent start. The paired start/end
    # below must therefore be adjacent, with no other launch in between.
    r_paired = run_hook('observe_task_start.py', {
        'tool': {'name': 'Agent',
                 'parameters': {'subagent_type': 'framework-code-reviewer', 'prompt': 'review'}}
    })
    with sqlite3.connect(DB_PATH) as conn:
        paired_id = conn.execute("SELECT MAX(id) FROM executions").fetchone()[0]

    # Duration must be positive. SQLite CURRENT_TIMESTAMP is UTC and datetime.now()
    # is local, so a naive comparison produced a large negative number.
    time.sleep(1.1)
    r_end = run_hook('observe_task_end.py', {
        'tool': {'name': 'Agent', 'parameters': {}},
        'result': {'usage': {'input_tokens': 10000, 'output_tokens': 5000,
                             'cache_read_input_tokens': 40000}},
    })
    duration_line = [l for l in r_end.stderr.splitlines() if 'Duration' in l]
    duration_ok = False
    if duration_line:
        ms = int(duration_line[0].split(':')[1].strip().rstrip('ms'))
        duration_ok = 0 < ms < 60_000
    log_test("Hooks: duration is positive without a payload timestamp",
             duration_ok,
             duration_line[0].strip() if duration_line else "no duration reported")

    # Cost must come from the recorded tier, not a hardcoded table in the hook.
    # opus: 10k in + 5k out + 40k cache reads = 0.05 + 0.125 + 0.02 = $0.195
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("""
            SELECT e.agent_name, e.model, e.effort, m.cost_usd
            FROM executions e JOIN execution_metrics m ON m.execution_id = e.id
            WHERE e.id = ?
        """, (paired_id,)).fetchone()
    log_test("Hooks: cost priced from the execution's own tier",
             row is not None and abs(row['cost_usd'] - 0.195) < 1e-6,
             f"{row['agent_name']} @ {row['model']} cost ${row['cost_usd']} (expected $0.195)"
             if row else "no row")
    log_test("Hooks: metrics attach to the launched agent",
             row is not None and row['agent_name'] == 'framework-code-reviewer',
             f"attributed to {row['agent_name'] if row else 'n/a'}")

    # Guard the specific regression: no hook may carry its own rate table
    end_src = (scripts / 'observe_task_end.py').read_text()
    log_test("Hooks: no duplicate pricing table in the end hook",
             'COST_PER_M_INPUT' not in end_src and '15.00' not in end_src,
             "pricing lives only in pricing.py")


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
    test_model_pricing()
    test_schema_migration()
    test_hook_integration()

    # Generate report
    success = generate_report()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
