"""
Health check and monitoring for RPC endpoints.
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class HealthStatus(Enum):
    """Health status enumeration."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheckResult:
    """Result of a health check."""

    url: str
    timestamp: datetime
    status: HealthStatus
    latency_ms: float
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class HealthChecker:
    """Monitors health of RPC endpoints."""

    def __init__(
        self,
        healthy_threshold_ms: float = 1000.0,
        degraded_threshold_ms: float = 3000.0,
        check_interval: float = 60.0
    ):
        """
        Initialize health checker.

        Args:
            healthy_threshold_ms: Max latency for healthy status
            degraded_threshold_ms: Max latency for degraded status
            check_interval: Seconds between health checks
        """
        self.healthy_threshold = healthy_threshold_ms
        self.degraded_threshold = degraded_threshold_ms
        self.check_interval = check_interval
        self.results: Dict[str, List[HealthCheckResult]] = {}
        self.running = False
        self.tasks: List[asyncio.Task] = []

    async def check_endpoint(
        self,
        url: str,
        method: str = "eth_blockNumber",
        params: Optional[List] = None
    ) -> HealthCheckResult:
        """
        Perform health check on endpoint.

        Args:
            url: Endpoint URL
            method: RPC method to test
            params: Method parameters

        Returns:
            HealthCheckResult
        """
        import aiohttp

        start_time = time.perf_counter()
        details = {}

        try:
            timeout = aiohttp.ClientTimeout(total=10.0)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                payload = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": method,
                    "params": params or []
                }

                async with session.post(url, json=payload) as resp:
                    latency = (time.perf_counter() - start_time) * 1000

                    details["status_code"] = resp.status
                    details["method"] = method

                    if resp.status == 200:
                        data = await resp.json()

                        if "error" in data:
                            status = HealthStatus.UNHEALTHY
                            error = str(data["error"])
                            details["error_type"] = "rpc_error"
                        else:
                            # Determine status based on latency
                            if latency <= self.healthy_threshold:
                                status = HealthStatus.HEALTHY
                            elif latency <= self.degraded_threshold:
                                status = HealthStatus.DEGRADED
                            else:
                                status = HealthStatus.UNHEALTHY

                            error = None
                            details["result"] = data.get("result")

                    else:
                        status = HealthStatus.UNHEALTHY
                        error = f"HTTP {resp.status}"
                        details["error_type"] = "http_error"

                    return HealthCheckResult(
                        url=url,
                        timestamp=datetime.now(),
                        status=status,
                        latency_ms=latency,
                        details=details,
                        error=error
                    )

        except asyncio.TimeoutError:
            latency = (time.perf_counter() - start_time) * 1000
            return HealthCheckResult(
                url=url,
                timestamp=datetime.now(),
                status=HealthStatus.UNHEALTHY,
                latency_ms=latency,
                details={"error_type": "timeout"},
                error="Request timeout"
            )

        except Exception as e:
            latency = (time.perf_counter() - start_time) * 1000
            return HealthCheckResult(
                url=url,
                timestamp=datetime.now(),
                status=HealthStatus.UNHEALTHY,
                latency_ms=latency,
                details={"error_type": "connection_error"},
                error=str(e)
            )

    async def monitor_endpoint(
        self,
        url: str,
        method: str = "eth_blockNumber",
        params: Optional[List] = None
    ):
        """
        Continuously monitor endpoint health.

        Args:
            url: Endpoint URL
            method: RPC method to test
            params: Method parameters
        """
        if url not in self.results:
            self.results[url] = []

        while self.running:
            result = await self.check_endpoint(url, method, params)
            self.results[url].append(result)

            # Keep only last 100 results per endpoint
            if len(self.results[url]) > 100:
                self.results[url] = self.results[url][-100:]

            await asyncio.sleep(self.check_interval)

    def start_monitoring(
        self,
        urls: List[str],
        method: str = "eth_blockNumber",
        params: Optional[List] = None
    ):
        """
        Start monitoring multiple endpoints.

        Args:
            urls: List of endpoint URLs
            method: RPC method to test
            params: Method parameters
        """
        self.running = True

        for url in urls:
            task = asyncio.create_task(
                self.monitor_endpoint(url, method, params)
            )
            self.tasks.append(task)

    async def stop_monitoring(self):
        """Stop all monitoring tasks."""
        self.running = False

        for task in self.tasks:
            task.cancel()

        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()

    def get_current_status(self, url: str) -> Optional[HealthStatus]:
        """
        Get current health status for endpoint.

        Args:
            url: Endpoint URL

        Returns:
            Current HealthStatus or None
        """
        if url not in self.results or not self.results[url]:
            return None

        return self.results[url][-1].status

    def get_uptime_percentage(
        self,
        url: str,
        time_window: Optional[timedelta] = None
    ) -> float:
        """
        Calculate uptime percentage for endpoint.

        Args:
            url: Endpoint URL
            time_window: Time window to calculate over (None for all)

        Returns:
            Uptime percentage
        """
        if url not in self.results or not self.results[url]:
            return 0.0

        results = self.results[url]

        if time_window:
            cutoff = datetime.now() - time_window
            results = [r for r in results if r.timestamp >= cutoff]

        if not results:
            return 0.0

        healthy_count = sum(
            1 for r in results
            if r.status in (HealthStatus.HEALTHY, HealthStatus.DEGRADED)
        )

        return (healthy_count / len(results)) * 100

    def get_average_latency(
        self,
        url: str,
        time_window: Optional[timedelta] = None
    ) -> float:
        """
        Calculate average latency for endpoint.

        Args:
            url: Endpoint URL
            time_window: Time window to calculate over

        Returns:
            Average latency in ms
        """
        if url not in self.results or not self.results[url]:
            return 0.0

        results = self.results[url]

        if time_window:
            cutoff = datetime.now() - time_window
            results = [r for r in results if r.timestamp >= cutoff]

        if not results:
            return 0.0

        # Only count successful checks
        successful = [r for r in results if r.status != HealthStatus.UNHEALTHY]

        if not successful:
            return 0.0

        return sum(r.latency_ms for r in successful) / len(successful)

    def get_error_rate(
        self,
        url: str,
        time_window: Optional[timedelta] = None
    ) -> float:
        """
        Calculate error rate for endpoint.

        Args:
            url: Endpoint URL
            time_window: Time window to calculate over

        Returns:
            Error rate percentage
        """
        if url not in self.results or not self.results[url]:
            return 0.0

        results = self.results[url]

        if time_window:
            cutoff = datetime.now() - time_window
            results = [r for r in results if r.timestamp >= cutoff]

        if not results:
            return 0.0

        error_count = sum(1 for r in results if r.error is not None)
        return (error_count / len(results)) * 100

    def get_health_summary(
        self,
        url: str,
        time_window: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive health summary for endpoint.

        Args:
            url: Endpoint URL
            time_window: Time window to calculate over

        Returns:
            Dictionary with health metrics
        """
        if url not in self.results:
            return {
                "url": url,
                "status": "unknown",
                "uptime_percentage": 0.0,
                "avg_latency_ms": 0.0,
                "error_rate": 0.0,
                "total_checks": 0
            }

        results = self.results[url]

        if time_window:
            cutoff = datetime.now() - time_window
            results = [r for r in results if r.timestamp >= cutoff]

        current_status = self.get_current_status(url)
        uptime = self.get_uptime_percentage(url, time_window)
        avg_latency = self.get_average_latency(url, time_window)
        error_rate = self.get_error_rate(url, time_window)

        # Count status distribution
        status_counts = {
            "healthy": 0,
            "degraded": 0,
            "unhealthy": 0
        }

        for result in results:
            if result.status == HealthStatus.HEALTHY:
                status_counts["healthy"] += 1
            elif result.status == HealthStatus.DEGRADED:
                status_counts["degraded"] += 1
            else:
                status_counts["unhealthy"] += 1

        return {
            "url": url,
            "current_status": current_status.value if current_status else "unknown",
            "uptime_percentage": uptime,
            "avg_latency_ms": avg_latency,
            "error_rate": error_rate,
            "total_checks": len(results),
            "status_distribution": status_counts,
            "last_check": results[-1].timestamp.isoformat() if results else None
        }

    def export_health_data(self) -> Dict[str, Any]:
        """Export all health data."""
        return {
            url: {
                "summary": self.get_health_summary(url),
                "recent_checks": [
                    {
                        "timestamp": r.timestamp.isoformat(),
                        "status": r.status.value,
                        "latency_ms": r.latency_ms,
                        "error": r.error
                    }
                    for r in self.results[url][-10:]  # Last 10 checks
                ]
            }
            for url in self.results.keys()
        }
