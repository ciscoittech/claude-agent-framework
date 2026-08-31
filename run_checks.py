#!/usr/bin/env python3
"""
Run every framework check. One command, so there is one thing to remember.

    python3 run_checks.py            # all suites
    python3 run_checks.py --fast     # skip the suites that spawn subprocesses

The suites, in the order they run:

  test_v2_structure.py     structure, doc examples, stale claims   (~0.05s)
  test_generated_system.py builds whole systems and validates them (~0.1s)
  test_hooks.py            executes the hook scripts for real      (~1.5s)

This is what CI runs and what the PostToolUse hook runs. Adding a suite here is
what makes it run without anyone remembering to.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

SUITES = [
    ('test_v2_structure.py', 'structure and documentation', True),
    ('test_generated_system.py', 'generated systems', True),
    ('test_hooks.py', 'hook execution', False),  # spawns subprocesses
]


def main():
    fast = '--fast' in sys.argv
    results = []
    for name, label, in_fast in SUITES:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            print(f"⚠️  {name} is missing")
            results.append((name, None))
            continue
        if fast and not in_fast:
            print(f"— {name} skipped (--fast)")
            continue
        print(f"\n{'=' * 60}\n{name} — {label}\n{'=' * 60}")
        code = subprocess.run([sys.executable, path], cwd=ROOT).returncode
        results.append((name, code))

    print(f"\n{'=' * 60}")
    failed = [n for n, c in results if c != 0]
    for name, code in results:
        print(f"  {'✓' if code == 0 else '✗'} {name}")
    if failed:
        print(f"\n❌ {len(failed)} suite(s) failed: {', '.join(failed)}")
        return 1
    print("\n✅ All suites passed")
    return 0


if __name__ == '__main__':
    sys.exit(main())
