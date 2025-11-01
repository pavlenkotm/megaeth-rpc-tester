"""
Core RPC testing functionality.
"""

import asyncio
import aiohttp
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from .logger import get_logger
from .exceptions import (
    RPCTesterError,
    ConnectionError as RPCConnectionError,
    TimeoutError as RPCTimeoutError,
    InvalidResponseError
)
from .utils import calculate_percentile, calculate_statistics

logger = get_logger(__name__)


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
    """Advanced RPC endpoint tester with improved error handling and performance."""

    def __init__(self, config):
        """
        Initialize the RPC tester.

        Args:
            config: Configuration object with test parameters
        """
        self.config = config
        self.results: List[TestResult] = []
        self.session: Optional[aiohttp.ClientSession] = None
        self._request_id = 0

    async def __aenter__(self):
        """Async context manager entry."""
        # Configure connection pooling and timeouts
        timeout = aiohttp.ClientTimeout(
            total=self.config.timeout,
            connect=min(10, self.config.timeout / 3),
            sock_read=self.config.timeout
        )

        # Configure TCP connector for better performance
        connector = aiohttp.TCPConnector(
            limit=self.config.concurrent_requests * 2,
            limit_per_host=self.config.concurrent_requests,
            ttl_dns_cache=300,
            enable_cleanup_closed=True
        )

        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={'Content-Type': 'application/json'}
        )

        logger.info(f"Initialized RPC tester with {self.config.concurrent_requests} concurrent requests")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
            logger.info("Closed RPC tester session")

    def _get_next_request_id(self) -> int:
        """Get next request ID."""
        self._request_id += 1
        return self._request_id

    async def _make_rpc_request(
        self,
        url: str,
        method: str,
        params: Optional[List[Any]] = None,
        attempt: int = 1
    ) -> TestResult:
        """
        Make a single RPC request with improved retry logic and error handling.

        Args:
            url: RPC endpoint URL
            method: RPC method name
            params: Method parameters
            attempt: Current attempt number

        Returns:
            TestResult with request outcome
        """
        if params is None:
            params = []

        payload = {
            "jsonrpc": "2.0",
            "id": self._get_next_request_id(),
            "method": method,
            "params": params
        }

        start_time = time.perf_counter()
        error = None
        response_data = None
        status_code = None
        success = False
        last_exception = None

        for retry in range(self.config.retry_attempts):
            try:
                async with self.session.post(url, json=payload) as resp:
                    latency = (time.perf_counter() - start_time) * 1000
                    status_code = resp.status

                    if resp.status == 200:
                        try:
                            data = await resp.json()
                        except Exception as json_error:
                            error = f"Invalid JSON response: {str(json_error)}"
                            logger.warning(f"JSON parsing error for {url}/{method}: {error}")
                            raise InvalidResponseError(error)

                        if "error" in data:
                            error = str(data["error"])
                            success = False
                            logger.debug(f"RPC error for {url}/{method}: {error}")
                        else:
                            response_data = data.get("result")
                            success = True
                            logger.debug(f"Successful request to {url}/{method} in {latency:.2f}ms")

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
                        # Try to get error message from response
                        try:
                            error_text = await resp.text()
                            if error_text:
                                error += f": {error_text[:100]}"
                        except Exception:
                            pass

                        logger.warning(f"HTTP error {resp.status} for {url}/{method}")

                        # Retry on server errors
                        if resp.status >= 500 and retry < self.config.retry_attempts - 1:
                            retry_delay = self.config.retry_delay * (2 ** retry)
                            logger.info(f"Retrying {url}/{method} after {retry_delay}s (attempt {retry + 1})")
                            await asyncio.sleep(retry_delay)
                            start_time = time.perf_counter()  # Reset timer for retry
                            continue
                        else:
                            break

            except asyncio.TimeoutError as e:
                last_exception = e
                error = f"Request timeout after {self.config.timeout}s"
                logger.warning(f"Timeout for {url}/{method}")

                if retry < self.config.retry_attempts - 1:
                    retry_delay = self.config.retry_delay * (2 ** retry)
                    logger.info(f"Retrying {url}/{method} after {retry_delay}s")
                    await asyncio.sleep(retry_delay)
                    start_time = time.perf_counter()
                    continue
                else:
                    break

            except aiohttp.ClientError as e:
                last_exception = e
                error = f"Connection error: {str(e)}"
                logger.warning(f"Connection error for {url}/{method}: {error}")

                if retry < self.config.retry_attempts - 1:
                    retry_delay = self.config.retry_delay * (2 ** retry)
                    await asyncio.sleep(retry_delay)
                    start_time = time.perf_counter()
                    continue
                else:
                    break

            except Exception as e:
                last_exception = e
                error = f"Unexpected error: {type(e).__name__}: {str(e)}"
                logger.error(f"Unexpected error for {url}/{method}: {error}")

                if retry < self.config.retry_attempts - 1:
                    retry_delay = self.config.retry_delay * (2 ** retry)
                    await asyncio.sleep(retry_delay)
                    start_time = time.perf_counter()
                    continue
                else:
                    break

        # All retries failed
        latency = (time.perf_counter() - start_time) * 1000
        logger.error(f"All {self.config.retry_attempts} attempts failed for {url}/{method}: {error}")

        return TestResult(
            url=url,
            method=method,
            success=False,
            latency_ms=latency,
            error=error or "Unknown error",
            status_code=status_code,
            attempt=self.config.retry_attempts
        )

    async def test_endpoint(
        self,
        url: str,
        method: str,
        params: Optional[List[Any]] = None
    ) -> List[TestResult]:
        """
        Test an endpoint with multiple requests using controlled concurrency.

        Args:
            url: RPC endpoint URL
            method: RPC method name
            params: Method parameters

        Returns:
            List of test results
        """
        logger.info(f"Testing {url}/{method} with {self.config.num_requests} requests")

        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(self.config.concurrent_requests)

        async def rate_limited_request():
            """Execute request with rate limiting."""
            async with semaphore:
                return await self._make_rpc_request(url, method, params)

        # Create all tasks
        tasks = [rate_limited_request() for _ in range(self.config.num_requests)]

        # Execute all tasks concurrently with rate limiting
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results and handle exceptions
        for result in batch_results:
            if isinstance(result, Exception):
                logger.error(f"Task exception for {url}/{method}: {result}")
                # Create failed result for exception
                self.results.append(TestResult(
                    url=url,
                    method=method,
                    success=False,
                    latency_ms=0,
                    error=f"Task exception: {str(result)}",
                    status_code=None,
                    attempt=1
                ))
            else:
                self.results.append(result)

        endpoint_results = [r for r in self.results if r.url == url and r.method == method]
        logger.info(f"Completed testing {url}/{method}: {len(endpoint_results)} results")

        return endpoint_results

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
        """
        Calculate comprehensive statistics for an endpoint/method combination.

        Args:
            url: RPC endpoint URL
            method: RPC method name

        Returns:
            EndpointStats with calculated statistics or None if no results
        """
        endpoint_results = [
            r for r in self.results
            if r.url == url and r.method == method
        ]

        if not endpoint_results:
            logger.warning(f"No results found for {url}/{method}")
            return None

        successful = [r for r in endpoint_results if r.success]
        failed = [r for r in endpoint_results if not r.success]

        latencies = [r.latency_ms for r in successful if r.latency_ms is not None]

        if not latencies:
            logger.info(f"No successful requests for {url}/{method}")
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

        # Calculate statistics using utility function
        stats_dict = calculate_statistics(latencies)

        logger.info(f"Statistics for {url}/{method}: success_rate={len(successful) / len(endpoint_results) * 100:.1f}%, avg={stats_dict['mean']:.2f}ms")

        return EndpointStats(
            url=url,
            method=method,
            total_requests=len(endpoint_results),
            successful_requests=len(successful),
            failed_requests=len(failed),
            success_rate=len(successful) / len(endpoint_results) * 100,
            latencies=latencies,
            avg_latency=stats_dict['mean'],
            min_latency=stats_dict['min'],
            max_latency=stats_dict['max'],
            p50_latency=stats_dict['p50'],
            p95_latency=stats_dict['p95'],
            p99_latency=stats_dict['p99'],
            errors=[r.error for r in failed if r.error]
        )

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
