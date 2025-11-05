#!/usr/bin/env python3
"""
Example using caching to improve performance.

This example demonstrates how to use result caching to avoid redundant requests.
"""

import asyncio
from rpc_tester.cache import ResultCache, PersistentCache


async def main():
    """Demonstrate caching functionality."""

    # Create in-memory cache
    print("=== In-Memory Cache Example ===\n")
    cache = ResultCache(default_ttl=3600)  # 1 hour TTL

    # Simulate cache operations
    url = "https://eth.llamarpc.com"
    method = "eth_blockNumber"

    # First request - cache miss
    result = cache.get(url, method)
    print(f"First request: {result}")
    print(f"Cache stats: {cache.get_stats()}")

    # Store result
    cache.set(url, method, {"result": "0x12345"})
    print("\nStored result in cache")

    # Second request - cache hit
    result = cache.get(url, method)
    print(f"Second request: {result}")
    print(f"Cache stats: {cache.get_stats()}")

    # Persistent cache example
    print("\n\n=== Persistent Cache Example ===\n")
    persistent_cache = PersistentCache(
        cache_dir=".cache",
        default_ttl=3600
    )

    # Store multiple results
    persistent_cache.set("https://eth.llamarpc.com", "eth_chainId", {"result": "0x1"})
    persistent_cache.set("https://eth.llamarpc.com", "eth_gasPrice", {"result": "0x3b9aca00"})
    persistent_cache.set("https://rpc.ankr.com/eth", "eth_blockNumber", {"result": "0x12346"})

    print("Stored 3 results in persistent cache")
    print(f"Cache stats: {persistent_cache.get_stats()}")

    # Retrieve results
    chain_id = persistent_cache.get("https://eth.llamarpc.com", "eth_chainId")
    gas_price = persistent_cache.get("https://eth.llamarpc.com", "eth_gasPrice")
    block_num = persistent_cache.get("https://rpc.ankr.com/eth", "eth_blockNumber")

    print(f"\nRetrieved results:")
    print(f"  Chain ID: {chain_id}")
    print(f"  Gas Price: {gas_price}")
    print(f"  Block Number: {block_num}")

    print("\nCache is persisted to disk and will survive restarts!")


if __name__ == "__main__":
    asyncio.run(main())
