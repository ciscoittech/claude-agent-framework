#!/usr/bin/env python3
"""
Test Template for Best Practice Validation
Tests improvements from applying Anthropic best practices to the framework

This template follows the proven pattern from test_observability.py:
- Easy: Single simple task
- Medium: Multi-step workflow
- Hard: Complex parallel agents with edge cases

USAGE:
1. Copy this file to test_best_practice_{name}.py
2. Customize the test scenarios for your specific best practice
3. Define before/after metrics
4. Run: pytest test_best_practice_{name}.py -v
"""

import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Test configuration
BEST_PRACTICE_NAME = "template"  # CUSTOMIZE THIS
EXPERIMENT_DIR = Path(f".claude-library/experiments/{BEST_PRACTICE_NAME}")
BASELINE_DIR = EXPERIMENT_DIR / "baseline"
IMPROVED_DIR = EXPERIMENT_DIR / "improved"

# Test results tracking
test_results = []
baseline_metrics = {}
improved_metrics = {}


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


def measure_metric(metric_name, value, category="baseline"):
    """Track a metric for before/after comparison"""
    if category == "baseline":
        baseline_metrics[metric_name] = value
    else:
        improved_metrics[metric_name] = value


# ============================================================================
# TEST CASE 1: EASY COMPLEXITY
# ============================================================================

def test_easy_baseline():
    """
    Baseline: Simple task with CURRENT framework implementation

    CUSTOMIZE:
    - Define your simple task scenario
    - Measure relevant metrics (tokens, time, quality)
    """
    print("\n" + "="*60)
    print("TEST CASE 1A: EASY - BASELINE (Current Framework)")
    print("="*60)

    try:
        start_time = time.time()

        # EXAMPLE: Simulate agent task with current framework
        # TODO: Customize this for your best practice
        task_description = "Create a simple Python function"

        # Simulate work (replace with actual agent invocation)
        time.sleep(0.1)  # Placeholder

        duration_ms = (time.time() - start_time) * 1000

        # Measure baseline metrics
        measure_metric("easy_duration_ms", duration_ms, "baseline")
        measure_metric("easy_tokens", 500, "baseline")  # Example
        measure_metric("easy_quality_score", 70, "baseline")  # Example

        log_test("Easy Baseline", True,
                f"Duration: {duration_ms:.0f}ms, Tokens: 500, Quality: 70/100")
        return True

    except Exception as e:
        log_test("Easy Baseline", False, str(e))
        return False


def test_easy_improved():
    """
    Improved: Same simple task with BEST PRACTICE applied

    CUSTOMIZE:
    - Apply your best practice improvements
    - Measure same metrics for comparison
    """
    print("\n" + "="*60)
    print("TEST CASE 1B: EASY - IMPROVED (With Best Practice)")
    print("="*60)

    try:
        start_time = time.time()

        # EXAMPLE: Simulate agent task with improvements
        # TODO: Customize with your best practice implementation
        task_description = "Create a simple Python function"

        # Simulate improved work
        time.sleep(0.08)  # Placeholder - should be faster/better

        duration_ms = (time.time() - start_time) * 1000

        # Measure improved metrics
        measure_metric("easy_duration_ms", duration_ms, "improved")
        measure_metric("easy_tokens", 400, "improved")  # Should be better
        measure_metric("easy_quality_score", 85, "improved")  # Should be better

        log_test("Easy Improved", True,
                f"Duration: {duration_ms:.0f}ms, Tokens: 400, Quality: 85/100")
        return True

    except Exception as e:
        log_test("Easy Improved", False, str(e))
        return False


# ============================================================================
# TEST CASE 2: MEDIUM COMPLEXITY
# ============================================================================

def test_medium_baseline():
    """
    Baseline: Multi-step workflow with current framework

    CUSTOMIZE:
    - Define multi-agent or multi-step scenario
    - Track coordination and handoff quality
    """
    print("\n" + "="*60)
    print("TEST CASE 2A: MEDIUM - BASELINE (Current Framework)")
    print("="*60)

    try:
        start_time = time.time()

        # EXAMPLE: Multi-agent workflow
        task_description = "Design and implement authentication system"

        # Simulate architect → engineer workflow
        time.sleep(0.2)  # Placeholder

        duration_ms = (time.time() - start_time) * 1000

        measure_metric("medium_duration_ms", duration_ms, "baseline")
        measure_metric("medium_tokens", 2500, "baseline")
        measure_metric("medium_handoff_quality", 65, "baseline")

        log_test("Medium Baseline", True,
                f"Duration: {duration_ms:.0f}ms, Tokens: 2500, Handoff: 65/100")
        return True

    except Exception as e:
        log_test("Medium Baseline", False, str(e))
        return False


def test_medium_improved():
    """
    Improved: Same workflow with best practice applied
    """
    print("\n" + "="*60)
    print("TEST CASE 2B: MEDIUM - IMPROVED (With Best Practice)")
    print("="*60)

    try:
        start_time = time.time()

        # EXAMPLE: Multi-agent workflow with improvements
        task_description = "Design and implement authentication system"

        # Simulate improved workflow
        time.sleep(0.15)  # Should be more efficient

        duration_ms = (time.time() - start_time) * 1000

        measure_metric("medium_duration_ms", duration_ms, "improved")
        measure_metric("medium_tokens", 2000, "improved")
        measure_metric("medium_handoff_quality", 85, "improved")

        log_test("Medium Improved", True,
                f"Duration: {duration_ms:.0f}ms, Tokens: 2000, Handoff: 85/100")
        return True

    except Exception as e:
        log_test("Medium Improved", False, str(e))
        return False


# ============================================================================
# TEST CASE 3: HARD COMPLEXITY
# ============================================================================

def test_hard_baseline():
    """
    Baseline: Complex parallel workflow with current framework

    CUSTOMIZE:
    - Define complex scenario with parallel agents
    - Test edge cases, error handling, recovery
    """
    print("\n" + "="*60)
    print("TEST CASE 3A: HARD - BASELINE (Current Framework)")
    print("="*60)

    try:
        start_time = time.time()

        # EXAMPLE: Complex parallel agents
        task_description = "Build API with tests, docs, and deployment"

        # Simulate parallel architect + engineer + tester + documenter
        time.sleep(0.4)  # Placeholder

        duration_ms = (time.time() - start_time) * 1000

        measure_metric("hard_duration_ms", duration_ms, "baseline")
        measure_metric("hard_tokens", 8000, "baseline")
        measure_metric("hard_error_rate", 15, "baseline")  # % of runs with errors
        measure_metric("hard_completeness", 80, "baseline")

        log_test("Hard Baseline", True,
                f"Duration: {duration_ms:.0f}ms, Tokens: 8000, Errors: 15%, Complete: 80%")
        return True

    except Exception as e:
        log_test("Hard Baseline", False, str(e))
        return False


def test_hard_improved():
    """
    Improved: Complex workflow with best practice applied
    """
    print("\n" + "="*60)
    print("TEST CASE 3B: HARD - IMPROVED (With Best Practice)")
    print("="*60)

    try:
        start_time = time.time()

        # EXAMPLE: Complex parallel agents with improvements
        task_description = "Build API with tests, docs, and deployment"

        # Simulate improved parallel workflow
        time.sleep(0.3)  # Should be better coordinated

        duration_ms = (time.time() - start_time) * 1000

        measure_metric("hard_duration_ms", duration_ms, "improved")
        measure_metric("hard_tokens", 6500, "improved")
        measure_metric("hard_error_rate", 5, "improved")
        measure_metric("hard_completeness", 95, "improved")

        log_test("Hard Improved", True,
                f"Duration: {duration_ms:.0f}ms, Tokens: 6500, Errors: 5%, Complete: 95%")
        return True

    except Exception as e:
        log_test("Hard Improved", False, str(e))
        return False


# ============================================================================
# BEFORE/AFTER COMPARISON
# ============================================================================

def compare_metrics():
    """Compare baseline vs improved metrics"""
    print("\n" + "="*80)
    print("BEFORE/AFTER COMPARISON")
    print("="*80)

    improvements = {}

    for metric_name in baseline_metrics:
        if metric_name in improved_metrics:
            baseline = baseline_metrics[metric_name]
            improved = improved_metrics[metric_name]

            # Calculate improvement percentage
            if "error" in metric_name or "duration" in metric_name:
                # Lower is better
                change_pct = ((baseline - improved) / baseline * 100)
            else:
                # Higher is better
                change_pct = ((improved - baseline) / baseline * 100)

            improvements[metric_name] = change_pct

            direction = "🔽" if change_pct > 0 else "🔼"
            print(f"\n{metric_name}:")
            print(f"  Baseline:  {baseline}")
            print(f"  Improved:  {improved}")
            print(f"  Change:    {direction} {abs(change_pct):.1f}%")

    # Calculate overall improvement score
    if improvements:
        avg_improvement = sum(improvements.values()) / len(improvements)
        print(f"\n{'='*80}")
        print(f"OVERALL IMPROVEMENT: {avg_improvement:+.1f}%")
        print(f"{'='*80}")

        return avg_improvement

    return 0.0


def check_simplicity_maintained():
    """Verify simplicity principle not violated"""
    print("\n" + "="*80)
    print("SIMPLICITY COMPLIANCE CHECK")
    print("="*80)

    # Check file count didn't explode
    baseline_files = len(list(BASELINE_DIR.rglob("*.md"))) if BASELINE_DIR.exists() else 0
    improved_files = len(list(IMPROVED_DIR.rglob("*.md"))) if IMPROVED_DIR.exists() else 0

    file_increase = improved_files - baseline_files

    print(f"File count: {baseline_files} → {improved_files} ({file_increase:+d})")

    if file_increase <= 2:
        print("✅ Simplicity maintained (file count acceptable)")
        simplicity_ok = True
    else:
        print("⚠️  Warning: File count increased significantly")
        simplicity_ok = False

    # Check context size
    # TODO: Implement actual context size checking

    return simplicity_ok


# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_report():
    """Generate final test report"""
    print("\n" + "="*80)
    print(f"BEST PRACTICE TEST REPORT: {BEST_PRACTICE_NAME.upper()}")
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
    print("TEST BREAKDOWN")
    print("-"*80)

    for result in test_results:
        status = "✅" if result['passed'] else "❌"
        print(f"{status} {result['name']}")
        if result['details']:
            print(f"   {result['details']}")

    # Comparison analysis
    avg_improvement = compare_metrics()
    simplicity_ok = check_simplicity_maintained()

    # Final verdict
    print("\n" + "="*80)
    print("VERDICT")
    print("="*80)

    if pass_rate == 100 and avg_improvement > 10 and simplicity_ok:
        print("🎉 RECOMMENDED FOR INTEGRATION")
        print(f"   - All tests passed")
        print(f"   - {avg_improvement:.1f}% average improvement")
        print(f"   - Simplicity maintained")
        verdict = "APPROVED"
    elif pass_rate >= 80 and avg_improvement > 5:
        print("⚠️  PARTIALLY RECOMMENDED")
        print(f"   - Most tests passed ({pass_rate:.0f}%)")
        print(f"   - {avg_improvement:.1f}% improvement")
        print(f"   - Review simplicity impact")
        verdict = "REVIEW"
    else:
        print("❌ NOT RECOMMENDED")
        print(f"   - Insufficient improvement or test failures")
        verdict = "REJECTED"

    print("="*80 + "\n")

    # Save report
    report_path = EXPERIMENT_DIR / "test-results" / f"report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, 'w') as f:
        json.dump({
            'best_practice': BEST_PRACTICE_NAME,
            'timestamp': datetime.now().isoformat(),
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'pass_rate': pass_rate,
            'avg_improvement': avg_improvement,
            'simplicity_ok': simplicity_ok,
            'verdict': verdict,
            'baseline_metrics': baseline_metrics,
            'improved_metrics': improved_metrics,
            'test_details': test_results
        }, f, indent=2)

    print(f"📄 Full report saved to: {report_path}")

    return verdict == "APPROVED"


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all test cases"""
    print("="*80)
    print(f"BEST PRACTICE VALIDATION: {BEST_PRACTICE_NAME.upper()}")
    print("Testing framework improvements across Easy, Medium, Hard scenarios")
    print("="*80)

    # Ensure experiment directory exists
    EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)

    # Run baseline tests
    print("\n" + "🔵 BASELINE TESTS (Current Framework)")
    test_easy_baseline()
    test_medium_baseline()
    test_hard_baseline()

    # Run improved tests
    print("\n" + "🟢 IMPROVED TESTS (With Best Practice)")
    test_easy_improved()
    test_medium_improved()
    test_hard_improved()

    # Generate comprehensive report
    success = generate_report()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
