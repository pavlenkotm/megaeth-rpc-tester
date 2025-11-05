"""
WebSocket support for RPC testing.
"""

import asyncio
import json
import time
from typing import Optional, Any, Dict, List
import aiohttp
from dataclasses import dataclass
from datetime import datetime


@dataclass
class WebSocketMessage:
    """Represents a WebSocket message."""

    id: int
    method: str
    params: List[Any]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_json(self) -> str:
        """Convert message to JSON-RPC format."""
        return json.dumps({
            "jsonrpc": "2.0",
            "id": self.id,
            "method": self.method,
            "params": self.params
        })


@dataclass
class WebSocketResponse:
    """Represents a WebSocket response."""

    id: int
    result: Optional[Any] = None
    error: Optional[Dict] = None
    latency_ms: float = 0.0
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class WebSocketTester:
    """WebSocket RPC endpoint tester."""

    def __init__(
        self,
        url: str,
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        """
        Initialize WebSocket tester.

        Args:
            url: WebSocket URL (ws:// or wss://)
            timeout: Connection timeout in seconds
            max_retries: Maximum number of connection retries
        """
        self.url = url
        self.timeout = timeout
        self.max_retries = max_retries
        self.session: Optional[aiohttp.ClientSession] = None
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.message_id = 0
        self.pending_requests: Dict[int, float] = {}
        self.responses: List[WebSocketResponse] = []

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()

    async def connect(self):
        """Establish WebSocket connection."""
        self.session = aiohttp.ClientSession()

        for attempt in range(self.max_retries):
            try:
                self.ws = await self.session.ws_connect(
                    self.url,
                    timeout=self.timeout,
                    autoping=True,
                    heartbeat=30.0
                )
                return
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise ConnectionError(f"Failed to connect to {self.url}: {str(e)}")
                await asyncio.sleep(1 * (2 ** attempt))  # Exponential backoff

    async def disconnect(self):
        """Close WebSocket connection."""
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()

    def _get_next_id(self) -> int:
        """Get next message ID."""
        self.message_id += 1
        return self.message_id

    async def send_request(
        self,
        method: str,
        params: Optional[List[Any]] = None
    ) -> WebSocketResponse:
        """
        Send a single RPC request over WebSocket.

        Args:
            method: RPC method name
            params: Method parameters

        Returns:
            WebSocketResponse object
        """
        if not self.ws or self.ws.closed:
            raise ConnectionError("WebSocket connection is not open")

        message_id = self._get_next_id()
        message = WebSocketMessage(
            id=message_id,
            method=method,
            params=params or []
        )

        start_time = time.perf_counter()
        self.pending_requests[message_id] = start_time

        try:
            # Send request
            await self.ws.send_str(message.to_json())

            # Wait for response with timeout
            async with asyncio.timeout(self.timeout):
                async for msg in self.ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)

                        if data.get("id") == message_id:
                            latency = (time.perf_counter() - start_time) * 1000

                            response = WebSocketResponse(
                                id=message_id,
                                result=data.get("result"),
                                error=data.get("error"),
                                latency_ms=latency
                            )

                            self.responses.append(response)
                            del self.pending_requests[message_id]

                            return response

                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        raise ConnectionError(f"WebSocket error: {self.ws.exception()}")

                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        raise ConnectionError("WebSocket connection closed")

        except asyncio.TimeoutError:
            if message_id in self.pending_requests:
                del self.pending_requests[message_id]
            raise TimeoutError(f"Request {message_id} timed out after {self.timeout}s")

        except Exception as e:
            if message_id in self.pending_requests:
                del self.pending_requests[message_id]
            raise

    async def send_batch(
        self,
        requests: List[tuple[str, Optional[List[Any]]]]
    ) -> List[WebSocketResponse]:
        """
        Send multiple RPC requests concurrently.

        Args:
            requests: List of (method, params) tuples

        Returns:
            List of WebSocketResponse objects
        """
        tasks = [
            self.send_request(method, params)
            for method, params in requests
        ]

        return await asyncio.gather(*tasks, return_exceptions=True)

    async def test_endpoint(
        self,
        method: str,
        params: Optional[List[Any]] = None,
        num_requests: int = 10
    ) -> List[WebSocketResponse]:
        """
        Test endpoint with multiple requests.

        Args:
            method: RPC method name
            params: Method parameters
            num_requests: Number of requests to send

        Returns:
            List of WebSocketResponse objects
        """
        results = []

        for _ in range(num_requests):
            try:
                response = await self.send_request(method, params)
                results.append(response)
            except Exception as e:
                # Create error response
                error_response = WebSocketResponse(
                    id=self._get_next_id(),
                    error={"code": -1, "message": str(e)}
                )
                results.append(error_response)

        return results

    async def subscribe(
        self,
        subscription_type: str,
        params: Optional[List[Any]] = None,
        callback: Optional[callable] = None
    ) -> str:
        """
        Subscribe to WebSocket notifications.

        Args:
            subscription_type: Type of subscription (e.g., 'newHeads')
            params: Subscription parameters
            callback: Callback function for notifications

        Returns:
            Subscription ID
        """
        # Send subscription request
        response = await self.send_request(
            "eth_subscribe",
            [subscription_type] + (params or [])
        )

        if response.error:
            raise Exception(f"Subscription failed: {response.error}")

        subscription_id = response.result

        # Start listening for notifications if callback provided
        if callback:
            asyncio.create_task(
                self._listen_for_notifications(subscription_id, callback)
            )

        return subscription_id

    async def _listen_for_notifications(
        self,
        subscription_id: str,
        callback: callable
    ):
        """Listen for subscription notifications."""
        try:
            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)

                    # Check if it's a notification for our subscription
                    if (data.get("method") == "eth_subscription" and
                        data.get("params", {}).get("subscription") == subscription_id):

                        notification_data = data["params"]["result"]
                        await callback(notification_data)

                elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                    break

        except Exception as e:
            print(f"Error in notification listener: {e}")

    async def unsubscribe(self, subscription_id: str) -> bool:
        """
        Unsubscribe from notifications.

        Args:
            subscription_id: ID of subscription to cancel

        Returns:
            True if successful
        """
        response = await self.send_request(
            "eth_unsubscribe",
            [subscription_id]
        )

        if response.error:
            raise Exception(f"Unsubscribe failed: {response.error}")

        return response.result

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics for all responses."""
        if not self.responses:
            return {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "avg_latency_ms": 0.0,
                "min_latency_ms": 0.0,
                "max_latency_ms": 0.0
            }

        successful = [r for r in self.responses if r.error is None]
        failed = [r for r in self.responses if r.error is not None]
        latencies = [r.latency_ms for r in successful]

        return {
            "total_requests": len(self.responses),
            "successful_requests": len(successful),
            "failed_requests": len(failed),
            "success_rate": len(successful) / len(self.responses) * 100,
            "avg_latency_ms": sum(latencies) / len(latencies) if latencies else 0,
            "min_latency_ms": min(latencies) if latencies else 0,
            "max_latency_ms": max(latencies) if latencies else 0
        }
