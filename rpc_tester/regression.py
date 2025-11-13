"""
Performance regression detection for RPC tests.

Detect performance degradations by comparing current results with baseline.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class RegressionSeverity(Enum):
    """Severity levels for performance regressions."""

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RegressionResult:
    """Result of regression detection."""

    endpoint: str
    method: str
    metric: str
    baseline_value: float
    current_value: float
    change_percent: float
    severity: RegressionSeverity
    timestamp: str
    details: Dict[str, Any]


class RegressionDetector:
    """Detect performance regressions in test results."""

    def __init__(self, thresholds: Optional[Dict[str, Dict[str, float]]] = None):
        """
        Initialize regression detector.

        Args:
            thresholds: Custom thresholds for different severity levels
                       Format: {'metric': {'low': 10, 'medium': 25, 'high': 50, 'critical': 100}}
        """
        self.thresholds = thresholds or {
            "latency": {
                "low": 10.0,  # 10% increase
                "medium": 25.0,  # 25% increase
                "high": 50.0,  # 50% increase
                "critical": 100.0,  # 100% increase (2x)
            },
            "success_rate": {
                "low": 1.0,  # 1% decrease
                "medium": 5.0,  # 5% decrease
                "high": 10.0,  # 10% decrease
                "critical": 20.0,  # 20% decrease
            },
            "error_rate": {
                "low": 1.0,  # 1% increase
                "medium": 5.0,  # 5% increase
                "high": 10.0,  # 10% increase
                "critical": 20.0,  # 20% increase
            },
        }

    def detect_latency_regression(
        self, baseline: Dict[str, float], current: Dict[str, float], endpoint: str, method: str
    ) -> Optional[RegressionResult]:
        """
        Detect latency regression.

        Args:
            baseline: Baseline latency metrics
            current: Current latency metrics
            endpoint: RPC endpoint
            method: RPC method

        Returns:
            RegressionResult if regression detected, None otherwise
        """
        baseline_latency = baseline.get("avg_latency_ms", 0)
        current_latency = current.get("avg_latency_ms", 0)

        if baseline_latency == 0:
            return None

        change_percent = ((current_latency - baseline_latency) / baseline_latency) * 100

        if change_percent <= 0:
            return None  # No regression, performance improved or stayed same

        severity = self._determine_severity("latency", change_percent)

        if severity == RegressionSeverity.NONE:
            return None

        return RegressionResult(
            endpoint=endpoint,
            method=method,
            metric="latency",
            baseline_value=baseline_latency,
            current_value=current_latency,
            change_percent=change_percent,
            severity=severity,
            timestamp=datetime.now().isoformat(),
            details={
                "baseline_p95": baseline.get("p95_latency_ms", 0),
                "current_p95": current.get("p95_latency_ms", 0),
                "baseline_p99": baseline.get("p99_latency_ms", 0),
                "current_p99": current.get("p99_latency_ms", 0),
            },
        )

    def detect_success_rate_regression(
        self, baseline: Dict[str, float], current: Dict[str, float], endpoint: str, method: str
    ) -> Optional[RegressionResult]:
        """
        Detect success rate regression.

        Args:
            baseline: Baseline success rate
            current: Current success rate
            endpoint: RPC endpoint
            method: RPC method

        Returns:
            RegressionResult if regression detected, None otherwise
        """
        baseline_rate = baseline.get("success_rate", 100)
        current_rate = current.get("success_rate", 100)

        change_percent = baseline_rate - current_rate  # Decrease is bad

        if change_percent <= 0:
            return None  # No regression

        severity = self._determine_severity("success_rate", change_percent)

        if severity == RegressionSeverity.NONE:
            return None

        return RegressionResult(
            endpoint=endpoint,
            method=method,
            metric="success_rate",
            baseline_value=baseline_rate,
            current_value=current_rate,
            change_percent=-change_percent,  # Negative to show decrease
            severity=severity,
            timestamp=datetime.now().isoformat(),
            details={
                "baseline_failed": baseline.get("failed_requests", 0),
                "current_failed": current.get("failed_requests", 0),
                "baseline_total": baseline.get("total_requests", 0),
                "current_total": current.get("total_requests", 0),
            },
        )

    def detect_all_regressions(
        self,
        baseline_results: Dict[str, Dict[str, Any]],
        current_results: Dict[str, Dict[str, Any]],
    ) -> List[RegressionResult]:
        """
        Detect all regressions between baseline and current results.

        Args:
            baseline_results: Baseline test results
            current_results: Current test results

        Returns:
            List of detected regressions
        """
        regressions = []

        for endpoint in current_results:
            if endpoint not in baseline_results:
                continue

            baseline_methods = baseline_results[endpoint]
            current_methods = current_results[endpoint]

            for method in current_methods:
                if method not in baseline_methods:
                    continue

                baseline_stats = baseline_methods[method]
                current_stats = current_methods[method]

                # Check latency regression
                latency_reg = self.detect_latency_regression(
                    baseline_stats, current_stats, endpoint, method
                )
                if latency_reg:
                    regressions.append(latency_reg)

                # Check success rate regression
                success_reg = self.detect_success_rate_regression(
                    baseline_stats, current_stats, endpoint, method
                )
                if success_reg:
                    regressions.append(success_reg)

        return regressions

    def _determine_severity(self, metric: str, change_percent: float) -> RegressionSeverity:
        """Determine severity based on change percentage."""
        thresholds = self.thresholds.get(metric, {})

        if change_percent >= thresholds.get("critical", 100):
            return RegressionSeverity.CRITICAL
        elif change_percent >= thresholds.get("high", 50):
            return RegressionSeverity.HIGH
        elif change_percent >= thresholds.get("medium", 25):
            return RegressionSeverity.MEDIUM
        elif change_percent >= thresholds.get("low", 10):
            return RegressionSeverity.LOW
        else:
            return RegressionSeverity.NONE

    def generate_report(self, regressions: List[RegressionResult]) -> str:
        """
        Generate human-readable regression report.

        Args:
            regressions: List of detected regressions

        Returns:
            Formatted report string
        """
        if not regressions:
            return "No performance regressions detected."

        report_lines = [
            "=" * 80,
            "PERFORMANCE REGRESSION REPORT",
            "=" * 80,
            f"\nTotal Regressions Found: {len(regressions)}",
            "",
        ]

        # Group by severity
        by_severity = {}
        for reg in regressions:
            severity = reg.severity.value
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(reg)

        # Report by severity (critical first)
        severity_order = ["critical", "high", "medium", "low"]
        for severity in severity_order:
            if severity not in by_severity:
                continue

            regs = by_severity[severity]
            report_lines.append(f"\n{severity.upper()} Severity ({len(regs)} issues)")
            report_lines.append("-" * 80)

            for reg in regs:
                report_lines.append(f"\nEndpoint: {reg.endpoint}")
                report_lines.append(f"Method: {reg.method}")
                report_lines.append(f"Metric: {reg.metric}")
                report_lines.append(f"Baseline: {reg.baseline_value:.2f}")
                report_lines.append(f"Current: {reg.current_value:.2f}")
                report_lines.append(f"Change: {reg.change_percent:+.2f}%")

                if reg.details:
                    report_lines.append("Details:")
                    for key, value in reg.details.items():
                        report_lines.append(f"  {key}: {value}")

        report_lines.append("\n" + "=" * 80)

        return "\n".join(report_lines)


class BaselineManager:
    """Manage baseline results for regression detection."""

    def __init__(self):
        """Initialize baseline manager."""
        self.baselines: Dict[str, Dict[str, Any]] = {}

    def set_baseline(
        self, identifier: str, results: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Set baseline for comparison.

        Args:
            identifier: Baseline identifier (e.g., "v1.0", "production")
            results: Test results to use as baseline
            metadata: Additional metadata
        """
        self.baselines[identifier] = {
            "results": results,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }

    def get_baseline(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Get baseline by identifier.

        Args:
            identifier: Baseline identifier

        Returns:
            Baseline data or None
        """
        baseline = self.baselines.get(identifier)
        if baseline:
            return baseline["results"]
        return None

    def list_baselines(self) -> List[str]:
        """List all baseline identifiers."""
        return list(self.baselines.keys())

    def remove_baseline(self, identifier: str):
        """Remove baseline."""
        if identifier in self.baselines:
            del self.baselines[identifier]

    def get_latest_baseline(self) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        Get most recent baseline.

        Returns:
            Tuple of (identifier, results) or None
        """
        if not self.baselines:
            return None

        latest = max(self.baselines.items(), key=lambda x: x[1]["timestamp"])

        return latest[0], latest[1]["results"]


class ChangePointDetector:
    """Detect change points in time series performance data."""

    @staticmethod
    def detect_change_points(values: List[float], threshold: float = 2.0) -> List[int]:
        """
        Detect points where performance significantly changed.

        Args:
            values: Time-ordered performance values
            threshold: Number of standard deviations for detection

        Returns:
            List of indices where change points were detected
        """
        if len(values) < 3:
            return []

        change_points = []

        # Calculate moving average and standard deviation
        window_size = min(10, len(values) // 3)

        for i in range(window_size, len(values) - window_size):
            before = values[i - window_size : i]
            after = values[i : i + window_size]

            mean_before = sum(before) / len(before)
            mean_after = sum(after) / len(after)

            # Simple change detection based on difference
            if len(before) > 1:
                std = (sum((x - mean_before) ** 2 for x in before) / len(before)) ** 0.5
                if std > 0:
                    z_score = abs(mean_after - mean_before) / std
                    if z_score > threshold:
                        change_points.append(i)

        return change_points
