#!/bin/bash
# Update PyPI package templates with latest framework files

set -e

echo "🔄 Updating PyPI package templates..."

# Ensure we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: Must run from repository root (setup.py not found)"
    exit 1
fi

# Remove old templates
echo "  🗑️  Removing old templates..."
rm -rf claude_network_engineering/templates/*

# Create template directory structure
mkdir -p claude_network_engineering/templates

# Copy current framework files
echo "  📁 Copying .claude directory..."
if [ -d ".claude" ]; then
    cp -r .claude claude_network_engineering/templates/
else
    echo "  ⚠️  Warning: .claude directory not found"
fi

echo "  📚 Copying .claude-library directory..."
if [ -d ".claude-library" ]; then
    cp -r .claude-library claude_network_engineering/templates/
else
    echo "  ⚠️  Warning: .claude-library directory not found"
fi

echo "  📖 Copying docs directory..."
if [ -d "docs" ]; then
    cp -r docs claude_network_engineering/templates/
else
    echo "  ⚠️  Warning: docs directory not found"
fi

echo "  📋 Copying examples directory..."
if [ -d "examples" ]; then
    cp -r examples claude_network_engineering/templates/
else
    echo "  ⚠️  Warning: examples directory not found"
fi

echo "  🔧 Copying scripts directory..."
if [ -d "scripts" ]; then
    cp -r scripts claude_network_engineering/templates/
else
    echo "  ⚠️  Warning: scripts directory not found"
fi

# Verify templates were copied
TEMPLATE_COUNT=$(find claude_network_engineering/templates -type f | wc -l)
echo "  📊 Copied $TEMPLATE_COUNT template files"

if [ "$TEMPLATE_COUNT" -lt 50 ]; then
    echo "  ⚠️  Warning: Low template file count, verify all directories copied correctly"
fi

echo "✅ Templates updated successfully"

# Show what was updated
echo ""
echo "📋 Template structure:"
tree claude_network_engineering/templates -L 2 2>/dev/null || ls -la claude_network_engineering/templates/