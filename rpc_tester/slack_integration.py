"""
Slack integration for RPC test notifications.

Send formatted messages to Slack channels with test results and alerts.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import aiohttp


class SlackNotifier:
    """Send notifications to Slack using webhooks."""

    def __init__(
        self,
        webhook_url: str,
        channel: Optional[str] = None,
        username: str = "RPC Tester",
        icon_emoji: str = ":rocket:",
    ):
        """
        Initialize Slack notifier.

        Args:
            webhook_url: Slack webhook URL
            channel: Override default channel (optional)
            username: Bot username
            icon_emoji: Bot icon emoji
        """
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username
        self.icon_emoji = icon_emoji

    async def send_message(self, text: str, attachments: Optional[List[Dict]] = None):
        """
        Send a message to Slack.

        Args:
            text: Message text
            attachments: Message attachments (for rich formatting)
        """
        payload = {"username": self.username, "icon_emoji": self.icon_emoji, "text": text}

        if self.channel:
            payload["channel"] = self.channel

        if attachments:
            payload["attachments"] = attachments

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status != 200:
                        print(f"Slack notification failed: {response.status}")
                        text = await response.text()
                        print(f"Response: {text}")
            except Exception as e:
                print(f"Failed to send Slack notification: {e}")

    async def send_test_results(
        self, results: Dict[str, Any], test_config: Optional[Dict[str, Any]] = None
    ):
        """
        Send test results to Slack with rich formatting.

        Args:
            results: Test results dictionary
            test_config: Test configuration (optional)
        """
        total_endpoints = len(results)
        total_tests = sum(len(methods) for methods in results.values())

        # Calculate overall success rate
        all_success_rates = []
        for methods in results.values():
            for stats in methods.values():
                all_success_rates.append(stats.get("success_rate", 0))

        avg_success_rate = (
            sum(all_success_rates) / len(all_success_rates) if all_success_rates else 0
        )

        # Determine color based on success rate
        if avg_success_rate >= 95:
            color = "good"  # Green
        elif avg_success_rate >= 80:
            color = "warning"  # Yellow
        else:
            color = "danger"  # Red

        text = f":bar_chart: *RPC Test Results Summary*"

        attachments = [
            {
                "color": color,
                "fields": [
                    {"title": "Endpoints Tested", "value": str(total_endpoints), "short": True},
                    {"title": "Total Tests", "value": str(total_tests), "short": True},
                    {
                        "title": "Average Success Rate",
                        "value": f"{avg_success_rate:.2f}%",
                        "short": True,
                    },
                    {
                        "title": "Timestamp",
                        "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "short": True,
                    },
                ],
            }
        ]

        # Add details for each endpoint
        for endpoint, methods in results.items():
            fields = []
            for method, stats in methods.items():
                latency_info = (
                    f"Avg: {stats.get('avg_latency_ms', 0):.2f}ms | "
                    f"P95: {stats.get('p95_latency_ms', 0):.2f}ms | "
                    f"P99: {stats.get('p99_latency_ms', 0):.2f}ms"
                )

                fields.append(
                    {
                        "title": f"{method}",
                        "value": (
                            f"Success: {stats.get('success_rate', 0):.1f}% | " f"{latency_info}"
                        ),
                        "short": False,
                    }
                )

            attachments.append(
                {"color": "#36a64f", "title": f":link: {endpoint}", "fields": fields}
            )

        await self.send_message(text, attachments)

    async def send_alert(
        self,
        alert_type: str,
        message: str,
        severity: str = "warning",
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Send an alert to Slack.

        Args:
            alert_type: Type of alert
            message: Alert message
            severity: Alert severity ('info', 'warning', 'error')
            details: Additional details
        """
        # Map severity to color
        color_map = {
            "info": "#36a64f",  # Green
            "warning": "#ff9900",  # Orange
            "error": "#ff0000",  # Red
        }

        # Map severity to emoji
        emoji_map = {
            "info": ":information_source:",
            "warning": ":warning:",
            "error": ":rotating_light:",
        }

        color = color_map.get(severity, "#808080")
        emoji = emoji_map.get(severity, ":bell:")

        text = f"{emoji} *RPC Tester Alert: {alert_type}*"

        fields = [
            {"title": "Message", "value": message, "short": False},
            {"title": "Severity", "value": severity.upper(), "short": True},
            {
                "title": "Timestamp",
                "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "short": True,
            },
        ]

        if details:
            for key, value in details.items():
                fields.append(
                    {"title": key.replace("_", " ").title(), "value": str(value), "short": True}
                )

        attachments = [{"color": color, "fields": fields}]

        await self.send_message(text, attachments)

    async def send_performance_degradation_alert(
        self,
        endpoint: str,
        method: str,
        current_latency: float,
        baseline_latency: float,
        threshold_percent: float,
    ):
        """
        Send performance degradation alert.

        Args:
            endpoint: RPC endpoint
            method: RPC method
            current_latency: Current latency
            baseline_latency: Baseline latency
            threshold_percent: Threshold percentage
        """
        degradation = ((current_latency - baseline_latency) / baseline_latency) * 100

        await self.send_alert(
            alert_type="Performance Degradation",
            message=f"Performance degradation detected for {method} on {endpoint}",
            severity="warning",
            details={
                "Endpoint": endpoint,
                "Method": method,
                "Current Latency": f"{current_latency:.2f}ms",
                "Baseline Latency": f"{baseline_latency:.2f}ms",
                "Degradation": f"{degradation:.2f}%",
                "Threshold": f"{threshold_percent:.2f}%",
            },
        )

    async def send_success_rate_alert(
        self, endpoint: str, method: str, success_rate: float, threshold: float
    ):
        """
        Send low success rate alert.

        Args:
            endpoint: RPC endpoint
            method: RPC method
            success_rate: Current success rate
            threshold: Success rate threshold
        """
        await self.send_alert(
            alert_type="Low Success Rate",
            message=f"Success rate below threshold for {method} on {endpoint}",
            severity="error",
            details={
                "Endpoint": endpoint,
                "Method": method,
                "Success Rate": f"{success_rate:.2f}%",
                "Threshold": f"{threshold:.2f}%",
            },
        )


class SlackFormatter:
    """Format test data for Slack messages."""

    @staticmethod
    def format_comparison_results(comparisons: List[Dict[str, Any]]) -> str:
        """
        Format endpoint comparison results for Slack.

        Args:
            comparisons: List of comparison results

        Returns:
            Formatted message
        """
        if not comparisons:
            return "No comparison data available"

        lines = ["*Endpoint Comparison Results*\n"]

        for comp in comparisons:
            endpoint = comp.get("endpoint", "Unknown")
            rank = comp.get("rank", 0)
            score = comp.get("score", 0)

            lines.append(f"{rank}. *{endpoint}*")
            lines.append(f"   Score: {score:.2f}")
            lines.append(f"   Avg Latency: {comp.get('avg_latency', 0):.2f}ms")
            lines.append(f"   Success Rate: {comp.get('success_rate', 0):.2f}%")
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def format_test_summary(summary: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Format test summary as Slack attachment fields.

        Args:
            summary: Test summary dictionary

        Returns:
            List of Slack fields
        """
        fields = []

        if "total_requests" in summary:
            fields.append(
                {"title": "Total Requests", "value": str(summary["total_requests"]), "short": True}
            )

        if "successful_requests" in summary:
            fields.append(
                {"title": "Successful", "value": str(summary["successful_requests"]), "short": True}
            )

        if "failed_requests" in summary:
            fields.append(
                {"title": "Failed", "value": str(summary["failed_requests"]), "short": True}
            )

        if "avg_latency_ms" in summary:
            fields.append(
                {
                    "title": "Average Latency",
                    "value": f"{summary['avg_latency_ms']:.2f}ms",
                    "short": True,
                }
            )

        return fields
