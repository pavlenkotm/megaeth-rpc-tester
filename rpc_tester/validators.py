"""
Configuration and data validators for RPC Tester.
"""

import re
from typing import Any, List, Optional
from urllib.parse import urlparse


class ValidationError(Exception):
    """Raised when validation fails."""

    pass


class ConfigValidator:
    """Validates RPC Tester configuration."""

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate RPC URL format.

        Args:
            url: URL to validate

        Returns:
            True if valid

        Raises:
            ValidationError: If URL is invalid
        """
        if not url:
            raise ValidationError("URL cannot be empty")

        try:
            parsed = urlparse(url)

            if not parsed.scheme:
                raise ValidationError(f"URL missing scheme: {url}")

            if parsed.scheme not in ["http", "https", "ws", "wss"]:
                raise ValidationError(f"Invalid URL scheme: {parsed.scheme}")

            if not parsed.netloc:
                raise ValidationError(f"URL missing host: {url}")

            return True

        except Exception as e:
            raise ValidationError(f"Invalid URL format: {url} - {str(e)}")

    @staticmethod
    def validate_rpc_urls(urls: List[str]) -> bool:
        """
        Validate list of RPC URLs.

        Args:
            urls: List of URLs to validate

        Returns:
            True if all valid

        Raises:
            ValidationError: If any URL is invalid
        """
        if not urls:
            raise ValidationError("At least one RPC URL is required")

        if not isinstance(urls, list):
            raise ValidationError("RPC URLs must be a list")

        for url in urls:
            ConfigValidator.validate_url(url)

        return True

    @staticmethod
    def validate_num_requests(num: int) -> bool:
        """
        Validate number of requests.

        Args:
            num: Number of requests

        Returns:
            True if valid

        Raises:
            ValidationError: If invalid
        """
        if not isinstance(num, int):
            raise ValidationError("Number of requests must be an integer")

        if num < 1:
            raise ValidationError("Number of requests must be at least 1")

        if num > 10000:
            raise ValidationError("Number of requests cannot exceed 10000")

        return True

    @staticmethod
    def validate_concurrent_requests(num: int) -> bool:
        """
        Validate concurrent requests setting.

        Args:
            num: Number of concurrent requests

        Returns:
            True if valid

        Raises:
            ValidationError: If invalid
        """
        if not isinstance(num, int):
            raise ValidationError("Concurrent requests must be an integer")

        if num < 1:
            raise ValidationError("Concurrent requests must be at least 1")

        if num > 100:
            raise ValidationError("Concurrent requests cannot exceed 100")

        return True

    @staticmethod
    def validate_timeout(timeout: float) -> bool:
        """
        Validate timeout setting.

        Args:
            timeout: Timeout in seconds

        Returns:
            True if valid

        Raises:
            ValidationError: If invalid
        """
        if not isinstance(timeout, (int, float)):
            raise ValidationError("Timeout must be a number")

        if timeout <= 0:
            raise ValidationError("Timeout must be positive")

        if timeout > 300:
            raise ValidationError("Timeout cannot exceed 300 seconds")

        return True

    @staticmethod
    def validate_retry_attempts(num: int) -> bool:
        """
        Validate retry attempts setting.

        Args:
            num: Number of retry attempts

        Returns:
            True if valid

        Raises:
            ValidationError: If invalid
        """
        if not isinstance(num, int):
            raise ValidationError("Retry attempts must be an integer")

        if num < 0:
            raise ValidationError("Retry attempts cannot be negative")

        if num > 10:
            raise ValidationError("Retry attempts cannot exceed 10")

        return True

    @staticmethod
    def validate_rpc_method(method: str) -> bool:
        """
        Validate RPC method name.

        Args:
            method: RPC method name

        Returns:
            True if valid

        Raises:
            ValidationError: If invalid
        """
        if not method:
            raise ValidationError("RPC method cannot be empty")

        if not isinstance(method, str):
            raise ValidationError("RPC method must be a string")

        # Valid method format: namespace_methodName
        pattern = r"^[a-z]+[a-zA-Z0-9]*_[a-zA-Z][a-zA-Z0-9]*$"
        if not re.match(pattern, method):
            raise ValidationError(
                f"Invalid RPC method format: {method}. "
                "Expected format: namespace_methodName (e.g., eth_blockNumber)"
            )

        return True

    @staticmethod
    def validate_test_methods(methods: List[str]) -> bool:
        """
        Validate list of RPC methods.

        Args:
            methods: List of RPC methods

        Returns:
            True if all valid

        Raises:
            ValidationError: If any method is invalid
        """
        if not methods:
            raise ValidationError("At least one RPC method is required")

        if not isinstance(methods, list):
            raise ValidationError("Test methods must be a list")

        for method in methods:
            ConfigValidator.validate_rpc_method(method)

        return True

    @staticmethod
    def validate_ethereum_address(address: str) -> bool:
        """
        Validate Ethereum address format.

        Args:
            address: Ethereum address

        Returns:
            True if valid

        Raises:
            ValidationError: If invalid
        """
        if not address:
            return True  # Optional field

        if not isinstance(address, str):
            raise ValidationError("Ethereum address must be a string")

        # Check format: 0x followed by 40 hexadecimal characters
        pattern = r"^0x[a-fA-F0-9]{40}$"
        if not re.match(pattern, address):
            raise ValidationError(
                f"Invalid Ethereum address format: {address}. "
                "Expected format: 0x followed by 40 hex characters"
            )

        return True

    @staticmethod
    def validate_output_dir(path: str) -> bool:
        """
        Validate output directory path.

        Args:
            path: Directory path

        Returns:
            True if valid

        Raises:
            ValidationError: If invalid
        """
        if not path:
            raise ValidationError("Output directory cannot be empty")

        if not isinstance(path, str):
            raise ValidationError("Output directory must be a string")

        # Check for invalid characters
        invalid_chars = ["<", ">", ":", '"', "|", "?", "*"]
        for char in invalid_chars:
            if char in path:
                raise ValidationError(f"Output directory contains invalid character: {char}")

        return True


class DataValidator:
    """Validates RPC response data."""

    @staticmethod
    def validate_json_rpc_response(data: Any) -> bool:
        """
        Validate JSON-RPC 2.0 response format.

        Args:
            data: Response data to validate

        Returns:
            True if valid

        Raises:
            ValidationError: If invalid
        """
        if not isinstance(data, dict):
            raise ValidationError("JSON-RPC response must be a dictionary")

        if "jsonrpc" not in data:
            raise ValidationError("Missing 'jsonrpc' field in response")

        if data["jsonrpc"] != "2.0":
            raise ValidationError(f"Invalid JSON-RPC version: {data['jsonrpc']}")

        if "id" not in data:
            raise ValidationError("Missing 'id' field in response")

        if "result" not in data and "error" not in data:
            raise ValidationError("Response must contain either 'result' or 'error'")

        if "error" in data:
            DataValidator.validate_json_rpc_error(data["error"])

        return True

    @staticmethod
    def validate_json_rpc_error(error: Any) -> bool:
        """
        Validate JSON-RPC error format.

        Args:
            error: Error object to validate

        Returns:
            True if valid

        Raises:
            ValidationError: If invalid
        """
        if not isinstance(error, dict):
            raise ValidationError("JSON-RPC error must be a dictionary")

        if "code" not in error:
            raise ValidationError("Missing 'code' in error object")

        if "message" not in error:
            raise ValidationError("Missing 'message' in error object")

        if not isinstance(error["code"], int):
            raise ValidationError("Error code must be an integer")

        if not isinstance(error["message"], str):
            raise ValidationError("Error message must be a string")

        return True
