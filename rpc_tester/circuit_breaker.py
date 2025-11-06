"""
Circuit breaker pattern implementation for RPC requests.

Prevents cascading failures by stopping requests to failing endpoints.
"""

import asyncio
from typing import Dict, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import time


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Blocking requests
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""
    failure_threshold: int = 5  # Number of failures before opening
    success_threshold: int = 2  # Number of successes to close from half-open
    timeout: float = 60.0  # Timeout in seconds before attempting recovery
    half_open_max_calls: int = 3  # Max calls in half-open state


class CircuitBreakerError(Exception):
    """Exception raised when circuit is open."""
    pass


class CircuitBreaker:
    """Circuit breaker for protecting against failing services."""

    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        """
        Initialize circuit breaker.

        Args:
            name: Circuit breaker name
            config: Configuration
        """
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.half_open_calls = 0
        self._lock = asyncio.Lock()

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.

        Args:
            func: Async function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            CircuitBreakerError: If circuit is open
        """
        async with self._lock:
            await self._check_state()

            if self.state == CircuitState.OPEN:
                raise CircuitBreakerError(
                    f"Circuit breaker '{self.name}' is OPEN"
                )

            if self.state == CircuitState.HALF_OPEN:
                if self.half_open_calls >= self.config.half_open_max_calls:
                    raise CircuitBreakerError(
                        f"Circuit breaker '{self.name}' max half-open calls reached"
                    )
                self.half_open_calls += 1

        # Execute function
        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except Exception as e:
            await self._on_failure()
            raise e

    async def _check_state(self):
        """Check and update circuit state."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
                print(f"Circuit breaker '{self.name}' entering HALF_OPEN state")

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return False

        elapsed = time.time() - self.last_failure_time
        return elapsed >= self.config.timeout

    async def _on_success(self):
        """Handle successful call."""
        async with self._lock:
            self.failure_count = 0

            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1

                if self.success_count >= self.config.success_threshold:
                    self.state = CircuitState.CLOSED
                    self.success_count = 0
                    print(f"Circuit breaker '{self.name}' CLOSED (recovered)")

    async def _on_failure(self):
        """Handle failed call."""
        async with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.state == CircuitState.HALF_OPEN:
                # Immediately open on failure in half-open state
                self.state = CircuitState.OPEN
                self.success_count = 0
                print(f"Circuit breaker '{self.name}' OPEN (half-open test failed)")

            elif self.failure_count >= self.config.failure_threshold:
                self.state = CircuitState.OPEN
                print(
                    f"Circuit breaker '{self.name}' OPEN "
                    f"(threshold: {self.config.failure_threshold} failures)"
                )

    def reset(self):
        """Manually reset circuit breaker."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0

    def get_state(self) -> Dict[str, Any]:
        """Get current circuit breaker state."""
        return {
            'name': self.name,
            'state': self.state.value,
            'failure_count': self.failure_count,
            'success_count': self.success_count,
            'last_failure_time': self.last_failure_time,
            'config': {
                'failure_threshold': self.config.failure_threshold,
                'success_threshold': self.config.success_threshold,
                'timeout': self.config.timeout,
                'half_open_max_calls': self.config.half_open_max_calls
            }
        }


class CircuitBreakerRegistry:
    """Registry for managing multiple circuit breakers."""

    def __init__(self):
        """Initialize registry."""
        self.breakers: Dict[str, CircuitBreaker] = {}

    def get_breaker(self, name: str,
                   config: Optional[CircuitBreakerConfig] = None) -> CircuitBreaker:
        """
        Get or create circuit breaker.

        Args:
            name: Circuit breaker name
            config: Configuration (only used for new breakers)

        Returns:
            CircuitBreaker instance
        """
        if name not in self.breakers:
            self.breakers[name] = CircuitBreaker(name, config)

        return self.breakers[name]

    def reset_all(self):
        """Reset all circuit breakers."""
        for breaker in self.breakers.values():
            breaker.reset()

    def get_all_states(self) -> Dict[str, Dict[str, Any]]:
        """Get states of all circuit breakers."""
        return {
            name: breaker.get_state()
            for name, breaker in self.breakers.items()
        }

    def get_open_circuits(self) -> List[str]:
        """Get list of open circuit breakers."""
        return [
            name for name, breaker in self.breakers.items()
            if breaker.state == CircuitState.OPEN
        ]


class AdaptiveCircuitBreaker(CircuitBreaker):
    """Circuit breaker with adaptive thresholds based on error rate."""

    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None,
                 window_size: int = 100):
        """
        Initialize adaptive circuit breaker.

        Args:
            name: Circuit breaker name
            config: Configuration
            window_size: Size of sliding window for error rate calculation
        """
        super().__init__(name, config)
        self.window_size = window_size
        self.recent_calls: List[bool] = []  # True = success, False = failure

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with adaptive circuit breaker."""
        result = await super().call(func, *args, **kwargs)

        # Track call result
        async with self._lock:
            self.recent_calls.append(True)
            if len(self.recent_calls) > self.window_size:
                self.recent_calls.pop(0)

        return result

    async def _on_failure(self):
        """Handle failure with adaptive threshold."""
        async with self._lock:
            self.recent_calls.append(False)
            if len(self.recent_calls) > self.window_size:
                self.recent_calls.pop(0)

            # Calculate error rate
            if len(self.recent_calls) >= 10:  # Minimum calls before adapting
                error_rate = sum(1 for x in self.recent_calls if not x) / len(self.recent_calls)

                # Open circuit if error rate > 50%
                if error_rate > 0.5:
                    self.state = CircuitState.OPEN
                    self.last_failure_time = time.time()
                    print(
                        f"Adaptive circuit breaker '{self.name}' OPEN "
                        f"(error rate: {error_rate:.2%})"
                    )
                    return

        await super()._on_failure()

    def get_metrics(self) -> Dict[str, Any]:
        """Get adaptive circuit breaker metrics."""
        base_state = self.get_state()

        if len(self.recent_calls) > 0:
            error_rate = sum(1 for x in self.recent_calls if not x) / len(self.recent_calls)
        else:
            error_rate = 0

        base_state['adaptive_metrics'] = {
            'window_size': self.window_size,
            'recent_calls_count': len(self.recent_calls),
            'error_rate': error_rate
        }

        return base_state


class BulkheadPattern:
    """Bulkhead pattern to limit concurrent requests."""

    def __init__(self, name: str, max_concurrent: int = 10):
        """
        Initialize bulkhead.

        Args:
            name: Bulkhead name
            max_concurrent: Maximum concurrent requests
        """
        self.name = name
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_calls = 0
        self.total_calls = 0
        self.rejected_calls = 0

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with bulkhead protection.

        Args:
            func: Async function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result
        """
        self.total_calls += 1

        acquired = self.semaphore.locked()
        if acquired:
            self.rejected_calls += 1
            raise Exception(f"Bulkhead '{self.name}' is full")

        async with self.semaphore:
            self.active_calls += 1
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                self.active_calls -= 1

    def get_stats(self) -> Dict[str, Any]:
        """Get bulkhead statistics."""
        return {
            'name': self.name,
            'max_concurrent': self.max_concurrent,
            'active_calls': self.active_calls,
            'total_calls': self.total_calls,
            'rejected_calls': self.rejected_calls,
            'rejection_rate': (
                self.rejected_calls / self.total_calls
                if self.total_calls > 0 else 0
            )
        }
