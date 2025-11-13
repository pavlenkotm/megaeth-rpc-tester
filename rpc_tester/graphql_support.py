"""
GraphQL support for testing GraphQL endpoints.

Extends RPC tester to support GraphQL queries and mutations.
"""

import asyncio
import json
import time
from typing import Any, Dict, List, Optional

import aiohttp


class GraphQLClient:
    """Client for making GraphQL requests."""

    def __init__(
        self, endpoint: str, headers: Optional[Dict[str, str]] = None, timeout: float = 30.0
    ):
        """
        Initialize GraphQL client.

        Args:
            endpoint: GraphQL endpoint URL
            headers: Additional HTTP headers
            timeout: Request timeout in seconds
        """
        self.endpoint = endpoint
        self.headers = headers or {}
        self.timeout = timeout

    async def execute(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute GraphQL query or mutation.

        Args:
            query: GraphQL query string
            variables: Query variables
            operation_name: Operation name (optional)

        Returns:
            Response data
        """
        payload = {"query": query}

        if variables:
            payload["variables"] = variables

        if operation_name:
            payload["operationName"] = operation_name

        start_time = time.time()

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    self.endpoint,
                    json=payload,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    latency = (time.time() - start_time) * 1000  # ms

                    if response.status != 200:
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}",
                            "latency_ms": latency,
                        }

                    data = await response.json()

                    return {
                        "success": "errors" not in data,
                        "data": data.get("data"),
                        "errors": data.get("errors", []),
                        "latency_ms": latency,
                    }

            except asyncio.TimeoutError:
                latency = (time.time() - start_time) * 1000
                return {"success": False, "error": "Timeout", "latency_ms": latency}
            except Exception as e:
                latency = (time.time() - start_time) * 1000
                return {"success": False, "error": str(e), "latency_ms": latency}


class GraphQLTester:
    """Test GraphQL endpoints with performance metrics."""

    def __init__(self, endpoint: str, headers: Optional[Dict[str, str]] = None):
        """
        Initialize GraphQL tester.

        Args:
            endpoint: GraphQL endpoint URL
            headers: Additional HTTP headers
        """
        self.endpoint = endpoint
        self.client = GraphQLClient(endpoint, headers)

    async def test_query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        num_requests: int = 10,
        concurrent: int = 5,
    ) -> Dict[str, Any]:
        """
        Test a GraphQL query with performance metrics.

        Args:
            query: GraphQL query string
            variables: Query variables
            num_requests: Number of requests to make
            concurrent: Number of concurrent requests

        Returns:
            Test results with metrics
        """
        semaphore = asyncio.Semaphore(concurrent)

        async def make_request():
            async with semaphore:
                return await self.client.execute(query, variables)

        # Execute requests
        tasks = [make_request() for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)

        # Calculate metrics
        successful = sum(1 for r in results if r.get("success", False))
        failed = num_requests - successful
        latencies = [r["latency_ms"] for r in results]

        return {
            "endpoint": self.endpoint,
            "query": query[:100] + "..." if len(query) > 100 else query,
            "total_requests": num_requests,
            "successful_requests": successful,
            "failed_requests": failed,
            "success_rate": (successful / num_requests * 100) if num_requests > 0 else 0,
            "avg_latency_ms": sum(latencies) / len(latencies) if latencies else 0,
            "min_latency_ms": min(latencies) if latencies else 0,
            "max_latency_ms": max(latencies) if latencies else 0,
            "p50_latency_ms": self._percentile(latencies, 50),
            "p95_latency_ms": self._percentile(latencies, 95),
            "p99_latency_ms": self._percentile(latencies, 99),
            "errors": [r.get("errors", []) for r in results if not r.get("success", False)],
        }

    async def test_multiple_queries(
        self, queries: List[Dict[str, Any]], num_requests: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Test multiple GraphQL queries.

        Args:
            queries: List of query configurations
                    Each item: {'query': str, 'variables': dict, 'name': str}
            num_requests: Number of requests per query

        Returns:
            List of test results
        """
        results = []

        for query_config in queries:
            query = query_config["query"]
            variables = query_config.get("variables")
            name = query_config.get("name", "Unnamed Query")

            result = await self.test_query(query, variables, num_requests)
            result["query_name"] = name
            results.append(result)

        return results

    @staticmethod
    def _percentile(data: List[float], percentile: float) -> float:
        """Calculate percentile."""
        if not data:
            return 0

        sorted_data = sorted(data)
        index = (len(sorted_data) - 1) * (percentile / 100)
        lower = int(index)
        upper = lower + 1

        if upper >= len(sorted_data):
            return sorted_data[-1]

        weight = index - lower
        return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight


class GraphQLQueryBuilder:
    """Helper to build common GraphQL queries."""

    @staticmethod
    def introspection_query() -> str:
        """Get introspection query for schema exploration."""
        return """
            query IntrospectionQuery {
                __schema {
                    queryType { name }
                    mutationType { name }
                    subscriptionType { name }
                    types {
                        name
                        kind
                        description
                    }
                }
            }
        """

    @staticmethod
    def health_check_query(field: str = "__schema") -> str:
        """
        Simple health check query.

        Args:
            field: Field to query

        Returns:
            GraphQL query string
        """
        return f"""
            query HealthCheck {{
                {field} {{
                    queryType {{
                        name
                    }}
                }}
            }}
        """

    @staticmethod
    def build_query(
        query_type: str, fields: List[str], filters: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Build a simple GraphQL query.

        Args:
            query_type: Query type name
            fields: List of fields to query
            filters: Query filters

        Returns:
            GraphQL query string
        """
        fields_str = "\n        ".join(fields)

        if filters:
            filter_args = ", ".join(f"{k}: {json.dumps(v)}" for k, v in filters.items())
            query = f"""
                query {{
                    {query_type}({filter_args}) {{
                        {fields_str}
                    }}
                }}
            """
        else:
            query = f"""
                query {{
                    {query_type} {{
                        {fields_str}
                    }}
                }}
            """

        return query


class GraphQLBenchmark:
    """Benchmark GraphQL endpoints."""

    def __init__(self, endpoints: List[str], headers: Optional[Dict[str, str]] = None):
        """
        Initialize GraphQL benchmark.

        Args:
            endpoints: List of GraphQL endpoints to test
            headers: Additional HTTP headers
        """
        self.endpoints = endpoints
        self.headers = headers
        self.testers = [GraphQLTester(ep, headers) for ep in endpoints]

    async def benchmark_query(
        self, query: str, variables: Optional[Dict[str, Any]] = None, num_requests: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Benchmark a query across all endpoints.

        Args:
            query: GraphQL query string
            variables: Query variables
            num_requests: Number of requests per endpoint

        Returns:
            List of results per endpoint
        """
        tasks = []
        for tester in self.testers:
            tasks.append(tester.test_query(query, variables, num_requests))

        results = await asyncio.gather(*tasks)
        return results

    async def compare_endpoints(self, query: str, num_requests: int = 10) -> Dict[str, Any]:
        """
        Compare endpoints for a specific query.

        Args:
            query: GraphQL query string
            num_requests: Number of requests per endpoint

        Returns:
            Comparison results
        """
        results = await self.benchmark_query(query, num_requests=num_requests)

        # Find fastest endpoint
        fastest = min(results, key=lambda x: x["avg_latency_ms"])
        most_reliable = max(results, key=lambda x: x["success_rate"])

        return {
            "query": query[:100] + "..." if len(query) > 100 else query,
            "total_endpoints": len(self.endpoints),
            "results": results,
            "fastest_endpoint": {
                "url": fastest["endpoint"],
                "avg_latency_ms": fastest["avg_latency_ms"],
            },
            "most_reliable_endpoint": {
                "url": most_reliable["endpoint"],
                "success_rate": most_reliable["success_rate"],
            },
        }


class GraphQLLoadTester:
    """Load testing for GraphQL endpoints."""

    def __init__(self, endpoint: str, headers: Optional[Dict[str, str]] = None):
        """
        Initialize load tester.

        Args:
            endpoint: GraphQL endpoint URL
            headers: Additional HTTP headers
        """
        self.client = GraphQLClient(endpoint, headers)
        self.endpoint = endpoint

    async def ramp_up_test(
        self,
        query: str,
        start_rps: int = 1,
        end_rps: int = 100,
        step: int = 10,
        step_duration: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Perform ramp-up load test.

        Args:
            query: GraphQL query to test
            start_rps: Starting requests per second
            end_rps: Ending requests per second
            step: RPS increment per step
            step_duration: Duration of each step in seconds

        Returns:
            Results for each step
        """
        results = []

        for rps in range(start_rps, end_rps + 1, step):
            print(f"Testing at {rps} RPS...")

            num_requests = rps * step_duration
            interval = 1.0 / rps

            latencies = []
            successful = 0

            for i in range(num_requests):
                start = time.time()
                result = await self.client.execute(query)

                if result.get("success", False):
                    successful += 1

                latencies.append(result["latency_ms"])

                # Wait to maintain target RPS
                elapsed = time.time() - start
                sleep_time = max(0, interval - elapsed)
                await asyncio.sleep(sleep_time)

            results.append(
                {
                    "rps": rps,
                    "total_requests": num_requests,
                    "successful_requests": successful,
                    "success_rate": (successful / num_requests * 100) if num_requests > 0 else 0,
                    "avg_latency_ms": sum(latencies) / len(latencies) if latencies else 0,
                    "max_latency_ms": max(latencies) if latencies else 0,
                    "p95_latency_ms": GraphQLTester._percentile(latencies, 95),
                }
            )

        return results
