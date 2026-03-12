#!/usr/bin/env python3
"""Structural validation for Claude Agent Framework v2.0"""
import json
import os
import re
import sys

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
    'AGENT_SYSTEM_TEMPLATE.md', 'MULTI_MODEL_ROUTING.md',
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
