"""
Performance comparison and analysis for SQL Server vs Snowflake query results.
"""

import logging
from typing import Any, Dict, List

from ..utils.exceptions import ValidationError

logger = logging.getLogger(__name__)


class PerformanceComparator:
    """Compares query performance between SQL Server and Snowflake."""

    def __init__(self):
        """Initialize the performance comparator."""
        pass

    def compare_results(
        self, sqlserver_results: List[Dict[str, Any]], snowflake_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Compare execution results between SQL Server and Snowflake.

        Args:
            sqlserver_results: List of SQL Server execution results
            snowflake_results: List of Snowflake execution results

        Returns:
            Comparison dictionary with aggregated metrics
        """
        if not sqlserver_results or not snowflake_results:
            raise ValidationError("Both SQL Server and Snowflake results are required")

        # Calculate averages
        sqlserver_times = [
            r["execution_time_ms"]
            for r in sqlserver_results
            if r.get("status") == "success" and r.get("execution_time_ms")
        ]
        snowflake_times = [
            r["execution_time_ms"]
            for r in snowflake_results
            if r.get("status") == "success" and r.get("execution_time_ms")
        ]

        sqlserver_avg = sum(sqlserver_times) / len(sqlserver_times) if sqlserver_times else None
        snowflake_avg = sum(snowflake_times) / len(snowflake_times) if snowflake_times else None

        # Calculate differences
        time_difference_ms = None
        time_difference_percent = None
        performance_winner = None

        if sqlserver_avg and snowflake_avg:
            time_difference_ms = snowflake_avg - sqlserver_avg
            time_difference_percent = (time_difference_ms / sqlserver_avg) * 100

            if abs(time_difference_percent) < 1.0:
                performance_winner = "Tie"
            elif time_difference_ms < 0:
                performance_winner = "Snowflake"
            else:
                performance_winner = "SQL Server"

        # Check row count match
        sqlserver_row_count = sqlserver_results[0].get("row_count") if sqlserver_results else None
        snowflake_row_count = snowflake_results[0].get("row_count") if snowflake_results else None
        row_count_match = sqlserver_row_count == snowflake_row_count

        return {
            "sqlserver_avg_time_ms": int(sqlserver_avg) if sqlserver_avg else None,
            "snowflake_avg_time_ms": int(snowflake_avg) if snowflake_avg else None,
            "time_difference_ms": int(time_difference_ms) if time_difference_ms else None,
            "time_difference_percent": round(time_difference_percent, 2)
            if time_difference_percent
            else None,
            "row_count_match": row_count_match,
            "sqlserver_row_count": sqlserver_row_count,
            "snowflake_row_count": snowflake_row_count,
            "performance_winner": performance_winner,
        }

    def calculate_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistical metrics for execution results.

        Args:
            results: List of execution results

        Returns:
            Dictionary with min, max, median, mean, std_dev
        """
        times = [
            r["execution_time_ms"]
            for r in results
            if r.get("status") == "success" and r.get("execution_time_ms")
        ]

        if not times:
            return {}

        times_sorted = sorted(times)
        n = len(times)

        return {
            "min": min(times),
            "max": max(times),
            "mean": sum(times) / n,
            "median": times_sorted[n // 2] if n > 0 else None,
            "count": n,
        }
