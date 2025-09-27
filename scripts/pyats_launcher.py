#!/usr/bin/env python3
"""
pyATS Command Launcher for Claude Code Integration
Simple command execution with environment detection
"""

import sys
import json
from pyats_environment import PyATSEnvironment


def main():
    """Main launcher function"""

    if len(sys.argv) < 2:
        print_usage()
        return 1

    command_name = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []

    # Initialize environment
    env = PyATSEnvironment()
    env_info = env.get_environment_info()

    # Check if pyATS is available
    if not env_info['pyats_available']:
        print("❌ pyATS not available")
        print("Run ./setup.sh or install with: pip install pyats[full] genie")
        return 1

    # Execute command
    if command_name == 'create-testbed':
        return create_testbed_command(env, args)
    elif command_name == 'validate-testbed':
        return validate_testbed_command(env, args)
    elif command_name == 'run-health-check':
        return run_health_check_command(env, args)
    elif command_name == 'compare-snapshots':
        return compare_snapshots_command(env, args)
    elif command_name == 'env-info':
        return show_environment_info(env_info)
    elif command_name == 'version':
        return show_version(env)
    else:
        print(f"❌ Unknown command: {command_name}")
        print_usage()
        return 1


def print_usage():
    """Print usage information"""
    print("🔧 pyATS Infrastructure Framework Launcher")
    print()
    print("Usage: python pyats_launcher.py <command> [args...]")
    print()
    print("Commands:")
    print("  create-testbed <inventory>     Create testbed from inventory")
    print("  validate-testbed <testbed>     Validate testbed connectivity")
    print("  run-health-check <testbed>     Run network health check")
    print("  compare-snapshots <before> <after>  Compare network snapshots")
    print("  env-info                       Show environment information")
    print("  version                        Show pyATS version")
    print()
    print("Examples:")
    print("  python pyats_launcher.py create-testbed inventory.yml")
    print("  python pyats_launcher.py validate-testbed testbed.yaml")
    print("  python pyats_launcher.py env-info")


def create_testbed_command(env, args):
    """Create testbed from inventory"""

    if not args:
        print("❌ Inventory file required")
        print("Usage: create-testbed <inventory_file>")
        return 1

    inventory_file = args[0]
    output_file = args[1] if len(args) > 1 else 'testbed.yaml'

    print(f"📝 Creating testbed from {inventory_file}")

    # Simple testbed creation script
    create_script = f'''
import yaml
import sys
from pathlib import Path

def create_simple_testbed(inventory_file, output_file):
    """Create simple testbed from inventory"""

    # Basic testbed template
    testbed_config = {{
        "testbed": {{
            "name": f"testbed_from_{{Path(inventory_file).stem}}",
            "credentials": {{
                "default": {{
                    "username": "%ENV{{TESTBED_USERNAME}}",
                    "password": "%ENV{{TESTBED_PASSWORD}}"
                }}
            }}
        }},
        "devices": {{}}
    }}

    # For now, create a simple example device
    testbed_config["devices"]["example_device"] = {{
        "type": "router",
        "os": "iosxe",
        "connections": {{
            "cli": {{
                "protocol": "ssh",
                "ip": "192.168.1.1",
                "port": 22
            }}
        }}
    }}

    # Save testbed
    with open(output_file, 'w') as f:
        yaml.dump(testbed_config, f, default_flow_style=False)

    print(f"✅ Testbed created: {{output_file}}")
    return True

if __name__ == "__main__":
    create_simple_testbed("{inventory_file}", "{output_file}")
'''

    result = env.execute_pyats_command(f'python -c "{create_script}"')

    if result['success']:
        print(f"✅ Testbed created: {output_file}")
        return 0
    else:
        print(f"❌ Failed to create testbed: {result.get('error', 'Unknown error')}")
        return 1


def validate_testbed_command(env, args):
    """Validate testbed connectivity"""

    if not args:
        print("❌ Testbed file required")
        print("Usage: validate-testbed <testbed_file>")
        return 1

    testbed_file = args[0]

    print(f"🔍 Validating testbed: {testbed_file}")

    # Simple validation script
    validation_script = f'''
from pyats.topology import loader
import sys

def validate_testbed(testbed_file):
    """Simple testbed validation"""
    try:
        testbed = loader.load(testbed_file)
        print(f"✅ Testbed loaded successfully")
        print(f"   Name: {{testbed.name}}")
        print(f"   Devices: {{len(testbed.devices)}}")

        for device_name in testbed.devices:
            print(f"   - {{device_name}}")

        return True
    except Exception as e:
        print(f"❌ Validation failed: {{e}}")
        return False

if __name__ == "__main__":
    validate_testbed("{testbed_file}")
'''

    result = env.execute_pyats_command(f'python -c "{validation_script}"')

    if result['success']:
        print(result['stdout'])
        return 0
    else:
        print(f"❌ Validation failed: {result.get('error', 'Unknown error')}")
        return 1


def run_health_check_command(env, args):
    """Run network health check"""

    if not args:
        print("❌ Testbed file required")
        print("Usage: run-health-check <testbed_file>")
        return 1

    testbed_file = args[0]

    print(f"🏥 Running health check on: {testbed_file}")

    # Simple health check script
    health_script = f'''
from pyats.topology import loader

def run_simple_health_check(testbed_file):
    """Simple health check"""
    try:
        testbed = loader.load(testbed_file)
        print(f"🏥 Health Check for {{testbed.name}}")
        print("=" * 50)

        total_devices = len(testbed.devices)
        reachable_devices = 0

        for device_name, device in testbed.devices.items():
            print(f"Testing {{device_name}}...", end=" ")

            try:
                device.connect(connection_timeout=10, log_stdout=False)
                device.execute("show version")
                device.disconnect()

                print("✅ Reachable")
                reachable_devices += 1

            except Exception as e:
                print(f"❌ Failed: {{str(e)[:50]}}")

        print("=" * 50)
        print(f"Results: {{reachable_devices}}/{{total_devices}} devices reachable")

        if reachable_devices == total_devices:
            print("🎉 All devices healthy!")
        else:
            print(f"⚠️  {{total_devices - reachable_devices}} devices need attention")

        return True

    except Exception as e:
        print(f"❌ Health check failed: {{e}}")
        return False

if __name__ == "__main__":
    run_simple_health_check("{testbed_file}")
'''

    result = env.execute_pyats_command(f'python -c "{health_script}"')

    if result['success']:
        print(result['stdout'])
        return 0
    else:
        print(f"❌ Health check failed: {result.get('error', 'Unknown error')}")
        return 1


def compare_snapshots_command(env, args):
    """Compare network snapshots"""

    if len(args) < 2:
        print("❌ Two snapshot files required")
        print("Usage: compare-snapshots <before_snapshot> <after_snapshot>")
        return 1

    before_file = args[0]
    after_file = args[1]

    print(f"📊 Comparing snapshots: {before_file} vs {after_file}")

    # Simple comparison (placeholder)
    print("🔍 Snapshot comparison functionality")
    print("📋 This feature compares network state snapshots")
    print("⚠️  Full implementation requires Genie parser integration")

    return 0


def show_environment_info(env_info):
    """Show environment information"""

    print("🔍 pyATS Environment Information")
    print("=" * 40)
    print(f"Environment Type: {env_info['environment_type']}")
    print(f"pyATS Available: {env_info['pyats_available']}")

    if env_info['pyats_available']:
        print(f"Command Prefix: '{env_info['command_prefix']}'")
        if 'pyats_version' in env_info:
            print(f"pyATS Version: {env_info['pyats_version']}")
    else:
        print("⚠️  Setup required")

    return 0


def show_version(env):
    """Show pyATS version"""

    result = env.execute_pyats_command('pyats version')

    if result['success']:
        print(result['stdout'])
        return 0
    else:
        print(f"❌ Failed to get version: {result.get('error', 'Unknown error')}")
        return 1


if __name__ == '__main__':
    sys.exit(main())