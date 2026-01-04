"""
Shared test fixtures and configuration for pytest.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


@pytest.fixture
def sample_config():
    """Provide a sample configuration dictionary for testing."""
    return {
        "version": "1.0",
        "connections": {
            "sql_server_test_run": {"server": "localhost", "database": "TestRunDB", "port": 1433},
            "sql_server_test_target": {
                "server": "localhost",
                "database": "TestTargetDB",
                "port": 1433,
            },
            "snowflake": {
                "account": "test_account",
                "warehouse": "TEST_WH",
                "database": "TEST_DB",
                "schema": "PUBLIC",
            },
        },
        "execution": {"parallel_workers": 5, "repeat_count": 3},
        "ui": {"framework": "tkinter"},
        "logging": {"level": "DEBUG", "file_enabled": False, "console_enabled": True},
    }


@pytest.fixture
def mock_sql_server_connection():
    """Mock SQL Server connection for testing."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


@pytest.fixture
def mock_snowflake_connection():
    """Mock Snowflake connection for testing."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


@pytest.fixture
def sample_sql_server_query():
    """Sample SQL Server query for testing."""
    return "SELECT TOP 10 * FROM users WHERE LEN(name) > 5"


@pytest.fixture
def sample_snowflake_query():
    """Sample Snowflake query for testing."""
    return "SELECT * FROM users WHERE LENGTH(name) > 5 LIMIT 10"


@pytest.fixture
def sample_execution_result():
    """Sample query execution result for testing."""
    return {"execution_time_ms": 150, "row_count": 10, "status": "success", "error_message": None}
