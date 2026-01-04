"""
Query execution engine for SQL Server and Snowflake.
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List

from ..database.connections import SnowflakeConnection, SQLServerConnection

logger = logging.getLogger(__name__)


class QueryExecutor:
    """Executes queries on SQL Server and Snowflake platforms."""

    def __init__(
        self,
        sql_server_conn: SQLServerConnection,
        snowflake_conn: SnowflakeConnection,
        parallel_workers: int = 10,
        timeout: int = 300,
    ):
        """
        Initialize query executor.

        Args:
            sql_server_conn: SQL Server connection
            snowflake_conn: Snowflake connection
            parallel_workers: Number of parallel worker threads
            timeout: Query timeout in seconds
        """
        self.sql_server_conn = sql_server_conn
        self.snowflake_conn = snowflake_conn
        self.parallel_workers = parallel_workers
        self.timeout = timeout

    def execute_sql_server(self, query: str) -> Dict[str, Any]:
        """
        Execute query on SQL Server.

        Args:
            query: SQL query to execute

        Returns:
            Dictionary with execution results (execution_time_ms, row_count, status, etc.)
        """
        try:
            start_time = time.time()
            conn = self.sql_server_conn.connect()
            cursor = conn.cursor()

            cursor.execute(query)
            rows = cursor.fetchall()
            row_count = len(rows)

            execution_time_ms = int((time.time() - start_time) * 1000)

            return {
                "execution_time_ms": execution_time_ms,
                "row_count": row_count,
                "status": "success",
                "error_message": None,
            }
        except Exception as e:
            logger.error(f"SQL Server query execution failed: {e}")
            return {
                "execution_time_ms": None,
                "row_count": None,
                "status": "error",
                "error_message": str(e),
            }

    def execute_snowflake(self, query: str) -> Dict[str, Any]:
        """
        Execute query on Snowflake.

        Args:
            query: SQL query to execute

        Returns:
            Dictionary with execution results (execution_time_ms, row_count, status, etc.)
        """
        try:
            start_time = time.time()
            conn = self.snowflake_conn.connect()
            cursor = conn.cursor()

            cursor.execute(query)
            rows = cursor.fetchall()
            row_count = len(rows)

            execution_time_ms = int((time.time() - start_time) * 1000)

            return {
                "execution_time_ms": execution_time_ms,
                "row_count": row_count,
                "status": "success",
                "error_message": None,
            }
        except Exception as e:
            logger.error(f"Snowflake query execution failed: {e}")
            return {
                "execution_time_ms": None,
                "row_count": None,
                "status": "error",
                "error_message": str(e),
            }

    def execute_parallel(self, queries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute multiple queries in parallel.

        Args:
            queries: List of query dictionaries with 'query', 'platform', 'query_id', etc.

        Returns:
            List of execution results
        """
        results = []

        with ThreadPoolExecutor(max_workers=self.parallel_workers) as executor:
            futures = []
            for query_info in queries:
                if query_info["platform"] == "SQL Server":
                    future = executor.submit(self.execute_sql_server, query_info["query"])
                else:
                    future = executor.submit(self.execute_snowflake, query_info["query"])
                futures.append((future, query_info))

            for future, query_info in futures:
                try:
                    result = future.result(timeout=self.timeout)
                    result.update(query_info)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Parallel execution failed: {e}")
                    results.append({**query_info, "status": "error", "error_message": str(e)})

        return results
