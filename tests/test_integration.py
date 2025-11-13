"""
Integration tests for RPC Tester.
"""

import asyncio
import json
import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_config(temp_dir):
    """Create sample configuration."""
    from rpc_tester.config import Config

    config = Config(
        rpc_urls=["https://eth.llamarpc.com"],
        num_requests=5,
        concurrent_requests=2,
        test_methods=["eth_blockNumber", "eth_chainId"],
        timeout=30.0,
        retry_attempts=2,
        output_dir=temp_dir,
    )
    return config


@pytest.mark.asyncio
async def test_full_test_flow(sample_config, temp_dir):
    """Test complete RPC testing flow."""
    from rpc_tester.core import RPCTester

    async with RPCTester(sample_config) as tester:
        # Run tests
        results = await tester.test_all_endpoints()

        # Verify results structure
        assert len(results) > 0
        assert "https://eth.llamarpc.com" in results

        # Verify methods were tested
        url_results = results["https://eth.llamarpc.com"]
        assert "eth_blockNumber" in url_results
        assert "eth_chainId" in url_results

        # Verify we got expected number of results
        assert len(url_results["eth_blockNumber"]) == sample_config.num_requests
        assert len(url_results["eth_chainId"]) == sample_config.num_requests


@pytest.mark.asyncio
async def test_statistics_calculation(sample_config):
    """Test statistics calculation."""
    from rpc_tester.core import RPCTester

    async with RPCTester(sample_config) as tester:
        await tester.test_all_endpoints()
        stats = tester.get_all_statistics()

        # Verify stats structure
        assert "https://eth.llamarpc.com" in stats
        url_stats = stats["https://eth.llamarpc.com"]

        # Verify method stats
        assert "eth_blockNumber" in url_stats
        block_stats = url_stats["eth_blockNumber"]

        # Verify required fields
        assert hasattr(block_stats, "total_requests")
        assert hasattr(block_stats, "successful_requests")
        assert hasattr(block_stats, "failed_requests")
        assert hasattr(block_stats, "success_rate")
        assert hasattr(block_stats, "avg_latency")
        assert hasattr(block_stats, "p95_latency")


@pytest.mark.asyncio
async def test_export_json(sample_config, temp_dir):
    """Test JSON export functionality."""
    from rpc_tester.core import RPCTester
    from rpc_tester.reporting import Reporter

    async with RPCTester(sample_config) as tester:
        await tester.test_all_endpoints()
        stats = tester.get_all_statistics()

        # Export to JSON
        reporter = Reporter(temp_dir)
        filepath = reporter.export_json(stats)

        # Verify file was created
        assert Path(filepath).exists()

        # Verify JSON content
        with open(filepath, "r") as f:
            data = json.load(f)
            assert "https://eth.llamarpc.com" in data
            assert "eth_blockNumber" in data["https://eth.llamarpc.com"]


@pytest.mark.asyncio
async def test_export_csv(sample_config, temp_dir):
    """Test CSV export functionality."""
    from rpc_tester.core import RPCTester
    from rpc_tester.reporting import Reporter

    async with RPCTester(sample_config) as tester:
        await tester.test_all_endpoints()
        stats = tester.get_all_statistics()

        # Export to CSV
        reporter = Reporter(temp_dir)
        filepath = reporter.export_csv(stats)

        # Verify file was created
        assert Path(filepath).exists()

        # Verify CSV has content
        with open(filepath, "r") as f:
            lines = f.readlines()
            assert len(lines) > 1  # Header + data rows


@pytest.mark.asyncio
async def test_export_html(sample_config, temp_dir):
    """Test HTML export functionality."""
    from rpc_tester.core import RPCTester
    from rpc_tester.reporting import Reporter

    async with RPCTester(sample_config) as tester:
        await tester.test_all_endpoints()
        stats = tester.get_all_statistics()

        # Export to HTML
        reporter = Reporter(temp_dir)
        filepath = reporter.export_html(stats)

        # Verify file was created
        assert Path(filepath).exists()

        # Verify HTML content
        with open(filepath, "r") as f:
            content = f.read()
            assert "<!DOCTYPE html>" in content
            assert "RPC Test Results" in content


@pytest.mark.asyncio
async def test_concurrent_requests(temp_dir):
    """Test concurrent request handling."""
    from rpc_tester.config import Config
    from rpc_tester.core import RPCTester

    config = Config(
        rpc_urls=["https://eth.llamarpc.com"],
        num_requests=10,
        concurrent_requests=5,
        test_methods=["eth_blockNumber"],
        timeout=30.0,
        output_dir=temp_dir,
    )

    async with RPCTester(config) as tester:
        results = await tester.test_endpoint("https://eth.llamarpc.com", "eth_blockNumber")

        # Should get all 10 results
        assert len(results) == 10


@pytest.mark.asyncio
async def test_retry_logic(temp_dir):
    """Test retry logic with invalid URL."""
    from rpc_tester.config import Config
    from rpc_tester.core import RPCTester

    config = Config(
        rpc_urls=["http://invalid-url-that-does-not-exist.local"],
        num_requests=2,
        concurrent_requests=1,
        test_methods=["eth_blockNumber"],
        timeout=5.0,
        retry_attempts=2,
        output_dir=temp_dir,
    )

    async with RPCTester(config) as tester:
        results = await tester.test_endpoint(config.rpc_urls[0], "eth_blockNumber")

        # All requests should fail
        assert all(not r.success for r in results)
        # Should have attempted retries
        assert all(r.attempt > 1 for r in results)


@pytest.mark.asyncio
async def test_cache_functionality():
    """Test caching mechanism."""
    from rpc_tester.cache import ResultCache

    cache = ResultCache(default_ttl=60)

    # Test cache miss
    result = cache.get("https://test.com", "eth_blockNumber")
    assert result is None
    assert cache.misses == 1

    # Test cache set and hit
    cache.set("https://test.com", "eth_blockNumber", {"result": "0x12345"})
    result = cache.get("https://test.com", "eth_blockNumber")
    assert result is not None
    assert result["result"] == "0x12345"
    assert cache.hits == 1

    # Test cache stats
    stats = cache.get_stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert stats["total_requests"] == 2


@pytest.mark.asyncio
async def test_metrics_collection():
    """Test metrics collection."""
    from datetime import datetime

    from rpc_tester.metrics import MetricsCollector, RequestMetrics

    collector = MetricsCollector()

    # Add some test metrics
    for i in range(10):
        metrics = RequestMetrics(
            url="https://test.com",
            method="eth_blockNumber",
            timestamp=datetime.now(),
            latency_ms=100.0 + i * 10,
            success=i < 8,  # 8 successes, 2 failures
        )
        collector.record_request(metrics)

    # Test overall summary
    summary = collector.get_overall_summary()
    assert summary["total_requests"] == 10
    assert summary["successful_requests"] == 8
    assert summary["failed_requests"] == 2
    assert summary["success_rate"] == 80.0

    # Test URL summary
    url_summary = collector.get_url_summary("https://test.com")
    assert url_summary["total_requests"] == 10


@pytest.mark.asyncio
async def test_rate_limiter():
    """Test rate limiting."""
    import time

    from rpc_tester.rate_limiter import TokenBucketRateLimiter

    limiter = TokenBucketRateLimiter(requests_per_second=5.0)

    # Acquire tokens rapidly
    start = time.time()
    for _ in range(10):
        await limiter.acquire()
    elapsed = time.time() - start

    # Should take at least 1 second to acquire 10 tokens at 5 req/s
    # (allowing some margin for timing variance)
    assert elapsed >= 0.8


@pytest.mark.asyncio
async def test_health_checker():
    """Test health checking."""
    from rpc_tester.health import HealthChecker, HealthStatus

    checker = HealthChecker(healthy_threshold_ms=1000.0, degraded_threshold_ms=3000.0)

    # Check a real endpoint
    result = await checker.check_endpoint("https://eth.llamarpc.com", "eth_blockNumber")

    # Basic assertions
    assert result.url == "https://eth.llamarpc.com"
    assert result.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNHEALTHY]
    assert result.latency_ms > 0


@pytest.mark.asyncio
async def test_config_from_file(temp_dir):
    """Test configuration file loading."""
    import yaml

    from rpc_tester.config import Config

    # Create config file
    config_data = {
        "rpc_urls": ["https://eth.llamarpc.com"],
        "num_requests": 15,
        "concurrent_requests": 7,
        "test_methods": ["eth_blockNumber", "eth_gasPrice"],
        "timeout": 45.0,
        "retry_attempts": 4,
    }

    config_path = Path(temp_dir) / "test_config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config_data, f)

    # Load config
    config = Config.from_file(str(config_path))

    # Verify loaded values
    assert config.rpc_urls == ["https://eth.llamarpc.com"]
    assert config.num_requests == 15
    assert config.concurrent_requests == 7
    assert config.test_methods == ["eth_blockNumber", "eth_gasPrice"]
    assert config.timeout == 45.0
    assert config.retry_attempts == 4


def test_prometheus_exporter():
    """Test Prometheus metrics export."""
    from rpc_tester.prometheus_exporter import PrometheusExporter

    exporter = PrometheusExporter(job_name="test_job")

    # Add various metrics
    exporter.add_gauge("test_gauge", 42.5, {"label": "value"}, "Test gauge metric")
    exporter.add_counter("test_counter", 100, {"label": "value"}, "Test counter metric")
    exporter.add_histogram(
        "test_histogram", [10, 20, 30, 40, 50], {"label": "value"}, "Test histogram"
    )

    # Export to string
    output = exporter.to_string()

    # Verify output format
    assert "test_gauge" in output
    assert "test_counter" in output
    assert "test_histogram" in output
    assert "# HELP" in output
    assert "# TYPE" in output
