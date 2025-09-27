# 📖 Documentation Navigation Guide

> **Quick reference for navigating the Network Engineering Edition documentation**

## 🎯 **Start Here Based on Your Role**

### **New to the Framework**
1. **[`README.md`](../README.md)** - Overview and 30-second setup
2. **[`docs/SIMPLICITY_GUIDE.md`](SIMPLICITY_GUIDE.md)** - ⚠️ **READ THIS FIRST**: Simplicity principles
3. **[`CLAUDE.md`](../CLAUDE.md)** - Detailed workflow guidance
4. **Choose your specialization path below** ⬇️

### **ISE Engineers**
```
📍 Start Here:
├── docs/network-engineering/ISE_TOOLKIT_INTEGRATION.md
├── examples/ise-sample-data/
└── Try: /ise-toolkit auth-troubleshoot "your-issue"
```

### **VoIP Engineers**
```
📍 Start Here:
├── docs/network-engineering/VOIP_WIRESHARK_INTEGRATION.md
├── examples/cucm-upgrade-example.md
└── Try: /voip-toolkit call-quality-analysis "audio-issue"
```

### **Network Automation Engineers**
```
📍 Start Here:
├── docs/network-engineering/PYATS_FRAMEWORK_GUIDE.md
├── examples/pyats-simple.md
└── Try: python scripts/pyats_launcher.py run-health-check testbed.yaml
```

### **Framework Developers** (Building Custom Agents)
```
📍 Start Here:
├── docs/framework/SIMPLICITY_ENFORCEMENT.md
├── docs/framework/SYSTEM_GENERATOR_PROMPT.md
└── docs/framework/CLAUDE_AGENT_FRAMEWORK.md
```

---

## 📂 **Documentation Categories**

### **🚀 Quick Start & Operations**
| Document | Purpose | Time to Read |
|----------|---------|--------------|
| [`README.md`](../README.md) | Project overview and setup | 5 minutes |
| [`CLAUDE.md`](../CLAUDE.md) | Detailed workflow guidance | 10 minutes |
| [`SIMPLICITY_GUIDE.md`](SIMPLICITY_GUIDE.md) | **START HERE**: Simplicity first principles | 10 minutes |
| [`docs/operations/DEPLOYMENT.md`](operations/DEPLOYMENT.md) | Production deployment | 15 minutes |

### **🔧 Network Engineering Guides**
| Document | Specialization | Complexity |
|----------|---------------|------------|
| [`ISE_TOOLKIT_INTEGRATION.md`](network-engineering/ISE_TOOLKIT_INTEGRATION.md) | ISE Authentication | Advanced |
| [`VOIP_WIRESHARK_INTEGRATION.md`](network-engineering/VOIP_WIRESHARK_INTEGRATION.md) | Voice Infrastructure | Advanced |
| [`PYATS_FRAMEWORK_GUIDE.md`](network-engineering/PYATS_FRAMEWORK_GUIDE.md) | Network Automation | Intermediate |
| [`INFRASTRUCTURE_KNOWLEDGE_SOURCES.md`](network-engineering/INFRASTRUCTURE_KNOWLEDGE_SOURCES.md) | Documentation | Basic |
| [`VENDOR_DOCUMENTATION_PATTERNS.md`](network-engineering/VENDOR_DOCUMENTATION_PATTERNS.md) | Integration | Intermediate |

### **⚙️ Operational Workflows**
| Document | Focus | Audience |
|----------|-------|----------|
| [`DEPLOYMENT.md`](operations/DEPLOYMENT.md) | Production setup | DevOps/SRE |
| [`EXPERT_CONSULTATION_WORKFLOW.md`](operations/EXPERT_CONSULTATION_WORKFLOW.md) | Escalation processes | Team Leads |
| [`SIMPLICITY_RESULTS.md`](operations/SIMPLICITY_RESULTS.md) | Performance metrics | Management |

### **🎓 Examples & Use Cases**
| Document | Complexity | Best For |
|----------|------------|----------|
| [`claude-docs-researcher.md`](../examples/claude-docs-researcher.md) | Basic | Platform research |
| [`network-troubleshooter.md`](../examples/network-troubleshooter.md) | Basic | General troubleshooting |
| [`automation-engineer.md`](../examples/automation-engineer.md) | Intermediate | Workflow automation |
| [`security-engineer.md`](../examples/security-engineer.md) | Advanced | Security operations |

### **📚 Framework Reference** (For Custom Development)
| Document | Purpose | When to Read |
|----------|---------|--------------|
| [`CLAUDE_AGENT_FRAMEWORK.md`](framework/CLAUDE_AGENT_FRAMEWORK.md) | Core concepts | Building custom agents |
| [`AGENT_PATTERNS.md`](framework/AGENT_PATTERNS.md) | Implementation patterns | Advanced customization |
| [`SIMPLICITY_ENFORCEMENT.md`](framework/SIMPLICITY_ENFORCEMENT.md) | Design principles | Understanding philosophy |
| [`SYSTEM_GENERATOR_PROMPT.md`](framework/SYSTEM_GENERATOR_PROMPT.md) | Auto-generation | Creating new systems |

---

## 🗺️ **Common Learning Paths**

### **Path 1: Network Operations Center (NOC) Engineer**
```
1. README.md (Overview)
2. SIMPLICITY_GUIDE.md (⚠️ Essential: Start simple first)
3. CLAUDE.md (Workflows)
4. ISE_TOOLKIT_INTEGRATION.md (ISE troubleshooting)
5. PYATS_FRAMEWORK_GUIDE.md (Automation)
6. EXPERT_CONSULTATION_WORKFLOW.md (Escalation)
```

### **Path 2: Voice/UC Engineer**
```
1. README.md (Overview)
2. VOIP_WIRESHARK_INTEGRATION.md (Voice analysis)
3. examples/cucm-upgrade-example.md (Practical example)
4. DEPLOYMENT.md (Production setup)
```

### **Path 3: Network Security Engineer**
```
1. README.md (Overview)
2. ISE_TOOLKIT_INTEGRATION.md (Authentication security)
3. examples/security-engineer.md (Security workflows)
4. EXPERT_CONSULTATION_WORKFLOW.md (Security escalation)
```

### **Path 4: Network Automation Developer**
```
1. README.md (Overview)
2. PYATS_FRAMEWORK_GUIDE.md (Automation framework)
3. docs/framework/AGENT_PATTERNS.md (Agent coordination)
4. examples/automation-engineer.md (Implementation examples)
```

### **Path 5: Team Lead/Architect**
```
1. README.md (Overview)
2. SIMPLICITY_RESULTS.md (Performance metrics)
3. DEPLOYMENT.md (Enterprise deployment)
4. EXPERT_CONSULTATION_WORKFLOW.md (Team processes)
5. docs/framework/CLAUDE_AGENT_FRAMEWORK.md (Architecture)
```

---

## 🔍 **Quick Reference Commands**

### **Daily Operations**
```bash
# Infrastructure health check
python scripts/pyats_launcher.py run-health-check infrastructure.yaml

# ISE authentication troubleshooting
/ise-toolkit auth-troubleshoot "authentication-issue"

# VoIP quality analysis
/voip-toolkit call-quality-analysis "call-quality-issue"

# Research platform best practices
/claude-docs best-practices "topic"
```

### **Setup & Configuration**
```bash
# Initial setup
./scripts/setup.sh

# Production deployment
docker-compose -f infrastructure/docker-compose.yml up -d

# Development environment
claude-code
```

---

## ❓ **Help & Support**

### **Getting Help**
- **Documentation Issues**: Check this navigation guide
- **Tool Problems**: Refer to specific toolkit integration guides
- **Advanced Usage**: Review framework reference documentation
- **Best Practices**: Use `/claude-docs` command for latest guidance

### **Troubleshooting Navigation**
- **Can't find what you need?** Check the examples directory for similar use cases
- **Tool not working?** Review the deployment documentation
- **Need custom agents?** Refer to the framework documentation
- **Performance issues?** Check the operations documentation

### **Contributing to Documentation**
- **Improvements**: Submit PRs with documentation enhancements
- **New Examples**: Add real-world use cases to examples directory
- **Integration Guides**: Contribute vendor-specific integration patterns

---

**💡 Pro Tip**: Start with the README.md, then follow the role-specific path that matches your responsibilities. Most network engineers can be productive within 30 minutes by following their specialized path.