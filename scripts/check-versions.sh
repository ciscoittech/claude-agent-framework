#!/bin/bash
# Check version consistency across package files

set -e

echo "🔍 Checking version consistency..."

# Get versions from different sources
if [ -f "package.json" ]; then
    NPM_VERSION=$(node -p "require('./package.json').version" 2>/dev/null || echo "unknown")
else
    NPM_VERSION="not-found"
fi

if [ -f "claude_network_engineering/__init__.py" ]; then
    PYTHON_VERSION=$(python3 -c "
import sys
sys.path.insert(0, 'claude_network_engineering')
import __init__
print(__init__.__version__)
" 2>/dev/null || echo "unknown")
else
    PYTHON_VERSION="not-found"
fi

if [ -f "setup.py" ]; then
    SETUP_VERSION=$(python3 -c "
import re
with open('setup.py', 'r') as f:
    content = f.read()
    match = re.search(r'version=[\"\'](.*?)[\"\']', content)
    print(match.group(1) if match else 'unknown')
" 2>/dev/null || echo "unknown")
else
    SETUP_VERSION="not-found"
fi

# Display versions
echo ""
echo "📦 Package Versions:"
echo "  NPM (package.json):     $NPM_VERSION"
echo "  Python (__init__.py):   $PYTHON_VERSION"
echo "  Setup (setup.py):       $SETUP_VERSION"

# Check consistency
ALL_SAME=true

if [ "$NPM_VERSION" != "not-found" ] && [ "$PYTHON_VERSION" != "not-found" ]; then
    if [ "$NPM_VERSION" != "$PYTHON_VERSION" ]; then
        ALL_SAME=false
    fi
fi

if [ "$PYTHON_VERSION" != "not-found" ] && [ "$SETUP_VERSION" != "not-found" ]; then
    if [ "$PYTHON_VERSION" != "$SETUP_VERSION" ]; then
        ALL_SAME=false
    fi
fi

if [ "$NPM_VERSION" != "not-found" ] && [ "$SETUP_VERSION" != "not-found" ]; then
    if [ "$NPM_VERSION" != "$SETUP_VERSION" ]; then
        ALL_SAME=false
    fi
fi

echo ""
if [ "$ALL_SAME" = true ]; then
    echo "✅ All versions are synchronized ($NPM_VERSION)"
    exit 0
else
    echo "❌ Versions are out of sync!"
    echo ""
    echo "🔧 To fix:"
    echo "  1. Choose target version (e.g., 1.0.1)"
    echo "  2. Run: npm version 1.0.1"
    echo "  3. Update setup.py version manually"
    echo "  4. Update claude_network_engineering/__init__.py __version__"
    exit 1
fi