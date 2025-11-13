"""
Unit tests for core RPC testing functionality.
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from rpc_tester.config import Config
from rpc_tester.core import EndpointStats, RPCTester, RpcTestResult


@pytest.fixture
def config():
    """Create a test configuration."""
    return Config(
        rpc_urls=["https://test.example.com"],
        num_requests=5,
        concurrent_requests=2,
        timeout=10.0,
        retry_attempts=2,
        test_methods=["eth_blockNumber"],
    )


@pytest.mark.asyncio
async def test_rpc_tester_initialization(config):
    """Test RPCTester initialization."""
    async with RPCTester(config) as tester:
        assert tester.config == config
        assert tester.session is not None
        assert len(tester.results) == 0


@pytest.mark.asyncio
async def test_successful_rpc_request(config):
    """Test successful RPC request."""
    async with RPCTester(config) as tester:
        # Mock successful response
        with patch.object(tester.session, "post") as mock_post:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(
                return_value={"jsonrpc": "2.0", "id": 1, "result": "0x1234567"}
            )
            mock_post.return_value.__aenter__.return_value = mock_response

            result = await tester._make_rpc_request("https://test.example.com", "eth_blockNumber")

            assert result.success is True
            assert result.error is None
            assert result.response_data == "0x1234567"
            assert result.latency_ms is not None


@pytest.mark.asyncio
async def test_failed_rpc_request(config):
    """Test failed RPC request."""
    async with RPCTester(config) as tester:
        # Mock failed response
        with patch.object(tester.session, "post") as mock_post:
            mock_response = AsyncMock()
            mock_response.status = 500
            mock_post.return_value.__aenter__.return_value = mock_response

            result = await tester._make_rpc_request("https://test.example.com", "eth_blockNumber")

            assert result.success is False
            assert result.error is not None


def test_calculate_statistics():
    """Test statistics calculation."""
    results = [
        RpcTestResult(
            url="https://test.example.com", method="eth_blockNumber", success=True, latency_ms=100.0
        ),
        RpcTestResult(
            url="https://test.example.com", method="eth_blockNumber", success=True, latency_ms=150.0
        ),
        RpcTestResult(
            url="https://test.example.com",
            method="eth_blockNumber",
            success=False,
            latency_ms=None,
            error="Timeout",
        ),
    ]

    config = Config(rpc_urls=["https://test.example.com"])
    tester = RPCTester(config)
    tester.results = results

    stats = tester.calculate_statistics("https://test.example.com", "eth_blockNumber")

    assert stats is not None
    assert stats.total_requests == 3
    assert stats.successful_requests == 2
    assert stats.failed_requests == 1
    assert stats.success_rate == pytest.approx(66.67, rel=1e-2)
    assert stats.avg_latency == 125.0
    assert stats.min_latency == 100.0
    assert stats.max_latency == 150.0


def test_percentile_calculation():
    """Test percentile calculation with linear interpolation."""
    data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    p50 = RPCTester._percentile(data, 0.50)
    p95 = RPCTester._percentile(data, 0.95)
    p99 = RPCTester._percentile(data, 0.99)

    # With linear interpolation:
    # p50: position = (10-1) * 0.50 = 4.5, interpolate between data[4]=50 and data[5]=60 -> 55.0
    # p95: position = (10-1) * 0.95 = 8.55, interpolate between data[8]=90 and data[9]=100 -> 95.5
    # p99: position = (10-1) * 0.99 = 8.91, interpolate between data[8]=90 and data[9]=100 -> 99.1
    assert p50 == 55.0
    assert p95 == pytest.approx(95.5, rel=1e-2)
    assert p99 == pytest.approx(99.1, rel=1e-2)


def test_get_params_for_method():
    """Test parameter generation for different methods."""
    config = Config(test_address="0x1234567890123456789012345678901234567890")
    tester = RPCTester(config)

    params_block = tester._get_params_for_method("eth_blockNumber")
    assert params_block == []

    params_gas = tester._get_params_for_method("eth_gasPrice")
    assert params_gas == []

    params_balance = tester._get_params_for_method("eth_getBalance")
    assert params_balance == [config.test_address, "latest"]
