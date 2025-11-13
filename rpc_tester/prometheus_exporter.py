"""
Prometheus metrics exporter for RPC test results.
"""

from datetime import datetime
from typing import Any, Dict, List


class PrometheusExporter:
    """Export RPC test metrics in Prometheus format."""

    def __init__(self, job_name: str = "rpc_tester"):
        """
        Initialize Prometheus exporter.

        Args:
            job_name: Job name for metrics
        """
        self.job_name = job_name
        self.metrics: List[str] = []

    def _format_labels(self, labels: Dict[str, str]) -> str:
        """Format labels for Prometheus."""
        if not labels:
            return ""

        label_pairs = [f'{k}="{v}"' for k, v in labels.items()]
        return "{" + ",".join(label_pairs) + "}"

    def add_gauge(
        self, name: str, value: float, labels: Dict[str, str] = None, help_text: str = None
    ):
        """
        Add a gauge metric.

        Args:
            name: Metric name
            value: Metric value
            labels: Metric labels
            help_text: Help text for metric
        """
        if help_text:
            self.metrics.append(f"# HELP {name} {help_text}")
            self.metrics.append(f"# TYPE {name} gauge")

        label_str = self._format_labels(labels or {})
        self.metrics.append(f"{name}{label_str} {value}")

    def add_counter(
        self, name: str, value: int, labels: Dict[str, str] = None, help_text: str = None
    ):
        """
        Add a counter metric.

        Args:
            name: Metric name
            value: Metric value
            labels: Metric labels
            help_text: Help text for metric
        """
        if help_text:
            self.metrics.append(f"# HELP {name} {help_text}")
            self.metrics.append(f"# TYPE {name} counter")

        label_str = self._format_labels(labels or {})
        self.metrics.append(f"{name}{label_str} {value}")

    def add_histogram(
        self,
        name: str,
        values: List[float],
        labels: Dict[str, str] = None,
        help_text: str = None,
        buckets: List[float] = None,
    ):
        """
        Add a histogram metric.

        Args:
            name: Metric name
            values: List of observed values
            labels: Metric labels
            help_text: Help text for metric
            buckets: Histogram buckets
        """
        if not buckets:
            buckets = [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]

        if help_text:
            self.metrics.append(f"# HELP {name} {help_text}")
            self.metrics.append(f"# TYPE {name} histogram")

        base_labels = labels or {}
        sorted_values = sorted(values)

        # Count values in each bucket
        for bucket in buckets:
            count = sum(1 for v in sorted_values if v <= bucket)
            bucket_labels = {**base_labels, "le": str(bucket)}
            label_str = self._format_labels(bucket_labels)
            self.metrics.append(f"{name}_bucket{label_str} {count}")

        # Add +Inf bucket
        inf_labels = {**base_labels, "le": "+Inf"}
        label_str = self._format_labels(inf_labels)
        self.metrics.append(f"{name}_bucket{label_str} {len(values)}")

        # Add sum and count
        label_str = self._format_labels(base_labels)
        self.metrics.append(f"{name}_sum{label_str} {sum(values)}")
        self.metrics.append(f"{name}_count{label_str} {len(values)}")

    def export_rpc_stats(self, stats: Dict[str, Dict[str, Any]], timestamp: datetime = None):
        """
        Export RPC test statistics as Prometheus metrics.

        Args:
            stats: Statistics from EndpointStats
            timestamp: Optional timestamp for metrics
        """
        ts = int(timestamp.timestamp() * 1000) if timestamp else None

        for url, methods in stats.items():
            # Clean URL for label
            url_label = url.replace("https://", "").replace("http://", "")

            for method, stat in methods.items():
                labels = {"url": url_label, "method": method, "job": self.job_name}

                # Total requests counter
                self.add_counter(
                    "rpc_test_requests_total",
                    stat.total_requests,
                    labels,
                    "Total number of RPC requests",
                )

                # Successful requests counter
                self.add_counter(
                    "rpc_test_requests_successful",
                    stat.successful_requests,
                    labels,
                    "Number of successful RPC requests",
                )

                # Failed requests counter
                self.add_counter(
                    "rpc_test_requests_failed",
                    stat.failed_requests,
                    labels,
                    "Number of failed RPC requests",
                )

                # Success rate gauge
                self.add_gauge(
                    "rpc_test_success_rate",
                    stat.success_rate / 100,
                    labels,
                    "Success rate of RPC requests (0-1)",
                )

                # Latency metrics
                self.add_gauge(
                    "rpc_test_latency_avg_ms",
                    stat.avg_latency,
                    labels,
                    "Average latency in milliseconds",
                )

                self.add_gauge(
                    "rpc_test_latency_min_ms",
                    stat.min_latency,
                    labels,
                    "Minimum latency in milliseconds",
                )

                self.add_gauge(
                    "rpc_test_latency_max_ms",
                    stat.max_latency,
                    labels,
                    "Maximum latency in milliseconds",
                )

                # Percentile gauges
                self.add_gauge(
                    "rpc_test_latency_p50_ms",
                    stat.p50_latency,
                    labels,
                    "50th percentile latency in milliseconds",
                )

                self.add_gauge(
                    "rpc_test_latency_p95_ms",
                    stat.p95_latency,
                    labels,
                    "95th percentile latency in milliseconds",
                )

                self.add_gauge(
                    "rpc_test_latency_p99_ms",
                    stat.p99_latency,
                    labels,
                    "99th percentile latency in milliseconds",
                )

                # Latency histogram
                if stat.latencies:
                    self.add_histogram(
                        "rpc_test_latency_ms",
                        stat.latencies,
                        labels,
                        "Latency distribution in milliseconds",
                    )

    def export_health_metrics(self, health_data: Dict[str, Any]):
        """
        Export health check metrics.

        Args:
            health_data: Health check data
        """
        for url, data in health_data.items():
            url_label = url.replace("https://", "").replace("http://", "")
            summary = data.get("summary", {})

            labels = {"url": url_label, "job": self.job_name}

            # Health status (1 = healthy, 0.5 = degraded, 0 = unhealthy)
            status_value = {"healthy": 1.0, "degraded": 0.5, "unhealthy": 0.0, "unknown": -1.0}.get(
                summary.get("current_status", "unknown"), -1.0
            )

            self.add_gauge(
                "rpc_health_status",
                status_value,
                labels,
                "Health status (1=healthy, 0.5=degraded, 0=unhealthy)",
            )

            # Uptime percentage
            self.add_gauge(
                "rpc_health_uptime_percentage",
                summary.get("uptime_percentage", 0) / 100,
                labels,
                "Uptime percentage (0-1)",
            )

            # Average latency
            self.add_gauge(
                "rpc_health_avg_latency_ms",
                summary.get("avg_latency_ms", 0),
                labels,
                "Average health check latency in milliseconds",
            )

            # Error rate
            self.add_gauge(
                "rpc_health_error_rate",
                summary.get("error_rate", 0) / 100,
                labels,
                "Error rate (0-1)",
            )

            # Total checks
            self.add_counter(
                "rpc_health_checks_total",
                summary.get("total_checks", 0),
                labels,
                "Total number of health checks performed",
            )

    def to_string(self) -> str:
        """
        Get all metrics as a Prometheus-formatted string.

        Returns:
            Metrics in Prometheus exposition format
        """
        return "\n".join(self.metrics) + "\n"

    def save_to_file(self, filepath: str):
        """
        Save metrics to a file.

        Args:
            filepath: Path to save metrics
        """
        with open(filepath, "w") as f:
            f.write(self.to_string())

    def clear(self):
        """Clear all metrics."""
        self.metrics.clear()


class PrometheusPushGateway:
    """Push metrics to Prometheus Pushgateway."""

    def __init__(self, gateway_url: str, job_name: str = "rpc_tester"):
        """
        Initialize Pushgateway client.

        Args:
            gateway_url: Pushgateway URL (e.g., 'http://localhost:9091')
            job_name: Job name for metrics
        """
        self.gateway_url = gateway_url.rstrip("/")
        self.job_name = job_name

    async def push_metrics(
        self, exporter: PrometheusExporter, grouping_key: Dict[str, str] = None
    ) -> bool:
        """
        Push metrics to Pushgateway.

        Args:
            exporter: PrometheusExporter with metrics
            grouping_key: Additional grouping labels

        Returns:
            True if successful
        """
        import aiohttp

        url = f"{self.gateway_url}/metrics/job/{self.job_name}"

        # Add grouping key to URL
        if grouping_key:
            for key, value in grouping_key.items():
                url += f"/{key}/{value}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, data=exporter.to_string(), headers={"Content-Type": "text/plain"}
                ) as resp:
                    return resp.status == 200

        except Exception:
            return False

    async def delete_metrics(self, grouping_key: Dict[str, str] = None) -> bool:
        """
        Delete metrics from Pushgateway.

        Args:
            grouping_key: Grouping labels

        Returns:
            True if successful
        """
        import aiohttp

        url = f"{self.gateway_url}/metrics/job/{self.job_name}"

        if grouping_key:
            for key, value in grouping_key.items():
                url += f"/{key}/{value}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(url) as resp:
                    return resp.status == 202

        except Exception:
            return False
