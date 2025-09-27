from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="claude-agent-network-engineering",
    version="1.0.0",
    author="Network Engineering Community",
    author_email="contact@example.com",
    description="Claude Agent Framework - Network Engineering Edition with pre-built agents for ISE, VoIP, and network automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ciscoittech/claude-agent-framework",
    project_urls={
        "Bug Tracker": "https://github.com/ciscoittech/claude-agent-framework/issues",
        "Documentation": "https://github.com/ciscoittech/claude-agent-framework/tree/network-engineering#readme",
        "Source Code": "https://github.com/ciscoittech/claude-agent-framework/tree/network-engineering",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "pyats": [
            "pyats[full]>=23.1",
            "genie>=23.1",
        ],
        "network": [
            "netmiko>=4.0.0",
            "napalm>=4.0.0",
            "paramiko>=2.9.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "claude-network-setup=claude_network_engineering.cli:setup_command",
            "claude-pyats-launcher=claude_network_engineering.pyats_launcher:main",
            "claude-framework-test=claude_network_engineering.testing:test_framework",
        ],
    },
    package_data={
        "claude_network_engineering": [
            "templates/.claude/**/*",
            "templates/.claude-library/**/*",
            "templates/docs/**/*",
            "templates/examples/**/*",
            "templates/scripts/**/*",
            "templates/*.md",
            "templates/*.json",
            "templates/*.yml",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "claude",
        "ai",
        "network-engineering",
        "cisco",
        "ise",
        "voip",
        "pyats",
        "automation",
        "troubleshooting",
        "infrastructure",
        "networking",
        "agents",
    ],
)