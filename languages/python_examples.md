# Python Web3 Examples

The Python RPC Tester is the original core of this repository. See [README_PYTHON_RPC_TESTER.md](../README_PYTHON_RPC_TESTER.md) for complete documentation.

## Quick Examples

### Basic RPC Testing

```python
from rpc_tester import RPCTester

tester = RPCTester('https://eth.llamarpc.com')
results = await tester.test_endpoint()
print(results)
```

### Multi-Endpoint Comparison

```python
endpoints = [
    'https://eth.llamarpc.com',
    'https://rpc.ankr.com/eth',
    'https://ethereum.publicnode.com'
]

for endpoint in endpoints:
    tester = RPCTester(endpoint)
    results = await tester.run_tests()
    print(f"{endpoint}: {results['avg_latency']}ms")
```

### Custom Configuration

```python
config = {
    'num_requests': 100,
    'concurrent': 10,
    'methods': ['eth_blockNumber', 'eth_gasPrice', 'eth_chainId'],
    'timeout': 30
}

tester = RPCTester(url, config)
results = await tester.run_tests()
```

## Features

- Async/await support
- Retry logic with exponential backoff
- Comprehensive metrics (P50, P95, P99)
- Multiple export formats (JSON, CSV, HTML)
- Beautiful CLI output with rich library

## See Also

- [Main RPC Tester README](../README_PYTHON_RPC_TESTER.md)
- [Python Package](../rpc_tester/)
- [Examples](../examples/)
