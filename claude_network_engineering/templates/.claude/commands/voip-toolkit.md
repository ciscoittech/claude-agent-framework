# VoIP Troubleshooting Toolkit

Load the comprehensive VoIP troubleshooting workflow with packet analysis, call quality assessment, and voice infrastructure diagnostics.

## Usage
```
/voip-toolkit [operation] [target]
```

## Operations
- `diagnose` - Complete VoIP system health check
- `call-quality` - Analyze call quality metrics and RTP streams
- `packet-analysis` - Deep packet inspection for voice traffic
- `sip-trace` - SIP signaling analysis and troubleshooting
- `codec-analysis` - Audio codec performance and compatibility
- `jitter-buffer` - Buffer analysis and optimization recommendations

## Examples
```bash
# Complete VoIP system diagnosis
/voip-toolkit diagnose cucm-cluster

# Analyze call quality from PCAP
/voip-toolkit call-quality capture.pcap

# SIP signaling troubleshooting
/voip-toolkit sip-trace "registration-failures"

# Codec analysis for bandwidth optimization
/voip-toolkit codec-analysis "g711-to-g729-migration"
```

## What This Loads
1. **VoIP Specialist Agent** - Expert in Cisco CUCM, voice gateways, SIP
2. **Packet Analysis Agent** - Wireshark/tshark automation for voice traffic
3. **Call Quality Agent** - RTP stream analysis, MOS scoring, jitter/latency
4. **SIP Protocol Agent** - SIP message analysis, registration troubleshooting
5. **Voice Infrastructure Context** - CUCM configs, gateway patterns, QoS policies

## Workflow Stages
1. **Assessment** - Gather symptoms and system information
2. **Packet Capture** - Guide capture strategy for voice traffic
3. **Analysis** - Multi-agent analysis of voice protocols
4. **Diagnosis** - Root cause identification with evidence
5. **Remediation** - Specific configuration recommendations
6. **Validation** - Verify fixes and performance improvements

## Integration Points
- **pyATS Integration** - Automated device configuration validation
- **Wireshark Container** - Headless packet analysis capabilities
- **CUCM APIs** - Direct integration with Cisco voice infrastructure
- **Expert Escalation** - TAC case preparation for complex issues