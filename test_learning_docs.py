#!/usr/bin/env python3
"""
Checks that keep the learning material honest.

Documentation that teaches a contract must satisfy that contract. The framework
already shipped a `context: fork` example that its own validator would reject
(AGENT_PATTERNS.md), which is the bug this suite is written to catch and keep
caught. A doc example nobody executes is indistinguishable from a correct one.

  C0  every skill-frontmatter example satisfies check_skills()'s own predicates
  C1  every frontmatter key used is a real key
  C3  every internal markdown link resolves
  C4  the decision material is linked from the documents people actually read
  C5  the canonical decision table exists exactly once

Run: python3 test_learning_docs.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

# Reuse the real validator's predicates so the doc check and the live check
# can never drift apart.
from validate_agent_system import _split_tools, _grants_wildcard  # noqa: E402

ERRORS = []
WARNINGS = []


def err(msg):
    ERRORS.append(msg)


def warn(msg):
    WARNINGS.append(msg)


SKIP_DIRS = {'.git', 'archive', 'node_modules', '__pycache__', '.claude-metrics'}


def live_docs():
    """Every markdown file that is not archived."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith('.md'):
                yield os.path.join(dirpath, fn)


def rel(path):
    return os.path.relpath(path, ROOT)


# Documents that teach the contract; their examples are held to it.
CONTRACT_DOCS = ('SYSTEM_GENERATOR_PROMPT.md', 'AGENT_SYSTEM_TEMPLATE.md',
                 'CLAUDE_AGENT_FRAMEWORK.md', 'AGENT_PATTERNS.md')

FENCE = re.compile(r'```[a-zA-Z]*\n(---\n.*?\n---)\s*\n', re.S)


def frontmatter_examples(text):
    """Yield (raw, dict) for every fenced block that opens with a --- block."""
    for m in FENCE.finditer(text):
        raw = m.group(1)
        body = raw.strip().strip('-').strip()
        d = {}
        for line in body.splitlines():
            line = line.rstrip()
            if not line or line.startswith('#') or line.startswith(' '):
                continue
            if ':' in line:
                k, v = line.split(':', 1)
                d[k.strip()] = v.strip()
        if d:
            yield raw, d


# A skill example, as opposed to a subagent example. Subagent frontmatter is
# identified by `model`+`tools`; a skill declares allowed-tools or context.
def is_skill_example(d):
    if 'allowed-tools' in d or 'allowed_tools' in d or 'context' in d:
        return True
    if 'tools' in d and 'model' in d:
        return False  # subagent stub
    return False


def docs_to_scan():
    for name in CONTRACT_DOCS:
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            yield p
    learn = os.path.join(ROOT, 'learn')
    if os.path.isdir(learn):
        for dirpath, dirnames, filenames in os.walk(learn):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if fn.endswith('.md'):
                    yield os.path.join(dirpath, fn)


# === C0: skill frontmatter examples satisfy the real predicates ===
c0 = 0
for path in docs_to_scan():
    text = open(path, encoding='utf-8').read()
    for raw, d in frontmatter_examples(text):
        if not is_skill_example(d):
            continue
        c0 += 1
        where = rel(path)
        if 'allowed_tools' in d:
            err(f"{where}: skill example uses `allowed_tools` (underscore). "
                f"Frontmatter uses `allowed-tools`; the underscore form is the registry spelling.")
        if not d.get('description'):
            err(f"{where}: skill example has no `description` - "
                f"check_skills() rejects a command file without one.")
        raw_tools = d.get('allowed-tools')
        if not raw_tools:
            err(f"{where}: skill example has no `allowed-tools` - "
                f"every tool use would prompt, or be denied in a non-interactive run.")
        else:
            for t in _split_tools(raw_tools):
                if _grants_wildcard(t):
                    err(f"{where}: skill example grants unrestricted '{t}'.")
print(f"✓ C0: {c0} skill frontmatter examples checked")

# === C1: every frontmatter key is real ===
# Pinned from code.claude.com/docs/en/skills and /sub-agents.
SKILL_KEYS = {
    'name', 'description', 'when_to_use', 'argument-hint', 'arguments',
    'disable-model-invocation', 'user-invocable', 'allowed-tools',
    'disallowed-tools', 'model', 'effort', 'context', 'agent', 'background',
    'hooks', 'paths', 'shell', 'metadata', 'license', 'compatibility',
}
SUBAGENT_KEYS = {
    'name', 'description', 'tools', 'disallowedTools', 'model', 'permissionMode',
    'maxTurns', 'skills', 'mcpServers', 'hooks', 'memory', 'background', 'effort',
    'isolation', 'color', 'initialPrompt', 'experimental',
}
c1 = 0
for path in docs_to_scan():
    text = open(path, encoding='utf-8').read()
    for raw, d in frontmatter_examples(text):
        allowed = SKILL_KEYS if is_skill_example(d) else SKILL_KEYS | SUBAGENT_KEYS
        for k in d:
            c1 += 1
            if k not in allowed:
                err(f"{rel(path)}: frontmatter key `{k}` is not a documented key.")
print(f"✓ C1: {c1} frontmatter keys checked")

# === C3: internal links resolve ===
LINK = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
c3 = 0
for path in live_docs():
    text = open(path, encoding='utf-8').read()
    for target in LINK.findall(text):
        if target.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        c3 += 1
        clean = target.split('#')[0].strip()
        if not clean:
            continue
        resolved = os.path.normpath(os.path.join(os.path.dirname(path), clean))
        if not os.path.exists(resolved):
            err(f"{rel(path)}: broken link -> {target}")
print(f"✓ C3: {c3} internal links checked")

# === C4: the decision material cannot be orphaned again ===
REQUIRED_LINKS = {
    'learn/01-four-surfaces.md': ('README.md', 'CLAUDE.md', 'CLAUDE_AGENT_FRAMEWORK.md'),
    'learn/README.md': ('README.md',),
}
for target, sources in REQUIRED_LINKS.items():
    if not os.path.exists(os.path.join(ROOT, target)):
        continue  # not written yet
    base = os.path.basename(target)
    for src in sources:
        p = os.path.join(ROOT, src)
        if not os.path.exists(p):
            continue
        if base not in open(p, encoding='utf-8').read():
            err(f"{src} does not link to {target} - "
                f"an orphaned decision table is the bug this check exists for.")
print(f"✓ C4: required inbound links checked")

# === C5: exactly one canonical decision table ===
SENTINEL = 'canonical: surface-decision-table'
hits = [rel(p) for p in live_docs() if SENTINEL in open(p, encoding='utf-8').read()]
if len(hits) > 1:
    err(f"decision table marked canonical in {len(hits)} files: {hits}. "
        f"Two copies drift and readers get different answers.")
elif len(hits) == 1:
    print(f"✓ C5: canonical decision table in {hits[0]}")
else:
    print("✓ C5: no canonical table yet (not written)")

# === C7: skills stay uploadable to claude.ai ===
# The Agent Skills spec subset accepted by claude.ai upload and the Skills API.
# Any other key is a HARD ERROR on upload, not an ignored field:
#   "Unexpected key(s) in SKILL.md frontmatter: argument-hint."
# A skill that only works in Claude Code is a skill most people cannot run.
SPEC_KEYS = {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}
skills_root = os.path.join(ROOT, '.claude/skills')
c7 = 0
if os.path.isdir(skills_root):
    for d in sorted(os.listdir(skills_root)):
        sp = os.path.join(skills_root, d, 'SKILL.md')
        if not os.path.isfile(sp):
            continue
        c7 += 1
        m = re.match(r'^---\n(.*?)\n---', open(sp, encoding='utf-8').read(), re.S)
        if not m:
            err(f".claude/skills/{d}/SKILL.md has no frontmatter")
            continue
        keys = {ln.split(':', 1)[0].strip() for ln in m.group(1).splitlines()
                if ln and not ln.startswith((' ', '-', '#')) and ':' in ln}
        for bad in sorted(keys - SPEC_KEYS):
            err(f".claude/skills/{d}/SKILL.md: `{bad}` is not an Agent Skills spec field - "
                f"uploading this skill to claude.ai fails with a hard error")
print(f"✓ C7: {c7} skills checked for claude.ai portability")

# === C8: no real home directories in a public repo ===
# Two problems when one leaks: it publishes whoever authored the line, and it is
# wrong for every other reader - it points at a machine nobody else has. These are
# agent playbooks, so an agent following one tries to read a path that is not there.
PLACEHOLDER_USERS = {'dev', 'you', 'user', 'me', 'username', 'someone'}
HOME_PATH = re.compile(r'/(?:Users|home)/([A-Za-z0-9_.-]+)')
c8 = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        if not fn.endswith(('.md', '.py', '.sh', '.json')):
            continue
        fp = os.path.join(dirpath, fn)
        try:
            text = open(fp, encoding='utf-8').read()
        except (UnicodeDecodeError, OSError):
            continue
        for user in set(HOME_PATH.findall(text)):
            c8 += 1
            if user not in PLACEHOLDER_USERS:
                err(f"{rel(fp)}: hardcoded home directory /Users/{user}/ - "
                    f"publishes an author and points at a machine no reader has. "
                    f"Use /absolute/path/to/... instead.")
print(f"✓ C8: {c8} home-directory references checked")

# === report ===
print()
for w in WARNINGS:
    print(f"  ⚠ {w}")
if ERRORS:
    print(f"\n{'=' * 60}")
    for e in ERRORS:
        print(f"  ✗ {e}")
    print(f"\n❌ {len(ERRORS)} error(s)")
    sys.exit(1)
print(f"{'=' * 60}\n✅ Learning docs OK")
