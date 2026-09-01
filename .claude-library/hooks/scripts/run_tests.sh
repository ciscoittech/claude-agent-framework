#!/bin/bash
# PostToolUse hook: run the tests relevant to an edited file and feed any
# failure back so it gets fixed immediately.
#
# Reads the hook payload as JSON on stdin (Claude Code's actual contract).
# A config passing "$file_path" hands this script nothing - that shell variable
# is never set by the harness. $1 is still accepted for direct testing.
#
# Exits 0 always. PostToolUse fires after the edit has already happened, so
# blocking the tool call is meaningless; a failing suite is reported with
# decision:block, which surfaces the output to Claude and lets the turn
# continue - the same contract check_structure.sh uses. Swallowing the failure
# instead (the old `|| true` + `2>/dev/null`) makes the hook look like it ran
# tests when nothing ever saw the result.

file_path="$1"
if [ -z "$file_path" ] && [ ! -t 0 ]; then
    file_path=$(jq -r '.tool_input.file_path // .tool_response.filePath // empty' 2>/dev/null)
fi

if [ -z "$file_path" ] || [ ! -f "$file_path" ]; then
    exit 0
fi

output=""
status=0
ran="none"

case "$file_path" in
  *.py)
    # `python3 -m pytest`, not `pytest`: pytest is frequently importable in the
    # active interpreter while no console script is on PATH.
    if python3 -c 'import pytest' 2>/dev/null \
       && { [ -f pytest.ini ] || [ -f pyproject.toml ] || [ -d tests ]; }; then
        output=$(python3 -m pytest --quiet --exitfirst 2>&1)
        status=$?
        ran="pytest"
    fi
    ;;

  *.js|*.jsx|*.ts|*.tsx)
    if [ -f package.json ] && grep -q '"jest"' package.json; then
        output=$(npx jest --findRelatedTests "$file_path" --bail 2>&1)
        status=$?
        ran="jest"
    fi
    ;;

  *.go)
    package_dir=$(dirname "$file_path")
    if [ -f go.mod ] || [ -f "${package_dir}/go.mod" ]; then
        output=$(go test "./${package_dir#./}" 2>&1)
        status=$?
        ran="go test"
    fi
    ;;

  *.rs)
    if [ -f Cargo.toml ]; then
        output=$(cargo test --quiet 2>&1)
        status=$?
        ran="cargo test"
    fi
    ;;
esac

if [ ! -z "$CLAUDE_HOOKS_LOG" ]; then
    echo "$(date -Iseconds) | run_tests | $file_path | $ran | exit=$status" >> "$CLAUDE_HOOKS_LOG"
fi

if [ "$ran" != "none" ] && [ "$status" -ne 0 ]; then
    jq -n --arg r "$output" --arg f "$file_path" \
      '{decision:"block", reason:("Tests FAILED after editing " + $f + ":\n\n" + $r)}'
fi

exit 0
