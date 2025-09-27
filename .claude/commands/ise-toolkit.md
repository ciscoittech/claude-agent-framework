# Cisco ISE Troubleshooting Toolkit

Load the comprehensive Cisco Identity Services Engine (ISE) troubleshooting workflow with authentication analysis, policy validation, and endpoint profiling diagnostics.

## Usage
```
/ise-toolkit [operation] [target]
```

## Operations
- `auth-troubleshoot` - Complete authentication flow analysis and debugging
- `policy-validate` - Authorization policy validation and condition analysis
- `endpoint-profile` - Device profiling and classification troubleshooting
- `guest-access` - Guest portal and sponsored access issue resolution
- `certificate-audit` - PKI and certificate-based authentication analysis
- `radius-analysis` - RADIUS authentication flow and AAA troubleshooting
- `compliance-check` - Posture assessment and compliance policy validation
- `performance-monitor` - ISE system performance and scalability analysis

## Examples
```bash
# Complete authentication troubleshooting
/ise-toolkit auth-troubleshoot "user-cannot-connect"

# Analyze RADIUS logs for failed authentications
/ise-toolkit radius-analysis failed-auth-logs.txt

# Validate authorization policies
/ise-toolkit policy-validate "network-access-policies"

# Troubleshoot endpoint profiling
/ise-toolkit endpoint-profile "unknown-devices"

# Guest access portal issues
/ise-toolkit guest-access "portal-redirect-failures"

# Certificate-based authentication problems
/ise-toolkit certificate-audit "eap-tls-failures"
```

## What This Loads
1. **ISE Specialist Agent** - Expert in ISE architecture, policies, and authentication flows
2. **Authentication Analyzer Agent** - RADIUS log analysis, 802.1X troubleshooting
3. **Policy Engine Agent** - Authorization policy validation and condition logic
4. **Endpoint Profiler Agent** - Device classification and profiling analysis
5. **Certificate Analyst Agent** - PKI troubleshooting and EAP-TLS diagnostics
6. **ISE Infrastructure Context** - ISE deployment models, integration patterns

## Workflow Stages
1. **Issue Assessment** - Gather symptoms and identify authentication scope
2. **Log Collection** - Guide collection of relevant ISE logs and traces
3. **Flow Analysis** - Multi-stage authentication and authorization analysis
4. **Policy Validation** - Verify policy logic and condition evaluation
5. **Root Cause** - Identify specific configuration or environmental issues
6. **Remediation** - Provide step-by-step resolution with validation
7. **Prevention** - Recommend monitoring and preventive measures

## Integration Points
- **Active Directory** - LDAP integration and group membership validation
- **Certificate Authorities** - PKI integration and certificate lifecycle
- **Network Infrastructure** - Switch/WLC configuration for 802.1X
- **SIEM Integration** - Security event correlation and threat response
- **Guest Portals** - Customization and branding troubleshooting
- **Compliance Tools** - Endpoint assessment and remediation workflows

## Authentication Flow Support
- **802.1X (EAP-TLS, PEAP, EAP-TTLS)** - Certificate and credential-based auth
- **MAC Authentication Bypass (MAB)** - Device-based authentication
- **Web Authentication** - Portal-based access control
- **Guest Access** - Sponsored and self-registration workflows
- **Device Registration** - BYOD enrollment and certificate provisioning

## Policy Engine Capabilities
- **Authorization Policies** - Network access permissions and VLAN assignment
- **Authentication Policies** - Identity source selection and method validation
- **Profiling Policies** - Device classification and automatic profiling
- **Posture Policies** - Compliance assessment and remediation requirements
- **Exception Policies** - Special case handling and bypass scenarios

## Compliance and Security
- **Endpoint Compliance** - Antivirus, patch level, and security posture
- **Threat Detection** - Anomalous behavior and security violations
- **Risk Assessment** - Device trust scoring and adaptive access
- **Quarantine Management** - Isolation and remediation workflows