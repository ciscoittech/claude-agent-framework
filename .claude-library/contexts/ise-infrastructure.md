# Cisco ISE Infrastructure Context

## Overview
This context provides essential Cisco Identity Services Engine (ISE) knowledge for troubleshooting network access control, authentication flows, policy enforcement, and identity management systems.

## ISE Architecture and Components

### **ISE Node Roles**
```yaml
Primary Administration Node (PAN):
  - Central configuration management and policy authoring
  - Certificate authority services and PKI management
  - Backup and restore operations
  - License management and node registration
  - Global configuration replication

Policy Service Node (PSN):
  - RADIUS/TACACS+ authentication and authorization
  - Network access control policy enforcement
  - Guest portal services and customization
  - Profiling and endpoint identification
  - Posture assessment and compliance validation

Monitoring and Troubleshooting (MnT):
  - Log collection, storage, and analysis
  - Reporting and analytics dashboards
  - Live log monitoring and alerting
  - Historical trend analysis
  - Performance monitoring and capacity planning

Secondary Administration Node:
  - Backup administration capabilities
  - Automatic failover for admin functions
  - Distributed administration for large deployments
```

### **ISE Deployment Models**
```yaml
Standalone Deployment:
  - Single ISE node with all services
  - Suitable for small environments (< 1000 endpoints)
  - Limited scalability and no high availability

Small Deployment:
  - 2 nodes: Admin/MnT and PSN
  - Basic high availability
  - Up to 5000 endpoints

Medium Deployment:
  - 4-6 nodes: Dedicated admin, MnT, and multiple PSNs
  - Load balancing and redundancy
  - Up to 50,000 endpoints

Large Deployment:
  - 6+ nodes with geographical distribution
  - Dedicated monitoring nodes
  - External database support
  - 100,000+ endpoints
```

## Authentication Methods and Flows

### **802.1X Authentication**
```yaml
Wired 802.1X Flow:
  1. Link Detection: Switch detects device connection
  2. EAP-Request Identity: Switch requests device identity
  3. EAP-Response Identity: Device provides username
  4. RADIUS Access-Request: Switch forwards to ISE
  5. EAP Method Negotiation: ISE and client agree on EAP type
  6. Authentication Exchange: Certificate or credential validation
  7. RADIUS Access-Accept/Reject: ISE returns result with attributes
  8. Port Authorization: Switch applies network access controls

Wireless 802.1X Flow:
  1. Association: Client associates with WLAN
  2. EAP-Start: WLC initiates 802.1X authentication
  3. EAP Exchange: Similar to wired but over wireless medium
  4. 4-Way Handshake: PTK/GTK key exchange after authentication
  5. Data Traffic: Encrypted data transmission begins
```

### **EAP Methods**
```yaml
EAP-TLS (Certificate-based):
  - Mutual certificate authentication
  - Strongest security but requires PKI infrastructure
  - Common in high-security environments
  - Issues: Certificate expiration, CA trust, time synchronization

PEAP-MSCHAPv2:
  - Server certificate with username/password
  - Most common in enterprise environments
  - Easier deployment than EAP-TLS
  - Issues: Certificate validation, password policies

EAP-TTLS:
  - Flexible inner authentication methods
  - Supports legacy authentication protocols
  - Less common than PEAP
  - Issues: Configuration complexity, compatibility

EAP-FAST:
  - Cisco proprietary method
  - Uses Protected Access Credentials (PAC)
  - Suitable for legacy devices
  - Issues: PAC provisioning, security concerns
```

### **Fallback Authentication Methods**
```yaml
MAC Authentication Bypass (MAB):
  - Device MAC address used as username/password
  - Suitable for devices without 802.1X supplicant
  - Often combined with device profiling
  - Issues: MAC spoofing, endpoint database management

Web Authentication (WebAuth):
  - Browser-based authentication portal
  - Used for guest access and BYOD
  - Supports multiple identity sources
  - Issues: Browser compatibility, certificate warnings

Central Web Authentication (CWA):
  - Initial network access with subsequent web authentication
  - More flexible than local web authentication
  - Better user experience for BYOD scenarios
  - Issues: Redirection timing, portal customization
```

## Policy Engine Structure

### **Authentication Policies**
```yaml
Policy Structure:
  - Conditions: Define when policy applies
  - Identity Sources: Where to authenticate users
  - Advanced Options: Certificate validation, EAP chaining

Common Conditions:
  - Network Device Groups
  - User identity groups
  - Time and date restrictions
  - Device types and locations

Identity Source Selection:
  - Active Directory
  - LDAP directories
  - Internal users
  - Certificate authentication
  - External RADIUS token servers
```

### **Authorization Policies**
```yaml
Policy Components:
  - Conditions: Complex boolean logic with attributes
  - Permissions: Network access privileges
  - Security Group Tags (SGT): for TrustSec integration

Standard Attributes:
  - User identity groups
  - Endpoint identity groups
  - Network device groups
  - Time and date
  - Location (Network Device Group)
  - Authentication method

Authorization Results:
  - Access Accept: Grant network access
  - Access Reject: Deny network access
  - Access Quarantine: Limited network access
  - Permit with modifications: Conditional access

RADIUS Attributes:
  - VLAN assignments (Tunnel attributes)
  - Access Control Lists (Filter-ID)
  - Session timeout values
  - Bandwidth limitations
  - Security Group Tags (SGT)
```

## Endpoint Profiling

### **Profiling Process**
```yaml
Data Collection:
  - DHCP fingerprinting
  - HTTP User-Agent strings
  - SNMP queries to network devices
  - NetFlow/sFlow analysis
  - NMAP scans (optional)
  - Active Directory machine accounts

Profiling Policies:
  - Conditions based on collected attributes
  - Certainty factor calculations
  - Parent-child policy relationships
  - Exception handling for unknown devices

Built-in Profiles:
  - Workstations (Windows, Mac, Linux)
  - Mobile devices (iOS, Android)
  - Printers and scanners
  - IP phones and video endpoints
  - Network infrastructure devices
  - IoT and specialized devices
```

### **Profiling Attributes**
```yaml
DHCP Attributes:
  - DHCP-Class-Identifier
  - DHCP-Parameter-Request-List
  - DHCP-Client-Identifier
  - DHCP-Vendor-Class-Identifier

HTTP Attributes:
  - HTTP-User-Agent
  - HTTP-Accept
  - HTTP-Accept-Language
  - HTTP-Accept-Encoding

Device Attributes:
  - MAC-Address
  - Operating-System
  - Device-Family
  - Hardware-Vendor
  - Software-Version

Network Attributes:
  - IP-Address
  - VLAN-ID
  - Switch-Port-ID
  - NAS-Port-Type
```

## Guest Access Management

### **Guest Portal Configuration**
```yaml
Portal Types:
  - Self-Registration: Users create own accounts
  - Sponsored Access: Approval-based guest access
  - Hotspot: Simple click-through access
  - BYOD: Device registration and certificate provisioning

Portal Customization:
  - Branding and logos
  - Terms and conditions
  - Multi-language support
  - Custom fields and validation
  - Integration with external systems

Guest User Lifecycle:
  1. Registration: Account creation or approval
  2. Authentication: Credential validation
  3. Authorization: Network access provisioning
  4. Session Management: Monitoring and control
  5. Expiration: Automatic account cleanup
```

### **Sponsor Portal Features**
```yaml
Sponsor Capabilities:
  - Guest account creation and management
  - Access duration and limitations
  - Password policies and requirements
  - Email notifications and instructions
  - Bulk guest account creation

Integration Options:
  - Active Directory for sponsor authentication
  - Email systems for notifications
  - SMS gateways for credential delivery
  - External databases for guest information
  - API integration for custom applications
```

## Integration Points

### **Active Directory Integration**
```yaml
Connection Configuration:
  - LDAP server settings and ports (389, 636, 3268, 3269)
  - Authentication credentials and service accounts
  - SSL/TLS encryption and certificate validation
  - Connection timeouts and retry settings

Group Management:
  - Group retrieval and nested group support
  - Group attribute mapping and filtering
  - Dynamic group membership updates
  - Group caching and performance optimization

Machine Authentication:
  - Computer account validation
  - Certificate-based machine authentication
  - Host/computer name resolution
  - Domain trust relationships

Attributes and Schema:
  - User attribute mapping (sAMAccountName, mail, memberOf)
  - Custom schema extensions
  - Attribute filtering and privacy controls
  - Multi-domain and multi-forest support
```

### **Certificate Authority Integration**
```yaml
Internal CA:
  - ISE built-in certificate authority
  - Root and subordinate CA hierarchy
  - Certificate templates and policies
  - Automatic certificate enrollment

External CA Integration:
  - Microsoft AD Certificate Services
  - Third-party PKI systems
  - Certificate import and trust chains
  - CRL and OCSP validation

Certificate Lifecycle:
  - Enrollment and provisioning
  - Renewal and expiration management
  - Revocation and CRL distribution
  - Key escrow and recovery
```

## Network Device Integration

### **RADIUS Configuration**
```yaml
Switch Configuration:
  - AAA method lists and authentication order
  - RADIUS server configuration and shared secrets
  - 802.1X port configuration and timers
  - VLAN and ACL integration
  - Change of Authorization (CoA) support

Wireless Controller:
  - WLAN security settings and authentication
  - RADIUS server groups and failover
  - Dynamic VLAN assignment
  - Guest tunneling and anchor controllers

Common RADIUS Attributes:
  - Tunnel-Type: VLAN (13)
  - Tunnel-Medium-Type: 802 (6)
  - Tunnel-Private-Group-ID: VLAN ID
  - Filter-ID: ACL name
  - Session-Timeout: Session duration
  - Termination-Action: Action after timeout
```

### **TrustSec Integration**
```yaml
Security Group Tags (SGT):
  - 16-bit tag values for policy enforcement
  - Manual and automatic SGT assignment
  - SGT propagation methods (inline tagging, SXP)
  - SGT to ACL mapping on enforcement devices

Security Group ACLs (SGACL):
  - Matrix-based policy enforcement
  - Source and destination SGT pairs
  - Permit, deny, and redirect actions
  - Logging and monitoring capabilities

SXP (SGT Exchange Protocol):
  - SGT-to-IP mapping propagation
  - Speaker and listener roles
  - Connection security and authentication
  - Scalability and performance considerations
```

## Compliance and Posture Assessment

### **Posture Policies**
```yaml
Compliance Requirements:
  - Antivirus software installation and updates
  - Operating system patch levels
  - Firewall enablement and configuration
  - Registry settings and security configurations
  - Custom compliance checks and scripts

Assessment Methods:
  - Agent-based assessment (NAC Agent)
  - Agentless assessment (registry and WMI queries)
  - Temporal agent (download and execution)
  - Certificate-based bypass
  - Custom posture agents

Remediation Actions:
  - Automatic remediation (file downloads, registry changes)
  - Manual remediation with instructions
  - Quarantine with limited network access
  - Block access until compliant
  - Time-based temporary access
```

### **Threat Detection**
```yaml
Anomaly Detection:
  - Behavioral analysis and baseline establishment
  - Velocity checking and threshold monitoring
  - Geolocation and impossible travel detection
  - Device fingerprinting and spoofing detection

Response Actions:
  - Automatic quarantine and isolation
  - Alert generation and notification
  - Session termination and re-authentication
  - Blacklist and whitelist management
  - Integration with security orchestration platforms
```

## Monitoring and Troubleshooting

### **Live Logs and Reporting**
```yaml
Authentication Logs:
  - RADIUS authentication and authorization
  - Guest access and portal usage
  - Administrative access and changes
  - Certificate validation and PKI events

Endpoint Activity:
  - Profiling and classification events
  - Posture assessment and compliance
  - Session establishment and termination
  - Network access and authorization changes

System Logs:
  - Node health and performance metrics
  - Database operations and replication
  - Certificate authority operations
  - Backup and restore activities
```

### **Performance Monitoring**
```yaml
Key Performance Indicators:
  - Authentication requests per second
  - Average authentication response time
  - Policy evaluation performance
  - Database query response times
  - Memory and CPU utilization

Capacity Planning:
  - Concurrent session limits
  - Database size and growth
  - Log retention and storage
  - Network bandwidth requirements
  - High availability considerations

Alerting and Thresholds:
  - Authentication failure rates
  - System resource utilization
  - Service availability and health
  - Certificate expiration warnings
  - Database connectivity issues
```

## Common Issues and Troubleshooting

### **Authentication Problems**
```yaml
Certificate Issues:
  - Certificate chain validation failures
  - Expired or revoked certificates
  - Time synchronization problems
  - CA trust and intermediate certificates

Credential Problems:
  - Username and password validation
  - Account lockout and expiration
  - Domain authentication failures
  - Service account permissions

Network Issues:
  - RADIUS connectivity and timeouts
  - Shared secret mismatches
  - Firewall and port blocking
  - Network device configuration
```

### **Policy Issues**
```yaml
Authorization Problems:
  - Policy condition evaluation
  - Attribute value mismatches
  - Multiple policy conflicts
  - Default policy behavior

Profiling Issues:
  - Incorrect device classification
  - Missing profiling attributes
  - Policy precedence problems
  - Performance impact

Guest Access Issues:
  - Portal customization problems
  - Sponsor workflow failures
  - Certificate warnings
  - Email delivery problems
```

This comprehensive ISE context provides the foundation for systematic troubleshooting and optimization of Cisco Identity Services Engine deployments.