#!/usr/bin/env python3
"""
Generate Test Observability Report
Comprehensive test session report with metrics, trends, and recommendations
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

METRICS_DIR = Path(".claude-metrics/testing")


def load_session_data():
    """Load current session data"""
    session_file_path = METRICS_DIR / "current_session"

    if not session_file_path.exists():
        return None

    try:
        session_file = Path(session_file_path.read_text().strip())
        if session_file.exists():
            with open(session_file) as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️  Could not load session data: {e}", file=sys.stderr)

    return None


def load_historical_metrics():
    """Load historical test metrics"""
    metrics_file = METRICS_DIR / "test_metrics.jsonl"

    if not metrics_file.exists():
        return []

    metrics = []
    try:
        with open(metrics_file) as f:
            for line in f:
                if line.strip():
                    metrics.append(json.loads(line))
    except Exception as e:
        print(f"⚠️  Could not load historical metrics: {e}", file=sys.stderr)

    return metrics


def analyze_trends(historical_metrics):
    """Analyze trends from historical data"""
    if len(historical_metrics) < 2:
        return None

    # Recent metrics (last 10 runs)
    recent = historical_metrics[-10:]

    trends = {
        "avg_pass_rate": sum(m.get("pass_rate", 0) for m in recent) / len(recent),
        "avg_execution_time_ms": sum(m.get("execution_time_ms", 0) for m in recent) / len(recent),
        "total_anomalies": sum(len(m.get("anomalies", [])) for m in recent),
        "pass_rate_trend": "stable"
    }

    # Determine pass rate trend
    if len(recent) >= 5:
        first_half = recent[:len(recent)//2]
        second_half = recent[len(recent)//2:]

        avg_first = sum(m.get("pass_rate", 0) for m in first_half) / len(first_half)
        avg_second = sum(m.get("pass_rate", 0) for m in second_half) / len(second_half)

        if avg_second > avg_first + 5:
            trends["pass_rate_trend"] = "improving"
        elif avg_second < avg_first - 5:
            trends["pass_rate_trend"] = "degrading"

    return trends


def generate_recommendations(session, trends):
    """Generate recommendations based on analysis"""
    recommendations = []

    # Session-based recommendations
    if session:
        pass_rate = (session["metrics"]["passed"] / session["metrics"]["total_tests"] * 100) if session["metrics"]["total_tests"] > 0 else 0

        if pass_rate < 90:
            recommendations.append({
                "priority": "high",
                "category": "quality",
                "message": f"Pass rate {pass_rate:.1f}% below 90% - investigate failing tests"
            })

        if session["metrics"]["errors"] > 5:
            recommendations.append({
                "priority": "high",
                "category": "reliability",
                "message": f"{session['metrics']['errors']} anomalies detected - review test stability"
            })

    # Trend-based recommendations
    if trends:
        if trends["pass_rate_trend"] == "degrading":
            recommendations.append({
                "priority": "high",
                "category": "trend",
                "message": "Pass rate trending downward - code quality may be degrading"
            })

        if trends["avg_execution_time_ms"] > 120000:  # > 2 minutes
            recommendations.append({
                "priority": "medium",
                "category": "performance",
                "message": f"Average execution time {trends['avg_execution_time_ms']/1000:.1f}s - consider optimization"
            })

    # General recommendations
    if not recommendations:
        recommendations.append({
            "priority": "info",
            "category": "status",
            "message": "Test suite is healthy - maintain current practices"
        })

    return recommendations


def print_report(session, trends, recommendations):
    """Print comprehensive test observability report"""
    print(f"\n{'='*80}")
    print("COMPREHENSIVE TEST OBSERVABILITY REPORT")
    print(f"{'='*80}")

    # Session Summary
    if session:
        print(f"\n📊 SESSION SUMMARY")
        print(f"{'─'*80}")
        print(f"Session ID: {session['session_id']}")
        print(f"Start Time: {session['start_time']}")
        print(f"Framework Version: {session['framework_version']}")
        print(f"Git Branch: {session['environment']['git_branch']}")
        print(f"Git Commit: {session['environment']['git_commit']}")

        print(f"\n📈 TEST METRICS")
        print(f"{'─'*80}")
        metrics = session["metrics"]
        print(f"Total Tests Executed: {metrics['total_tests']}")
        print(f"Passed: {metrics['passed']} ✅")
        print(f"Failed: {metrics['failed']} ❌")
        print(f"Anomalies: {metrics['errors']} ⚠️")

        if metrics['total_tests'] > 0:
            pass_rate = (metrics['passed'] / metrics['total_tests']) * 100
            print(f"Pass Rate: {pass_rate:.1f}%")

        if metrics['execution_time_ms'] > 0:
            print(f"Total Execution Time: {metrics['execution_time_ms']/1000:.2f}s")

        # Coverage
        if session["coverage"]["files_modified"]:
            print(f"\n📝 CODE COVERAGE")
            print(f"{'─'*80}")
            print(f"Files Modified: {len(session['coverage']['files_modified'])}")
            print(f"Lines Added: {session['coverage']['lines_added']}")
            print(f"Lines Removed: {session['coverage']['lines_removed']}")

    # Trends
    if trends:
        print(f"\n📉 HISTORICAL TRENDS")
        print(f"{'─'*80}")
        print(f"Average Pass Rate: {trends['avg_pass_rate']:.1f}%")
        print(f"Average Execution Time: {trends['avg_execution_time_ms']/1000:.2f}s")
        print(f"Total Anomalies (last 10 runs): {trends['total_anomalies']}")
        print(f"Pass Rate Trend: {trends['pass_rate_trend'].upper()}")

    # Recommendations
    if recommendations:
        print(f"\n💡 RECOMMENDATIONS")
        print(f"{'─'*80}")

        priority_order = {"high": 1, "medium": 2, "low": 3, "info": 4}
        sorted_recs = sorted(recommendations, key=lambda r: priority_order.get(r["priority"], 5))

        for rec in sorted_recs:
            icon = {"high": "🔴", "medium": "🟡", "low": "🟢", "info": "ℹ️"}.get(rec["priority"], "•")
            print(f"{icon} [{rec['priority'].upper()}] {rec['message']}")

    print(f"\n{'='*80}")
    print(f"Report generated: {datetime.utcnow().isoformat()}Z")
    print(f"Metrics stored: {METRICS_DIR}")
    print(f"{'='*80}\n")


def save_report(session, trends, recommendations):
    """Save report to file"""
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_file = METRICS_DIR / f"report_{timestamp}.json"

    report = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "session": session,
        "trends": trends,
        "recommendations": recommendations
    }

    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"📄 Full report saved: {report_file}")


def main():
    """Generate comprehensive test report"""
    # Load data
    session = load_session_data()
    historical = load_historical_metrics()
    trends = analyze_trends(historical)

    # Generate recommendations
    recommendations = generate_recommendations(session, trends)

    # Print report
    print_report(session, trends, recommendations)

    # Save report
    if session or trends:
        save_report(session, trends, recommendations)

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"⚠️  Report generation error: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block on errors
