# VoIP Infrastructure Context

## Overview
This context provides essential VoIP infrastructure knowledge for troubleshooting Cisco Unified Communications environments, voice gateways, and SIP-based systems.

## Cisco CUCM Architecture

### **Call Processing Components**
```yaml
Core Services:
  - Call Manager: Primary call processing engine
  - Database Publisher: Central configuration and CDR storage
  - Subscriber Nodes: Distributed call processing for scalability
  - TFTP Server: Device configuration file distribution
  - CTI Manager: Computer Telephony Integration services

Supporting Services:
  - Unity Connection: Voicemail and unified messaging
  - IM&P: Instant messaging and presence
  - UCCX: Contact center applications
  - Emergency Responder: E911 location services
```

### **Device Registration Process**
```
1. DHCP Discovery → Option 150/66 for TFTP server
2. TFTP Download → Device configuration file (SEPxxxxx.cnf.xml)
3. HTTP/HTTPS → Authenticate with Call Manager
4. TCP 2000/2443 → Skinny (SCCP) or SIP registration
5. RTP Setup → Media path establishment for calls
```

### **Dial Plan Components**
```yaml
Route Patterns:
  - Pattern: 9.@ (External calls via gateway)
  - Pattern: [2-5]XXX (Internal 4-digit extensions)
  - Pattern: 911 (Emergency services)

Route Lists:
  - Primary Gateway Group
  - Secondary Gateway Group
  - Long Distance Restrictions

Translation Patterns:
  - Called Party: Digit manipulation for outbound
  - Calling Party: Number presentation control
```

## Voice Quality Metrics

### **Key Performance Indicators**
```yaml
MOS (Mean Opinion Score):
  - Excellent: 4.3 - 5.0
  - Good: 4.0 - 4.3
  - Fair: 3.6 - 4.0
  - Poor: 3.1 - 3.6
  - Bad: 1.0 - 3.1

Network Requirements:
  - Latency: < 150ms one-way (< 200ms acceptable)
  - Jitter: < 30ms (< 50ms acceptable)
  - Packet Loss: < 1% (< 3% acceptable)
  - Bandwidth: G.711 = 64kbps, G.729 = 8kbps codec payload
```

### **QoS Configuration**
```yaml
DSCP Markings:
  - Voice (RTP): EF (46) - Expedited Forwarding
  - Voice Signaling: AF31 (26) - SIP/SCCP
  - Video: AF41 (34) - High priority video
  - Call Control: CS3 (24) - CUCM cluster communication

Queue Priorities:
  - Priority Queue: Voice RTP traffic
  - Class-Based Weighted Fair Queue: Other traffic classes
  - Low Latency Queue: Real-time applications
```

## SIP Protocol Essentials

### **SIP Methods**
```yaml
Core Methods:
  - INVITE: Establish session/call setup
  - ACK: Acknowledge final response
  - BYE: Terminate session
  - CANCEL: Cancel pending request
  - REGISTER: Register with SIP server
  - OPTIONS: Query server capabilities

Response Codes:
  - 1xx: Provisional (100 Trying, 180 Ringing)
  - 2xx: Success (200 OK)
  - 3xx: Redirection (302 Moved Temporarily)
  - 4xx: Client Error (404 Not Found, 486 Busy Here)
  - 5xx: Server Error (503 Service Unavailable)
  - 6xx: Global Failure (600 Busy Everywhere)
```

### **SDP (Session Description Protocol)**
```yaml
Media Attributes:
  - m=audio: Media type and port
  - c=IN IP4: Connection information
  - a=rtpmap: RTP payload type mapping
  - a=sendrecv: Media direction capability
  - a=ptime: Packetization time

Codec Examples:
  - G.711 PCMU: rtpmap:0 PCMU/8000
  - G.711 PCMA: rtpmap:8 PCMA/8000
  - G.729: rtpmap:18 G729/8000
  - G.722: rtpmap:9 G722/8000
```

## Voice Gateway Configuration

### **Common Gateway Types**
```yaml
Cisco ISR Routers:
  - ISR 4000 Series: Enterprise branch gateways
  - ISR 1000 Series: Small branch connectivity
  - ASR 1000 Series: Service provider edge

Interface Types:
  - FXS: Foreign Exchange Station (analog phones)
  - FXO: Foreign Exchange Office (PSTN connection)
  - E1/T1: Digital trunk interfaces
  - SIP Trunks: IP-based carrier connections
```

### **Dial Peer Configuration**
```cisco
voice-port 0/1/0
 signal groundStart
 cptone US

dial-peer voice 1 pots
 destination-pattern 9T
 port 0/1/0
 forward-digits 7

dial-peer voice 2 voip
 destination-pattern 2...
 session target ipv4:10.1.1.10
 codec g711ulaw
 dtmf-relay h245-alphanumeric
```

## Common Troubleshooting Scenarios

### **Call Quality Issues**
```yaml
Symptoms:
  - Choppy/robotic audio
  - One-way audio
  - Audio delay/echo
  - Dropped calls

Investigation Steps:
  1. Check RTP statistics and packet loss
  2. Verify QoS configuration end-to-end
  3. Analyze jitter buffer performance
  4. Validate codec selection and transcoding
  5. Test network path with ping/traceroute
```

### **Registration Failures**
```yaml
Common Causes:
  - DNS resolution issues
  - Firewall blocking signaling ports
  - Authentication credential mismatch
  - Certificate validation failures
  - Network connectivity problems

Debug Commands:
  - debug ccsip messages
  - debug voice register
  - show sip-ua register status
  - show voice register pool
```

### **PSTN Connectivity Issues**
```yaml
Symptoms:
  - Calls not completing to PSTN
  - Incorrect caller ID presentation
  - DTMF not working
  - Busy signal on all calls

Validation Steps:
  1. Test analog/digital trunk connectivity
  2. Verify dial peer matching
  3. Check digit manipulation rules
  4. Validate carrier settings
  5. Monitor gateway debug output
```

## Monitoring and Diagnostics

### **CUCM Serviceability Tools**
```yaml
Real-Time Monitoring:
  - Device Status
  - Gateway Status
  - Call Activities
  - System Performance

Alert Configuration:
  - Service Down Alerts
  - High CPU/Memory Usage
  - Failed Registration Attempts
  - Call Quality Degradation
```

### **Voice Gateway Monitoring**
```cisco
show voice call summary
show voice dsp
show voice port summary
show call active voice brief
show dial-peer voice summary
debug voice ccapi inout
```

### **Network Analysis Tools**
```yaml
Packet Capture:
  - Wireshark/tshark for protocol analysis
  - CUCM built-in packet capture
  - Gateway embedded packet capture

Performance Testing:
  - SIP OPTIONS pings for connectivity
  - RTP stream analysis for quality
  - Bandwidth testing for capacity planning
```

## Security Considerations

### **SIP Security**
```yaml
Authentication:
  - Digest authentication for registration
  - TLS encryption for signaling
  - SRTP for media encryption

Firewall Configuration:
  - SIP: TCP/UDP 5060-5061
  - RTP: UDP 16384-32767 (configurable range)
  - SCCP: TCP 2000, 2443 (TLS)
  - HTTP/HTTPS: TCP 80, 443, 8080, 8443
```

### **Best Practices**
```yaml
Network Security:
  - Separate voice and data VLANs
  - QoS enforcement at network edge
  - Voice firewall with ALG support
  - Regular security patch management

Configuration Security:
  - Strong authentication credentials
  - Certificate-based authentication
  - Encrypted signaling protocols
  - Access control lists for management
```

This context provides the foundational knowledge needed for comprehensive VoIP troubleshooting and infrastructure management.