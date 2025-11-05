#!/usr/bin/env python3
"""
Basic usage example for RPC Tester.

This example shows how to test a single RPC endpoint with basic configuration.
"""

import asyncio
from rpc_tester.config import Config
from rpc_tester.core import RPCTester


async def main():
    """Run basic RPC test."""

    # Create configuration
    config = Config(
        rpc_urls=["https://eth.llamarpc.com"],
        num_requests=10,
        concurrent_requests=3,
        test_methods=["eth_blockNumber", "eth_chainId", "eth_gasPrice"],
        timeout=30.0,
        retry_attempts=3
    )

    print("Testing RPC endpoint: https://eth.llamarpc.com")
    print(f"Requests: {config.num_requests}")
    print(f"Methods: {', '.join(config.test_methods)}\n")

    # Run tests
    async with RPCTester(config) as tester:
        await tester.test_all_endpoints()
        stats = tester.get_all_statistics()

        # Display results
        for url, methods in stats.items():
            print(f"\n=== Results for {url} ===\n")

            for method, stat in methods.items():
                print(f"Method: {method}")
                print(f"  Total Requests: {stat.total_requests}")
                print(f"  Successful: {stat.successful_requests}")
                print(f"  Failed: {stat.failed_requests}")
                print(f"  Success Rate: {stat.success_rate:.2f}%")
                print(f"  Avg Latency: {stat.avg_latency:.2f}ms")
                print(f"  P95 Latency: {stat.p95_latency:.2f}ms")
                print()


if __name__ == "__main__":
    asyncio.run(main())
