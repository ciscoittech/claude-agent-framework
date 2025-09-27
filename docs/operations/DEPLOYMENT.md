# Deployment Options
*Simple deployment strategies for the pyATS Infrastructure Framework*

## 🎯 Quick Start (Recommended)

### **Docker Deployment (Orb Stack Compatible)**
```bash
# Clone the repository
git clone https://github.com/your-repo/claude-agent-framework
cd claude-agent-framework

# Run setup script
./setup.sh

# Start using pyATS
docker-compose run --rm pyats pyats version
```

## 🐳 **Docker Options**

### **Option 1: Docker Compose (Simplest)**
```bash
# Build and run
docker-compose build
docker-compose run --rm pyats python

# Interactive shell
docker-compose run --rm pyats bash

# Execute pyATS commands
docker-compose run --rm pyats pyats version
docker-compose run --rm pyats genie --help
```

### **Option 2: Direct Docker**
```bash
# Build image
docker build -t pyats-infrastructure .

# Run container
docker run -it --rm -v $(pwd):/workspace pyats-infrastructure

# Execute commands
docker run --rm -v $(pwd):/workspace pyats-infrastructure pyats version
```

## 💻 **Local Installation Options**

### **Option 1: pip install (Advanced Users)**
```bash
# Install pyATS locally
pip install pyats[full] genie

# Verify installation
pyats version
genie --help
```

### **Option 2: Virtual Environment**
```bash
# Create virtual environment
python -m venv pyats-env
source pyats-env/bin/activate  # Linux/Mac
# pyats-env\Scripts\activate   # Windows

# Install pyATS
pip install pyats[full] genie

# Verify installation
pyats version
```

### **Option 3: Conda Environment**
```bash
# Create conda environment
conda create -n pyats python=3.11
conda activate pyats

# Install pyATS
pip install pyats[full] genie

# Verify installation
pyats version
```

## 🔧 **Development Setup**

### **For Framework Development**
```bash
# Clone repository
git clone https://github.com/your-repo/claude-agent-framework
cd claude-agent-framework

# Development with Docker
docker-compose run --rm pyats bash

# Mount current directory for live editing
# (Already configured in docker-compose.yml)
```

### **VS Code Dev Container**
```bash
# Open in VS Code
code .

# Use "Reopen in Container" when prompted
# Or: Ctrl+Shift+P -> "Remote-Containers: Reopen in Container"
```

## 🧪 **Testing Your Setup**

### **Basic Functionality Test**
```bash
# Test pyATS installation
docker-compose run --rm pyats pyats version

# Test Genie library
docker-compose run --rm pyats python -c "from genie.libs.parser.utils.common import get_parser; print('Genie working!')"

# Test framework agents
docker-compose run --rm pyats python -c "print('Framework ready!')"
```

### **Network Device Test (Optional)**
```bash
# Create test testbed file
cat > testbed.yaml << EOF
testbed:
  name: test_testbed
devices:
  test_device:
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
        password: admin
EOF

# Test device connectivity (if you have a test device)
docker-compose run --rm pyats pyats run job --testbed-file testbed.yaml
```

## 🔒 **Security Considerations**

### **SSH Key Management**
```bash
# SSH keys are mounted read-only from ~/.ssh
# No additional configuration needed for Orb Stack

# For custom SSH key location:
docker run -v /path/to/keys:/home/pyats/.ssh:ro pyats-infrastructure
```

### **Credential Management**
```bash
# Use environment variables for sensitive data
export TESTBED_USERNAME="your_username"
export TESTBED_PASSWORD="your_password"

# Pass to container
docker-compose run --rm -e TESTBED_USERNAME -e TESTBED_PASSWORD pyats python
```

## 🚀 **Production Deployment**

### **CI/CD Integration**
```yaml
# .github/workflows/test.yml
name: Test Infrastructure Framework
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker-compose build
      - name: Test pyATS installation
        run: docker-compose run --rm pyats pyats version
      - name: Run framework tests
        run: docker-compose run --rm pyats python -m pytest tests/
```

### **Container Registry**
```bash
# Build and tag for registry
docker build -t your-registry/pyats-infrastructure:latest .

# Push to registry
docker push your-registry/pyats-infrastructure:latest

# Pull and use
docker pull your-registry/pyats-infrastructure:latest
docker run -it --rm your-registry/pyats-infrastructure:latest
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Docker Permission Issues**
```bash
# If permission denied on Orb Stack
sudo chown -R $USER:$USER ~/.docker

# Or run Docker commands with sudo (not recommended)
sudo docker-compose run --rm pyats pyats version
```

#### **Port Conflicts**
```bash
# Framework doesn't expose ports by default
# No port conflicts with Orb Stack

# If you need to expose ports (advanced):
docker-compose run --rm -p 8080:8080 pyats python
```

#### **Volume Mount Issues**
```bash
# Check if current directory is mounted
docker-compose run --rm pyats ls -la /workspace

# Should show your framework files
```

### **Performance Optimization**
```bash
# Pre-build image for faster startup
docker-compose build

# Use Docker BuildKit for faster builds
DOCKER_BUILDKIT=1 docker-compose build

# Clean up unused containers
docker system prune -f
```

## 📊 **Resource Requirements**

### **Minimum Requirements**
- **RAM**: 2GB available
- **Disk**: 1GB for Docker image
- **Network**: Internet access for package installation

### **Recommended**
- **RAM**: 4GB+ for multiple device testing
- **Disk**: 2GB+ for logs and results
- **Network**: Stable connection to network devices

## 🆘 **Getting Help**

### **Framework Issues**
- Check logs: `docker-compose logs`
- Interactive debugging: `docker-compose run --rm pyats bash`
- GitHub Issues: [Framework Issues](https://github.com/your-repo/claude-agent-framework/issues)

### **pyATS Issues**
- pyATS Documentation: [https://developer.cisco.com/docs/pyats/](https://developer.cisco.com/docs/pyats/)
- Genie Documentation: [https://developer.cisco.com/docs/genie/](https://developer.cisco.com/docs/genie/)
- Community Forum: [https://community.cisco.com/t5/pyats-genie/bd-p/5672-discussions-pyats](https://community.cisco.com/t5/pyats-genie/bd-p/5672-discussions-pyats)

---

**Remember**: Start simple with Docker Compose, expand as needed!