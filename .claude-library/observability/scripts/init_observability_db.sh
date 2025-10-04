#!/bin/bash
# Initialize Local Observability Database
# Creates project-local SQLite database and applies schema
# Runs once per session on SessionStart

set -e

METRICS_DIR=".claude-metrics"
DB_FILE="${METRICS_DIR}/observability.db"
SCHEMA_FILE=".claude-library/observability/schema.sql"

# Create metrics directory
mkdir -p "${METRICS_DIR}"

# Check if database exists
if [[ ! -f "${DB_FILE}" ]]; then
    echo "✅ Initializing observability database: ${DB_FILE}"

    # Create database and apply schema
    if [[ -f "${SCHEMA_FILE}" ]]; then
        sqlite3 "${DB_FILE}" < "${SCHEMA_FILE}"
        echo "   Schema applied successfully"
    else
        echo "   ⚠️  Warning: Schema file not found: ${SCHEMA_FILE}"
        echo "   Creating empty database"
        sqlite3 "${DB_FILE}" "SELECT 1"
    fi
else
    # Database exists, check if schema needs updating
    CURRENT_VERSION=$(sqlite3 "${DB_FILE}" "SELECT COALESCE(MAX(version), 0) FROM schema_version" 2>/dev/null || echo "0")
    echo "   Observability database ready (schema v${CURRENT_VERSION})"
fi

# Initialize session
python3 << 'PYTHON_SCRIPT'
import sys
sys.path.insert(0, '.claude-library/observability')
try:
    from db_helper import get_session_id, init_database
    # Ensure database is initialized
    init_database()
    # Get or create session ID
    session_id = get_session_id()
    print(f"   Session ID: {session_id[:8]}...")
except Exception as e:
    print(f"   ⚠️  Error initializing session: {e}", file=sys.stderr)
    sys.exit(0)  # Don't block on error
PYTHON_SCRIPT

exit 0
