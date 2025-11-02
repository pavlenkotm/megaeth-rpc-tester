"""
Core RPC testing functionality.
"""

import asyncio
import aiohttp
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import statistics
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """Result of a single RPC test."""

    url: str
    method: str
    success: bool
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    response_data: Optional[Any] = None
    timestamp: datetime = field(default_factory=datetime.now)
    status_code: Optional[int] = None
    attempt: int = 1


@dataclass
class EndpointStats:
    """Statistics for an RPC endpoint."""

    url: str
    method: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    success_rate: float
    latencies: List[float]
    avg_latency: float
    min_latency: float
    max_latency: float
    p50_latency: float
    p95_latency: float
    p99_latency: float
    errors: List[str]


class RPCTester:
    """Advanced RPC endpoint tester."""

    def __init__(self, config):
        """Initialize the RPC tester."""
        self.config = config
        self.results: List[TestResult] = []
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry."""
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def _make_rpc_request(
        self,
        url: str,
        method: str,
        params: Optional[List[Any]] = None,
        attempt: int = 1
    ) -> TestResult:
        """Make a single RPC request with retry logic."""

        if params is None:
            params = []

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }

        start_time = time.perf_counter()
        error = None
        response_data = None
        status_code = None
        success = False

        for retry in range(self.config.retry_attempts):
            try:
                async with self.session.post(url, json=payload) as resp:
                    status_code = resp.status
                    if resp.status == 200:
                        data = await resp.json()
                        latency = (time.perf_counter() - start_time) * 1000

                        if "error" in data:
                            error = str(data["error"])
                            success = False
                        else:
                            response_data = data.get("result")
                            success = True

                        return TestResult(
                            url=url,
                            method=method,
                            success=success,
                            latency_ms=latency,
                            error=error,
                            response_data=response_data,
                            status_code=status_code,
                            attempt=retry + 1
                        )
                    else:
                        error = f"HTTP {resp.status}"
                        # Retry on server errors
                        if resp.status >= 500 and retry < self.config.retry_attempts - 1:
                            await asyncio.sleep(self.config.retry_delay * (2 ** retry))
                            continue
                        else:
                            break

            except asyncio.TimeoutError:
                error = "Timeout"
                if retry < self.config.retry_attempts - 1:
                    await asyncio.sleep(self.config.retry_delay * (2 ** retry))
                    continue
                else:
                    break

            except Exception as e:
                error = str(e)
                if retry < self.config.retry_attempts - 1:
                    await asyncio.sleep(self.config.retry_delay * (2 ** retry))
                    continue
                else:
                    break

        latency = (time.perf_counter() - start_time) * 1000
        return TestResult(
            url=url,
            method=method,
            success=False,
            latency_ms=latency,
            error=error,
            status_code=status_code,
            attempt=self.config.retry_attempts
        )

    async def test_endpoint(
        self,
        url: str,
        method: str,
        params: Optional[List[Any]] = None
    ) -> List[TestResult]:
        """Test an endpoint with multiple requests."""

        tasks = []
        for i in range(self.config.num_requests):
            # Control concurrency
            if i > 0 and i % self.config.concurrent_requests == 0:
                # Wait for the previous batch to complete
                batch_results = await asyncio.gather(*tasks)
                self.results.extend(batch_results)
                tasks = []

            task = self._make_rpc_request(url, method, params)
            tasks.append(task)

        # Complete remaining tasks
        if tasks:
            batch_results = await asyncio.gather(*tasks)
            self.results.extend(batch_results)

        return [r for r in self.results if r.url == url and r.method == method]

    async def test_all_endpoints(self) -> Dict[str, Dict[str, List[TestResult]]]:
        """Test all configured endpoints with all methods."""

        results_by_endpoint = {}

        for url in self.config.rpc_urls:
            results_by_endpoint[url] = {}

            for method in self.config.test_methods:
                params = self._get_params_for_method(method)
                endpoint_results = await self.test_endpoint(url, method, params)
                results_by_endpoint[url][method] = endpoint_results

        return results_by_endpoint

    def _get_params_for_method(self, method: str) -> Optional[List[Any]]:
        """Get appropriate parameters for RPC method."""

        if method == "eth_blockNumber":
            return []
        elif method == "eth_chainId":
            return []
        elif method == "eth_gasPrice":
            return []
        elif method == "net_version":
            return []
        elif method == "eth_getBalance" and self.config.test_address:
            return [self.config.test_address, "latest"]
        elif method == "eth_call" and self.config.test_eth_call:
            # Simple eth_call example
            return [{"to": "0x0000000000000000000000000000000000000000", "data": "0x"}, "latest"]
        elif method == "eth_getLogs" and self.config.test_eth_getLogs:
            # Get logs from recent blocks
            return [{"fromBlock": "latest", "toBlock": "latest"}]
        else:
            return []

    def calculate_statistics(
        self,
        url: str,
        method: str
    ) -> Optional[EndpointStats]:
        """Calculate statistics for an endpoint/method combination."""

        endpoint_results = [
            r for r in self.results
            if r.url == url and r.method == method
        ]

        if not endpoint_results:
            return None

        successful = [r for r in endpoint_results if r.success]
        failed = [r for r in endpoint_results if not r.success]

        latencies = [r.latency_ms for r in successful if r.latency_ms is not None]

        if not latencies:
            return EndpointStats(
                url=url,
                method=method,
                total_requests=len(endpoint_results),
                successful_requests=0,
                failed_requests=len(failed),
                success_rate=0.0,
                latencies=[],
                avg_latency=0.0,
                min_latency=0.0,
                max_latency=0.0,
                p50_latency=0.0,
                p95_latency=0.0,
                p99_latency=0.0,
                errors=[r.error for r in failed if r.error]
            )

        return EndpointStats(
            url=url,
            method=method,
            total_requests=len(endpoint_results),
            successful_requests=len(successful),
            failed_requests=len(failed),
            success_rate=len(successful) / len(endpoint_results) * 100,
            latencies=latencies,
            avg_latency=statistics.mean(latencies),
            min_latency=min(latencies),
            max_latency=max(latencies),
            p50_latency=statistics.median(latencies),
            p95_latency=self._percentile(latencies, 0.95),
            p99_latency=self._percentile(latencies, 0.99),
            errors=[r.error for r in failed if r.error]
        )

    @staticmethod
    def _percentile(data: List[float], percentile: float) -> float:
        """Calculate percentile using linear interpolation."""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        n = len(sorted_data)

        # Using the same method as numpy's percentile with linear interpolation
        # Position in array (0-indexed)
        pos = (n - 1) * percentile
        floor_pos = int(pos)
        ceil_pos = min(floor_pos + 1, n - 1)

        # Linear interpolation between floor and ceiling positions
        if floor_pos == ceil_pos:
            return sorted_data[floor_pos]

        weight = pos - floor_pos
        return sorted_data[floor_pos] * (1 - weight) + sorted_data[ceil_pos] * weight

    def get_all_statistics(self) -> Dict[str, Dict[str, EndpointStats]]:
        """Get statistics for all endpoints and methods."""

        stats = {}
        for url in self.config.rpc_urls:
            stats[url] = {}
            for method in self.config.test_methods:
                endpoint_stats = self.calculate_statistics(url, method)
                if endpoint_stats:
                    stats[url][method] = endpoint_stats

        return stats
