#!/usr/bin/env python3
"""
Command-line interface for Claude Agent Framework - Network Engineering Edition
"""

import os
import sys
import shutil
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Confirm
import pkg_resources

from . import FRAMEWORK_INFO, print_banner

console = Console()

def get_template_dir():
    """Get the template directory from the package."""
    try:
        return pkg_resources.resource_filename('claude_network_engineering', 'templates')
    except:
        # Fallback for development
        return Path(__file__).parent / 'templates'

@click.group()
@click.version_option(version=FRAMEWORK_INFO['version'])
def cli():
    """Claude Agent Framework - Network Engineering Edition CLI"""
    pass

@click.command()
@click.option('--project-dir', default='.', help='Project directory to setup (default: current directory)')
@click.option('--include-examples', default=True, help='Include example configurations')
@click.option('--include-docs', default=True, help='Include documentation')
@click.option('--force', is_flag=True, help='Overwrite existing files')
def setup(project_dir, include_examples, include_docs, force):
    """Setup Claude Agent Framework in your project directory."""

    print_banner()

    project_path = Path(project_dir).resolve()

    if not project_path.exists():
        if Confirm.ask(f"Directory {project_path} doesn't exist. Create it?"):
            project_path.mkdir(parents=True, exist_ok=True)
        else:
            console.print("❌ Setup cancelled", style="red")
            sys.exit(1)

    console.print(f"📂 Setting up framework in: {project_path}")

    template_dir = get_template_dir()

    # Files and directories to copy
    items_to_copy = [
        ('.claude', '.claude'),
        ('.claude-library', '.claude-library'),
        ('scripts', 'scripts'),
    ]

    if include_examples:
        items_to_copy.append(('examples', 'examples'))

    if include_docs:
        items_to_copy.append(('docs', 'docs'))

    # Copy framework files
    for src_name, dst_name in items_to_copy:
        src_path = Path(template_dir) / src_name
        dst_path = project_path / dst_name

        if dst_path.exists() and not force:
            if not Confirm.ask(f"{dst_name} already exists. Overwrite?"):
                console.print(f"⏭️  Skipping {dst_name}")
                continue
            shutil.rmtree(dst_path)

        if src_path.exists():
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            console.print(f"✅ Created {dst_name}")
        else:
            console.print(f"⚠️  Template {src_name} not found", style="yellow")

    # Create CLAUDE.md if it doesn't exist
    claude_md_path = project_path / 'CLAUDE.md'
    if not claude_md_path.exists() or force:
        claude_md_content = f"""# Claude Code Project Configuration

## Project Overview
Network engineering project with Claude Agent Framework integration.

## 🎯 PRIMARY PRINCIPLE: Simplicity First

**CRITICAL**: This framework follows "simplest approach first" - always try simple solutions before complex ones.

**ESCALATION PATH**: Basic Commands → Scripts → Single Agent → Multi-Agent Coordination

## Available Commands

### Network Engineering Toolkits
- `/ise-toolkit` - ISE authentication and troubleshooting
- `/voip-toolkit` - VoIP call quality and infrastructure analysis
- `/claude-docs` - Claude Code documentation research
- `/load-cisco-docs` - Cisco documentation integration

### Daily Operations
```bash
# Basic health monitoring
python3 scripts/pyats_launcher.py run-health-check

# ISE authentication troubleshooting
/ise-toolkit auth-troubleshoot "authentication-issue"

# VoIP call quality analysis
/voip-toolkit call-quality-analysis "call-quality-issue"

# Research best practices
/claude-docs best-practices "network-automation"
```

## Framework Information
- **Edition**: Network Engineering
- **Version**: {FRAMEWORK_INFO['version']}
- **Grade**: {FRAMEWORK_INFO['grade']}
- **Agents**: {FRAMEWORK_INFO['agents']} specialized network agents
- **Commands**: {FRAMEWORK_INFO['commands']} ready-to-use toolkits

For detailed usage, see docs/NAVIGATION_GUIDE.md
"""
        claude_md_path.write_text(claude_md_content)
        console.print("✅ Created CLAUDE.md")

    # Validation
    console.print("\n🧪 Validating setup...")

    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        console.print(f"✅ Python {python_version.major}.{python_version.minor} detected")
    else:
        console.print("⚠️  Python 3.8+ recommended", style="yellow")

    # Check if in a git repository
    if (project_path / '.git').exists():
        console.print("✅ Git repository detected")
    else:
        console.print("💡 Consider initializing a git repository", style="blue")

    # Success message
    success_panel = Panel.fit(
        Text.from_markup("""[bold green]🎉 Setup Complete![/bold green]

[bold]Next steps:[/bold]
1. Run: [cyan]claude-code[/cyan]
2. Try: [cyan]/ise-toolkit auth-troubleshoot "test"[/cyan]
3. Read: [cyan]docs/NAVIGATION_GUIDE.md[/cyan]
4. Explore: [cyan]examples/[/cyan] directory

[bold]Documentation:[/bold]
• Quick start: [cyan]docs/NAVIGATION_GUIDE.md[/cyan]
• Simplicity guide: [cyan]docs/SIMPLICITY_GUIDE.md[/cyan]
• Testing: [cyan]docs/operations/FRAMEWORK_TEST_REPORT.md[/cyan]"""),
        title="Framework Ready",
        border_style="green"
    )

    console.print(success_panel)

def setup_command():
    """Entry point for console script."""
    setup()

if __name__ == '__main__':
    cli()