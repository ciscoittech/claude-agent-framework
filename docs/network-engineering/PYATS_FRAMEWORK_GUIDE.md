# pyATS Framework Integration Guide
*Transform your infrastructure automation with Cisco's pyATS testing framework*

## 🎯 Overview

This guide details how the Claude Infrastructure Agent Framework integrates with Cisco's pyATS (Python Automation Test System) to provide enterprise-grade network testing, validation, and automation capabilities. pyATS brings structured, data-driven testing to infrastructure operations.

## 🏗️ Architecture Integration

### Core pyATS Components

#### **1. pyATS Framework**
- **Test orchestration engine**: Manages test execution lifecycle
- **Device abstraction**: Platform-agnostic device connectivity
- **Result aggregation**: Comprehensive test reporting
- **Plugin architecture**: Extensible via custom libraries

#### **2. Genie Library**
- **1000+ parsers**: Structured output parsing for network commands
- **Device models**: Platform-agnostic Python objects
- **State comparison**: Network state diff capabilities
- **Health validation**: Built-in health check functions

#### **3. XPRESSO Dashboard**
- **Web interface**: Test management and visualization
- **Result tracking**: Historical test execution data
- **Environment management**: Testbed and device inventory
- **Report generation**: Automated test documentation

### Framework Integration Points

```python
# pyATS Integration Architecture
PYATS_INTEGRATION = {
    'testbed_management': 'pyats-testbed-manager agent',
    'data_parsing': 'genie-parser agent',
    'test_orchestration': 'test-orchestrator agent',
    'network_profiling': 'network-profiler agent',
    'validation_workflows': 'automated test execution',
    'reporting': 'XPRESSO dashboard integration'
}
```

## 🚀 Quick Start with pyATS

### Installation and Setup

```bash
# Install pyATS and Genie
pip install pyats[full]
pip install genie

# Verify installation
pyats version
genie --help
```

### Basic Testbed Configuration

```yaml
# testbed.yaml - Core connectivity configuration
testbed:
  name: infrastructure_testbed

devices:
  router1:
    type: router
    os: iosxe
    credentials:
      default:
        username: admin
        password: admin
    connections:
      cli:
        protocol: ssh
        ip: 192.168.1.10
        port: 22

  switch1:
    type: switch
    os: iosxe
    credentials:
      default:
        username: admin
        password: admin
    connections:
      cli:
        protocol: ssh
        ip: 192.168.1.20
        port: 22

topology:
  router1:
    interfaces:
      GigabitEthernet0/0/1:
        type: ethernet
        link: link1
  switch1:
    interfaces:
      GigabitEthernet1/0/1:
        type: ethernet
        link: link1
```

### Device Connection and Basic Operations

```python
# Basic pyATS device operations
from pyats.topology import loader
from genie.libs.parser.utils.common import ParserNotFound

# Load testbed
testbed = loader.load('testbed.yaml')

# Connect to device
device = testbed.devices['router1']
device.connect()

# Execute and parse commands
try:
    # Structured output via Genie parsers
    version_output = device.parse('show version')
    interface_output = device.parse('show interfaces')

    # Raw command output when needed
    raw_output = device.execute('show running-config')

except ParserNotFound:
    # Fallback to raw output
    raw_output = device.execute('show version')

# Disconnect
device.disconnect()
```

## 🔧 Agent Integration Patterns

### Pattern 1: Testbed Management

```python
class PyATSTestbedManager:
    """
    Manages dynamic testbed creation and device connectivity
    """

    def __init__(self, inventory_source='ansible'):
        self.inventory_source = inventory_source
        self.testbed_template = self._load_testbed_template()

    def generate_testbed_from_inventory(self, ansible_inventory_path):
        """
        Convert Ansible inventory to pyATS testbed format

        Args:
            ansible_inventory_path: Path to Ansible inventory file

        Returns:
            Generated testbed dictionary
        """

        from ansible.inventory.manager import InventoryManager
        from ansible.parsing.dataloader import DataLoader

        loader = DataLoader()
        inventory = InventoryManager(loader=loader, sources=ansible_inventory_path)

        testbed_config = {
            'testbed': {
                'name': 'auto_generated_testbed'
            },
            'devices': {}
        }

        # Convert inventory hosts to pyATS devices
        for host_name in inventory.hosts:
            host = inventory.hosts[host_name]
            host_vars = host.get_vars()

            device_config = {
                'type': self._determine_device_type(host_vars),
                'os': self._determine_device_os(host_vars),
                'credentials': {
                    'default': {
                        'username': host_vars.get('ansible_user', 'admin'),
                        'password': host_vars.get('ansible_password', 'admin')
                    }
                },
                'connections': {
                    'cli': {
                        'protocol': 'ssh',
                        'ip': host_vars.get('ansible_host', host_name),
                        'port': host_vars.get('ansible_port', 22)
                    }
                }
            }

            testbed_config['devices'][host_name] = device_config

        return testbed_config

    def validate_testbed_connectivity(self, testbed_config):
        """
        Validate all devices in testbed are reachable

        Returns:
            Connectivity validation results
        """

        testbed = loader.load(testbed_config)
        validation_results = {}

        for device_name, device in testbed.devices.items():
            try:
                device.connect(log_stdout=False)

                # Basic connectivity test
                output = device.execute('show version')

                validation_results[device_name] = {
                    'status': 'connected',
                    'connection_time': device.connectionmgr.connections['cli'].connection_time,
                    'device_info': self._extract_device_info(output)
                }

                device.disconnect()

            except Exception as e:
                validation_results[device_name] = {
                    'status': 'failed',
                    'error': str(e),
                    'recommendations': self._generate_connectivity_recommendations(e)
                }

        return validation_results
```

### Pattern 2: Genie Parser Integration

```python
class GenieParserAgent:
    """
    Leverages Genie's 1000+ parsers for structured data extraction
    """

    def __init__(self, testbed_file):
        self.testbed = loader.load(testbed_file)
        self.supported_parsers = self._discover_supported_parsers()

    def parse_device_state(self, device_name, commands):
        """
        Parse multiple commands and return structured data

        Args:
            device_name: Target device
            commands: List of commands to parse

        Returns:
            Structured parsed output
        """

        device = self.testbed.devices[device_name]
        device.connect()

        parsed_outputs = {}

        for command in commands:
            try:
                # Use Genie parser for structured output
                parsed_output = device.parse(command)
                parsed_outputs[command] = {
                    'status': 'parsed',
                    'data': parsed_output,
                    'parser_used': True
                }

            except ParserNotFound:
                # Fallback to raw output
                raw_output = device.execute(command)
                parsed_outputs[command] = {
                    'status': 'raw',
                    'data': raw_output,
                    'parser_used': False,
                    'recommendation': f'Consider creating custom parser for: {command}'
                }

        device.disconnect()
        return parsed_outputs

    def compare_device_states(self, device_name, before_snapshot, after_snapshot):
        """
        Compare two device state snapshots

        Returns:
            Detailed diff analysis
        """

        from genie.utils.diff import Diff

        diff_results = {}

        for command in before_snapshot.keys():
            if command in after_snapshot:
                diff = Diff(before_snapshot[command]['data'],
                           after_snapshot[command]['data'])
                diff.findDiff()

                diff_results[command] = {
                    'changes_detected': len(diff.diffs) > 0,
                    'diff_details': diff.diffs,
                    'summary': self._summarize_differences(diff.diffs)
                }

        return diff_results

    def generate_health_report(self, device_name):
        """
        Generate comprehensive device health report using Genie

        Returns:
            Health assessment with recommendations
        """

        device = self.testbed.devices[device_name]
        device.connect()

        # Standard health check commands
        health_commands = [
            'show version',
            'show interfaces',
            'show ip route summary',
            'show processes cpu',
            'show memory statistics',
            'show logging',
            'show environment'
        ]

        health_data = {}

        for command in health_commands:
            try:
                parsed_output = device.parse(command)
                health_data[command] = parsed_output
            except ParserNotFound:
                # Skip commands without parsers
                continue

        device.disconnect()

        # Analyze health metrics
        health_analysis = self._analyze_health_metrics(health_data)

        return health_analysis
```

### Pattern 3: Test Orchestration

```python
class TestOrchestrator:
    """
    Orchestrates complex test scenarios using pyATS framework
    """

    def __init__(self, testbed_file):
        self.testbed = loader.load(testbed_file)
        self.test_results = {}

    def execute_network_validation_suite(self):
        """
        Execute comprehensive network validation test suite

        Returns:
            Complete test execution results
        """

        from pyats.aetest import AEtest
        import logging

        test_suite = {
            'connectivity_tests': self._connectivity_test_suite(),
            'configuration_tests': self._configuration_validation_suite(),
            'performance_tests': self._performance_test_suite(),
            'security_tests': self._security_validation_suite()
        }

        execution_results = {}

        for suite_name, test_cases in test_suite.items():
            logging.info(f"Executing {suite_name}")

            suite_results = []

            for test_case in test_cases:
                result = self._execute_test_case(test_case)
                suite_results.append(result)

            execution_results[suite_name] = {
                'total_tests': len(test_cases),
                'passed': len([r for r in suite_results if r['status'] == 'passed']),
                'failed': len([r for r in suite_results if r['status'] == 'failed']),
                'details': suite_results
            }

        return execution_results

    def _connectivity_test_suite(self):
        """
        Define connectivity validation tests
        """

        return [
            {
                'name': 'device_reachability',
                'description': 'Verify all devices are reachable',
                'test_function': self._test_device_reachability
            },
            {
                'name': 'interface_status',
                'description': 'Verify critical interfaces are up',
                'test_function': self._test_interface_status
            },
            {
                'name': 'routing_convergence',
                'description': 'Verify routing protocol convergence',
                'test_function': self._test_routing_convergence
            }
        ]

    def _test_device_reachability(self):
        """
        Test that all testbed devices are reachable
        """

        results = []

        for device_name, device in self.testbed.devices.items():
            try:
                device.connect(connection_timeout=30)

                # Basic command to verify functionality
                device.execute('show version')

                results.append({
                    'device': device_name,
                    'status': 'passed',
                    'message': 'Device is reachable and responsive'
                })

                device.disconnect()

            except Exception as e:
                results.append({
                    'device': device_name,
                    'status': 'failed',
                    'message': f'Device unreachable: {str(e)}'
                })

        # Overall test result
        all_passed = all(r['status'] == 'passed' for r in results)

        return {
            'status': 'passed' if all_passed else 'failed',
            'details': results,
            'summary': f"{len([r for r in results if r['status'] == 'passed'])}/{len(results)} devices reachable"
        }
```

## 📊 Network State Management

### State Collection and Baseline

```python
class NetworkProfiler:
    """
    Manages network state collection and baseline establishment
    """

    def __init__(self, testbed_file):
        self.testbed = loader.load(testbed_file)
        self.baseline_commands = [
            'show version',
            'show interfaces',
            'show ip route',
            'show ip arp',
            'show mac address-table',
            'show spanning-tree',
            'show vlan',
            'show running-config'
        ]

    def collect_network_baseline(self, save_to_file=True):
        """
        Collect comprehensive network baseline

        Returns:
            Complete network state baseline
        """

        import json
        from datetime import datetime

        baseline_data = {
            'collection_time': datetime.now().isoformat(),
            'testbed_name': self.testbed.name,
            'devices': {}
        }

        for device_name, device in self.testbed.devices.items():
            print(f"Collecting baseline from {device_name}")

            device.connect()
            device_baseline = {}

            for command in self.baseline_commands:
                try:
                    # Try structured parsing first
                    parsed_output = device.parse(command)
                    device_baseline[command] = {
                        'type': 'parsed',
                        'data': parsed_output
                    }
                except ParserNotFound:
                    # Fall back to raw output
                    raw_output = device.execute(command)
                    device_baseline[command] = {
                        'type': 'raw',
                        'data': raw_output
                    }

            baseline_data['devices'][device_name] = device_baseline
            device.disconnect()

        if save_to_file:
            filename = f"network_baseline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(baseline_data, f, indent=2, default=str)

            baseline_data['saved_to'] = filename

        return baseline_data

    def compare_against_baseline(self, baseline_file, current_state=None):
        """
        Compare current network state against saved baseline

        Returns:
            Detailed comparison results
        """

        import json
        from genie.utils.diff import Diff

        # Load baseline
        with open(baseline_file, 'r') as f:
            baseline_data = json.load(f)

        # Collect current state if not provided
        if current_state is None:
            current_state = self.collect_network_baseline(save_to_file=False)

        comparison_results = {
            'baseline_time': baseline_data['collection_time'],
            'current_time': current_state['collection_time'],
            'devices_compared': len(baseline_data['devices']),
            'changes_detected': False,
            'device_changes': {}
        }

        # Compare each device
        for device_name in baseline_data['devices']:
            if device_name in current_state['devices']:
                device_diff = self._compare_device_state(
                    baseline_data['devices'][device_name],
                    current_state['devices'][device_name]
                )

                if device_diff['has_changes']:
                    comparison_results['changes_detected'] = True
                    comparison_results['device_changes'][device_name] = device_diff

        return comparison_results
```

## 🔄 Workflow Commands

### Command Integration Examples

```python
# /create-testbed command implementation
def create_testbed_command(inventory_source, output_file='testbed.yaml'):
    """
    Generate pyATS testbed from various inventory sources
    """

    testbed_manager = PyATSTestbedManager()

    if inventory_source.endswith('.yml') or inventory_source.endswith('.yaml'):
        # Ansible inventory
        testbed_config = testbed_manager.generate_testbed_from_inventory(inventory_source)
    else:
        # Other inventory sources (CSV, database, etc.)
        testbed_config = testbed_manager.generate_from_custom_source(inventory_source)

    # Save testbed file
    import yaml
    with open(output_file, 'w') as f:
        yaml.dump(testbed_config, f, default_flow_style=False)

    # Validate connectivity
    validation_results = testbed_manager.validate_testbed_connectivity(testbed_config)

    return {
        'testbed_file': output_file,
        'devices_configured': len(testbed_config['devices']),
        'connectivity_validation': validation_results
    }

# /run-health-check command implementation
def run_health_check_command(testbed_file, devices='all', save_report=True):
    """
    Execute comprehensive health check across network devices
    """

    parser_agent = GenieParserAgent(testbed_file)

    if devices == 'all':
        testbed = loader.load(testbed_file)
        target_devices = list(testbed.devices.keys())
    else:
        target_devices = devices.split(',')

    health_results = {}

    for device_name in target_devices:
        health_report = parser_agent.generate_health_report(device_name)
        health_results[device_name] = health_report

    # Generate summary report
    summary = {
        'devices_checked': len(target_devices),
        'healthy_devices': len([d for d in health_results.values() if d['overall_health'] == 'healthy']),
        'devices_with_issues': len([d for d in health_results.values() if d['overall_health'] != 'healthy']),
        'detailed_results': health_results
    }

    if save_report:
        report_file = f"health_check_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        summary['report_saved_to'] = report_file

    return summary
```

## 🎯 Best Practices

### 1. Testbed Design
- **Modular testbeds**: Separate files for different environments
- **Credential management**: Use external credential stores
- **Connection pooling**: Reuse connections across tests
- **Error handling**: Graceful fallbacks for connectivity issues

### 2. Parser Utilization
- **Prefer structured data**: Use Genie parsers when available
- **Fallback gracefully**: Handle ParserNotFound exceptions
- **Custom parsers**: Create parsers for unsupported commands
- **Data validation**: Verify parsed data integrity

### 3. Test Development
- **Atomic tests**: Each test should validate one specific aspect
- **Parallel execution**: Run independent tests concurrently
- **State isolation**: Tests shouldn't depend on each other
- **Comprehensive assertions**: Validate expected vs actual results

### 4. Performance Optimization
- **Connection reuse**: Maintain device connections across tests
- **Selective parsing**: Only parse necessary command outputs
- **Caching**: Cache static device information
- **Parallel collection**: Collect data from multiple devices simultaneously

## 🔧 Troubleshooting Guide

### Common Issues and Solutions

#### **Connection Failures**
```python
# Issue: Device connection timeout
# Solution: Adjust connection parameters
device_config = {
    'connections': {
        'cli': {
            'protocol': 'ssh',
            'ip': '192.168.1.1',
            'port': 22,
            'timeout': 60,  # Increase timeout
            'connection_timeout': 30
        }
    }
}
```

#### **Parser Errors**
```python
# Issue: ParserNotFound for specific commands
# Solution: Implement graceful fallback
try:
    parsed_output = device.parse('show custom-command')
except ParserNotFound:
    raw_output = device.execute('show custom-command')
    # Optional: Create custom parser
    parsed_output = custom_parser(raw_output)
```

#### **Memory Management**
```python
# Issue: Memory usage with large testbeds
# Solution: Implement connection pooling
class ConnectionPool:
    def __init__(self, max_connections=10):
        self.pool = {}
        self.max_connections = max_connections

    def get_connection(self, device_name):
        if len(self.pool) >= self.max_connections:
            # Close oldest connection
            oldest = min(self.pool.items(), key=lambda x: x[1]['last_used'])
            self.pool[oldest[0]]['device'].disconnect()
            del self.pool[oldest[0]]

        # Create or reuse connection
        # Implementation details...
```

This comprehensive guide provides the foundation for integrating pyATS throughout the infrastructure framework, transforming it into a enterprise-grade testing and automation system.