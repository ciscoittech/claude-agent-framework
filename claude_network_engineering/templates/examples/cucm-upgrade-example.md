# CUCM Upgrade Project Example

## Real-World Usage: CUCM 14.0.1 Upgrade

This demonstrates how to use the smart documentation fetcher for your Cisco voice upgrade project.

### Document Analysis Results

**Target Document**: CUCM Upgrade and Migration Guide 14.0.1
**Total Size**: 2.83 MB (too large for context)
**Structure**: Well-organized by upgrade phases

### Available Sections:
1. **Upgrade Planning** - Overview and preparation
2. **Upgrade Tasks** - Step-by-step execution procedures
3. **Pre-Upgrade Tasks (Manual Process)** - Prerequisites and preparation
4. **Post-Upgrade Tasks (Manual Process)** - Validation and verification
5. **Change Virtualization Software** - VM/hardware considerations
6. **Sequencing Rules and Time Requirements** - Timing and dependencies
7. **Upgrading from Legacy Releases** - Special migration scenarios
8. **Troubleshooting** - Common issues and solutions
9. **Frequently Asked Questions** - Quick reference

## Smart Loading by Project Phase

### Phase 1: Planning (Load ~15KB)
```bash
claude> load-cisco-docs "https://www.cisco.com/c/en/us/td/docs/voice_ip_comm/cucm/upgrade/14_0_1/cucm_b_upgrade-and-migration-guide_14.html" --project="CUCM upgrade planning" --sections="upgrade-planning,sequencing-rules"
```

**Recommended for Planning:**
- ✅ Upgrade Planning
- ✅ Sequencing Rules and Time Requirements
- ✅ Pre-Upgrade Tasks (Manual Process)
- ❌ Skip: Detailed execution steps (save for later)

### Phase 2: Execution (Load ~20KB)
```bash
claude> load-cisco-docs "https://cisco.com/cucm/upgrade/guide" --project="CUCM upgrade execution" --sections="upgrade-tasks,pre-upgrade-manual"
```

**Recommended for Execution:**
- ✅ Upgrade Tasks
- ✅ Pre-Upgrade Tasks (Manual Process)
- ✅ Change Virtualization Software (if applicable)
- ❌ Skip: Planning sections (already loaded)

### Phase 3: Validation (Load ~12KB)
```bash
claude> load-cisco-docs "https://cisco.com/cucm/upgrade/guide" --project="CUCM post-upgrade validation" --sections="post-upgrade-tasks,troubleshooting"
```

**Recommended for Validation:**
- ✅ Post-Upgrade Tasks (Manual Process)
- ✅ Troubleshooting
- ✅ Frequently Asked Questions
- ❌ Skip: Installation procedures (already complete)

## Interactive Session Example

```bash
claude> I'm working on a CUCM upgrade from 12.5 to 14.0.1. Can you help me load the relevant planning documentation?

# Claude responds:
📖 Document: CUCM Upgrade and Migration Guide 14.0.1
📊 Full document: 2.83 MB (too large for context)
🎯 Your project: CUCM upgrade from 12.5 to 14.0.1

📋 Recommended sections for planning phase:
  1. Upgrade Planning (est. 8KB)
  2. Sequencing Rules and Time Requirements (est. 4KB)
  3. Pre-Upgrade Tasks Manual Process (est. 6KB)

🔍 Other available sections:
  4. Upgrade Tasks (est. 25KB) - Save for execution phase?
  5. Troubleshooting (est. 8KB) - Save for later?
  6. Upgrading from Legacy Releases (est. 5KB) - Relevant for 12.5?

Which sections should I load? (1,2,3,6 recommended for your planning phase)
```

## Project-Specific Questions

The system asks smart questions to filter content:

### For Voice Upgrades:
- Current CUCM version?
- Cluster size (single/multi-node)?
- VM or hardware deployment?
- Upgrade phase (planning/execution/validation)?
- Any integration with other UC apps?

### Content Filtering Based on Answers:

**Single Node** → Skip: Sequencing rules, multi-node procedures
**Hardware** → Skip: Virtualization software changes
**Planning Phase** → Skip: Detailed execution steps
**Legacy Version** → Include: Special migration procedures

## Caching Strategy

```bash
# Content gets cached by project context:
cisco_docs_cache/
├── cucm_14_upgrade_planning_20250927.json
├── cucm_14_upgrade_execution_20250927.json
└── cucm_14_upgrade_validation_20250927.json

# Quick access later:
claude> load-cached-doc "cucm_14_upgrade_planning_20250927.json"
```

## Benefits for Your Project

1. **Context Efficiency**: Load only 15KB instead of 2.83MB
2. **Phase-Appropriate**: Get exactly what you need for current work
3. **Reusability**: Cache content for team sharing
4. **Smart Filtering**: Skip irrelevant sections automatically
5. **Safety**: Never hit context limits

## Command Variations

```bash
# Quick analysis without loading
claude> analyze-cisco-doc "https://cisco.com/cucm/upgrade/guide"

# Load specific sections directly
claude> load-cisco-docs "url" --sections="planning,prerequisites" --no-interactive

# Interactive mode with project context
claude> load-cisco-docs "url" --project="4-node CUCM cluster upgrade" --interactive

# Troubleshooting mode
claude> load-cisco-docs "url" --project="CUCM upgrade issues" --focus="troubleshooting"
```

This approach ensures you get exactly the Cisco documentation you need for your current task, without overwhelming the context with irrelevant information.