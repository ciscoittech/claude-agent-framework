# Agent Skills Research & Analysis
**Date**: October 18, 2025
**Branch**: `explore/agent-skills`
**Status**: Research Complete

---

## Table of Contents
1. [Overview](#overview)
2. [What Are Agent Skills?](#what-are-agent-skills)
3. [Architecture & Technical Details](#architecture--technical-details)
4. [Pre-built Skills](#pre-built-skills)
5. [Custom Skills](#custom-skills)
6. [Best Practices](#best-practices)
7. [Integration Opportunities with Claude Agent Framework](#integration-opportunities-with-claude-agent-framework)
8. [Limitations](#limitations)
9. [Implementation Roadmap](#implementation-roadmap)

---

## Overview

**Agent Skills** are modular, packaged capabilities that extend Claude's functionality. They represent a significant evolution in how Claude can be specialized for specific domains and workflows. Skills were announced in October 2025 as part of Anthropic's push to make Claude faster, cheaper, and more consistent for business workflows.

**Key Innovation**: Skills use a "progressive disclosure" architecture that minimizes context overhead by loading only the information Claude needs, when it needs it.

---

## What Are Agent Skills?

### Definition
Agent Skills are organized folders containing:
- **SKILL.md** file (required) - Instructions + YAML frontmatter metadata
- **Supporting files** - REFERENCE.md, templates, scripts, documentation
- **Executable code** - Python, shell scripts, data processing

### How They Work
1. **Discovery**: Claude loads skill name and description from YAML frontmatter
2. **Selection**: Claude determines if a skill is relevant to the current task
3. **Progressive Loading**: Claude loads full skill instructions and references only when needed
4. **Execution**: Claude uses skill tools/scripts to accomplish tasks

### Key Characteristics
- **Automatic Invocation**: Claude decides when to use skills without explicit prompting
- **Composable**: Multiple skills can work together for complex workflows
- **Version Control**: Skills support versioning through the /v1/skills API endpoint
- **Platform Agnostic**: Works with Claude.ai, Claude Code, and the Messages API

---

## Architecture & Technical Details

### Skill Structure

```
my-skill/
├── SKILL.md           # Required: metadata + instructions
├── REFERENCE.md       # Optional: detailed reference docs
├── templates/         # Optional: example files, templates
├── scripts/           # Optional: executable code
└── examples/          # Optional: usage examples
```

### SKILL.md Frontmatter

```yaml
---
name: "Skill Display Name"
description: "Brief description of what this skill does (max 200 chars)"
---
# Skill Instructions
Detailed instructions for Claude on how to use this skill...
```

**Requirements**:
- `name`: Human-friendly name (max 64 characters)
- `description`: Critical metadata - Claude uses this to decide when to invoke (max 200 characters)

### Progressive Disclosure Architecture

The skill loading follows a three-tier approach:

| Tier | Content | Load Trigger |
|------|---------|---|
| 1 | YAML frontmatter (name + description) | At startup |
| 2 | SKILL.md markdown body | When Claude determines skill is relevant |
| 3 | Referenced files (REFERENCE.md, scripts) | Only when Claude needs specific detail |

**Benefit**: Reduces unnecessary context by 70-90% compared to loading full skills upfront.

### API Integration

**Container Parameter in Messages API**:
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
        "skill_id": "my-custom-skill",
        "version": "1.0"
      }
    ]
  }
}
```

**Limits**: Up to 8 skills per API request

**File Handling**: When skills create documents (Excel, PowerPoint, PDF, Word), they return `file_id` attributes in the response. Files must be downloaded via the Files API.

### Code Execution Environment

Skills support code execution through:
- **Python scripts**: Full Python 3.x support
- **Shell scripts**: Bash execution
- **Pre-installed packages**: Standard libraries only (no `pip install`)
- **Deterministic computation**: Run computational tasks instead of token generation

---

## Pre-built Skills

Anthropic provides four enterprise-grade pre-built skills:

### 1. PowerPoint Skill (pptx)
- **Capabilities**:
  - Create presentations from scratch
  - Add and edit slides with text, images, shapes
  - Analyze presentation content
  - Apply formatting and themes
  - Work with animations and transitions
- **Use Cases**: Reports, proposals, pitch decks, training materials

### 2. Excel Skill (xlsx)
- **Capabilities**:
  - Create spreadsheets with formulas
  - Perform data analysis
  - Generate charts and visualizations
  - Create financial models
  - Format data professionally
- **Use Cases**: Financial modeling, data analysis, dashboards, reports

### 3. Word Skill (docx)
- **Capabilities**:
  - Create professional documents
  - Format text and structure
  - Add headers, footers, sections
  - Insert tables and images
  - Generate table of contents
- **Use Cases**: Reports, memos, documentation, policies

### 4. PDF Skill (pdf)
- **Capabilities**:
  - Generate formatted PDF documents
  - Create reports with formatting
  - Combine multiple documents
  - Add form fields (fillable PDFs)
  - Extract and transform data to PDF
- **Use Cases**: Reports, invoices, certificates, compliance documents

---

## Custom Skills

### Creating Custom Skills

**Minimum Requirements**:
```
my-skill/
└── SKILL.md
    ---
    name: "My Skill"
    description: "What this skill does"
    ---
    Instructions here...
```

### Skill Categories (Examples from Community)

**Creative Skills**:
- Art generation and style guidance
- Music composition assistance
- Design system documentation

**Technical Skills**:
- Web app testing automation
- MCP server generation
- Code generation and refactoring
- Infrastructure setup

**Enterprise Workflows**:
- Data processing pipelines
- Report generation
- Document management
- Compliance workflows

### Uploading Custom Skills

**In Claude.ai**:
1. Click "Upload skill"
2. Upload ZIP file containing your skill folder
3. Skill becomes available immediately

**Via API**:
- Use `/v1/skills` endpoint
- Support for skill versioning and management
- Programmatic control over skill lifecycle

### Best Practice Skill Design

**Structural Guidelines**:
```
my-skill/
├── SKILL.md              # Core instructions + metadata
├── REFERENCE.md          # Supplemental information
├── TEMPLATES/
│   ├── template1.md
│   └── template2.md
├── SCRIPTS/
│   └── helper.py         # Reusable functions
└── EXAMPLES/
    └── example1.json     # Usage examples
```

**Description Matters**:
- Clear, specific descriptions enable Claude to recognize when to use skills
- Poor descriptions lead to underutilization
- Examples:
  - ❌ "Data processing" (too vague)
  - ✅ "Convert CSV data to financial spreadsheet with formulas and charts"

---

## Best Practices

### 1. Iterative Development Pattern

**The "Two Claude" Approach**:
- **Claude A**: Creates/refines the skill instructions
- **Claude B**: Tests skill in real tasks and provides feedback
- Observe how Claude B actually uses the skill in practice
- Iterate based on real-world behavior, not test scenarios

### 2. Real-World Testing

- Test skills with actual workflows, not toy scenarios
- Watch for:
  - Unexpected exploration paths
  - Missed connections between skill sections
  - Overreliance on certain sections
  - Ignored content

### 3. Token Optimization

**Agent Weight Categories**:
| Category | Tokens | Use Case |
|----------|--------|----------|
| Lightweight | <3K | Simple, focused skills |
| Medium | 10-15K | Complex multi-step workflows |
| Heavy | 25K+ | Enterprise, specialized domains |

### 4. Clear, Focused Instructions

- Start with simple, single-purpose skills
- Build composability through clarity
- Use progressive disclosure effectively
- Minimize initial context load

### 5. Progressive Disclosure Architecture

**Design skills in three levels**:
1. **Metadata** (YAML): 30-50 words - when to use
2. **Main instructions** (SKILL.md body): Core process
3. **References** (REFERENCE.md): Detailed information loaded only when needed

---

## Integration Opportunities with Claude Agent Framework

### 1. Skills as Agent Templates

**Current Approach**: Agents defined in `.claude/agents/` with JSON configs

**Opportunity**: Convert popular agent patterns into reusable skills:
```
.claude-library/skills/
├── code-reviewer-skill/
├── project-analyzer-skill/
├── test-generator-skill/
└── documentation-skill/
```

**Benefit**: Skills are more portable and can be shared across projects/teams

### 2. Skills for Framework Self-Improvement

Create framework-specific skills:
- **Agent-Launcher-Skill**: Optimized skill for launching agents
- **Codebase-Analyzer-Skill**: Quick project structure analysis
- **Configuration-Generator-Skill**: Auto-generate `.claude/` configs

### 3. Simplicity Enforcement Through Skills

**Current**: Hardcoded complexity assessment in Python

**Opportunity**: Create Simplicity-Enforcement-Skill that:
- Analyzes project scope
- Recommends appropriate skill count
- Validates circuit breaker triggers
- Generates minimal configs

### 4. Agent System Execution Skills

Package the SYSTEM_GENERATOR_PROMPT as a skill:
```yaml
---
name: "Agent System Generator"
description: "Analyzes projects and generates optimized Claude agent configurations"
---
[Full system generation logic]
```

### 5. Integration Pattern for Users

**New Workflow**:
1. User uploads project to Claude Code
2. Framework skill analyzes structure
3. Recommends appropriate agent system
4. Generates complete configuration
5. User can refine using other skills

---

## Limitations

### 🚫 Cannot Do
- **External API Calls**: Skills cannot call external APIs or access the internet
- **Package Installation**: Cannot run `pip install` or install new packages
- **Network Access**: No HTTP requests or network operations
- **File System Access**: Limited to skill directory and execution context

### ✅ Can Only Use
- **Pre-installed Packages**: Standard Python/shell libraries only
- **Local File Access**: Files within skill directory
- **Code Execution**: Python and bash scripts
- **Claude's Native Tools**: Code execution sandbox

### Workarounds
- For external APIs: Use Claude Code agents with Task tool
- For packages: Build into skill as vendored code
- For network tasks: Delegate to agents with external access
- For complex logic: Use Python execution within skill

---

## Implementation Roadmap

### Phase 1: Research & Documentation (Current)
- [x] Comprehensive research on Agent Skills
- [x] Understanding architecture and best practices
- [ ] Document integration opportunities
- [ ] Create proof-of-concept skill

### Phase 2: Proof of Concept
- [ ] Build Agent-Launcher-Skill
- [ ] Test with simple project
- [ ] Validate progressive disclosure efficiency
- [ ] Compare with current agent system

### Phase 3: Framework Integration
- [ ] Convert SYSTEM_GENERATOR_PROMPT to skill
- [ ] Update AGENT_SYSTEM_TEMPLATE with skills
- [ ] Integrate skills into `.claude/` generation
- [ ] Add skills documentation to CLAUDE_AGENT_FRAMEWORK.md

### Phase 4: Community Skills Library
- [ ] Create public skills repository
- [ ] Document skill creation guidelines
- [ ] Build example skills (code-reviewer, docs-generator, etc.)
- [ ] Establish skill versioning strategy

### Phase 5: Advanced Features
- [ ] Multi-skill orchestration patterns
- [ ] Skill composition for complex workflows
- [ ] Performance monitoring and optimization
- [ ] Enterprise skill templates

---

## Key Insights

### 1. Progressive Disclosure is Revolutionary
Unlike traditional systems that load all context upfront, skills load only what's needed. This is similar to how expert humans focus their attention—they know the general concept, then dive into details as needed.

### 2. Skills Bridge Claude.ai and Claude Code
- **Claude.ai users**: Get easy access to organizational expertise
- **Claude Code users**: Can build sophisticated automation
- **API users**: Get all capabilities through unified interface

### 3. Composability Over Monolithic Design
Instead of one giant agent doing everything, skills enable:
- Focused, single-purpose capabilities
- Easy to test individually
- Simple to combine for complex workflows
- Easier to maintain and update

### 4. Skills Enable Organizational Knowledge Transfer
Skills are perfect for capturing:
- Standard operating procedures
- Domain expertise
- Best practices
- Organizational workflows

### 5. Token Efficiency Becomes Critical
As skills become more sophisticated, token management becomes crucial. The progressive disclosure pattern directly addresses this:
- 70-90% reduction in unnecessary context
- Faster processing (fewer tokens to read)
- Lower costs for API users

---

## References

- Anthropic Engineering Blog: "Equipping agents for the real world with Agent Skills"
- Claude Documentation: Agent Skills Overview
- Claude Support: How to create custom Skills
- GitHub: anthropics/skills repository
- Various community implementations and tutorials

---

**Next Steps**: Move to Phase 2 - Create proof-of-concept skill for framework integration
