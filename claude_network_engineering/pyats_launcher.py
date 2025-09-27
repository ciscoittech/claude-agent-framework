#!/usr/bin/env python3
"""
pyATS Launcher - Integrated with Claude Agent Framework
Network Engineering Edition
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from rich.console import Console
from rich.table import Table
import click

console = Console()

def detect_environment():
    """Detect the current environment and pyATS availability."""
    env_info = {
        'platform': platform.system(),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'pyats_available': False,
        'genie_available': False,
        'docker_available': False,
        'environment_type': 'local'
    }

    # Check for pyATS
    try:
        import pyats
        env_info['pyats_available'] = True
        env_info['pyats_version'] = pyats.__version__
    except ImportError:
        pass

    # Check for Genie
    try:
        import genie
        env_info['genie_available'] = True
        env_info['genie_version'] = genie.__version__
    except ImportError:
        pass

    # Check for Docker
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            env_info['docker_available'] = True
            env_info['docker_version'] = result.stdout.strip()
    except FileNotFoundError:
        pass

    # Determine environment type
    if os.path.exists('/.dockerenv'):
        env_info['environment_type'] = 'docker'
    elif env_info['docker_available']:
        env_info['environment_type'] = 'docker-host'

    return env_info

def run_pyats_command(command, args=None):
    """Execute a pyATS command with proper error handling."""
    if args is None:
        args = []

    env_info = detect_environment()

    if not env_info['pyats_available']:
        console.print("❌ pyATS not installed. Install with:", style="red")
        console.print("   pip install pyats[full] genie", style="cyan")
        return False

    try:
        cmd = ['pyats', command] + args
        console.print(f"🚀 Running: {' '.join(cmd)}")

        result = subprocess.run(cmd, check=True)
        return result.returncode == 0

    except subprocess.CalledProcessError as e:
        console.print(f"❌ Command failed with exit code {e.returncode}", style="red")
        return False
    except FileNotFoundError:
        console.print("❌ pyATS command not found in PATH", style="red")
        return False

@click.group()
def cli():
    """pyATS Launcher for Claude Agent Framework"""
    pass

@click.command()
def version():
    """Show version and environment information."""
    from . import FRAMEWORK_INFO

    console.print("🌐 Claude Agent Framework - Network Engineering Edition")
    console.print(f"Version: {FRAMEWORK_INFO['version']}")

    env_info = detect_environment()

    table = Table(title="Environment Information")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Version", style="yellow")

    table.add_row("Platform", "✅", env_info['platform'])
    table.add_row("Python", "✅", env_info['python_version'])

    pyats_status = "✅" if env_info['pyats_available'] else "❌"
    pyats_version = env_info.get('pyats_version', 'Not installed')
    table.add_row("pyATS", pyats_status, pyats_version)

    genie_status = "✅" if env_info['genie_available'] else "❌"
    genie_version = env_info.get('genie_version', 'Not installed')
    table.add_row("Genie", genie_status, genie_version)

    docker_status = "✅" if env_info['docker_available'] else "❌"
    docker_version = env_info.get('docker_version', 'Not available')
    table.add_row("Docker", docker_status, docker_version)

    console.print(table)
    console.print(f"\nEnvironment Type: {env_info['environment_type']}")

@click.command()
@click.argument('testbed_file', required=False)
def run_health_check(testbed_file):
    """Run health check on network devices."""
    if not testbed_file:
        testbed_file = 'testbed.yaml'

    if not Path(testbed_file).exists():
        console.print(f"❌ Testbed file not found: {testbed_file}", style="red")
        console.print("💡 Create a testbed.yaml file or specify a different file", style="blue")
        return

    console.print(f"🔍 Running health check with testbed: {testbed_file}")

    # Simple health check using pyATS
    success = run_pyats_command('run', ['job', '--testbed-file', testbed_file])

    if success:
        console.print("✅ Health check completed successfully", style="green")
    else:
        console.print("❌ Health check failed", style="red")

@click.command()
def install_pyats():
    """Install pyATS and Genie."""
    console.print("📦 Installing pyATS and Genie...")

    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyats[full]', 'genie'], check=True)
        console.print("✅ pyATS and Genie installed successfully", style="green")
    except subprocess.CalledProcessError:
        console.print("❌ Failed to install pyATS and Genie", style="red")
        console.print("💡 Try running manually: pip install pyats[full] genie", style="blue")

@click.command()
def create_testbed():
    """Create a sample testbed file."""
    testbed_content = """# Sample pyATS Testbed Configuration
# Customize this for your network devices

testbed:
  name: sample_testbed

devices:
  router1:
    type: router
    os: iosxe
    connections:
      cli:
        protocol: ssh
        ip: 192.168.1.1
        port: 22
    credentials:
      default:
        username: admin
        password: "%ENV{DEVICE_PASSWORD}"  # Use environment variable

  switch1:
    type: switch
    os: iosxe
    connections:
      cli:
        protocol: ssh
        ip: 192.168.1.10
        port: 22
    credentials:
      default:
        username: admin
        password: "%ENV{DEVICE_PASSWORD}"

# Environment variables to set:
# export DEVICE_PASSWORD="your_device_password"
"""

    testbed_path = Path('testbed.yaml')
    if testbed_path.exists():
        if not click.confirm(f"{testbed_path} already exists. Overwrite?"):
            return

    testbed_path.write_text(testbed_content)
    console.print(f"✅ Created sample testbed: {testbed_path}", style="green")
    console.print("💡 Edit the file to match your network devices", style="blue")
    console.print("💡 Set DEVICE_PASSWORD environment variable", style="blue")

cli.add_command(version)
cli.add_command(run_health_check)
cli.add_command(install_pyats)
cli.add_command(create_testbed)

def main():
    """Entry point for console script."""
    cli()

if __name__ == '__main__':
    main()