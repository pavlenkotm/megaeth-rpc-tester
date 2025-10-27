import asyncio
import aiohttp
import time
import argparse

async def test_rpc(url):
    async with aiohttp.ClientSession() as session:
        start = time.perf_counter()
        try:
            async with session.post(url, json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "eth_blockNumber",
                "params": []
            }) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    latency = (time.perf_counter() - start) * 1000
                    block_hex = data.get("result")
                    block = int(block_hex, 16) if isinstance(block_hex, str) else None
                    print(f"✅ {url} — OK ({latency:.1f} ms, block {block})")
                else:
                    print(f"⚠️ {url} — HTTP {resp.status}")
        except Exception as e:
            print(f"❌ {url} — error: {e}")

async def main():
    parser = argparse.ArgumentParser(description="MegaETH RPC Speed Tester")
    parser.add_argument("urls", nargs="+", help="RPC URLs to test")
    args = parser.parse_args()
    await asyncio.gather(*(test_rpc(u) for u in args.urls))

if __name__ == "__main__":
    asyncio.run(main())
