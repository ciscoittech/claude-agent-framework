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

# === 5b. REGISTRY referential integrity ===
# Every declared path and every agent context must resolve to a real file.
# An agent told to load a missing context degrades silently, so this is an error.
dead_paths = 0
for section in ('agents', 'commands', 'contexts', 'skills'):
    for name, cfg in registry.get(section, {}).items():
        rel = cfg.get('path')
        if rel and not os.path.exists(os.path.join(ROOT, rel)):
            errors.append(f"REGISTRY [{section}] '{name}' -> missing file: {rel}")
            dead_paths += 1

contexts_dir = os.path.join(ROOT, '.claude-library/contexts')
for name, cfg in registry.get('agents', {}).items():
    for ctx in cfg.get('contexts', []):
        if not os.path.exists(os.path.join(contexts_dir, ctx)):
            errors.append(f"Agent '{name}' references missing context: {ctx}")
            dead_paths += 1

# Agents named in a command's agents[] must exist in the registry
for name, cfg in registry.get('commands', {}).items():
    for agent in cfg.get('agents', []):
        if agent not in registry.get('agents', {}):
            errors.append(f"Command '{name}' references unknown agent: {agent}")
            dead_paths += 1

print(f"{'✓' if dead_paths == 0 else '✗'} Referential integrity: {dead_paths} dead references")

# === 5b2. subagent_type references must resolve ===
# A subagent_type naming an agent that does not exist fails only at launch time,
# which is the worst place to find out. Scan playbooks and commands for them.
BUILTIN_AGENTS = {'general-purpose', 'Explore', 'Plan', 'claude', 'statusline-setup'}
# Generic placeholders in documentation that teach the mechanism rather than wire
# a real agent. They intentionally do not exist in REGISTRY.json.
DOC_PLACEHOLDER_AGENTS = {'security-reviewer', 'my-specialist', 'performance-analyst'}
subagent_pat = re.compile(r'subagent_type[=:]\s*["\']([a-zA-Z0-9_-]+)["\']')
dangling = 0
scan_roots = [
    os.path.join(ROOT, '.claude-library/agents'),
    os.path.join(ROOT, '.claude/commands'),
    os.path.join(ROOT, '.claude/agents'),
    os.path.join(ROOT, '.claude-library/contexts'),
]
for root in scan_roots:
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, ROOT)
            for referenced in set(subagent_pat.findall(open(path, encoding='utf-8').read())):
                if (referenced in registry.get('agents', {})
                        or referenced in BUILTIN_AGENTS
                        or referenced in DOC_PLACEHOLDER_AGENTS):
                    continue
                errors.append(f"{rel}: subagent_type '{referenced}' is not a registry agent")
                dangling += 1
print(f"{'✓' if dangling == 0 else '✗'} subagent_type references: {dangling} dangling")

# === 5c. Model and effort tiers ===
# model = capability floor, effort = reasoning depth. Two dials, not one.
VALID_MODELS = {'haiku', 'sonnet', 'opus', 'fable'}
VALID_EFFORT = {'low', 'medium', 'high', 'xhigh', 'max'}
for name, cfg in registry.get('agents', {}).items():
    model, effort = cfg.get('model'), cfg.get('effort')
    check(model is not None, f"Agent '{name}' has no model tier")
    check(effort is not None, f"Agent '{name}' has no effort tier")
    if model is not None:
        check(model in VALID_MODELS, f"Agent '{name}' invalid model '{model}' (allowed: {sorted(VALID_MODELS)})")
    if effort is not None:
        check(effort in VALID_EFFORT, f"Agent '{name}' invalid effort '{effort}' (allowed: {sorted(VALID_EFFORT)})")
    # Haiku is the only 200K model; it must not be paired with deep-reasoning effort
    if model == 'haiku':
        check(effort in {'low', 'medium'}, f"Agent '{name}': haiku at effort '{effort}' - use a higher model tier instead", warn=True)
print(f"✓ Model/effort tiers: {len(registry.get('agents', {}))} agents checked")

# === 5d. .claude/agents/ subagent definitions ===
# Registry declares the tier; the stub is what Claude Code actually honors.
# They must agree, or the tier is prose again.
def parse_frontmatter(path):
    """Flat `key: value` frontmatter between --- delimiters. No YAML dependency."""
    lines = open(path).read().split('\n')
    if not lines or lines[0].strip() != '---':
        return None
    fm = {}
    for line in lines[1:]:
        if line.strip() == '---':
            return fm
        if ':' in line and not line.startswith((' ', '\t')):
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip()
    return None  # unterminated frontmatter block

agents_dir = os.path.join(ROOT, '.claude/agents')
REQUIRED_FM = ('name', 'description', 'model', 'effort', 'tools')
if not os.path.isdir(agents_dir):
    errors.append("Missing .claude/agents/ - registry tiers are not enforced without it")
else:
    stubs = {f[:-3] for f in os.listdir(agents_dir) if f.endswith('.md')}
    reg_agents = set(registry.get('agents', {}))
    for missing in sorted(reg_agents - stubs):
        errors.append(f"Registry agent '{missing}' has no .claude/agents/{missing}.md definition")
    for orphan in sorted(stubs - reg_agents):
        errors.append(f".claude/agents/{orphan}.md has no REGISTRY.json entry")

    for name in sorted(stubs & reg_agents):
        path = os.path.join(agents_dir, f'{name}.md')
        fm = parse_frontmatter(path)
        if fm is None:
            errors.append(f".claude/agents/{name}.md: no parseable frontmatter block")
            continue
        for key in REQUIRED_FM:
            check(key in fm, f".claude/agents/{name}.md missing frontmatter key: {key}")
        check(fm.get('name') == name, f".claude/agents/{name}.md: name '{fm.get('name')}' != filename")
        cfg = registry['agents'][name]
        check(fm.get('model') == cfg.get('model'),
              f".claude/agents/{name}.md model '{fm.get('model')}' != registry '{cfg.get('model')}'")
        check(fm.get('effort') == cfg.get('effort'),
              f".claude/agents/{name}.md effort '{fm.get('effort')}' != registry '{cfg.get('effort')}'")
        fm_tools = {t.strip() for t in fm.get('tools', '').split(',') if t.strip()}
        check(fm_tools == set(cfg.get('tools', [])),
              f".claude/agents/{name}.md tools {sorted(fm_tools)} != registry {sorted(cfg.get('tools', []))}")
        # The stub body is the system prompt, paid on every launch. Keep it lean.
        nlines = sum(1 for _ in open(path))
        check(nlines <= 100, f".claude/agents/{name}.md is {nlines} lines (keep stubs <=100; depth belongs in .claude-library/)", warn=True)
    print(f"✓ Subagent definitions: {len(stubs)} stubs validated against registry")

# Deprecated tool names must not reappear
for name, cfg in registry.get('agents', {}).items():
    for dead in ('Task', 'MultiEdit'):
        check(dead not in cfg.get('tools', []),
              f"Agent '{name}' uses deprecated tool name '{dead}' (use Agent / Edit)")

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
