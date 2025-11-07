# Changelog

All notable changes to this project will be documented in this file.

## [3.1.0] - 2025-11-07

### Major Release: Multi-Language Web3 Playground

This release transforms the repository into a comprehensive showcase of Web3 development across 14+ programming languages.

#### New Languages & Examples (14 total)

**Smart Contract Languages:**
- **Solidity**: ERC-20 and ERC-721 implementations with Hardhat
- **Vyper**: Secure vault and token contracts with Brownie
- **Rust**: Solana SPL token program using Anchor framework
- **Move**: Aptos token module with comprehensive tests

**Frontend & Application:**
- **TypeScript**: React components (WalletConnect, useContract, web3Utils)
- **JavaScript**: Web3 utilities and Ethers.js integration
- **HTML/CSS**: Professional DApp landing page with MetaMask

**Backend & Clients:**
- **Go**: Full RPC client with go-ethereum
- **Java**: Enterprise Web3j integration with Maven
- **Ruby**: Elegant RPC client wrapper

**Low-Level & Systems:**
- **C++**: Cryptographic utilities (SHA-256, ECDSA, secp256k1)
- **Zig**: WASM-compatible Web3 utilities
- **AssemblyScript**: WebAssembly modules
- **Haskell**: Functional type-safe RPC client

**DevOps:**
- **Bash**: Deployment scripts and node management

#### Documentation
- Comprehensive multi-language README
- Individual READMEs for all 14+ languages
- CODE_OF_CONDUCT.md (Contributor Covenant)
- Updated CONTRIBUTING.md for multi-language contributions
- Detailed setup and usage guides

#### CI/CD
- Multi-language GitHub Actions pipeline
- Automated testing for 10+ languages
- Code quality checks and linting
- Build verification across all platforms

#### Infrastructure
- Organized `languages/` directory structure
- Consistent documentation patterns
- Package manager configs for all languages
- Build systems (CMake, Cargo, Maven, npm, etc.)

## [3.0.0] - 2025-11-06

### Major Release: Enterprise Features & Advanced Analytics

This is a major release with 14 new modules adding enterprise-grade features, advanced analytics, and comprehensive monitoring capabilities.

### New Modules (14 total)

#### Data Persistence & Storage
- **`database.py`**: Database integration with SQLite and PostgreSQL support
  - Store test results persistently
  - Query historical data
  - Test run tracking with metadata
  - Performance metrics storage

#### Notifications & Communication
- **`notifications.py`**: Multi-channel notification system
  - Email notifications via SMTP
  - Webhook notifications
  - Test completion alerts
  - Performance degradation alerts

- **`slack_integration.py`**: Rich Slack integration
  - Formatted test result messages
  - Color-coded alerts (green/yellow/red)
  - Performance degradation notifications
  - Success rate alerts
  - Slack message formatting utilities

#### Analytics & Intelligence
- **`statistics.py`**: Advanced statistical analysis
  - 15+ statistical metrics (mean, median, mode, std dev, variance)
  - Percentile calculations (P25, P50, P75, P90, P95, P99, P99.9)
  - Skewness and kurtosis
  - Outlier detection (IQR and Z-score methods)
  - Trend analysis with linear regression
  - Histogram generation
  - Distribution comparison
  - APDEX score calculation
  - SLA compliance checking
  - Availability metrics with "nines" calculation

- **`regression.py`**: Performance regression detection
  - Multi-level severity classification (low, medium, high, critical)
  - Latency regression detection
  - Success rate regression detection
  - Baseline management
  - Change point detection
  - Configurable thresholds
  - Detailed regression reporting

- **`benchmarks.py`**: Comprehensive benchmark scoring
  - Weighted multi-criteria scoring
  - Letter grade system (A-F)
  - Endpoint ranking and comparison
  - Score by latency, success rate, consistency, availability, throughput
  - Best endpoint recommendations
  - Performance comparison tables

- **`historical.py`**: Historical data analysis
  - Time-series data storage (JSON-based)
  - Baseline comparison (N-day baselines)
  - Trend analysis with linear regression
  - Status classification (stable, degraded, improved, changed)
  - Historical data cleanup
  - Detailed comparison reports

#### Monitoring & Reliability
- **`alerts.py`**: Advanced alert system
  - Multi-level alerts (info, warning, error, critical)
  - Configurable thresholds with operators
  - Alert rules engine
  - Default rules for common scenarios
  - Alert history tracking
  - Alert aggregation and summarization
  - Alert suppression to prevent spam

- **`circuit_breaker.py`**: Circuit breaker and bulkhead patterns
  - Three-state circuit breaker (CLOSED/OPEN/HALF_OPEN)
  - Adaptive circuit breaker with error rate monitoring
  - Bulkhead pattern for request limiting
  - Automatic recovery with configurable timeout
  - CircuitBreakerRegistry for managing multiple breakers
  - Detailed state tracking and metrics

#### Extensibility & Integration
- **`plugins.py`**: Extensible plugin system
  - Plugin base classes (TestHook, Metrics, Exporter)
  - Lifecycle management (initialize, cleanup)
  - Dynamic plugin loading from files/directories
  - Built-in example plugins
  - Test lifecycle hooks (on_test_start, on_test_complete, etc.)
  - Custom metrics collection
  - Custom export formats

- **`auth.py`**: Comprehensive authentication
  - API Key authentication (header or query param)
  - HTTP Basic authentication
  - Bearer token authentication
  - JWT authentication with refresh
  - OAuth 2.0 authentication
  - HMAC signature authentication
  - AWS Signature V4 authentication
  - Custom header authentication
  - AuthManager for multi-endpoint auth
  - Configuration from files (JSON/YAML)

#### Advanced Testing
- **`graphql_support.py`**: Full GraphQL testing
  - GraphQL query and mutation execution
  - Performance metrics for GraphQL
  - Multiple query testing
  - GraphQL query builder utilities
  - Introspection query support
  - GraphQL benchmarking
  - Load testing with ramp-up
  - Endpoint comparison

#### Export & Reporting
- **`exporters.py`**: Multiple export formats
  - Markdown exporter with formatted tables
  - XML exporter with pretty-printing
  - JSON Lines (JSONL) exporter
  - Prometheus text exposition format
  - ExporterRegistry for managing exporters
  - Custom exporter support

#### Automation
- **`scheduler.py`**: Test scheduling system
  - Interval-based scheduling
  - Daily scheduling at specific times
  - Weekly scheduling on specific days
  - One-time scheduled tasks
  - Task enable/disable controls
  - Callback system for test completion
  - Save/load schedules from JSON
  - Async task execution
  - Task status tracking

### Features Summary

#### Database & Persistence
- SQLite database integration with async support
- PostgreSQL support (placeholder for future)
- Persistent storage of test runs and results
- Historical data queries by endpoint, method, date range
- Performance metrics tracking over time

#### Notifications
- Email notifications via SMTP with TLS support
- Webhook notifications for any HTTP endpoint
- Slack integration with rich formatting
- Color-coded alerts based on severity
- Test completion notifications
- Performance degradation alerts

#### Advanced Analytics
- 15+ statistical metrics including skewness, kurtosis
- Comprehensive percentile calculations
- Outlier detection using IQR and Z-score
- Trend analysis with linear regression
- Distribution comparison utilities
- APDEX score for application performance
- SLA compliance checking
- Availability metrics with "nines"

#### Regression Detection
- Automatic performance regression detection
- Multi-level severity (low, medium, high, critical)
- Baseline management and comparison
- Configurable thresholds per metric
- Change point detection in time series
- Detailed regression reports

#### Benchmarking
- Multi-criteria endpoint scoring
- Weighted scoring algorithm
- Letter grades (A-F) for endpoints
- Endpoint ranking and recommendations
- Performance comparison tables
- Find best endpoint by criterion

#### Historical Analysis
- Long-term performance tracking
- Baseline comparison (7-day, 30-day, etc.)
- Trend detection (increasing, decreasing, stable)
- Historical data cleanup
- Status classification
- Comprehensive comparison reports

#### Alerting
- Configurable alert rules with thresholds
- Multi-level severity (info, warning, error, critical)
- Default rules for common scenarios
- Alert history and tracking
- Alert aggregation by level, endpoint, metric
- Alert suppression to prevent spam

#### Reliability Patterns
- Circuit breaker with CLOSED/OPEN/HALF_OPEN states
- Adaptive circuit breaker with error rate monitoring
- Bulkhead pattern for request isolation
- Automatic recovery mechanisms
- Registry for managing multiple breakers
- Detailed metrics and state tracking

#### Plugin System
- Extensible plugin architecture
- Test lifecycle hooks
- Custom metrics collection plugins
- Custom export format plugins
- Dynamic plugin loading
- Example plugins included

#### Authentication
- 8+ authentication methods
- API Key (header or query param)
- HTTP Basic, Bearer Token, JWT
- OAuth 2.0, HMAC, AWS Signature V4
- Multi-endpoint auth management
- Configuration from files

#### GraphQL Support
- Full GraphQL query/mutation testing
- Performance metrics for GraphQL
- Query builder utilities
- Introspection support
- Benchmarking across endpoints
- Load testing with ramp-up

#### Export Formats
- Markdown reports with tables
- XML export with pretty-printing
- JSON Lines (JSONL) format
- Prometheus text exposition format
- Extensible exporter registry

#### Test Scheduling
- Automated periodic testing
- Multiple schedule types (interval, daily, weekly, once)
- Task management (enable/disable)
- Callback system
- Save/load schedules
- Async execution

### Enhanced

#### Statistics & Analytics
- Extended statistical analysis beyond basic metrics
- Advanced outlier detection
- Histogram generation
- Coefficient of variation
- Performance trend analysis

#### Monitoring
- Comprehensive alert system
- Circuit breaker patterns
- Historical data tracking
- Regression detection

#### Integration
- Multi-channel notifications
- Database persistence
- Plugin extensibility
- Authentication flexibility

### Technical Improvements
- Async-first architecture throughout
- Type hints in all new modules
- Comprehensive error handling
- Modular design for extensibility
- Thread-safe operations where needed
- Memory-efficient data structures

### Performance
- Circuit breaker prevents cascade failures
- Bulkhead pattern limits resource usage
- Adaptive thresholds in circuit breakers
- Efficient historical data storage
- Optimized statistical calculations

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
