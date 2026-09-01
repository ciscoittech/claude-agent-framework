#!/bin/bash
# PostToolUse hook: run the framework checks after a change to anything the
# checks cover, and feed any failure back so it gets fixed immediately.
#
# Reads the hook payload on stdin. Exits 0 (silent) unless a suite fails, in
# which case it emits decision:block with the failure output - on PostToolUse
# that is the documented shape, and it surfaces the reason to Claude.
#
# No absolute paths: the repo root is found by walking up from the edited file
# to the directory containing run_checks.py, so this stays portable.

payload=$(cat)
file=$(printf '%s' "$payload" | jq -r '.tool_input.file_path // .tool_response.filePath // empty')
[ -n "$file" ] || exit 0

# Walk up to the repo root
dir=$(dirname "$file")
while [ "$dir" != "/" ] && [ ! -f "$dir/run_checks.py" ]; do
  dir=$(dirname "$dir")
done
[ -f "$dir/run_checks.py" ] || exit 0

# Which edits the checks can actually have an opinion about: framework config,
# and the root documents whose examples the suites hold to the contract. An edit
# to a project's own source is none of this hook's business.
rel=${file#"$dir"/}
case "$rel" in
  .claude/*|.claude-library/*) ;;
  *[!/]*/*) exit 0 ;;                 # nested elsewhere - not ours
  *.md|*.py) ;;                       # a root document or script
  *) exit 0 ;;
esac

if ! output=$(cd "$dir" && python3 run_checks.py 2>&1); then
  jq -n --arg r "$output" \
    '{decision:"block", reason:("Framework checks FAILED after this edit:\n\n" + $r)}'
fi
exit 0
