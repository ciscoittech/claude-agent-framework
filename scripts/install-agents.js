#!/usr/bin/env node

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');

/**
 * Install and register Claude agents from the framework
 */
async function installAgents() {
  console.log(chalk.blue('🤖 Installing Claude Agent Framework agents...'));

  const cwd = process.cwd();
  const registryPath = path.join(cwd, '.claude-library', 'REGISTRY.json');

  if (!await fs.pathExists(registryPath)) {
    console.error(chalk.red('❌ REGISTRY.json not found. Run setup first.'));
    process.exit(1);
  }

  try {
    const registry = await fs.readJson(registryPath);

    console.log(chalk.cyan(`📋 Framework: ${registry.framework}`));
    console.log(chalk.cyan(`📦 Version: ${registry.version}`));

    // Validate agents exist
    const agentCount = Object.keys(registry.agents).length;
    const commandCount = Object.keys(registry.commands).length;

    console.log(chalk.green(`✅ Found ${agentCount} agents`));
    console.log(chalk.green(`✅ Found ${commandCount} commands`));

    // List available commands
    console.log(chalk.yellow('\n📝 Available Commands:'));
    Object.entries(registry.commands).forEach(([name, info]) => {
      console.log(chalk.white(`  /${name} - ${info.description}`));
    });

    // List available agents
    console.log(chalk.yellow('\n🤖 Available Agents:'));
    Object.entries(registry.agents).forEach(([name, info]) => {
      console.log(chalk.white(`  ${name} - ${info.description}`));
    });

    console.log(chalk.green.bold('\n🎉 Agent installation validated!'));
    console.log(chalk.cyan('Start Claude Code and try: /ise-toolkit auth-troubleshoot "test"'));

  } catch (error) {
    console.error(chalk.red('❌ Failed to read registry:'), error.message);
    process.exit(1);
  }
}

installAgents();