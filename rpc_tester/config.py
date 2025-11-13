"""
Configuration management for RPC Tester.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import yaml


@dataclass
class Config:
    """Configuration for RPC testing."""

    # RPC endpoints to test
    rpc_urls: List[str] = field(default_factory=list)

    # Test parameters
    num_requests: int = 10
    concurrent_requests: int = 5
    timeout: float = 30.0
    retry_attempts: int = 3
    retry_delay: float = 1.0

    # RPC methods to test
    test_methods: List[str] = field(
        default_factory=lambda: ["eth_blockNumber", "eth_chainId", "eth_gasPrice", "net_version"]
    )

    # Advanced test parameters
    test_eth_call: bool = False
    test_eth_getLogs: bool = False
    test_address: Optional[str] = None  # For eth_getBalance
    test_block_range: int = 100  # For eth_getLogs

    # Output options
    export_json: bool = False
    export_csv: bool = False
    export_html: bool = False
    output_dir: str = "results"

    # Display options
    verbose: bool = False
    quiet: bool = False
    show_percentiles: bool = True

    @classmethod
    def from_file(cls, config_path: str) -> "Config":
        """Load configuration from YAML or JSON file."""
        path = Path(config_path)

        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(path, "r") as f:
            if path.suffix in [".yaml", ".yml"]:
                data = yaml.safe_load(f)
            elif path.suffix == ".json":
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported config file format: {path.suffix}")

        return cls(**data)

    def to_file(self, config_path: str) -> None:
        """Save configuration to YAML or JSON file."""
        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "rpc_urls": self.rpc_urls,
            "num_requests": self.num_requests,
            "concurrent_requests": self.concurrent_requests,
            "timeout": self.timeout,
            "retry_attempts": self.retry_attempts,
            "retry_delay": self.retry_delay,
            "test_methods": self.test_methods,
            "test_eth_call": self.test_eth_call,
            "test_eth_getLogs": self.test_eth_getLogs,
            "test_address": self.test_address,
            "test_block_range": self.test_block_range,
            "export_json": self.export_json,
            "export_csv": self.export_csv,
            "export_html": self.export_html,
            "output_dir": self.output_dir,
            "verbose": self.verbose,
            "quiet": self.quiet,
            "show_percentiles": self.show_percentiles,
        }

        with open(path, "w") as f:
            if path.suffix in [".yaml", ".yml"]:
                yaml.dump(data, f, default_flow_style=False)
            elif path.suffix == ".json":
                json.dump(data, f, indent=2)
            else:
                raise ValueError(f"Unsupported config file format: {path.suffix}")
