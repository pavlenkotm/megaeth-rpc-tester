"""
MegaETH RPC Tester - Advanced Ethereum RPC endpoint testing and benchmarking tool.

This package provides comprehensive tools for testing and benchmarking Ethereum RPC endpoints
with support for multiple methods, concurrent testing, detailed statistics, and beautiful reports.
"""

__version__ = "2.1.0"
__author__ = "pavlenkotm"
__description__ = "Advanced async RPC testing tool for Ethereum nodes with enhanced reporting"
__license__ = "MIT"

# Core functionality
from .core import RPCTester, TestResult, EndpointStats
from .config import Config
from .reporting import Reporter

# Utilities
from .logger import setup_logger, get_logger
from .exceptions import (
    RPCTesterError,
    ConfigurationError,
    ConnectionError,
    TimeoutError,
    InvalidResponseError,
    ValidationError,
    ExportError,
    MethodNotSupportedError
)

__all__ = [
    # Core classes
    "RPCTester",
    "Config",
    "Reporter",
    "TestResult",
    "EndpointStats",

    # Logger
    "setup_logger",
    "get_logger",

    # Exceptions
    "RPCTesterError",
    "ConfigurationError",
    "ConnectionError",
    "TimeoutError",
    "InvalidResponseError",
    "ValidationError",
    "ExportError",
    "MethodNotSupportedError",

    # Package metadata
    "__version__",
    "__author__",
    "__description__",
    "__license__",
]
