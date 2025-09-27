#!/usr/bin/env python3
"""
Testing utilities for Claude Agent Framework - Network Engineering Edition
"""

import os
import sys
from pathlib import Path
import json
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def test_framework_structure():
    """Test that the framework structure is properly installed."""
    results = {
        'claude_dir': False,
        'claude_library': False,
        'registry': False,
        'commands': 0,
        'agents': 0,
        'contexts': 0,
        'scripts': False,
        'docs': False,
        'examples': False
    }

    cwd = Path.cwd()

    # Check .claude directory
    claude_dir = cwd / '.claude'
    if claude_dir.exists():
        results['claude_dir'] = True
        # Count commands
        commands_dir = claude_dir / 'commands'
        if commands_dir.exists():
            results['commands'] = len(list(commands_dir.glob('*.md')))

    # Check .claude-library directory
    library_dir = cwd / '.claude-library'
    if library_dir.exists():
        results['claude_library'] = True

        # Check registry
        registry_file = library_dir / 'REGISTRY.json'
        if registry_file.exists():
            results['registry'] = True
            try:
                with open(registry_file) as f:
                    registry = json.load(f)
                    results['agents'] = len(registry.get('agents', {}))
                    results['contexts'] = len(registry.get('contexts', {}))
            except Exception:
                pass

    # Check other directories
    results['scripts'] = (cwd / 'scripts').exists()
    results['docs'] = (cwd / 'docs').exists()
    results['examples'] = (cwd / 'examples').exists()

    return results

def test_agent_registration():
    """Test that agents are properly registered."""
    registry_file = Path.cwd() / '.claude-library' / 'REGISTRY.json'

    if not registry_file.exists():
        return None

    try:
        with open(registry_file) as f:
            registry = json.load(f)

        # Test agent files exist
        agent_files = {}
        for name, info in registry.get('agents', {}).items():
            agent_path = Path.cwd() / info['path']
            agent_files[name] = agent_path.exists()

        # Test command files exist
        command_files = {}
        for name, info in registry.get('commands', {}).items():
            command_path = Path.cwd() / info['path']
            command_files[name] = command_path.exists()

        return {
            'registry': registry,
            'agent_files': agent_files,
            'command_files': command_files
        }

    except Exception as e:
        console.print(f"❌ Error reading registry: {e}", style="red")
        return None

def display_test_results(structure_results, registration_results):
    """Display test results in a formatted table."""

    # Framework structure table
    structure_table = Table(title="Framework Structure")
    structure_table.add_column("Component", style="cyan")
    structure_table.add_column("Status", style="green")
    structure_table.add_column("Details", style="yellow")

    # Add structure results
    structure_table.add_row(
        ".claude directory",
        "✅" if structure_results['claude_dir'] else "❌",
        f"{structure_results['commands']} commands" if structure_results['claude_dir'] else "Missing"
    )

    structure_table.add_row(
        ".claude-library directory",
        "✅" if structure_results['claude_library'] else "❌",
        f"{structure_results['agents']} agents, {structure_results['contexts']} contexts" if structure_results['claude_library'] else "Missing"
    )

    structure_table.add_row(
        "REGISTRY.json",
        "✅" if structure_results['registry'] else "❌",
        "Agent registration" if structure_results['registry'] else "Missing"
    )

    structure_table.add_row(
        "scripts directory",
        "✅" if structure_results['scripts'] else "⚠️",
        "pyATS integration" if structure_results['scripts'] else "Optional"
    )

    structure_table.add_row(
        "docs directory",
        "✅" if structure_results['docs'] else "⚠️",
        "Documentation" if structure_results['docs'] else "Optional"
    )

    structure_table.add_row(
        "examples directory",
        "✅" if structure_results['examples'] else "⚠️",
        "Sample data" if structure_results['examples'] else "Optional"
    )

    console.print(structure_table)

    # Registration results
    if registration_results:
        registry = registration_results['registry']

        # Commands table
        commands_table = Table(title="Registered Commands")
        commands_table.add_column("Command", style="cyan")
        commands_table.add_column("File Status", style="green")
        commands_table.add_column("Description", style="yellow")

        for name, info in registry.get('commands', {}).items():
            file_exists = registration_results['command_files'].get(name, False)
            commands_table.add_row(
                f"/{name}",
                "✅" if file_exists else "❌",
                info.get('description', 'No description')
            )

        console.print(commands_table)

        # Agents table
        agents_table = Table(title="Registered Agents")
        agents_table.add_column("Agent", style="cyan")
        agents_table.add_column("File Status", style="green")
        agents_table.add_column("Category", style="yellow")
        agents_table.add_column("Description", style="white")

        for name, info in registry.get('agents', {}).items():
            file_exists = registration_results['agent_files'].get(name, False)
            agents_table.add_row(
                name,
                "✅" if file_exists else "❌",
                info.get('category', 'Unknown'),
                info.get('description', 'No description')
            )

        console.print(agents_table)

@click.command()
def test_framework():
    """Test the Claude Agent Framework installation."""
    from . import FRAMEWORK_INFO

    console.print("🧪 Testing Claude Agent Framework Installation")
    console.print(f"Framework Version: {FRAMEWORK_INFO['version']}\n")

    # Test framework structure
    structure_results = test_framework_structure()

    # Test agent registration
    registration_results = test_agent_registration()

    # Display results
    display_test_results(structure_results, registration_results)

    # Overall assessment
    critical_components = [
        structure_results['claude_dir'],
        structure_results['claude_library'],
        structure_results['registry'],
        structure_results['commands'] >= 4,
        structure_results['agents'] >= 6
    ]

    if all(critical_components):
        status_panel = Panel.fit(
            "✅ [bold green]Framework installation successful![/bold green]\n\n"
            "Ready to use:\n"
            "1. Run: [cyan]claude-code[/cyan]\n"
            "2. Try: [cyan]/ise-toolkit auth-troubleshoot \"test\"[/cyan]\n"
            "3. Read: [cyan]docs/NAVIGATION_GUIDE.md[/cyan]",
            title="Test Results",
            border_style="green"
        )
        console.print(status_panel)
    else:
        status_panel = Panel.fit(
            "❌ [bold red]Framework installation incomplete![/bold red]\n\n"
            "Missing critical components. Try:\n"
            "1. Run: [cyan]claude-network-setup --force[/cyan]\n"
            "2. Check: [cyan]PACKAGE_INSTALLATION.md[/cyan]\n"
            "3. Report issues: [cyan]GitHub Issues[/cyan]",
            title="Test Results",
            border_style="red"
        )
        console.print(status_panel)
        sys.exit(1)

if __name__ == '__main__':
    test_framework()