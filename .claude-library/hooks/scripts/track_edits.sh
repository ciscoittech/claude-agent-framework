#!/bin/bash
# Track file edits for build checking
# Usage: track_edits.sh <file_path> <tool_name>

FILE_PATH="$1"
TOOL_NAME="$2"
EDIT_LOG="/tmp/claude-edits.json"

# Initialize edit log if doesn't exist
if [ ! -f "$EDIT_LOG" ]; then
  echo "[]" > "$EDIT_LOG"
fi

# Determine repo root for this file
REPO_ROOT=$(cd "$(dirname "$FILE_PATH")" && git rev-parse --show-toplevel 2>/dev/null || pwd)

# Determine repo name (last directory of repo root)
REPO_NAME=$(basename "$REPO_ROOT")

# Get timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create edit entry
EDIT_ENTRY=$(cat <<EOF
{
  "file_path": "$FILE_PATH",
  "repo_root": "$REPO_ROOT",
  "repo_name": "$REPO_NAME",
  "tool": "$TOOL_NAME",
  "timestamp": "$TIMESTAMP"
}
EOF
)

# Append to log (using temp file to avoid race conditions)
TEMP_LOG=$(mktemp)
jq ". += [$EDIT_ENTRY]" "$EDIT_LOG" > "$TEMP_LOG" 2>/dev/null && mv "$TEMP_LOG" "$EDIT_LOG" || {
  # Fallback if jq not available - simple append
  echo "$EDIT_ENTRY" >> "$EDIT_LOG"
}

# Keep log size manageable (last 100 edits)
if command -v jq &> /dev/null; then
  TEMP_LOG=$(mktemp)
  jq '.[.-100:]' "$EDIT_LOG" > "$TEMP_LOG" 2>/dev/null && mv "$TEMP_LOG" "$EDIT_LOG"
fi

exit 0
