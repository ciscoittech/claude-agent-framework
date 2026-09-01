#!/bin/bash
# Track agent execution timing
# Usage: track_timing.sh <start|end>
#
# The action is a literal in the hook config; the description is read from the
# hook payload on stdin (Claude Code's actual contract). A config passing
# "$description" would hand this script nothing - that variable is never set.

action="$1"
description="$2"
if [ -z "$description" ] && [ ! -t 0 ]; then
    description=$(jq -r '.tool_input.description // .tool_input.subagent_type // empty' 2>/dev/null)
fi
[ -n "$description" ] || description="(unknown)"

# Create metrics directory if it doesn't exist
mkdir -p .claude-metrics

timing_log=".claude-metrics/timing.log"
# date +%s%3N is GNU-only; BSD/macOS date emits a literal "N". Use python3,
# which the framework already depends on, for a portable millisecond stamp.
timestamp=$(python3 -c 'import time;print(int(time.time()*1000))')

case "$action" in
  start)
    echo "${timestamp} | START | ${description}" >> "$timing_log"
    ;;
  end)
    echo "${timestamp} | END | ${description}" >> "$timing_log"

    # Calculate duration if we have a matching start entry
    start_time=$(grep "START | ${description}" "$timing_log" | tail -1 | cut -d' ' -f1)
    if [ ! -z "$start_time" ]; then
      duration=$((timestamp - start_time))
      echo "${timestamp} | DURATION | ${description} | ${duration}ms" >> "$timing_log"

      # Log to hooks log if enabled
      if [ ! -z "$CLAUDE_HOOKS_LOG" ]; then
        echo "$(date -Iseconds) | track_timing | ${description} | ${duration}ms" >> "$CLAUDE_HOOKS_LOG"
      fi
    fi
    ;;
esac

exit 0
