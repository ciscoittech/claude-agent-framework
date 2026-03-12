# Agent Skills - Quick Reference Guide

## What Are Agent Skills?
Modular, packaged capabilities that extend Claude with domain expertise. Skills use progressive disclosure to minimize context overhead.

## Basic Structure
```
skill-name/
├── SKILL.md              # Required: metadata + instructions
├── REFERENCE.md          # Optional: detailed reference
├── templates/
├── scripts/              # Python/bash executable code
└── examples/
```

## SKILL.md Template
```yaml
---
name: "Display Name (max 64 chars)"
description: "What this skill does (max 200 chars, critical for Claude to know when to use)"
---

# Your Skill Name

## Overview
Clear explanation of what this skill does and when to use it.

## How to Use
Step-by-step instructions for Claude.

## Examples
Concrete examples of using this skill.
```

## Pre-built Skills (Anthropic)
- **pptx** - Create and edit PowerPoint presentations
- **xlsx** - Create spreadsheets with formulas and charts
- **docx** - Create professional Word documents
- **pdf** - Generate formatted PDF reports

## Progressive Disclosure Architecture
```
1. YAML Frontmatter (30-50 words)
   ↓ Claude reads at startup - decides if skill needed

2. SKILL.md Body (main instructions)
   ↓ Claude loads if skill is relevant

3. REFERENCE.md + Scripts (detailed info)
   ↓ Claude loads only when specific details needed
```

**Benefit**: 70-90% reduction in unnecessary context

## API Usage
```json
{
  "container": {
    "type": "skills",
    "skills": [
      {
        "type": "anthropic",
        "skill_id": "pptx",
        "version": "latest"
      },
      {
        "type": "custom",
        "skill_id": "my-skill",
        "version": "1.0"
      }
    ]
  }
}
```

**Limit**: Up to 8 skills per API request

## Key Limitations
❌ Cannot make external API calls
❌ Cannot install new packages
❌ Limited network access
✅ Only pre-installed packages available

## Best Practices

### 1. Clear Descriptions
- **Vague**: "Data processing" ❌
- **Clear**: "Convert CSV to financial spreadsheet with formulas and charts" ✅

### 2. Iterative Testing
- Create skill with Claude A
- Test with Claude B in real tasks
- Observe actual usage patterns
- Iterate based on real-world behavior

### 3. Progressive Disclosure
- Minimize initial context (YAML only ~30-50 words)
- Organize complex content into REFERENCE.md
- Let Claude load details as needed

### 4. Single-Purpose Skills
- Focus each skill on one domain
- Build composability through clarity
- Easier to test, maintain, and update

## Integration Points with Claude Agent Framework

### Current State
- Agents in `.claude/agents/` with JSON configs
- SYSTEM_GENERATOR_PROMPT auto-generates configs

### Opportunities
1. **Skills as Agent Templates**: Convert popular patterns to reusable skills
2. **Framework Self-Improvement**: Create framework-specific skills
3. **Simplicity Enforcement**: Package circuit breakers as a skill
4. **System Generation**: Convert SYSTEM_GENERATOR_PROMPT to skill
5. **Portability**: Skills are more shareable across projects/teams

## Skill Size Guidelines

| Category | Tokens | When to Use |
|----------|--------|---|
| Lightweight | <3K | Simple, focused tasks |
| Medium | 10-15K | Complex workflows |
| Heavy | 25K+ | Enterprise, specialized |

## How Skills Compare to Alternatives

| Aspect | Skills | Agents | MCP Servers |
|--------|--------|--------|---|
| **Scope** | Single capability | Multi-tool system | External services |
| **Context Load** | Progressive | Upfront | Lazy via function calls |
| **Composability** | High | High | Via Claude |
| **Network** | ❌ None | ✅ Via agents | ✅ Full access |
| **Packages** | Pre-installed only | ✅ Full Python | ✅ Full Python |
| **Setup Time** | 5-10 min | 30-60 min | 20-40 min |

## Creating a Custom Skill: 5-Minute Steps

1. **Create folder**:
   ```bash
   mkdir my-skill && cd my-skill
   ```

2. **Create SKILL.md**:
   ```yaml
   ---
   name: "My Skill"
   description: "Clear description of what it does"
   ---
   # My Skill
   Instructions here...
   ```

3. **Add optional files**:
   - REFERENCE.md for detailed docs
   - scripts/ for Python/bash code
   - templates/ for examples

4. **Upload to Claude**:
   - In Claude.ai: Click "Upload skill" and upload ZIP
   - Via API: POST to /v1/skills with skill folder

5. **Test in conversation**:
   - Request a task that would use the skill
   - Claude auto-invokes when needed

## File Handling in Skills

When skills create documents (Excel, PowerPoint, PDF, Word):
- Response includes `file_id` attribute
- Must use Files API to download
- Each skill returns files in its own format

## Real-World Examples

### Example 1: Financial Report Skill
- Input: CSV data, company info
- Process: Create Excel model + PowerPoint slides + PDF summary
- Output: Three files ready for distribution

### Example 2: Code Review Skill
- Input: Code files, review criteria
- Process: Analyze code against patterns
- Output: Structured review recommendations

### Example 3: Documentation Skill
- Input: Code and API specs
- Process: Generate formatted documentation
- Output: Word document + PDF

## When to Use Skills vs Other Approaches

**Use Skills when**:
- ✅ Creating reusable organizational capabilities
- ✅ Packaging domain expertise
- ✅ Building document generation workflows
- ✅ Want automatic invocation based on context

**Use Agents instead when**:
- ✅ Need external API access
- ✅ Require package installation
- ✅ Complex multi-step orchestration
- ✅ Need extensive tool ecosystem

**Use MCP Servers instead when**:
- ✅ Need persistent external services
- ✅ Building ecosystem of tools
- ✅ Network access required
- ✅ Long-lived connections needed

---

**Created**: October 18, 2025
**Branch**: `explore/agent-skills`
