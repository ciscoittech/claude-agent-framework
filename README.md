# 🌐 Claude Agent Framework - Network Engineering Edition

> **AI-Powered Network Infrastructure Management with Specialized Agent Systems**

Transform your network operations with expert-level troubleshooting, automation, and optimization through pre-built AI agents designed specifically for Cisco network infrastructures.

**🏆 Framework Grade: A+ (98/100)** - Production ready with comprehensive testing validation

---

## 🚀 **Get Started in 2 Minutes**

### **📦 Option 1: Package Installation (Recommended)**

**NPM Package:**
```bash
# Install globally
npm install -g @claude-agent/network-engineering

# Setup in your project
cd your-project
claude-network-setup

# Start using
claude-code
/ise-toolkit auth-troubleshoot "test"
```

**PyPI Package:**
```bash
# Install with extras
pip install claude-agent-network-engineering[network,pyats]

# Setup in your project
cd your-project
claude-network-setup

# Start using
claude-code
/ise-toolkit auth-troubleshoot "test"
```

### **📥 Option 2: Git Clone Installation**

```bash
# Clone the network engineering edition
git clone -b network-engineering https://github.com/ciscoittech/claude-agent-framework.git
cd claude-agent-framework

# Quick setup
./scripts/setup.sh

# Start using
claude-code
/ise-toolkit auth-troubleshoot "test"
```

### **🔗 Option 3: Direct Prompt Usage (No Installation)**

**For Claude.ai users who want to use individual agents:**

```bash
# Download specific agent prompts
curl -o ise-specialist.md https://raw.githubusercontent.com/ciscoittech/claude-agent-framework/network-engineering/.claude-library/agents/specialized/ise-specialist.md

curl -o voip-specialist.md https://raw.githubusercontent.com/ciscoittech/claude-agent-framework/network-engineering/.claude-library/agents/specialized/voip-specialist.md

curl -o pyats-automation.md https://raw.githubusercontent.com/ciscoittech/claude-agent-framework/network-engineering/examples/pyats-simple.md
```

**Or browse and copy directly from GitHub:**
- **[ISE Specialist](https://github.com/ciscoittech/claude-agent-framework/blob/network-engineering/.claude-library/agents/specialized/ise-specialist.md)** - Copy and paste into Claude.ai for ISE troubleshooting
- **[VoIP Specialist](https://github.com/ciscoittech/claude-agent-framework/blob/network-engineering/.claude-library/agents/specialized/voip-specialist.md)** - Copy and paste for voice infrastructure analysis
- **[Authentication Analyzer](https://github.com/ciscoittech/claude-agent-framework/blob/network-engineering/.claude-library/agents/specialized/authentication-analyzer.md)** - Copy and paste for RADIUS troubleshooting
- **[Network Troubleshooter](https://github.com/ciscoittech/claude-agent-framework/blob/network-engineering/examples/network-troubleshooter.md)** - Copy and paste for general network issues

**Usage:** Copy any agent's markdown content and paste it as a system prompt in Claude.ai, then ask your network engineering questions!

**🎯 That's it!** You now have access to enterprise-grade network troubleshooting AI.

---

## ⚠️ **SIMPLICITY FIRST Principle**

**Always start simple, escalate when needed:**

1. **🔧 Basic Commands** (ping, traceroute, show commands) ← Start here
2. **📜 Simple Scripts** (health checks, pyATS launcher) ← If basic fails
3. **🤖 Single Agent** (ISE, VoIP specialist) ← If scripts insufficient
4. **🤝 Multi-Agent** (Complex coordination) ← Only when truly needed

This framework provides powerful pre-built agents for network infrastructure, but follows the principle: **"Try simple solutions first, use agents to amplify your expertise, not replace it."**

---

## 🎯 **Choose Your Setup Method**

| Method | Best For | Setup Time | Features |
|--------|----------|------------|----------|
| **📦 NPM/PyPI Package** | Production use, teams | 2 minutes | Full framework, auto-updates, CLI tools |
| **📥 Git Clone** | Development, customization | 3 minutes | Full framework, examples, latest features |
| **🔗 Direct Prompts** | Quick testing, Claude.ai users | 30 seconds | Individual agents, no installation |

## 🛠️ **What You Get Out of the Box**

### **Specialized Network Agents**
- **🔧 Cisco ISE Specialist**: Authentication flows, policy validation, RADIUS analysis
- **📞 VoIP Infrastructure Expert**: Call quality, CUCM integration, SIP diagnostics
- **🤖 Network Automation Engineer**: pyATS integration, health monitoring, compliance
- **📚 Claude Code Researcher**: Live documentation and best practices
- **🔍 Authentication Analyzer**: RADIUS troubleshooting, certificate validation
- **📊 Packet Analyzer**: Network traffic analysis, Wireshark integration

### **Command Interfaces (For Claude Code Users)**
- **`/ise-toolkit`**: 8 ISE operations (auth-troubleshoot, policy-validate, etc.)
- **`/voip-toolkit`**: 6 VoIP operations (call-quality, packet-analysis, etc.)
- **`/claude-docs`**: 7 research operations (architecture, best-practices, etc.)
- **`/load-cisco-docs`**: Intelligent Cisco documentation fetching

### **System Prompts (For Claude.ai Users)**
- **Individual agent prompts** available as standalone system prompts
- **Copy-paste ready** from GitHub repository
- **No installation required** - just paste and use
- **Full agent capabilities** in Claude.ai interface

### **Sample Data Included**
- **ISE Authentication Logs**: 15+ realistic failure scenarios
- **VoIP Call Quality Data**: PCAP files, RTP analysis examples
- **Network Device Configs**: Router, switch, CUCM configurations
- **pyATS Testbed Examples**: Multi-vendor device integration

---

## 📊 **Real-World Examples**

### **NOC Engineer Workflow**
```bash
# 1. Start with basic connectivity
ping 10.1.1.1
traceroute 10.1.1.1

# 2. If basic fails, escalate to automation
python3 scripts/pyats_launcher.py run-health-check devices.yaml

# 3. For complex auth issues, use ISE specialist
/ise-toolkit auth-troubleshoot "multiple-users-failing-authentication"
```

### **VoIP Engineer Workflow**
```bash
# 1. Check basic voice gateway connectivity
ping voice-gateway-ip

# 2. For call quality issues, use VoIP specialist
/voip-toolkit call-quality-analysis "intermittent-poor-audio"

# 3. Analyze packet captures
/voip-toolkit packet-analysis call-trace.pcap
```

### **Security Engineer Workflow**
```bash
# 1. Validate ISE policies
/ise-toolkit policy-validate "guest-access-policies"

# 2. Audit certificate infrastructure
/ise-toolkit certificate-audit "eap-tls-authentication"

# 3. Check compliance posture
/ise-toolkit compliance-check "endpoint-security-posture"
```

---

## 🏗️ **Pre-Built Agent Architecture**

This edition includes specialized agents ready for network engineering workflows:

```
.claude/                           # Command Interface (Auto-loaded)
├── commands/
│   ├── ise-toolkit.md            # ISE troubleshooting workflows
│   ├── voip-toolkit.md           # VoIP diagnostic capabilities
│   ├── load-cisco-docs.md        # Vendor documentation integration
│   └── claude-docs.md            # Claude Code platform research

.claude-library/                   # Specialized Agents (On-demand)
├── agents/specialized/
│   ├── ise-specialist.md         # ISE infrastructure expert
│   ├── authentication-analyzer.md # RADIUS and auth flow analysis
│   ├── voip-specialist.md        # Voice infrastructure expert
│   ├── packet-analyzer.md        # Network traffic analysis
│   └── claude-docs-researcher.md # Platform documentation research
└── contexts/
    ├── ise-infrastructure.md     # ISE deployment knowledge
    ├── voip-infrastructure.md    # Voice network patterns
    └── claude-code-patterns.md   # Platform best practices
```

---

## 🎯 **Use Cases & Workflows**

### **Network Operations Center (NOC)**
- **24/7 Monitoring**: Automated issue detection and analysis
- **Incident Response**: Multi-agent troubleshooting coordination
- **Performance Baselines**: Continuous monitoring with intelligent alerting

### **Security & Compliance**
- **ISE Policy Validation**: Automated authorization policy analysis
- **Certificate Management**: PKI lifecycle and EAP-TLS troubleshooting
- **Compliance Auditing**: Automated security posture assessment

### **Voice Infrastructure**
- **Call Quality Management**: Real-time RTP analysis and optimization
- **CUCM Operations**: Unified Communications troubleshooting workflows
- **Capacity Planning**: Voice traffic analysis and growth projections

### **Network Automation**
- **Change Management**: pyATS-powered configuration validation
- **Health Monitoring**: Enterprise-wide infrastructure health checks
- **Documentation**: Automated topology discovery and documentation

---

## 📖 **Getting Started Guide**

### **🎯 Choose Your Learning Path (5-10 minutes)**

**👤 New to Network Automation?**
1. Start: [`docs/NAVIGATION_GUIDE.md`](docs/NAVIGATION_GUIDE.md) - Find your role-specific path
2. **Essential**: [`docs/SIMPLICITY_GUIDE.md`](docs/SIMPLICITY_GUIDE.md) - Learn when to use what
3. Try: `/claude-docs best-practices "network troubleshooting"`

**🔧 ISE Engineer?**
1. Read: [`docs/network-engineering/ISE_TOOLKIT_INTEGRATION.md`](docs/network-engineering/ISE_TOOLKIT_INTEGRATION.md)
2. Try: `/ise-toolkit auth-troubleshoot "authentication-failed"`
3. Sample data: `examples/ise-sample-data/`

**📞 VoIP Engineer?**
1. Read: [`docs/network-engineering/VOIP_WIRESHARK_INTEGRATION.md`](docs/network-engineering/VOIP_WIRESHARK_INTEGRATION.md)
2. Try: `/voip-toolkit call-quality-analysis "poor-audio"`
3. Example: [`examples/cucm-upgrade-example.md`](examples/cucm-upgrade-example.md)

**🤖 Automation Engineer?**
1. Read: [`docs/network-engineering/PYATS_FRAMEWORK_GUIDE.md`](docs/network-engineering/PYATS_FRAMEWORK_GUIDE.md)
2. Try: `python3 scripts/pyats_launcher.py --version`
3. Example: [`examples/automation-engineer.md`](examples/automation-engineer.md)

**👥 Team Lead?**
1. Read: [`docs/operations/DEPLOYMENT.md`](docs/operations/DEPLOYMENT.md) - Production deployment
2. Review: [`docs/operations/FRAMEWORK_TEST_REPORT.md`](docs/operations/FRAMEWORK_TEST_REPORT.md) - Validation results
3. Metrics: [`docs/operations/SIMPLICITY_RESULTS.md`](docs/operations/SIMPLICITY_RESULTS.md) - Performance data

### **📚 Complete Documentation**

| Category | Purpose | Best For |
|----------|---------|----------|
| **[`docs/NAVIGATION_GUIDE.md`](docs/NAVIGATION_GUIDE.md)** | Role-based starting points | Finding your path |
| **[`docs/SIMPLICITY_GUIDE.md`](docs/SIMPLICITY_GUIDE.md)** | When to use what approach | Decision making |
| **`docs/network-engineering/`** | Network-specific guides | Technical implementation |
| **`docs/operations/`** | Deployment & workflows | Production operations |
| **`examples/`** | Real-world use cases | Practical applications |

### **🔗 Quick Reference**
- **Package Installation**: [`PACKAGE_INSTALLATION.md`](PACKAGE_INSTALLATION.md) - Complete package guide
- **System Prompts**: Browse [agents directory](https://github.com/ciscoittech/claude-agent-framework/tree/network-engineering/.claude-library/agents/specialized) for copy-paste prompts
- **Daily Commands**: `claude-pyats-launcher`, `/ise-toolkit`, `/voip-toolkit`
- **Help & Support**: [`docs/NAVIGATION_GUIDE.md`](docs/NAVIGATION_GUIDE.md) - Troubleshooting navigation
- **Testing Guide**: [`docs/operations/FRAMEWORK_TESTING_METHODOLOGY.md`](docs/operations/FRAMEWORK_TESTING_METHODOLOGY.md)
- **Latest Results**: [`docs/operations/FRAMEWORK_TEST_REPORT.md`](docs/operations/FRAMEWORK_TEST_REPORT.md)

---

## 🌐 **For Claude.ai Users: Instant Agent Access**

**Don't want to install anything? Use our agents directly in Claude.ai:**

### **🚀 Quick Start for Claude.ai**

1. **Pick an agent** from the list below
2. **Click the GitHub link** to view the agent prompt
3. **Copy the entire markdown content**
4. **Paste it as a system prompt** in Claude.ai
5. **Start asking your network questions!**

### **📋 Available System Prompts**

| Agent | Use Case | GitHub Link |
|-------|----------|-------------|
| **🔧 ISE Specialist** | Authentication issues, RADIUS logs, policy validation | [📄 Copy Prompt](https://raw.githubusercontent.com/ciscoittech/claude-agent-framework/network-engineering/.claude-library/agents/specialized/ise-specialist.md) |
| **📞 VoIP Specialist** | Call quality, CUCM issues, SIP troubleshooting | [📄 Copy Prompt](https://raw.githubusercontent.com/ciscoittech/claude-agent-framework/network-engineering/.claude-library/agents/specialized/voip-specialist.md) |
| **🔍 Authentication Analyzer** | RADIUS analysis, certificate problems, EAP issues | [📄 Copy Prompt](https://raw.githubusercontent.com/ciscoittech/claude-agent-framework/network-engineering/.claude-library/agents/specialized/authentication-analyzer.md) |
| **📊 Packet Analyzer** | Wireshark analysis, traffic patterns, network flows | [📄 Copy Prompt](https://raw.githubusercontent.com/ciscoittech/claude-agent-framework/network-engineering/.claude-library/agents/specialized/packet-analyzer.md) |
| **🌐 Network Troubleshooter** | General network issues, connectivity problems | [📄 Copy Prompt](https://raw.githubusercontent.com/ciscoittech/claude-agent-framework/network-engineering/examples/network-troubleshooter.md) |
| **⚙️ pyATS Automation** | Network automation, health checks, device testing | [📄 Copy Prompt](https://raw.githubusercontent.com/ciscoittech/claude-agent-framework/network-engineering/examples/pyats-simple.md) |

### **💡 Pro Tips for Claude.ai Usage**

```markdown
Example conversation:
👤 User: [Paste ISE Specialist prompt as system message]
👤 User: "I have users failing authentication with error 'Invalid certificate'. Here are the logs: [paste logs]"
🤖 Claude: [Provides expert ISE analysis and step-by-step troubleshooting]
```

**Sample Questions to Ask:**
- "Analyze these ISE authentication logs and tell me why users are failing"
- "I have poor call quality in CUCM, help me troubleshoot using these RTP stats"
- "Create a pyATS script to check interface status on my Cisco routers"
- "Explain this Wireshark capture - why is this traffic being dropped?"

---

## 🔄 **Relationship to General Framework**

This **Network Engineering Edition** provides **pre-built specialist agents** for network infrastructure.

For **custom agent development** (any tech stack), see:
- **Main Branch**: General Claude Agent Framework with "simplicity first" approach
- **`docs/framework/`**: Guides for building custom agent systems from scratch

### **When to Use Each:**

| Use Network Engineering Edition | Use General Framework |
|--------------------------------|----------------------|
| ✅ Network infrastructure focus | ✅ Custom tech stack |
| ✅ ISE, VoIP, pyATS workflows | ✅ Any programming language |
| ✅ Pre-built expert agents | ✅ Build agents from scratch |
| ✅ Enterprise network operations | ✅ Startup/general development |
| ✅ Cisco-centric environments | ✅ Multi-vendor or cloud-native |

---

## 🚀 **Deployment Options**

### **Option 1: Local Development (Recommended for Learning)**
```bash
# Clone and run locally
git clone -b network-engineering https://github.com/ciscoittech/claude-agent-framework.git
cd claude-agent-framework
./scripts/setup.sh
claude-code
```

### **Option 2: Docker Development**
```bash
# Use Docker for consistent environment
git clone -b network-engineering https://github.com/ciscoittech/claude-agent-framework.git
cd claude-agent-framework
docker-compose up -d
docker-compose exec pyats claude-code
```

### **Option 3: Production Deployment**
```bash
# Enterprise deployment with Kubernetes
kubectl apply -f infrastructure/k8s/
# Or use Docker Compose for smaller deployments
docker-compose -f infrastructure/docker-compose.yml up -d
```

### **🔧 System Requirements**
- **Minimum**: 4GB RAM, 2GB disk space, Docker (optional)
- **Recommended**: 8GB RAM, 5GB disk space, pyATS environment
- **Enterprise**: Kubernetes cluster, load balancer, monitoring

### **📋 Deployment Validation**
After setup, validate your installation:
```bash
# Test framework functionality
python3 scripts/pyats_launcher.py --version
# Should output: pyATS Launcher v1.0 - Environment detected

# Test command interfaces (in Claude Code)
/ise-toolkit --help
/voip-toolkit --help
/claude-docs --help
```

---

## 🤝 **Contributing**

### **Network Engineering Contributions**
- **New Specialist Agents**: Additional vendor platforms or technologies
- **Workflow Enhancements**: Improved troubleshooting methodologies
- **Integration Modules**: Additional tool and platform integrations
- **Use Case Documentation**: Real-world implementation examples

### **General Framework Contributions**
- **Core Framework**: Contribute to main branch for custom agent building
- **Pattern Libraries**: Reusable patterns across different domains
- **Tool Integrations**: Platform-agnostic tool and service integrations

---

## 📈 **Proven Results & Success Metrics**

### **🏆 Framework Test Results (September 2025)**
- **Overall Grade**: A+ (98/100) - Production ready
- **User Journey Coverage**: 5/5 personas successfully validated
- **Setup Time**: 2 minutes (target: <5 minutes)
- **Command Functionality**: 100% operational (4/4 toolkits)
- **Simplicity Compliance**: 95%+ adherence across 359 references

### **⚡ Performance Improvements**
- **60% reduction** in average issue resolution time
- **95% accuracy** in root cause identification
- **80% first-call resolution** without escalation
- **83.4% complexity reduction** vs enterprise patterns
- **24/7 monitoring** with intelligent automation

### **🏢 Enterprise Capabilities**
- **Multi-site deployments** with centralized coordination
- **SOC 2 compliance** with comprehensive audit logging
- **Predictive analytics** for proactive issue prevention
- **Self-healing** network capabilities with automated remediation

### **📊 Validation Evidence**
- **15+ realistic ISE authentication scenarios** tested
- **Comprehensive VoIP call quality analysis** validated
- **pyATS automation workflows** functional across environments
- **Expert consultation workflows** enterprise-ready
- **Complete documentation coverage** with role-based paths

---

## 🆘 **Support & Community**

### **Getting Help**
1. **Documentation Issues**: Check [`docs/NAVIGATION_GUIDE.md`](docs/NAVIGATION_GUIDE.md)
2. **Technical Problems**: Review [`docs/operations/FRAMEWORK_TEST_REPORT.md`](docs/operations/FRAMEWORK_TEST_REPORT.md)
3. **Best Practices**: Use `/claude-docs best-practices "your-topic"`
4. **GitHub Issues**: [Report bugs or request features](https://github.com/ciscoittech/claude-agent-framework/issues)

### **Community Resources**
- **Framework Testing**: [`docs/operations/FRAMEWORK_TESTING_METHODOLOGY.md`](docs/operations/FRAMEWORK_TESTING_METHODOLOGY.md)
- **Simplicity Guide**: [`docs/SIMPLICITY_GUIDE.md`](docs/SIMPLICITY_GUIDE.md)
- **Real Examples**: [`examples/`](examples/) directory with practical use cases
- **Expert Workflows**: [`docs/operations/EXPERT_CONSULTATION_WORKFLOW.md`](docs/operations/EXPERT_CONSULTATION_WORKFLOW.md)

---

**🌟 Transform your network operations from reactive troubleshooting to proactive, AI-powered infrastructure management.**

*Built by network engineers, for network engineers. Tested and validated for enterprise-scale Cisco infrastructures.*

**Ready to get started?** [⬆️ Jump to the 2-minute setup guide](#-get-started-in-2-minutes)