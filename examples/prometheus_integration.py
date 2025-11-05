#!/usr/bin/env python3
"""
Prometheus integration example.

This example shows how to export metrics in Prometheus format.
"""

import asyncio
from datetime import datetime
from rpc_tester.config import Config
from rpc_tester.core import RPCTester
from rpc_tester.prometheus_exporter import PrometheusExporter, PrometheusPushGateway


async def main():
    """Export metrics to Prometheus format."""

    # Run tests
    config = Config(
        rpc_urls=["https://eth.llamarpc.com"],
        num_requests=20,
        concurrent_requests=5,
        test_methods=["eth_blockNumber", "eth_chainId"],
        timeout=30.0
    )

    print("Running RPC tests...")
    async with RPCTester(config) as tester:
        await tester.test_all_endpoints()
        stats = tester.get_all_statistics()

    # Create Prometheus exporter
    exporter = PrometheusExporter(job_name="rpc_tester")

    print("\nExporting metrics to Prometheus format...")
    exporter.export_rpc_stats(stats, timestamp=datetime.now())

    # Save to file
    metrics_file = "metrics.prom"
    exporter.save_to_file(metrics_file)
    print(f"✓ Metrics saved to: {metrics_file}")

    # Display metrics
    print("\n=== Prometheus Metrics ===\n")
    print(exporter.to_string())

    # Optional: Push to Pushgateway
    # Uncomment if you have a Pushgateway running
    """
    pushgateway = PrometheusPushGateway(
        gateway_url="http://localhost:9091",
        job_name="rpc_tester"
    )

    success = await pushgateway.push_metrics(
        exporter,
        grouping_key={"instance": "test-instance"}
    )

    if success:
        print("\n✓ Metrics pushed to Pushgateway")
    else:
        print("\n✗ Failed to push metrics to Pushgateway")
    """

    print("\nMetrics can be scraped by Prometheus or pushed to Pushgateway")
    print("Configure your prometheus.yml to scrape this file or push endpoint")


if __name__ == "__main__":
    asyncio.run(main())
