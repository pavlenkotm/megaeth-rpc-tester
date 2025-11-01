"""
Configuration management for RPC Tester.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json
import yaml
import os
from pathlib import Path

from .exceptions import ConfigurationError, ValidationError
from .utils import validate_url, validate_ethereum_address
from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class Config:
    """Configuration for RPC testing with validation and environment variable support."""

    # RPC endpoints to test
    rpc_urls: List[str] = field(default_factory=list)

    # Test parameters
    num_requests: int = 10
    concurrent_requests: int = 5
    timeout: float = 30.0
    retry_attempts: int = 3
    retry_delay: float = 1.0

    # RPC methods to test
    test_methods: List[str] = field(default_factory=lambda: [
        "eth_blockNumber",
        "eth_chainId",
        "eth_gasPrice",
        "net_version"
    ])

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

    def __post_init__(self):
        """Validate configuration after initialization."""
        self.validate()

    def validate(self) -> None:
        """
        Validate configuration parameters.

        Raises:
            ValidationError: If configuration is invalid
        """
        errors = []

        # Validate RPC URLs
        if not self.rpc_urls:
            errors.append("At least one RPC URL must be provided")
        else:
            for url in self.rpc_urls:
                if not validate_url(url):
                    errors.append(f"Invalid RPC URL: {url}")

        # Validate test parameters
        if self.num_requests < 1:
            errors.append(f"num_requests must be at least 1, got {self.num_requests}")

        if self.concurrent_requests < 1:
            errors.append(f"concurrent_requests must be at least 1, got {self.concurrent_requests}")

        if self.concurrent_requests > self.num_requests:
            logger.warning(f"concurrent_requests ({self.concurrent_requests}) > num_requests ({self.num_requests}), adjusting")
            self.concurrent_requests = self.num_requests

        if self.timeout <= 0:
            errors.append(f"timeout must be positive, got {self.timeout}")

        if self.retry_attempts < 0:
            errors.append(f"retry_attempts must be non-negative, got {self.retry_attempts}")

        if self.retry_delay < 0:
            errors.append(f"retry_delay must be non-negative, got {self.retry_delay}")

        # Validate RPC methods
        if not self.test_methods:
            errors.append("At least one test method must be provided")

        # Validate Ethereum address if provided
        if self.test_address and not validate_ethereum_address(self.test_address):
            errors.append(f"Invalid Ethereum address: {self.test_address}")

        # Validate block range
        if self.test_block_range < 1:
            errors.append(f"test_block_range must be at least 1, got {self.test_block_range}")

        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            logger.error(error_msg)
            raise ValidationError(error_msg)

        logger.info("Configuration validated successfully")

    @classmethod
    def from_file(cls, config_path: str) -> "Config":
        """
        Load configuration from YAML or JSON file.

        Args:
            config_path: Path to configuration file

        Returns:
            Config instance

        Raises:
            ConfigurationError: If file cannot be loaded or parsed
        """
        path = Path(config_path)

        if not path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")

        try:
            with open(path, 'r') as f:
                if path.suffix in ['.yaml', '.yml']:
                    data = yaml.safe_load(f)
                elif path.suffix == '.json':
                    data = json.load(f)
                else:
                    raise ConfigurationError(f"Unsupported config file format: {path.suffix}")

            if not isinstance(data, dict):
                raise ConfigurationError("Configuration file must contain a dictionary")

            logger.info(f"Loaded configuration from {config_path}")

            # Apply environment variable overrides
            data = cls._apply_env_overrides(data)

            return cls(**data)

        except (yaml.YAMLError, json.JSONDecodeError) as e:
            raise ConfigurationError(f"Failed to parse configuration file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")

    @staticmethod
    def _apply_env_overrides(data: Dict) -> Dict:
        """
        Apply environment variable overrides to configuration.

        Environment variables format: RPC_TESTER_<PARAM_NAME>
        Example: RPC_TESTER_NUM_REQUESTS=20

        Args:
            data: Configuration dictionary

        Returns:
            Updated configuration dictionary
        """
        env_mapping = {
            'RPC_TESTER_NUM_REQUESTS': ('num_requests', int),
            'RPC_TESTER_CONCURRENT': ('concurrent_requests', int),
            'RPC_TESTER_TIMEOUT': ('timeout', float),
            'RPC_TESTER_RETRY_ATTEMPTS': ('retry_attempts', int),
            'RPC_TESTER_RETRY_DELAY': ('retry_delay', float),
            'RPC_TESTER_OUTPUT_DIR': ('output_dir', str),
            'RPC_TESTER_VERBOSE': ('verbose', lambda x: x.lower() in ['true', '1', 'yes']),
            'RPC_TESTER_QUIET': ('quiet', lambda x: x.lower() in ['true', '1', 'yes']),
        }

        for env_var, (config_key, converter) in env_mapping.items():
            value = os.environ.get(env_var)
            if value:
                try:
                    data[config_key] = converter(value)
                    logger.info(f"Applied environment override: {env_var}={value}")
                except Exception as e:
                    logger.warning(f"Failed to apply environment override {env_var}: {e}")

        # Handle RPC URLs from environment (comma-separated)
        rpc_urls_env = os.environ.get('RPC_TESTER_URLS')
        if rpc_urls_env:
            data['rpc_urls'] = [url.strip() for url in rpc_urls_env.split(',')]
            logger.info(f"Applied RPC URLs from environment: {len(data['rpc_urls'])} URLs")

        # Handle methods from environment (comma-separated)
        methods_env = os.environ.get('RPC_TESTER_METHODS')
        if methods_env:
            data['test_methods'] = [method.strip() for method in methods_env.split(',')]
            logger.info(f"Applied methods from environment: {data['test_methods']}")

        return data

    def to_file(self, config_path: str) -> None:
        """Save configuration to YAML or JSON file."""
        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'rpc_urls': self.rpc_urls,
            'num_requests': self.num_requests,
            'concurrent_requests': self.concurrent_requests,
            'timeout': self.timeout,
            'retry_attempts': self.retry_attempts,
            'retry_delay': self.retry_delay,
            'test_methods': self.test_methods,
            'test_eth_call': self.test_eth_call,
            'test_eth_getLogs': self.test_eth_getLogs,
            'test_address': self.test_address,
            'test_block_range': self.test_block_range,
            'export_json': self.export_json,
            'export_csv': self.export_csv,
            'export_html': self.export_html,
            'output_dir': self.output_dir,
            'verbose': self.verbose,
            'quiet': self.quiet,
            'show_percentiles': self.show_percentiles
        }

        with open(path, 'w') as f:
            if path.suffix in ['.yaml', '.yml']:
                yaml.dump(data, f, default_flow_style=False)
            elif path.suffix == '.json':
                json.dump(data, f, indent=2)
            else:
                raise ValueError(f"Unsupported config file format: {path.suffix}")
