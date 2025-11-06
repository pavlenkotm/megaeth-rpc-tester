"""
Database integration module for storing test results.

Supports SQLite and PostgreSQL for persistent storage of RPC test results.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import asyncio
from contextlib import asynccontextmanager


class DatabaseManager:
    """Manages database operations for RPC test results."""

    def __init__(self, db_path: str = "rpc_test_results.db", db_type: str = "sqlite"):
        """
        Initialize database manager.

        Args:
            db_path: Path to database file (SQLite) or connection string (PostgreSQL)
            db_type: Type of database ('sqlite' or 'postgresql')
        """
        self.db_path = db_path
        self.db_type = db_type
        self.connection = None

    async def initialize(self):
        """Initialize database and create tables."""
        if self.db_type == "sqlite":
            await self._init_sqlite()
        elif self.db_type == "postgresql":
            await self._init_postgresql()
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    async def _init_sqlite(self):
        """Initialize SQLite database."""
        self.connection = sqlite3.connect(self.db_path)
        cursor = self.connection.cursor()

        # Create test_runs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                config TEXT,
                total_endpoints INTEGER,
                total_methods INTEGER,
                total_requests INTEGER,
                duration_seconds REAL
            )
        """)

        # Create test_results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                endpoint TEXT NOT NULL,
                method TEXT NOT NULL,
                total_requests INTEGER,
                successful_requests INTEGER,
                failed_requests INTEGER,
                success_rate REAL,
                avg_latency_ms REAL,
                min_latency_ms REAL,
                max_latency_ms REAL,
                p50_latency_ms REAL,
                p95_latency_ms REAL,
                p99_latency_ms REAL,
                errors TEXT,
                FOREIGN KEY (run_id) REFERENCES test_runs(id)
            )
        """)

        # Create performance_metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                result_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                latency_ms REAL,
                status TEXT,
                error_message TEXT,
                FOREIGN KEY (result_id) REFERENCES test_results(id)
            )
        """)

        self.connection.commit()

    async def _init_postgresql(self):
        """Initialize PostgreSQL database (placeholder for future implementation)."""
        # This will be implemented when asyncpg is added to requirements
        raise NotImplementedError("PostgreSQL support coming soon")

    async def save_test_run(self, config: Dict[str, Any], metadata: Dict[str, Any]) -> int:
        """
        Save a test run record.

        Args:
            config: Test configuration
            metadata: Test run metadata

        Returns:
            Test run ID
        """
        if self.db_type == "sqlite":
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO test_runs (
                    timestamp, config, total_endpoints, total_methods,
                    total_requests, duration_seconds
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                json.dumps(config),
                metadata.get('total_endpoints', 0),
                metadata.get('total_methods', 0),
                metadata.get('total_requests', 0),
                metadata.get('duration_seconds', 0.0)
            ))
            self.connection.commit()
            return cursor.lastrowid

        return -1

    async def save_test_result(self, run_id: int, endpoint: str, method: str,
                               results: Dict[str, Any]):
        """
        Save individual test results.

        Args:
            run_id: Test run ID
            endpoint: RPC endpoint URL
            method: RPC method name
            results: Test results dictionary
        """
        if self.db_type == "sqlite":
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO test_results (
                    run_id, endpoint, method, total_requests,
                    successful_requests, failed_requests, success_rate,
                    avg_latency_ms, min_latency_ms, max_latency_ms,
                    p50_latency_ms, p95_latency_ms, p99_latency_ms, errors
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                run_id, endpoint, method,
                results.get('total_requests', 0),
                results.get('successful_requests', 0),
                results.get('failed_requests', 0),
                results.get('success_rate', 0.0),
                results.get('avg_latency_ms', 0.0),
                results.get('min_latency_ms', 0.0),
                results.get('max_latency_ms', 0.0),
                results.get('p50_latency_ms', 0.0),
                results.get('p95_latency_ms', 0.0),
                results.get('p99_latency_ms', 0.0),
                json.dumps(results.get('errors', []))
            ))
            self.connection.commit()

    async def get_test_history(self, endpoint: Optional[str] = None,
                               limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get test history.

        Args:
            endpoint: Filter by endpoint (optional)
            limit: Maximum number of records to return

        Returns:
            List of test run records
        """
        if self.db_type == "sqlite":
            cursor = self.connection.cursor()

            if endpoint:
                cursor.execute("""
                    SELECT DISTINCT tr.* FROM test_runs tr
                    JOIN test_results res ON tr.id = res.run_id
                    WHERE res.endpoint = ?
                    ORDER BY tr.timestamp DESC
                    LIMIT ?
                """, (endpoint, limit))
            else:
                cursor.execute("""
                    SELECT * FROM test_runs
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

        return []

    async def get_endpoint_statistics(self, endpoint: str,
                                     days: int = 7) -> Dict[str, Any]:
        """
        Get statistics for an endpoint over time.

        Args:
            endpoint: RPC endpoint URL
            days: Number of days to analyze

        Returns:
            Statistics dictionary
        """
        if self.db_type == "sqlite":
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT
                    method,
                    AVG(avg_latency_ms) as avg_latency,
                    AVG(success_rate) as avg_success_rate,
                    COUNT(*) as test_count
                FROM test_results
                WHERE endpoint = ?
                AND run_id IN (
                    SELECT id FROM test_runs
                    WHERE datetime(timestamp) > datetime('now', '-' || ? || ' days')
                )
                GROUP BY method
            """, (endpoint, days))

            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return {
                'endpoint': endpoint,
                'period_days': days,
                'methods': results
            }

        return {}

    async def close(self):
        """Close database connection."""
        if self.connection:
            if self.db_type == "sqlite":
                self.connection.close()


@asynccontextmanager
async def get_db_manager(db_path: str = "rpc_test_results.db",
                         db_type: str = "sqlite"):
    """
    Context manager for database operations.

    Args:
        db_path: Path to database file
        db_type: Type of database

    Yields:
        DatabaseManager instance
    """
    manager = DatabaseManager(db_path, db_type)
    await manager.initialize()
    try:
        yield manager
    finally:
        await manager.close()
