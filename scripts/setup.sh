#!/bin/bash
# Simple setup script for pyATS Infrastructure Framework

set -e

echo "🚀 Setting up pyATS Infrastructure Framework"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# Build the container
echo "📦 Building pyATS container..."
docker-compose build

# Test the installation
echo "🧪 Testing pyATS installation..."
docker-compose run --rm pyats pyats version

echo "✅ Setup complete!"
echo ""
echo "Quick start:"
echo "  docker-compose run --rm pyats python"
echo "  docker-compose run --rm pyats pyats version"
echo ""
echo "For interactive shell:"
echo "  docker-compose run --rm pyats bash"