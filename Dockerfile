# Simple pyATS Environment for Infrastructure Testing
FROM python:3.11-slim

# Install essential system packages
RUN apt-get update && apt-get install -y \
    openssh-client \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Install pyATS and essential packages
RUN pip install --no-cache-dir \
    pyats[full] \
    genie

# Set working directory
WORKDIR /workspace

# Create non-root user for security
RUN useradd -m -s /bin/bash pyats
USER pyats

# Default command
CMD ["python"]