#!/usr/bin/env python3
"""
Security check hook - validates bash commands before execution
Blocks dangerous operations that could damage the system
"""

import sys
import re
import os
import json
from datetime import datetime


def read_command():
    """
    Claude Code delivers the hook payload as JSON on stdin - NOT as argv.
    A config passing "$command" hands this script an empty string, which used to
    mean every command was approved: a security hook that silently allowed
    everything. argv is kept as a fallback for direct testing.
    """
    if len(sys.argv) > 1 and sys.argv[1]:
        return sys.argv[1]
    if sys.stdin is None or sys.stdin.isatty():
        return ""
    raw = sys.stdin.read()
    if not raw.strip():
        return ""
    try:
        return json.loads(raw).get("tool_input", {}).get("command", "")
    except (json.JSONDecodeError, AttributeError):
        # Not JSON - treat the raw text as the command rather than failing open
        return raw.strip()


command = read_command()

# Dangerous command patterns to block
DANGEROUS_PATTERNS = [
    # Destructive filesystem operations
    (r'rm\s+-rf\s+/', "Attempting to delete from root directory"),
    (r'rm\s+-rf\s+\*', "Attempting to delete all files"),
    (r'rm\s+-rf\s+~', "Attempting to delete home directory"),
    (r':\s*\(\s*\)\s*\{.*:\s*\|\s*:', "Fork bomb detected"),

    # Disk operations
    (r'dd\s+if=.*of=/dev/sd', "Attempting to write to disk device"),
    (r'mkfs\.', "Attempting to format disk"),
    (r'>\s*/dev/sd', "Attempting to overwrite disk"),

    # Dangerous pipes
    (r'curl.*\|\s*bash', "Piping curl output to bash (security risk)"),
    (r'wget.*\|\s*sh', "Piping wget output to shell (security risk)"),

    # Git force operations on protected branches
    (r'git\s+push.*--force.*\s+(main|master)', "Force push to protected branch"),
    (r'git\s+push.*-f.*\s+(main|master)', "Force push to protected branch"),

    # Production database operations (customize for your setup)
    (r'DROP\s+DATABASE.*production', "Attempting to drop production database"),
    (r'DELETE\s+FROM.*production', "Attempting to delete from production database"),

    # System modifications
    (r'chmod\s+777\s+/', "Setting world-writable permissions on root"),
    (r'chown.*root', "Attempting to change ownership to root"),
]

# Check command against dangerous patterns
blocked = False
reason = ""

for pattern, description in DANGEROUS_PATTERNS:
    if re.search(pattern, command, re.IGNORECASE):
        blocked = True
        reason = description
        break

def audit(blocked, reason, command):
    """
    Best-effort audit trail. NEVER let logging failure change the verdict - the
    block must already be decided and emitted before this runs. A read-only CWD,
    or .claude-metrics existing as a file, previously raised here and skipped the
    block entirely.
    """
    try:
        log_dir = os.getenv("CLAUDE_METRICS_DIR", ".claude-metrics")
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().isoformat()
        status = "BLOCKED" if blocked else "ALLOWED"
        with open(os.path.join(log_dir, "bash_commands.log"), 'a') as f:
            f.write(f"{timestamp} | {status} | {command}\n")
        if blocked:
            hooks_log = os.getenv("CLAUDE_HOOKS_LOG", os.path.join(log_dir, "hooks.log"))
            with open(hooks_log, 'a') as f:
                f.write(f"{timestamp} | security_check | BLOCKED | {reason}\n")
    except OSError:
        pass  # auditing is best-effort; the verdict stands regardless


if blocked:
    # PreToolUse blocking contract: exit code 2 blocks. Exit 1 is a NON-blocking
    # error - the tool call proceeds and only a "hook error" notice is shown. This
    # script used to exit 1 while printing a convincing block banner, so it
    # announced a block that never happened.
    #
    # The JSON permissionDecision is the explicit documented mechanism; exit 2 is
    # the belt-and-braces fallback if stdout is not parsed. Both deny.
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Blocked by security_check: {reason}",
        }
    }))
    print(f"🚫 SECURITY: {reason}", file=sys.stderr)
    print(f"Command blocked: {command}", file=sys.stderr)
    audit(blocked, reason, command)
    sys.exit(2)

audit(blocked, reason, command)
sys.exit(0)
