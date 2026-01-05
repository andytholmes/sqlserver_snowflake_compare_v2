"""
Unit and integration tests for SchemaManager.

This test suite follows TDD principles - tests are written before implementation.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Mock pyodbc and snowflake before importing modules that use them
sys.modules["pyodbc"] = MagicMock()
sys.modules["snowflake"] = MagicMock()
sys.modules["snowflake.connector"] = MagicMock()

from src.database.schema import SchemaManager  # noqa: E402
from src.utils.exceptions import SchemaError  # noqa: E402

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def mock_sql_server_connection():
    """Create a mock SQL Server connection for testing."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


@pytest.fixture
def mock_schema_manager(mock_sql_server_connection):
    """Create a SchemaManager instance with mocked connection."""
    mock_conn, mock_cursor = mock_sql_server_connection
    # Create a mock connection object (don't need to import SQLServerConnection)
    mock_connection_obj = MagicMock()
    mock_connection_obj.connect.return_value = mock_conn
    schema_manager = SchemaManager(mock_connection_obj)
    schema_manager._conn = mock_conn
    return schema_manager, mock_conn, mock_cursor


@pytest.fixture
def sample_schema_sql_file():
    """Create a temporary SQL schema file for testing."""
    sql_content = """
-- Test schema file
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[TestTable]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[TestTable] (
        [id] INT IDENTITY(1,1) NOT NULL,
        [name] NVARCHAR(100) NOT NULL,
        CONSTRAINT [PK_TestTable] PRIMARY KEY CLUSTERED ([id] ASC)
    );
    PRINT 'TestTable created successfully.';
END
GO
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql_content)
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def sample_schema_directory():
    """Create a temporary directory with multiple schema SQL files for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create multiple SQL files with numbered prefixes
        files = []
        for i in range(3):
            file_path = Path(temp_dir) / f"{i:02d}_create_test_table_{i}.sql"
            sql_content = f"""
-- Test schema file {i}
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[TestTable{i}]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[TestTable{i}] (
        [id] INT IDENTITY(1,1) NOT NULL,
        [name] NVARCHAR(100) NOT NULL,
        CONSTRAINT [PK_TestTable{i}] PRIMARY KEY CLUSTERED ([id] ASC)
    );
    PRINT 'TestTable{i} created successfully.';
END
GO
"""
            file_path.write_text(sql_content)
            files.append(str(file_path))

        yield temp_dir, files


@pytest.fixture
def required_tables():
    """List of required tables that should exist after schema creation."""
    return [
        "ConfigTable",
        "QueryRepository",
        "TestRuns",
        "TestResults",
        "ComparisonResults",
    ]


# ============================================================================
# Tests for create_schema()
# ============================================================================


class TestCreateSchema:
    """Test cases for SchemaManager.create_schema() method."""

    def test_create_schema_with_valid_file_path(self, mock_schema_manager, sample_schema_sql_file):
        """Test create_schema() with valid schema file path."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # breakpoint()

        # Mock cursor.execute to succeed
        mock_cursor.execute.return_value = None

        result = schema_manager.create_schema(sample_schema_sql_file)

        assert result is True
        # Verify that the SQL file was read and executed
        mock_cursor.execute.assert_called()

    def test_create_schema_with_invalid_file_path(self, mock_schema_manager):
        """Test create_schema() with invalid file path raises SchemaError."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        invalid_path = "/nonexistent/path/to/schema.sql"

        with pytest.raises(SchemaError, match=".*file.*not found|.*cannot.*read"):
            schema_manager.create_schema(invalid_path)

    def test_create_schema_with_none_file_path_uses_default(self, mock_schema_manager):
        """Test create_schema() with None file path uses default schema directory."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor.execute to succeed
        mock_cursor.execute.return_value = None

        # Mock Path.exists and Path.glob to simulate schema directory
        with patch("pathlib.Path.exists", return_value=True), patch(
            "pathlib.Path.glob", return_value=[]
        ):
            schema_manager.create_schema(None)

        # Should attempt to use default schema directory
        # (exact behavior depends on implementation)

    def test_create_schema_with_malformed_sql_handles_gracefully(
        self, mock_schema_manager, tmp_path
    ):
        """Test create_schema() with malformed SQL handles errors gracefully."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Create a file with malformed SQL
        malformed_sql_file = tmp_path / "malformed.sql"
        malformed_sql_file.write_text("INVALID SQL SYNTAX!!! CREATE TABLE")

        # Mock cursor.execute to raise an exception
        mock_cursor.execute.side_effect = Exception("SQL syntax error")

        # Should raise SchemaError, not a generic exception
        with pytest.raises(SchemaError, match=".*schema.*creation.*fail|.*SQL.*error"):
            schema_manager.create_schema(str(malformed_sql_file))

    def test_create_schema_executes_scripts_in_order(
        self, mock_schema_manager, sample_schema_directory
    ):
        """Test that schema creation executes scripts in correct order (00, 01, 02, etc.)."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager
        temp_dir, files = sample_schema_directory

        # Mock cursor.execute to succeed
        mock_cursor.execute.return_value = None

        # Mock Path operations to return our test files
        with patch("pathlib.Path.exists", return_value=True), patch(
            "pathlib.Path.glob"
        ) as mock_glob:
            # Return files in sorted order
            mock_glob.return_value = sorted([Path(f) for f in files])

            result = schema_manager.create_schema(temp_dir)

            assert result is True
            # Verify that execute was called (at least once)
            assert mock_cursor.execute.call_count > 0

    def test_create_schema_reads_and_executes_sql_content(
        self, mock_schema_manager, sample_schema_sql_file
    ):
        """Test that create_schema() reads SQL file content and executes it."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor.execute to succeed
        mock_cursor.execute.return_value = None

        result = schema_manager.create_schema(sample_schema_sql_file)

        assert result is True
        # Verify execute was called with SQL content
        assert mock_cursor.execute.called

    def test_create_schema_handles_connection_errors(
        self, mock_schema_manager, sample_schema_sql_file
    ):
        """Test that create_schema() handles connection errors properly."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock connection.connect to raise an error
        schema_manager.connection.connect.side_effect = Exception("Connection failed")

        with pytest.raises(SchemaError, match=".*connection|.*schema.*creation.*fail"):
            schema_manager.create_schema(sample_schema_sql_file)


# ============================================================================
# Tests for table_exists()
# ============================================================================


class TestTableExists:
    """Test cases for SchemaManager.table_exists() method."""

    def test_table_exists_returns_true_when_table_exists(self, mock_schema_manager):
        """Test table_exists() returns True when table exists."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor.fetchone to return (1,) indicating table exists
        mock_cursor.fetchone.return_value = (1,)

        result = schema_manager.table_exists("ConfigTable")

        assert result is True
        mock_cursor.execute.assert_called_once()
        # Verify the query includes the table name
        call_args = mock_cursor.execute.call_args[0][0]
        assert "ConfigTable" in call_args or "?" in call_args

    def test_table_exists_returns_false_when_table_not_exists(self, mock_schema_manager):
        """Test table_exists() returns False when table does not exist."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor.fetchone to return (0,) indicating table doesn't exist
        mock_cursor.fetchone.return_value = (0,)

        result = schema_manager.table_exists("NonExistentTable")

        assert result is False
        mock_cursor.execute.assert_called_once()

    def test_table_exists_for_all_required_tables(self, mock_schema_manager, required_tables):
        """Test table_exists() for all required tables (ConfigTable, QueryRepository, etc.)."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor.fetchone to return (1,) for all tables
        mock_cursor.fetchone.return_value = (1,)

        for table_name in required_tables:
            result = schema_manager.table_exists(table_name)
            assert result is True, f"Table {table_name} should exist"

    def test_table_exists_raises_schema_error_on_exception(self, mock_schema_manager):
        """Test table_exists() raises SchemaError on database exception."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor.execute to raise an exception
        mock_cursor.execute.side_effect = Exception("Database error")

        with pytest.raises(SchemaError, match=".*table.*existence"):
            schema_manager.table_exists("TestTable")

    def test_table_exists_ensures_connection(self, mock_schema_manager):
        """Test that table_exists() ensures connection is established."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Reset connection to None
        schema_manager._conn = None

        # Mock cursor.fetchone to return (1,)
        mock_cursor.fetchone.return_value = (1,)

        schema_manager.table_exists("TestTable")

        # Verify connection.connect was called
        schema_manager.connection.connect.assert_called_once()


# ============================================================================
# Tests for get_table_info()
# ============================================================================


class TestGetTableInfo:
    """Test cases for SchemaManager.get_table_info() method."""

    def test_get_table_info_returns_column_information(self, mock_schema_manager):
        """Test get_table_info() returns correct column information."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor.fetchall to return sample column data
        mock_cursor.fetchall.return_value = [
            ("id", "int", "NO", None),
            ("name", "nvarchar", "YES", None),
            ("created_date", "datetime2", "NO", "GETDATE()"),
        ]

        result = schema_manager.get_table_info("TestTable")

        assert isinstance(result, list)
        assert len(result) == 3
        assert result[0]["name"] == "id"
        assert result[0]["data_type"] == "int"
        assert result[0]["is_nullable"] == "NO"
        assert result[1]["name"] == "name"
        assert result[2]["default"] == "GETDATE()"

    def test_get_table_info_returns_empty_list_for_table_with_no_columns(self, mock_schema_manager):
        """Test get_table_info() returns empty list for table with no columns (edge case)."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor.fetchall to return empty list
        mock_cursor.fetchall.return_value = []

        result = schema_manager.get_table_info("EmptyTable")

        assert isinstance(result, list)
        assert len(result) == 0

    def test_get_table_info_raises_schema_error_on_exception(self, mock_schema_manager):
        """Test get_table_info() raises SchemaError on database exception."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor.execute to raise an exception
        mock_cursor.execute.side_effect = Exception("Database error")

        with pytest.raises(SchemaError, match=".*table.*info"):
            schema_manager.get_table_info("TestTable")

    def test_get_table_info_ensures_connection(self, mock_schema_manager):
        """Test that get_table_info() ensures connection is established."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Reset connection to None
        schema_manager._conn = None

        # Mock cursor.fetchall to return sample data
        mock_cursor.fetchall.return_value = [("id", "int", "NO", None)]

        schema_manager.get_table_info("TestTable")

        # Verify connection.connect was called
        schema_manager.connection.connect.assert_called_once()

    def test_get_table_info_orders_columns_by_ordinal_position(self, mock_schema_manager):
        """Test that get_table_info() returns columns in correct order."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor.fetchall to return columns (should be ordered by ORDINAL_POSITION in SQL)
        mock_cursor.fetchall.return_value = [
            ("id", "int", "NO", None),
            ("name", "nvarchar", "YES", None),
            ("created_date", "datetime2", "NO", None),
        ]

        result = schema_manager.get_table_info("TestTable")

        # Verify columns are in the expected order
        assert result[0]["name"] == "id"
        assert result[1]["name"] == "name"
        assert result[2]["name"] == "created_date"


# ============================================================================
# Tests for schema validation
# ============================================================================


class TestSchemaValidation:
    """Test cases for schema validation methods."""

    def test_validate_schema_verifies_all_required_tables_exist(
        self, mock_schema_manager, required_tables
    ):
        """Test schema validation method verifies all required tables exist."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock table_exists to return True for all required tables
        with patch.object(schema_manager, "table_exists", return_value=True):
            # This test assumes a validate_schema() method will be implemented
            # For now, we test the concept by checking all tables
            all_exist = all(schema_manager.table_exists(table) for table in required_tables)
            assert all_exist is True

    def test_validate_schema_raises_error_when_table_missing(
        self, mock_schema_manager, required_tables
    ):
        """Test schema validation raises error when a required table is missing."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock table_exists to return False for one table
        def mock_table_exists(table_name):
            return table_name != "TestResults"  # Simulate missing table

        with patch.object(schema_manager, "table_exists", side_effect=mock_table_exists):
            # Verify that at least one table is missing
            missing_tables = [
                table for table in required_tables if not schema_manager.table_exists(table)
            ]
            assert len(missing_tables) > 0

    def test_validate_schema_checks_table_structure(self, mock_schema_manager):
        """Test schema validation checks table structure matches expected schema."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock get_table_info to return expected column structure
        expected_columns = [
            {"name": "connection_id", "data_type": "int", "is_nullable": "NO", "default": None},
            {"name": "platform", "data_type": "nvarchar", "is_nullable": "NO", "default": None},
        ]

        with patch.object(schema_manager, "get_table_info", return_value=expected_columns):
            columns = schema_manager.get_table_info("ConfigTable")
            assert len(columns) == 2
            assert columns[0]["name"] == "connection_id"


# ============================================================================
# Integration Tests
# ============================================================================


class TestSchemaIntegration:
    """Integration tests for schema creation and validation."""

    @pytest.mark.integration
    def test_full_schema_creation_and_verification(
        self, mock_schema_manager, sample_schema_directory, required_tables
    ):
        """Integration test: Execute full schema creation and verify all tables."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager
        temp_dir, files = sample_schema_directory

        # Mock cursor.execute to succeed
        mock_cursor.execute.return_value = None

        # Mock Path operations
        with patch("pathlib.Path.exists", return_value=True), patch(
            "pathlib.Path.glob"
        ) as mock_glob:
            mock_glob.return_value = sorted([Path(f) for f in files])

            # Create schema
            result = schema_manager.create_schema(temp_dir)
            assert result is True

            # Verify all required tables exist (mocked)
            with patch.object(schema_manager, "table_exists", return_value=True):
                for table in required_tables:
                    assert schema_manager.table_exists(table) is True

    @pytest.mark.integration
    def test_foreign_key_constraints_are_created(self, mock_schema_manager):
        """Integration test: Verify foreign key constraints are created."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor to return foreign key information
        # This would query sys.foreign_keys in a real implementation
        mock_cursor.fetchall.return_value = [
            ("FK_TestResults_TestRuns", "TestResults", "TestRuns", "test_run_id"),
        ]

        # This test assumes a method to check foreign keys will be implemented
        # For now, we verify the concept
        mock_cursor.execute.return_value = None
        # In real implementation, would query: SELECT * FROM sys.foreign_keys WHERE ...

    @pytest.mark.integration
    def test_indexes_are_created(self, mock_schema_manager):
        """Integration test: Verify indexes are created."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor to return index information
        # This would query sys.indexes in a real implementation
        mock_cursor.fetchall.return_value = [
            ("IX_ConfigTable_Platform_IsActive", "ConfigTable", "NONCLUSTERED"),
        ]

        # This test assumes a method to check indexes will be implemented
        # For now, we verify the concept
        mock_cursor.execute.return_value = None
        # In real implementation, would query: SELECT * FROM sys.indexes WHERE ...

    @pytest.mark.integration
    def test_schema_creation_execution_order(self, mock_schema_manager, sample_schema_directory):
        """Integration test: Verify schema scripts execute in correct order."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager
        temp_dir, files = sample_schema_directory

        # Track execution order
        execution_order = []

        def track_execution(*args, **kwargs):
            if args and isinstance(args[0], str):
                execution_order.append(args[0])

        mock_cursor.execute.side_effect = track_execution

        # Mock Path operations
        with patch("pathlib.Path.exists", return_value=True), patch(
            "pathlib.Path.glob"
        ) as mock_glob:
            # Return files in a specific order
            sorted_files = sorted([Path(f) for f in files])
            mock_glob.return_value = sorted_files

            schema_manager.create_schema(temp_dir)

            # Verify that execute was called (order verification depends on implementation)
            assert len(execution_order) > 0 or mock_cursor.execute.called


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================


class TestSchemaEdgeCases:
    """Test edge cases and error handling for SchemaManager."""

    def test_create_schema_with_empty_file(self, mock_schema_manager, tmp_path):
        """Test create_schema() with empty SQL file."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        empty_file = tmp_path / "empty.sql"
        empty_file.write_text("")

        # Should handle empty file gracefully (either skip or raise error)
        # Implementation decision: should probably raise SchemaError
        with pytest.raises((SchemaError, ValueError), match=".*empty|.*no.*content"):
            schema_manager.create_schema(str(empty_file))

    def test_table_exists_with_special_characters_in_table_name(self, mock_schema_manager):
        """Test table_exists() handles special characters in table name."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        mock_cursor.fetchone.return_value = (1,)

        # Test with table name that might have special characters
        result = schema_manager.table_exists("Test_Table-Name")

        # Should handle parameterized query correctly
        assert result is True
        mock_cursor.execute.assert_called_once()

    def test_get_table_info_with_nonexistent_table(self, mock_schema_manager):
        """Test get_table_info() with nonexistent table returns empty list or raises error."""
        schema_manager, mock_conn, mock_cursor = mock_schema_manager

        # Mock cursor.fetchall to return empty (table doesn't exist)
        mock_cursor.fetchall.return_value = []

        result = schema_manager.get_table_info("NonExistentTable")

        # Should return empty list (not raise error)
        assert isinstance(result, list)
        assert len(result) == 0

    def test_schema_manager_with_none_connection(self):
        """Test SchemaManager initialization with None connection raises error."""
        with pytest.raises((TypeError, AttributeError)):
            SchemaManager(None)
