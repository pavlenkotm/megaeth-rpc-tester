# MegaETH RPC Tester Examples

This directory contains example scripts demonstrating various features of the RPC Tester.

## Examples

### 1. Basic Usage (`basic_usage.py`)

Simple example showing how to test a single RPC endpoint.

```bash
python examples/basic_usage.py
```

**Features demonstrated:**
- Basic configuration
- Running tests
- Displaying results

---

### 2. Compare Endpoints (`compare_endpoints.py`)

Compare performance of multiple RPC providers.

```bash
python examples/compare_endpoints.py
```

**Features demonstrated:**
- Testing multiple endpoints
- Performance comparison
- Export to multiple formats (JSON, CSV, HTML)
- Ranking endpoints by performance

---

### 3. Caching (`with_caching.py`)

Use caching to improve performance and reduce redundant requests.

```bash
python examples/with_caching.py
```

**Features demonstrated:**
- In-memory caching
- Persistent disk caching
- Cache hit/miss tracking
- TTL configuration

---

### 4. Health Monitoring (`health_monitoring.py`)

Continuous health monitoring of RPC endpoints.

```bash
python examples/health_monitoring.py
```

**Features demonstrated:**
- Health status checking (healthy/degraded/unhealthy)
- Continuous monitoring
- Uptime percentage calculation
- Error rate tracking
- Health summaries

---

### 5. Prometheus Integration (`prometheus_integration.py`)

Export metrics in Prometheus format.

```bash
python examples/prometheus_integration.py
```

**Features demonstrated:**
- Prometheus metrics export
- Pushgateway integration
- Metric types (gauges, counters, histograms)
- File-based metrics for scraping

---

## Running Examples

All examples can be run directly:

```bash
# Make scripts executable
chmod +x examples/*.py

# Run any example
./examples/basic_usage.py
```

Or using Python:

```bash
python examples/basic_usage.py
```

## Prerequisites

Make sure you have installed all dependencies:

```bash
pip install -r requirements.txt
```

## Customization

Each example can be easily customized by modifying:
- RPC endpoint URLs
- Number of requests
- Test methods
- Configuration parameters

## Integration

These examples can be used as templates for:
- CI/CD pipelines
- Monitoring systems
- Performance testing
- Load testing
- Health checks

## Output

Examples create various output files:
- `comparison_results/` - Comparison reports
- `.cache/` - Cached results
- `metrics.prom` - Prometheus metrics
- Test results in JSON/CSV/HTML formats

## Support

For more information, see the main [README.md](../README.md) in the repository root.
