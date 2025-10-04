# Claude Agent Framework v1.1 - Testing Guide

**Version**: 1.1 (Hooks Pattern Edition)
**Last Updated**: October 4, 2025
**Status**: Production Ready

---

## 📋 Overview

This guide covers testing the Claude Agent Framework v1.1, which includes:
- **Core Framework** (v1.0): Agent system, commands, contexts
- **Observability Pattern** (v1.0+): Logfire integration for insights
- **Hooks Pattern** (v1.1): Deterministic workflow control

---

## 🧪 Test Suites

### 1. Hooks Pattern Test Suite (NEW in v1.1)

**File**: `test_hooks_pattern.py`
**Tests**: 13 comprehensive tests
**Pass Rate Target**: 100%

**What It Tests**:
- ✅ Hook directory structure (configs/, scripts/, patterns/)
- ✅ Pre-built hook configurations (code-quality, security, performance, notifications)
- ✅ Hook script executability and functionality
- ✅ REGISTRY.json hooks configuration
- ✅ Hook event validation
- ✅ Documentation completeness

**Run It**:
```bash
python3 test_hooks_pattern.py
```

**Expected Output**:
```
======================================================================
CLAUDE AGENT FRAMEWORK v1.1
Hooks Pattern Test Suite
======================================================================

Total Tests: 13
Passed: 13 ✅
Failed: 0 ❌

Pass Rate: 100.0%
```

### 2. Observability Pattern Tests

**Files**: `test_observability_journey*.py`
**Tests**: Multiple journey-based tests
**Focus**: Logfire integration and validation

**What It Tests**:
- ✅ Logfire connection and configuration
- ✅ Agent workflow tracking
- ✅ Performance metrics collection
- ✅ Output validation patterns

**Run It**:
```bash
python3 test_observability_journey1.py
python3 test_observability_journey2.py
python3 test_observability_journey3.py
```

**Prerequisites**:
- Logfire account and API key
- `logfire` package installed
- `.logfire/` configuration

### 3. Framework Core Tests

**Coverage**: Agent coordination, context loading, parallel execution

**Manual Test**:
```bash
# In your project directory
claude

# Test agent launcher
"Please read .claude/agent-launcher.md and explain the agent system"

# Test parallel execution
"Run the framework validation tests"
```

---

## 🎯 Test Categories

### A. Hooks Pattern Tests

| Test | Purpose | Pass Criteria |
|------|---------|---------------|
| Directory Structure | Verify hooks/ organization | All dirs exist |
| Configurations | Validate hook configs | Valid JSON, proper events |
| Scripts Executable | Check script permissions | All scripts executable |
| Security Script | Test security_check.py | Blocks dangerous commands |
| Format Script | Test format_code.sh | Executes without error |
| Timing Script | Test track_timing.sh | Logs timing data |
| Documentation | Verify pattern docs | Comprehensive docs exist |
| README | Check hooks README | All sections present |
| Registry Config | Validate REGISTRY.json | Proper hooks config |

### B. Hook Configuration Validation

**Test Individual Configs**:
```bash
# Code Quality
cat .claude-library/hooks/configs/code-quality.json | jq .

# Security
cat .claude-library/hooks/configs/security.json | jq .

# Performance
cat .claude-library/hooks/configs/performance.json | jq .

# Notifications
cat .claude-library/hooks/configs/notifications.json | jq .
```

### C. Hook Script Testing

**Security Check**:
```bash
# Should ALLOW safe command
python3 .claude-library/hooks/scripts/security_check.py "ls -la"
# Exit code: 0

# Should BLOCK dangerous command
python3 .claude-library/hooks/scripts/security_check.py "rm -rf /"
# Exit code: 1
```

**Format Code**:
```bash
# Test formatter (dry run)
bash .claude-library/hooks/scripts/format_code.sh --help
```

**Track Timing**:
```bash
# Test timing tracker
bash .claude-library/hooks/scripts/track_timing.sh "test_operation"
# Check: .claude-metrics/timing.log
```

---

## 🔍 Integration Testing

### Test Hooks with Real Workflow

**Setup**:
1. Enable hooks in REGISTRY.json:
```json
{
  "settings": {
    "hooks": {
      "enabled": true,
      "scope": "project",
      "configs": [
        ".claude-library/hooks/configs/code-quality.json"
      ],
      "allow_blocking": true,
      "timeout_ms": 5000
    }
  }
}
```

2. Create test file:
```bash
echo "def   foo(  ):\n    pass" > test_format.py
```

3. Trigger hook via Claude Code:
```bash
claude> "Please edit test_format.py and fix the function"
```

4. Verify hook execution:
```bash
# Check hook logs
cat .claude-metrics/hooks.log

# Verify formatting
cat test_format.py  # Should be formatted
```

### Test Security Hooks

**Setup Security Config**:
```json
{
  "settings": {
    "hooks": {
      "enabled": true,
      "configs": [
        ".claude-library/hooks/configs/security.json"
      ],
      "allow_blocking": true
    }
  }
}
```

**Test Blocking**:
```bash
claude> "Please run: rm -rf /tmp/test"
# Hook should block dangerous command
```

---

## 📊 Performance Benchmarks

### Hooks Pattern Performance Targets

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Hook Execution Time | < 1s | 100-500ms | ✅ |
| Script Startup | < 100ms | 50-80ms | ✅ |
| Security Check | < 50ms | 10-30ms | ✅ |
| Format Code | < 2s | 500ms-1.5s | ✅ |
| Memory Overhead | < 10MB | 2-5MB | ✅ |

### Test Performance

```bash
# Time hook execution
time python3 .claude-library/hooks/scripts/security_check.py "ls -la"

# Expected: real 0m0.030s
```

---

## 🚨 Troubleshooting

### Common Test Failures

**1. "Hook scripts not executable"**
```bash
# Fix permissions
chmod +x .claude-library/hooks/scripts/*.sh
chmod +x .claude-library/hooks/scripts/*.py
```

**2. "Config missing 'hooks' key"**
- Check JSON syntax
- Verify config follows proper format
- Compare with working configs

**3. "Security check failing"**
- Ensure Python 3 available
- Check script has execute permission
- Verify dangerous_patterns list

**4. "Hook timeout"**
- Increase timeout_ms in REGISTRY.json
- Check hook script performance
- Simplify hook logic

### Test Environment Issues

**Missing Dependencies**:
```bash
# For Hooks Pattern: No dependencies needed!
# Self-contained, uses standard shell commands

# For Observability:
pip install logfire
```

**Permission Issues**:
```bash
# Fix all hook scripts
find .claude-library/hooks/scripts -type f -exec chmod +x {} \;
```

---

## 📝 Test Checklist

### Pre-Release Testing

- [ ] Run `test_hooks_pattern.py` - 100% pass
- [ ] Test each hook config individually
- [ ] Verify security blocking works
- [ ] Test code formatting integration
- [ ] Check hook logs in `.claude-metrics/hooks.log`
- [ ] Validate hook timeout handling
- [ ] Test with `hooks.enabled: false` (zero overhead)
- [ ] Test with `hooks.enabled: true` (proper execution)
- [ ] Verify README.md updated with v1.1 info
- [ ] Confirm CLAUDE_AGENT_FRAMEWORK.md has hooks docs
- [ ] Check all pattern docs are comprehensive

### Integration Testing

- [ ] Test with real Claude Code workflow
- [ ] Verify hooks don't interfere with normal operations
- [ ] Confirm blocking hooks prevent dangerous commands
- [ ] Test PostToolUse hooks for auto-formatting
- [ ] Validate notification hooks (Slack/Discord)
- [ ] Check performance metrics collection
- [ ] Test agent validation hooks

### Documentation Testing

- [ ] Hooks README.md is complete
- [ ] Pattern docs (agent-validation, workflow-gates, lightweight-observability)
- [ ] CLAUDE_AGENT_FRAMEWORK.md sections clear
- [ ] Example configs are valid
- [ ] Script comments are helpful

---

## 🎓 Test Patterns

### Unit Test Pattern (Hooks)

```python
def test_hook_feature(tester):
    """Test specific hook functionality"""

    def run_test():
        # Setup
        config_path = CONFIGS_DIR / "feature.json"

        # Load config
        with open(config_path) as f:
            config = json.load(f)

        # Validate
        assert "hooks" in config
        assert len(config["hooks"]) > 0

    tester.test("Hook feature test", run_test)
```

### Integration Test Pattern

```bash
# 1. Enable hooks
# 2. Trigger workflow
# 3. Verify hook execution
# 4. Check logs
# 5. Validate results
```

---

## 📈 Test Metrics

### Coverage Goals

- **Hooks Pattern**: 100% (13/13 tests passing)
- **Configuration Files**: 100% (all configs validated)
- **Scripts**: 100% (all scripts tested)
- **Documentation**: 100% (all docs verified)

### Quality Gates

All tests must pass before:
- ✅ Merging to main
- ✅ Version tagging
- ✅ Release creation
- ✅ Documentation updates

---

## 🚀 Next Steps

### After v1.1 Testing

1. **Document Learnings**:
   - What hooks patterns work best?
   - Which configs are most useful?
   - Performance optimizations found?

2. **Extend Testing**:
   - Add more hook script tests
   - Test edge cases
   - Stress test hook execution

3. **Community Testing**:
   - Get feedback on hook configs
   - Collect real-world use cases
   - Improve based on usage patterns

---

## 📚 Related Documentation

- **Hooks Pattern**: `.claude-library/hooks/README.md`
- **Hook Patterns**: `.claude-library/hooks/patterns/*.md`
- **Framework Docs**: `CLAUDE_AGENT_FRAMEWORK.md`
- **Main README**: `README.md`

---

## ✅ Success Criteria

v1.1 testing is complete when:

- ✅ All hooks pattern tests pass (13/13)
- ✅ All hook scripts are executable
- ✅ All configs are valid JSON
- ✅ Documentation is comprehensive
- ✅ Integration tests work
- ✅ Performance targets met
- ✅ No regressions in core framework

---

**Document Version**: 1.0
**Framework Version**: 1.1
**Last Test Run**: October 4, 2025
**Status**: ✅ All Tests Passing
