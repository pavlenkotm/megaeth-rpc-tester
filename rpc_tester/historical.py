"""
Historical data comparison and analysis.

Compare current test results with historical data to track trends.
"""

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class HistoricalDataPoint:
    """Single historical data point."""

    timestamp: datetime
    endpoint: str
    method: str
    avg_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    success_rate: float
    total_requests: int
    metadata: Dict[str, Any]


class HistoricalDataStore:
    """Store and retrieve historical test data."""

    def __init__(self, storage_path: str = "historical_data.json"):
        """
        Initialize historical data store.

        Args:
            storage_path: Path to storage file
        """
        self.storage_path = Path(storage_path)
        self.data: List[HistoricalDataPoint] = []
        self._load()

    def _load(self):
        """Load data from storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, "r") as f:
                    raw_data = json.load(f)
                    self.data = [
                        HistoricalDataPoint(
                            timestamp=datetime.fromisoformat(item["timestamp"]),
                            endpoint=item["endpoint"],
                            method=item["method"],
                            avg_latency_ms=item["avg_latency_ms"],
                            p95_latency_ms=item["p95_latency_ms"],
                            p99_latency_ms=item["p99_latency_ms"],
                            success_rate=item["success_rate"],
                            total_requests=item["total_requests"],
                            metadata=item.get("metadata", {}),
                        )
                        for item in raw_data
                    ]
            except Exception as e:
                print(f"Error loading historical data: {e}")
                self.data = []

    def save(self):
        """Save data to storage."""
        try:
            serialized = [
                {
                    "timestamp": dp.timestamp.isoformat(),
                    "endpoint": dp.endpoint,
                    "method": dp.method,
                    "avg_latency_ms": dp.avg_latency_ms,
                    "p95_latency_ms": dp.p95_latency_ms,
                    "p99_latency_ms": dp.p99_latency_ms,
                    "success_rate": dp.success_rate,
                    "total_requests": dp.total_requests,
                    "metadata": dp.metadata,
                }
                for dp in self.data
            ]

            with open(self.storage_path, "w") as f:
                json.dump(serialized, f, indent=2)
        except Exception as e:
            print(f"Error saving historical data: {e}")

    def add_results(
        self, results: Dict[str, Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Add test results to historical data.

        Args:
            results: Test results dictionary
            metadata: Additional metadata
        """
        timestamp = datetime.now()
        metadata = metadata or {}

        for endpoint, methods in results.items():
            for method, stats in methods.items():
                data_point = HistoricalDataPoint(
                    timestamp=timestamp,
                    endpoint=endpoint,
                    method=method,
                    avg_latency_ms=stats.get("avg_latency_ms", 0),
                    p95_latency_ms=stats.get("p95_latency_ms", 0),
                    p99_latency_ms=stats.get("p99_latency_ms", 0),
                    success_rate=stats.get("success_rate", 0),
                    total_requests=stats.get("total_requests", 0),
                    metadata=metadata,
                )
                self.data.append(data_point)

        self.save()

    def get_data(
        self,
        endpoint: Optional[str] = None,
        method: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[HistoricalDataPoint]:
        """
        Query historical data.

        Args:
            endpoint: Filter by endpoint
            method: Filter by method
            start_date: Start date filter
            end_date: End date filter

        Returns:
            List of historical data points
        """
        filtered = self.data

        if endpoint:
            filtered = [d for d in filtered if d.endpoint == endpoint]

        if method:
            filtered = [d for d in filtered if d.method == method]

        if start_date:
            filtered = [d for d in filtered if d.timestamp >= start_date]

        if end_date:
            filtered = [d for d in filtered if d.timestamp <= end_date]

        return filtered

    def cleanup_old_data(self, days: int = 30):
        """
        Remove data older than specified days.

        Args:
            days: Number of days to keep
        """
        cutoff = datetime.now() - timedelta(days=days)
        self.data = [d for d in self.data if d.timestamp >= cutoff]
        self.save()


class HistoricalComparator:
    """Compare current results with historical data."""

    def __init__(self, data_store: HistoricalDataStore):
        """
        Initialize comparator.

        Args:
            data_store: Historical data store
        """
        self.data_store = data_store

    def compare_with_baseline(
        self, current_results: Dict[str, Dict[str, Any]], baseline_days: int = 7
    ) -> Dict[str, Any]:
        """
        Compare current results with historical baseline.

        Args:
            current_results: Current test results
            baseline_days: Number of days for baseline calculation

        Returns:
            Comparison results
        """
        start_date = datetime.now() - timedelta(days=baseline_days)
        comparisons = {}

        for endpoint, methods in current_results.items():
            endpoint_comparisons = {}

            for method, current_stats in methods.items():
                # Get historical data
                historical = self.data_store.get_data(
                    endpoint=endpoint, method=method, start_date=start_date
                )

                if not historical:
                    endpoint_comparisons[method] = {
                        "status": "no_baseline",
                        "message": "No historical data available",
                    }
                    continue

                # Calculate baseline metrics
                baseline_avg_latency = sum(h.avg_latency_ms for h in historical) / len(historical)
                baseline_success_rate = sum(h.success_rate for h in historical) / len(historical)

                current_avg_latency = current_stats.get("avg_latency_ms", 0)
                current_success_rate = current_stats.get("success_rate", 0)

                # Calculate changes
                latency_change = (
                    ((current_avg_latency - baseline_avg_latency) / baseline_avg_latency * 100)
                    if baseline_avg_latency > 0
                    else 0
                )

                success_change = current_success_rate - baseline_success_rate

                # Determine status
                if abs(latency_change) < 10 and abs(success_change) < 5:
                    status = "stable"
                elif latency_change > 25 or success_change < -10:
                    status = "degraded"
                elif latency_change < -10 and success_change > 5:
                    status = "improved"
                else:
                    status = "changed"

                endpoint_comparisons[method] = {
                    "status": status,
                    "baseline_avg_latency_ms": baseline_avg_latency,
                    "current_avg_latency_ms": current_avg_latency,
                    "latency_change_percent": latency_change,
                    "baseline_success_rate": baseline_success_rate,
                    "current_success_rate": current_success_rate,
                    "success_rate_change": success_change,
                    "baseline_data_points": len(historical),
                    "baseline_period_days": baseline_days,
                }

            comparisons[endpoint] = endpoint_comparisons

        return comparisons

    def get_trends(self, endpoint: str, method: str, days: int = 30) -> Dict[str, Any]:
        """
        Analyze trends for endpoint/method.

        Args:
            endpoint: Endpoint URL
            method: RPC method
            days: Number of days to analyze

        Returns:
            Trend analysis
        """
        start_date = datetime.now() - timedelta(days=days)
        historical = self.data_store.get_data(
            endpoint=endpoint, method=method, start_date=start_date
        )

        if not historical:
            return {"status": "no_data"}

        # Sort by timestamp
        historical = sorted(historical, key=lambda x: x.timestamp)

        # Calculate trends
        latencies = [h.avg_latency_ms for h in historical]
        success_rates = [h.success_rate for h in historical]

        # Simple trend detection
        latency_trend = self._calculate_trend(latencies)
        success_trend = self._calculate_trend(success_rates)

        return {
            "endpoint": endpoint,
            "method": method,
            "period_days": days,
            "data_points": len(historical),
            "latency_trend": latency_trend,
            "success_rate_trend": success_trend,
            "avg_latency_range": {
                "min": min(latencies),
                "max": max(latencies),
                "current": latencies[-1] if latencies else 0,
            },
            "success_rate_range": {
                "min": min(success_rates),
                "max": max(success_rates),
                "current": success_rates[-1] if success_rates else 0,
            },
        }

    @staticmethod
    def _calculate_trend(values: List[float]) -> str:
        """Calculate trend direction from values."""
        if len(values) < 2:
            return "stable"

        # Simple linear regression slope
        n = len(values)
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(values) / n

        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        slope = numerator / denominator if denominator != 0 else 0

        # Determine trend
        if abs(slope) < 0.1:
            return "stable"
        elif slope > 0:
            return "increasing"
        else:
            return "decreasing"

    def generate_report(self, comparisons: Dict[str, Any]) -> str:
        """
        Generate human-readable comparison report.

        Args:
            comparisons: Comparison results

        Returns:
            Formatted report
        """
        lines = ["=" * 80, "HISTORICAL COMPARISON REPORT", "=" * 80, ""]

        for endpoint, methods in comparisons.items():
            lines.append(f"\nEndpoint: {endpoint}")
            lines.append("-" * 80)

            for method, comparison in methods.items():
                status = comparison.get("status", "unknown")
                lines.append(f"\n  Method: {method}")
                lines.append(f"  Status: {status.upper()}")

                if status != "no_baseline":
                    lines.append(
                        f"  Baseline Latency: {comparison['baseline_avg_latency_ms']:.2f}ms"
                    )
                    lines.append(f"  Current Latency: {comparison['current_avg_latency_ms']:.2f}ms")
                    lines.append(f"  Change: {comparison['latency_change_percent']:+.2f}%")
                    lines.append(
                        f"  Baseline Success Rate: {comparison['baseline_success_rate']:.2f}%"
                    )
                    lines.append(
                        f"  Current Success Rate: {comparison['current_success_rate']:.2f}%"
                    )
                    lines.append(f"  Change: {comparison['success_rate_change']:+.2f}%")

        lines.append("\n" + "=" * 80)

        return "\n".join(lines)
