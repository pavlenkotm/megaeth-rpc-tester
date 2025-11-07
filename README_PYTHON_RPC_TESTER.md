# ⚡ MegaETH RPC Tester

**Advanced async CLI tool for testing speed, reliability, and performance of Ethereum RPC endpoints.**

Perfect for benchmarking MegaETH, Alchemy, Ankr, Infura, or any EVM-compatible RPC node with comprehensive metrics, beautiful CLI output, and detailed reporting.

## ✨ Features

### 🚀 Core Capabilities
- **Multi-endpoint testing** - Test multiple RPC endpoints simultaneously
- **Multiple RPC methods** - Test various JSON-RPC methods (eth_blockNumber, eth_gasPrice, eth_chainId, etc.)
- **Advanced benchmarking** - Get detailed performance statistics including percentiles (P50, P95, P99)
- **Retry logic** - Automatic retry with exponential backoff for failed requests
- **Concurrent testing** - Control the number of parallel requests
- **Comparison mode** - Compare multiple endpoints side-by-side

### 📊 Reporting & Export
- **Rich CLI output** - Beautiful terminal interface with colors and progress bars
- **JSON export** - Machine-readable test results
- **CSV export** - Spreadsheet-compatible format
- **HTML reports** - Styled web-based reports with charts and tables
- **Detailed statistics** - Min, max, average, median, P95, P99 latencies

### ⚙️ Configuration
- **CLI arguments** - Quick testing with command-line options
- **Config files** - YAML/JSON configuration for complex test scenarios
- **Flexible parameters** - Customize timeouts, retries, concurrency, and more

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/pavlenkotm/megaeth-rpc-tester
cd megaeth-rpc-tester

# Install dependencies
python -m pip install -r requirements.txt
```

### Basic Usage

```bash
# Test a single RPC endpoint
python -m rpc_tester https://eth.llamarpc.com

# Test multiple endpoints
python -m rpc_tester https://eth.llamarpc.com https://rpc.ankr.com/eth

# Test with custom number of requests
python -m rpc_tester https://eth.llamarpc.com -n 50

# Test specific methods
python -m rpc_tester https://eth.llamarpc.com -m eth_blockNumber eth_gasPrice eth_chainId
```

### Advanced Usage

```bash
# Export results to multiple formats
python -m rpc_tester https://eth.llamarpc.com --json --csv --html

# Use configuration file
python -m rpc_tester --config config.yaml

# Generate example configuration
python -m rpc_tester --generate-config my_config.yaml

# Adjust concurrency and retries
python -m rpc_tester https://eth.llamarpc.com --concurrent 10 --retry 5

# Verbose output with detailed errors
python -m rpc_tester https://eth.llamarpc.com -v
```

---

## 📖 Documentation

### Command-Line Options

```
positional arguments:
  urls                  RPC URLs to test

options:
  -h, --help            Show help message and exit
  -c, --config FILE     Path to configuration file (YAML or JSON)
  -n, --num-requests N  Number of requests per endpoint (default: 10)
  --concurrent N        Number of concurrent requests (default: 5)
  -m, --methods M [M ...]
                        RPC methods to test (default: eth_blockNumber eth_chainId eth_gasPrice)
  --timeout SECONDS     Request timeout in seconds (default: 30)
  --retry N             Number of retry attempts (default: 3)
  --json                Export results to JSON
  --csv                 Export results to CSV
  --html                Export results to HTML
  -o, --output-dir DIR  Output directory for reports (default: results)
  -v, --verbose         Verbose output
  -q, --quiet           Quiet mode (minimal output)
  --generate-config FILE
                        Generate example configuration file and exit
```

### Configuration File

Create a `config.yaml` file:

```yaml
# RPC endpoints to test
rpc_urls:
  - https://eth.llamarpc.com
  - https://rpc.ankr.com/eth
  - https://ethereum.publicnode.com

# Test parameters
num_requests: 20
concurrent_requests: 5
timeout: 30.0
retry_attempts: 3
retry_delay: 1.0

# RPC methods to test
test_methods:
  - eth_blockNumber
  - eth_chainId
  - eth_gasPrice
  - net_version

# Output options
export_json: true
export_csv: true
export_html: true
output_dir: results

# Display options
verbose: false
quiet: false
show_percentiles: true
```

Then run:

```bash
python -m rpc_tester --config config.yaml
```

### Supported RPC Methods

The tester supports all standard Ethereum JSON-RPC methods:

| Method | Description | Parameters Required |
|--------|-------------|---------------------|
| `eth_blockNumber` | Get latest block number | None |
| `eth_chainId` | Get chain ID | None |
| `eth_gasPrice` | Get current gas price | None |
| `net_version` | Get network ID | None |
| `eth_getBalance` | Get account balance | Address (via config) |
| `eth_call` | Execute call | Optional (via config) |
| `eth_getLogs` | Get event logs | Optional (via config) |

---

## 📊 Output Examples

### Terminal Output

```
⚡ MegaETH RPC Tester

Testing 2 endpoint(s) with 3 method(s)
Requests per test: 20 | Concurrent: 5

Running RPC tests... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

================================================================================
📊 Test Results
================================================================================

🔗 https://eth.llamarpc.com

┌────────────────────┬──────────┬──────────────┬─────────────┬──────────┬──────────┬──────────┐
│ Method             │ Requests │ Success Rate │ Avg Latency │ P50      │ P95      │ P99      │
├────────────────────┼──────────┼──────────────┼─────────────┼──────────┼──────────┼──────────┤
│ eth_blockNumber    │ 20       │ 100.0%       │ 145.23ms    │ 142.1ms  │ 189.5ms  │ 205.3ms  │
│ eth_chainId        │ 20       │ 100.0%       │ 138.45ms    │ 135.8ms  │ 175.2ms  │ 192.1ms  │
│ eth_gasPrice       │ 20       │ 100.0%       │ 152.67ms    │ 149.3ms  │ 198.7ms  │ 215.8ms  │
└────────────────────┴──────────┴──────────────┴─────────────┴──────────┴──────────┴──────────┘
```

### JSON Export

```json
{
  "https://eth.llamarpc.com": {
    "eth_blockNumber": {
      "total_requests": 20,
      "successful_requests": 20,
      "failed_requests": 0,
      "success_rate": 100.0,
      "avg_latency_ms": 145.23,
      "min_latency_ms": 98.45,
      "max_latency_ms": 205.32,
      "p50_latency_ms": 142.10,
      "p95_latency_ms": 189.50,
      "p99_latency_ms": 205.30
    }
  }
}
```

---

## 🏗️ Project Structure

```
megaeth-rpc-tester/
├── rpc_tester/
│   ├── __init__.py       # Package initialization
│   ├── __main__.py       # Entry point
│   ├── cli.py            # CLI interface with rich output
│   ├── core.py           # Core testing logic
│   ├── config.py         # Configuration management
│   └── reporting.py      # Results export (JSON, CSV, HTML)
├── example_config.yaml   # Example configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

---

## 🎯 Use Cases

### 1. Compare Multiple RPC Providers

Test different providers to find the fastest and most reliable:

```bash
python -m rpc_tester \
  https://eth.llamarpc.com \
  https://rpc.ankr.com/eth \
  https://ethereum.publicnode.com \
  https://cloudflare-eth.com \
  -n 50 --html
```

### 2. Monitor RPC Endpoint Health

Regular health checks with detailed metrics:

```bash
python -m rpc_tester https://your-rpc-endpoint.com \
  -n 100 \
  --concurrent 10 \
  --json \
  -o monitoring/
```

### 3. Load Testing

Test endpoint performance under load:

```bash
python -m rpc_tester https://your-rpc-endpoint.com \
  -n 1000 \
  --concurrent 50 \
  --timeout 60 \
  -v
```

### 4. Method-Specific Testing

Test specific RPC methods for your application:

```bash
python -m rpc_tester https://eth.llamarpc.com \
  -m eth_getBalance eth_call eth_estimateGas \
  -n 30
```

---

## 🔧 Development

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run with coverage
pytest --cov=rpc_tester
```

### Type Checking

```bash
mypy rpc_tester/
```

---

## 📝 Examples

### Example 1: Quick Performance Check

```bash
python -m rpc_tester https://eth.llamarpc.com -n 20
```

### Example 2: Comprehensive Benchmarking

```bash
python -m rpc_tester \
  https://eth.llamarpc.com \
  https://rpc.ankr.com/eth \
  -n 100 \
  --concurrent 20 \
  --json --csv --html \
  -v
```

### Example 3: Using Configuration File

Create `my_test.yaml`:

```yaml
rpc_urls:
  - https://eth.llamarpc.com
  - https://rpc.ankr.com/eth

num_requests: 50
concurrent_requests: 10
test_methods:
  - eth_blockNumber
  - eth_gasPrice
  - eth_chainId

export_json: true
export_html: true
verbose: true
```

Run:

```bash
python -m rpc_tester --config my_test.yaml
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built for testing MegaETH and other Ethereum RPC endpoints
- Uses `aiohttp` for async HTTP requests
- Uses `rich` for beautiful CLI output

---

## 🔗 Links

- **GitHub**: https://github.com/pavlenkotm/megaeth-rpc-tester
- **Issues**: https://github.com/pavlenkotm/megaeth-rpc-tester/issues

---

Made with ⚡ for the Ethereum community
