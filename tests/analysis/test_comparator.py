"""
Unit tests for performance comparator.
"""

import pytest

from src.analysis.comparator import PerformanceComparator
from src.utils.exceptions import ValidationError


class TestPerformanceComparator:
    """Test PerformanceComparator functionality."""

    @pytest.fixture
    def comparator(self):
        """Create a PerformanceComparator instance."""
        return PerformanceComparator()

    @pytest.fixture
    def sample_sqlserver_results(self):
        """Sample SQL Server execution results."""
        return [
            {"execution_time_ms": 100, "row_count": 10, "status": "success"},
            {"execution_time_ms": 110, "row_count": 10, "status": "success"},
            {"execution_time_ms": 90, "row_count": 10, "status": "success"},
        ]

    @pytest.fixture
    def sample_snowflake_results(self):
        """Sample Snowflake execution results."""
        return [
            {"execution_time_ms": 80, "row_count": 10, "status": "success"},
            {"execution_time_ms": 85, "row_count": 10, "status": "success"},
            {"execution_time_ms": 75, "row_count": 10, "status": "success"},
        ]

    def test_compare_results_basic(
        self, comparator, sample_sqlserver_results, sample_snowflake_results
    ):
        """Test basic comparison of results."""
        result = comparator.compare_results(sample_sqlserver_results, sample_snowflake_results)

        assert "sqlserver_avg_time_ms" in result
        assert "snowflake_avg_time_ms" in result
        assert "time_difference_ms" in result
        assert "time_difference_percent" in result
        assert "row_count_match" in result
        assert "performance_winner" in result

    def test_compare_results_calculates_averages(
        self, comparator, sample_sqlserver_results, sample_snowflake_results
    ):
        """Test that averages are calculated correctly."""
        result = comparator.compare_results(sample_sqlserver_results, sample_snowflake_results)

        # SQL Server average: (100 + 110 + 90) / 3 = 100
        assert result["sqlserver_avg_time_ms"] == 100
        # Snowflake average: (80 + 85 + 75) / 3 = 80
        assert result["snowflake_avg_time_ms"] == 80

    def test_compare_results_determines_winner(
        self, comparator, sample_sqlserver_results, sample_snowflake_results
    ):
        """Test that performance winner is determined correctly."""
        result = comparator.compare_results(sample_sqlserver_results, sample_snowflake_results)

        # Snowflake is faster (80ms vs 100ms)
        assert result["performance_winner"] == "Snowflake"

    def test_compare_results_row_count_match(
        self, comparator, sample_sqlserver_results, sample_snowflake_results
    ):
        """Test row count matching."""
        result = comparator.compare_results(sample_sqlserver_results, sample_snowflake_results)

        # Both have row_count of 10
        assert result["row_count_match"] is True

    def test_compare_results_empty_lists(self, comparator):
        """Test that empty results raise ValidationError."""
        with pytest.raises(ValidationError):
            comparator.compare_results([], [])

    def test_calculate_statistics(self, comparator):
        """Test statistical calculation."""
        results = [
            {"execution_time_ms": 100, "status": "success"},
            {"execution_time_ms": 110, "status": "success"},
            {"execution_time_ms": 90, "status": "success"},
            {"execution_time_ms": 120, "status": "success"},
            {"execution_time_ms": 80, "status": "success"},
        ]

        stats = comparator.calculate_statistics(results)

        assert "min" in stats
        assert "max" in stats
        assert "mean" in stats
        assert "median" in stats
        assert "count" in stats
        assert stats["min"] == 80
        assert stats["max"] == 120
        assert stats["count"] == 5
