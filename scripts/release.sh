#!/bin/bash
# Complete release workflow for both NPM and PyPI packages

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}🚀 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "setup.py" ] || [ ! -f "package.json" ]; then
    print_error "Must run from repository root (setup.py and package.json not found)"
    exit 1
fi

# Get current version
CURRENT_VERSION=$(node -p "require('./package.json').version")
print_status "Current version: $CURRENT_VERSION"

# Ask for new version
echo ""
echo "📋 Version bump options:"
echo "  1. patch ($CURRENT_VERSION → $(npm version --no-git-tag-version patch && npm version --no-git-tag-version $CURRENT_VERSION))"
echo "  2. minor ($CURRENT_VERSION → $(npm version --no-git-tag-version minor && npm version --no-git-tag-version $CURRENT_VERSION))"
echo "  3. major ($CURRENT_VERSION → $(npm version --no-git-tag-version major && npm version --no-git-tag-version $CURRENT_VERSION))"
echo "  4. custom"

read -p "Choose version bump (1-4): " VERSION_CHOICE

case $VERSION_CHOICE in
    1)
        NEW_VERSION=$(npm version --no-git-tag-version patch)
        ;;
    2)
        NEW_VERSION=$(npm version --no-git-tag-version minor)
        ;;
    3)
        NEW_VERSION=$(npm version --no-git-tag-version major)
        ;;
    4)
        read -p "Enter new version: " CUSTOM_VERSION
        npm version --no-git-tag-version $CUSTOM_VERSION
        NEW_VERSION=$CUSTOM_VERSION
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

# Remove 'v' prefix if present
NEW_VERSION=${NEW_VERSION#v}

print_status "New version: $NEW_VERSION"

# Update Python package version
print_status "Updating Python package version..."
sed -i.bak "s/version=\".*\"/version=\"$NEW_VERSION\"/" setup.py
sed -i.bak "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" claude_network_engineering/__init__.py

# Clean up backup files
rm -f setup.py.bak claude_network_engineering/__init__.py.bak

# Update templates
print_status "Updating PyPI package templates..."
./scripts/update-templates.sh

# Check version consistency
print_status "Checking version consistency..."
./scripts/check-versions.sh

# Run tests
print_status "Running tests..."

# Test NPM package
print_status "Testing NPM package..."
npm run install-agents
node scripts/install-agents.js

# Test Python package (if dependencies available)
if command -v python3 >/dev/null 2>&1; then
    print_status "Testing Python package..."
    # Basic import test
    python3 -c "import claude_network_engineering; claude_network_engineering.print_banner()" || print_warning "Python package test failed (dependencies missing)"
fi

# Update CHANGELOG.md
print_status "Please update CHANGELOG.md with release notes..."
read -p "Press Enter when CHANGELOG.md is updated..."

# Commit changes
print_status "Committing changes..."
git add .
git commit -m "Release version $NEW_VERSION

- Update package versions
- Update PyPI templates
- Update CHANGELOG.md"

# Create git tag
print_status "Creating git tag..."
git tag "v$NEW_VERSION"

# Ask for publishing confirmation
echo ""
print_warning "Ready to publish:"
echo "  📦 NPM: @claude-agent/network-engineering@$NEW_VERSION"
echo "  🐍 PyPI: claude-agent-network-engineering==$NEW_VERSION"
echo "  🏷️  Git tag: v$NEW_VERSION"
echo ""

read -p "Proceed with publishing? (y/N): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    print_warning "Publishing cancelled"
    print_status "To publish later:"
    echo "  git push origin network-engineering --tags"
    echo "  # This will trigger GitHub Actions to publish both packages"
    exit 0
fi

# Push to GitHub (triggers automated publishing)
print_status "Pushing to GitHub..."
git push origin network-engineering
git push origin "v$NEW_VERSION"

print_success "Release $NEW_VERSION initiated!"
print_status "GitHub Actions will now:"
echo "  ✅ Publish NPM package"
echo "  ✅ Publish PyPI package"
echo "  ✅ Create GitHub release"
echo ""
print_status "Monitor progress at:"
echo "  https://github.com/ciscoittech/claude-agent-framework/actions"
echo ""
print_status "Packages will be available at:"
echo "  📦 NPM: https://www.npmjs.com/package/@claude-agent/network-engineering"
echo "  🐍 PyPI: https://pypi.org/project/claude-agent-network-engineering/"