"""
MegaETH RPC Tester - Advanced Ethereum RPC endpoint testing and benchmarking tool.
"""

__version__ = "2.0.0"
__author__ = "pavlenkotm"
__description__ = "Advanced async RPC testing tool for Ethereum nodes"

from .core import RPCTester
from .config import Config

__all__ = ["RPCTester", "Config"]
