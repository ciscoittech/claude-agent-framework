#!/bin/bash
# Track Test File Changes Hook
# Records test file modifications for coverage analysis

set -e

FILE_PATH="$1"
TOOL="$2"
METRICS_DIR=".claude-metrics/testing"

mkdir -p "${METRICS_DIR}"

# Only track test files
if [[ ! "${FILE_PATH}" =~ test.*\.py$ ]]; then
    exit 0
fi

# Count lines added/removed if git is available
LINES_ADDED=0
LINES_REMOVED=0

if command -v git &> /dev/null && git rev-parse --git-dir &> /dev/null 2>&1; then
    # Get diff stats
    DIFF_STATS=$(git diff --numstat "${FILE_PATH}" 2>/dev/null || echo "0 0")
    LINES_ADDED=$(echo "${DIFF_STATS}" | awk '{print $1}')
    LINES_REMOVED=$(echo "${DIFF_STATS}" | awk '{print $2}')
fi

# Record change
cat >> "${METRICS_DIR}/test_changes.jsonl" <<EOF
{"timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)", "file": "${FILE_PATH}", "tool": "${TOOL}", "lines_added": ${LINES_ADDED:-0}, "lines_removed": ${LINES_REMOVED:-0}}
EOF

# Update session coverage if available
SESSION_FILE_PATH="${METRICS_DIR}/current_session"
if [[ -f "${SESSION_FILE_PATH}" ]]; then
    SESSION_FILE=$(cat "${SESSION_FILE_PATH}")
    if [[ -f "${SESSION_FILE}" ]]; then
        # Update coverage section using jq if available
        if command -v jq &> /dev/null; then
            TMP_FILE=$(mktemp)
            jq ".coverage.files_modified += [\"${FILE_PATH}\"] | .coverage.lines_added += ${LINES_ADDED:-0} | .coverage.lines_removed += ${LINES_REMOVED:-0}" "${SESSION_FILE}" > "${TMP_FILE}"
            mv "${TMP_FILE}" "${SESSION_FILE}"
        fi
    fi
fi

echo "✅ Tracked test change: ${FILE_PATH} (+${LINES_ADDED:-0}/-${LINES_REMOVED:-0})"
exit 0
