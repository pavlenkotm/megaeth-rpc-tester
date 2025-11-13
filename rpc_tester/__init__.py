"""
MegaETH RPC Tester - Advanced Ethereum RPC endpoint testing and benchmarking tool.
"""

__version__ = "2.0.0"
__author__ = "pavlenkotm"
__description__ = "Advanced async RPC testing tool for Ethereum nodes"

from .config import Config
from .core import RPCTester

__all__ = ["RPCTester", "Config"]
