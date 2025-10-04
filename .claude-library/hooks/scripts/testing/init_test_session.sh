#!/bin/bash
# Initialize Test Session Observability
# Creates baseline tracking for test execution session

set -e

METRICS_DIR=".claude-metrics/testing"
SESSION_FILE="${METRICS_DIR}/session_$(date +%Y%m%d_%H%M%S).json"

# Create metrics directory
mkdir -p "${METRICS_DIR}"

# Initialize session tracking
cat > "${SESSION_FILE}" <<EOF
{
  "session_id": "$(uuidgen 2>/dev/null || echo "session_$(date +%s)")",
  "start_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "framework_version": "1.1",
  "environment": {
    "os": "$(uname -s)",
    "python_version": "$(python3 --version 2>&1 | cut -d' ' -f2)",
    "git_branch": "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')",
    "git_commit": "$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
  },
  "tests_executed": [],
  "metrics": {
    "total_tests": 0,
    "passed": 0,
    "failed": 0,
    "errors": 0,
    "execution_time_ms": 0
  },
  "coverage": {
    "files_modified": [],
    "lines_added": 0,
    "lines_removed": 0
  }
}
EOF

# Store session file path for other hooks
echo "${SESSION_FILE}" > "${METRICS_DIR}/current_session"

echo "✅ Test session initialized: ${SESSION_FILE}"
exit 0
