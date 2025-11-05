"""
Rate limiting functionality for RPC requests.
"""

import asyncio
import time
from typing import Dict, Optional
from dataclasses import dataclass
from collections import deque


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""

    requests_per_second: float
    burst_size: int = None

    def __post_init__(self):
        if self.burst_size is None:
            self.burst_size = int(self.requests_per_second)


class TokenBucketRateLimiter:
    """Token bucket algorithm for rate limiting."""

    def __init__(
        self,
        requests_per_second: float,
        burst_size: Optional[int] = None
    ):
        """
        Initialize token bucket rate limiter.

        Args:
            requests_per_second: Maximum requests per second
            burst_size: Maximum burst size (defaults to requests_per_second)
        """
        self.rate = requests_per_second
        self.burst_size = burst_size or int(requests_per_second)
        self.tokens = float(self.burst_size)
        self.last_update = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1):
        """
        Acquire tokens before making a request.

        Args:
            tokens: Number of tokens to acquire

        Blocks until tokens are available.
        """
        async with self.lock:
            while True:
                now = time.time()
                elapsed = now - self.last_update

                # Add tokens based on elapsed time
                self.tokens = min(
                    self.burst_size,
                    self.tokens + elapsed * self.rate
                )
                self.last_update = now

                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return

                # Calculate wait time
                wait_time = (tokens - self.tokens) / self.rate
                await asyncio.sleep(wait_time)

    def get_available_tokens(self) -> float:
        """Get number of available tokens."""
        now = time.time()
        elapsed = now - self.last_update
        return min(
            self.burst_size,
            self.tokens + elapsed * self.rate
        )


class SlidingWindowRateLimiter:
    """Sliding window algorithm for rate limiting."""

    def __init__(
        self,
        requests_per_second: float,
        window_size: float = 1.0
    ):
        """
        Initialize sliding window rate limiter.

        Args:
            requests_per_second: Maximum requests per second
            window_size: Time window in seconds
        """
        self.rate = requests_per_second
        self.window_size = window_size
        self.requests = deque()
        self.lock = asyncio.Lock()

    async def acquire(self):
        """Acquire permission to make a request."""
        async with self.lock:
            while True:
                now = time.time()

                # Remove old requests outside the window
                while self.requests and self.requests[0] < now - self.window_size:
                    self.requests.popleft()

                # Check if we can make a new request
                if len(self.requests) < self.rate * self.window_size:
                    self.requests.append(now)
                    return

                # Calculate wait time
                if self.requests:
                    oldest_request = self.requests[0]
                    wait_time = (oldest_request + self.window_size) - now
                    if wait_time > 0:
                        await asyncio.sleep(wait_time)
                else:
                    return

    def get_request_count(self) -> int:
        """Get current request count in window."""
        now = time.time()
        while self.requests and self.requests[0] < now - self.window_size:
            self.requests.popleft()
        return len(self.requests)


class PerEndpointRateLimiter:
    """Rate limiter that tracks limits per endpoint."""

    def __init__(self, default_rate: float = 10.0):
        """
        Initialize per-endpoint rate limiter.

        Args:
            default_rate: Default requests per second for endpoints
        """
        self.default_rate = default_rate
        self.limiters: Dict[str, TokenBucketRateLimiter] = {}
        self.custom_rates: Dict[str, float] = {}
        self.lock = asyncio.Lock()

    def set_rate_limit(self, url: str, requests_per_second: float):
        """
        Set custom rate limit for an endpoint.

        Args:
            url: Endpoint URL
            requests_per_second: Rate limit
        """
        self.custom_rates[url] = requests_per_second
        self.limiters[url] = TokenBucketRateLimiter(requests_per_second)

    async def acquire(self, url: str):
        """
        Acquire permission to make request to endpoint.

        Args:
            url: Endpoint URL
        """
        async with self.lock:
            if url not in self.limiters:
                rate = self.custom_rates.get(url, self.default_rate)
                self.limiters[url] = TokenBucketRateLimiter(rate)

        limiter = self.limiters[url]
        await limiter.acquire()

    def get_stats(self, url: str) -> Dict[str, float]:
        """
        Get statistics for endpoint.

        Args:
            url: Endpoint URL

        Returns:
            Dictionary with rate limit stats
        """
        if url not in self.limiters:
            return {
                "rate_limit": self.custom_rates.get(url, self.default_rate),
                "available_tokens": 0
            }

        limiter = self.limiters[url]
        return {
            "rate_limit": limiter.rate,
            "burst_size": limiter.burst_size,
            "available_tokens": limiter.get_available_tokens()
        }


class AdaptiveRateLimiter:
    """Adaptive rate limiter that adjusts based on errors."""

    def __init__(
        self,
        initial_rate: float = 10.0,
        min_rate: float = 1.0,
        max_rate: float = 100.0,
        increase_factor: float = 1.2,
        decrease_factor: float = 0.5
    ):
        """
        Initialize adaptive rate limiter.

        Args:
            initial_rate: Initial requests per second
            min_rate: Minimum rate limit
            max_rate: Maximum rate limit
            increase_factor: Factor to increase rate on success
            decrease_factor: Factor to decrease rate on error
        """
        self.current_rate = initial_rate
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.increase_factor = increase_factor
        self.decrease_factor = decrease_factor
        self.limiter = TokenBucketRateLimiter(initial_rate)
        self.consecutive_successes = 0
        self.consecutive_errors = 0
        self.lock = asyncio.Lock()

    async def acquire(self):
        """Acquire permission to make request."""
        await self.limiter.acquire()

    async def report_success(self):
        """Report successful request to adapt rate."""
        async with self.lock:
            self.consecutive_errors = 0
            self.consecutive_successes += 1

            # Increase rate after 10 consecutive successes
            if self.consecutive_successes >= 10:
                new_rate = min(
                    self.max_rate,
                    self.current_rate * self.increase_factor
                )
                if new_rate != self.current_rate:
                    self.current_rate = new_rate
                    self.limiter = TokenBucketRateLimiter(new_rate)
                    self.consecutive_successes = 0

    async def report_error(self, is_rate_limit_error: bool = False):
        """
        Report failed request to adapt rate.

        Args:
            is_rate_limit_error: Whether error was due to rate limiting
        """
        async with self.lock:
            self.consecutive_successes = 0

            if is_rate_limit_error:
                # Immediately decrease rate on rate limit error
                new_rate = max(
                    self.min_rate,
                    self.current_rate * self.decrease_factor
                )
                self.current_rate = new_rate
                self.limiter = TokenBucketRateLimiter(new_rate)
                self.consecutive_errors = 0
            else:
                self.consecutive_errors += 1

                # Decrease rate after 3 consecutive errors
                if self.consecutive_errors >= 3:
                    new_rate = max(
                        self.min_rate,
                        self.current_rate * self.decrease_factor
                    )
                    if new_rate != self.current_rate:
                        self.current_rate = new_rate
                        self.limiter = TokenBucketRateLimiter(new_rate)
                        self.consecutive_errors = 0

    def get_current_rate(self) -> float:
        """Get current rate limit."""
        return self.current_rate

    def get_stats(self) -> Dict[str, float]:
        """Get rate limiter statistics."""
        return {
            "current_rate": self.current_rate,
            "min_rate": self.min_rate,
            "max_rate": self.max_rate,
            "consecutive_successes": self.consecutive_successes,
            "consecutive_errors": self.consecutive_errors,
            "available_tokens": self.limiter.get_available_tokens()
        }
