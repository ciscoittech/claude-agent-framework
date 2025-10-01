#!/bin/bash
# Run tests for changed files
# Usage: run_tests.sh <file_path>

file_path="$1"

if [ -z "$file_path" ]; then
    exit 0
fi

# Determine test command based on file type and project structure
case "$file_path" in
  *.py)
    # Python tests
    if [ -f "pytest.ini" ] || [ -d "tests" ]; then
        # Try to find corresponding test file
        test_file=$(echo "$file_path" | sed 's/\.py$//' | sed 's|^src/|tests/|' | sed 's|^|tests/test_|')_test.py

        if [ -f "$test_file" ]; then
            pytest "$test_file" --quiet 2>/dev/null || true
        else
            # Run all tests if specific test not found
            pytest --quiet --exitfirst 2>/dev/null || true
        fi
    fi
    ;;

  *.js|*.jsx|*.ts|*.tsx)
    # JavaScript/TypeScript tests
    if [ -f "package.json" ]; then
        # Check if jest is configured
        if grep -q "jest" package.json; then
            npm test -- --findRelatedTests "$file_path" --bail 2>/dev/null || true
        fi
    fi
    ;;

  *.go)
    # Go tests
    package_dir=$(dirname "$file_path")
    if [ -f "${package_dir}/go.mod" ]; then
        go test "$package_dir" 2>/dev/null || true
    fi
    ;;

  *.rs)
    # Rust tests
    if [ -f "Cargo.toml" ]; then
        cargo test --quiet 2>/dev/null || true
    fi
    ;;
esac

# Log test execution
if [ ! -z "$CLAUDE_HOOKS_LOG" ]; then
    echo "$(date -Iseconds) | run_tests | $file_path | completed" >> "$CLAUDE_HOOKS_LOG"
fi

exit 0  # Never block on test failures in hooks
