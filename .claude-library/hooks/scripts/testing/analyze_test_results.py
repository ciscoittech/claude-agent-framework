#!/usr/bin/env python3
"""
Post-Test Analysis Hook
Analyzes test results, extracts metrics, detects anomalies, and tracks accuracy
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

METRICS_DIR = Path(".claude-metrics/testing")
METRICS_DIR.mkdir(parents=True, exist_ok=True)

def parse_test_output(output, exit_code):
    """Parse test output and extract metrics"""
    metrics = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "exit_code": exit_code,
        "total_tests": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "pass_rate": 0.0,
        "execution_time_ms": 0,
        "anomalies": [],
        "warnings": []
    }

    # Parse test results from output
    # Pattern: "Total Tests: X"
    if match := re.search(r'Total Tests:\s+(\d+)', output):
        metrics["total_tests"] = int(match.group(1))

    # Pattern: "Passed: X"
    if match := re.search(r'Passed:\s+(\d+)', output):
        metrics["passed"] = int(match.group(1))

    # Pattern: "Failed: X"
    if match := re.search(r'Failed:\s+(\d+)', output):
        metrics["failed"] = int(match.group(1))

    # Calculate pass rate
    if metrics["total_tests"] > 0:
        metrics["pass_rate"] = (metrics["passed"] / metrics["total_tests"]) * 100

    # Extract execution time if available
    # Pattern: "real 0m2.345s" or similar
    if match := re.search(r'real\s+(\d+)m([\d.]+)s', output):
        minutes = int(match.group(1))
        seconds = float(match.group(2))
        metrics["execution_time_ms"] = int((minutes * 60 + seconds) * 1000)

    # Detect anomalies
    detect_anomalies(metrics, output)

    return metrics


def detect_anomalies(metrics, output):
    """Detect anomalies in test execution"""

    # Anomaly 1: Low pass rate
    if metrics["pass_rate"] < 90 and metrics["total_tests"] > 0:
        metrics["anomalies"].append({
            "type": "low_pass_rate",
            "severity": "high",
            "message": f"Pass rate {metrics['pass_rate']:.1f}% below 90% threshold"
        })

    # Anomaly 2: All tests failed
    if metrics["total_tests"] > 0 and metrics["passed"] == 0:
        metrics["anomalies"].append({
            "type": "all_tests_failed",
            "severity": "critical",
            "message": "All tests failed - possible environment issue"
        })

    # Anomaly 3: Execution time outlier (> 5 minutes)
    if metrics["execution_time_ms"] > 300000:
        metrics["anomalies"].append({
            "type": "slow_execution",
            "severity": "medium",
            "message": f"Execution time {metrics['execution_time_ms']/1000:.1f}s exceeds 5min threshold"
        })

    # Warning 1: Test errors in output
    if "ERROR" in output or "Exception" in output:
        error_count = output.count("ERROR") + output.count("Exception")
        metrics["warnings"].append({
            "type": "errors_detected",
            "count": error_count,
            "message": f"Found {error_count} error/exception references in output"
        })

    # Warning 2: Deprecation warnings
    if "DeprecationWarning" in output or "deprecated" in output.lower():
        metrics["warnings"].append({
            "type": "deprecations",
            "message": "Deprecation warnings detected - code may need updates"
        })


def update_session_metrics(metrics):
    """Update session metrics with test results"""
    session_file_path = METRICS_DIR / "current_session"

    if not session_file_path.exists():
        return

    try:
        session_file = Path(session_file_path.read_text().strip())

        if session_file.exists():
            with open(session_file) as f:
                session = json.load(f)

            # Update metrics
            session["metrics"]["total_tests"] += metrics["total_tests"]
            session["metrics"]["passed"] += metrics["passed"]
            session["metrics"]["failed"] += metrics["failed"]
            session["metrics"]["errors"] += len(metrics.get("anomalies", []))
            session["metrics"]["execution_time_ms"] += metrics["execution_time_ms"]

            # Add test result
            session["tests_executed"].append({
                "timestamp": metrics["timestamp"],
                "pass_rate": metrics["pass_rate"],
                "total_tests": metrics["total_tests"],
                "anomalies": len(metrics["anomalies"])
            })

            # Write updated session
            with open(session_file, 'w') as f:
                json.dump(session, f, indent=2)

    except Exception as e:
        print(f"⚠️  Warning: Could not update session metrics: {e}", file=sys.stderr)


def save_metrics(metrics):
    """Save metrics to individual file"""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    metrics_file = METRICS_DIR / f"test_run_{timestamp}.json"

    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)

    # Append to metrics log
    with open(METRICS_DIR / "test_metrics.jsonl", 'a') as f:
        f.write(json.dumps(metrics) + "\n")


def print_summary(metrics):
    """Print observability summary"""
    print(f"\n{'='*70}")
    print("TEST OBSERVABILITY SUMMARY")
    print(f"{'='*70}")
    print(f"Tests: {metrics['total_tests']} | Passed: {metrics['passed']} | Failed: {metrics['failed']}")
    print(f"Pass Rate: {metrics['pass_rate']:.1f}%")

    if metrics["execution_time_ms"] > 0:
        print(f"Execution Time: {metrics['execution_time_ms']/1000:.2f}s")

    if metrics["anomalies"]:
        print(f"\n⚠️  ANOMALIES DETECTED ({len(metrics['anomalies'])}):")
        for anomaly in metrics["anomalies"]:
            severity_icon = "🔴" if anomaly["severity"] == "critical" else "🟡"
            print(f"  {severity_icon} {anomaly['message']}")

    if metrics["warnings"]:
        print(f"\n⚠️  WARNINGS ({len(metrics['warnings'])}):")
        for warning in metrics["warnings"]:
            print(f"  ⚠️  {warning['message']}")

    print(f"{'='*70}\n")


def main():
    """Main analysis function"""
    if len(sys.argv) < 3:
        print("Usage: analyze_test_results.py <output> <exit_code>", file=sys.stderr)
        sys.exit(0)  # Don't block on missing args

    output = sys.argv[1]
    exit_code = int(sys.argv[2]) if sys.argv[2].isdigit() else 1

    # Parse and analyze
    metrics = parse_test_output(output, exit_code)

    # Save metrics
    save_metrics(metrics)

    # Update session
    update_session_metrics(metrics)

    # Print summary
    print_summary(metrics)

    # Exit with 0 (don't block workflow)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"⚠️  Test analysis error: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block on errors
