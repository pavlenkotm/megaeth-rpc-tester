"""
Custom exceptions for RPC Tester.
"""


class RPCTesterError(Exception):
    """Base exception for RPC Tester."""
    pass


class ConfigurationError(RPCTesterError):
    """Raised when configuration is invalid."""
    pass


class ConnectionError(RPCTesterError):
    """Raised when connection to RPC endpoint fails."""
    pass


class TimeoutError(RPCTesterError):
    """Raised when request times out."""
    pass


class InvalidResponseError(RPCTesterError):
    """Raised when RPC response is invalid."""
    pass


class ValidationError(RPCTesterError):
    """Raised when validation fails."""
    pass


class ExportError(RPCTesterError):
    """Raised when export operation fails."""
    pass


class MethodNotSupportedError(RPCTesterError):
    """Raised when RPC method is not supported."""
    pass
