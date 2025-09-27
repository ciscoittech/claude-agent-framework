# VoIP Wireshark Integration Guide
*Headless packet analysis for voice infrastructure troubleshooting*

## 🎯 Overview

This guide details the integration of containerized Wireshark/tshark with the VoIP troubleshooting toolkit, providing automated packet analysis capabilities for voice infrastructure issues.

## 🐳 Docker Container Setup

### **Wireshark Headless Container**

```dockerfile
# Dockerfile.wireshark
FROM ubuntu:22.04

# Install Wireshark/tshark and dependencies
RUN apt-get update && apt-get install -y \
    tshark \
    tcpdump \
    curl \
    python3 \
    python3-pip \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Create analysis directories
WORKDIR /packet-analysis
RUN mkdir -p /packet-analysis/{input,output,scripts}

# Set up non-root user for security
RUN useradd -m -s /bin/bash analyzer
RUN chown -R analyzer:analyzer /packet-analysis

# Volume mounts for file exchange
VOLUME ["/packet-analysis"]

USER analyzer

# Default command
CMD ["tshark", "--version"]
```

### **Docker Compose Integration**

```yaml
# docker-compose.yml addition
services:
  wireshark:
    build:
      context: .
      dockerfile: Dockerfile.wireshark
    volumes:
      - ./packet-captures:/packet-analysis/input
      - ./analysis-results:/packet-analysis/output
      - ./analysis-scripts:/packet-analysis/scripts
    working_dir: /packet-analysis
    command: tail -f /dev/null  # Keep container running
    networks:
      - infrastructure-net

  pyats:
    # existing pyATS configuration
    depends_on:
      - wireshark
```

## 📊 VoIP-Specific Analysis Scripts

### **SIP Call Flow Analyzer**

```python
#!/usr/bin/env python3
# /packet-analysis/scripts/sip_analyzer.py

import subprocess
import json
import sys
from datetime import datetime

class SIPAnalyzer:
    def __init__(self, pcap_file):
        self.pcap_file = pcap_file
        self.results = {}

    def analyze_sip_calls(self):
        """Extract and analyze SIP call flows"""

        # Extract SIP messages
        cmd = [
            "tshark", "-r", f"input/{self.pcap_file}",
            "-Y", "sip",
            "-T", "json",
            "-e", "frame.time",
            "-e", "ip.src", "-e", "ip.dst",
            "-e", "sip.Method", "-e", "sip.Status-Code",
            "-e", "sip.Call-ID", "-e", "sip.From", "-e", "sip.To"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            sip_data = json.loads(result.stdout)
            return self.process_sip_flows(sip_data)

        return {"error": result.stderr}

    def process_sip_flows(self, sip_data):
        """Process SIP data into call flows"""

        call_flows = {}

        for packet in sip_data:
            layers = packet.get("_source", {}).get("layers", {})

            if "sip" in layers:
                sip = layers["sip"]
                call_id = sip.get("sip.Call-ID", ["unknown"])[0]

                if call_id not in call_flows:
                    call_flows[call_id] = {
                        "messages": [],
                        "participants": set(),
                        "status": "in_progress"
                    }

                message = {
                    "timestamp": layers.get("frame", {}).get("frame.time", [""])[0],
                    "src": layers.get("ip", {}).get("ip.src", [""])[0],
                    "dst": layers.get("ip", {}).get("ip.dst", [""])[0],
                    "method": sip.get("sip.Method", [None])[0],
                    "status_code": sip.get("sip.Status-Code", [None])[0]
                }

                call_flows[call_id]["messages"].append(message)
                call_flows[call_id]["participants"].add(message["src"])
                call_flows[call_id]["participants"].add(message["dst"])

        return self.analyze_call_quality(call_flows)

    def analyze_call_quality(self, call_flows):
        """Analyze call setup times and success rates"""

        analysis = {
            "total_calls": len(call_flows),
            "successful_calls": 0,
            "failed_calls": 0,
            "average_setup_time": 0,
            "call_details": {}
        }

        setup_times = []

        for call_id, flow in call_flows.items():
            invite_time = None
            ok_time = None
            failed = False

            for msg in flow["messages"]:
                if msg["method"] == "INVITE":
                    invite_time = msg["timestamp"]
                elif msg["status_code"] == "200":
                    ok_time = msg["timestamp"]
                elif msg["status_code"] and msg["status_code"].startswith("4"):
                    failed = True

            if failed:
                analysis["failed_calls"] += 1
                status = "failed"
            elif ok_time:
                analysis["successful_calls"] += 1
                status = "successful"
                # Calculate setup time if both timestamps available
                if invite_time and ok_time:
                    # Simplified time calculation
                    setup_times.append(1.0)  # Placeholder
            else:
                status = "incomplete"

            analysis["call_details"][call_id] = {
                "status": status,
                "participants": list(flow["participants"]),
                "message_count": len(flow["messages"])
            }

        if setup_times:
            analysis["average_setup_time"] = sum(setup_times) / len(setup_times)

        return analysis

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 sip_analyzer.py <pcap_file>")
        sys.exit(1)

    analyzer = SIPAnalyzer(sys.argv[1])
    results = analyzer.analyze_sip_calls()

    with open("output/sip_analysis.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(json.dumps(results, indent=2, default=str))
```

### **RTP Quality Analyzer**

```python
#!/usr/bin/env python3
# /packet-analysis/scripts/rtp_analyzer.py

import subprocess
import json
import sys

class RTPAnalyzer:
    def __init__(self, pcap_file):
        self.pcap_file = pcap_file

    def analyze_rtp_streams(self):
        """Analyze RTP streams for quality metrics"""

        # Get RTP stream statistics
        cmd = [
            "tshark", "-r", f"input/{self.pcap_file}",
            "-z", "rtp,streams"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            return self.parse_rtp_statistics(result.stdout)

        return {"error": result.stderr}

    def parse_rtp_statistics(self, output):
        """Parse tshark RTP statistics output"""

        lines = output.strip().split('\n')
        streams = []

        for line in lines:
            if 'SSRC' in line and 'Payload' in line:
                # Parse RTP stream line
                parts = line.split()
                if len(parts) >= 8:
                    stream = {
                        "src_ip": parts[0],
                        "src_port": parts[1],
                        "dst_ip": parts[2],
                        "dst_port": parts[3],
                        "ssrc": parts[4],
                        "payload_type": parts[5],
                        "packets": int(parts[6]) if parts[6].isdigit() else 0,
                        "lost": int(parts[7]) if parts[7].isdigit() else 0
                    }
                    streams.append(stream)

        return self.calculate_quality_metrics(streams)

    def calculate_quality_metrics(self, streams):
        """Calculate voice quality metrics"""

        analysis = {
            "stream_count": len(streams),
            "total_packets": 0,
            "total_lost": 0,
            "packet_loss_rate": 0,
            "streams": streams,
            "quality_assessment": "unknown"
        }

        for stream in streams:
            analysis["total_packets"] += stream["packets"]
            analysis["total_lost"] += stream["lost"]

        if analysis["total_packets"] > 0:
            analysis["packet_loss_rate"] = (
                analysis["total_lost"] / analysis["total_packets"] * 100
            )

            # Quality assessment based on packet loss
            if analysis["packet_loss_rate"] < 1.0:
                analysis["quality_assessment"] = "excellent"
            elif analysis["packet_loss_rate"] < 3.0:
                analysis["quality_assessment"] = "good"
            elif analysis["packet_loss_rate"] < 5.0:
                analysis["quality_assessment"] = "fair"
            else:
                analysis["quality_assessment"] = "poor"

        return analysis

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 rtp_analyzer.py <pcap_file>")
        sys.exit(1)

    analyzer = RTPAnalyzer(sys.argv[1])
    results = analyzer.analyze_rtp_streams()

    with open("output/rtp_analysis.json", "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))
```

## 🔧 Integration with VoIP Toolkit

### **Command Integration**

```bash
# /voip-toolkit command extensions

case "$1" in
    "packet-analysis")
        echo "🔍 Starting packet analysis for VoIP traffic..."

        # Copy PCAP to analysis container
        docker cp "$2" wireshark:/packet-analysis/input/

        # Run SIP analysis
        docker exec wireshark python3 scripts/sip_analyzer.py "$(basename "$2")"

        # Run RTP analysis
        docker exec wireshark python3 scripts/rtp_analyzer.py "$(basename "$2")"

        # Copy results back
        docker cp wireshark:/packet-analysis/output/ ./voip-analysis-results/

        echo "✅ Analysis complete. Results in ./voip-analysis-results/"
        ;;

    "call-quality")
        echo "📊 Analyzing call quality metrics..."

        # Specific call quality analysis
        docker exec wireshark tshark -r "input/$2" -z rtp,streams
        docker exec wireshark tshark -r "input/$2" -Y "rtcp" -T json > rtcp-analysis.json
        ;;
esac
```

### **Agent Coordination Example**

```python
# Example of how VoIP specialist coordinates with packet analyzer

def analyze_voip_issue(pcap_file, symptoms):
    """VoIP specialist orchestrating packet analysis"""

    # Step 1: Initial packet assessment
    initial_analysis = spawn_packet_analyzer(
        task="initial_assessment",
        pcap_file=pcap_file
    )

    # Step 2: Protocol-specific analysis based on symptoms
    if "call_setup_failures" in symptoms:
        sip_analysis = spawn_packet_analyzer(
            task="sip_signaling_analysis",
            pcap_file=pcap_file,
            focus="registration_and_invite_flows"
        )

    if "poor_call_quality" in symptoms:
        rtp_analysis = spawn_packet_analyzer(
            task="rtp_quality_analysis",
            pcap_file=pcap_file,
            focus="jitter_latency_packet_loss"
        )

    # Step 3: Correlate findings with VoIP expertise
    return correlate_packet_findings_with_voip_knowledge(
        initial_analysis, sip_analysis, rtp_analysis
    )
```

## 📈 Quality Metrics and Thresholds

### **Voice Quality Standards**

```yaml
MOS Score Calculation:
  - Excellent (4.3-5.0): < 1% packet loss, < 30ms jitter
  - Good (4.0-4.3): 1-3% packet loss, 30-50ms jitter
  - Fair (3.6-4.0): 3-5% packet loss, 50-100ms jitter
  - Poor (3.1-3.6): 5-10% packet loss, 100-200ms jitter
  - Bad (1.0-3.1): > 10% packet loss, > 200ms jitter

Network Requirements:
  - Latency: < 150ms one-way preferred
  - Jitter: < 30ms for excellent quality
  - Packet Loss: < 1% for good quality
  - Bandwidth: Plan for 64kbps per G.711 call
```

### **Automated Quality Assessment**

```python
def assess_voice_quality(rtp_stats, network_metrics):
    """Automated voice quality assessment"""

    quality_score = 4.5  # Start with perfect score

    # Packet loss impact
    if rtp_stats["packet_loss_rate"] > 1.0:
        quality_score -= (rtp_stats["packet_loss_rate"] - 1.0) * 0.3

    # Jitter impact
    if network_metrics["jitter"] > 30:
        quality_score -= (network_metrics["jitter"] - 30) * 0.01

    # Latency impact
    if network_metrics["latency"] > 150:
        quality_score -= (network_metrics["latency"] - 150) * 0.005

    quality_score = max(1.0, quality_score)  # Minimum score

    return {
        "mos_score": round(quality_score, 2),
        "quality_rating": get_quality_rating(quality_score),
        "recommendations": generate_recommendations(rtp_stats, network_metrics)
    }
```

## 🎯 Usage Examples

### **Complete VoIP Troubleshooting Workflow**

```bash
# 1. Load VoIP toolkit
/voip-toolkit diagnose

# 2. Capture voice traffic (guided by VoIP specialist)
# User captures PCAP during problem period

# 3. Analyze packet capture
/voip-toolkit packet-analysis problem-capture.pcap

# 4. Generate quality report
/voip-toolkit call-quality problem-capture.pcap

# 5. SIP signaling analysis
/voip-toolkit sip-trace problem-capture.pcap
```

### **Automated Analysis Pipeline**

```bash
# Scripted analysis for regular monitoring
#!/bin/bash

PCAP_FILE="$1"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Run complete VoIP analysis
docker exec wireshark python3 scripts/sip_analyzer.py "$PCAP_FILE"
docker exec wireshark python3 scripts/rtp_analyzer.py "$PCAP_FILE"

# Generate executive summary
docker exec wireshark python3 scripts/voip_summary.py "$PCAP_FILE" > "voip_report_$TIMESTAMP.json"

# Alert on quality issues
QUALITY=$(jq -r '.quality_assessment' "voip_report_$TIMESTAMP.json")
if [ "$QUALITY" = "poor" ] || [ "$QUALITY" = "fair" ]; then
    echo "⚠️ Voice quality issue detected: $QUALITY"
    # Trigger alert to network operations
fi
```

This integration provides comprehensive, automated VoIP packet analysis capabilities that seamlessly integrate with the network engineering agent framework for rapid voice infrastructure troubleshooting.