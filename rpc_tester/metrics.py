"""
Advanced metrics tracking for RPC testing.
"""

import statistics
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class RequestMetrics:
    """Metrics for individual requests."""

    url: str
    method: str
    timestamp: datetime
    latency_ms: float
    success: bool
    status_code: Optional[int] = None
    error: Optional[str] = None
    attempt: int = 1
    cached: bool = False


@dataclass
class AggregatedMetrics:
    """Aggregated metrics for analysis."""

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    cached_requests: int = 0
    total_latency_ms: float = 0.0
    min_latency_ms: float = float("inf")
    max_latency_ms: float = 0.0
    latencies: List[float] = field(default_factory=list)

    def add_request(self, metrics: RequestMetrics):
        """Add request metrics to aggregation."""
        self.total_requests += 1

        if metrics.success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1

        if metrics.cached:
            self.cached_requests += 1

        self.total_latency_ms += metrics.latency_ms
        self.min_latency_ms = min(self.min_latency_ms, metrics.latency_ms)
        self.max_latency_ms = max(self.max_latency_ms, metrics.latency_ms)
        self.latencies.append(metrics.latency_ms)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        if not self.latencies:
            return {
                "total_requests": self.total_requests,
                "successful_requests": self.successful_requests,
                "failed_requests": self.failed_requests,
                "cached_requests": self.cached_requests,
                "success_rate": 0.0,
                "cache_hit_rate": 0.0,
                "avg_latency_ms": 0.0,
                "min_latency_ms": 0.0,
                "max_latency_ms": 0.0,
                "median_latency_ms": 0.0,
                "p95_latency_ms": 0.0,
                "p99_latency_ms": 0.0,
                "std_dev_ms": 0.0,
            }

        success_rate = (
            (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0
        )
        cache_hit_rate = (
            (self.cached_requests / self.total_requests * 100) if self.total_requests > 0 else 0
        )

        sorted_latencies = sorted(self.latencies)
        n = len(sorted_latencies)

        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "cached_requests": self.cached_requests,
            "success_rate": success_rate,
            "cache_hit_rate": cache_hit_rate,
            "avg_latency_ms": statistics.mean(self.latencies),
            "min_latency_ms": self.min_latency_ms,
            "max_latency_ms": self.max_latency_ms,
            "median_latency_ms": statistics.median(self.latencies),
            "p95_latency_ms": sorted_latencies[int(n * 0.95)] if n > 0 else 0,
            "p99_latency_ms": sorted_latencies[int(n * 0.99)] if n > 0 else 0,
            "std_dev_ms": statistics.stdev(self.latencies) if len(self.latencies) > 1 else 0.0,
        }


class MetricsCollector:
    """Collects and aggregates metrics for RPC testing."""

    def __init__(self):
        """Initialize metrics collector."""
        self.requests: List[RequestMetrics] = []
        self.by_url: Dict[str, AggregatedMetrics] = defaultdict(AggregatedMetrics)
        self.by_method: Dict[str, AggregatedMetrics] = defaultdict(AggregatedMetrics)
        self.by_url_method: Dict[str, Dict[str, AggregatedMetrics]] = defaultdict(
            lambda: defaultdict(AggregatedMetrics)
        )
        self.start_time = time.time()

    def record_request(self, metrics: RequestMetrics):
        """Record a request metric."""
        self.requests.append(metrics)
        self.by_url[metrics.url].add_request(metrics)
        self.by_method[metrics.method].add_request(metrics)
        self.by_url_method[metrics.url][metrics.method].add_request(metrics)

    def get_url_summary(self, url: str) -> Dict[str, Any]:
        """Get summary for specific URL."""
        if url not in self.by_url:
            return {}
        return self.by_url[url].get_summary()

    def get_method_summary(self, method: str) -> Dict[str, Any]:
        """Get summary for specific method."""
        if method not in self.by_method:
            return {}
        return self.by_method[method].get_summary()

    def get_url_method_summary(self, url: str, method: str) -> Dict[str, Any]:
        """Get summary for specific URL and method combination."""
        if url not in self.by_url_method or method not in self.by_url_method[url]:
            return {}
        return self.by_url_method[url][method].get_summary()

    def get_overall_summary(self) -> Dict[str, Any]:
        """Get overall summary across all requests."""
        overall = AggregatedMetrics()
        for req in self.requests:
            overall.add_request(req)

        summary = overall.get_summary()
        summary["duration_seconds"] = time.time() - self.start_time
        summary["requests_per_second"] = (
            len(self.requests) / summary["duration_seconds"]
            if summary["duration_seconds"] > 0
            else 0
        )

        return summary

    def get_error_distribution(self) -> Dict[str, int]:
        """Get distribution of errors."""
        errors = defaultdict(int)
        for req in self.requests:
            if req.error:
                errors[req.error] += 1
        return dict(errors)

    def get_latency_histogram(self, bucket_size_ms: float = 50) -> Dict[str, int]:
        """Get latency histogram."""
        histogram = defaultdict(int)
        for req in self.requests:
            bucket = int(req.latency_ms / bucket_size_ms) * bucket_size_ms
            bucket_label = f"{bucket}-{bucket + bucket_size_ms}ms"
            histogram[bucket_label] += 1
        return dict(sorted(histogram.items()))

    def get_time_series(self, interval_seconds: int = 60) -> List[Dict[str, Any]]:
        """Get time series data for requests."""
        if not self.requests:
            return []

        # Sort requests by timestamp
        sorted_requests = sorted(self.requests, key=lambda r: r.timestamp)

        # Group by time intervals
        series = []
        current_bucket_start = sorted_requests[0].timestamp
        current_bucket = []

        for req in sorted_requests:
            time_diff = (req.timestamp - current_bucket_start).total_seconds()

            if time_diff >= interval_seconds:
                # Process current bucket
                if current_bucket:
                    bucket_metrics = AggregatedMetrics()
                    for bucket_req in current_bucket:
                        bucket_metrics.add_request(bucket_req)

                    summary = bucket_metrics.get_summary()
                    summary["timestamp"] = current_bucket_start.isoformat()
                    series.append(summary)

                # Start new bucket
                current_bucket_start = req.timestamp
                current_bucket = [req]
            else:
                current_bucket.append(req)

        # Process last bucket
        if current_bucket:
            bucket_metrics = AggregatedMetrics()
            for bucket_req in current_bucket:
                bucket_metrics.add_request(bucket_req)

            summary = bucket_metrics.get_summary()
            summary["timestamp"] = current_bucket_start.isoformat()
            series.append(summary)

        return series

    def export_metrics(self) -> Dict[str, Any]:
        """Export all metrics as a dictionary."""
        return {
            "overall": self.get_overall_summary(),
            "by_url": {url: metrics.get_summary() for url, metrics in self.by_url.items()},
            "by_method": {
                method: metrics.get_summary() for method, metrics in self.by_method.items()
            },
            "by_url_method": {
                url: {method: metrics.get_summary() for method, metrics in methods.items()}
                for url, methods in self.by_url_method.items()
            },
            "error_distribution": self.get_error_distribution(),
            "latency_histogram": self.get_latency_histogram(),
            "time_series": self.get_time_series(),
        }
