#!/usr/bin/env python3
"""
Security check hook - validates bash commands before execution
Blocks dangerous operations that could damage the system
"""

import sys
import re
import os
from datetime import datetime

command = sys.argv[1] if len(sys.argv) > 1 else ""

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

# Log all bash commands for audit trail
log_dir = ".claude-metrics"
os.makedirs(log_dir, exist_ok=True)

audit_log = os.path.join(log_dir, "bash_commands.log")
with open(audit_log, 'a') as f:
    timestamp = datetime.now().isoformat()
    status = "BLOCKED" if blocked else "ALLOWED"
    f.write(f"{timestamp} | {status} | {command}\n")

# If blocked, also log to hooks log
if blocked:
    hooks_log = os.getenv("CLAUDE_HOOKS_LOG", os.path.join(log_dir, "hooks.log"))
    with open(hooks_log, 'a') as f:
        f.write(f"{timestamp} | security_check | BLOCKED | {reason}\n")

    print(f"🚫 SECURITY: {reason}", file=sys.stderr)
    print(f"Command blocked: {command}", file=sys.stderr)
    sys.exit(1)  # Non-zero exit blocks the command

# Command is safe, allow it
sys.exit(0)
