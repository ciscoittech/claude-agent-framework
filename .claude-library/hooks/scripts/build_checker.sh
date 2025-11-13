#!/bin/bash
# Build Checker - Runs builds on all modified repos
# Catches TypeScript errors, test failures, etc.

EDIT_LOG="/tmp/claude-edits.json"
ERROR_THRESHOLD=5

# Check if edit log exists
if [ ! -f "$EDIT_LOG" ]; then
  exit 0
fi

# Check if any edits were made
EDIT_COUNT=$(jq 'length' "$EDIT_LOG" 2>/dev/null || echo "0")
if [ "$EDIT_COUNT" -eq 0 ]; then
  exit 0
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 BUILD CHECKER"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get unique repos that were modified
AFFECTED_REPOS=$(python3 .claude-library/hooks/scripts/parse_affected_repos.py "$EDIT_LOG" 2>/dev/null || echo "")

if [ -z "$AFFECTED_REPOS" ]; then
  echo "✅ No repos to check"
  rm -f "$EDIT_LOG"
  exit 0
fi

echo "Modified repos: $AFFECTED_REPOS"
echo ""

# Build each affected repo
for REPO_INFO in $AFFECTED_REPOS; do
  # Parse repo_name:repo_path format
  REPO_NAME=$(echo "$REPO_INFO" | cut -d: -f1)
  REPO_PATH=$(echo "$REPO_INFO" | cut -d: -f2-)

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "📦 Building: $REPO_NAME"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Detect build command based on project type
  BUILD_CMD=""

  if [ -f "$REPO_PATH/package.json" ]; then
    # Check for build script
    if grep -q '"build"' "$REPO_PATH/package.json"; then
      BUILD_CMD="cd '$REPO_PATH' && npm run build"
    elif grep -q '"typecheck"' "$REPO_PATH/package.json"; then
      BUILD_CMD="cd '$REPO_PATH' && npm run typecheck"
    elif [ -f "$REPO_PATH/tsconfig.json" ]; then
      BUILD_CMD="cd '$REPO_PATH' && npx tsc --noEmit"
    else
      echo "⚠️  No build command found for $REPO_NAME (skipping)"
      continue
    fi
  elif [ -f "$REPO_PATH/pyproject.toml" ] || [ -f "$REPO_PATH/setup.py" ]; then
    BUILD_CMD="cd '$REPO_PATH' && python -m pytest --collect-only"
  elif [ -f "$REPO_PATH/go.mod" ]; then
    BUILD_CMD="cd '$REPO_PATH' && go build ./..."
  elif [ -f "$REPO_PATH/Cargo.toml" ]; then
    BUILD_CMD="cd '$REPO_PATH' && cargo check"
  else
    echo "⚠️  Unknown project type for $REPO_NAME (skipping)"
    continue
  fi

  # Run build command
  LOG_FILE="/tmp/build-$REPO_NAME.log"
  eval "$BUILD_CMD" > "$LOG_FILE" 2>&1
  BUILD_EXIT_CODE=$?

  # Analyze results
  ERROR_COUNT=$(grep -i "error" "$LOG_FILE" | wc -l)

  if [ $BUILD_EXIT_CODE -ne 0 ]; then
    if [ "$ERROR_COUNT" -ge "$ERROR_THRESHOLD" ]; then
      echo "❌ $ERROR_COUNT errors found in $REPO_NAME"
      echo ""
      echo "💡 Consider launching auto-error-resolver agent to fix these systematically."
      echo ""
      echo "First 20 errors:"
      grep -i "error" "$LOG_FILE" | head -20
    else
      echo "⚠️  $ERROR_COUNT error(s) in $REPO_NAME"
      echo ""
      cat "$LOG_FILE"
    fi
  else
    if [ "$ERROR_COUNT" -eq 0 ]; then
      echo "✅ $REPO_NAME builds successfully"
    else
      echo "⚠️  $REPO_NAME builds with $ERROR_COUNT warning(s)"
    fi
  fi

  echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Clear edit log
rm -f "$EDIT_LOG"

exit 0
