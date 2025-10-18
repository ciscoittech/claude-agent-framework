# Multi-Model Routing for Claude Agent Framework
*Cost Optimization Through Intelligent Model Selection*

## Overview

The Claude Agent Framework can leverage **claude-code-router** to route different agent types to different models based on task complexity. This enables significant cost savings by using:
- **Fast, cheap models** for simple tasks
- **Powerful models** for complex reasoning
- **Specialized models** for specific domains (code, thinking, etc.)

### Performance & Cost Benefits

| Agent Type | Without Routing | With Qwen3 Routing | Savings |
|-----------|----------------|-------------------|---------|
| Background tasks | Claude Opus ($15/1M tokens) | Qwen3 Coder ($0.06/1M) | **99.6%** |
| Code review | Claude Opus ($15/1M tokens) | Qwen3 235B ($0.11/1M) | **99.3%** |
| General tasks | Claude Sonnet ($3/1M tokens) | Qwen3 80B ($0.10/1M) | **96.7%** |

**Real Impact**: A typical 10-agent workflow costing $2-5 drops to **$0.05-0.15**.

---

## Quick Start

### 1. Install Claude Code Router

```bash
npm install -g @musistudio/claude-code-router
```

### 2. Configure Router with Qwen3 Models

Create `~/.claude-code-router/config.json`:

```json
{
  "Providers": [
    {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
      "api_key": "${OPENROUTER_API_KEY}",
      "models": [
        "qwen/qwen3-next-80b-a3b-instruct-2509",
        "qwen/qwen3-next-80b-a3b-thinking-2509",
        "qwen/qwen3-235b-a22b-thinking-2507",
        "qwen/qwen3-coder-30b-a3b-instruct"
      ]
    }
  ],
  "Router": {
    "default": "openrouter,qwen/qwen3-next-80b-a3b-instruct-2509",
    "background": "openrouter,qwen/qwen3-coder-30b-a3b-instruct",
    "think": "openrouter,qwen/qwen3-next-80b-a3b-thinking-2509",
    "longContext": "openrouter,qwen/qwen3-235b-a22b-thinking-2507",
    "longContextThreshold": 100000
  },
  "SubAgents": {
    "general-purpose": "openrouter,qwen/qwen3-next-80b-a3b-instruct-2509",
    "code-reviewer": "openrouter,qwen/qwen3-235b-a22b-thinking-2507",
    "test-runner": "openrouter,qwen/qwen3-coder-30b-a3b-instruct",
    "framework-analyzer": "openrouter,qwen/qwen3-next-80b-a3b-thinking-2509"
  }
}
```

### 3. Set OpenRouter API Key

```bash
# Add to ~/.zshrc or ~/.bashrc
export OPENROUTER_API_KEY="your-key-here"

# Reload shell
source ~/.zshrc
```

### 4. Start Router Server

```bash
ccr start

# Verify it's running
ccr status
```

### 5. Update Your Agent System (Optional)

The router automatically intercepts requests. No code changes needed! But you can optimize further by documenting model preferences in your REGISTRY.json.

---

## Model Selection Strategy

### Qwen3 Model Family (Recommended for Cost Optimization)

| Model | Context | Cost (per 1M tokens) | Best For |
|-------|---------|---------------------|----------|
| **Qwen3 Coder 30B** | 262K | $0.06 (prompt) / $0.25 (completion) | Code generation, test writing, formatting |
| **Qwen3 Next 80B Instruct** | 262K | $0.10 (prompt) / $0.80 (completion) | General tasks, implementation, docs |
| **Qwen3 Next 80B Thinking** | 262K | $0.14 (prompt) / $1.20 (completion) | Architecture, complex reasoning |
| **Qwen3 235B Thinking** | 262K | $0.11 (prompt) / $0.60 (completion) | Code review, deep analysis |

### Agent-to-Model Mapping

Based on Claude Agent Framework agent types:

#### Core Agents
```
Architect Agent       → Qwen3 Next 80B Thinking
                        (Needs structured reasoning)

Engineer Agent        → Qwen3 Next 80B Instruct
                        (Balanced performance/cost)

Code Reviewer         → Qwen3 235B Thinking
                        (Deep analysis with reasoning)

Test Engineer         → Qwen3 Coder 30B
                        (Specialized + cheapest)
```

#### Specialized Agents
```
Database Specialist   → Qwen3 Next 80B Instruct
API Architect         → Qwen3 Next 80B Thinking
Security Auditor      → Qwen3 235B Thinking
Performance Engineer  → Qwen3 Next 80B Thinking
Documentation Writer  → Qwen3 Coder 30B
Deployment Manager    → Qwen3 Next 80B Instruct
```

#### Utility Agents
```
File Search Agent     → Qwen3 Coder 30B
Pattern Matcher       → Qwen3 Coder 30B
Workflow Orchestrator → Qwen3 Next 80B Instruct
Observer Agent        → Qwen3 Coder 30B
```

---

## Integration with REGISTRY.json

Update your `.claude-library/REGISTRY.json` to document model preferences:

```json
{
  "version": "1.0.0",
  "settings": {
    "multi_model_routing": {
      "enabled": true,
      "router": "claude-code-router",
      "router_url": "http://127.0.0.1:3456",
      "default_provider": "openrouter"
    }
  },
  "agents": {
    "architect": {
      "path": ".claude-library/agents/core/architect.md",
      "tools": ["Read", "Write", "Grep"],
      "category": "core",
      "model_preference": {
        "provider": "openrouter",
        "model": "qwen/qwen3-next-80b-a3b-thinking-2509",
        "reason": "Requires structured reasoning for architecture decisions"
      }
    },
    "engineer": {
      "path": ".claude-library/agents/core/engineer.md",
      "tools": ["*"],
      "category": "core",
      "model_preference": {
        "provider": "openrouter",
        "model": "qwen/qwen3-next-80b-a3b-instruct-2509",
        "reason": "Balanced performance for implementation tasks"
      }
    },
    "code-reviewer": {
      "path": ".claude-library/agents/core/reviewer.md",
      "tools": ["Read", "Grep", "Glob"],
      "category": "core",
      "model_preference": {
        "provider": "openrouter",
        "model": "qwen/qwen3-235b-a22b-thinking-2507",
        "reason": "Deep analysis with reasoning for quality assurance"
      }
    },
    "test-engineer": {
      "path": ".claude-library/agents/specialized/test-engineer.md",
      "tools": ["Read", "Write", "Bash"],
      "category": "specialized",
      "model_preference": {
        "provider": "openrouter",
        "model": "qwen/qwen3-coder-30b-a3b-instruct",
        "reason": "Code-specialized model, lowest cost for test generation"
      }
    }
  }
}
```

---

## Cost Analysis Example

### Scenario: Feature Development Workflow

**Workflow**: `/feature "Add user authentication"`

**Agents Used** (parallel execution):
1. Architect Agent (design specs)
2. Test Spec Agent (test plans)
3. Implementation Agent (code)
4. Review Agent (quality check)
5. Integration Agent (final validation)

#### Cost Comparison

**Without Routing** (all Claude Opus @ $15/1M):
- 5 agents × 8K tokens average = 40K tokens
- Cost: 40K × $15/1M = **$0.60 per workflow**

**With Qwen3 Routing**:
- Architect: 10K tokens × $0.14/1M = $0.0014
- Test Spec: 6K tokens × $0.06/1M = $0.00036
- Implementation: 15K tokens × $0.10/1M = $0.0015
- Review: 12K tokens × $0.11/1M = $0.00132
- Integration: 5K tokens × $0.06/1M = $0.0003
- **Total: $0.00488 per workflow**

**Savings: 99.2%** ($0.60 → $0.005)

---

## Advanced Patterns

### Pattern 1: Dynamic Model Selection

For agents that handle varying complexity:

```json
{
  "agents": {
    "adaptive-engineer": {
      "model_strategy": "dynamic",
      "model_rules": {
        "simple_crud": "qwen/qwen3-coder-30b-a3b-instruct",
        "complex_logic": "qwen/qwen3-next-80b-a3b-thinking-2509",
        "architecture_change": "qwen/qwen3-235b-a22b-thinking-2507"
      },
      "complexity_detection": "auto"
    }
  }
}
```

### Pattern 2: Fallback Chains

Handle model failures gracefully:

```json
{
  "Router": {
    "fallback_strategy": "cascade",
    "default": [
      "openrouter,qwen/qwen3-next-80b-a3b-instruct-2509",
      "openrouter,qwen/qwen3-235b-a22b-thinking-2507"
    ]
  }
}
```

### Pattern 3: Budget-Aware Routing

Set cost limits:

```json
{
  "settings": {
    "cost_control": {
      "max_cost_per_workflow": 0.10,
      "prefer_cheaper_models": true,
      "upgrade_on_failure": true
    }
  }
}
```

---

## Performance Monitoring

### Track Router Performance

```bash
# Check router status
ccr status

# View routing decisions (if router supports logging)
tail -f ~/.claude-code-router/router.log
```

### Measure Cost Savings

Add to your observability system:

```python
# .claude-library/observability/track_costs.py
import json
from pathlib import Path

def log_model_usage(agent_name, model_id, tokens, cost):
    metrics_file = Path('.claude-metrics/model-costs.json')

    data = json.loads(metrics_file.read_text()) if metrics_file.exists() else {}

    if agent_name not in data:
        data[agent_name] = {"total_cost": 0, "total_tokens": 0, "models": {}}

    data[agent_name]["total_cost"] += cost
    data[agent_name]["total_tokens"] += tokens
    data[agent_name]["models"][model_id] = data[agent_name]["models"].get(model_id, 0) + cost

    metrics_file.write_text(json.dumps(data, indent=2))
```

---

## Troubleshooting

### Router Not Intercepting Requests

```bash
# Verify router is running
ccr status

# Check config is valid
cat ~/.claude-code-router/config.json

# Restart router
ccr restart
```

### API Key Issues

```bash
# Verify key is set
echo $OPENROUTER_API_KEY

# Test OpenRouter directly
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

### Model Not Available

Update config with available models:
```bash
# List available models
curl https://openrouter.ai/api/v1/models | jq '.data[] | select(.id | contains("qwen3"))'
```

---

## Migration Guide

### From Single-Model to Multi-Model

1. **Audit Current Usage**
   ```bash
   # Analyze which agents run most frequently
   python3 .claude-library/observability/obs.py agents
   ```

2. **Install Router** (see Quick Start above)

3. **Map Agents to Models**
   - High-frequency, simple → Cheap models
   - Low-frequency, complex → Powerful models

4. **Test Incrementally**
   - Start with background/utility agents
   - Gradually migrate core agents
   - Monitor quality and cost

5. **Optimize**
   - Review cost metrics weekly
   - Adjust model assignments based on performance
   - Add fallback chains for critical agents

---

## Best Practices

### 1. **Start Conservative**
Use powerful models initially, then optimize:
```
Week 1: All agents → Qwen3 235B (learn baseline quality)
Week 2: Simple agents → Qwen3 Coder 30B (test cost savings)
Week 3: General agents → Qwen3 80B Instruct (balance cost/quality)
Week 4: Keep critical agents → Qwen3 235B (maintain quality)
```

### 2. **Monitor Quality**
Don't sacrifice quality for cost:
- Track task completion rates
- Review agent outputs regularly
- Use observability to catch degradation
- Upgrade models if quality drops

### 3. **Leverage Specialization**
- Code tasks → Qwen3 Coder models
- Reasoning tasks → Qwen3 Thinking models
- General tasks → Qwen3 Instruct models

### 4. **Cache Aggressively**
Router may support caching:
```json
{
  "Router": {
    "enable_cache": true,
    "cache_ttl": 3600
  }
}
```

---

## Integration Checklist

- [ ] Install `claude-code-router`
- [ ] Configure `~/.claude-code-router/config.json`
- [ ] Set `OPENROUTER_API_KEY` environment variable
- [ ] Start router server (`ccr start`)
- [ ] Update REGISTRY.json with model preferences
- [ ] Map agents to appropriate Qwen3 models
- [ ] Add cost tracking to observability
- [ ] Test with simple workflow
- [ ] Monitor quality vs. cost
- [ ] Document model selection decisions

---

## Future Enhancements

### Planned Features
- **Auto-Model-Selection**: Agent launcher auto-selects based on task complexity
- **Cost Dashboard**: Real-time cost visualization
- **A/B Testing**: Compare model performance side-by-side
- **Smart Fallbacks**: Automatic model upgrade on failure

### Community Contributions
Help improve multi-model routing:
- Share your model-to-agent mappings
- Report quality/cost findings
- Contribute routing strategies
- Add new provider integrations

---

## References

- [Claude Code Router GitHub](https://github.com/musistudio/claude-code-router)
- [OpenRouter Models](https://openrouter.ai/models)
- [Qwen3 Documentation](https://github.com/QwenLM/Qwen3)
- [Claude Agent Framework](./CLAUDE_AGENT_FRAMEWORK.md)

---

*Multi-Model Routing v1.0 | Cost optimization through intelligent model selection*
*Compatible with Claude Agent Framework v1.0+*
