#!/usr/bin/env python3
"""
Health monitoring example.

This example demonstrates continuous health monitoring of RPC endpoints.
"""

import asyncio
from datetime import timedelta
from rpc_tester.health import HealthChecker, HealthStatus


async def main():
    """Monitor endpoint health."""

    endpoints = [
        "https://eth.llamarpc.com",
        "https://rpc.ankr.com/eth",
    ]

    # Create health checker
    checker = HealthChecker(
        healthy_threshold_ms=1000.0,
        degraded_threshold_ms=3000.0,
        check_interval=10.0  # Check every 10 seconds
    )

    print("Starting health monitoring...")
    print(f"Monitoring {len(endpoints)} endpoints")
    print(f"Check interval: {checker.check_interval}s\n")

    # Perform initial health checks
    print("=== Initial Health Check ===\n")
    for url in endpoints:
        result = await checker.check_endpoint(url)

        status_emoji = {
            HealthStatus.HEALTHY: "✅",
            HealthStatus.DEGRADED: "⚠️",
            HealthStatus.UNHEALTHY: "❌",
            HealthStatus.UNKNOWN: "❓"
        }[result.status]

        print(f"{status_emoji} {url}")
        print(f"   Status: {result.status.value}")
        print(f"   Latency: {result.latency_ms:.2f}ms")
        if result.error:
            print(f"   Error: {result.error}")
        print()

    # Start continuous monitoring
    print("\n=== Starting Continuous Monitoring ===")
    print("(Monitoring for 60 seconds...)\n")

    checker.start_monitoring(endpoints)

    # Let it run for a minute
    await asyncio.sleep(60)

    # Stop monitoring
    await checker.stop_monitoring()

    # Display summary
    print("\n=== Health Summary ===\n")
    for url in endpoints:
        summary = checker.get_health_summary(url, time_window=timedelta(minutes=5))

        print(f"Endpoint: {url}")
        print(f"  Current Status: {summary['current_status']}")
        print(f"  Uptime: {summary['uptime_percentage']:.2f}%")
        print(f"  Avg Latency: {summary['avg_latency_ms']:.2f}ms")
        print(f"  Error Rate: {summary['error_rate']:.2f}%")
        print(f"  Total Checks: {summary['total_checks']}")
        print(f"  Status Distribution:")
        print(f"    Healthy: {summary['status_distribution']['healthy']}")
        print(f"    Degraded: {summary['status_distribution']['degraded']}")
        print(f"    Unhealthy: {summary['status_distribution']['unhealthy']}")
        print()


if __name__ == "__main__":
    asyncio.run(main())
