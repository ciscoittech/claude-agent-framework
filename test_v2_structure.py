#!/usr/bin/env python3
"""Structural validation for Claude Agent Framework v2.0"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_agent_system

ROOT = os.path.dirname(os.path.abspath(__file__))
errors = []
warnings = []

def check(condition, msg, warn=False):
    if not condition:
        (warnings if warn else errors).append(msg)

# === 1. Root doc count ===
root_mds = [f for f in os.listdir(ROOT) if f.endswith('.md') and os.path.isfile(os.path.join(ROOT, f))]
check(len(root_mds) <= 10, f"Root docs: {len(root_mds)} (expected ≤10)")
print(f"✓ Root docs: {len(root_mds)} files")

# === 2. Expected files exist ===
expected_files = [
    'SIMPLICITY_ENFORCEMENT.md', 'SYSTEM_GENERATOR_PROMPT.md',
    'CLAUDE_AGENT_FRAMEWORK.md', 'AGENT_PATTERNS.md',
    'AGENT_SYSTEM_TEMPLATE.md', 'MODEL_SELECTION.md',
    'CLAUDE.md', 'README.md', 'CHANGELOG.md',
    '.claude-library/REGISTRY.json',
]
for f in expected_files:
    path = os.path.join(ROOT, f)
    check(os.path.exists(path), f"Missing expected file: {f}")
print(f"✓ All {len(expected_files)} expected files exist")

# === 3. Archived files should NOT exist at root ===
archived = [
    'AGENT_REFERENCE_PATTERNS.md', 'ANTHROPIC_TEAM_PATTERNS.md',
    'PROJECT_ANALYZER_PROMPT.md', 'QUICK_START_BEST_PRACTICES.md',
    'AGENT_SKILLS_RESEARCH.md', 'SKILLS_EXPLORATION_OVERVIEW.md',
    'SKILLS_INTEGRATION_GUIDE.md', 'SKILLS_INTEGRATION_STRATEGY.md',
    'SKILLS_QUICK_REFERENCE.md',
]
for f in archived:
    check(not os.path.exists(os.path.join(ROOT, f)), f"Archived file still at root: {f}")
print(f"✓ No archived files at root")

# === 4. Archive directories exist and have correct file counts ===
skills_archive = os.path.join(ROOT, 'archive/v1-skills-research')
patterns_archive = os.path.join(ROOT, 'archive/v1-patterns')
check(os.path.isdir(skills_archive), "Missing archive/v1-skills-research/")
check(os.path.isdir(patterns_archive), "Missing archive/v1-patterns/")
if os.path.isdir(skills_archive):
    check(len(os.listdir(skills_archive)) == 5, f"Expected 5 files in skills archive, got {len(os.listdir(skills_archive))}")
if os.path.isdir(patterns_archive):
    check(len(os.listdir(patterns_archive)) == 4, f"Expected 4 files in patterns archive, got {len(os.listdir(patterns_archive))}")
print(f"✓ Archive directories intact")

# === 5. REGISTRY.json is valid JSON ===
registry_path = os.path.join(ROOT, '.claude-library/REGISTRY.json')
try:
    with open(registry_path) as f:
        registry = json.load(f)
    check(registry.get('version') == '2.0.0', f"REGISTRY version: {registry.get('version')} (expected 2.0.0)")
    check('agents' in registry, "REGISTRY missing 'agents' section")
    check('commands' in registry, "REGISTRY missing 'commands' section")
    check('contexts' in registry, "REGISTRY missing 'contexts' section")
    check('skills' in registry, "REGISTRY missing 'skills' section")
    check('agent_defaults' in registry, "REGISTRY missing 'agent_defaults' section")
    check('workflows' not in registry, "REGISTRY still has removed 'workflows' section")
    check('performance_baselines' not in registry, "REGISTRY still has removed 'performance_baselines'")
    check('meta_framework_config' not in registry, "REGISTRY still has removed 'meta_framework_config'")
    print(f"✓ REGISTRY.json valid (v{registry.get('version')}, {len(registry.get('agents', {}))} agents, {len(registry.get('commands', {}))} commands)")
except json.JSONDecodeError as e:
    errors.append(f"REGISTRY.json invalid JSON: {e}")
    registry = {}

# === 5b-5d. Portable agent-system checks ===
# These live in validate_agent_system.py so the SAME checks run against a
# generated system, not just this repo. Importing them here means the generator
# smoke test and this suite can never drift apart.
portable_errors, portable_warnings = validate_agent_system.validate(ROOT, registry)
errors.extend(portable_errors)
warnings.extend(portable_warnings)
print(f"{'✓' if not portable_errors else '✗'} Agent system validation: "
      f"{len(portable_errors)} errors, {len(portable_warnings)} warnings "
      f"({len(registry.get('agents', {}))} agents)")

# === 6. Line count targets ===
targets = {
    'AGENT_PATTERNS.md': (1200, 1600),
    'SYSTEM_GENERATOR_PROMPT.md': (450, 650),
    'CLAUDE_AGENT_FRAMEWORK.md': (550, 850),
    'AGENT_SYSTEM_TEMPLATE.md': (550, 750),
    'README.md': (180, 300),
    'CLAUDE.md': (100, 200),
}
for fname, (lo, hi) in targets.items():
    path = os.path.join(ROOT, fname)
    if os.path.exists(path):
        lines = sum(1 for _ in open(path))
        check(lo <= lines <= hi, f"{fname}: {lines} lines (expected {lo}-{hi})", warn=True)
        print(f"  {fname}: {lines} lines {'✓' if lo <= lines <= hi else '⚠️'}")

# === 7. CLAUDE.md has no references to archived files ===
with open(os.path.join(ROOT, 'CLAUDE.md')) as f:
    claude_content = f.read()
for archived_name in ['PROJECT_ANALYZER_PROMPT', 'AGENT_REFERENCE_PATTERNS', 'ANTHROPIC_TEAM_PATTERNS',
                       'SKILLS_INTEGRATION', 'SKILLS_EXPLORATION', 'SKILLS_QUICK_REFERENCE']:
    check(archived_name not in claude_content, f"CLAUDE.md still references archived: {archived_name}")
print(f"✓ CLAUDE.md has no stale references")

# === 8. New v2.0 features present ===
with open(os.path.join(ROOT, 'AGENT_PATTERNS.md')) as f:
    patterns = f.read()
v2_features = ['Agent Teams', 'worktree', 'run_in_background', 'Effort Level', 'context: fork']
for feat in v2_features:
    check(feat.lower() in patterns.lower(), f"AGENT_PATTERNS.md missing v2.0 feature: {feat}", warn=True)
print(f"✓ v2.0 features check complete")

# === 8b. Stale model-era claims must not reappear ===
# These were the specific wrong statements the v2.1 model pass removed. They are
# cheap to reintroduce by copy-paste, so guard them explicitly.
def live_docs():
    """Every tracked .md/.py outside archive/ (archive is history, left as-is)."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {'archive', '.git', '__pycache__', '.claude-metrics'}]
        for fn in filenames:
            if fn.endswith(('.md', '.py', '.json')):
                yield os.path.join(dirpath, fn)

STALE_PATTERNS = [
    # (regex, why it is wrong now)
    (r'Opus\s*\(\$15/1M', "Opus 5 is $5/$25 per 1M, not $15"),
    (r'Claude Sonnet \(\$3/1M', "Sonnet 5 is $2/$10 per 1M, not $3"),
    (r'`model:\s*"haiku"`\s*for fast/cheap', "conflates model tier with effort"),
    (r'qwen', "third-party routing was removed in favour of Claude-native tiers"),
    (r'MULTI_MODEL_ROUTING\.md', "renamed to MODEL_SELECTION.md"),
    # Observability was retired to archive/v2-observability/. The live tree must not
    # reference it - a dangling obs.py call or Logfire config fails only at runtime.
    (r'\.claude-library/observability', "observability retired to archive/v2-observability/"),
    (r'obs\.py', "observability CLI is archived"),
    (r'logfire', "Logfire integration was removed with observability"),
    (r'/self-improve', "command removed - it consumed observability data"),
]
stale_hits = 0
for path in live_docs():
    rel = os.path.relpath(path, ROOT)
    if rel in ('test_v2_structure.py', 'CHANGELOG.md'):
        continue  # this file defines the patterns; CHANGELOG records history
    if rel.startswith('archive' + os.sep):
        continue  # archived material is history, left exactly as retired
    try:
        content = open(path, encoding='utf-8').read()
    except (UnicodeDecodeError, OSError):
        continue
    for pattern, why in STALE_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f"{rel}: stale model-era claim /{pattern}/ - {why}")
            stale_hits += 1
print(f"{'✓' if stale_hits == 0 else '✗'} Stale model claims: {stale_hits} found")

# === 9. Context files updated ===
contexts_dir = os.path.join(ROOT, '.claude-library/contexts')
for ctx in ['claude-code-subagents.md', 'claude-code-best-practices.md', 'claude-code-mcp.md']:
    path = os.path.join(contexts_dir, ctx)
    if os.path.exists(path):
        content = open(path).read()
        check('2026' in content, f"{ctx}: Last Updated not refreshed to 2026", warn=True)

print(f"✓ Context files date check complete")

# === Results ===
print("\n" + "="*60)
if errors:
    print(f"❌ {len(errors)} ERRORS:")
    for e in errors:
        print(f"  ✗ {e}")
if warnings:
    print(f"⚠️  {len(warnings)} WARNINGS:")
    for w in warnings:
        print(f"  ⚠ {w}")
if not errors and not warnings:
    print("✅ ALL CHECKS PASSED")
elif not errors:
    print(f"✅ PASSED with {len(warnings)} warnings")
else:
    print(f"❌ FAILED: {len(errors)} errors, {len(warnings)} warnings")

sys.exit(1 if errors else 0)
