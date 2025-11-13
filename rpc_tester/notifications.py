"""
Notification system for sending alerts about test results.

Supports email and webhook notifications for test completion and alerts.
"""

import asyncio
import json
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, List, Optional

import aiohttp


class EmailNotifier:
    """Send email notifications for test results."""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int = 587,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = True,
    ):
        """
        Initialize email notifier.

        Args:
            smtp_host: SMTP server hostname
            smtp_port: SMTP server port
            username: SMTP username
            password: SMTP password
            use_tls: Whether to use TLS encryption
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    async def send_test_completion(self, recipient: str, subject: str, results: Dict[str, Any]):
        """
        Send test completion notification.

        Args:
            recipient: Email recipient address
            subject: Email subject
            results: Test results dictionary
        """
        body = self._format_results_email(results)
        await self._send_email(recipient, subject, body)

    async def send_alert(
        self,
        recipient: str,
        alert_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Send alert notification.

        Args:
            recipient: Email recipient address
            alert_type: Type of alert (e.g., 'high_latency', 'low_success_rate')
            message: Alert message
            details: Additional alert details
        """
        subject = f"RPC Tester Alert: {alert_type}"
        body = f"""
RPC Tester Alert
================

Alert Type: {alert_type}
Timestamp: {datetime.now().isoformat()}

Message:
{message}

"""
        if details:
            body += f"\nDetails:\n{json.dumps(details, indent=2)}\n"

        await self._send_email(recipient, subject, body)

    def _format_results_email(self, results: Dict[str, Any]) -> str:
        """Format test results as email body."""
        body = """
MegaETH RPC Tester - Test Results
==================================

"""
        for endpoint, methods in results.items():
            body += f"\nEndpoint: {endpoint}\n"
            body += "-" * 50 + "\n"

            for method, stats in methods.items():
                body += f"\nMethod: {method}\n"
                body += f"  Total Requests: {stats.get('total_requests', 0)}\n"
                body += f"  Success Rate: {stats.get('success_rate', 0):.2f}%\n"
                body += f"  Avg Latency: {stats.get('avg_latency_ms', 0):.2f}ms\n"
                body += f"  P95 Latency: {stats.get('p95_latency_ms', 0):.2f}ms\n"
                body += f"  P99 Latency: {stats.get('p99_latency_ms', 0):.2f}ms\n"

        return body

    async def _send_email(self, recipient: str, subject: str, body: str):
        """Send email using SMTP."""
        msg = MIMEMultipart()
        msg["From"] = self.username or "rpc-tester@localhost"
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Run SMTP operations in thread pool to avoid blocking
        await asyncio.get_event_loop().run_in_executor(None, self._smtp_send, recipient, msg)

    def _smtp_send(self, recipient: str, msg: MIMEMultipart):
        """Send email via SMTP (blocking operation)."""
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                if self.username and self.password:
                    server.login(self.username, self.password)
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email: {e}")


class WebhookNotifier:
    """Send webhook notifications for test results."""

    def __init__(self, webhook_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Initialize webhook notifier.

        Args:
            webhook_url: Webhook URL
            headers: Additional HTTP headers
        """
        self.webhook_url = webhook_url
        self.headers = headers or {}

    async def send_notification(self, payload: Dict[str, Any]):
        """
        Send notification to webhook.

        Args:
            payload: Notification payload
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    self.webhook_url, json=payload, headers=self.headers
                ) as response:
                    if response.status >= 400:
                        print(f"Webhook notification failed: {response.status}")
            except Exception as e:
                print(f"Failed to send webhook notification: {e}")

    async def send_test_completion(self, results: Dict[str, Any]):
        """
        Send test completion notification.

        Args:
            results: Test results dictionary
        """
        payload = {
            "event": "test_completion",
            "timestamp": datetime.now().isoformat(),
            "results": results,
        }
        await self.send_notification(payload)

    async def send_alert(
        self, alert_type: str, message: str, details: Optional[Dict[str, Any]] = None
    ):
        """
        Send alert notification.

        Args:
            alert_type: Type of alert
            message: Alert message
            details: Additional alert details
        """
        payload = {
            "event": "alert",
            "alert_type": alert_type,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details or {},
        }
        await self.send_notification(payload)


class NotificationManager:
    """Manage multiple notification channels."""

    def __init__(self):
        """Initialize notification manager."""
        self.notifiers: List[Any] = []

    def add_email_notifier(
        self,
        smtp_host: str,
        smtp_port: int = 587,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """Add email notifier."""
        notifier = EmailNotifier(smtp_host, smtp_port, username, password)
        self.notifiers.append(notifier)
        return notifier

    def add_webhook_notifier(self, webhook_url: str, headers: Optional[Dict[str, str]] = None):
        """Add webhook notifier."""
        notifier = WebhookNotifier(webhook_url, headers)
        self.notifiers.append(notifier)
        return notifier

    async def notify_test_completion(
        self, results: Dict[str, Any], email_recipients: Optional[List[str]] = None
    ):
        """
        Notify all channels about test completion.

        Args:
            results: Test results dictionary
            email_recipients: List of email recipients (for email notifiers)
        """
        tasks = []

        for notifier in self.notifiers:
            if isinstance(notifier, EmailNotifier) and email_recipients:
                for recipient in email_recipients:
                    tasks.append(
                        notifier.send_test_completion(recipient, "RPC Test Results", results)
                    )
            elif isinstance(notifier, WebhookNotifier):
                tasks.append(notifier.send_test_completion(results))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def notify_alert(
        self,
        alert_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        email_recipients: Optional[List[str]] = None,
    ):
        """
        Notify all channels about an alert.

        Args:
            alert_type: Type of alert
            message: Alert message
            details: Additional alert details
            email_recipients: List of email recipients (for email notifiers)
        """
        tasks = []

        for notifier in self.notifiers:
            if isinstance(notifier, EmailNotifier) and email_recipients:
                for recipient in email_recipients:
                    tasks.append(notifier.send_alert(recipient, alert_type, message, details))
            elif isinstance(notifier, WebhookNotifier):
                tasks.append(notifier.send_alert(alert_type, message, details))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
