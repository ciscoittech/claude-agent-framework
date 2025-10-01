# Agent Output Validation Pattern

**Pattern Type:** Hooks Integration
**Complexity:** Medium
**Use Case:** Verify agents actually completed claimed work

## Overview

Agents sometimes claim to have created files or made changes, but validation ensures reality matches claims. This pattern uses hooks to automatically verify agent outputs.

## Problem: The Claim vs Reality Gap

### Common Issues

**Agent claims:**
- "I created `src/utils/helper.py` with the new function"
- "I updated `package.json` with the dependency"
- "I ran tests and they all passed"

**Reality check needed:**
- Does the file actually exist?
- Was the change actually made?
- Did tests really pass?

## Pattern: Post-Agent Validation

### Implementation

**Hook Configuration:**
```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude-library/hooks/scripts/validate_agent_output.py"
          }
        ]
      }
    ]
  }
}
```

**Workflow:**
```
Agent completes → SubagentStop hook → Validate output → Report discrepancies
```

### Validation Script

```python
#!/usr/bin/env python3
"""Validate agent claimed outputs match reality"""

import sys
import json
from pathlib import Path
from datetime import datetime

def validate_files_exist(expected_files):
    """Check if files agents claimed to create exist"""
    missing = []
    for file_path in expected_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    return missing

def validate_file_contents(file_checks):
    """Verify file contents match expectations"""
    failures = []
    for file_path, expected_content in file_checks.items():
        if not Path(file_path).exists():
            failures.append(f"{file_path}: File not found")
            continue

        with open(file_path, 'r') as f:
            content = f.read()
            if expected_content not in content:
                failures.append(f"{file_path}: Expected content not found")

    return failures

def validate_tests_passed(test_results):
    """Check if test output indicates success"""
    # Parse test output for failures
    # Implementation depends on test framework
    pass

def main():
    """Main validation routine"""

    # Read agent output context (if available)
    context_file = "/tmp/agent-output-context.json"

    if Path(context_file).exists():
        with open(context_file, 'r') as f:
            context = json.load(f)

        agent_name = context.get('agent_name', 'unknown')
        claimed_files = context.get('files_created', [])
        claimed_changes = context.get('files_modified', {})

        # Validate claimed file creations
        missing_files = validate_files_exist(claimed_files)
        if missing_files:
            log_validation_failure(agent_name, "files_not_created", missing_files)

        # Validate claimed file modifications
        content_failures = validate_file_contents(claimed_changes)
        if content_failures:
            log_validation_failure(agent_name, "content_mismatch", content_failures)

        # Log success
        if not missing_files and not content_failures:
            log_validation_success(agent_name)

    sys.exit(0)

def log_validation_failure(agent_name, failure_type, details):
    """Log validation failure"""
    log_file = ".claude-metrics/validation_failures.log"
    timestamp = datetime.now().isoformat()

    with open(log_file, 'a') as f:
        f.write(f"{timestamp} | {agent_name} | {failure_type} | {details}\n")

    print(f"⚠️  Agent validation failed: {failure_type}", file=sys.stderr)
    for detail in details:
        print(f"   - {detail}", file=sys.stderr)

def log_validation_success(agent_name):
    """Log successful validation"""
    log_file = ".claude-metrics/validation_success.log"
    timestamp = datetime.now().isoformat()

    with open(log_file, 'a') as f:
        f.write(f"{timestamp} | {agent_name} | validated\n")

if __name__ == "__main__":
    main()
```

## Pattern: File Existence Validation

### Simple Implementation

```bash
#!/bin/bash
# validate_files.sh - Check agent claimed files exist

# Read claimed files from agent output (passed as args)
claimed_files=("$@")

missing=()
for file in "${claimed_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing+=("$file")
    fi
done

if [ ${#missing[@]} -gt 0 ]; then
    echo "⚠️  Agent claimed to create files that don't exist:"
    for file in "${missing[@]}"; do
        echo "   - $file"
    done
    echo "$(date) | validation_failed | missing_files: ${missing[*]}" >> .claude-metrics/validation.log
else
    echo "✅ All claimed files exist"
    echo "$(date) | validation_passed" >> .claude-metrics/validation.log
fi

exit 0  # Never block workflow
```

## Pattern: Test Output Validation

### Verify Tests Actually Passed

```python
#!/usr/bin/env python3
"""Verify test execution results"""

import subprocess
import sys
from pathlib import Path

def run_tests_and_validate():
    """Run tests and verify they pass"""

    # Determine test command based on project
    if Path("pytest.ini").exists():
        result = subprocess.run(
            ["pytest", "--quiet", "--tb=no"],
            capture_output=True,
            text=True
        )
    elif Path("package.json").exists():
        result = subprocess.run(
            ["npm", "test", "--", "--passWithNoTests"],
            capture_output=True,
            text=True
        )
    else:
        return True  # No tests configured

    # Check result
    if result.returncode != 0:
        log_failure("tests_failed", result.stderr)
        return False

    log_success("tests_passed")
    return True

def log_failure(reason, details):
    """Log test validation failure"""
    with open(".claude-metrics/test_validation.log", 'a') as f:
        from datetime import datetime
        f.write(f"{datetime.now()} | FAILED | {reason} | {details}\n")

def log_success(status):
    """Log test validation success"""
    with open(".claude-metrics/test_validation.log", 'a') as f:
        from datetime import datetime
        f.write(f"{datetime.now()} | SUCCESS | {status}\n")

if __name__ == "__main__":
    success = run_tests_and_validate()
    sys.exit(0 if success else 1)
```

## Pattern: Build Validation

### Verify Code Actually Compiles/Builds

```bash
#!/bin/bash
# validate_build.sh - Ensure code builds successfully

# Determine build command
if [ -f "Cargo.toml" ]; then
    build_cmd="cargo build"
elif [ -f "package.json" ]; then
    build_cmd="npm run build"
elif [ -f "go.mod" ]; then
    build_cmd="go build ./..."
elif [ -f "pom.xml" ]; then
    build_cmd="mvn compile"
else
    exit 0  # No build configured
fi

# Run build
if $build_cmd > /tmp/build_output.log 2>&1; then
    echo "✅ Build successful"
    echo "$(date) | build_validation | passed" >> .claude-metrics/validation.log
else
    echo "⚠️  Build failed after agent changes"
    cat /tmp/build_output.log
    echo "$(date) | build_validation | failed" >> .claude-metrics/validation.log
fi

exit 0  # Never block
```

## Integration with Observability

### Combined Pattern: Hooks + Observability

When both are enabled, hooks validate and observability tracks:

```python
#!/usr/bin/env python3
"""Validation with observability tracking"""

import sys
from pathlib import Path
import json

# Check if observability is enabled
registry = json.loads(Path('.claude-library/REGISTRY.json').read_text())
obs_enabled = registry.get('settings', {}).get('observability', {}).get('enabled', False)

def validate_with_tracking(agent_name, claimed_outputs):
    """Validate and optionally track to Logfire"""

    validation_results = {
        'agent': agent_name,
        'claimed': claimed_outputs,
        'validated': [],
        'missing': [],
        'failed': []
    }

    # Perform validation
    for file_path in claimed_outputs:
        if Path(file_path).exists():
            validation_results['validated'].append(file_path)
        else:
            validation_results['missing'].append(file_path)

    # Track to observability if enabled
    if obs_enabled:
        try:
            from observability.logfire_helper import log_validation_result
            log_validation_result(agent_name, validation_results)
        except ImportError:
            pass  # Observability not available

    # Log locally
    log_file = ".claude-metrics/validation.log"
    with open(log_file, 'a') as f:
        import json
        from datetime import datetime
        f.write(f"{datetime.now()} | {json.dumps(validation_results)}\n")

    # Report to user
    if validation_results['missing']:
        print(f"⚠️  Agent {agent_name} validation issues:")
        for missing in validation_results['missing']:
            print(f"   - Missing: {missing}")

    return len(validation_results['missing']) == 0

if __name__ == "__main__":
    # Example usage
    validate_with_tracking('architect', ['schema.md', 'api_spec.md'])
```

## Best Practices

### 1. Validate Immediately After Agent Completes

```json
{
  "hooks": {
    "SubagentStop": [/* validation here */]
  }
}
```

### 2. Log All Validation Results

Even successes should be logged for audit trail.

### 3. Never Block Workflow on Validation Failure

Report the issue but let workflow continue - human can decide.

### 4. Use Validation to Improve Agent Prompts

Review validation logs to identify agents that frequently claim work not done.

### 5. Combine Multiple Validation Types

```bash
# validate_all.sh
validate_files.sh && \
validate_tests.sh && \
validate_build.sh
```

## Validation Dashboard

### Generate Validation Report

```python
#!/usr/bin/env python3
"""Generate validation report from logs"""

from pathlib import Path
from collections import defaultdict
import json

def parse_validation_logs():
    """Parse validation logs into summary"""

    log_file = Path(".claude-metrics/validation.log")
    if not log_file.exists():
        return {}

    summary = defaultdict(lambda: {'passed': 0, 'failed': 0})

    with open(log_file, 'r') as f:
        for line in f:
            try:
                parts = line.strip().split(' | ')
                if len(parts) >= 3:
                    timestamp, agent, status = parts[:3]
                    if 'passed' in status.lower():
                        summary[agent]['passed'] += 1
                    else:
                        summary[agent]['failed'] += 1
            except:
                continue

    return dict(summary)

def generate_report():
    """Generate human-readable validation report"""

    summary = parse_validation_logs()

    print("\n📊 Agent Validation Report\n")
    print("Agent                    | Passed | Failed | Success Rate")
    print("-" * 60)

    for agent, stats in summary.items():
        total = stats['passed'] + stats['failed']
        rate = (stats['passed'] / total * 100) if total > 0 else 0
        print(f"{agent:24} | {stats['passed']:6} | {stats['failed']:6} | {rate:5.1f}%")

if __name__ == "__main__":
    generate_report()
```

### Run Validation Report

```bash
# Add to Stop hook
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [{
          "command": "python .claude-library/hooks/scripts/validation_report.py"
        }]
      }
    ]
  }
}
```

## Summary

Agent validation hooks provide:
- ✅ Verify claimed outputs exist
- ✅ Catch discrepancies early
- ✅ Improve agent reliability
- ✅ Audit trail of agent work
- ✅ Identify problematic agents
- ✅ Works with or without observability

Start with simple file existence checks, add content validation, then layer in test/build verification as needed.
