#!/usr/bin/env python3
"""
Portable validator for a Claude Agent Framework system.

Works against ANY generated system, not just this repo - which is the point:
it is how we prove the generator's output actually loads, rather than reading
the template and assuming.

Usage:
    python3 validate_agent_system.py [path-to-project-root]

Import:
    from validate_agent_system import validate, load_registry
    errors, warnings = validate(root, registry)

Exit code is 0 when there are no errors (warnings alone do not fail).
"""
import json
import os
import re
import sys

VALID_MODELS = {'haiku', 'sonnet', 'opus', 'fable'}
VALID_EFFORT = {'low', 'medium', 'high', 'xhigh', 'max'}
REQUIRED_FRONTMATTER = ('name', 'description', 'model', 'effort', 'tools')
DEPRECATED_TOOLS = ('Task', 'MultiEdit')

# Agent types Claude Code provides itself - never in a project registry.
BUILTIN_AGENTS = {'general-purpose', 'Explore', 'Plan', 'claude', 'statusline-setup'}

# Generic placeholders used in documentation to teach the mechanism. They are
# intentionally absent from REGISTRY.json and must not be reported as dangling.
DOC_PLACEHOLDER_AGENTS = {'security-reviewer', 'my-specialist', 'performance-analyst'}

SUBAGENT_PATTERN = re.compile(r'subagent_type[=:]\s*["\']([a-zA-Z0-9_-]+)["\']')

# The stub body becomes the subagent's system prompt and is paid on every launch.
MAX_STUB_LINES = 100


def load_registry(root):
    """Load REGISTRY.json. Returns (registry, error) - registry is {} on failure."""
    path = os.path.join(root, '.claude-library/REGISTRY.json')
    if not os.path.exists(path):
        return {}, f"Missing {path}"
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return {}, f"REGISTRY.json is not valid JSON: {e}"


def parse_frontmatter(path):
    """
    Flat `key: value` frontmatter between --- delimiters.

    Deliberately dependency-free: PyYAML is not guaranteed to be present in a
    generated project, and agent frontmatter is flat by contract. Returns None
    if there is no frontmatter block or it is unterminated.
    """
    try:
        with open(path, encoding='utf-8') as f:
            lines = f.read().split('\n')
    except OSError:
        return None
    if not lines or lines[0].strip() != '---':
        return None
    fm = {}
    for line in lines[1:]:
        if line.strip() == '---':
            return fm
        if ':' in line and not line.startswith((' ', '\t')):
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip()
    return None


def check_referential_integrity(root, registry):
    """Every declared path and context must resolve. A missing context degrades
    an agent silently, which is why this is an error and not a warning."""
    errors = []
    for section in ('agents', 'commands', 'contexts', 'skills'):
        for name, cfg in registry.get(section, {}).items():
            rel = cfg.get('path')
            if rel and not os.path.exists(os.path.join(root, rel)):
                errors.append(f"REGISTRY [{section}] '{name}' -> missing file: {rel}")

    contexts_dir = os.path.join(root, '.claude-library/contexts')
    for name, cfg in registry.get('agents', {}).items():
        for ctx in cfg.get('contexts', []):
            if not os.path.exists(os.path.join(contexts_dir, ctx)):
                errors.append(f"Agent '{name}' references missing context: {ctx}")

    for name, cfg in registry.get('commands', {}).items():
        for agent in cfg.get('agents', []):
            if agent not in registry.get('agents', {}):
                errors.append(f"Command '{name}' references unknown agent: {agent}")
    return errors


def check_subagent_references(root, registry):
    """A subagent_type naming a nonexistent agent fails only at launch time."""
    errors = []
    known = set(registry.get('agents', {})) | BUILTIN_AGENTS | DOC_PLACEHOLDER_AGENTS
    scan_roots = [
        os.path.join(root, '.claude-library/agents'),
        os.path.join(root, '.claude-library/contexts'),
        os.path.join(root, '.claude/commands'),
        os.path.join(root, '.claude/agents'),
    ]
    for scan_root in scan_roots:
        for dirpath, _, filenames in os.walk(scan_root):
            for fn in filenames:
                if not fn.endswith('.md'):
                    continue
                path = os.path.join(dirpath, fn)
                try:
                    content = open(path, encoding='utf-8').read()
                except (OSError, UnicodeDecodeError):
                    continue
                for ref in sorted(set(SUBAGENT_PATTERN.findall(content))):
                    if ref not in known:
                        rel = os.path.relpath(path, root)
                        errors.append(f"{rel}: subagent_type '{ref}' is not a registry agent")
    return errors


def check_tiers(root, registry):
    """model = capability floor, effort = reasoning depth. Two dials, not one."""
    errors, warnings = [], []
    for name, cfg in registry.get('agents', {}).items():
        model, effort = cfg.get('model'), cfg.get('effort')
        if model is None:
            errors.append(f"Agent '{name}' has no model tier")
        elif model not in VALID_MODELS:
            errors.append(f"Agent '{name}' invalid model '{model}' (allowed: {sorted(VALID_MODELS)})")
        if effort is None:
            errors.append(f"Agent '{name}' has no effort tier")
        elif effort not in VALID_EFFORT:
            errors.append(f"Agent '{name}' invalid effort '{effort}' (allowed: {sorted(VALID_EFFORT)})")
        # Haiku is the only 200K model; deep reasoning there is a tier mistake
        if model == 'haiku' and effort not in {'low', 'medium'}:
            warnings.append(
                f"Agent '{name}': haiku at effort '{effort}' - use a higher model tier instead")
        for dead in DEPRECATED_TOOLS:
            if dead in cfg.get('tools', []):
                errors.append(f"Agent '{name}' uses deprecated tool name '{dead}' (use Agent / Edit)")
    return errors, warnings


def check_subagent_definitions(root, registry):
    """The registry declares the tier; .claude/agents/ is what Claude Code honors.
    If they disagree, the tier is prose again."""
    errors, warnings = [], []
    agents_dir = os.path.join(root, '.claude/agents')
    if not os.path.isdir(agents_dir):
        errors.append("Missing .claude/agents/ - registry tiers are not enforced without it")
        return errors, warnings

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
        for key in REQUIRED_FRONTMATTER:
            if key not in fm:
                errors.append(f".claude/agents/{name}.md missing frontmatter key: {key}")
        if fm.get('name') != name:
            errors.append(f".claude/agents/{name}.md: name '{fm.get('name')}' != filename")
        cfg = registry['agents'][name]
        if fm.get('model') != cfg.get('model'):
            errors.append(
                f".claude/agents/{name}.md model '{fm.get('model')}' != registry '{cfg.get('model')}'")
        if fm.get('effort') != cfg.get('effort'):
            errors.append(
                f".claude/agents/{name}.md effort '{fm.get('effort')}' != registry '{cfg.get('effort')}'")
        fm_tools = {t.strip() for t in fm.get('tools', '').split(',') if t.strip()}
        if fm_tools != set(cfg.get('tools', [])):
            errors.append(
                f".claude/agents/{name}.md tools {sorted(fm_tools)} != registry {sorted(cfg.get('tools', []))}")
        nlines = sum(1 for _ in open(path, encoding='utf-8'))
        if nlines > MAX_STUB_LINES:
            warnings.append(
                f".claude/agents/{name}.md is {nlines} lines "
                f"(keep stubs <={MAX_STUB_LINES}; depth belongs in .claude-library/)")
    return errors, warnings


def validate(root, registry):
    """Run every portable check. Returns (errors, warnings)."""
    errors, warnings = [], []
    errors += check_referential_integrity(root, registry)
    errors += check_subagent_references(root, registry)
    e, w = check_tiers(root, registry)
    errors += e
    warnings += w
    e, w = check_subagent_definitions(root, registry)
    errors += e
    warnings += w
    return errors, warnings


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
    print(f"Validating agent system at: {root}\n")

    registry, load_error = load_registry(root)
    if load_error:
        print(f"❌ {load_error}")
        return 1

    n_agents = len(registry.get('agents', {}))
    n_commands = len(registry.get('commands', {}))
    print(f"REGISTRY.json: {n_agents} agents, {n_commands} commands")

    errors, warnings = validate(root, registry)

    print(f"{'✓' if not errors else '✗'} {len(errors)} errors, {len(warnings)} warnings\n")
    for e in errors:
        print(f"  ✗ {e}")
    for w in warnings:
        print(f"  ⚠ {w}")

    if not errors:
        print("\n✅ Agent system is valid" + (f" ({len(warnings)} warnings)" if warnings else ""))
    else:
        print(f"\n❌ Agent system is INVALID: {len(errors)} errors")
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
