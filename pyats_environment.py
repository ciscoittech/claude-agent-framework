#!/usr/bin/env python3
"""
pyATS Environment Detection and Management
Simple environment detection for Claude Code agents
"""

import subprocess
import os
import sys
from pathlib import Path


class PyATSEnvironment:
    """
    Simple pyATS environment detection and command execution
    """

    def __init__(self):
        self.env_type = self._detect_environment()
        self.command_prefix = self._get_command_prefix()

    def _detect_environment(self):
        """
        Detect available pyATS environment

        Returns:
            str: 'local', 'docker', or 'none'
        """

        # Check if we're already inside a container
        if self._is_in_container():
            return 'container'

        # Check for local pyATS installation
        if self._check_local_pyats():
            return 'local'

        # Check for Docker availability
        if self._check_docker_available():
            return 'docker'

        return 'none'

    def _is_in_container(self):
        """Check if running inside a Docker container"""
        return os.path.exists('/.dockerenv') or os.path.exists('/workspace')

    def _check_local_pyats(self):
        """Check if pyATS is installed locally"""
        try:
            result = subprocess.run(['pyats', 'version'],
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _check_docker_available(self):
        """Check if Docker and our container are available"""
        try:
            # Check if docker command exists
            result = subprocess.run(['docker', '--version'],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                return False

            # Check if our docker-compose setup exists
            return Path('docker-compose.yml').exists()

        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def _get_command_prefix(self):
        """Get command prefix based on environment"""

        prefixes = {
            'container': '',  # Already in container
            'local': '',      # Local installation
            'docker': 'docker-compose run --rm pyats ',
            'none': ''
        }

        return prefixes.get(self.env_type, '')

    def execute_pyats_command(self, command, timeout=60):
        """
        Execute pyATS command in detected environment

        Args:
            command (str): pyATS command to execute
            timeout (int): Command timeout in seconds

        Returns:
            dict: Command execution results
        """

        if self.env_type == 'none':
            return {
                'success': False,
                'error': 'pyATS not available. Run ./setup.sh or install locally.',
                'stdout': '',
                'stderr': 'Environment setup required'
            }

        full_command = self.command_prefix + command

        try:
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': full_command,
                'environment': self.env_type
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': f'Command timed out after {timeout} seconds',
                'stdout': '',
                'stderr': 'Timeout',
                'command': full_command,
                'environment': self.env_type
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'stdout': '',
                'stderr': str(e),
                'command': full_command,
                'environment': self.env_type
            }

    def get_environment_info(self):
        """
        Get detailed environment information

        Returns:
            dict: Environment details
        """

        info = {
            'environment_type': self.env_type,
            'command_prefix': self.command_prefix,
            'pyats_available': self.env_type != 'none'
        }

        # Get pyATS version if available
        if info['pyats_available']:
            version_result = self.execute_pyats_command('pyats version')
            if version_result['success']:
                info['pyats_version'] = version_result['stdout'].strip()
            else:
                info['pyats_version'] = 'Unable to determine'

        return info

    def setup_environment(self):
        """
        Setup pyATS environment if needed

        Returns:
            dict: Setup results
        """

        if self.env_type != 'none':
            return {
                'success': True,
                'message': f'pyATS already available in {self.env_type} environment',
                'environment': self.env_type
            }

        # Try to run setup script
        if Path('setup.sh').exists():
            try:
                result = subprocess.run(['./setup.sh'],
                                      capture_output=True, text=True, timeout=300)

                if result.returncode == 0:
                    # Re-detect environment after setup
                    self.env_type = self._detect_environment()
                    self.command_prefix = self._get_command_prefix()

                    return {
                        'success': True,
                        'message': 'Environment setup completed successfully',
                        'environment': self.env_type,
                        'setup_output': result.stdout
                    }
                else:
                    return {
                        'success': False,
                        'message': 'Environment setup failed',
                        'error': result.stderr,
                        'setup_output': result.stdout
                    }

            except subprocess.TimeoutExpired:
                return {
                    'success': False,
                    'message': 'Environment setup timed out',
                    'error': 'Setup took longer than 5 minutes'
                }
            except Exception as e:
                return {
                    'success': False,
                    'message': 'Environment setup error',
                    'error': str(e)
                }
        else:
            return {
                'success': False,
                'message': 'No setup script found. Please install pyATS manually or use Docker.',
                'recommendations': [
                    'Run: pip install pyats[full] genie',
                    'Or: Install Docker and run ./setup.sh',
                    'Or: Use provided docker-compose.yml'
                ]
            }


# Simple CLI for testing
if __name__ == '__main__':
    env = PyATSEnvironment()

    print("🔍 pyATS Environment Detection")
    print("=" * 40)

    info = env.get_environment_info()

    print(f"Environment Type: {info['environment_type']}")
    print(f"pyATS Available: {info['pyats_available']}")

    if info['pyats_available']:
        print(f"Command Prefix: '{info['command_prefix']}'")
        if 'pyats_version' in info:
            print(f"pyATS Version: {info['pyats_version']}")
    else:
        print("\n⚠️  pyATS not available")
        print("Run ./setup.sh or install locally with: pip install pyats[full] genie")

    # Test command execution if available
    if len(sys.argv) > 1 and info['pyats_available']:
        command = ' '.join(sys.argv[1:])
        print(f"\n🧪 Testing command: {command}")
        result = env.execute_pyats_command(command)

        if result['success']:
            print("✅ Command successful")
            print(result['stdout'])
        else:
            print("❌ Command failed")
            print(result.get('error', result.get('stderr', 'Unknown error')))