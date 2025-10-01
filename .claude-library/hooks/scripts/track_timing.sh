#!/bin/bash
# Track agent execution timing
# Usage: track_timing.sh <start|end> <description>

action="$1"
description="$2"

# Create metrics directory if it doesn't exist
mkdir -p .claude-metrics

timing_log=".claude-metrics/timing.log"
timestamp=$(date +%s%3N)  # Milliseconds since epoch

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
