#!/bin/bash
# PostToolUse hook: run the framework structure test after edits to .claude/ or
# .claude-library/, and feed any failure back so it gets fixed immediately.
#
# Reads the hook payload on stdin. Exits 0 (silent) unless the structure test
# fails, in which case it emits decision:block with the failure output — for
# PostToolUse that surfaces the reason to Claude and the turn continues.
#
# No absolute paths: the repo root is found by walking up from the edited file
# to the directory containing test_v2_structure.py, so this stays portable.

payload=$(cat)
file=$(printf '%s' "$payload" | jq -r '.tool_input.file_path // .tool_response.filePath // empty')
[ -n "$file" ] || exit 0

# Only framework config changes matter here
case "$file" in
  */.claude/*|*/.claude-library/*) ;;
  *) exit 0 ;;
esac

# Walk up to the repo root
dir=$(dirname "$file")
while [ "$dir" != "/" ] && [ ! -f "$dir/test_v2_structure.py" ]; do
  dir=$(dirname "$dir")
done
[ -f "$dir/test_v2_structure.py" ] || exit 0

if ! output=$(cd "$dir" && python3 test_v2_structure.py 2>&1); then
  jq -n --arg r "$output" \
    '{decision:"block", reason:("Framework structure check FAILED after this edit:\n\n" + $r)}'
fi
exit 0
