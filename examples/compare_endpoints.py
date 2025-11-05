#!/usr/bin/env python3
"""
Compare multiple RPC endpoints example.

This example shows how to compare performance of multiple RPC providers.
"""

import asyncio
from rpc_tester.config import Config
from rpc_tester.core import RPCTester
from rpc_tester.reporting import Reporter


async def main():
    """Compare multiple RPC endpoints."""

    # List of endpoints to compare
    endpoints = [
        "https://eth.llamarpc.com",
        "https://rpc.ankr.com/eth",
        "https://ethereum.publicnode.com",
    ]

    config = Config(
        rpc_urls=endpoints,
        num_requests=20,
        concurrent_requests=5,
        test_methods=["eth_blockNumber", "eth_chainId", "eth_gasPrice"],
        timeout=30.0,
        retry_attempts=3,
        export_json=True,
        export_csv=True,
        export_html=True,
        output_dir="comparison_results"
    )

    print(f"Comparing {len(endpoints)} RPC endpoints")
    print(f"Testing {len(config.test_methods)} methods with {config.num_requests} requests each\n")

    async with RPCTester(config) as tester:
        await tester.test_all_endpoints()
        stats = tester.get_all_statistics()

        # Find best performer for each method
        print("\n=== Performance Comparison ===\n")

        all_methods = set()
        for methods in stats.values():
            all_methods.update(methods.keys())

        for method in sorted(all_methods):
            print(f"\nMethod: {method}")
            print("-" * 60)

            method_stats = []
            for url in endpoints:
                if method in stats[url]:
                    stat = stats[url][method]
                    method_stats.append({
                        'url': url,
                        'latency': stat.avg_latency,
                        'success_rate': stat.success_rate
                    })

            # Sort by latency
            method_stats.sort(key=lambda x: x['latency'])

            for i, stat in enumerate(method_stats, 1):
                marker = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
                print(f"{marker} {stat['url']}")
                print(f"   Latency: {stat['latency']:.2f}ms | Success: {stat['success_rate']:.1f}%")

        # Export results
        reporter = Reporter(config.output_dir)

        if config.export_json:
            json_file = reporter.export_json(stats)
            print(f"\n✓ JSON report: {json_file}")

        if config.export_csv:
            csv_file = reporter.export_csv(stats)
            print(f"✓ CSV report: {csv_file}")

        if config.export_html:
            html_file = reporter.export_html(stats)
            print(f"✓ HTML report: {html_file}")


if __name__ == "__main__":
    asyncio.run(main())
