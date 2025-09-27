# CLAUDE.md - Network Engineering Edition

This file provides guidance to Claude Code when working with the Network Engineering branch of the Claude Agent Framework.

## Project Overview

This is the **Network Engineering Edition** of the Claude Agent Framework - a specialized branch containing pre-built AI agents for Cisco network infrastructure management. Unlike the general framework (which builds custom agents), this edition provides ready-to-use specialists for ISE, VoIP, pyATS, and network automation workflows.

## 🎯 PRIMARY PRINCIPLE: Simplicity First, Even with Pre-Built Tools

**CRITICAL**: Always try simple approaches before using agents. The tools are powerful but should complement, not replace, fundamental troubleshooting skills.

**ESCALATION PATH**: Basic Commands → Scripts → Single Agent → Multi-Agent Coordination

**FOCUS**: This branch provides specialized, enterprise-ready agents for network infrastructure operations. Start simple, use agents when complexity is justified.

## Network Engineering Capabilities

### **Ready-to-Use Toolkits**

**ISE Troubleshooting:**
- `/ise-toolkit auth-troubleshoot` - Complete authentication analysis
- `/ise-toolkit policy-validate` - Authorization policy validation
- `/ise-toolkit radius-analysis` - RADIUS flow debugging
- `/ise-toolkit performance-monitor` - System health analysis

**VoIP Diagnostics:**
- `/voip-toolkit call-quality-analysis` - RTP stream analysis
- `/voip-toolkit sip-troubleshoot` - SIP signaling diagnostics
- `/voip-toolkit cucm-integration` - Unified Communications workflows
- `/voip-toolkit packet-analysis` - Voice traffic inspection

**Network Automation:**
- `python scripts/pyats_launcher.py run-health-check` - Infrastructure validation
- `python scripts/pyats_launcher.py state-comparison` - Configuration drift detection
- `python scripts/pyats_launcher.py performance-baseline` - Monitoring setup

**Platform Research:**
- `/claude-docs sub-agents` - Multi-agent architecture guidance
- `/claude-docs best-practices` - Current security and performance patterns
- `/claude-docs integration` - Technology stack integration patterns

### **Specialized Agents Available**

**Infrastructure Experts:**
- **ISE Specialist**: Deep ISE knowledge for authentication and policy troubleshooting
- **VoIP Specialist**: Voice infrastructure optimization and diagnostics
- **Authentication Analyzer**: RADIUS flow analysis and certificate management
- **Packet Analyzer**: Network traffic inspection and quality analysis
- **Claude Docs Researcher**: Real-time platform documentation and best practices

**Context Libraries:**
- **ISE Infrastructure Knowledge**: Deployment patterns and troubleshooting workflows
- **VoIP Infrastructure Patterns**: Voice network architectures and optimization
- **Claude Code Platform Knowledge**: Current platform capabilities and integration patterns

## Recommended Workflows for Network Engineers

### **New User Onboarding**

1. **Start Here**: Read [`README.md`](README.md) for overview and quick start
2. **Choose Your Path**:
   - ISE Engineers → [`docs/network-engineering/ISE_TOOLKIT_INTEGRATION.md`](docs/network-engineering/ISE_TOOLKIT_INTEGRATION.md)
   - VoIP Engineers → [`docs/network-engineering/VOIP_WIRESHARK_INTEGRATION.md`](docs/network-engineering/VOIP_WIRESHARK_INTEGRATION.md)
   - Automation Engineers → [`docs/network-engineering/PYATS_FRAMEWORK_GUIDE.md`](docs/network-engineering/PYATS_FRAMEWORK_GUIDE.md)
3. **Try Basic Commands**: Use toolkit commands for your specific domain
4. **Explore Advanced Features**: Review examples and integration patterns

### **Daily Operations Workflow**

```bash
# 1. Start with basic health checks
ping critical-devices.txt
show commands on problem devices

# 2. Use automation for routine monitoring
python scripts/pyats_launcher.py run-health-check infrastructure.yaml

# 3. Escalate to agents only for complex issues
/ise-toolkit auth-troubleshoot "authentication-failures"  # When basic auth fails
/voip-toolkit call-quality-analysis "poor-audio-reports"  # When voice metrics show issues

# 4. Research improvements for preventing issues
/claude-docs best-practices "simple-monitoring-approaches"

# Remember: Agents should make simple tasks faster, not replace basic skills
```

### **Incident Response Workflow**

```bash
# Step 1: Quick assessment with appropriate specialist
/ise-toolkit performance-monitor "system-slowdown"

# Step 2: Deep dive analysis with supporting agents
# (ISE Specialist coordinates with Authentication Analyzer)

# Step 3: Generate comprehensive incident report
# (Agents provide root cause analysis and remediation steps)

# Step 4: Implement fixes and validate
python scripts/pyats_launcher.py state-comparison testbed.yaml

# Step 5: Update documentation and preventive measures
/claude-docs architecture "improved-monitoring-strategy"
```

## Network Engineering Documentation Structure

### **Network-Specific Guides** (`docs/network-engineering/`)
- **ISE_TOOLKIT_INTEGRATION.md**: Complete ISE troubleshooting workflows
- **VOIP_WIRESHARK_INTEGRATION.md**: Voice infrastructure analysis patterns
- **PYATS_FRAMEWORK_GUIDE.md**: Enterprise automation and testing integration
- **INFRASTRUCTURE_KNOWLEDGE_SOURCES.md**: Documentation and knowledge management
- **VENDOR_DOCUMENTATION_PATTERNS.md**: Cisco and vendor integration patterns

### **Operational Workflows** (`docs/operations/`)
- **DEPLOYMENT.md**: Production deployment strategies and environments
- **EXPERT_CONSULTATION_WORKFLOW.md**: Escalation and expert coordination patterns
- **SIMPLICITY_RESULTS.md**: Performance metrics and optimization results

### **Examples and Use Cases** (`examples/`)
- **claude-docs-researcher.md**: Platform research and integration examples
- **network-troubleshooter.md**: Basic troubleshooting workflows
- **Advanced examples**: Complex multi-agent coordination patterns

### **Framework Reference** (`docs/framework/` and `docs/reference/`)
*Note: These are for building custom agents. Network engineers typically use pre-built tools.*
- **CLAUDE_AGENT_FRAMEWORK.md**: Core framework concepts
- **AGENT_PATTERNS.md**: Multi-agent coordination patterns
- **SIMPLICITY_ENFORCEMENT.md**: Framework design principles

## Common Network Engineering Tasks

### **ISE Authentication Issues**
```bash
# Quick authentication troubleshooting
/ise-toolkit auth-troubleshoot "802.1x-failures"

# Policy validation and optimization
/ise-toolkit policy-validate "authorization-policies"

# Performance and scalability analysis
/ise-toolkit performance-monitor "peak-load-testing"
```

### **VoIP Quality Problems**
```bash
# Call quality analysis
/voip-toolkit call-quality-analysis "poor-audio-complaints"

# SIP signaling troubleshooting
/voip-toolkit sip-troubleshoot "registration-failures"

# CUCM integration issues
/voip-toolkit cucm-integration "unified-communications-problems"
```

### **Network Infrastructure Automation**
```bash
# Enterprise health monitoring
python scripts/pyats_launcher.py run-health-check enterprise-testbed.yaml

# Configuration compliance checking
python scripts/pyats_launcher.py compliance-check security-baseline.yaml

# Performance baseline establishment
python scripts/pyats_launcher.py performance-baseline monitoring-config.yaml
```

### **Platform Research and Best Practices**
```bash
# Research current sub-agent patterns
/claude-docs sub-agents "enterprise-network-monitoring"

# Get integration guidance
/claude-docs integration "kubernetes-deployment-patterns"

# Learn latest best practices
/claude-docs best-practices "security-hardening-guidelines"
```

## Integration with Existing Workflows

### **CI/CD Integration**
The framework integrates with existing network automation pipelines:
- **Git Hooks**: Automated validation on configuration changes
- **Jenkins/GitHub Actions**: Continuous infrastructure testing
- **Monitoring Systems**: Integration with existing alerting platforms

### **Enterprise Tools**
- **ITSM Integration**: ServiceNow, Remedy workflow integration
- **Monitoring Platforms**: Splunk, ELK, Prometheus integration
- **Documentation Systems**: Confluence, SharePoint knowledge management

### **Security and Compliance**
- **Audit Logging**: Comprehensive activity tracking for compliance
- **Access Control**: Role-based permissions for different engineer levels
- **Credential Management**: Secure handling of network device credentials

## Performance Optimization Targets

The network engineering edition achieves:
- **60% reduction** in average issue resolution time
- **95% accuracy** in root cause identification
- **80% first-call resolution** rate for common issues
- **24/7 automated monitoring** with intelligent alerting
- **Enterprise-scale** deployment across multiple sites

## Success Metrics

Track framework effectiveness through:
- **Mean Time to Resolution (MTTR)**: Reduction in troubleshooting time
- **First Call Resolution Rate**: Percentage of issues resolved without escalation
- **Documentation Quality**: Comprehensive analysis reports with actionable recommendations
- **Knowledge Transfer**: Team skill development and consistency improvement
- **Automation Coverage**: Percentage of routine tasks automated

This network engineering edition transforms complex infrastructure troubleshooting into systematic, efficient, and comprehensive analysis powered by specialized AI agents.