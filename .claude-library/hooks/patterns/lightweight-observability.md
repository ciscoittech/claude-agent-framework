# Lightweight Observability Pattern (Hooks-Based)

**Pattern Type:** Hooks Integration
**Complexity:** Low
**Use Case:** Simple metrics without external services

## Overview

Get basic observability using only hooks and local file logging - no Logfire, no external services, no API keys. Perfect for simple projects or when you want metrics but not full observability.

## When to Use This Pattern

✅ **Use hooks-based observability when:**
- You want basic metrics without external dependencies
- You're learning the framework (keep it simple)
- Project is small (1-5 agents)
- You need offline capability
- You want to avoid external API costs
- You prefer file-based logging

❌ **Use full Observability pattern when:**
- Complex workflows (5+ agents)
- Need visual trace analysis
- Want real-time dashboards
- Need advanced analytics
- Production monitoring required

## Architecture

```
┌─────────────────────────────────────────┐
│     HOOKS CAPTURE EVENTS                │
│  PreToolUse, PostToolUse, Stop, etc.    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     LOG TO LOCAL FILES                  │
│  .claude-metrics/*.log                  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     ANALYZE WITH SCRIPTS                │
│  Python/Bash analysis tools             │
└─────────────────────────────────────────┘
```

## Implementation

### Step 1: Enable Performance Hooks

```json
{
  "settings": {
    "hooks": {
      "enabled": true,
      "configs": [
        ".claude-library/hooks/configs/performance.json"
      ]
    }
  }
}
```

### Step 2: Metrics Collection

**Timing Metrics:**
```bash
# .claude-library/hooks/scripts/track_timing.sh
timestamp=$(date +%s%3N)
echo "${timestamp} | START | ${description}" >> .claude-metrics/timing.log
```

**Tool Usage Metrics:**
```bash
# Track which tools agents use
echo "$(date) | ${tool_name} | ${agent_name}" >> .claude-metrics/tool_usage.log
```

**File Operations:**
```bash
# Track file creations/edits
echo "$(date) | ${operation} | ${file_path}" >> .claude-metrics/file_ops.log
```

## Metrics Directory Structure

```
.claude-metrics/
├── timing.log           # Agent execution times
├── tool_usage.log       # Tools used by agents
├── file_ops.log         # File operations
├── hooks.log            # Hook execution results
├── bash_commands.log    # All bash commands (audit)
└── validation.log       # Validation results
```

## Log Format Standards

### Timing Log

```
timestamp_ms | event_type | description | duration_ms
1706558400123 | START | architect-design | -
1706558430456 | END | architect-design | 30333
1706558430456 | DURATION | architect-design | 30333ms
```

### Tool Usage Log

```
timestamp | tool_name | agent_name | file_path
2025-01-30T14:30:22 | Write | architect | schema.md
2025-01-30T14:30:25 | Read | engineer | src/main.py
2025-01-30T14:30:28 | Bash | engineer | npm test
```

### File Operations Log

```
timestamp | operation | file_path | agent_name
2025-01-30T14:30:22 | CREATE | schema.md | architect
2025-01-30T14:30:25 | EDIT | src/main.py | engineer
2025-01-30T14:30:28 | DELETE | temp.txt | engineer
```

## Analysis Scripts

### Timing Analysis

```python
#!/usr/bin/env python3
"""Analyze agent execution timing"""

from pathlib import Path
from collections import defaultdict
from datetime import datetime

def parse_timing_log():
    """Parse timing.log and calculate statistics"""

    log_file = Path(".claude-metrics/timing.log")
    if not log_file.exists():
        return {}

    timings = defaultdict(list)

    with open(log_file, 'r') as f:
        for line in f:
            parts = line.strip().split(' | ')
            if len(parts) == 4 and parts[1] == 'DURATION':
                agent_name = parts[2]
                duration_ms = int(parts[3].replace('ms', ''))
                timings[agent_name].append(duration_ms)

    return dict(timings)

def generate_timing_report():
    """Generate timing statistics report"""

    timings = parse_timing_log()

    print("\n⏱️  Agent Execution Timing Report\n")
    print(f"{'Agent':<25} {'Count':>6} {'Min':>8} {'Max':>8} {'Avg':>8}")
    print("-" * 65)

    for agent, durations in sorted(timings.items()):
        count = len(durations)
        min_time = min(durations) / 1000  # Convert to seconds
        max_time = max(durations) / 1000
        avg_time = sum(durations) / count / 1000

        print(f"{agent:<25} {count:>6} {min_time:>7.1f}s {max_time:>7.1f}s {avg_time:>7.1f}s")

if __name__ == "__main__":
    generate_timing_report()
```

### Tool Usage Analysis

```python
#!/usr/bin/env python3
"""Analyze tool usage patterns"""

from pathlib import Path
from collections import defaultdict

def parse_tool_usage():
    """Parse tool usage log"""

    log_file = Path(".claude-metrics/tool_usage.log")
    if not log_file.exists():
        return {}

    usage = defaultdict(lambda: defaultdict(int))

    with open(log_file, 'r') as f:
        for line in f:
            parts = line.strip().split(' | ')
            if len(parts) >= 3:
                timestamp, tool, agent = parts[:3]
                usage[agent][tool] += 1

    return dict(usage)

def generate_tool_usage_report():
    """Generate tool usage report"""

    usage = parse_tool_usage()

    print("\n🔧 Tool Usage Report\n")

    for agent, tools in sorted(usage.items()):
        print(f"\n{agent}:")
        for tool, count in sorted(tools.items(), key=lambda x: x[1], reverse=True):
            print(f"  {tool:<20} {count:>4} times")

if __name__ == "__main__":
    generate_tool_usage_report()
```

### Workflow Summary

```python
#!/usr/bin/env python3
"""Generate complete workflow summary"""

import sys
from pathlib import Path
from datetime import datetime

def generate_summary():
    """Generate comprehensive workflow summary"""

    metrics_dir = Path(".claude-metrics")
    if not metrics_dir.exists():
        print("No metrics found")
        return

    print("\n" + "="*60)
    print("   CLAUDE AGENT FRAMEWORK - WORKFLOW SUMMARY")
    print("="*60)

    # Timing summary
    print("\n📊 PERFORMANCE METRICS")
    print("-" * 60)
    import subprocess
    subprocess.run([sys.executable, ".claude-library/hooks/scripts/timing_analysis.py"])

    # Tool usage summary
    print("\n\n🔧 TOOL USAGE")
    print("-" * 60)
    subprocess.run([sys.executable, ".claude-library/hooks/scripts/tool_usage_analysis.py"])

    # File operations
    print("\n\n📁 FILE OPERATIONS")
    print("-" * 60)
    file_ops = Path(".claude-metrics/file_ops.log")
    if file_ops.exists():
        creates = sum(1 for line in file_ops.open() if 'CREATE' in line)
        edits = sum(1 for line in file_ops.open() if 'EDIT' in line)
        print(f"  Files created: {creates}")
        print(f"  Files edited:  {edits}")

    # Hook executions
    print("\n\n🪝 HOOK EXECUTIONS")
    print("-" * 60)
    hooks_log = Path(".claude-metrics/hooks.log")
    if hooks_log.exists():
        total = sum(1 for _ in hooks_log.open())
        successes = sum(1 for line in hooks_log.open() if 'success' in line.lower())
        print(f"  Total hooks:   {total}")
        print(f"  Successful:    {successes}")
        print(f"  Failed:        {total - successes}")

    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    generate_summary()
```

## Real-Time Monitoring

### Tail Logs During Execution

```bash
# Terminal 1: Run workflow
claude> /build "new feature"

# Terminal 2: Watch timing
tail -f .claude-metrics/timing.log

# Terminal 3: Watch hooks
tail -f .claude-metrics/hooks.log
```

### Watch Script

```bash
#!/bin/bash
# watch_workflow.sh - Monitor workflow in real-time

echo "🔍 Monitoring Claude Agent Framework..."
echo ""

# Use 'watch' command if available, otherwise loop
if command -v watch &> /dev/null; then
    watch -n 1 'tail -10 .claude-metrics/timing.log'
else
    while true; do
        clear
        echo "🔍 Last 10 timing events:"
        tail -10 .claude-metrics/timing.log 2>/dev/null || echo "No timing data yet"
        sleep 1
    done
fi
```

## Dashboard Generation

### HTML Dashboard

```python
#!/usr/bin/env python3
"""Generate HTML dashboard from logs"""

from pathlib import Path
from datetime import datetime

def generate_html_dashboard():
    """Create simple HTML dashboard"""

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agent Metrics Dashboard</title>
        <style>
            body { font-family: monospace; padding: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
            .metric { font-size: 24px; font-weight: bold; color: #4CAF50; }
        </style>
    </head>
    <body>
        <h1>🤖 Claude Agent Framework - Metrics Dashboard</h1>
        <p>Generated: {timestamp}</p>

        <h2>⏱️ Performance Metrics</h2>
        {timing_table}

        <h2>🔧 Tool Usage</h2>
        {tool_usage_table}

        <h2>📁 File Operations</h2>
        <p class="metric">{file_ops}</p>

    </body>
    </html>
    """

    # Parse data and generate tables
    # (Implementation details omitted for brevity)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dashboard_path = Path(".claude-metrics/dashboard.html")
    dashboard_path.write_text(html.format(
        timestamp=timestamp,
        timing_table="<p>Timing data here</p>",
        tool_usage_table="<p>Tool usage here</p>",
        file_ops="42 files created, 18 edited"
    ))

    print(f"✅ Dashboard generated: {dashboard_path}")
    print(f"   Open in browser: file://{dashboard_path.absolute()}")

if __name__ == "__main__":
    generate_html_dashboard()
```

## Comparison: Hooks vs Full Observability

| Feature | Hooks-Based | Full Observability |
|---------|-------------|-------------------|
| **External Service** | ❌ No | ✅ Logfire |
| **API Key Required** | ❌ No | ✅ Yes |
| **Setup Time** | 2 min | 5 min |
| **Overhead** | ~50ms | ~500ms |
| **Visual Traces** | ❌ No | ✅ Yes |
| **Real-time Dashboard** | ❌ No | ✅ Yes |
| **File-based Logs** | ✅ Yes | ⚠️  Also available |
| **Offline Capable** | ✅ Yes | ❌ No |
| **Cost** | Free | Free tier available |
| **Query Capabilities** | Basic (grep/awk) | Advanced (SQL-like) |
| **Retention** | Unlimited (local) | Plan-dependent |

## Graduation Path

### Start Simple

```json
{
  "hooks": {
    "enabled": true,
    "configs": ["performance.json"]
  }
}
```

### Add More Metrics

```json
{
  "hooks": {
    "configs": [
      "performance.json",
      "code-quality.json"
    ]
  }
}
```

### Graduate to Full Observability

When you need more:

```json
{
  "hooks": {
    "enabled": true,
    "configs": ["performance.json"]
  },
  "observability": {
    "enabled": true,
    "provider": "logfire"
  }
}
```

Both work together - hooks for local logs, observability for advanced analysis.

## Best Practices

### 1. Rotate Logs Periodically

```bash
# rotate_logs.sh
mkdir -p .claude-metrics/archive
mv .claude-metrics/*.log .claude-metrics/archive/$(date +%Y%m%d-%H%M%S)/
```

### 2. Compress Old Logs

```bash
# Archive logs older than 7 days
find .claude-metrics/archive -type f -mtime +7 -exec gzip {} \;
```

### 3. Add to .gitignore

```gitignore
.claude-metrics/
```

### 4. Generate Reports After Each Workflow

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [{
          "command": "python .claude-library/hooks/scripts/generate_summary.py"
        }]
      }
    ]
  }
}
```

## Summary

Lightweight observability via hooks provides:
- ✅ Basic metrics without external services
- ✅ File-based logging for audit trails
- ✅ Simple analysis scripts
- ✅ Zero external dependencies
- ✅ Works offline
- ✅ Free forever

Perfect for learning the framework, small projects, or when you want simplicity over sophistication.

Upgrade to full Observability pattern when you need visual traces, real-time dashboards, or advanced analytics.
