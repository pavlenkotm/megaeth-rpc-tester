"""
Authentication handlers for RPC requests.

Support for various authentication methods including API keys, OAuth, JWT, etc.
"""

import base64
import hashlib
import hmac
import time
from typing import Dict, Optional, Any
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import json


class AuthHandler(ABC):
    """Base class for authentication handlers."""

    @abstractmethod
    def get_headers(self) -> Dict[str, str]:
        """
        Get authentication headers.

        Returns:
            Dictionary of HTTP headers
        """
        pass

    @abstractmethod
    def get_params(self) -> Dict[str, str]:
        """
        Get authentication query parameters.

        Returns:
            Dictionary of query parameters
        """
        pass


class NoAuth(AuthHandler):
    """No authentication."""

    def get_headers(self) -> Dict[str, str]:
        """Get headers (empty)."""
        return {}

    def get_params(self) -> Dict[str, str]:
        """Get params (empty)."""
        return {}


class APIKeyAuth(AuthHandler):
    """API key authentication."""

    def __init__(self, api_key: str, header_name: str = "X-API-Key",
                 in_query: bool = False, query_param: str = "api_key"):
        """
        Initialize API key auth.

        Args:
            api_key: API key
            header_name: Header name for API key
            in_query: Whether to send API key as query parameter
            query_param: Query parameter name
        """
        self.api_key = api_key
        self.header_name = header_name
        self.in_query = in_query
        self.query_param = query_param

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        if not self.in_query:
            return {self.header_name: self.api_key}
        return {}

    def get_params(self) -> Dict[str, str]:
        """Get authentication parameters."""
        if self.in_query:
            return {self.query_param: self.api_key}
        return {}


class BasicAuth(AuthHandler):
    """HTTP Basic authentication."""

    def __init__(self, username: str, password: str):
        """
        Initialize basic auth.

        Args:
            username: Username
            password: Password
        """
        self.username = username
        self.password = password

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {encoded}"
        }

    def get_params(self) -> Dict[str, str]:
        """Get params (empty for Basic auth)."""
        return {}


class BearerTokenAuth(AuthHandler):
    """Bearer token authentication."""

    def __init__(self, token: str):
        """
        Initialize bearer token auth.

        Args:
            token: Bearer token
        """
        self.token = token

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        return {
            "Authorization": f"Bearer {self.token}"
        }

    def get_params(self) -> Dict[str, str]:
        """Get params (empty)."""
        return {}


class JWTAuth(AuthHandler):
    """JWT (JSON Web Token) authentication."""

    def __init__(self, token: str, refresh_token: Optional[str] = None,
                 refresh_callback: Optional[callable] = None):
        """
        Initialize JWT auth.

        Args:
            token: JWT token
            refresh_token: Refresh token (optional)
            refresh_callback: Callback to refresh token
        """
        self.token = token
        self.refresh_token = refresh_token
        self.refresh_callback = refresh_callback
        self.token_expiry: Optional[datetime] = None

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        # Check if token needs refresh
        if self.token_expiry and datetime.now() >= self.token_expiry:
            if self.refresh_callback:
                self.token = self.refresh_callback(self.refresh_token)

        return {
            "Authorization": f"Bearer {self.token}"
        }

    def get_params(self) -> Dict[str, str]:
        """Get params (empty)."""
        return {}

    def set_token_expiry(self, expiry: datetime):
        """Set token expiry time."""
        self.token_expiry = expiry


class OAuth2Auth(AuthHandler):
    """OAuth 2.0 authentication."""

    def __init__(self, access_token: str, token_type: str = "Bearer",
                 refresh_token: Optional[str] = None,
                 expires_at: Optional[datetime] = None):
        """
        Initialize OAuth2 auth.

        Args:
            access_token: Access token
            token_type: Token type (usually "Bearer")
            refresh_token: Refresh token
            expires_at: Token expiration time
        """
        self.access_token = access_token
        self.token_type = token_type
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        return {
            "Authorization": f"{self.token_type} {self.access_token}"
        }

    def get_params(self) -> Dict[str, str]:
        """Get params (empty)."""
        return {}

    def is_expired(self) -> bool:
        """Check if token is expired."""
        if self.expires_at:
            return datetime.now() >= self.expires_at
        return False


class HMACAuth(AuthHandler):
    """HMAC signature authentication."""

    def __init__(self, access_key: str, secret_key: str,
                 algorithm: str = "sha256"):
        """
        Initialize HMAC auth.

        Args:
            access_key: Access key
            secret_key: Secret key
            algorithm: Hash algorithm
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.algorithm = algorithm

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        timestamp = str(int(time.time()))
        message = f"{self.access_key}{timestamp}"

        # Calculate HMAC signature
        signature = hmac.new(
            self.secret_key.encode(),
            message.encode(),
            getattr(hashlib, self.algorithm)
        ).hexdigest()

        return {
            "X-Access-Key": self.access_key,
            "X-Timestamp": timestamp,
            "X-Signature": signature
        }

    def get_params(self) -> Dict[str, str]:
        """Get params (empty)."""
        return {}


class CustomHeaderAuth(AuthHandler):
    """Custom header-based authentication."""

    def __init__(self, headers: Dict[str, str]):
        """
        Initialize custom header auth.

        Args:
            headers: Custom authentication headers
        """
        self.custom_headers = headers

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        return self.custom_headers.copy()

    def get_params(self) -> Dict[str, str]:
        """Get params (empty)."""
        return {}


class AWSSignatureAuth(AuthHandler):
    """AWS Signature Version 4 authentication."""

    def __init__(self, access_key: str, secret_key: str,
                 region: str = "us-east-1", service: str = "execute-api"):
        """
        Initialize AWS Signature auth.

        Args:
            access_key: AWS access key
            secret_key: AWS secret key
            region: AWS region
            service: AWS service name
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.service = service

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers (simplified)."""
        # This is a simplified version
        # Full AWS SigV4 implementation would be more complex
        timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

        return {
            "X-Amz-Date": timestamp,
            "Authorization": f"AWS4-HMAC-SHA256 Credential={self.access_key}/..."
        }

    def get_params(self) -> Dict[str, str]:
        """Get params (empty)."""
        return {}


class AuthManager:
    """Manage authentication for multiple endpoints."""

    def __init__(self):
        """Initialize auth manager."""
        self.handlers: Dict[str, AuthHandler] = {}
        self.default_handler: AuthHandler = NoAuth()

    def register_handler(self, endpoint: str, handler: AuthHandler):
        """
        Register authentication handler for endpoint.

        Args:
            endpoint: Endpoint URL or pattern
            handler: Authentication handler
        """
        self.handlers[endpoint] = handler

    def set_default_handler(self, handler: AuthHandler):
        """Set default authentication handler."""
        self.default_handler = handler

    def get_handler(self, endpoint: str) -> AuthHandler:
        """
        Get authentication handler for endpoint.

        Args:
            endpoint: Endpoint URL

        Returns:
            AuthHandler instance
        """
        # Exact match
        if endpoint in self.handlers:
            return self.handlers[endpoint]

        # Pattern matching (simple contains check)
        for pattern, handler in self.handlers.items():
            if pattern in endpoint or endpoint.startswith(pattern):
                return handler

        return self.default_handler

    def get_auth_headers(self, endpoint: str) -> Dict[str, str]:
        """Get authentication headers for endpoint."""
        handler = self.get_handler(endpoint)
        return handler.get_headers()

    def get_auth_params(self, endpoint: str) -> Dict[str, str]:
        """Get authentication parameters for endpoint."""
        handler = self.get_handler(endpoint)
        return handler.get_params()


class AuthConfig:
    """Configuration for authentication."""

    @staticmethod
    def from_dict(config: Dict[str, Any]) -> AuthHandler:
        """
        Create auth handler from configuration dictionary.

        Args:
            config: Configuration dictionary

        Returns:
            AuthHandler instance
        """
        auth_type = config.get('type', 'none').lower()

        if auth_type == 'none':
            return NoAuth()

        elif auth_type == 'api_key':
            return APIKeyAuth(
                api_key=config['api_key'],
                header_name=config.get('header_name', 'X-API-Key'),
                in_query=config.get('in_query', False),
                query_param=config.get('query_param', 'api_key')
            )

        elif auth_type == 'basic':
            return BasicAuth(
                username=config['username'],
                password=config['password']
            )

        elif auth_type == 'bearer':
            return BearerTokenAuth(
                token=config['token']
            )

        elif auth_type == 'jwt':
            return JWTAuth(
                token=config['token'],
                refresh_token=config.get('refresh_token')
            )

        elif auth_type == 'oauth2':
            return OAuth2Auth(
                access_token=config['access_token'],
                token_type=config.get('token_type', 'Bearer'),
                refresh_token=config.get('refresh_token')
            )

        elif auth_type == 'hmac':
            return HMACAuth(
                access_key=config['access_key'],
                secret_key=config['secret_key'],
                algorithm=config.get('algorithm', 'sha256')
            )

        elif auth_type == 'custom':
            return CustomHeaderAuth(
                headers=config['headers']
            )

        else:
            raise ValueError(f"Unknown auth type: {auth_type}")

    @staticmethod
    def from_file(file_path: str) -> AuthHandler:
        """
        Load auth configuration from file.

        Args:
            file_path: Path to configuration file (JSON or YAML)

        Returns:
            AuthHandler instance
        """
        import json
        from pathlib import Path

        path = Path(file_path)

        with open(path, 'r') as f:
            if path.suffix in ['.json']:
                config = json.load(f)
            elif path.suffix in ['.yaml', '.yml']:
                import yaml
                config = yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported file format: {path.suffix}")

        return AuthConfig.from_dict(config)
