# ISE Troubleshooting: Specialized System vs Normal Prompts

This directory contains realistic ISE sample data to demonstrate the difference between our specialized ISE toolkit and normal prompt interactions.

## Test Scenarios

### 1. Authentication Failure Analysis
**File**: `authentication-failure-logs.txt`
**Scenario**: Multiple 802.1X authentication failures with different root causes

#### Normal Prompt Test:
```
"I have users who can't authenticate to the network. Here are the logs: [paste logs]"
```

#### Specialized System Test:
```
/ise-toolkit auth-troubleshoot authentication-failure-logs.txt
```

**Expected Difference**:
- **Normal Prompt**: Generic troubleshooting advice, may miss subtle certificate timing issues
- **Specialized System**: Systematic flow analysis, identifies specific failure reasons with evidence, provides targeted remediation steps

### 2. Performance Analysis
**File**: `radius-trace-slow-auth.txt`
**Scenario**: Authentication taking >5 seconds due to infrastructure delays

#### Normal Prompt Test:
```
"Authentication is slow. Here's a RADIUS trace: [paste trace]"
```

#### Specialized System Test:
```
/ise-toolkit radius-analysis radius-trace-slow-auth.txt
```

**Expected Difference**:
- **Normal Prompt**: General advice about checking servers and network
- **Specialized System**: Precise timing analysis, identifies specific bottlenecks (certificate validation: 2.656s, AD lookup: 2.555s), provides specific optimization recommendations

### 3. Profiling Issues
**File**: `profiling-issue-logs.txt`
**Scenario**: Devices not being classified correctly, causing authorization failures

#### Normal Prompt Test:
```
"Devices are being profiled as unknown instead of their correct types. Here are the logs: [paste logs]"
```

#### Specialized System Test:
```
/ise-toolkit endpoint-profile profiling-issue-logs.txt
```

**Expected Difference**:
- **Normal Prompt**: Basic profiling advice, may not identify policy precedence issues
- **Specialized System**: Detailed analysis of profiling conditions, identifies certainty factor thresholds, policy conflicts, and performance impacts

### 4. Guest Access Problems
**File**: `guest-access-issues.txt`
**Scenario**: Multiple guest portal issues affecting user experience

#### Normal Prompt Test:
```
"Our guest portal isn't working properly. Users are having various issues: [paste logs]"
```

#### Specialized System Test:
```
/ise-toolkit guest-access guest-access-issues.txt
```

**Expected Difference**:
- **Normal Prompt**: General portal troubleshooting steps
- **Specialized System**: Systematic analysis of each issue type (certificate warnings, email validation, SMS failures, redirect loops), with specific configuration fixes

### 5. Complex Policy Logic
**File**: `policy-evaluation-complex.txt`
**Scenario**: Subtle policy engine logic problems causing inconsistent results

#### Normal Prompt Test:
```
"Users are getting inconsistent network access. Same users, different VLANs. Here are the policy evaluation logs: [paste logs]"
```

#### Specialized System Test:
```
/ise-toolkit policy-validate policy-evaluation-complex.txt
```

**Expected Difference**:
- **Normal Prompt**: May identify obvious policy conflicts but miss subtle issues
- **Specialized System**: Deep policy logic analysis, identifies boolean logic problems, case sensitivity issues, timezone confusion, AD cache staleness, and policy ranking problems

## Key Advantages of Specialized System

### 1. **Domain Expertise**
- **Normal**: Generic networking knowledge
- **Specialized**: Deep ISE architecture understanding, authentication flows, policy engine behavior

### 2. **Systematic Analysis**
- **Normal**: Ad-hoc troubleshooting suggestions
- **Specialized**: Structured workflows (Assessment → Analysis → Diagnosis → Remediation)

### 3. **Evidence-Based Diagnosis**
- **Normal**: General recommendations
- **Specialized**: Specific log evidence, timing analysis, configuration validation

### 4. **Root Cause Identification**
- **Normal**: Symptom-based suggestions
- **Specialized**: Multi-layer analysis connecting authentication, authorization, profiling, and infrastructure

### 5. **Actionable Remediation**
- **Normal**: "Check your configuration"
- **Specialized**: Specific configuration changes, commands, and validation steps

## Testing Methodology

### Step 1: Baseline Normal Prompt Testing
1. Use standard Claude without specialized toolkit
2. Provide same log data and symptoms
3. Document response quality and specificity

### Step 2: Specialized System Testing
1. Load ISE toolkit: `/ise-toolkit [operation] [data]`
2. Allow agent coordination and analysis
3. Document systematic approach and findings

### Step 3: Compare Results
Evaluate on these criteria:
- **Accuracy**: Correct identification of root causes
- **Specificity**: Detailed vs generic recommendations
- **Completeness**: Coverage of all issues in logs
- **Actionability**: Specific steps vs general advice
- **Efficiency**: Time to resolution

## Sample Comparison Results

### Authentication Failure Example

**Normal Prompt Response** (simplified):
```
"Based on your logs, you have several authentication issues:
1. Check certificate expiration
2. Verify Active Directory connectivity
3. Review RADIUS configuration
4. Check time synchronization

Try these general troubleshooting steps..."
```

**Specialized System Response** (detailed):
```
🎯 AUTHENTICATION ANALYSIS COMPLETE

Issues Identified:
1. Certificate Validation Failure (jdoe@company.com)
   - Root Cause: Certificate expired at 2024-09-26 15:30:00
   - Evidence: Line 15:23,067 - Certificate validation failed
   - Fix: Renew certificate, check auto-enrollment policy

2. Credential Issues (msmith@company.com)
   - Root Cause: Invalid password or account lockout
   - Evidence: Active Directory authentication failed after 145ms
   - Fix: Check account status, verify password policy

3. Time Synchronization (alice@company.com)
   - Root Cause: Certificate not yet valid due to time skew
   - Evidence: Current time 09:18:33, cert valid from 09:25:00
   - Fix: Synchronize NTP on client and certificate authority

4. Infrastructure Issues
   - RADIUS shared secret mismatch on 192.168.10.20
   - Unknown network device 192.168.50.100
   - Policy evaluation failure for contractors

Resolution Priority:
1. Fix time synchronization (immediate impact)
2. Update certificate auto-enrollment
3. Add missing network device to ISE
4. Review contractor access policies

Validation Commands:
- show ntp status
- certificate authority renewal status
- ISE network device configuration
```

This demonstrates the significant difference in diagnostic quality, specificity, and actionability between normal prompts and our specialized ISE troubleshooting system.