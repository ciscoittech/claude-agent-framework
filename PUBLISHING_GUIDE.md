# 📦 Package Publishing Guide

> **How to update and publish NPM and PyPI packages when the framework changes**

## 🔄 Publishing Workflow

### **Version Management**

Both packages use [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backward compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, backward compatible

### **Before Publishing**

1. **Update Version Numbers**
   ```bash
   # Update package.json
   npm version patch  # or minor/major

   # Update setup.py manually
   vim setup.py  # Change version = "1.0.1"

   # Update __init__.py
   vim claude_network_engineering/__init__.py  # Update __version__
   ```

2. **Update CHANGELOG.md**
   ```markdown
   ## [1.0.1] - 2025-09-28
   ### Fixed
   - Bug fixes and improvements
   ```

3. **Test Everything**
   ```bash
   # Test NPM package
   npm run test-framework
   node scripts/install-agents.js

   # Test Python package
   python3 claude_network_engineering/testing.py
   ```

---

## 📦 NPM Publishing

### **Setup (One-time)**

1. **Create NPM Account**
   ```bash
   # Sign up at npmjs.com
   npm login
   ```

2. **Verify Organization Access**
   ```bash
   # Check if you can publish to @claude-agent scope
   npm whoami
   npm access list packages @claude-agent
   ```

### **Publishing Process**

```bash
# 1. Ensure you're on the right branch
git checkout network-engineering
git pull origin network-engineering

# 2. Update version
npm version patch  # Creates git tag automatically

# 3. Build package (if needed)
npm run build  # Optional: if you have build steps

# 4. Test package locally
npm pack
# This creates @claude-agent-network-engineering-1.0.1.tgz

# 5. Test installation locally
npm install -g ./claude-agent-network-engineering-1.0.1.tgz
claude-network-setup --help

# 6. Publish to NPM
npm publish

# 7. Push version tag to git
git push origin network-engineering --tags
```

### **Automated NPM Publishing**

Create `.github/workflows/publish-npm.yml`:

```yaml
name: Publish NPM Package

on:
  push:
    tags:
      - 'v*'

jobs:
  publish-npm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          registry-url: 'https://registry.npmjs.org'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Publish to NPM
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

---

## 🐍 PyPI Publishing

### **Setup (One-time)**

1. **Create PyPI Account**
   - Sign up at [pypi.org](https://pypi.org)
   - Enable 2FA

2. **Install Publishing Tools**
   ```bash
   pip install twine build
   ```

3. **Create API Token**
   - Go to PyPI Account Settings
   - Create API token for the project
   - Store in `~/.pypirc`:
   ```ini
   [pypi]
   username = __token__
   password = pypi-your-api-token-here
   ```

### **Publishing Process**

```bash
# 1. Ensure you're on the right branch
git checkout network-engineering
git pull origin network-engineering

# 2. Update version in setup.py and __init__.py
vim setup.py  # version="1.0.1"
vim claude_network_engineering/__init__.py  # __version__ = "1.0.1"

# 3. Update templates (important!)
rm -rf claude_network_engineering/templates/*
cp -r .claude claude_network_engineering/templates/
cp -r .claude-library claude_network_engineering/templates/
cp -r docs claude_network_engineering/templates/
cp -r examples claude_network_engineering/templates/
cp -r scripts claude_network_engineering/templates/

# 4. Clean previous builds
rm -rf dist/ build/ *.egg-info/

# 5. Build package
python -m build

# 6. Test package locally
pip install dist/claude_agent_network_engineering-1.0.1-py3-none-any.whl
claude-network-setup --help

# 7. Check package with twine
twine check dist/*

# 8. Upload to PyPI
twine upload dist/*

# 9. Commit version changes
git add setup.py claude_network_engineering/__init__.py
git commit -m "Bump version to 1.0.1"
git push origin network-engineering
```

### **Automated PyPI Publishing**

Create `.github/workflows/publish-pypi.yml`:

```yaml
name: Publish PyPI Package

on:
  push:
    tags:
      - 'v*'

jobs:
  publish-pypi:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install build twine

      - name: Update templates
        run: |
          rm -rf claude_network_engineering/templates/*
          cp -r .claude claude_network_engineering/templates/
          cp -r .claude-library claude_network_engineering/templates/
          cp -r docs claude_network_engineering/templates/
          cp -r examples claude_network_engineering/templates/
          cp -r scripts claude_network_engineering/templates/

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

---

## 🚀 Complete Update Workflow

### **For Framework Updates**

```bash
# 1. Make your framework changes
vim .claude/commands/ise-toolkit.md  # Example: update ISE toolkit

# 2. Test changes
claude-code
/ise-toolkit auth-troubleshoot "test"

# 3. Update documentation
vim CHANGELOG.md  # Document changes

# 4. Update version numbers
npm version patch  # Updates package.json and creates git tag
vim setup.py  # Update version manually
vim claude_network_engineering/__init__.py  # Update __version__

# 5. Update PyPI templates
./scripts/update-templates.sh  # Create this script

# 6. Test both packages
npm run test-framework
python3 claude_network_engineering/testing.py

# 7. Commit changes
git add .
git commit -m "Update framework - version 1.0.1"

# 8. Create release tag
git tag v1.0.1
git push origin network-engineering --tags

# 9. Packages auto-publish via GitHub Actions
# Or publish manually:
npm publish
twine upload dist/*
```

### **Update Templates Script**

Create `scripts/update-templates.sh`:

```bash
#!/bin/bash
# Update PyPI package templates with latest framework files

echo "🔄 Updating PyPI package templates..."

# Remove old templates
rm -rf claude_network_engineering/templates/*

# Copy current framework files
cp -r .claude claude_network_engineering/templates/
cp -r .claude-library claude_network_engineering/templates/
cp -r docs claude_network_engineering/templates/
cp -r examples claude_network_engineering/templates/
cp -r scripts claude_network_engineering/templates/

echo "✅ Templates updated"
```

---

## 📋 Version Synchronization

Keep versions synchronized across all files:

### **Files to Update for Each Version**

1. **package.json** - NPM version (use `npm version`)
2. **setup.py** - PyPI version (manual)
3. **claude_network_engineering/__init__.py** - Python package version (manual)
4. **CHANGELOG.md** - Release notes (manual)
5. **Git tags** - Release tagging (manual or automated)

### **Version Check Script**

Create `scripts/check-versions.sh`:

```bash
#!/bin/bash
# Check version consistency across files

NPM_VERSION=$(node -p "require('./package.json').version")
PYTHON_VERSION=$(python3 -c "import claude_network_engineering; print(claude_network_engineering.__version__)")
SETUP_VERSION=$(python3 -c "import setup; print(setup.setup.keywords['version'])" 2>/dev/null || echo "unknown")

echo "NPM version:    $NPM_VERSION"
echo "Python version: $PYTHON_VERSION"
echo "Setup version:  $SETUP_VERSION"

if [ "$NPM_VERSION" = "$PYTHON_VERSION" ]; then
    echo "✅ Versions synchronized"
else
    echo "❌ Versions out of sync!"
    exit 1
fi
```

---

## 🔐 Security & Access

### **NPM Security**

- Use **2FA** on NPM account
- Store **NPM_TOKEN** in GitHub Secrets
- Use **scoped packages** (@claude-agent/network-engineering)
- Enable **package provenance** in GitHub Actions

### **PyPI Security**

- Use **API tokens** instead of passwords
- Store **PYPI_API_TOKEN** in GitHub Secrets
- Enable **2FA** on PyPI account
- Use **trusted publishing** from GitHub Actions

### **Git Security**

- **Sign commits** with GPG
- **Protect main branch** from direct pushes
- **Require PR reviews** for package updates
- **Automate security scanning** in CI/CD

---

## 📊 Monitoring & Analytics

### **Track Package Usage**

```bash
# NPM download stats
npm info @claude-agent/network-engineering

# PyPI download stats (via pypistats)
pip install pypistats
pypistats recent claude-agent-network-engineering
```

### **User Feedback**

- Monitor **GitHub Issues** for package problems
- Check **NPM/PyPI reviews** and ratings
- Track **download statistics** for usage trends
- Collect **user feedback** through documentation

---

## 🆘 Troubleshooting Publishing

### **Common NPM Issues**

```bash
# Permission denied
npm whoami  # Check login
npm login   # Re-authenticate

# Package already exists
npm version patch  # Bump version

# Scope access denied
npm access list packages @claude-agent  # Check permissions
```

### **Common PyPI Issues**

```bash
# Upload fails
twine check dist/*  # Validate package
pip install twine --upgrade  # Update twine

# Version already exists
# Update version in setup.py and __init__.py

# Authentication fails
# Check ~/.pypirc or use API token
```

This publishing guide ensures you can easily update and distribute framework changes to users through both package managers! 🚀