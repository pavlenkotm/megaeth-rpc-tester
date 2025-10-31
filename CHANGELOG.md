# Changelog

All notable changes to this project will be documented in this file.

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
