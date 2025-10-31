"""
Setup script for MegaETH RPC Tester.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
else:
    requirements = [
        "aiohttp>=3.9.0",
        "rich>=13.7.0",
        "pyyaml>=6.0.1"
    ]

setup(
    name="megaeth-rpc-tester",
    version="2.0.0",
    author="pavlenkotm",
    description="Advanced async RPC testing tool for Ethereum nodes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pavlenkotm/megaeth-rpc-tester",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "mypy>=1.7.0",
            "types-PyYAML>=6.0.12",
        ]
    },
    entry_points={
        "console_scripts": [
            "rpc-tester=rpc_tester.cli:main",
        ],
    },
)
