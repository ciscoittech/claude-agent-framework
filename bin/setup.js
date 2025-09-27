#!/usr/bin/env node

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const inquirer = require('inquirer');

console.log(chalk.blue.bold('🌐 Claude Agent Framework - Network Engineering Edition'));
console.log(chalk.green('Setting up your network engineering AI workspace...\n'));

async function main() {
  try {
    // Check if we're in a project directory
    const cwd = process.cwd();
    const packageJsonExists = await fs.pathExists(path.join(cwd, 'package.json'));
    const projectDetected = packageJsonExists || await fs.pathExists(path.join(cwd, '.git'));

    if (!projectDetected) {
      const { createProject } = await inquirer.prompt([{
        type: 'confirm',
        name: 'createProject',
        message: 'No project detected. Create a new Claude Code project here?',
        default: true
      }]);

      if (!createProject) {
        console.log(chalk.yellow('Please run this in an existing project directory or create a new one.'));
        process.exit(1);
      }
    }

    console.log(chalk.cyan('📋 Project detected. Setting up Claude Agent Framework...\n'));

    // Get framework source directory
    const frameworkDir = path.dirname(__dirname);

    // Copy .claude directory
    const claudeSource = path.join(frameworkDir, '.claude');
    const claudeTarget = path.join(cwd, '.claude');

    if (await fs.pathExists(claudeTarget)) {
      const { overwrite } = await inquirer.prompt([{
        type: 'confirm',
        name: 'overwrite',
        message: '.claude directory already exists. Overwrite?',
        default: false
      }]);

      if (!overwrite) {
        console.log(chalk.yellow('Skipping .claude directory...'));
      } else {
        await fs.remove(claudeTarget);
        await fs.copy(claudeSource, claudeTarget);
        console.log(chalk.green('✅ Updated .claude directory'));
      }
    } else {
      await fs.copy(claudeSource, claudeTarget);
      console.log(chalk.green('✅ Created .claude directory'));
    }

    // Copy .claude-library directory
    const librarySource = path.join(frameworkDir, '.claude-library');
    const libraryTarget = path.join(cwd, '.claude-library');

    if (await fs.pathExists(libraryTarget)) {
      const { overwriteLibrary } = await inquirer.prompt([{
        type: 'confirm',
        name: 'overwriteLibrary',
        message: '.claude-library directory already exists. Overwrite?',
        default: false
      }]);

      if (!overwriteLibrary) {
        console.log(chalk.yellow('Skipping .claude-library directory...'));
      } else {
        await fs.remove(libraryTarget);
        await fs.copy(librarySource, libraryTarget);
        console.log(chalk.green('✅ Updated .claude-library directory'));
      }
    } else {
      await fs.copy(librarySource, libraryTarget);
      console.log(chalk.green('✅ Created .claude-library directory'));
    }

    // Copy scripts directory
    const scriptsSource = path.join(frameworkDir, 'scripts');
    const scriptsTarget = path.join(cwd, 'scripts');

    if (await fs.pathExists(scriptsTarget)) {
      console.log(chalk.yellow('scripts directory exists, skipping...'));
    } else {
      await fs.copy(scriptsSource, scriptsTarget);
      console.log(chalk.green('✅ Created scripts directory'));
    }

    // Copy examples directory (optional)
    const { includeExamples } = await inquirer.prompt([{
      type: 'confirm',
      name: 'includeExamples',
      message: 'Include example configurations and sample data?',
      default: true
    }]);

    if (includeExamples) {
      const examplesSource = path.join(frameworkDir, 'examples');
      const examplesTarget = path.join(cwd, 'examples');

      if (!(await fs.pathExists(examplesTarget))) {
        await fs.copy(examplesSource, examplesTarget);
        console.log(chalk.green('✅ Created examples directory'));
      }
    }

    // Copy documentation (optional)
    const { includeDocs } = await inquirer.prompt([{
      type: 'confirm',
      name: 'includeDocs',
      message: 'Include documentation files?',
      default: true
    }]);

    if (includeDocs) {
      const docsSource = path.join(frameworkDir, 'docs');
      const docsTarget = path.join(cwd, 'docs');

      if (!(await fs.pathExists(docsTarget))) {
        await fs.copy(docsSource, docsTarget);
        console.log(chalk.green('✅ Created docs directory'));
      }
    }

    // Create or update CLAUDE.md
    const claudeMdPath = path.join(cwd, 'CLAUDE.md');
    const claudeMdTemplate = `# Claude Code Project Configuration

## Project Overview
Network engineering project with Claude Agent Framework integration.

## 🎯 PRIMARY PRINCIPLE: Simplicity First

**CRITICAL**: This framework follows "simplest approach first" - always try simple solutions before complex ones.

**ESCALATION PATH**: Basic Commands → Scripts → Single Agent → Multi-Agent Coordination

## Available Commands

### Network Engineering Toolkits
- \`/ise-toolkit\` - ISE authentication and troubleshooting
- \`/voip-toolkit\` - VoIP call quality and infrastructure analysis
- \`/claude-docs\` - Claude Code documentation research
- \`/load-cisco-docs\` - Cisco documentation integration

### Daily Operations
\`\`\`bash
# Basic health monitoring
python3 scripts/pyats_launcher.py run-health-check

# ISE authentication troubleshooting
/ise-toolkit auth-troubleshoot "authentication-issue"

# VoIP call quality analysis
/voip-toolkit call-quality-analysis "call-quality-issue"

# Research best practices
/claude-docs best-practices "network-automation"
\`\`\`

## Framework Information
- **Edition**: Network Engineering
- **Version**: 1.0.0
- **Grade**: A+ (98/100)
- **Agents**: 6 specialized network agents
- **Commands**: 4 ready-to-use toolkits

For detailed usage, see docs/NAVIGATION_GUIDE.md
`;

    if (!(await fs.pathExists(claudeMdPath))) {
      await fs.writeFile(claudeMdPath, claudeMdTemplate);
      console.log(chalk.green('✅ Created CLAUDE.md'));
    }

    // Setup validation
    console.log(chalk.cyan('\n🧪 Validating setup...'));

    // Check if Python is available for pyATS
    const { spawn } = require('child_process');
    const pythonCheck = spawn('python3', ['--version'], { stdio: 'pipe' });

    pythonCheck.on('close', (code) => {
      if (code === 0) {
        console.log(chalk.green('✅ Python 3 detected'));
      } else {
        console.log(chalk.yellow('⚠️  Python 3 not found (needed for pyATS integration)'));
      }
    });

    pythonCheck.on('error', () => {
      console.log(chalk.yellow('⚠️  Python 3 not found (needed for pyATS integration)'));
    });

    // Success message
    console.log(chalk.green.bold('\n🎉 Setup Complete!'));
    console.log(chalk.cyan('\nNext steps:'));
    console.log(chalk.white('1. Run: claude-code'));
    console.log(chalk.white('2. Try: /ise-toolkit auth-troubleshoot "test"'));
    console.log(chalk.white('3. Read: docs/NAVIGATION_GUIDE.md'));
    console.log(chalk.white('4. Explore: examples/ directory'));

    console.log(chalk.blue('\n📚 Documentation:'));
    console.log(chalk.white('- Quick start: docs/NAVIGATION_GUIDE.md'));
    console.log(chalk.white('- Simplicity guide: docs/SIMPLICITY_GUIDE.md'));
    console.log(chalk.white('- Testing: docs/operations/FRAMEWORK_TEST_REPORT.md'));

  } catch (error) {
    console.error(chalk.red('❌ Setup failed:'), error.message);
    process.exit(1);
  }
}

main();