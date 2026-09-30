#!/usr/bin/env python3
"""
Generated-system tests: build whole agent systems and validate them.

`test_v2_structure.py` holds the docs' JSON examples to the contract, and
`validate_agent_system.py` checks a system that already exists. Neither one
builds a system and runs it through the validator end to end - that was a manual
step involving a subagent, so it ran when someone remembered, and it is the step
that found the worst generator defects.

Three suites here:

1. **Canonical fixture** - the minimal system §4.1 describes, built exactly as
   §4.6b specifies, must validate clean. If the contract as written produces an
   invalid system, the contract is wrong.
2. **Negative fixtures** - each deviates from that fixture in exactly one way and
   must be caught. A validator is only worth its passing runs if its failing runs
   are proven, and every check here corresponds to a defect that shipped green.
3. **Doc-derived systems** - every registry example in the documentation is
   materialized into a real tree and validated. An example that cannot be built
   is an example that costs its reader a debugging session.

Usage: python3 test_generated_system.py
Exit code 0 when every check passes.
"""
import json
import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_agent_system as V

ROOT = os.path.dirname(os.path.abspath(__file__))

failures = []
passes = 0


def ok(name):
    global passes
    passes += 1
    print(f"  ✓ {name}")


def fail(name, detail):
    failures.append(f"{name}: {detail}")
    print(f"  ✗ {name}\n      {detail}")


def check(cond, name, detail=""):
    ok(name) if cond else fail(name, detail)


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


# --------------------------------------------------------------- the fixture

CANONICAL = {
    "version": "2.0.0",
    "agents": {
        "architect": {
            "path": ".claude-library/agents/core/architect.md",
            "type": "core",
            "domain": "architecture",
            "tools": ["Read", "Write", "Edit", "Grep", "Glob"],
            "model": "opus",
            "effort": "xhigh",
            "triggers": ["design", "architecture", "spec"],
            "contexts": ["project.md"],
            "priority": 1,
        },
        "engineer": {
            "path": ".claude-library/agents/core/engineer.md",
            "type": "core",
            "domain": "implementation",
            "tools": ["Read", "Write", "Edit", "Grep", "Glob", "Bash"],
            "model": "opus",
            "effort": "high",
            "triggers": ["implement", "build", "fix"],
            "contexts": ["project.md"],
            "priority": 1,
        },
        "reviewer": {
            "path": ".claude-library/agents/core/reviewer.md",
            "type": "core",
            "domain": "quality",
            "tools": ["Read", "Grep", "Glob"],
            "model": "opus",
            "effort": "high",
            "triggers": ["review", "quality"],
            "contexts": ["project.md"],
            "priority": 2,
        },
    },
    "commands": {
        "build": {
            "path": ".claude/commands/build.md",
            "agents": ["architect", "engineer", "reviewer"],
            "workflow": "sequential",
        },
    },
    "contexts": {
        "project": {
            "path": ".claude-library/contexts/project.md",
            "description": "Stack, conventions, and layout",
        },
    },
    "skills": {
        "build": {
            "path": ".claude/commands/build.md",
            "description": "Build the feature described, using the project's agents",
            "allowed_tools": ["Agent", "Read", "Write", "Edit", "Grep", "Glob"],
        },
    },
}

SETTINGS = {
    "hooks": {
        "PostToolUse": [
            {
                "matcher": "Write|Edit",
                "hooks": [{"type": "command",
                           "command": 'bash "$CLAUDE_PROJECT_DIR"/scripts/format.sh'}],
            }
        ]
    }
}


def stub(name, cfg):
    """The .claude/agents/<name>.md a correct generator emits for this entry."""
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {cfg.get('domain', name)} specialist. "
        f"Use for {', '.join(cfg.get('triggers', [name]))}.\n"
        f"model: {cfg['model']}\n"
        f"effort: {cfg['effort']}\n"
        f"tools: {', '.join(cfg['tools'])}\n"
        "---\n\n"
        f"You are the {name}.\n\n"
        "## When you are the right agent\n"
        f"{', '.join(cfg.get('triggers', []))}.\n\n"
        "## Before you start\n"
        f"Read `{cfg['path']}` for the full playbook.\n"
    )


def command_file(cfg):
    return (
        "---\n"
        f"description: {cfg['description']}\n"
        f"allowed-tools: {', '.join(cfg['allowed_tools'])}\n"
        + ("disable-model-invocation: true\n" if cfg.get('disable_model_invocation') else "")
        + "---\n\n"
        "## Steps\n1. Do the thing.\n"
    )


def materialize(root, registry, settings=None):
    """
    Write out every file the registry declares, following §4.6b exactly.

    This is what a correct generator does, so anything it cannot build from a
    registry entry is a registry entry a generator cannot build either.
    """
    write(os.path.join(root, '.claude-library/REGISTRY.json'),
          json.dumps(registry, indent=2))

    for name, cfg in registry.get('agents', {}).items():
        if cfg.get('path'):
            write(os.path.join(root, cfg['path']),
                  f"# {name}\n\nFull playbook. Depth lives here.\n")
        if cfg.get('model') and cfg.get('effort') and cfg.get('tools'):
            write(os.path.join(root, '.claude/agents', f'{name}.md'), stub(name, cfg))
        # contexts[] are bare filenames under .claude-library/contexts/
        for ctx in cfg.get('contexts', []):
            write(os.path.join(root, '.claude-library/contexts', ctx),
                  f"# {ctx}\n\nProject knowledge.\n")

    for section in ('contexts', 'patterns'):
        for name, cfg in registry.get(section, {}).items():
            if isinstance(cfg, dict) and cfg.get('path'):
                write(os.path.join(root, cfg['path']), f"# {name}\n")

    for name, cfg in registry.get('skills', {}).items():
        write(os.path.join(root, '.claude/commands', f'{name}.md'), command_file(cfg))

    # A command with no skills entry has no frontmatter and fails validation, so
    # a correct generator writes both. Mirror that.
    for name, cfg in registry.get('commands', {}).items():
        path = os.path.join(root, '.claude/commands', f'{name}.md')
        if not os.path.exists(path) and cfg.get('path'):
            write(os.path.join(root, cfg['path']), "## Steps\n1. Do the thing.\n")

    if settings is not None:
        write(os.path.join(root, '.claude/settings.json'), json.dumps(settings, indent=2))
    return root


def build(registry=None, settings=None):
    """Materialize into a temp dir and validate. Returns (errors, warnings, root)."""
    root = tempfile.mkdtemp()
    materialize(root, json.loads(json.dumps(registry or CANONICAL)), settings)
    loaded, err = V.load_registry(root)
    if err:
        return [err], [], root
    e, w = V.validate(root, loaded)
    return e, w, root


# ------------------------------------------------------- 1. canonical fixture
print("\ncanonical fixture (the system §4.1 and §4.6b describe)")
errors, warnings, root = build(settings=SETTINGS)
check(not errors, "a system built exactly to the contract validates clean",
      "\n      ".join(errors))
check(not warnings, "and produces no warnings", "\n      ".join(warnings))
# The two path conventions really are different, and the fixture proves it
check(os.path.exists(os.path.join(root, '.claude-library/agents/core/architect.md')),
      "path entries resolve from the repo root")
check(os.path.exists(os.path.join(root, '.claude-library/contexts/project.md')),
      "contexts[] entries resolve under .claude-library/contexts/")
check(os.path.exists(os.path.join(root, '.claude/agents/architect.md')),
      "every registry agent gets a .claude/agents stub")
shutil.rmtree(root, ignore_errors=True)


# ------------------------------------------------------- 2. negative fixtures
print("\nnegative fixtures (one deviation each; all must be caught)")


def deviate(mutate, label, settings=SETTINGS):
    """Apply one mutation to a materialized canonical system and validate."""
    root = tempfile.mkdtemp()
    try:
        reg = json.loads(json.dumps(CANONICAL))
        reg = mutate(reg, root) or reg
        materialize(root, reg, settings)
        # a second pass lets a mutation edit files after they are written
        post = getattr(mutate, 'post', None)
        if post:
            post(root)
        loaded, err = V.load_registry(root)
        errs = [err] if err else V.validate(root, loaded)[0]
        check(bool(errs), f"caught: {label}", "validator reported no error")
    finally:
        shutil.rmtree(root, ignore_errors=True)


def post_mutation(label, edit, settings=SETTINGS):
    """A deviation applied to the tree after it is written."""
    root = tempfile.mkdtemp()
    try:
        materialize(root, json.loads(json.dumps(CANONICAL)), settings)
        edit(root)
        loaded, err = V.load_registry(root)
        errs = [err] if err else V.validate(root, loaded)[0]
        check(bool(errs), f"caught: {label}", "validator reported no error")
    finally:
        shutil.rmtree(root, ignore_errors=True)


# --- registry-side deviations
def _no_agents(reg, root):
    reg['agents'] = {}
deviate(_no_agents, "registry declares zero agents")

def _wildcard_tools(reg, root):
    reg['agents']['architect']['tools'] = ['*']
deviate(_wildcard_tools, "agent granted wildcard tools")

def _empty_tools(reg, root):
    reg['agents']['architect']['tools'] = []
deviate(_empty_tools, "agent granted an empty tools list")

def _deprecated_tool(reg, root):
    reg['agents']['architect']['tools'].append('Task')
deviate(_deprecated_tool, "agent uses the retired tool name 'Task'")

def _no_model(reg, root):
    del reg['agents']['architect']['model']
deviate(_no_model, "agent has no model tier")

def _no_effort(reg, root):
    del reg['agents']['architect']['effort']
deviate(_no_effort, "agent has no effort tier")

def _bad_model(reg, root):
    reg['agents']['architect']['model'] = 'gpt-4'
deviate(_bad_model, "agent declares a model outside the allowed set")

def _bad_effort(reg, root):
    reg['agents']['architect']['effort'] = 'extreme'
deviate(_bad_effort, "agent declares an effort outside the allowed set")

def _missing_context(reg, root):
    reg['agents']['architect']['contexts'] = ['nonexistent.md']
    # materialize() writes declared contexts, so remove it after the fact
_missing_context.post = lambda root: os.remove(
    os.path.join(root, '.claude-library/contexts/nonexistent.md'))
deviate(_missing_context, "agent references a context file that is absent")

def _context_as_path(reg, root):
    # The single most common generation error: contexts[] written as a
    # repo-root path instead of a bare filename.
    reg['agents']['architect']['contexts'] = ['.claude-library/contexts/project.md']
_context_as_path.post = lambda root: shutil.rmtree(
    os.path.join(root, '.claude-library/contexts/.claude-library'), ignore_errors=True)
deviate(_context_as_path, "contexts[] written as a repo-root path")

def _unknown_command_agent(reg, root):
    reg['commands']['build']['agents'].append('ghost')
deviate(_unknown_command_agent, "command references an agent that does not exist")

def _skill_without_file(reg, root):
    reg['skills']['deploy'] = dict(reg['skills']['build'],
                                   path='.claude/commands/deploy.md')
_skill_without_file.post = lambda root: os.remove(
    os.path.join(root, '.claude/commands/deploy.md'))
deviate(_skill_without_file, "registry skill with no command file")

# --- the SKILL.md form (issue #11) -------------------------------------------
# Both forms create /name. A SKILL.md wins over a same-named command file, so a
# project carrying both has a command file that looks live and is dead.

def _skill_md_both_forms(reg, root):
    """SKILL.md alongside the command file of the same name."""
    d = os.path.join(root, '.claude/skills/build')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'SKILL.md'), 'w').write(
        "---\nname: build\ndescription: %s\nallowed-tools: %s\n---\nbody\n"
        % (reg['skills']['build']['description'],
           ', '.join(reg['skills']['build']['allowed_tools'])))
deviate(_skill_md_both_forms, "skill exists as both SKILL.md and a command file")


def _skill_md_name_mismatch(reg, root):
    """SKILL.md whose name: disagrees with its directory."""
    reg['skills']['audit'] = dict(reg['skills']['build'],
                                  path='.claude/skills/audit/SKILL.md')
    d = os.path.join(root, '.claude/skills/audit')
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'SKILL.md'), 'w').write(
        "---\nname: not-audit\ndescription: %s\nallowed-tools: %s\n---\nbody\n"
        % (reg['skills']['build']['description'],
           ', '.join(reg['skills']['build']['allowed_tools'])))
deviate(_skill_md_name_mismatch, "SKILL.md name does not match its directory")

def _wildcard_bash(reg, root):
    reg['skills']['build']['allowed_tools'] = ['Bash(*)']
deviate(_wildcard_bash, "command pre-approves unrestricted Bash(*)")

def _no_allowed_tools(reg, root):
    reg['skills']['build']['allowed_tools'] = []
deviate(_no_allowed_tools, "command declares no allowed-tools")

def _dead_path(reg, root):
    reg['agents']['architect']['path'] = '.claude-library/agents/core/gone.md'
_dead_path.post = lambda root: os.remove(
    os.path.join(root, '.claude-library/agents/core/gone.md'))
deviate(_dead_path, "agent path points at a file that is not there")

# --- file-side deviations
post_mutation("stub has no frontmatter", lambda root: write(
    os.path.join(root, '.claude/agents/architect.md'), "You are the architect.\n"))

post_mutation("stub model disagrees with the registry", lambda root: write(
    os.path.join(root, '.claude/agents/architect.md'),
    stub('architect', dict(CANONICAL['agents']['architect'], model='haiku'))))

post_mutation("stub effort disagrees with the registry", lambda root: write(
    os.path.join(root, '.claude/agents/architect.md'),
    stub('architect', dict(CANONICAL['agents']['architect'], effort='low'))))

post_mutation("stub tools disagree with the registry", lambda root: write(
    os.path.join(root, '.claude/agents/architect.md'),
    stub('architect', dict(CANONICAL['agents']['architect'], tools=['Read']))))

post_mutation("stub tools written as a YAML block list", lambda root: write(
    os.path.join(root, '.claude/agents/architect.md'),
    "---\nname: architect\ndescription: d\nmodel: opus\neffort: xhigh\ntools:\n"
    "  - Read\n  - Write\n---\n\nBody.\n"))

post_mutation("registry agent has no .claude/agents stub", lambda root: os.remove(
    os.path.join(root, '.claude/agents/architect.md')))

post_mutation("orphan stub with no registry entry", lambda root: write(
    os.path.join(root, '.claude/agents/ghost.md'),
    stub('ghost', CANONICAL['agents']['reviewer'])))

post_mutation("command file has no frontmatter", lambda root: write(
    os.path.join(root, '.claude/commands/build.md'), "Just do it.\n"))

post_mutation("command description disagrees with the registry", lambda root: write(
    os.path.join(root, '.claude/commands/build.md'),
    command_file(dict(CANONICAL['skills']['build'], description='Something else'))))

post_mutation("command file with no registry skills entry", lambda root: write(
    os.path.join(root, '.claude/commands/rogue.md'),
    command_file(CANONICAL['skills']['build'])))

post_mutation("settings.json is malformed", lambda root: write(
    os.path.join(root, '.claude/settings.json'), '{"hooks": [,]}'))

post_mutation("hook matcher uses the retired tool name Task", lambda root: write(
    os.path.join(root, '.claude/settings.json'), json.dumps({
        "hooks": {"PreToolUse": [{"matcher": "Task", "hooks": [
            {"type": "command", "command": "true"}]}]}})))

post_mutation("subagent_type names an agent that does not exist", lambda root: write(
    os.path.join(root, '.claude/commands/build.md'),
    command_file(CANONICAL['skills']['build'])
    + '\nLaunch with subagent_type="does-not-exist".\n'))


# ---------------------------------------------------- 3. doc-derived systems
print("\ndoc-derived systems (every registry example, built and validated)")

CONTRACT_DOCS = ('SYSTEM_GENERATOR_PROMPT.md', 'AGENT_SYSTEM_TEMPLATE.md',
                 'CLAUDE_AGENT_FRAMEWORK.md', 'AGENT_PATTERNS.md')

examples = []
for doc in CONTRACT_DOCS:
    path = os.path.join(ROOT, doc)
    if not os.path.exists(path):
        continue
    text = open(path, encoding='utf-8').read()
    for m in re.finditer(r'```json\n(.*?)```', text, re.S):
        try:
            block = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue  # not every fragment is standalone JSON
        if isinstance(block, dict) and isinstance(block.get('agents'), dict) \
                and block['agents']:
            examples.append((doc, text[:m.start()].count('\n') + 1, block))

check(len(examples) >= 3, "found registry examples to build",
      f"only {len(examples)} found across {len(CONTRACT_DOCS)} documents")

for doc, line_no, block in examples:
    block.setdefault('version', '2.0.0')
    errors, warnings, root = build(registry=block)
    shutil.rmtree(root, ignore_errors=True)
    check(not errors, f"{doc}:{line_no} builds into a valid system",
          "\n      ".join(errors))


# ----------------------------------------------------------------- the repo
print("\nthis repository")
registry, err = V.load_registry(ROOT)
check(err is None, "REGISTRY.json loads", err or "")
if not err:
    errors, warnings = V.validate(ROOT, registry)
    check(not errors, "the framework's own system validates", "\n      ".join(errors))
    check(not warnings, "with no warnings", "\n      ".join(warnings))


# ---------------------------------------------------------------------- result
print("\n" + "=" * 60)
if failures:
    print(f"❌ FAILED: {len(failures)} of {passes + len(failures)} checks")
    for f in failures:
        print(f"  ✗ {f}")
else:
    print(f"✅ ALL {passes} GENERATION CHECKS PASSED")
sys.exit(1 if failures else 0)
