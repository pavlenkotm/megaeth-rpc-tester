"""
Alert system for monitoring RPC test results.

Trigger alerts when metrics exceed defined thresholds.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import asyncio


class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class MetricType(Enum):
    """Types of metrics that can be monitored."""
    LATENCY = "latency"
    SUCCESS_RATE = "success_rate"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"
    AVAILABILITY = "availability"


@dataclass
class AlertThreshold:
    """Threshold configuration for alerts."""
    metric_type: MetricType
    operator: str  # >, <, >=, <=, ==
    value: float
    level: AlertLevel
    message_template: str


@dataclass
class Alert:
    """Alert instance."""
    alert_id: str
    level: AlertLevel
    metric_type: MetricType
    endpoint: str
    method: str
    message: str
    current_value: float
    threshold_value: float
    timestamp: str
    metadata: Dict[str, Any]


class AlertRule:
    """Define rules for triggering alerts."""

    def __init__(self, name: str, description: str,
                 thresholds: List[AlertThreshold],
                 enabled: bool = True):
        """
        Initialize alert rule.

        Args:
            name: Rule name
            description: Rule description
            thresholds: List of threshold configurations
            enabled: Whether rule is enabled
        """
        self.name = name
        self.description = description
        self.thresholds = thresholds
        self.enabled = enabled

    def evaluate(self, endpoint: str, method: str,
                metrics: Dict[str, float]) -> List[Alert]:
        """
        Evaluate metrics against thresholds.

        Args:
            endpoint: RPC endpoint
            method: RPC method
            metrics: Metrics to evaluate

        Returns:
            List of triggered alerts
        """
        if not self.enabled:
            return []

        alerts = []

        for threshold in self.thresholds:
            metric_name = threshold.metric_type.value
            current_value = metrics.get(metric_name, 0)

            if self._evaluate_condition(current_value, threshold.operator, threshold.value):
                alert_id = f"{endpoint}_{method}_{metric_name}_{datetime.now().timestamp()}"

                message = threshold.message_template.format(
                    endpoint=endpoint,
                    method=method,
                    metric=metric_name,
                    value=current_value,
                    threshold=threshold.value
                )

                alert = Alert(
                    alert_id=alert_id,
                    level=threshold.level,
                    metric_type=threshold.metric_type,
                    endpoint=endpoint,
                    method=method,
                    message=message,
                    current_value=current_value,
                    threshold_value=threshold.value,
                    timestamp=datetime.now().isoformat(),
                    metadata=metrics
                )

                alerts.append(alert)

        return alerts

    @staticmethod
    def _evaluate_condition(value: float, operator: str, threshold: float) -> bool:
        """Evaluate condition based on operator."""
        if operator == '>':
            return value > threshold
        elif operator == '<':
            return value < threshold
        elif operator == '>=':
            return value >= threshold
        elif operator == '<=':
            return value <= threshold
        elif operator == '==':
            return abs(value - threshold) < 0.001  # Float comparison
        return False


class AlertManager:
    """Manage alerts and notifications."""

    def __init__(self):
        """Initialize alert manager."""
        self.rules: List[AlertRule] = []
        self.handlers: List[Callable] = []
        self.alert_history: List[Alert] = []
        self.suppression_rules: Dict[str, int] = {}  # alert_key -> count

    def add_rule(self, rule: AlertRule):
        """Add alert rule."""
        self.rules.append(rule)

    def remove_rule(self, rule_name: str):
        """Remove alert rule by name."""
        self.rules = [r for r in self.rules if r.name != rule_name]

    def add_handler(self, handler: Callable):
        """
        Add alert handler.

        Handler signature: async def handler(alert: Alert) -> None
        """
        self.handlers.append(handler)

    async def evaluate_metrics(self, endpoint: str, method: str,
                              metrics: Dict[str, float]):
        """
        Evaluate metrics and trigger alerts.

        Args:
            endpoint: RPC endpoint
            method: RPC method
            metrics: Metrics to evaluate
        """
        all_alerts = []

        for rule in self.rules:
            alerts = rule.evaluate(endpoint, method, metrics)
            all_alerts.extend(alerts)

        # Process alerts
        for alert in all_alerts:
            if self._should_suppress_alert(alert):
                continue

            self.alert_history.append(alert)
            await self._trigger_alert(alert)

    async def _trigger_alert(self, alert: Alert):
        """Trigger alert handlers."""
        tasks = [handler(alert) for handler in self.handlers]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    def _should_suppress_alert(self, alert: Alert) -> bool:
        """Check if alert should be suppressed (to avoid spam)."""
        # Simple suppression: don't send same alert more than once per minute
        alert_key = f"{alert.endpoint}_{alert.method}_{alert.metric_type.value}"

        if alert_key in self.suppression_rules:
            # For now, simple counter-based suppression
            # In production, this would check time windows
            return False

        self.suppression_rules[alert_key] = 1
        return False

    def get_alert_history(self, limit: int = 100,
                         level: Optional[AlertLevel] = None) -> List[Alert]:
        """
        Get alert history.

        Args:
            limit: Maximum number of alerts to return
            level: Filter by alert level

        Returns:
            List of alerts
        """
        alerts = self.alert_history

        if level:
            alerts = [a for a in alerts if a.level == level]

        return alerts[-limit:]

    def create_default_rules(self) -> List[AlertRule]:
        """Create default alert rules."""
        rules = [
            # High latency rule
            AlertRule(
                name="high_latency",
                description="Alert when average latency exceeds threshold",
                thresholds=[
                    AlertThreshold(
                        metric_type=MetricType.LATENCY,
                        operator='>',
                        value=1000.0,  # 1 second
                        level=AlertLevel.WARNING,
                        message_template="High latency detected on {endpoint} for {method}: {value:.2f}ms (threshold: {threshold}ms)"
                    ),
                    AlertThreshold(
                        metric_type=MetricType.LATENCY,
                        operator='>',
                        value=5000.0,  # 5 seconds
                        level=AlertLevel.CRITICAL,
                        message_template="CRITICAL: Very high latency on {endpoint} for {method}: {value:.2f}ms (threshold: {threshold}ms)"
                    )
                ]
            ),

            # Low success rate rule
            AlertRule(
                name="low_success_rate",
                description="Alert when success rate drops below threshold",
                thresholds=[
                    AlertThreshold(
                        metric_type=MetricType.SUCCESS_RATE,
                        operator='<',
                        value=95.0,
                        level=AlertLevel.WARNING,
                        message_template="Low success rate on {endpoint} for {method}: {value:.2f}% (threshold: {threshold}%)"
                    ),
                    AlertThreshold(
                        metric_type=MetricType.SUCCESS_RATE,
                        operator='<',
                        value=80.0,
                        level=AlertLevel.ERROR,
                        message_template="Very low success rate on {endpoint} for {method}: {value:.2f}% (threshold: {threshold}%)"
                    ),
                    AlertThreshold(
                        metric_type=MetricType.SUCCESS_RATE,
                        operator='<',
                        value=50.0,
                        level=AlertLevel.CRITICAL,
                        message_template="CRITICAL: Success rate severely degraded on {endpoint} for {method}: {value:.2f}% (threshold: {threshold}%)"
                    )
                ]
            ),

            # High error rate rule
            AlertRule(
                name="high_error_rate",
                description="Alert when error rate exceeds threshold",
                thresholds=[
                    AlertThreshold(
                        metric_type=MetricType.ERROR_RATE,
                        operator='>',
                        value=5.0,
                        level=AlertLevel.WARNING,
                        message_template="High error rate on {endpoint} for {method}: {value:.2f}% (threshold: {threshold}%)"
                    ),
                    AlertThreshold(
                        metric_type=MetricType.ERROR_RATE,
                        operator='>',
                        value=20.0,
                        level=AlertLevel.CRITICAL,
                        message_template="CRITICAL: Very high error rate on {endpoint} for {method}: {value:.2f}% (threshold: {threshold}%)"
                    )
                ]
            )
        ]

        return rules

    def enable_default_rules(self):
        """Enable all default alert rules."""
        for rule in self.create_default_rules():
            self.add_rule(rule)


class AlertAggregator:
    """Aggregate and summarize alerts."""

    @staticmethod
    def aggregate_by_level(alerts: List[Alert]) -> Dict[AlertLevel, List[Alert]]:
        """Group alerts by severity level."""
        aggregated = {level: [] for level in AlertLevel}

        for alert in alerts:
            aggregated[alert.level].append(alert)

        return aggregated

    @staticmethod
    def aggregate_by_endpoint(alerts: List[Alert]) -> Dict[str, List[Alert]]:
        """Group alerts by endpoint."""
        aggregated: Dict[str, List[Alert]] = {}

        for alert in alerts:
            if alert.endpoint not in aggregated:
                aggregated[alert.endpoint] = []
            aggregated[alert.endpoint].append(alert)

        return aggregated

    @staticmethod
    def aggregate_by_metric(alerts: List[Alert]) -> Dict[MetricType, List[Alert]]:
        """Group alerts by metric type."""
        aggregated = {metric: [] for metric in MetricType}

        for alert in alerts:
            aggregated[alert.metric_type].append(alert)

        return aggregated

    @staticmethod
    def generate_summary(alerts: List[Alert]) -> Dict[str, Any]:
        """Generate alert summary statistics."""
        if not alerts:
            return {
                'total': 0,
                'by_level': {},
                'by_endpoint': {},
                'by_metric': {}
            }

        by_level = AlertAggregator.aggregate_by_level(alerts)
        by_endpoint = AlertAggregator.aggregate_by_endpoint(alerts)
        by_metric = AlertAggregator.aggregate_by_metric(alerts)

        return {
            'total': len(alerts),
            'by_level': {level.value: len(alerts) for level, alerts in by_level.items() if alerts},
            'by_endpoint': {endpoint: len(alerts) for endpoint, alerts in by_endpoint.items()},
            'by_metric': {metric.value: len(alerts) for metric, alerts in by_metric.items() if alerts},
            'oldest': min(alerts, key=lambda a: a.timestamp).timestamp if alerts else None,
            'newest': max(alerts, key=lambda a: a.timestamp).timestamp if alerts else None
        }
