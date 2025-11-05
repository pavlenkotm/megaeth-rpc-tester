# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] - 2024-11-05

### Added

#### New Core Features
- **WebSocket Support**: Full WebSocket RPC testing with subscriptions and real-time notifications
- **Result Caching**: In-memory and persistent disk-based caching mechanisms
- **Advanced Metrics**: Comprehensive metrics collection, aggregation, and time-series tracking
- **Rate Limiting**: Multiple algorithms (token bucket, sliding window, adaptive)
- **Health Monitoring**: Continuous endpoint health checking with uptime tracking
- **Prometheus Integration**: Export metrics in Prometheus format with Pushgateway support
- **Structured Logging**: JSON and colored console logging with log levels
- **Configuration Validation**: Comprehensive input and data validation

#### New Export Formats
- **Markdown Export**: GitHub-flavored Markdown reports with tables and emojis
- **Prometheus Metrics**: Gauges, counters, and histograms for monitoring

#### New Modules (9 total)
- `rpc_tester/exceptions.py`: Custom exception hierarchy
- `rpc_tester/cache.py`: Caching mechanisms (in-memory and persistent)
- `rpc_tester/metrics.py`: Advanced metrics tracking
- `rpc_tester/logger.py`: Structured logging system
- `rpc_tester/validators.py`: Configuration and data validation
- `rpc_tester/websocket.py`: WebSocket RPC client
- `rpc_tester/rate_limiter.py`: Rate limiting implementations
- `rpc_tester/health.py`: Health monitoring system
- `rpc_tester/prometheus_exporter.py`: Prometheus metrics export

#### Infrastructure & DevOps
- **Docker Support**: Multi-stage Dockerfile and docker-compose.yml
- **GitHub Actions**: CI/CD workflows for testing, linting, and releases
- **Makefile**: Development automation with 30+ commands
- **Security Scanning**: Integrated bandit and safety checks
- **Multi-Python Testing**: Test matrix for Python 3.9-3.12

#### Documentation & Examples
- **5 Complete Examples**: Basic usage, comparison, caching, health monitoring, Prometheus
- **CONTRIBUTING.md**: Comprehensive contributor guidelines
- **Enhanced README**: Detailed documentation with all new features

### Enhanced

#### Extended RPC Method Support
Added 10+ new methods:
- `eth_getBlockByNumber`
- `eth_getTransactionCount`
- `eth_estimateGas`
- `eth_getBlockTransactionCountByNumber`
- `eth_syncing`
- `eth_mining`
- `eth_hashrate`
- `eth_accounts`
- `web3_clientVersion`

#### CLI Enhancements
New command-line options:
- `--markdown`: Export to Markdown
- `--prometheus`: Export Prometheus metrics
- `--cache`: Enable caching
- `--cache-ttl`: Configure cache TTL
- `--rate-limit`: Set request rate limit
- `--version`: Display version

#### Dependencies
- Added `websockets>=12.0` for WebSocket support
- Added `pandas>=2.0.0` for advanced analytics
- Added `diskcache>=5.6.3` for persistent caching
- Added `prometheus-client>=0.19.0` for metrics
- Added development tools (black, isort, flake8, bandit)

### Testing
- **Integration Test Suite**: 13 comprehensive integration tests
- **Coverage Reports**: HTML and XML coverage reporting
- **Async Testing**: Full pytest-asyncio support
- **Docker Testing**: Automated Docker image testing

## [2.0.0] - 2024

### Major Improvements

This release represents a complete rewrite of the RPC tester with extensive new features and improvements.

### Added

#### Core Features
- **Multiple RPC Method Testing**: Support for testing various JSON-RPC methods (eth_blockNumber, eth_chainId, eth_gasPrice, net_version, eth_getBalance, eth_call, eth_getLogs)
- **Advanced Benchmarking**: Comprehensive performance statistics including:
  - Average, min, max latencies
  - Percentiles (P50, P95, P99)
  - Success rates
  - Error tracking
- **Retry Logic**: Intelligent retry mechanism with exponential backoff
- **Concurrent Testing**: Configurable number of parallel requests
- **Comparison Mode**: Side-by-side comparison of multiple RPC endpoints

#### Configuration
- **Configuration File Support**: YAML and JSON configuration files
- **CLI Configuration Generator**: `--generate-config` option to create example configs
- **Flexible Parameters**: Extensive CLI options for customizing test behavior

#### Reporting
- **Rich CLI Output**: Beautiful terminal interface with:
  - Color-coded results
  - Progress bars
  - Formatted tables
  - Success/failure indicators
- **JSON Export**: Machine-readable test results
- **CSV Export**: Spreadsheet-compatible format
- **HTML Reports**: Styled web-based reports with charts and visualizations

#### Project Structure
- **Proper Python Package**: Organized modular structure
  - `core.py`: Core testing logic
  - `config.py`: Configuration management
  - `reporting.py`: Results export
  - `cli.py`: Rich CLI interface
- **Unit Tests**: Comprehensive test coverage with pytest
- **Type Hints**: Full type annotation support
- **Package Installation**: setup.py for pip installation

#### Documentation
- **Comprehensive README**: Detailed documentation with examples
- **Example Configuration**: Pre-built configuration templates
- **Use Case Examples**: Real-world usage scenarios

### Changed
- Complete rewrite from simple script to full-featured package
- Improved error handling and logging
- Better async/await implementation
- Enhanced user experience with rich terminal UI

### Technical Improvements
- Modular architecture for better maintainability
- Comprehensive error handling
- Async context manager support
- Statistical analysis of results
- Configurable timeouts and retries
- Progress tracking during tests

## [1.0.0] - 2024 (Previous Version)

### Initial Release
- Basic async RPC testing
- Single method testing (eth_blockNumber)
- Simple CLI interface
- Basic error handling
