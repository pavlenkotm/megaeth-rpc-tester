"""
Custom exceptions for RPC Tester.
"""


class RPCTesterException(Exception):
    """Base exception for all RPC Tester errors."""
    pass


class ConfigurationError(RPCTesterException):
    """Raised when configuration is invalid."""
    pass


class EndpointError(RPCTesterException):
    """Raised when an RPC endpoint returns an error."""

    def __init__(self, message: str, url: str = None, method: str = None):
        super().__init__(message)
        self.url = url
        self.method = method


class TimeoutError(RPCTesterException):
    """Raised when an RPC request times out."""

    def __init__(self, message: str, url: str = None, timeout: float = None):
        super().__init__(message)
        self.url = url
        self.timeout = timeout


class NetworkError(RPCTesterException):
    """Raised when a network error occurs."""

    def __init__(self, message: str, url: str = None, status_code: int = None):
        super().__init__(message)
        self.url = url
        self.status_code = status_code


class ValidationError(RPCTesterException):
    """Raised when data validation fails."""
    pass


class ExportError(RPCTesterException):
    """Raised when result export fails."""

    def __init__(self, message: str, format: str = None, filepath: str = None):
        super().__init__(message)
        self.format = format
        self.filepath = filepath


class RateLimitError(RPCTesterException):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, url: str = None, retry_after: float = None):
        super().__init__(message)
        self.url = url
        self.retry_after = retry_after


class AuthenticationError(RPCTesterException):
    """Raised when authentication fails."""

    def __init__(self, message: str, url: str = None):
        super().__init__(message)
        self.url = url
