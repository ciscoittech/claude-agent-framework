#!/bin/bash
# Pre-Test Validation Hook
# Validates test environment and dependencies before test execution

set -e

TOOL="$1"
ARGUMENTS="$2"
METRICS_DIR=".claude-metrics/testing"
VALIDATION_LOG="${METRICS_DIR}/pre_test_validation.log"

mkdir -p "${METRICS_DIR}"

# Extract test file from arguments
TEST_FILE=$(echo "${ARGUMENTS}" | grep -oE 'test_[a-zA-Z0-9_]+\.py' || echo "unknown")

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Pre-test validation: ${TEST_FILE}" >> "${VALIDATION_LOG}"

# Validation checks
VALIDATION_PASSED=true

# 1. Check Python availability
if ! command -v python3 &> /dev/null; then
    echo "❌ FAIL: Python3 not available" >> "${VALIDATION_LOG}"
    VALIDATION_PASSED=false
fi

# 2. Check test file exists
if [[ "${TEST_FILE}" != "unknown" ]] && [[ ! -f "${TEST_FILE}" ]]; then
    echo "⚠️  WARN: Test file not found: ${TEST_FILE}" >> "${VALIDATION_LOG}"
fi

# 3. Check .claude-library structure
if [[ ! -d ".claude-library" ]]; then
    echo "❌ FAIL: .claude-library directory missing" >> "${VALIDATION_LOG}"
    VALIDATION_PASSED=false
fi

# 4. Check hooks directory
if [[ ! -d ".claude-library/hooks" ]]; then
    echo "⚠️  WARN: Hooks directory missing" >> "${VALIDATION_LOG}"
fi

# 5. Record baseline metrics
if [[ "${VALIDATION_PASSED}" == "true" ]]; then
    echo "✅ PASS: Environment validated for ${TEST_FILE}" >> "${VALIDATION_LOG}"

    # Record pre-test state
    cat >> "${METRICS_DIR}/pre_test_state.json" <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "test_file": "${TEST_FILE}",
  "memory_mb": $(ps -o rss= -p $$ | awk '{print int($1/1024)}'),
  "disk_usage_kb": $(du -sk . | cut -f1)
}
EOF

    exit 0
else
    echo "❌ Environment validation failed" >> "${VALIDATION_LOG}"
    # Don't block execution, just warn
    exit 0
fi
