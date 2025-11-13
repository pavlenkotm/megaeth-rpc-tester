"""
Structured logging configuration for RPC Tester.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"

        return super().format(record)


class RPCLogger:
    """Centralized logger configuration for RPC Tester."""

    _instance = None

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize logger configuration."""
        if self._initialized:
            return

        self.logger = logging.getLogger("rpc_tester")
        self.logger.setLevel(logging.DEBUG)
        self._initialized = True

    def setup_console_logging(self, level: int = logging.INFO, use_colors: bool = True):
        """
        Setup console logging handler.

        Args:
            level: Logging level
            use_colors: Use colored output
        """
        # Remove existing console handlers
        for handler in self.logger.handlers[:]:
            if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                self.logger.removeHandler(handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)

        if use_colors:
            formatter = ColoredFormatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
        else:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )

        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def setup_file_logging(
        self, log_file: str = "rpc_tester.log", level: int = logging.DEBUG, use_json: bool = False
    ):
        """
        Setup file logging handler.

        Args:
            log_file: Path to log file
            level: Logging level
            use_json: Use JSON formatting
        """
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Remove existing file handlers
        for handler in self.logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                self.logger.removeHandler(handler)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        if use_json:
            formatter = JSONFormatter()
        else:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance."""
        return self.logger

    def log_request(
        self,
        url: str,
        method: str,
        params: Any = None,
        latency_ms: float = None,
        success: bool = True,
        error: str = None,
    ):
        """
        Log RPC request with structured data.

        Args:
            url: RPC endpoint URL
            method: RPC method
            params: Request parameters
            latency_ms: Request latency
            success: Request success status
            error: Error message if failed
        """
        extra = {
            "url": url,
            "method": method,
            "params": params,
            "latency_ms": latency_ms,
            "success": success,
        }

        if success:
            self.logger.info(
                f"RPC request succeeded: {method} to {url} ({latency_ms:.2f}ms)",
                extra={"extra": extra},
            )
        else:
            extra["error"] = error
            self.logger.error(
                f"RPC request failed: {method} to {url} - {error}", extra={"extra": extra}
            )

    def log_test_start(self, config: Dict[str, Any]):
        """
        Log test start with configuration.

        Args:
            config: Test configuration
        """
        self.logger.info("Starting RPC tests", extra={"extra": {"config": config}})

    def log_test_complete(self, summary: Dict[str, Any]):
        """
        Log test completion with summary.

        Args:
            summary: Test summary statistics
        """
        self.logger.info("RPC tests completed", extra={"extra": {"summary": summary}})

    def log_cache_hit(self, url: str, method: str):
        """Log cache hit."""
        self.logger.debug(
            f"Cache hit for {method} to {url}",
            extra={"extra": {"url": url, "method": method, "cache": "hit"}},
        )

    def log_cache_miss(self, url: str, method: str):
        """Log cache miss."""
        self.logger.debug(
            f"Cache miss for {method} to {url}",
            extra={"extra": {"url": url, "method": method, "cache": "miss"}},
        )


# Global logger instance
def get_logger() -> logging.Logger:
    """Get the global RPC Tester logger."""
    return RPCLogger().get_logger()


def setup_logging(
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    log_file: str = None,
    use_json: bool = False,
    use_colors: bool = True,
):
    """
    Setup logging configuration.

    Args:
        console_level: Console logging level
        file_level: File logging level
        log_file: Path to log file (None to disable file logging)
        use_json: Use JSON formatting for file logs
        use_colors: Use colored console output
    """
    rpc_logger = RPCLogger()
    rpc_logger.setup_console_logging(level=console_level, use_colors=use_colors)

    if log_file:
        rpc_logger.setup_file_logging(log_file=log_file, level=file_level, use_json=use_json)
